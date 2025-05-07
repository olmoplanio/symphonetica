import fontforge
import os

# Get the currently open font
font = fontforge.activeFont()
if font is None:
    raise ValueError("No active font is open in FontForge. Please open a font before running the script.")

# Extract the original font name (without extension)
original_font_name = os.path.splitext(font.fontname)[0]
new_font_name = f"{original_font_name}_marks.sfd"

# Define the range of mark glyphs
glyph_ranges = range(768, 879)

# Loop through the specified glyphs
for i in glyph_ranges:
    # Check if the glyph exists in the font
    if i not in font:
        print(f"Skipping glyph {i} (not present in font)")
        continue

    glyph = font[i]  # Get the glyph safely

    # Skip if the glyph has no contours and no references
    if (not glyph.foreground or len(glyph.foreground) == 0) and not glyph.references:
        print(f"Skipping empty glyph: {i}")
        continue

    # Initialize bounding box values
    x_min, y_min, x_max, y_max = None, None, None, None

    if glyph.references:
        # Process composite glyphs by considering all referenced components
        for ref in glyph.references:
            ref_name = ref[0]  # The referenced glyph name
            transform = ref[1]  # The affine transformation matrix

            ref_glyph = font[ref_name]  # Get the referenced glyph
            rx_min, ry_min, rx_max, ry_max = ref_glyph.boundingBox()

            # Ensure transform contains six values (FontForge affine matrix)
            if len(transform) == 6:
                dx, dy = transform[4], transform[5]  # Extract X and Y translation
            else:
                dx, dy = 0, 0  # Default to no shift if transform is incorrect

            # Apply translation to referenced bounding box
            rx_min += dx
            ry_min += dy
            rx_max += dx
            ry_max += dy

            # Expand bounding box to include transformed reference
            x_min = min(x_min, rx_min) if x_min is not None else rx_min
            y_min = min(y_min, ry_min) if y_min is not None else ry_min
            x_max = max(x_max, rx_max) if x_max is not None else rx_max
            y_max = max(y_max, ry_max) if y_max is not None else ry_max
    else:
        # Process normal (non-referenced) glyphs
        x_min, y_min, x_max, y_max = glyph.boundingBox()

    # Calculate the actual average x-position of the bounding box
    x_position = (x_min + x_max) / 2  # Actual center of the bounding box

    # Set the width of the glyph to 2 * x_position (as an integer)
    glyph.width = int(2 * x_position)

    # Add top anchor if y_min is greater than 250
    if y_min > 250:
        glyph.addAnchorPoint("top", "mark", int(x_position), int(y_min))

    # Add bottom anchor if y_max is less than 250
    if y_max < 250:
        glyph.addAnchorPoint("bottom", "mark", int(x_position), int(y_max))

# Save the modified font with the new name
font.save(new_font_name)

print(f"Mark anchors added successfully, glyph widths updated, and saved as {new_font_name}!")

import fontforge
import os

# Get the currently open font
font = fontforge.activeFont()
if font is None:
    raise ValueError("No active font is open in FontForge. Please open a font before running the script.")

# Extract the original font name (without extension)
original_font_name = os.path.splitext(font.fontname)[0]
new_font_name = f"{original_font_name}_anchors.sfd"

# Define the glyph ranges
glyph_ranges = list(range(98, 123)) + list(range(592, 672))  # Merging ranges

# Loop through the specified glyphs
for i in glyph_ranges:
    # Check if the glyph exists in the font
    if i not in font:
        print(f"Skipping glyph {i} (not present in font)")
        continue    
    
    glyph = font[i]

    # Skip if the glyph is empty (has no contours)
    if not glyph.foreground or len(glyph.foreground) == 0:
        print(f"Skipping empty glyph: {i}")
        continue

    # Get the actual glyph width
    glyph_width = glyph.width
    x_median = glyph_width / 2  # Middle of the glyph width

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
    
    
    lowest_y = 250
    highest_y = 150
    
    
    closest_high_distance = float("inf")
    closest_low_distance = float("inf")

    # Iterate through contours and their points
    for contour in glyph.foreground:
        prev_x, prev_y = None, None  # To track the previous point

        for point in contour:
            x, y = point.x, point.y  # Get coordinates of the current point

            # If we have a previous point, check if we crossed x_median
            if prev_x is not None:
                if (prev_x < x_median and x > x_median) or (prev_x > x_median and x < x_median):
                    # Calculate the interpolation ratio
                    ratio = (x_median - prev_x) / (x - prev_x)
                    interpolated_y = prev_y + ratio * (y - prev_y)

                    # Calculate the distance of this crossing from x_median
                    distance = abs(x - x_median)

                    # Update highest crossing
                    if interpolated_y > (highest_y if highest_y is not None else float("-inf")):
                        highest_y = interpolated_y
                        closest_high_distance = distance

                    # Update lowest crossing
                    if interpolated_y < (lowest_y if lowest_y is not None else float("inf")):
                        lowest_y = interpolated_y
                        closest_low_distance = distance

            # Update previous point for the next iteration
            prev_x, prev_y = x, y

    # If no valid crossing points were found, skip the glyph
    if highest_y is None or lowest_y is None:
        top_y = y_max + 1
        bottom_y = y_min - 1

    # Calculate the positions for the anchors
    top_y = highest_y + 1
    bottom_y = lowest_y - 1

    # Add the anchors as "base" type
    glyph.addAnchorPoint("top", "base", x_median, top_y)      # Top anchor
    glyph.addAnchorPoint("bottom", "base", x_median, bottom_y)  # Bottom anchor
    glyph.addAnchorPoint("center", "base", x_median, 200)  # Center anchor

# Save the modified font with the new name
font.save(new_font_name)

print(f"Anchors added successfully to non-empty glyphs and saved as {new_font_name}!")

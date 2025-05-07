import fontforge
import re
import sys

# Prompt user for intervals file and output file name
intervals_path = "../scripts/intervals.txt"  # Modify as needed
output_path = "symphonetica-43543.sfd"  # Modify as needed

if not intervals_path or not output_path:
    print("Error: Intervals file or output file name not provided.")
    sys.exit(1)

# Parse intervals from the file, ignoring comments and empty lines
def parse_intervals(file_path):
    intervals = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):  # Skip empty lines and comments
                continue
            line = line.split("#")[0].strip()  # Remove inline comments
            match = re.match(r"([0-9A-Fa-f]+)-([0-9A-Fa-f]+)", line)
            if match:
                start, end = map(lambda x: int(x, 16), match.groups())
                intervals.append((start, end))
    return intervals

intervals = parse_intervals(intervals_path)
print(f"Parsed intervals: {intervals}")

# Get the active font
font = fontforge.activeFont()
if not font:
    print("Error: No active font found.")
    sys.exit(1)

# Collect glyph names to keep based on intervals
glyphs_to_keep = set()
for start, end in intervals:
    for codepoint in range(start, end + 1):
        if codepoint in font:
            glyph = font[codepoint]
            if glyph is not None and glyph.glyphname:
                glyphs_to_keep.add(glyph.glyphname)

print(f"Glyphs to keep: {glyphs_to_keep}")

# Collect all glyph names in the font
all_glyph_names = {glyph.glyphname for glyph in font.glyphs()}

# Determine glyphs to remove
glyphs_to_remove = all_glyph_names - glyphs_to_keep
print(f"Glyphs to remove: {glyphs_to_remove}")

# Remove specified glyphs
for glyph_name in glyphs_to_remove:
    if glyph_name in font:
        font.removeGlyph(glyph_name)
        print(f"Removed glyph: {glyph_name}")


# Save the cleaned-up font
font.save(output_path)
print(f"Font saved successfully as '{output_path}'")

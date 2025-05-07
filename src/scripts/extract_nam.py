# FontForge script to extract a .nam-style file from the active font
import fontforge

font = fontforge.activeFont()
if font is None:
    raise RuntimeError("No active font. Open a font first in FontForge.")

output_filename = font.fontname + ".nam"

with open(output_filename, "w", encoding="utf-8") as f:
    for glyph in font.glyphs():
        # The second encoding value is stored in glyph.unicode
        unicode_val = glyph.unicode
        if unicode_val < 0:
            continue  # Skip unencoded glyphs
        hexcode = f"0x{unicode_val:04X}"
        name = glyph.glyphname
        f.write(f"{hexcode} {name}\n")

print(f".nam file written to {output_filename}")

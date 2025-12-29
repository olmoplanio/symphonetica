import fontforge

# Define the anchor points you want to ignore
common_anchors = {"TopRight", "Top", "Middle", "Bottom", "HigherTop", "HigherTopRight", "HigherTopLeft", "TopLeft", "Top2"}

# Dictionary: anchor name -> set of glyph names where it's used
anchor_usage = {}

font = fontforge.activeFont()

if font is None:
    print("No font is open.")
else:
    for glyph in font.glyphs():
        for anchor in glyph.anchorPoints:
            name = anchor[0]
            if name not in common_anchors:
                if name not in anchor_usage:
                    anchor_usage[name] = set()
                anchor_usage[name].add(glyph.glyphname)

    # Save the results to a file
    with open("anchors.txt", "w", encoding="utf-8") as f:
        if anchor_usage:
            f.write("Anchor points used in the font (excluding common ones):\n\n")
            for name in sorted(anchor_usage.keys()):
                glyph_list = sorted(anchor_usage[name])
                f.write(f"- {name} (used in {len(glyph_list)} glyphs):\n")
                for glyph_name in glyph_list:
                    f.write(f"    • {glyph_name}\n")
                f.write("\n")
        else:
            f.write("No unusual anchor points found.\n")

    print("Anchor list saved to anchors.txt.")

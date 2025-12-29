import fontforge

font = fontforge.activeFont()

code_point = 0x131CB

if code_point not in font:
    glyph = font.createChar(code_point)
    glyph.glyphname = "M17"

import fontforge  # type: ignore
import os
import sys
import shutil

input_dir = sys.argv[1] if len(sys.argv) > 1 else "src"
output_dir = sys.argv[2] if len(sys.argv) > 2 else "bin"

input_dir = os.path.abspath(input_dir)
output_dir = os.path.abspath(output_dir)

print(f"📁 Input directory:  {input_dir}")
print(f"📂 Output directory: {output_dir}")
os.makedirs(output_dir, exist_ok=True)

# Font definitions: (input file, output base name, namelist file or None)
fonts_to_build = [
    ("Laudosia-Regular.sfd", "Laudosia-Regular", "Laudosia.nam"),
    ("Laudosia-Literal.sfd", "Laudosia-Literal", "Laudosia.nam"),
    ("Hibis-Hiero.sfd", "Hibis-Hiero", "Kemic.nam"),
    ("Hibis-Demotic.sfd", "Hibis-Demotic", "Kemic.nam"),
]

used_namelists = set()

for input_file, output_name, namelist_filename in fonts_to_build:
    input_path = os.path.join(input_dir, input_file)

    if not os.path.exists(input_path):
        print(f"❌ File not found: {input_path}")
        continue

    print(f"🔧 Opening {input_file}")
    font = fontforge.open(input_path)

    if namelist_filename:
        namelist_path = os.path.join(input_dir, namelist_filename)
        if os.path.exists(namelist_path):
            print(f"🔤 Loading NameList: {namelist_path}")
            fontforge.loadNamelist(namelist_path)
            used_namelists.add(namelist_filename)
        else:
            print(f"⚠️  NameList not found: {namelist_path} — skipping")

    fonts_dir = os.path.join(output_dir, "fonts")
    os.makedirs(fonts_dir, exist_ok=True)
    ttf_path = os.path.join(fonts_dir, f"{output_name}.ttf")
    otf_path = os.path.join(fonts_dir, f"{output_name}.otf")
    woff2_path = os.path.join(fonts_dir, f"{output_name}.woff2")

    font.generate(ttf_path)
    font.generate(otf_path)
    font.generate(woff2_path)

    print(f"✅ Compiled {input_file} →")
    print(f"  • {ttf_path}")
    print(f"  • {otf_path}")
    print(f"  • {woff2_path}")

    del font

# Copy each used namelist to the output directory
for namelist in used_namelists:
    src = os.path.join(input_dir, namelist)
    dst = os.path.join(output_dir, namelist)
    if os.path.exists(src):
        shutil.copy(src, dst)
        print(f"✅ Copied {namelist} to output directory")

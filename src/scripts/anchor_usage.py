import fontforge
import os
import traceback
from collections import defaultdict

def log_to_file(message, filename="fontforge_output.log"):
    """Universal logging function for FontForge scripts"""
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{message}\n")

def main():
    log_file = "script_results.txt"
    
    try:
        font = fontforge.activeFont()
        log_to_file(f"Processing font: {font.fontname}", log_file)

        # Dictionary: anchor_name → role → set of glyphnames
        anchor_usage = defaultdict(lambda: defaultdict(set))

        for glyph in font.glyphs():
            try:
                if glyph.anchorPoints:
                    for anchor in glyph.anchorPoints:
                        name, anchor_type, x, y = anchor
                        anchor_usage[name][anchor_type].add(glyph.glyphname)
            except Exception as gex:
                log_to_file(f"Error reading glyph '{glyph.glyphname}': {str(gex)}", log_file)

        # Compute total usage for sorting
        sorted_anchors = sorted(
            anchor_usage.items(),
            key=lambda item: sum(len(glyphs) for glyphs in item[1].values()),
            reverse=True
        )

        # Format report
        anchor_report = ["Anchor Usage Report (sorted by total occurrences):"]
        for anchor_name, roles in sorted_anchors:
            total = sum(len(glyphs) for glyphs in roles.values())
            anchor_report.append(f"\nAnchor: {anchor_name} (Total: {total})")
            for role in sorted(roles.keys()):
                anchor_report.append(f"  {role}: {len(roles[role])} glyph(s)")

        log_to_file("\n".join(anchor_report), log_file)

    except Exception as e:
        error_msg = f"Error: {str(e)}\n{traceback.format_exc()}"
        log_to_file(error_msg, log_file)
    finally:
        fontforge.logWarning(f"Script complete. Results saved to:\n{os.path.abspath(log_file)}")

if __name__ == "__main__":
    main()

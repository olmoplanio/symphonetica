import fontforge
import os

# Configurazione
font = fontforge.activeFont()
output_file = os.path.join(os.getcwd(), "anchor_census.txt")

# Dizionario per tracciare gli anchor point
anchor_registry = {}

# Scansione di tutti i glifi
for glyph in font.glyphs():
    for anchor in glyph.anchorPoints:
        anchor_name, anchor_type, x, y = anchor[:4]
        
        # Inizializza se non esiste
        if anchor_name not in anchor_registry:
            anchor_registry[anchor_name] = {
                'base': [],
                'mark': [],
                'type': anchor_type.lower()
            }
        
        # Aggiorna la lista appropriata
        if anchor_type.lower() == 'base':
            anchor_registry[anchor_name]['base'].append(glyph.glyphname)
        elif anchor_type.lower() == 'mark':
            anchor_registry[anchor_name]['mark'].append(glyph.glyphname)

# Scrittura del file di output
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("CENSIMENTO ANCHOR POINT\n")
    f.write("======================\n\n")
    
    for anchor in sorted(anchor_registry.keys()):
        base_list = sorted(anchor_registry[anchor]['base'])
        mark_list = sorted(anchor_registry[anchor]['mark'])
        
        f.write(f"ANCHOR: {anchor} ({anchor_registry[anchor]['type']})\n")
        f.write(f"Base in: {', '.join(base_list) if base_list else 'Nessuno'}\n")
        f.write(f"Mark in: {', '.join(mark_list) if mark_list else 'Nessuno'}\n")
        f.write("-"*50 + "\n\n")

print(f"Censimento generato: {output_file}")

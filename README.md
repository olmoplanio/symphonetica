# Symphonetica - Transcription system and fonts

## About

Symphonetica is a font and a transcription specification and method based on the International Phonetic Alphabet (IPA), designed to solve the readability, inconsistency and regionality problems present in standard IPA.
Inspired by Luciano Canepari's Natural Phonetics and canIPA, Symphonetica provides a balanced and readable approach to phonetic transcription while maintaining Unicode compatibility.

See the site at [olmoplanio.github.io/symphonetica](https://olmoplanio.github.io/symphonetica).

## Key Features

- Unicode Compatibility: glyphs map to standard Unicode code points, referring to Official IPA or other phonetic methods;
- Fallback Readability: glyphs degrade to readable text even when the font is not available;
- Balanced Design: asymmetry (e.g. the position of [ɪ]), readability (e.g. tonemes and diacritics), and regionality (e.g. the position of [a]) are resolved;
- Extended Symbol Set: additional phonetic symbols not available in standard IPA to be used consistently across different languages and dialects;
- Open Source: Released under GNU GPL license

## Transcription System

- Symphonetica introduces a transcription system that:
- Maintains compatibility with Unicode
- Repurposes obsolescent or inconsistent phonetic symbols of IPA
- Balances the system to pursue generalization
- Ensures readability even when the font is not available

## Fonts in the Symphonetica System

The system includes four fonts, designed for precision and typographic elegance:

- **Laudosia Regular**  
  A high-legibility font for English text and natural phonetic transcription, able to fallback to Unicode.
  Suitable for body text in academic work.

- **Laudosia Literal**  
  A stylistically distinct companion to Laudosia Regular, intended for quoting **Latin, Greek, Coptic, and other alphabetic** script sources. Maintains philological neutrality while remaining typographically harmonious.

- **Hibis Hiero**  
  A specialized font based on **Noto Sans Hieroglyphic**, extended with phonologically **ad hoc signs** for Ancient Egyptian. Tailored for phonological and diachronic analysis using hieroglyphs.
  Example: 〈𓆑𓈖𓆓𓂉𓎡𓅓𓃥𓇋𓐍𓅓𓋴𓎡⟩ ‹fnḏ⸗k m zꜣb jḫm-sk› «your nose is the jackal, (you) non-sinking one».

- **Hibis Demotic**  
  A custom-designed font for the **Demotic script**, built for typographic use in linguistic and historical publications. Includes additional signs needed for accurate transcription and analysis.
  Set RTL direction for relevant blocks (`U+202E` and `U+202C`).
  Example: 〈[‮𓇋𓋴𓏏𓄟𓋴𓀔𓅱𓈖𓈙𓄛𓋴𓌶𓀢𓀁𓉐𓏤𓎟𓏏‬]⟩ ‹ỉw⸗s msi̯ wnš smꜣꜥ pr nb› «when a jackal is born, it blesses every house».
  
## Format and Usage

Fonts are provided in **TrueType (TTF)**, **OpenType (OTF)** and **Web Open Font Format (WOFF2)** formats, ready for use in digital publications, typesetting environments, and academic documentation.

## License

All fonts in the Symphonetica project are distributed under the  
[SIL Open Font License (OFL)](https://scripts.sil.org/OFL),  
allowing free use, modification, and redistribution for both academic and commercial purposes, with attribution.

# POC data
Blind transcriptions from the 20-page proof of concept (PDF pages 9, 10, 17, 18, 20), written from images only, in the POC's old markup (no `@L`; later-layer marks use plain `~~ ~~` and `^ ^`).
- `blind-opus/`: Opus with the spelling rules. `blind-sonnet/`: Sonnet with the rules (pages 9, 10). `opus-glossary/`: Opus with a glossary added to the prompt (pages 17, 18, 20; no gain).
- `poc_compare_jsp.py`: the POC comparison script (maps PDF page n to JSP page n-5; superseded by `tools/compare_reference.py`).
Use as a regression set: re-run a candidate prompt/model on these pages blind and compare against JSP with `tools/compare_reference.py --map 9:4,10:5,17:12,18:13,20:15`. The POC's other 15 page files are not included because they were corrected after seeing JSP differences and are no longer blind.

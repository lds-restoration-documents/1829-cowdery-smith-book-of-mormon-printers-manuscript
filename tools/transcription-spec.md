# Transcription spec: Printer's Manuscript of the Book of Mormon (1829-30)

Instructions for transcribing agents. Source: `source-images/` (468 photos of single leaves, ~2000 px wide, no text layer). Files are keyed to the **page number** = position in `source-images/manifest.tsv` (3 digits; 1 = `_000`, 2 = `_000-01`, ..., 5 = `_001`; see `prepare_bands.py --list`): `book-of-mormon-printers-manuscript-pages/page-NNN.md`.
Inputs for PDF page N: `work/img/pNNN_B.jpg`, overlapping bands from `tools/prepare_bands.py` (~120 px overlap; do not duplicate lines). View **every** band with Read before writing. If an image fails, stop and report the page; never transcribe unseen, never from memory.

## The manuscript (JSP source note)
Copied by Oliver Cowdery, an unknown scribe ("scribe 2") and Hyrum Smith, ca. Aug 1829 to Jan 1830, from the original dictated manuscript, for the Palmyra typesetters. Most pages have **37 ruled lines**. Pages are numbered by the scribes themselves (Cowdery: upper right on recto, upper left on verso; Hyrum and scribe 2: upper left on both); the title/copyright leaf, the preface leaf and the first leaf are unnumbered. It carries three layers:
1. **Original inscription** (the base text), including the scribe's own same-ink strikes and insertions.
2. **Added punctuation and pilcrows** (the 1830 compositor John H. Gilbert, pencil, occasionally ink; some dark-ink punctuation may be the 1837 hand, so we tag by ink, not by author): transcribe as `{mark}@pencil` (grey pencil) or `{mark}@ink` (dark ink), see Rules. **PILOT:** best-effort layer, unverified. Do not transcribe capitals traced over; note them in the page comment.
3. **1837 emendations** (Joseph Smith, preparing the second edition; darker ink): e.g. `which`->`who`, `saith`->`said`, `was`->`were`, added `should be`.

## Rules (diplomatic transcription)
- **Write the letters the scribe wrote**, never what you think it should say: no correction from memory, printed editions, the KJV or other manuscripts. This applies above all to **spelling**: the first POC pass silently modernised ~100 words (`exceding`->`exceeding`, `haveing`->`having`, `presance`->`presence`, `destroid`->`destroyed`, `angery`->`angry`). Typical scribe forms: `-eing` (`haveing`, `makeing`), `exceding`, `presance`, `desireous`, `vally`, `journied`, `treasuary`, `scorge`, `shold`. Decide letter by letter. (A glossary in the prompt did not help; do not rely on one.)
- The scribe's `r` often looks like `n` (`after`, `often`): decide by the letters, then by sense. `u`/`n`, `e`/`o` can look alike.
- One output line per manuscript line (keep the scribe's line breaks). The page files in the repo have a blank line between lines so Markdown renders them one per paragraph (`python3 tools/space_page_lines.py` adds them; agents may write the lines tight or spaced, and every tool ignores blank lines). A word split at a line end without a hyphen is split as on the page (`La` / `ban`); write a hyphen only if one is written. Run-together words stay run together (`somuch`, `inthewhich`).
- `&` is written as `&`. Capitals as written (the scribe's large `C` mid-sentence: `Came`, `Commanded`, `Cast`).
- **No punctuation is added**; only what the scribe wrote (dashes and flourishes in headings: describe in a comment; never write them with `~`, which is the strike mark). The exception is the compositor's own marks (layer 2), which you record only when you can actually see them on the page, never from the sense or from memory of the printed text: `said{,}@pencil` (a pencil comma after `said`), `{.}@pencil`, `{;}@ink` (a dark-ink semicolon), `{¶}@pencil` (pilcrow, at the place where it is drawn). The suffix is the **ink you see**: `@pencil` for grey graphite, `@ink` for any pen ink; never guess an author or date for punctuation. Braces mean an added mark, not a word; put them where the mark sits. An unclear faint mark: leave it out. **Every** added mark carries `{…}@pencil` or `{…}@ink`; never write a bare punctuation mark for one (a bare mark would read as the scribe's own). Look for pilcrows (`¶`, a pencil P-shaped mark between sentences) as well as commas. If a mark and a word's position conflict, the word's position wins: place braces after the word the mark follows, and never move a scribe's `^insertion^` to fit a mark. Do not tag the scribe's own pen punctuation, which is in the scribe's usual brown ink and is written as plain text; if a mark in brown ink could be either, write it plain and add `<!-- uncertain: scribe or added -->`.
- **Strikes and insertions.** Scribe layer: struck text `~~word~~` (if legible; else `~~[illegible]~~`), inserted text above the line `^word^`, overwritten letters: best reading + `<!-- uncertain: overwrite -->`. **Later layer: add a dated suffix** to the mark: `@1837` for darker-ink emendations (Joseph Smith, 1837), `@1830` for a change to the words by the compositor (pencil or ink), `@later` when you cannot tell which layer. Example: `~~which~~@1837 ^who^@1837`. Struck words are part of the base text; read them (they matter: omitting a struck word was a common error). A struck word that is truly unreadable is `~~[illegible]~~`.
- Doubtful reading: best guess + terse `<!-- uncertain: ... -->`. Unreadable: `[illegible]`. Text lost at a torn or clipped edge: `[...]`, never completed from memory.
- Other hands, pencil, stamps, library marks, stains: HTML comment only. Folio number: `<!-- folio N -->`; unnumbered leaf: `<!-- folio none -->`. Name the scribe if you can tell (`<!-- hand: Cowdery -->`), else omit.
- No commentary, summaries or modern corrections in the text. Keep comments short (output tokens are the expensive part).

## Format
```
<!-- image NNN -->
<!-- folio N; hand/condition notes -->
line 1
line 2
...
```
A blank leaf: the image comment plus `<!-- blank leaf -->` (then a `<!-- folio none; ... -->` condition note if useful).
**Front matter (pages 1-4: title page with the copyright entry, blank, preface, blank; unnumbered):** not ruled continuous text, so the 37-line rule does not apply. Keep the scribe's line breaks and transcribe by the same rules; mark the folio `<!-- folio none -->`; describe headings, braces, flourishes and signature lines in comments only. Where the leaf holds two texts (title page above, copyright entry below), put one comment line between them (`<!-- gap; copyright entry follows -->`) and no blank line.

## Run notes
- One agent per page (or two), fresh context; **view each band exactly once, in order**: no re-viewing, cropping or zooming, except one extra look at a specific unreadable word. Write the file with a single Write call and do not re-read it. View the 4-5 bands, write the file, final reply one line (file, line count, failed bands). Never paste the transcription in the reply.
- Use **Opus** for transcription: in the POC it was ahead of or level with Sonnet on every page tested (0-8 fewer differing words per 600), at about the same tokens per page (~45k).
- Blind second reads must not see the first transcription (see proofread-spec.md).

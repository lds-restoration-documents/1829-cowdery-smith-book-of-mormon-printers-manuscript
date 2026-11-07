# 1829 Cowdery & Smith Book of Mormon Printer's Manuscript
[Markdown](#what-is-markdown) & Plain Text extractions of the content of the handwritten Printer's Manuscript of the Book of Mormon, copied by Oliver Cowdery, Hyrum Smith and one other scribe from the original dictated manuscript between August 1829 and January 1830 for the typesetters in Palmyra, New York. Because the manuscript carries later changes in other hands, the text is offered in **layers**, from the scribes' first writing to the manuscript with its 1837 emendations applied. Extracted using AI.

## Files
Each layer is a separate text and each includes the layers before it. All files are about 274,000 words.

| Files | Layer | What it shows |
|---|---|---|
| [printers-⁠manuscript-⁠all-⁠layers.md](printers-manuscript-all-layers.md)<br>[printers-⁠manuscript-⁠all-⁠layers.txt](printers-manuscript-all-layers.txt) | **All layers** | Nothing applied: the scribes' own strikes and insertions, every later change with its tag, and the added punctuation, all inline |
| [printers-⁠manuscript-⁠first-⁠inscription.md](printers-manuscript-first-inscription.md)<br>[printers-⁠manuscript-⁠first-⁠inscription.txt](printers-manuscript-first-inscription.txt)<br>[printers-⁠manuscript-⁠first-⁠inscription-⁠sparse.txt](printers-manuscript-first-inscription-sparse.txt) | **First inscription** | The scribes' writing before any correction |
| [printers-⁠manuscript-⁠scribal-⁠corrections.md](printers-manuscript-scribal-corrections.md)<br>[printers-⁠manuscript-⁠scribal-⁠corrections.txt](printers-manuscript-scribal-corrections.txt)<br>[printers-⁠manuscript-⁠scribal-⁠corrections-⁠sparse.txt](printers-manuscript-scribal-corrections-sparse.txt) | **Scribal corrections** | + the scribes' own strikes and insertions applied |
| [printers-⁠manuscript-⁠compositor-⁠marks.md](printers-manuscript-compositor-marks.md)<br>[printers-⁠manuscript-⁠compositor-⁠marks.txt](printers-manuscript-compositor-marks.txt)<br>[printers-⁠manuscript-⁠compositor-⁠marks-⁠sparse.txt](printers-manuscript-compositor-marks-sparse.txt) | **Compositor's marks** | + the typesetter's added punctuation and pilcrows (pencil and ink) and a few word changes |
| [printers-⁠manuscript-⁠1837-⁠emendations.md](printers-manuscript-1837-emendations.md)<br>[printers-⁠manuscript-⁠1837-⁠emendations.txt](printers-manuscript-1837-emendations.txt)<br>[printers-⁠manuscript-⁠1837-⁠emendations-⁠sparse.txt](printers-manuscript-1837-emendations-sparse.txt) | **1837 emendations** | + the darker-ink word changes made for the 1837 edition |

* The `.md` files are [Markdown](#what-is-markdown) with YAML frontmatter (layer, source, method, status, version) and a `<!-- page NNN -->` comment where each image begins. The `.txt` files are the same text as plain text with a single `#` line (layer, status, link to this repository) and no page markers.
* The `-sparse.txt` files hold the Book of Mormon text only, from the first page of 1 Nephi to the end of Moroni. They leave out the title and copyright leaf, the preface and the witness testimonies, have no page markers, and join words that the scribe broke across lines. (Lines otherwise follow the manuscript lines.)
* [book-of-mormon-printers-manuscript-pages/](book-of-mormon-printers-manuscript-pages/): one [Markdown](#what-is-markdown) file per image of the scan (`page-001.md` to `page-468.md`). File numbers are image numbers, not folio numbers; the scribes' folio number is recorded in a comment in each file. These are the source of truth; the files above are generated from them.

## The layers
The manuscript has three layers of writing, which the files separate:
1. **The scribes' own text.** Their first writing, and their own corrections in the same ink: struck words and words inserted above the line. The *first inscription* file keeps the struck words and leaves out the insertions; the *scribal corrections* file removes the strikes and applies the insertions. Immediate corrections cannot be told apart from later proofreading by a scribe, so "scribal corrections" is the scribes' text as it stands, not necessarily the text as first delivered to the printer.
2. **The compositor's marks** (John H. Gilbert, 1830): added punctuation and pilcrows (¶), mostly in pencil and sometimes in ink, on about 40% of the pages. The scribes wrote almost no punctuation of their own. Only about a dozen word changes are tagged as the compositor's, so this layer is nearly all punctuation.
3. **The 1837 emendations** (Joseph Smith, for the second edition): words struck or added in darker ink, such as *which* to *who*, *saith* to *said* and *was* to *were*. This file is the manuscript with these emendations applied; it is not the printed 1837 edition.

In the all-layers files a later change carries a tag: `@1837` (darker-ink emendation), `@1830` (compositor's word change) or `@later` (the layer could not be told). In the Markdown file strikes are shown as ~~strikethrough~~, insertions as superscript and tags in square brackets; the text file keeps the page-file notation: `~~struck~~`, `^inserted^`, `{,}@pencil` for an added comma.

**Cautions about the layers:**
* Layers are told apart by ink, as seen in the photographs, not by a known hand. Punctuation is tagged pencil or ink; **ink punctuation is assigned to the compositor** because it rarely appears with the 1837 word changes, which is an inference.
* **About 400 marks tagged `@later` are applied in no layer** and appear only in the all-layers files. Most are single struck words ("that", "the", "they") whose ink could not be judged.
* Added punctuation and pencil marks are best-effort and **much thinner after about page 268**, so the compositor and 1837 layers are not even across the book.
* Where letters were written over others the files show the visible form, so the first inscription is not fully recoverable at those places (a few are `[illegible]` in that layer).

## What is in the manuscript
* **The scribes' spelling, capitalization and grammar are kept exactly as written** (*desending*, *destroid*, *procede*, *sayd*), with nothing corrected from the printed editions. Words are separated as the scribe separated them, including run-together words.
* **Lines are kept as written**: most pages have 37 ruled lines, one per line of text. A word broken at the end of a line is split, and the scribe's hyphen at the start of the next line (a hyphen opens the continuation line) is kept in the non-sparse files. The line-start hyphens were missed by the transcribing agents in many places and were patched afterwards, so some may still be missing.
* **No verse numbers, no chapter or paragraph division beyond the scribes' own headings.** Chapter headings are in the text, often with a flourish; at least one heading ("Chapter 1st" on page 5) was added later in another hand.
* `[illegible]` marks writing that is there but cannot be read; `[...]` marks text lost where the leaf is torn, clipped or worn (34 places on 20 pages). Neither is completed from the printed text.
* Pages 1 to 4 are the title and copyright leaf, a blank leaf, the preface and a blank leaf. Pages 466 to 468 are the end of Moroni and the testimonies of the Three and Eight Witnesses. Page 432 is a short leaf that ends the book before the Book of Ether, which begins on page 433.
* Not transcribed: capitals traced over by a later hand, library stamps, stains, and other hands' notes beyond a comment in the page file.

## Source
Transcribed from 468 photographs of the leaves (about 2000 pixels wide, taken in 2012) published by the [Joseph Smith Papers](https://www.josephsmithpapers.org/) as "Printer's Manuscript of the Book of Mormon, [ca. Aug. 1829–ca. Jan. 1830]", handwriting of Oliver Cowdery, an unidentified scribe ("scribe 2") and Hyrum Smith, held by the Church History Library of The Church of Jesus Christ of Latter-day Saints (acquired from the Community of Christ in 2017). The page images were downloaded with the [Archive Viewer](https://archiveviewer.org) tool and are not included in this repository. The images have no text layer. The Joseph Smith Papers online transcript holds only the original inscription, not the later changes; it was not shown to the transcribing agents, so expect differences from it where the later layers apply. The manuscript is 466 pages; two leaves, probably blank, are missing, and the images add the unnumbered title, copyright and preface leaves.

## What is Markdown?
Markdown is a simple way of writing formatted text using plain characters, such as `#` for headings and `*asterisks*` for *italics*. A Markdown file is still readable as ordinary text, and can also be displayed with formatting.
* Learn more at [markdown.org](https://markdown.org/).
* Tools for displaying, editing, or converting Markdown files: [https://markdown.org/tools/](https://markdown.org/tools/)

## Artificial Intelligence
Extracted with Claude Code from Anthropic. Each page was transcribed from overlapping crops of its photograph (there is no text layer or OCR) by a fresh Claude Opus agent, one page per agent, with at most three agents at a time. Scripts then checked each page file for structure (line count, folio comment, balanced marks) and flagged spellings that may have been modernized. Two kinds of misses were found in the first pass and patched: modernized spellings and missing line-start hyphens (a patch on pages 5–94 and a by-eye check of the left margins on about 35 pages). A second blind read of pages 7, 8, 11 and 13, compared word by word against the first, found about 5 differences per 600 words, four of them real first-pass errors in the four pages.

**This is an AI transcription. Apart from those four pages it has had no second read and no human proofread.** The text is meant to show what the page shows, including later hands, but the layer tags, added punctuation and hyphens are best-effort. The most likely places for an error are overwritten and struck words, faint pencil, the layer of a change, line-start hyphens and the scribes' folio numbers. For anything that matters, check the images.

**Status: all 468 images are transcribed and structure-checked; pages 7, 8, 11 and 13 have been proofread blind. The next step is a second blind read of the pages with the most strikes, uncertain readings and later-layer marks, plus a random sample of the rest, with an ink-color check of the layer tags.** 
These files record how it was made and checked:

* [transcription-notes.md](transcription-notes.md): the sources, conventions and review status, batch by batch.
* [docs/](docs/): the 20-page proof of concept that set the method ([poc-findings.md](docs/poc-findings.md)), a note on the Joseph Smith Papers edition ([jsp-source-note.md](docs/jsp-source-note.md)), and [open questions](docs/open-questions.md).
* [tools/README.md](tools/README.md): the transcription and checking pipeline.

## Rebuilding the combined files
```
python3 tools/make_outputs.py       # the 14 layered files above, plus work/outputs-report.txt
python3 tools/compile.py --layer first|scribal|compositor|1837|full --format md|txt [--sparse] --out FILE
python3 tools/check_structure.py    # mechanical checks of the page files
```
See [tools/README.md](tools/README.md) for the full pipeline.

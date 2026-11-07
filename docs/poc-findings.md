# Test-page transcription vs. Joseph Smith Papers (JSP) transcript

Method: `tools/compare_jsp.py` aligns our 20 page files with the JSP text (extracted from the JSP PDF to `work/jsp.txt`, not used during transcription), lowercases, drops punctuation and markup, and word-diffs per page. Raw differences: `work/jsp_diff.txt`. Categories below are rough (automated, then eyeballed).

PDF page n = JSP page n-5 for n >= 6; pages 1 and 3 are the unnumbered title and preface leaves; page 5 is the chapter-summary leaf.

| Page | JSP words | differing words | % |
|---|---|---|---|
| 1 | 371 | 36 | 9.7 |
| 3 | 359 | 27 | 7.5 |
| 5 | 511 | 56 | 11.0 |
| 6 | 592 | 66 | 11.1 |
| 7-17, 19 | 544-676 | 14-26 each | 2.2-4.5 |
| 18 | 635 | 45 | 7.1 |
| 20 | 600 | 33 | 5.5 |
| Total | 10,339 | 494 | 4.8 |

Raw 4.8% overstates real errors (see below); about 3% is a fairer figure for genuine misreadings, omissions and over-normalised spellings combined, but the spelling errors are systematic and matter most.

## What went wrong (in order of importance)
1. **Spelling normalised toward standard English (~100 words).** The scribe wrote `exceding`, `haveing`, `presance`, `destroid`, `desireous`, `treasuary`, `procedings`, `knowledg`, `cours`, `praiseing`, `follouing`, `statture`, `scorge`, `rememberance`, `egytians`, `boddy`, `convinceing`, `Juniour`, `Northen`; I wrote the modern forms. This is the "reading from memory" risk predicted at the start, and it is the largest error class. It also means pages 1 and 3 (the title and preface) are less faithful than the main text.
2. **Wrong words (~25):** `after` read as `often` (pp 14, 18), `choice` as `chosen`, `bear` as `hear`, `thou shalt` as `ye shall`, `unto` as `with`, `hid` as `led`, `in` as `up`, `drest` missed, `methought` as `thought`, `fled` as `flee`, `beheld` as `behold`, `mine` as `my`.
3. **Omitted words (~25-40):** e.g. `it` (twice on p 6), `of my father`, `these words`, `dead`, `slay`, `lord`, `now`. A few are words the scribe had struck, which I did not see.
4. **Invented/added words (~10):** `is` inserted on p 5 ("I make ^is^ true"), where JSP has "to be true"; this looks like recall of the printed text. Also `of`, `then`, `even`, `to`.
5. **Fragment handling:** line-start/line-end fragments (`mannea`, `par took`, `bro ught`) differ from JSP only in where the break falls; cosmetic.

## What the comparison does NOT show as errors
- **Later-hand layer.** On many pages I transcribed dark-ink strikes and insertions (`which`->`who`, `saith`->`said`, `was`->`were`, `should be`, `dead`, `land of`). The JSP text shows the earlier wording (`which`, `saith`) and mostly leaves out these later corrections. So ~30 differences are a different layer, not misreadings; I captured something the JSP text omits, but I cannot confirm it is a later hand without the JSP editorial notes.
- **Reconstructed text.** JSP fills lost line ends and the torn bottom of p 5 with bracketed conjecture (e.g. 24 words at the end of p 5). I rightly did not transcribe what I could not see.
- **Footnote markers, headings, line-break splits** in the JSP PDF account for roughly 20-25 differences.

## Where we were right and JSP's PDF text is the odd one
- JSP "`may`" for "many" (p 6) and `◊` placeholders are extraction artifacts, not scholarship.
- p 12 "Brother Sariah": the scribe began "b..." and overwrote it with "mother"; JSP gives "mother", I gave the false start. Minor.

## Conclusions for the full project
- Handwriting recognition at this level is feasible: ~97% of words match on ordinary pages with no JSP help.
- The pipeline must **stop normalising spelling**. Needed: an explicit rule list of the scribe's spellings in the spec (`-eing`, `exceding`, `presance`, `-id` for `-ied`), a second pass that checks each line for modernised spellings, and a blind second read as in the 1840 project.
- Decide the policy for the later-hand layer (transcribe both layers, tagged).
- Decide whether JSP may be used as a check after the fact; the best use is as a diff tool, not as a source.

## Spelling pass (round 2)
Backup of the first pass: `work/pre-spelling-pass/`. Changes: rule-based restoration of the frequent scribal spellings (`exceding`, `haveing`, `presance`, `destroid`, `desireous`, `treasuary`, `procedings`, `knowledg`, `praiseing`: ~50 replacements), plus per-instance corrections checked against the images (`Choice`, `scorge`, `rememberance`, `makeing`, `Brothres`, `after` for `often` x3, `bear`, struck `things`, `hid`, `in`, `Egytians`). Re-score: 494 -> 435 differing words (4.8% -> 4.2%).
This re-score is **not blind**: I knew the error classes from the first comparison, and the rule-based replacements were applied across all pages after checking only a few instances on the images. About 50 one-off scribal spellings remain (`prophits`, `follouing`, `statture`, `shold`, `empted`, ...). Fixing those needs a fresh line-by-line read of each page, ideally by an independent blind pass.

## Source note from JSP (explains the "layer" differences)
The JSP page note says its online transcript "includes only the original inscriptions, not the later redactions". The manuscript carries 1830 compositor's marks (John H. Gilbert: pencil/ink punctuation, capitals, pilcrows) and emendations made by Joseph Smith for the 1837 edition. So the dark-ink strikes/insertions I transcribed (`which`->`who`, `saith`->`said`, `should be`, ...) are very likely the 1837 layer, and the dark punctuation on pages 18-20 the compositor's. About 30 differences across the 20 pages (about 20 per version on page 18) are this layer, not misreadings, which makes the true error rate on the original inscription lower than the raw 4.2% / 5.8% figures.
Corrections to my page notes: (1) the corner page numbers are the scribes' own original pagination, not "later"; (2) most pages have 37 lines, not the 30-32 I recorded in several comments (the Opus agents counted 37); (3) the preface/title leaves are unnumbered, as the note says.
Policy now in `tools/transcription-spec.md`: tag layers 1/2/3, record folio numbers. A fairer score would strip the 1837-layer marks (and keep the scribe's own struck words) before diffing; not done yet.

## Layer-aware re-score (pages 10 and 18)
Method: JSP has the original inscription only, so each version was also scored with all `^insertions^` removed and struck words kept (`work/layerA/`; diffs in `work/ld_*`). Dropping every insertion also drops the scribe's own same-ink insertions, so this is an approximation, best read as a bound. Differing words / JSP words:

| Version | p10 keep ins. | p10 drop ins. | p18 keep ins. | p18 drop ins. |
|---|---|---|---|---|
| Sonnet first pass | 18 | 19 | 45 | 38 |
| Sonnet corrected (not blind) | 13 | 14 | 43 | 36 |
| Sonnet blind re-run | 16 | 19 | - | - |
| Opus blind | 13 | 15 | 37 | 23 |

On page 18 about 6 of Opus's 23 and about 6 of Sonnet's 36 are artifacts of the JSP PDF text (footnote numbers, headings, line-break splits such as `acc ount`). That leaves about 4 real errors for Opus (0.6%: `how` omitted, `what` for `which`, a dropped `&`, `betha`) against about 14 for Sonnet (2.2%). The main difference: Opus transcribed the scribe's struck words legibly (`were`, `are`, `which`, `was`, `ever`, `be`), where Sonnet wrote `[illegible]` or misread them (`even`, `he`, `enheritance`, `yed`). On page 10 the two are level.
Caveat: two pages, one blind run each.

## Strategy 2 test: Opus checks a Sonnet first-pass draft (pages 10, 18)
Drafts: Sonnet first pass (`work/pre-spelling-pass/`). Opus viewed all five bands and returned only corrected lines (`work/checker-out/`, merged by `tools/apply_corrections.py` into `work/checker-final/`). Differing words keep-ins./drop-ins.: p10 13/15, p18 see below. Tokens per page: about 46k (checker) vs about 47-49k (full Opus), so no input saving: the image reads dominate.

## Strategy 1 test: can cheap signals route pages to Opus?
Signals vs Sonnet first-pass error (differing words per page), pages 5-20:
- Dark-ink pixel fraction from the scan: correlation -0.21 (useless).
- Draft's strike / `[illegible]` / `uncertain` counts: 0.10 / 0.21 / 0.35 on all 16 pages (pages 5-6 are inflated by JSP bracket reconstructions at torn edges, not Sonnet errors).
Per-page counts in `work/pre-spelling-pass/` vs `work/first_all.txt`.

## Opus vs Sonnet on pages 9, 17, 20 (blind, spelling rules for Opus; Sonnet first pass = no rules)
Differing words (all marks / insertions dropped): p9 Sonnet-first 17/16, Opus 9/8; p17 25/35 vs 20/27; p20 33/23 vs 27/18. ~45k tokens per Opus page. Page 9 control (blind Sonnet with rules): see below.

## Glossary in prompt: no gain (held-out pages 17, 18, 20, Opus)
No glossary 20/37/27 differing words vs with glossary 26/38/27 (all marks). Opus wrote `exceeding` etc. despite the listed `exceding`. Run-to-run noise is about +-6 words. Glossary removed from the spec.
## Post-check (tools/check_spelling.py, list in tools/scribe-forms.tsv)
Flags standard forms where the scribe likely wrote another (plus line-count and mark-balance checks). On pages 17/18/20: Opus blind 6 flags (3 correct), Opus+glossary 8 (5 correct), Sonnet first pass 11 (9 correct).

# Proofread spec: blind second read

A second, independent reading of a page, done fresh from the images, then reconciled with the first transcription by diff. Selected pages only (see CLAUDE.md for the selection rule). The rules for the text are those in `tools/transcription-spec.md`; read it fully first.

## Independence rules
- Make your own bands (`tools/prepare_bands.py --pages N --out work/proofN`). Do **not** read the existing `page-NNN.md`, other proofreads, any reference transcript (JSP) or `docs/`. Transcribe the page yourself to `work/proof/page-NNN.md`.
- Same rules, same markup (`~~ ~~`, `^ ^`, `@1837`/`@1830`/`@later`, `{,}@pencil`/`{,}@ink`, `[illegible]`, `<!-- uncertain -->`).

## Reconciliation (done by the coordinator, not the blind reader)
1. Diff the two readings word by word (`tools/compare_reference.py` works for this: `--ref` = the second reading in a JSP-like file, or use `diff`).
2. Words where the two disagree go to a short list `work/proof-disagreements-NNN.md`: page, line, reading A, reading B.
3. Resolve each by viewing the crop of that line (one small image), not the whole page. If still unclear, keep the first reading and leave `<!-- uncertain -->`; if a human decides, record it in `proofread-disagreements.md`.
4. Never "fix" a spelling toward the standard form; the only spelling edit allowed is restoring a scribe form that was normalised.
5. Log edits in `transcription-notes.md` section 3 (page, before, after, evidence).

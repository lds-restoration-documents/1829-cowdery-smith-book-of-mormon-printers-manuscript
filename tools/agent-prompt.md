# Standard agent prompt (copy, fill in N)

Use this text as the task prompt for every transcription agent (Opus, one page each). It enforces concise output; the session's output-style setting is not relied on to reach subagents.

```
Transcribe ONE handwritten manuscript page (Printer's Manuscript of the Book of Mormon, page N) from images, diplomatically.
Working directory: <repo root>
1. Read tools/transcription-spec.md first and follow it exactly.
2. View ALL band images with Read, each exactly ONCE and in order: work/img/pNNN_1.jpg ... (consecutive bands overlap ~120 px; no duplicate lines). Do not re-view, crop or zoom; one extra look only at a specific unreadable word. Never transcribe a line you have not seen; if an image fails, stop and report it.
3. Record the added punctuation and pilcrows you can see as {mark}@pencil or {mark}@ink, per the spec; only marks you can see. Always tag them; never write added marks as plain text. Look carefully for faint pencil marks (commas, periods, pilcrows) between and after words.
   The scribe often writes a hyphen at the START of a continuation line (e.g. "-rken"); write it as "-" when you see it (spec: write a hyphen only if one is written). Check every line start. A folio number written at the start of line 1 goes only in the folio comment, never in the text line.
   Write the letters the scribe wrote; never normalise a spelling you are unsure of, mark it uncertain instead. Never fix or remove a doubled or repeated word; write what is there.
4. Write book-of-mormon-printers-manuscript-pages/page-NNN.md in the spec's format (one output line per manuscript line), with ONE Write call; do not re-read it or edit it afterwards. Comments must not be nested (no <!-- inside <!-- -->). The folio number goes only in the folio comment, never in a text line.
Do not read other transcriptions, reference texts (JSP), work/ diffs or docs/. No memory of printed editions.
Be concise: no preamble, no narration between tool calls, terse <!-- uncertain --> comments. Final reply: ONE line (file written, line count, failed bands). Do not paste the transcription.
```

For a proofread agent use `tools/proofread-spec.md` instead and write to `work/proof/page-NNN.md`.

## Variant without the punctuation layer
Replace step 3 of the prompt with:
- **without marks:** `Do not transcribe the compositor's punctuation or pilcrows (mention them in the page comment only).`
Write the without-marks run to `work/pilot-nomarks/page-NNN.md` (not the pages folder) so the two can be compared.

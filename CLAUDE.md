# CLAUDE.md

Course notebooks for CAS AICP M4. `upstream` is the teacher's repo; `origin` is the user's fork.
The user is a student learning Python, NumPy and image processing. Their questions are usually about the notebook currently open in VS Code.

## Notes (`NOTES.md`)

`NOTES.md` holds the user's study notes, distilled from chats with Claude. It syncs across their machines.

- **`+++`** in a message means "add this to the notes": add the exchanges since the last save that aren't in the notes yet. Text after it (e.g. `+++ only the broadcasting part`) narrows or adds to what gets saved.
- Structure:
  - One `##` section per notebook, named by filename, in course order. Use the notebook that was open or selected in the IDE when the question was asked, or the one the question refers to. Questions not tied to a notebook go under `## General`.
  - One `###` per topic with the date, e.g. `### Average color (2026-10-27)`.
  - Write distilled notes, not transcripts: the key explanation, short code snippets, gotchas marked with ⚠️. Merge into an existing topic instead of duplicating it.
  - Questions the user wants to ask the teacher go under `## ❓ Questions for teacher` at the end, with the notebook name.
- Read `NOTES.md` before adding to it, and when the user refers to something discussed earlier. There's no need to read it otherwise.
- After updating, confirm in one line what was added. Don't commit unless asked.

# Project Notes

Internal working notes for SecurityScanner. Not user-facing — see README.md for that.

## Current state

Single-file CLI (`scanner.py`, ~98 lines). Takes a file path as `argv[1]`, reads it as
text, drops the whole file contents into a fixed prompt template, sends it to
`gemini-2.5-flash` via `google-genai`, then parses the plain-text response into blocks
split on `---`, sorts by a severity keyword found anywhere in the block, and prints each
block colorized by severity via `colorama`.

`vulnerable.py` is the fixture used to exercise it — has SQL injection (f-string into
`cursor.execute`), command injection (`os.system` with unsanitized input), MD5 password
hashing, and hardcoded credentials/API secret. Good coverage across OWASP-ish categories
for demo purposes.

No requirements.txt / pyproject.toml — dependencies are only documented in the README
install command (`google-genai`, `python-dotenv`, `colorama`). If this project grows,
pin these in a requirements.txt so `pip install -r requirements.txt` works and versions
are reproducible.

## Known issues / TODOs

- **`.env` is tracked in git** (`git ls-files` includes it). Currently it only holds an
  empty `GOOGLE_API_KEY=` placeholder, so nothing sensitive is exposed today, but the
  `.gitignore` does not exclude `.env` — only `__pycache__/`, `*.pyc`, `.venv/`. If
  someone fills in a real key locally and runs `git add -A` or similar out of habit,
  it will get committed. Should add `.env` to `.gitignore` and keep only an
  `.env.example` tracked instead. This is the top-priority fix.
- `sort_blocks()` / `color_block()` in `scanner.py` score by `"critical"`/`"high"`/
  `"medium"`/`"low"` appearing *anywhere* in the block text, not just in the
  `Severity:` line. A `Why:` or `Fix:` sentence that happens to mention a different
  severity word (e.g. "this is not as severe as a critical issue") will misclassify
  the block. Should parse the `Severity: X` line specifically with a regex instead of
  substring search.
- No handling for a bad/missing file path — `open(code_path, ...)` will raise and
  print a raw Python traceback instead of a clean CLI error. Same for empty files.
- No handling for empty/malformed Gemini responses (e.g. if the model ever returns
  markdown despite the "DO NOT use markdown" instruction, or returns zero `---`
  blocks) — `sort_blocks` would just return a single unclassified block, which is
  probably fine, but never verified.
- Model name (`gemini-2.5-flash`) and the full prompt text are hardcoded constants in
  `scanner.py`. No CLI flag or config to swap models or tweak the prompt. Fine for a
  personal/demo tool; would need extraction if this becomes a shared utility.
- No automated tests. `vulnerable.py` is a manual smoke-test fixture, not a test suite.
  If this project keeps growing, worth adding a small pytest suite that mocks the
  Gemini client and asserts on `sort_blocks`/`color_block` parsing logic (that's the
  actual custom logic worth covering — the Gemini call itself doesn't need unit tests).
- venv/ is checked out in the working tree but excluded via `.venv/` in `.gitignore`
  — note the mismatch: the actual directory here is named `venv/`, not `.venv/`. It
  happens to not be tracked (double-check with `git status` before assuming it's
  ignored on a fresh clone), but the gitignore pattern is technically wrong for this
  directory name. Worth fixing to `venv/` or documenting that contributors should name
  it `.venv/`.

## Ideas for next steps

- Add a `--json` output mode so the scanner's findings could be piped into other
  tooling (CI gate, dashboard) instead of only pretty-printed to a terminal.
- Support scanning a directory / multiple files in one invocation instead of one path
  at a time.
- Add a `requirements.txt` (or move to `pyproject.toml` with a proper `[project]`
  table) so setup is `pip install -r requirements.txt` rather than a hand-typed list
  in the README that can drift from actual dependencies.
- Consider a confidence/false-positive note in the output — an LLM security review is
  a good triage step, not a replacement for SAST tooling, and the README/output could
  say so explicitly for anyone who stumbles on this expecting a complete scanner.

## Architecture decisions worth remembering

- Chose plain-text output from Gemini (explicitly instructing "DO NOT use markdown")
  over structured JSON output. Simpler to prompt for and parse with a `---` splitter,
  at the cost of the fragile keyword-based severity sort noted above. If severity
  misclassification becomes an actual problem, switching the prompt to request JSON
  (or using Gemini's structured output mode) would fix it at the source instead of
  patching the parser.
- `google-genai` (the new unified Google GenAI SDK) is used rather than the older
  `google-generativeai` package — worth remembering when searching for docs/examples,
  since the two packages have similar names but different APIs.

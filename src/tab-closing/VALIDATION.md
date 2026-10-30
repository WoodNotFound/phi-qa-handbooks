# Handbook validation

Validated on 2026-10-30 against the generated local site, using Computer Use in the
local Phi OpenSource build. These checks validate the handbook UI and fixtures;
they do not establish that all browser feature cases pass.

- Built with `python3 build.py`; existing mail handbook outputs remained unchanged.
- Validated 87 unique base cases, 202 unique execution points, 12 sections, and
  12 localized strings in each of 9 languages.
- Checked the embedded JavaScript syntax with `node --check` and whitespace with
  `git diff --check`.
- Observed 202 initially untested execution points and 134 P0 points awaiting pass.
- Searched for ENV-01, recorded a synthetic pass and note against a synthetic build,
  reloaded, and observed the record and note retained.
- Selected the smoke filter and observed 19 of 202 points displayed.
- Downloaded Markdown and JSON through the UI. Read back the downloaded Markdown:
  all 202 execution point headings were present despite the active smoke filter.
  The JSON retained the recorded result, note, and build metadata.
- Changed the build identifier and observed 202 untested / 0 passed again.
- Opened the unsaved fixture with a label and run identifier, typed a disposable
  marker, and followed its navigation link. Phi displayed the native leave-site
  dialog. Cancelling retained the marker and document instance identifier.
- Disarmed the fixture through its visible button and closed that test tab without
  another leave-site dialog.

All synthetic records belong to the local preview origin only. No results are
embedded in the published handbook. Dark mode, narrow-window rendering, every
filter combination, clipboard fallback, and every fixture variant were not all
manually exercised in this validation pass.

## Revision r2 coverage audit and UI checks

The expanded specification was reviewed against the current native implementation:
`BrowserState` candidate filtering, split expansion and batch lifecycle;
`Tab.closeOnDoubleClick` and its sidebar, group and horizontal surfaces;
tab/group menu validation and invocation; preferences; and intercepted legacy
commands. The source working-diff fingerprint remains unchanged.

- The specification now contains 166 base cases, 512 execution points, 13 sections,
  and 18 coverage dimensions. Every case is referenced by the coverage matrix.
- Priorities: 272 P0 points, 208 P1 points, 32 P2 points. All 9 languages have
  separate results for the 3 layouts. Hardware, OS and channel matrices are
  repeated runs, not falsely represented as already-tested configurations.
- Corrected missing setup requirements, enabled unsaved fixtures before confirming
  leaving, distinguished horizontal ordinary bookmark copies from protected bound
  pages, and separated exploratory restoration claims from acceptance contracts.
- Split setting combinations and modifier/confirmation/device variants into unique
  result keys. Old build, run, or handbook-revision records do not count as passes.
- Rebuilt the HTML and full static Markdown, validated unique IDs, required fields,
  coverage references, locale completeness, execution counts and script syntax.
- Through Computer Use, observed 512 untested points after the revision update.
  Searching SET-06 displayed 12 independent layout/setting combinations. Marking
  SET-06-PER-off-off produced exactly one synthetic pass.
- Downloaded both reports with that 12-point filter active. Read back 512 Markdown
  result headings and 512 JSON execution snapshots; only that one variant was
  passed, with the expected run and revision stamps.
- Changed the run ID and observed 512 untested / 0 passed. Selected the exploratory
  type filter and observed the expected 11 exploration points.

These remain handbook validation checks, not execution of all 512 feature points.
The optional audio/download fixture controls received syntax validation; actual
media/download lifecycle combinations, all UI filters, hardware, locales, OSes,
conditional official features and the full native feature matrix remain manual QA
work to record in the published checklist.

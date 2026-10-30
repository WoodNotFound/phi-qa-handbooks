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

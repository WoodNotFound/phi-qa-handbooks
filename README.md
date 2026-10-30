# Phi QA handbooks

Test handbooks for Phi features, written for QA: how a feature works, what to test, and what to expect.
Published at https://woodnotfound.github.io/phi-qa-handbooks/ (GitHub Pages, `main` branch root; every
page is `noindex`).

| Handbook | Page | Source |
| --- | --- | --- |
| Mail guard (Kensington), in Chinese | [`mail-guard/`](https://woodnotfound.github.io/phi-qa-handbooks/mail-guard/) | `src/mail-guard/` |
| Tab closing operations, in Chinese | [`tab-closing/`](https://woodnotfound.github.io/phi-qa-handbooks/tab-closing/) | `src/tab-closing/` |

## Updating a handbook

1. Edit `src/<name>/template.html` (and `rules.json` when the rule table changes).
2. Run `python3 build.py`. It writes `<name>/index.html` for the site, `index.html`, and
   `dist/<name>.artifact.html` (not committed).
3. Commit and push; Pages rebuilds in a minute or two.

Handbooks may include standalone HTML test pages in `src/<name>/fixtures/`. The build copies them
to `<name>/fixtures/`. Tab-closing fixtures accept `tab`, `run`, and `kind` (`normal`, `unsaved`,
or `long`) query parameters. They make no API requests and never close browser tabs automatically.
The handbook stores manual results locally; export a report before switching builds, runs, revisions, or clearing data.
The tab-closing build also writes `tab-closing/handbook.md`: all execution points with their steps and expected results, readable without JavaScript.

The mail guard handbook also has a private claude.ai copy,
https://claude.ai/artifact/HBKwHhxprqCSD8U8g5QN4y, republished from `dist/mail-guard.artifact.html`.
Update both together.

`template.html` is the page as written for an Artifact: no document skeleton, and Mermaid diagrams as
`<pre class="mermaid">`. The build wraps it in a full document and loads Mermaid, which an Artifact
host does by itself.

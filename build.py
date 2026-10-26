#!/usr/bin/env python3
"""Builds the published QA handbooks.

Each handbook lives in src/<name>/: template.html is the page as written for a
claude.ai Artifact (no document skeleton; `__RULES__` where the rule table's data
goes) and rules.json is that data. For every handbook the build writes:

  <name>/index.html          the GitHub Pages copy: a full document, noindex,
                             with Mermaid loaded (the Artifact host loads it
                             itself, a plain page has to)
  dist/<name>.artifact.html  the Artifact copy (gitignored), to publish with
                             Claude's Artifact tool to the handbook's link

and index.html, the list of handbooks. Run: python3 build.py
"""

import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent

# name, title, one line for the index
HANDBOOKS = [
    (
        "mail-guard",
        "邮件防护 QA 手册",
        "Kensington 邮件防护：Gmail、Outlook、Yahoo Mail 上一封邮件的安全等级是怎么判断的，以及测试指南与清单。",
    ),
]

MERMAID = """<script src="https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({
    startOnLoad: true,
    securityLevel: "strict",
    theme: matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "neutral",
  });
</script>"""

# The leading <title>, <meta>, <link> and <style> elements of a template belong in <head>.
HEAD_PART = re.compile(
    r"\s*(?:<title>.*?</title>|<meta\b[^>]*>|<link\b[^>]*>|<style\b[^>]*>.*?</style>)",
    re.S,
)


def split_head(page: str) -> tuple[str, str]:
    end = 0
    while True:
        match = HEAD_PART.match(page, end)
        if match is None:
            return page[:end], page[end:]
        end = match.end()


def document(head: str, body: str) -> str:
    # The Artifact-only viewport hint means nothing on a plain page.
    head = re.sub(r'\s*<meta name="claude:[^"]*"[^>]*>', "", head)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
{head.strip()}
</head>
<body>
{body.strip()}
{MERMAID}
</body>
</html>
"""


INDEX = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Phi QA 手册</title>
<style>
  :root { --paper: #f6f7f4; --sheet: #ffffff; --ink: #1d2320; --soft: #4f5a54; --rule: #dfe3dd; --accent: #2f6b4f; }
  @media (prefers-color-scheme: dark) {
    :root { --paper: #151917; --sheet: #1d2220; --ink: #e6ebe7; --soft: #a6b0aa; --rule: #323a36; --accent: #8fc9a8; }
  }
  * { box-sizing: border-box; }
  body { margin: 0; background: var(--paper); color: var(--ink);
    font: 16px/1.6 "Noto Sans SC", system-ui, -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif; }
  main { max-width: 760px; margin: 0 auto; padding: 48px 16px 64px; }
  h1 { font-size: 28px; margin: 0 0 6px; }
  .lede { color: var(--soft); margin: 0 0 32px; }
  ul { list-style: none; padding: 0; margin: 0; display: grid; gap: 12px; }
  li { background: var(--sheet); border: 1px solid var(--rule); border-radius: 10px; padding: 16px 18px; }
  a { color: var(--accent); font-weight: 600; font-size: 18px; text-decoration: none; }
  a:hover { text-decoration: underline; }
  p.line { margin: 4px 0 0; color: var(--soft); font-size: 14.5px; }
</style>
</head>
<body>
<main>
  <h1>Phi QA 手册</h1>
  <p class="lede">各功能的测试手册：功能怎么工作、该测什么、预期是什么。</p>
  <ul>
{items}
  </ul>
</main>
</body>
</html>
"""


def main() -> None:
    (ROOT / "dist").mkdir(exist_ok=True)
    items = []
    for name, title, line in HANDBOOKS:
        source = ROOT / "src" / name
        template = (source / "template.html").read_text(encoding="utf-8")
        rules = (source / "rules.json").read_text(encoding="utf-8").strip()
        if template.count("__RULES__") != 1:
            raise SystemExit(f"{name}: template must hold __RULES__ exactly once")
        json.loads(rules)
        page = template.replace("__RULES__", rules)

        (ROOT / "dist" / f"{name}.artifact.html").write_text(page, encoding="utf-8")
        head, body = split_head(page)
        out = ROOT / name / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(document(head, body), encoding="utf-8")

        items.append(
            f'    <li><a href="{html.escape(name)}/">{html.escape(title)}</a>'
            f'<p class="line">{html.escape(line)}</p></li>'
        )
        print(f"built {out.relative_to(ROOT)}")

    (ROOT / "index.html").write_text(INDEX.replace("{items}", "\n".join(items)), encoding="utf-8")
    print("built index.html")


if __name__ == "__main__":
    main()

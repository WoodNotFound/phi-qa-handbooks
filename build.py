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
import shutil

ROOT = pathlib.Path(__file__).resolve().parent

# name, title, one line for the index
HANDBOOKS = [
    (
        "mail-guard",
        "邮件防护 QA 手册",
        "Kensington 邮件防护：Gmail、Outlook、Yahoo Mail 上一封邮件的安全等级是怎么判断的，以及测试指南与清单。",
    ),
    (
        "mail-guard-landing",
        "落地页守卫 QA 手册",
        "邮件防护的下一步：用户点开（或复制）可疑邮件里的链接后，落地页顶部的提示条何时出现、写什么，以及测试指南与清单。",
    ),
    (
        "tab-closing",
        "标签页关闭操作手测指南",
        "双击关闭与按位置批量关闭：三种布局、分屏、固定项、标签组、书签，以及可记录和导出的完整手测清单。",
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


def manual_markdown(spec: dict) -> str:
    """Renders the tab-closing case specification without browser scripting."""
    layouts = {"once": "通用", "performance": "Performance / 性能",
               "balanced": "Balanced / 均衡", "comfortable": "Comfortable / 舒适"}
    codes = {"once": "COMMON", "performance": "PER", "balanced": "BAL", "comfortable": "COM"}
    lines = [f"# {spec['title']}", "", f"手册修订：{spec['revision']}", "",
             "本文件是完整手测规范，所有结果初始为未测；不是全量通过报告。",
             "在线操作说明与对象搭建：https://woodnotfound.github.io/phi-qa-handbooks/tab-closing/", "",
             "每轮记录测试人、本轮编号、实际构建、渠道、macOS/芯片及 Framework；每个支持环境单独建报告。",
             "只操作 TC- 可丢弃页面、组、pin 和书签；保护项核对输入标记及本次打开编号。",
             "普通序列 A→F 以真实原生顺序为准；S[B+C] 为分屏，G[B,C] 为组。",
             "双击默认关、位置关闭默认开；两个开关独立。性能/均衡上下，舒适左右。",
             "方向与关闭其他保护整个 split；双击只关点击的一侧。pin 和纵向绑定书签页受保护。",
             "beforeunload 与组确认可以部分完成；取消文档必须存活，不承诺整批回滚。",
             "P0 适用项全部通过；P1 完整回归无未处理失败；P2 缺失前置和探索标准必须说明。",
             "探索项未有产品判定标准时记阻塞；跳过不等于通过。收尾恢复配置，仅清理本轮资料。", "",
             f"功能分支：{spec['source']['branch']}；状态：{spec['source']['status']}",
             f"Sources/Resources diff SHA-256：{spec['source']['workingDiffSha256']}", "",
             "## 覆盖矩阵", ""]
    for row in spec["coverage"]:
        lines.extend([f"- **{row['dimension']}**：{row['scope']}。用例：{'、'.join(row['cases'])}"])
    for section in spec["sections"]:
        lines.extend(["", f"## {section['id']} {section['title']}", "", section["summary"], ""])
        for case in section["cases"]:
            for layout in case["layouts"]:
                def direction(value: str) -> str:
                    return value.replace("{before}", "关闭左侧标签页" if layout == "comfortable" else "关闭上方标签页").replace("{after}", "关闭右侧标签页" if layout == "comfortable" else "关闭下方标签页")
                for language in case.get("languages", [""]):
                    for variant in case.get("variants", [{"id": "", "label": ""}]):
                        key = case["id"] + "-" + codes[layout] + ("-" + language if language else "") + ("-" + variant["id"] if variant["id"] else "")
                        lines.extend([f"### {key} {case['title']}", "",
                                      f"优先级：{case['priority']}；布局：{layouts[layout]}；语言：{language or '按本轮环境'}；变体：{variant['label'] or '无'}",
                                      "类型：" + ("探索／待定标准" if case["kind"] == "exploratory" else "验收／回归"), "",
                                      "前置：" + direction(case["pre"]), "", "步骤：", ""])
                        lines.extend(f"{index}. {direction(step)}" for index, step in enumerate(case["steps"], 1))
                        lines.extend(["", "预期：", ""])
                        lines.extend(f"- {direction(item)}" for item in case["expected"])
                        lines.extend(["", "重置：" + case["reset"], "证据：" + case["evidence"],
                                      "", "结果：未测；备注：", ""])
    lines.extend(["## 9 种语言文案对照", ""])
    for locale, labels in spec["labels"].items():
        lines.extend([f"### {locale}", ""])
        lines.extend(f"- `{key}`：{value}" for key, value in labels.items())
        lines.append("")
    return "\n".join(lines)


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
        spec = json.loads(rules)
        page = template.replace("__RULES__", rules)

        (ROOT / "dist" / f"{name}.artifact.html").write_text(page, encoding="utf-8")
        head, body = split_head(page)
        out = ROOT / name / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(document(head, body), encoding="utf-8")
        if name == "tab-closing":
            (out.parent / "handbook.md").write_text(manual_markdown(spec), encoding="utf-8")

        for fixture in sorted((source / "fixtures").glob("*.html")):
            fixture_out = out.parent / "fixtures" / fixture.name
            fixture_out.parent.mkdir(exist_ok=True)
            shutil.copyfile(fixture, fixture_out)
            print(f"copied {fixture_out.relative_to(ROOT)}")

        items.append(
            f'    <li><a href="{html.escape(name)}/">{html.escape(title)}</a>'
            f'<p class="line">{html.escape(line)}</p></li>'
        )
        print(f"built {out.relative_to(ROOT)}")

    (ROOT / "index.html").write_text(INDEX.replace("{items}", "\n".join(items)), encoding="utf-8")
    print("built index.html")


if __name__ == "__main__":
    main()

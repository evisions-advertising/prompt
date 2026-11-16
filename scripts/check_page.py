#!/usr/bin/env python3
"""CI check for the prompt page: HTML parses, the prompt is present and non-empty, all buttons are wired."""
import html.parser, json, re, sys, pathlib

page = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "index.html").read_text(encoding="utf-8")
errors = []

class P(html.parser.HTMLParser):
    ids = set()
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if "id" in d:
            self.ids.add(d["id"])
p = P(); p.feed(page)
for i in ("copy", "chatgpt", "claude", "gemini", "text"):
    if i not in p.ids:
        errors.append(f"missing element #{i}")
m = re.search(r"const PROMPT = (\".*?\");\n", page, re.S)
if not m:
    errors.append("PROMPT constant not found")
else:
    prompt = json.loads(m.group(1))
    if len(prompt) < 200:
        errors.append(f"prompt too short ({len(prompt)} chars)")
for needle in ("https://chatgpt.com/?q=", "https://claude.ai/new?q=", "{{"):
    if needle == "{{":
        if needle in page:
            errors.append("unreplaced template placeholder")
    elif needle not in page:
        errors.append(f"missing link {needle}")
if errors:
    print("\n".join(errors)); sys.exit(1)
print("ok: page valid")

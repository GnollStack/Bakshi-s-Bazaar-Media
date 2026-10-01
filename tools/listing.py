"""Foundry package listings and shared module tables for GnollStack modules.

Commands (run from anywhere):
  python tools/listing.py build [module-id ...]   Write each module's docs/README.html from its README.md
  python tools/listing.py check [module-id ...]   Report stale or broken listings (exit 1 on problems)
  python tools/listing.py sync-lists              Refresh the Bakshi's Bazaar / Free Modules tables in every README

With no module ids, every module in listing-config.json is used.
Requires: pip install -r tools/requirements.txt
"""
import argparse, html, json, os, pathlib, re, sys, urllib.parse

TOOLS = pathlib.Path(__file__).resolve().parent
MEDIA_REPO = TOOLS.parent
CONFIG = json.loads((TOOLS / "listing-config.json").read_text(encoding="utf-8"))
LISTS = json.loads((TOOLS / "module-lists.json").read_text(encoding="utf-8"))
MEDIA_PREFIXES = (
    "https://raw.githubusercontent.com/GnollStack/Bakshi-s-Bazaar-Media/main/",
    "https://raw.githubusercontent.com/GnollStack/Bakshi-s-Bazaar-Media/refs/heads/main/",
)
ALERTS = {"NOTE": "Note", "TIP": "Tip", "IMPORTANT": "Important", "WARNING": "Warning", "CAUTION": "Caution"}
IMG_STYLE = "max-width: 100%; height: auto;"


def modules_dir(override=None):
    raw = override or os.environ.get("FOUNDRY_MODULES_DIR") or CONFIG["modulesDir"]
    path = pathlib.Path(os.path.expandvars(raw))
    if not path.is_dir():
        sys.exit(f"Modules folder not found: {path}. Pass --modules-dir or set FOUNDRY_MODULES_DIR.")
    return path


def read_readme(root, module):
    return (root / module / "README.md").read_text(encoding="utf-8")


# ---------------------------------------------------------------- version guard

def version_problems(root, module):
    """Static version mentions in README.md must match module.json."""
    version = json.loads((root / module / "module.json").read_text(encoding="utf-8-sig"))["version"]
    readme = read_readme(root, module)
    found = re.findall(r"img\.shields\.io/badge/[^)\s\"]*?-(\d+\.\d+\.\d+)-", readme)
    found += re.findall(r"\bversion (\d+\.\d+\.\d+)\]\(https://img\.shields\.io", readme)
    found += re.findall(r"\*\*(?:Module )?[Vv]ersion:\*\* `?(\d+\.\d+\.\d+)`?", readme)
    return [f"README says {v}, module.json says {version}" for v in sorted(set(found)) if v != version]


# ---------------------------------------------------------------- listing build

def github_slug(text, used):
    s = re.sub(r"<[^>]+>", "", html.unescape(text)).strip().lower()
    s = re.sub(r"[^\w\- ]", "", s).replace(" ", "-")
    base, n = s, 1
    while s in used:
        s = f"{base}-{n}"
        n += 1
    used.add(s)
    return s


def media_dims(src):
    from PIL import Image
    for prefix in MEDIA_PREFIXES:
        if src.startswith(prefix):
            rel = urllib.parse.unquote(src[len(prefix):])
            path = MEDIA_REPO / rel
            if not path.is_file():
                raise SystemExit(f"Media file referenced but missing from the media repo: {rel}")
            with Image.open(path) as im:
                return im.size
    return None


def render(root, module):
    from markdown_it import MarkdownIt
    settings = CONFIG["modules"].get(module, {})
    src = read_readme(root, module).replace("\r\n", "\n")
    src = re.sub(r"^> \[!(\w+)\]\n> ",
                 lambda m: f"> **{ALERTS.get(m.group(1).upper(), m.group(1).title())}:** ", src, flags=re.M)
    md = MarkdownIt("commonmark", {"html": True}).enable("table").enable("strikethrough")
    out = md.render(src)
    out = out.replace('<div align="center">', '<div style="text-align: center;">')

    # Headings take the id of the <a id> anchors just above them, otherwise a GitHub-style slug.
    used = set(re.findall(r'<a id="([^"]+)"></a>', out))
    def heading(m):
        ids = re.findall(r'<a id="([^"]+)"></a>', m.group(1) or "")
        level, inner = m.group(2), m.group(3)
        if ids:
            rest = "".join(f'<a id="{i}"></a>' for i in ids[1:])
            return f'{rest}{chr(10) if rest else ""}<h{level} id="{ids[0]}">{inner}</h{level}>'
        return f'<h{level} id="{github_slug(inner, used)}">{inner}</h{level}>'
    anchor_run = r'(?:<p>)?(?:<a id="[^"]+"></a>\s*)+(?:</p>)?\s*'
    out = re.sub(rf'((?:{anchor_run})+)?<h([1-6])>(.*?)</h\2>', heading, out, flags=re.S)
    out = re.sub(r'^((?:<a id="[^"]+"></a>\n?)+)$',
                 lambda m: "<p>" + m.group(1).replace("\n", "") + "</p>\n", out, flags=re.M)

    # Listing-only trims (README keeps everything).
    omit = settings.get("omitFromListing")
    if omit:
        pattern = re.compile(omit["anchoredDetails"])
        removed = []
        def drop(m):
            if pattern.search(m.group(1)):
                removed.append(m.group(1))
                return ""
            return m.group(0)
        out = re.sub(r'<p><a id="([^"]+)"></a></p>\n<details>.*?</details>\n', drop, out, flags=re.S)
        for anchor in removed:
            out = out.replace(f'href="#{anchor}"', f'href="{settings["github"]}#{anchor}"')
        if omit.get("noteAfterHeading"):
            out = re.sub(rf'(<h[1-6] id="{re.escape(omit["noteAfterHeading"])}">.*?</h[1-6]>\n<p>.*?</p>\n)',
                         lambda m: m.group(1) + f'<p>{omit["note"]}</p>\n', out, count=1, flags=re.S)

    # Relative links: GitHub for free modules, "in the installed module" for premium ones.
    blob = settings.get("github")
    def link(m):
        href, text = m.group(1), m.group(2)
        if re.match(r"^(https?:|mailto:|#)", href):
            return m.group(0)
        if blob:
            return f'<a href="{blob}/blob/main/{href}">{text}</a>'
        path = html.escape(urllib.parse.unquote(html.unescape(href)))
        return f"{text} (<code>{path}</code> in the installed module)"
    out = re.sub(r'<a href="([^"]+)">(.*?)</a>', link, out)

    # Images scale to width; media-repo images link to the full-size original and lazy-load after the first.
    first = [True]
    def img(m):
        lead, tag = m.group(1) or "", m.group(2)
        srcm = re.search(r'src="([^"]+)"', tag)
        src = html.unescape(srcm.group(1)) if srcm else ""
        attrs = re.sub(r"\s*/?>$", "", tag)
        if "style=" not in attrs:
            attrs += f' style="{IMG_STYLE}"'
        dims = media_dims(src)
        if dims is None:
            return lead + attrs + " />"
        if "width=" not in attrs:
            attrs += f' width="{dims[0]}" height="{dims[1]}"'
        attrs += ' decoding="async"' if first[0] else ' loading="lazy" decoding="async"'
        first[0] = False
        return lead + attrs + " />" if lead else f'<a href="{html.escape(src)}">{attrs} /></a>'
    out = re.sub(r'(<a [^>]*>\s*)?(<img [^>]*>)', img, out)
    return re.sub(r"<hr />\n(?=<h[23])", "<hr />\n\n", out)


def listing_path(root, module):
    return root / module / "docs" / "README.html"


def structural_problems(text):
    nocode = re.sub(r"<pre>.*?</pre>", "", text, flags=re.S)
    ids = re.findall(r'id="([^"]+)"', nocode)
    problems = [f"duplicate id: {i}" for i in sorted({i for i in ids if ids.count(i) > 1})]
    problems += [f"broken anchor: #{a}" for a in sorted(set(re.findall(r'href="#([^"]+)"', nocode)) - set(ids))]
    problems += [f"relative link: {h}" for h in re.findall(r'(?:href|src)="([^"]+)"', nocode)
                 if not re.match(r"(https?:|mailto:|#)", h)]
    if nocode.count("<details>") != nocode.count("</details>"):
        problems.append("unbalanced <details>")
    if re.search(r"(?m)^(#{1,6} |\|---|```|\[!)", nocode):
        problems.append("unrendered Markdown")
    return problems


# ---------------------------------------------------------------- shared tables

def table(entries, overrides, linked):
    rows = ["| Module | What it adds |", "| --- | --- |"]
    for e in entries:
        name = f"[{e['name']}]({e['url']})" if linked and e.get("url") else e["name"]
        rows.append(f"| **{name}** | {overrides.get(e['id'], e['summary'])} |")
    return rows


def sync_lists(root):
    changed = 0
    for module, settings in CONFIG["modules"].items():
        path = root / module / "README.md"
        # Only the table lines are rewritten; every other byte (including mixed line endings) is kept.
        lines = path.read_bytes().decode("utf-8").splitlines(keepends=True)
        bare = [line.rstrip("\r\n") for line in lines]
        if settings["tier"] == "free":
            anchor, rows = '<a id="bakshis-bazaar"></a>', table(LISTS["premium"], LISTS["overrides"].get(module, {}), False)
        else:
            anchor, rows = '<a id="free-modules"></a>', table(LISTS["free"], LISTS["overrides"].get(module, {}), True)
        if anchor not in bare:
            print(f"{module}: no {anchor} section; skipped")
            continue
        start = bare.index(anchor)
        first = next(i for i in range(start, len(bare)) if bare[i].startswith("| Module |"))
        last = first
        while last + 1 < len(bare) and bare[last + 1].startswith("|"):
            last += 1
        if bare[first:last + 1] != rows:
            eol = "\r\n" if lines[first].endswith("\r\n") else "\n"
            lines[first:last + 1] = [row + eol for row in rows]
            path.write_bytes("".join(lines).encode("utf-8"))
            changed += 1
            print(f"{module}: table updated")
    print(f"{changed} README(s) changed")


# ---------------------------------------------------------------- CLI

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=["build", "check", "sync-lists"])
    parser.add_argument("modules", nargs="*")
    parser.add_argument("--modules-dir")
    args = parser.parse_args()
    root = modules_dir(args.modules_dir)
    if args.command == "sync-lists":
        return sync_lists(root)
    targets = args.modules or list(CONFIG["modules"])
    failed = False
    for module in targets:
        if module not in CONFIG["modules"]:
            sys.exit(f"Unknown module {module!r}; add it to tools/listing-config.json")
        versions = version_problems(root, module)
        if versions:
            print(f"{module}: version mismatch: " + "; ".join(versions))
            failed = True
            continue
        out = render(root, module)
        problems = structural_problems(out)
        dest = listing_path(root, module)
        if args.command == "build":
            dest.parent.mkdir(exist_ok=True)
            dest.write_text(out, encoding="utf-8", newline="\n")
            print(f"{module}: wrote {dest} ({len(out) // 1024} KB)" + (f"; problems: {problems}" if problems else ""))
        else:
            current = dest.read_text(encoding="utf-8") if dest.is_file() else None
            if current is None:
                problems.append("docs/README.html is missing")
            elif current != out:
                problems.append("docs/README.html is out of date; run build")
            print(f"{module}: " + ("ok" if not problems else "; ".join(problems)))
        failed |= bool(problems)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()

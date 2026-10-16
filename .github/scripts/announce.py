"""Post a Discord announcement when a module release goes live.

Reads each module's published manifest. When its version is newer than the
last one announced, posts that version's notes from the module's CHANGELOG.md
to Discord, then records the version in .github/announcer/announced.json.

Environment:
  DISCORD_WEBHOOK_URL          Webhook for announcements.
  DISCORD_WEBHOOK_URL_PREMIUM  Optional separate webhook for premium modules.
  DISCORD_ROLE_ID              Optional role to ping.
  DRY_RUN                      "true" to preview without posting.

Without a webhook, or with --dry-run, it only previews and changes nothing.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / ".github" / "announcer" / "modules.json"
STATE = ROOT / ".github" / "announcer" / "announced.json"
USER_AGENT = "BakshisBazaarAnnouncer/1.0 (+https://github.com/GnollStack/bakshis-bazaar-archives)"
COLORS = {"premium": 0xC9A227, "free": 0x4F8A5B}
SYSTEM_NAMES = {"dnd5e": "D&D5e"}
DESCRIPTION_LIMIT = 3500  # Discord allows 4096; leave room for the trim marker
HEADING = re.compile(r"^## \[?v?(\d+(?:\.\d+)*)\]?(?:\s+-\s+\d{4}-\d{2}-\d{2})?\s*$", re.IGNORECASE)


def version_key(version):
    return tuple(int(part) for part in re.findall(r"\d+", str(version)))


def is_newer(published, announced):
    return version_key(published) > version_key(announced)


def changelog_section(text, version):
    """Return the notes under the heading for this version, or None."""
    notes = None
    for line in text.splitlines():
        if line.startswith("## "):
            if notes is not None:
                break
            match = HEADING.match(line)
            if match and version_key(match.group(1)) == version_key(version):
                notes = []
            continue
        if notes is not None:
            notes.append(line)
    if notes is None:
        return None
    return "\n".join(notes).strip() or None


def to_discord(markdown):
    """Discord embeds don't render ### headings, so make them bold."""
    return re.sub(r"^#{3,6}\s+(.+?)\s*$", r"**\1**", markdown, flags=re.MULTILINE)


def trim(text, limit=DESCRIPTION_LIMIT):
    if len(text) <= limit:
        return text
    cut = text[:limit]
    newline = cut.rfind("\n")
    if newline > 0:
        cut = cut[:newline]
    return cut.rstrip() + "\n…"


def requirements(manifest):
    parts = []
    minimum = (manifest.get("compatibility") or {}).get("minimum")
    if minimum:
        parts.append(f"Foundry VTT {minimum}+")
    for system in (manifest.get("relationships") or {}).get("systems") or []:
        name = SYSTEM_NAMES.get(system.get("id"), system.get("id"))
        system_min = (system.get("compatibility") or {}).get("minimum")
        parts.append(f"{name} {system_min}+" if system_min else name)
    return " · ".join(parts)


def changelog_url(site, module):
    return f"{site}/{module['folder']}/CHANGELOG.html"


def build_payload(module, manifest, notes, notes_url, role_id=""):
    version = manifest["version"]
    if notes:
        description = trim(to_discord(notes))
    else:
        description = f"V{version} is out. See the changelog for details."
    get_it = "Foundry package page" if module["tier"] == "premium" else "GitHub release"
    fields = []
    needs = requirements(manifest)
    if needs:
        fields.append({"name": "Requires", "value": needs, "inline": True})
    fields.append({"name": "Get it", "value": f"[{get_it}]({module['page']})", "inline": True})
    fields.append({"name": "Full notes", "value": f"[Changelog]({notes_url})", "inline": True})
    payload = {
        "embeds": [{
            "title": f"{module['name']} V{version}",
            "url": notes_url,
            "description": description,
            "color": COLORS.get(module["tier"], 0),
            "fields": fields,
            "footer": {"text": "Bakshi's Bazaar"},
        }],
        "allowed_mentions": {"parse": []},
    }
    if role_id:
        payload["content"] = f"<@&{role_id}>"
        payload["allowed_mentions"]["roles"] = [role_id]
    return payload


def fetch_json(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Cache-Control": "no-cache"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def post(webhook, payload):
    body = json.dumps(payload).encode("utf-8")
    for attempt in range(2):
        request = urllib.request.Request(
            webhook + ("&" if "?" in webhook else "?") + "wait=true", data=body, method="POST",
            headers={"Content-Type": "application/json", "User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=30):
                return
        except urllib.error.HTTPError as error:
            if error.code == 429 and attempt == 0:
                retry = json.loads(error.read() or b"{}").get("retry_after", 5)
                time.sleep(min(float(retry), 30))
                continue
            raise


def write_summary(lines):
    text = "\n".join(lines) + "\n"
    print(text)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as handle:
            handle.write(text)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true", help="preview announcements without posting")
    args = parser.parse_args(argv)

    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    state = json.loads(STATE.read_text(encoding="utf-8"))
    main_hook = os.environ.get("DISCORD_WEBHOOK_URL", "").strip()
    hooks = {"free": main_hook, "premium": os.environ.get("DISCORD_WEBHOOK_URL_PREMIUM", "").strip() or main_hook}
    role_id = os.environ.get("DISCORD_ROLE_ID", "").strip()
    dry_run = args.dry_run or os.environ.get("DRY_RUN", "").lower() == "true" or not main_hook

    report = ["## Release announcements", ""]
    if dry_run:
        report += ["Preview only. Nothing was posted.", ""]
    failed = changed = False

    for module in config["modules"]:
        name, module_id = module["name"], module["id"]
        try:
            manifest = fetch_json(module["manifest"])
        except (urllib.error.URLError, OSError, ValueError) as error:
            print(f"::warning::{name}: could not read the published manifest ({error})")
            report.append(f"- {name}: could not read the published manifest")
            continue
        version = str(manifest.get("version", ""))
        if manifest.get("id") != module_id or not version_key(version):
            print(f"::warning::{name}: published manifest has an unexpected id or version")
            report.append(f"- {name}: published manifest has an unexpected id or version")
            continue

        announced = state.get(module_id)
        if announced is None:
            # First time this module is seen: record it without announcing old releases.
            report.append(f"- {name}: now tracking from V{version}")
            if not dry_run:
                state[module_id] = version
                changed = True
            continue
        if not is_newer(version, announced):
            report.append(f"- {name}: V{version}, already announced")
            continue

        changelog = ROOT / module["folder"] / "CHANGELOG.md"
        notes = changelog_section(changelog.read_text(encoding="utf-8"), version) if changelog.exists() else None
        if notes is None:
            print(f"::warning::{name}: no changelog section for V{version}; posting a short notice")
        payload = build_payload(module, manifest, notes, changelog_url(config["site"], module), role_id)

        if dry_run:
            report += [f"- {name}: **V{version} would be announced**", "", "```json",
                       json.dumps(payload, indent=2, ensure_ascii=False), "```", ""]
            continue
        try:
            post(hooks[module["tier"]], payload)
        except (urllib.error.URLError, OSError) as error:
            print(f"::error::{name}: Discord post failed ({error})")
            report.append(f"- {name}: V{version} post failed")
            failed = True
            continue
        state[module_id] = version
        changed = True
        report.append(f"- {name}: announced V{version}")

    if changed:
        STATE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
    write_summary(report)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

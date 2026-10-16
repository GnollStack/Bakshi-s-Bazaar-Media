import json
import unittest

import announce

CHANGELOG = """# Example changelog

History starts with the next release.

## Unreleased

- Work in progress.

## [14.2.1] - 2026-10-08

### Fixed

- Something now works.

## [14.2.0] - 2026-09-01

- Older notes.
"""

MODULE = {"id": "example", "name": "Example", "folder": "example", "tier": "premium",
          "manifest": "https://example.com/module.json", "page": "https://foundryvtt.com/packages/example"}
MANIFEST = {"id": "example", "version": "14.2.1",
            "compatibility": {"minimum": "14.369"},
            "relationships": {"systems": [{"id": "dnd5e", "compatibility": {"minimum": "6.0.6"}}]}}


class VersionTests(unittest.TestCase):
    def test_numeric_comparison(self):
        self.assertTrue(announce.is_newer("14.10.0", "14.9.9"))
        self.assertTrue(announce.is_newer("14.15.6", "14.15.5"))
        self.assertFalse(announce.is_newer("14.2.1", "14.2.1"))
        self.assertFalse(announce.is_newer("14.2.0", "14.2.1"))


class ChangelogTests(unittest.TestCase):
    def test_extracts_only_that_version(self):
        notes = announce.changelog_section(CHANGELOG, "14.2.1")
        self.assertEqual(notes, "### Fixed\n\n- Something now works.")

    def test_last_section(self):
        self.assertEqual(announce.changelog_section(CHANGELOG, "14.2.0"), "- Older notes.")

    def test_unbracketed_heading(self):
        self.assertEqual(announce.changelog_section("## 14.1.5 - 2026-09-23\n\n- Fixed.\n", "14.1.5"), "- Fixed.")

    def test_missing_version(self):
        self.assertIsNone(announce.changelog_section(CHANGELOG, "14.3.0"))

    def test_unreleased_is_never_matched(self):
        self.assertNotIn("Work in progress", announce.changelog_section(CHANGELOG, "14.2.1"))


class FormattingTests(unittest.TestCase):
    def test_headings_become_bold(self):
        self.assertEqual(announce.to_discord("### Fixed\n- a"), "**Fixed**\n- a")

    def test_trim_cuts_at_a_line(self):
        text = "\n".join(f"- line {n}" for n in range(1000))
        trimmed = announce.trim(text, 100)
        self.assertLessEqual(len(trimmed), 102)
        self.assertTrue(trimmed.endswith("\n…"))
        self.assertTrue(trimmed.splitlines()[-2].startswith("- line "))

    def test_requirements(self):
        self.assertEqual(announce.requirements(MANIFEST), "Foundry VTT 14.369+ · D&D5e 6.0.6+")


class PayloadTests(unittest.TestCase):
    def payload(self, role="", notes="### Fixed\n\n- Something now works."):
        return announce.build_payload(MODULE, MANIFEST, notes, "https://example.com/CHANGELOG.html", role)

    def test_embed_shape(self):
        embed = self.payload()["embeds"][0]
        self.assertEqual(embed["title"], "Example V14.2.1")
        self.assertIn("**Fixed**", embed["description"])
        self.assertEqual(embed["color"], announce.COLORS["premium"])
        self.assertIn("Foundry package page", embed["fields"][1]["value"])
        self.assertLessEqual(len(embed["description"]), 4096)

    def test_no_role_pings_nobody(self):
        payload = self.payload()
        self.assertNotIn("content", payload)
        self.assertEqual(payload["allowed_mentions"], {"parse": []})

    def test_role_ping_is_limited_to_that_role(self):
        payload = self.payload(role="123")
        self.assertEqual(payload["content"], "<@&123>")
        self.assertEqual(payload["allowed_mentions"], {"parse": [], "roles": ["123"]})

    def test_missing_notes(self):
        self.assertIn("V14.2.1 is out", self.payload(notes=None)["embeds"][0]["description"])


class ConfigTests(unittest.TestCase):
    def test_every_module_folder_is_configured(self):
        config = json.loads(announce.CONFIG.read_text(encoding="utf-8"))
        configured = {module["folder"] for module in config["modules"]}
        folders = {path.parent.name for path in announce.ROOT.glob("*/CHANGELOG.md")}
        self.assertEqual(folders, configured)

    def test_config_entries(self):
        config = json.loads(announce.CONFIG.read_text(encoding="utf-8"))
        state = json.loads(announce.STATE.read_text(encoding="utf-8"))
        for module in config["modules"]:
            self.assertIn(module["tier"], announce.COLORS, module["id"])
            self.assertTrue(module["manifest"].startswith("https://"), module["id"])
            self.assertTrue(announce.version_key(state.get(module["id"], "0")), module["id"])


if __name__ == "__main__":
    unittest.main()

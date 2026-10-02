# README, Package Listing, and Media Standard

Shared by all nine GnollStack modules. Each module keeps an identical copy at `LLM-Instructions/90-readme-listing-and-media.md`. The canonical copy is `tools/README-STANDARD.md` in the Bakshi-s-Bazaar-Media repository; change it there first, then copy it into every module.

Read this before editing `README.md`, `docs/README.html`, promotional media, or the `url`, `bugs`, `readme`, `changelog`, or `media` fields of `module.json`.

## What lives where

| Item | Location | Notes |
| --- | --- | --- |
| Public docs | `README.md` | GitHub page and the source for the Foundry listing. |
| Foundry package listing | `docs/README.html` | Generated from `README.md`. Never edit it by hand. Release allowlists keep it out of the module ZIP. |
| Promotional GIFs and screenshots | `GnollStack/Bakshi-s-Bazaar-Media` (local clone: `Desktop\Bakshi-s-Bazaar-Media`) | Public repository. Use raw URLs only. |
| Listing tool, shared tables, patron benefits | `Bakshi-s-Bazaar-Media/tools/` | `listing.py`, `listing-config.json`, `module-lists.json`. |

## The hand-written zone

The maintainer wrote the end of every README. Do not reword it, reorder it, or "tidy" it. Any change there needs the maintainer's explicit approval for that specific edit.

- **Premium modules and The Sound of Silence:** from `<a id="roadmap"></a>` to EOF.
- **Free modules without a Roadmap** (5e Item Importer, Show of Hands, Squad Combat Initiative): from `<a id="community"></a>` to EOF.

The zone holds Roadmap, Community, Contributing, AI-Assisted Development, Support Development, License & Permissions, Contact, and the footer.

**Approved changes made on 2026-09-30:**
- The free modules' Community section gained an "Ask on Discord" bullet.
- FileSmith's Community section gained the "Support is handled through the Bakshi’s Bazaar Discord" line, and its "Follow updates" bullet now points to Discord because the repository is private.
- Squad's old combined "Support" section was split into Community and Support Development, using only its existing lines.
- Every `##` title in the zone is wrapped in a centering `<div>`; no wording changed.
- In the free modules, the Support Development (Ko-fi) section is centered as a whole: its title's centering `<div>` closes after the quote instead of after the title. No wording changed.
- Third-person references to the author became first person: premium License sections say "contact me", and the free Contributing sections say "remain with me" and "I may adapt, decline, or implement submitted ideas."

**Procedure for any README edit:**
1. Copy the README first.
2. Afterwards, confirm the zone is byte-identical, or differs only by approved lines.
3. Preserve each line's own ending. Several READMEs and manifests mix CRLF and LF lines. Edit line by line, keeping each line's terminator.
4. Never use Git Bash `sed -i`, which converts CRLF to LF. Never re-dump `module.json` through a JSON serializer either; several manifests do not round-trip byte for byte.

## Section order

1. **Header** (centered `<div align="center">`):
   - Title.
   - Tagline: premium modules use **A premium Bakshi’s Bazaar module for Foundry VTT.**; free modules use their own hook.
   - Badges.
   - An italic one-line description.
   - A nav line using ` · ` separators, in section order.
2. **Feature Index**: a table with columns `Feature | What it does`, plus one italic intro sentence.
3. **Preview**: one hero image or GIF.
4. **Quick Start**: five numbered steps or fewer.
5. **Features**: one `###` subsection per feature, separated by `---`. The collapsed details blocks that close the section sit under `### More Details`. Squad is the exception: its whole Features section is details blocks with an intro, so it has no More Details heading.
6. **Use It For**: optional; free modules that already have it.
7. **Installation**: numbered steps plus a `Requirement | Version` table.
   - Premium modules add "Your Bazaar Patron membership includes:" with the shared benefits list.
   - Premium modules add the line "Updates install from Foundry's **Add-on Modules** screen like any other module. Release notes are posted in the Bakshi’s Bazaar Discord."
8. **Compatibility**: bold-label lines (**Foundry VTT:**, **Game system:**, and so on) and at most one details block for limits.
9. **Developer API**:
   - Free modules document their API and example macros.
   - Premium modules state that the `api` object serves the module's own integrations and diagnostics and isn't a supported public API, and point integration requests to Discord.
10. **Cross-promotion**: free modules have **Bakshi's Bazaar**; premium modules have **Free Modules**.
11. **The hand-written zone.**

**Badges:**
- **Premium:** version (static, linked to the Patreon join page), `Foundry v14`, and `Requires <system or library>` linked to `#installation`.
- **Free:** Latest Release, Downloads, Latest Downloads, Foundry, Ko-fi, Patreon (main page), and Discord.
- **Download badges count only the module's `.zip` release asset:** `https://img.shields.io/github/downloads/GnollStack/<Repo>/<module-id>.zip` and `…/<Repo>/latest/<module-id>.zip`. Never use `/total`, which also counts `module.json`; Foundry fetches that file on every update check, so it inflates the number by roughly ten times or more. If a release ever renames the zip, the badge stops counting it, so keep the asset name `<module-id>.zip`.

Premium READMEs no longer carry "Changes in x.y.z" blocks. Release notes are posted on Discord, and Custom Currency also keeps `CHANGELOG.md`.

## Layout and alignment

GitHub ignores CSS but honors `align="center"`. The listing tool turns it into centered styles.

- **Section titles:** every `##` title is centered. Wrap the title, together with the `<a id>` anchor(s) directly above it, in a centered div. `###` and lower headings stay left.
- **Feature Index:** the heading, table, and italic intro sentence share one centered block. The table separator is `| :--- | :--- |` so cell text stays left-aligned.
- **Cross-promotion intros:** the intro sentence under **Bakshi's Bazaar** and under **Free Modules** is italic and inside the title's centered block.
- **Media:** each standalone screenshot or GIF gets its own centered block. A "▶ Watch demo" link or a bold or italic caption directly attached to an image goes in the same block.
- **Not centered:** body text, lists, Quick Start, details blocks, and the hand-written zone's content. The exception is the free modules' Support Development (Ko-fi) section, which is centered as a whole.
- **Blank lines are required** inside every centered div, or GitHub will not render the Markdown in it.

```md
<div align="center">

<a id="new-section"></a>

## New Section

</div>

<div align="center">

![Alt text](https://raw.githubusercontent.com/GnollStack/Bakshi-s-Bazaar-Media/main/<folder>/images/<file>.png)

</div>
```

## Writing style

- Keep it plain and user-facing: say what a GM or player can do. Implementation detail, test evidence, and release logs belong in `LLM-Instructions/`, not the README.
- **Avoid these AI-isms:**
  - a bold slogan under every heading (keep one or two per README at most);
  - stacks of disclaimers such as "does not establish compatibility with every…";
  - the reflexive "X, not Y" construction;
  - em-dash headings;
  - filler such as "actually", "clean", or "seamless".
- Put MCP diagnostics in one collapsed "Diagnostics (MCP Bridge)" block. Developer-only notes go in "Notes for other module authors".
- **Apostrophes:** premium READMEs spell the brand "Bakshi’s" with a curly apostrophe, and IVFX uses curly apostrophes throughout. Free READMEs use straight apostrophes. `sync-lists` matches each file automatically.
- Never put prices in a README.
- Write about the author in the first person (I, me, my), never as "GnollStack", "the maintainer", or "the publisher". "GnollStack" stays only as a name: the **Author:** footer credit, the Discord handle, URLs, manifest author fields, and the license title "GnollStack Proprietary EULA". The same applies to shipped docs such as `docs/*.md`.

## Links and support routing

| Link | Target |
| --- | --- |
| Patreon discovery links: free modules' badge, Bakshi's Bazaar intro, companion mentions; premium manifests' `url` | `https://www.patreon.com/cw/GnollStack` |
| Patreon join links: premium version badge and Installation step 1 | `https://www.patreon.com/16504080/join` |
| Discord | `https://discord.gg/bGQDnyqYJ`. It must stay a non-expiring invite. |
| A premium module by name | Its Foundry package page, `https://foundryvtt.com/packages/<module-id>` |
| A free module by name | Its GitHub repository |

- Premium repositories are private, so never link GitHub URLs for premium modules.
- **Free modules:** bug reports go to GitHub issues. Everyone may ask in the Discord's public channels; patrons get patron-only channels and priority support.
- **Premium modules:** support is through Discord, and patrons receive priority support without guaranteed response times.

## Shared tables and patron benefits

`tools/module-lists.json` holds the premium list, the free list, the patron benefits, and per-module row overrides. Two READMEs have overrides: Item Importer's Activity Importer row and Activity Importer's Item Importer row.

Never edit those table rows or the benefits bullets by hand. Edit the JSON, then run `python tools/listing.py sync-lists`. It rewrites only those lines, keeps every other byte, and matches each file's apostrophe style.

**Adding a module:**
1. Add it to `tools/listing-config.json` (tier, and for free modules the GitHub URL).
2. Add it to `tools/module-lists.json`.
3. Create its media folder with `New-ModuleMedia.ps1`.
4. Run `sync-lists` and `build`.

## Package listing (`docs/README.html`)

Install the tool's dependencies once with `python -m pip install -r tools/requirements.txt`. Then run from the media repo:

| Command | Purpose |
| --- | --- |
| `python tools/listing.py build [module-id …]` | Regenerates listings from the READMEs. |
| `python tools/listing.py check [module-id …]` | Reports stale or broken listings (exits 1 on any problem). |
| `python tools/listing.py sync-lists` | Refreshes the shared tables and benefits. |

**What `build` does:**
- Converts centered divs to styles and gives centered tables auto margins.
- Uses the `<a id>` anchors as heading ids, so ids stay stable.
- Rewrites relative links: free modules link to their GitHub files; premium modules show "(`path` in the installed module)".
- Links each media-repo image to its full-size original, adds width and height, and lazy-loads every image after the first.
- Turns GitHub alerts into bold labels.
- Applies listing-only trims from `listing-config.json`. Item Importer's listing leaves out the validated YAML examples and links them on GitHub instead.
- Refuses to build when a README version disagrees with `module.json`.

**Release order:**
1. `sync-lists`
2. `build`
3. `check`
4. Commit `README.md` and `docs/README.html` together.

## Media

- **Hosting:** all promotional media lives in Bakshi-s-Bazaar-Media under `<folder>/gifs/` and `<folder>/images/`. Each folder's README lists its assets with alt text and direct URLs; update that table when adding files.
- **URLs:** use raw URLs (`https://raw.githubusercontent.com/GnollStack/Bakshi-s-Bazaar-Media/main/...`). Never use GitHub `/blob/` pages, `github.com/user-attachments` uploads, or local `Media/` or `gifs/` paths.
- **New filenames:** lowercase, hyphenated, and prefixed with the module ID.
- **Published files:** never rename or move them, because published listings link to them. Traffick's older copies stay in `immersive-vision/`, and new links use `traffick/`.
- **Before committing a README that uses new media:** push the media repo, then open each URL signed out to confirm it loads.
- **Free modules' screenshots** keep their display sizes through `<img width height>` attributes. Retina captures are shown at half their pixel size.

## Versions and release checks

Free modules use dynamic GitHub release badges. Every fixed version written in a README must match `module.json`. Bump the README in the same change as the manifest.

| Module | README version text | Check |
| --- | --- | --- |
| 5e Activity Importer | Version badge alt text and URL | `tools/Release-Contract.ps1` `Assert-ImporterReadmeVersion` (run by `Build-Release.ps1`; tests in `Test-ReleaseContract.ps1`; keep both importers' copies identical) |
| 5e Item Importer | None (dynamic badges) | Same shared contract |
| Custom Currency 5e, FileSmith, Traffick | Version badge alt text and URL | `tests/readme-version.test.mjs` (part of each module's test command) |
| Immersive Vision FX | Version badge and `**Version:** x` in Compatibility | `node tools/check-release.mjs` requires `**Version:** x` |
| Show of Hands | `` **Module version:** `x` `` in Compatibility and `**Version:** x` in the footer | `node --test tests/release-integrity.test.mjs` |
| Squad Combat Initiative, The Sound of Silence | None (dynamic badges) | `listing.py check` |

## Manifest metadata

| Field | Free modules | Premium modules |
| --- | --- | --- |
| `url` | GitHub repository | Patreon main page; FileSmith uses its Foundry package page |
| `bugs` | GitHub issues | Discord invite |
| `readme` | `README.md`; Show of Hands and Squad use their GitHub blob URL, and Show of Hands' contract pins it | `README.md` |
| `changelog` | GitHub releases page | Omitted; the repositories are private |
| `media` | Cover, then screenshots, then videos, with media-repo raw URLs and the alt text as caption | Same |

- **`media` field:** Foundry core documents only the `setup` media type (used on the setup screen). The other entries are metadata for listing sites and tools.
- **Pinned values:** some release contracts pin manifest values: Show of Hands pins `url`, `readme`, and `bugs`; IVFX pins `readme`. Run each module's release checks after any manifest edit.
- **Relative paths:** Activity Importer's and Item Importer's release verifiers require any relative `readme` or `changelog` path to be present in the release ZIP.

## Per-module facts

| Module | Tier | Hand-written zone starts at | Media folder | Notes |
| --- | --- | --- | --- | --- |
| 5e Activity Importer | Premium | `<a id="roadmap"></a>` | `activity-Importer-5e` | Developer API keeps both `developer-api` and `integration-support` anchors. |
| 5e Item Importer | Free | `<a id="community"></a>` | `5e-item-importer` | Uses Activity Importer's `Import-Full-Item.gif` in **Activity Importer Companion**; listing omits the validated YAML examples. |
| Custom Currency 5e | Premium | `<a id="roadmap"></a>` | `custom-currency-5e` | Its manifest and README mix CRLF and LF lines. |
| FileSmith | Premium | `<a id="roadmap"></a>` | `filesmith` | Old `docs/foundry-description.html` was replaced by `docs/README.html`. |
| Immersive Vision FX | Premium | `<a id="roadmap"></a>` | `immersive-vision` | URLs use the `refs/heads/main/` form; the folder also holds Traffick's legacy copies. |
| Show of Hands | Free | `<a id="community"></a>` | `show-of-hands` | `origin` is `GnollStack/Show-Of-Hands`; the legacy `target-the-beastie` name is migration-only. |
| Squad Combat Initiative | Free | `<a id="community"></a>` | `squad-combat-initiative` | Screenshots show the pre-14.2.0 compact headers and are captioned as such. |
| The Sound of Silence | Free | `<a id="roadmap"></a>` | `the-sound-of-silence` | `00-start-here.md` records the protected-zone SHA-256. |
| Traffick | Premium | `<a id="roadmap"></a>` | `traffick` | Trades move items only; the README says so, because Traffick doesn't handle coins or payment. |

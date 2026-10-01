# Bakshi's Bazaar Media

Public promotional GIFs and images for GnollStack's Foundry VTT modules.

Each module has its own folder. The module source code and installation packages live in their separate repositories.

```text
filesmith/
  README.md
  gifs/
  images/
_module-template/
  README.md
  gifs/
  images/
tools/
  listing.py
  listing-config.json
  module-lists.json
New-ModuleMedia.ps1
```

## Modules

Premium (Bakshi's Bazaar):

- [5e Activity Importer](activity-Importer-5e/README.md)
- [Custom Currency 5e](custom-currency-5e/README.md)
- [FileSmith](filesmith/README.md)
- [Immersive Vision FX](immersive-vision/README.md)
- [Traffick](traffick/README.md)

Free:

- [5e Item Importer](5e-item-importer/README.md)
- [Show of Hands](show-of-hands/README.md)
- [Squad Combat Initiative](squad-combat-initiative/README.md)
- [The Sound of Silence](the-sound-of-silence/README.md)

## Add another module

Open PowerShell in this repository and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\New-ModuleMedia.ps1 -ModuleId "your-module-id" -Title "Your Module Name"
```

The command copies `_module-template` into a new folder and fills in its name and example links. It will not overwrite an existing module folder.

You can also copy `_module-template` manually, rename the copy to the module's ID, and replace `__MODULE_ID__` and `__MODULE_TITLE__` in its README.

1. Put animated demos in the module's `gifs` folder and still images in `images`.
2. Use lowercase filenames with hyphens, such as `your-module-id-folder-demo.gif`.
3. Update the module's README with its media links and add it to the Modules list above.
4. Commit and push the new files using GitHub Desktop or Git.
5. Open each public image URL in a signed-out or private browser window before using it on a store page.

## Use media on a Foundry package page

Use the direct image URL in the editor's **Insert/Edit Image → Source** field. For example:

```text
https://raw.githubusercontent.com/GnollStack/Bakshi-s-Bazaar-Media/main/filesmith/gifs/filesmith-control-click.gif
```

Use the raw image URL, rather than a GitHub `/blob/` file-viewing page. The same URL can be used in an HTML `<img src="...">` tag.

Keep published filenames and folder paths stable. Replacing a file at the same path keeps existing links usable, although cached images can take a little while to update. Keep older files when introducing a new filename so existing descriptions continue to work.

The `.gitkeep` files only preserve empty folders in Git. They are not images and do not need to be uploaded into a description.

## Package listings and shared module tables

Each module's `docs/README.html` is the Foundry package listing, built from that module's `README.md`. Build it with `tools/listing.py` rather than editing the HTML by hand. The tool expects your modules in `%LOCALAPPDATA%\FoundryVTT\Data\modules`. Use `--modules-dir` or the `FOUNDRY_MODULES_DIR` environment variable if they live elsewhere.

Install the two dependencies once:

```powershell
python -m pip install -r tools/requirements.txt
```

| Command | What it does |
| --- | --- |
| `python tools/listing.py build` | Rebuilds every `docs/README.html`. Add module IDs to rebuild only those. |
| `python tools/listing.py check` | Reports listings that are out of date or have broken anchors, relative links, or unrendered Markdown. |
| `python tools/listing.py sync-lists` | Rewrites the **Bakshi's Bazaar** table in the free READMEs and the **Free Modules** table in the premium READMEs from `tools/module-lists.json`. |

- **Version check:** `build` and `check` stop if a README states a version (badge or **Version:** line) that differs from its `module.json`.
- **Listing rules:** `tools/listing-config.json` holds the per-module settings, such as each free module's GitHub URL for repository links and sections left out of a listing.
- **New module:** add it to `tools/listing-config.json`, and to `tools/module-lists.json` if it should appear in the shared tables.
- **Release order:** run `sync-lists`, then `build`, before each release, so the README and listing ship together.

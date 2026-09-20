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
New-ModuleMedia.ps1
```

## Modules

- [FileSmith](filesmith/README.md)

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

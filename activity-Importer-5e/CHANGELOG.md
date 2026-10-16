# 5e Activity Importer changelog

History starts with the next release. **Unreleased** lists changes that haven't shipped yet.

## Unreleased

### Import window improvements

- Previews show full mechanical detail by default, with an optional Compact view. The window remembers which panels you had open. Warnings and missing references always stay visible, and Version status collapses when everything is up to date.
- Templates, recipes and saved presets now share one picker with a Manage button. Auto-parse and Compare after import moved into Import options. The Activity and Effect tabs keep separate drafts and remember the target Item.
- Renamed **Parse** to **Preview** and **Dry Run** to **Check import**.
- Reference fields have inline search and drag-and-drop, plus a Resolve All button when references need resolving. Editing the source or a reference clears old check results.
- Import History is now optional and hidden by default (View options). Hiding it keeps your session entries and Undo. When it's turned on, it opens after each import.
- New **Import options > Restore defaults** resets the import and view settings. Your drafts, target Item, resolved references, presets and history are kept. Reset layout still only changes the layout.
- Updated the in-window instructions and authoring guides.

### 14.3.0 recipes and automation support

- New editable recipes in the template picker: conditional effects, filtered roll bonuses, AC calculations, minimum proficiency, effect expiry, area behaviors, transformations and shared effects.
- MIDI-QOL and DAE recipes appear when those modules are active. Loading a recipe asks before replacing your current draft and checks that the documents it needs exist.
- YAML schema 4 imports and exports MIDI-QOL activity settings and DAE effect settings, including inactive options, conditions, macros, overtime, region rules, lighting, stacking and expiry. Macros and conditions are never run while parsing, exporting or previewing.
- Linked activities are checked before anything is written. Missing, ambiguous or circular links are reported.
- External effect references stay external through import and undo.
- Fields the importer doesn't support now show an error. Previously they were dropped without warning.
- Updated previews, comparisons, field catalogs and the bundled authoring guides.
- Full-Item imports need Item Importer 14.3.0. Existing YAML still imports.
- Requirements are unchanged: Foundry 14.369 and D&D5e 6.0.6. Tested with MIDI-QOL and DAE 14.6.0.

### 14.2.0 compatibility update

- Now requires Foundry VTT 14.369 and D&D5e 6.0.6 (Foundry V14).
- Imports now keep activity descriptions, damage modifiers, Check and Save bonuses and visibility, effect expiry, area behaviors and Transform settings.
- Effects now keep their conditions, typed change values, origin details, magical status, riders and replacement context.
- Effects can link to embedded effects already on the Item or to external effect UUIDs. Check import validates the targets, and Undo removes only what that import created.
- Updated previews, comparisons, field catalogs and authoring references for D&D5e 6.
- Strict activity and effect exports now use YAML schema 3. Older YAML still imports. Full-Item imports need Item Importer 14.2.0.
- MIDI-QOL and DAE workflows need versions that support D&D5e 6. Tested with both at 14.6.0.

### Added

- This changelog, linked from the Foundry package page and the README.

### Changed

- Supports Foundry V14 only for now. I'll add newer Foundry versions after testing them.
- Updated the package description and author information.
- The module's website link now goes to its Foundry package page.

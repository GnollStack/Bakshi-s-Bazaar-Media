# 5e Item Importer changelog

History starts with the next release. **Unreleased** lists changes that haven't shipped yet.

## Unreleased

### Import window improvements

- Previews show full mechanical detail by default, with an optional Compact view. The window remembers which panels you had open. Parser findings are collected under Review, and the technical Parser details start collapsed. Warnings, missing references and batch controls always stay visible.
- Templates, recipes and saved presets now share one picker with a Manage button. Import options are grouped into parsing, comparison, images and automation, and image settings only appear when they apply. **Parse** is now **Preview**.
- The generated YAML editor is now optional (View options). Turn it on to see parsed values and defaults next to your natural-language text. **Use and preview** applies your edits, and copy/download exports the current preview even when the editor is hidden.
- Export errors are now reported, and an older parse can no longer overwrite a newer one.
- Import History is now optional and hidden by default. Turn it on for session entries, Undo and report downloads. Hiding it keeps the records.
- New **Import options > Restore defaults** resets the import and view settings. Your source text, unapplied YAML edits, destination, duplicate handling, presets and history are kept. Reset layout still only changes the layout.
- Destination and duplicate controls are always visible. The Activity Importer attachment builder only appears for a valid single-Item preview.
- Updated the in-window instructions and the natural-text and authoring guides.

### 14.3.0 recipes and automation support

- New free, editable Item recipes for multiple rarities and dawn/dusk charge recovery, plus a MIDI-QOL Item recipe when MIDI-QOL is active.
- With Activity Importer 14.3.0 installed, the template picker also offers complete-Item recipes that include its activities and effects.
- YAML schema 4 keeps MIDI-QOL Item flags and DAE Item macros. Full-Item export keeps Activity Importer's automation settings alongside native activities and effects.
- When updating an existing Item, an explicitly empty automation flag list clears the old values. Leaving it out keeps the existing flags.
- Keeps the 1.5× tool proficiency multiplier. Previews and comparisons now show supported automation settings.
- Updated templates, field catalogs and authoring guides. Older YAML still imports. The public API stays at version 3.
- Requirements are unchanged: Foundry 14.369 and D&D5e 6.0.6. Tested with MIDI-QOL and DAE 14.6.0.

### 14.2.0 compatibility update

- Now requires Foundry VTT 14.369 and D&D5e 6.0.6 (Foundry V14).
- Items with more than one rarity keep all of them through import, updates, export, preview and comparison. The old single-rarity format still works.
- Keeps damage modifiers and spell expiry settings, including deliberately empty, false or zero values.
- Fixed comparisons that reported untouched D&D5e 6 damage defaults as extra versatile damage.
- Updated the field catalogs for current D&D5e item, activity, effect and advancement data. These are reference updates and don't add new importable fields.
- Item YAML now uses schema 3. Older versions still import. Activity Importer 14.2.0 adds optional activity and effect attachments with the new fields.
- Before attaching, Item Importer checks that Activity Importer is new enough, so an outdated version can't drop fields without warning.

### Added

- This changelog, linked from the Foundry package page and the README.

### Changed

- Supports Foundry V14 only for now. I'll add newer Foundry versions after testing them.
- Updated the package description and author information.
- Fixed the description of the Activity Importer companion.

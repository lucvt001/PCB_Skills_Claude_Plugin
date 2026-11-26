# Print readability (PDF for readers without KiCad)

Read before laying out a sheet. The target is a printed page that someone outside the project can read without zooming.

## Export and page setup
- Plot, don't print: `kicad-cli sch export pdf --no-background-color --draw-hop-over` (searchable text, bookmarks, sheet links, hops at crossings). "Print to PDF" turns text into strokes. Keep the command in the README.
- Use one paper size for all sheets (A4 landscape by default). Fit content inside the frame, centred, clear of the title block. Changing the paper size moves content off the page, so plan a re-layout round right after.
- Fill the title block on every sheet: a title naming the function (generic on reused sheets), date, revision, company/project.
- Page numbers run in order with no gaps, each parent followed by its children; the root is 0.

## Text and boxes
- Every field, label, pin name, sheet name and note is at least 1.27 mm; box titles are 2.0 mm.
- Box rules:
  - the title sits top-left inside the box;
  - boxes don't overlap each other or the title block, with about 2.5 mm padding;
  - a wire crosses a frame only to reach a part inside that box, at a right angle; it never runs along a frame or through a foreign box.
- Outputs and connectors sit in one aligned right-hand column.
- Test points and PWR_FLAGs go in one "Test points and power flags" box at the bottom of each page, connected through power symbols or a label with the net's name.
- Mounting holes and net ties go on the root sheet.
- Root: wire sheet pin to sheet pin; draw crossings that can't be avoided as a grid and export with hop-overs.
- When labels are replaced by wires, keep the existing label text on the wire as a name tag, so net names stay stable.

## Symbols and grounds
- Use full-size `Device:R`/`C`/`C_Polarized`, not `_Small`. Their pins sit at ±3.81 mm, not ±2.54 mm, so re-attach the wires.
- Ground is a triangle with its name visible (`GND1`, `GND2`).
- Reused sheets on different grounds take ground through a `GND` sheet pin (input) and draw it inside with a sheet-local power symbol (KiCad 9+ `(power local)`); the parent's net name wins.
- Point power and ground symbols away from their wire, never onto a part body or the next pin row.
- Field text on rotated or mirrored symbols:
  - stored angle and justification are relative to the symbol;
  - `(mirror y)` flips left/right justification;
  - `fields_autoplaced` can override manual positions;
  - verify on a render.
- Multi-unit parts show their Value once.

## Values
- Make every Value visible.
- Resistors use the IEC 60062 RKM code: `10R`, `47R`, `4k7`, `100k`, and `3m` for 3 mΩ. Capacitors are value, one space, voltage: `100n 100V`, `100u 6V3` (no dot or comma).
- Connectors show the manufacturer part number. Parts without one get a short description (`Open`/`Bridged`, `M3`, the module name).
- Check every passive's Value against the value coded in its part number or LCSC part. Keep a single part-number field per symbol.

## Notes
- Notes are for the reader: 1-3 lines on what the circuit does, with its key values, thresholds and currents.
- Decision IDs, evidence tags, history, file paths and derivations go in the companion document.
- Never invent a number. Flag old notes that contradict the design docs instead of silently fixing them.
- On reused sheets, don't name per-instance references in notes.

## Re-annotation (page × 100 + n)
- Edit only the instance `reference` entries and the Reference property; symbol and pin UUIDs stay, so Update PCB renames footprints in place.
- Write an old-to-new map (CSV).
- Update references in notes, the README and the sourcing lock, including references after a `\n` line break and inside ranges (`H307-H310`).
- Ask how the root sheet's parts are numbered.

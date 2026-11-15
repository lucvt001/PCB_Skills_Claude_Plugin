# Footprint assignment (KiCad)

Assign and check a footprint for every symbol once its exact MPN is chosen. Read the datasheet package drawing and recommended land pattern from `pcb/datasheets/` first.

## Where footprints come from (in order)

1. KiCad standard libraries, when the package matches the datasheet exactly.
2. Manufacturer/LCSC/JLCPCB footprint, copied into `pcb/project.pretty` (registered in `fp-lib-table`), never referenced from a download folder.
3. Search online (SnapEDA, Ultra Librarian, Component Search Engine, manufacturer site, EasyEDA/LCSC import) and copy the result into `pcb/project.pretty/`.

- **Never create custom footprints or symbols; default to searching online.** Do not draw a footprint or symbol from the datasheet yourself, and do not call `create_footprint` / `create_symbol`. If nothing usable turns up after searching, stop and ask the user rather than drawing one. Downloaded parts still go through the checks below.
- Symbols come the same way into `pcb/sym/`. 3D models are optional, in `pcb/step/`, not reviewed.

## Check every assignment

| check | how |
|---|---|
| package matches MPN suffix | datasheet ordering table vs footprint name |
| land pattern | pad size, pitch, row span, exposed pad vs datasheet recommendation |
| pad numbering | each footprint pad maps to the symbol pin of the same function (datasheet pin table); mismatches are invisible to ERC and netlist checks |
| pin 1 and polarity | marked on silk **and** Fab; diode/LED/electrolytic/tantalum polarity matches symbol |
| body outline | Fab outline and courtyard match the drawing body in plan view |
| exposed pad | right net, paste reduced/windowed per datasheet, thermal vias if required |
| origin and rotation | origin at package centre; zero orientation per IPC-7351 (pin 1 top-left for ICs) so JLCPCB CPL corrections stay predictable |
| assembly-tier limits | package size and pitch within the selected JLCPCB PCBA tier |

- Record results in the sourcing lock's `footprint`, `package_verified`, `pinout_verified` columns.
- Any footprint change after placement invalidates placement and everything after.

## Confirm in the netlist

Export a fresh netlist; confirm every component has a non-empty footprint resolving in the project library tables, from exported files or `kicad-cli` output, not the canvas.

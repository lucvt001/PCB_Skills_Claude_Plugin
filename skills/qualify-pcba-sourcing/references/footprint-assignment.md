# Footprint assignment (KiCad)

Assign and check a footprint for every symbol once its exact MPN is chosen. Read the datasheet package drawing and recommended land pattern from `pcb/datasheets/` first.

## Where footprints come from (in order)

1. KiCad standard libraries, when the package matches the datasheet exactly.
2. Manufacturer/LCSC/JLCPCB footprint, copied into `pcb/project.pretty` (registered in `fp-lib-table`), never referenced from a download folder.
3. Drawn from the datasheet's recommended land pattern (IPC-7351 naming, zero orientation), saved in `pcb/project.pretty/`.

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

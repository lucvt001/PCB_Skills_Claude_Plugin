# Drawing a new schematic in KiCad

For creating a schematic or new sheet, not reviewing one. Rules on datasheets, hierarchy, designators, value formats, ask-the-user, and sheet arrangement: [schematic-rules.md](schematic-rules.md).

## Before drawing

1. Brief and architecture exist (or run `/plan-electronic-product`).
2. Datasheets (and EVM PDFs) for every IC, module, regulator, connector are in `pcb/datasheets/` and read.
3. Plan hierarchy: one sheet per functional block (power input, regulators, MCU, comms, motor drive, sensors, connectors); list each sheet's hierarchical signals and directions first.

## Sheets and connections

- **Root sheet:** block diagram of sheet symbols with sheet pins wired together. The root sheet is always sheet 0; subsheets continue from there (1, 2, 3, ...), set the page numbers explicitly.
- **Between sheets:** hierarchical labels and sheet pins, correctly typed (input/output/bidirectional/passive). No global labels.
- **Power:** KiCad power symbols (`+3V3`, `+5V`, `VBAT`, `GND`), same names on all sheets. `PWR_FLAG` only where a rail is really driven by a connector/regulator ERC can't see.
- **Within a sheet:** wires for local connections; local labels only for long or repeated connections (buses).
- **Net names:** name every meaningful net (`CAN1_H`, `MOTOR_A`, `I2C1_SDA`) for readable assertions and layout.
- **Unused pins:** no-connect flag on every deliberately open pin (checked against datasheet) so ERC flags the rest.

## Symbols and fields

- Standard KiCad symbols when the pinout matches the exact part; else search online (SnapEDA, Ultra Librarian, manufacturer, EasyEDA/LCSC import) and copy it into `pcb/sym/`. **Never create custom symbols or footprints; default to searching online.** If nothing usable is found, ask the user. Check the pin types of any downloaded symbol (power in/out, input, output, bidirectional, passive, open collector) against the datasheet so ERC is meaningful.
- Fields: Value; `MPN` and `LCSC` (filled in sourcing); `Datasheet` pointing to `pcb/datasheets/`. Footprints may be provisional; sourcing assigns final ones.
- **Value strings:** no dot or comma as a decimal separator (they break CSV/BOM parsing and locale handling). Use the unit letter as the decimal point (`4k7`, `2R2`, `0R`, `1M5`, `3V3`). Do not use underscores in values, except in capacitors (below).
- **Capacitors:** always spell out capacitance followed by voltage rating, separated by an underscore, e.g. `10u_100V`, `100n_50V`, `4u7_16V`. Never a bare capacitance. The underscore is used only here, as the separator between capacitance and voltage.
- Mark DNP parts (hedges, optional termination) with KiCad's DNP attribute.

## Annotation and checks

- Annotate every design as sheet number x 100 + increment ("Use first free number after sheet number x 100"); root sheet 0 gives R1, C1, U1, sheet 1 gives R101, and so on.
- ERC with all severities; fix or explain every item; never silence pin-type warnings by changing pins to passive.
- Export KiCad XML netlist, write `netlist-assertions.json` from design intent, run `<skill-dir>/scripts/assert_netlist.py`.
- Export schematic PDF and check each page is readable (else `/schematic-humanizer`).

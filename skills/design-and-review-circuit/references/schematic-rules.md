# Schematic rules

- **Datasheets first.**
  - Read each part's datasheet in `pcb/datasheets/` before designing/reviewing its circuit; also its EVM/EVK PDF if present (use as reference design; record deviations in `DECISIONS.md`).
  - Name files `<MPN>.pdf`, `<MPN>_EVM.pdf`.
  - Contents page first, then only: pin table, abs max and recommended conditions, electrical characteristics, application circuit, component selection, layout guidelines.
  - Missing: ask the user for it or for permission to download from the manufacturer.
- **Hierarchy for large designs** (>1 page or ~40+ parts): one sheet per functional block, hierarchical labels and sheet pins on the parent. No global labels between sheets; power rails may use power symbols.
- **Sheet numbering:** root sheet is sheet 0; subsheets continue from there (1, 2, 3, ...).
- **Designators:** sheet number x 100 + increment (root/sheet 0: R1, R2, C1, U1; sheet 1: R101, C101, U101; sheet 2: R201, C201, U201). Annotate with "Use first free number after sheet number x 100". Split a sheet needing >99 of one prefix.
- **Ask, don't assume, selectable IC options:** EN polarity/tie/divider, PG/open-drain use, UVLO thresholds, mode/config pins, address pins, soft-start, switching frequency, connector types and pinouts, etc. List datasheet options with a recommendation. Don't ask about capacitor ratings or other small details.
- **Capacitor Value field:** capacitance then voltage: `1u_50V`, `100n_16V`, `22p_50V`.
- **Standard values:** resistors E12 or E24 only, so JLCPCB Basic parts exist for every value (pick the nearest E12/E24 value and recheck the calculation; E96 or other values only with a stated reason, and then check Basic availability); capacitors E6/E12 (1u, 2.2u, 4.7u, 10u, 22u, 47u, 100n).
- **Sheet arrangement:** main IC in the middle, support circuitry around it, one titled dashed box per functional sub-circuit holding only the equation or datasheet rationale (no part numbers, no prose), with datasheet/EVM source section/page tagged; text 40 mil (1.016 mm), titles 70 mil (1.778 mm). Keep each sub-circuit's wiring to the IC compact and visible for datasheet cross-check. See `schematic-humanizer`.
- Each part carries `MPN` and `LCSC` once sourcing has run.

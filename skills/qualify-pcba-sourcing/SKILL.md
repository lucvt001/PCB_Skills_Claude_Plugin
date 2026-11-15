---
name: qualify-pcba-sourcing
description: Verify MPNs, LCSC/JLCPCB parts, stock, Basic/Extended class, cost, substitutes, and KiCad footprint assignment.
---

# PCBA Sourcing Qualifier

> `${CLAUDE_SKILL_DIR}`: scripts in `scripts/`, sibling skills in the parent folder. In references, `<skill-dir>` = this directory, `<skills>` = its parent. Run scripts from `pcb/` (or use absolute paths).

Create `.pcba-workflow/sourcing-lock.csv` from [assets/sourcing-lock.csv](assets/sourcing-lock.csv). Stock and price are time-sensitive: browse current manufacturer and supplier sources, not memory. Read each part's datasheet (and EVM PDF if in `pcb/datasheets/`) before qualifying. Default assembly is JLCPCB PCBA; read [pcba-cost-and-stock.md](references/pcba-cost-and-stock.md) before comparing parts.

## Part selection

**JLCPCB Basic is strongly preferred**: each Extended part type adds a loading fee. Use Extended only when no Basic part meets the requirement; record why in `DECISIONS.md` with the rejected Basic options. Priority:

1. Meets the electrical requirement with margin (value, tolerance, voltage, current, power at real operating point and temperature).
2. JLCPCB Basic and in assembly stock.
3. Smallest package satisfying 1-2, within the selected assembly tier's minimum size (generic parts: normally the smallest Basic size).

Basic outranks size: if a value is Basic only in a larger package, use it. Go larger when the part handles power or stress:

- **Resistors:** P = I²R (or V²/R) at most ~half rated power (datasheet, VERIFIED); check max working voltage on high-rail dividers; size shunts by power and pulse rating.
- **Capacitors:** voltage rating ~1.5-2x working voltage; derate ceramics for DC bias; bulk/high-voltage usually need a larger case.
- **Inductors, ferrites, fuses, diodes, MOSFETs:** by saturation/rated current, dissipation, thermal path.
- **Connectors/mechanical:** by mating, current, strength.

## Workflow

1. Read brief, architecture, `DECISIONS.md`, schematic/netlist, BOM, layout, quantity; derive the real requirement first.
2. Per populated reference record: manufacturer, orderable MPN, LCSC number, package drawing, footprint, pin semantics, electrical/timing requirements, lifecycle, CAD status. Resolve each LCSC/MPN to its live page and confirm it's the intended part.
3. Record JLCPCB assembly stock + timestamp, MOQ, price break, Basic/Extended class (as billed on the page), per-board and assembled quantities, attrition/minimum loading, order quantity, parts cost, setup/loading charges, reconciled line and total cost. Hand-fit parts: **retail** stock, pack-rounded totals.
4. Apply the selection rules to every line. Compare on total assembled-order cost (compute break-even loading fee before reading the live one); consolidate values onto Basic parts where possible.
5. Sanity-check ratings against physics and the real operating point (supply range, dropout, saturation, temperature).
6. Treat memories, programmables, modules, regulators, translators, connectors, sensors, protection, timing-critical parts as design-critical unless evidence says otherwise.
7. Alternates: read [substitution-gate.md](references/substitution-gate.md). Compare every pin and package dimension (family names or pin counts are not evidence); look for pin- and land-compatible parts first. Record requested and selected MPN; a different MPN must be listed, explicitly approved, and tied to approval evidence in the lock.
8. Check every part against the JLCPCB tier's package, pitch, side limits; check each connector's mating half is sourced.
9. **Assign and check footprints** per [footprint-assignment.md](references/footprint-assignment.md): land pattern and pad numbering vs datasheet, pin-1/polarity, body outline, exposed pad, origin/rotation. Write `MPN` and `LCSC` fields on each symbol.
10. Classify each line `PASS`/`BLOCKED`/`USER_REVIEW`; a critical alternate always needs explicit design-owner approval.
11. Run `${CLAUDE_SKILL_DIR}/scripts/validate_sourcing_lock.py` with a suitable live-data age limit.

## Gate

- Don't freeze circuit or placement while a critical MPN, pinout, package, footprint, CAD model, lifecycle, or availability is unresolved.
- A selected MPN/package change invalidates the circuit and all downstream artifacts. A stock/price-only refresh invalidates sourcing and order approval only.
- Report dated evidence, line and total cost (VERIFIED or ESTIMATE), risk, substitution class, unresolved items. Never silently change a released BOM or website match.
- `/adversarial-review` of the lock only on request; otherwise `USER_REVIEW` until the user accepts.

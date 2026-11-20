# Linear regulators (LDOs)

**Read when:** any LDO or linear regulator, voltage reference with output cap requirements.
**Also read:** `thermal-power-parts.md` if dissipation is more than a few hundred mW.

## Placement

- Input and output caps at the pins, of the type and ESR the datasheet requires for stability.
- Compute dissipation P = (Vin - Vout) x I at worst case before placement; give the part room for the copper it needs.

## Routing

- Short, wide connections from the caps to the pins and to GND.
- Tab/thermal pad: copper area and vias for the computed P (`thermal-power-parts.md`).

## Verify

- Cap type/ESR matches the datasheet; P recorded `[COMPUTED]`.

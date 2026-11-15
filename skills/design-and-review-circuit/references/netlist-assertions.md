# Netlist intent assertions

Adapted from `daishuge/pcb-skill` (MIT, see `../LICENSE-pcb-skill`).

ERC can pass with zero errors while nets resolve consistently to the wrong thing. On the reference project five nets were silently merged (a switch node into a card supply; I2S data and UART TX into ground); only assertions on the EDA's exported netlist caught it. Gate the schematic on **intent**, not ERC alone.

## What to assert

| class | meaning | catches |
|---|---|---|
| `must_connect` | pin (ref, pin) is on net N | missing/mis-labelled connections |
| `must_not_connect` | pins A and B are on different nets | silent merges, shorts |
| `must_be_open` | pin has no connection to any other pin | stray labels on NC pins |
| `net_pin_counts` | net N has exactly k pins | merged (too many) or split (too few) nets |

- Write negative assertions too: a design never asked a must-not-connect question hasn't been checked for shorts. Candidates: every rail vs GND and vs every other rail; every switch node vs its input and output; each bus data line vs its neighbours; any connector pin carrying a different voltage domain.
- Write from **design intent** (architecture, datasheet pin tables, connector pinouts), not by copying the current netlist; copying makes a wrong netlist the expected answer.

## File format

`.pcba-workflow/netlist-assertions.json`:

```json
{
  "schema": "netlist-assertions-v1",
  "must_connect": [
    {"ref": "U1", "pin": "1", "net": "+3V3"},
    {"ref": "J1", "pin": "A6", "net": "USB_DP"}
  ],
  "must_not_connect": [
    {"a": {"ref": "U1", "pin": "1"}, "b": {"ref": "U1", "pin": "8"}}
  ],
  "must_be_open": [
    {"ref": "U3", "pin": "7"}
  ],
  "net_pin_counts": {"+3V3": 14, "USB_DP": 3}
}
```

- Pins are netlist pad numbers (e.g. `A6`), not pin names.
- Net names as KiCad exports them: hierarchical-label nets carry the sheet path (`/Power/VBAT`); power-symbol nets keep plain names (`+3V3`, `GND`).
- References follow the sheet number x 100 scheme, root sheet 0 (`U1`, `U101`, `R203`).

## Running it

```bash
"$K" sch export netlist --format kicadxml -o ../.pcba-workflow/netlist.xml template.kicad_sch
python <skills>/design-and-review-circuit/scripts/assert_netlist.py \
  ../.pcba-workflow/netlist.xml ../.pcba-workflow/netlist-assertions.json
```

- Exit 0 = all pass; 1 = assertion failed (gate BLOCKED); 2 = bad input.
- Refuses an empty file, and a file with no `must_not_connect` unless `--allow-no-negative`. Also accepts `schematic-connectivity-v1` JSON.
- Limits: sees only the netlist. A must-connect through a series part correctly fails (assert each side). Footprint pad numbering that differs from symbol pin numbering is invisible; check pad-by-pad against footprint/datasheet.

## Also part of the schematic gate

- Every footprint resolves (no missing library entries), from the exported netlist or `kicad-cli` output, not the canvas.
- BOM reconciles against the sourcing lock; every deliberate substitution has a written reason.
- Save, close KiCad, reopen, re-export before calling the gate; the running session is not evidence about the saved file.

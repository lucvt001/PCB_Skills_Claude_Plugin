# High-voltage clearance

**Read when:** any net pair with a peak difference >= 31 V (battery packs, motor buses, mains-derived rails, PoE, transients), or a wet/condensing environment.

## Rule

Pick the row for each net pair's **peak** voltage difference (DC or AC peak incl. transients). IPC-2221B Table 6-1 minimum spacing, mm `[as commonly reproduced; confirm against the standard above 50 V]`:

| voltage (V peak) | B1 internal | B2 external, uncoated (<3050 m) | B4 external, permanent polymer coating | A5 external, conformal-coated assembly | A6 component lead, uncoated |
|---|---|---|---|---|---|
| 0-15 | 0.05 | 0.1 | 0.05 | 0.13 | 0.13 |
| 16-30 | 0.05 | 0.1 | 0.05 | 0.13 | 0.25 |
| 31-50 | 0.1 | 0.6 | 0.13 | 0.13 | 0.4 |
| 51-100 | 0.1 | 0.6 | 0.13 | 0.13 | 0.5 |
| 101-150 | 0.2 | 0.6 | 0.4 | 0.4 | 0.8 |
| 151-170 | 0.2 | 1.25 | 0.4 | 0.4 | 0.8 |
| 171-250 | 0.2 | 1.25 | 0.4 | 0.4 | 0.8 |
| 251-300 | 0.2 | 1.25 | 0.4 | 0.4 | 0.8 |
| 301-500 | 0.25 | 2.5 | 0.8 | 0.8 | 1.5 |

## Placement

- Group high-voltage parts so their clearance zone doesn't cut through low-voltage corridors.

## Routing

- Outer layers = **B2 (uncoated)** unless conformally coated; solder mask alone isn't normally a permanent coating.
- **A6** for exposed pads and component leads.
- **Flag, don't apply:** list every net pair >= 31 V with the table value and ask the user before creating an HV net class (`board-defaults.md` section 2). The 0.3 mm pour clearance covers outer-layer uncoated spacing only up to 30 V; traces and pads use the smaller template clearance.
- Wet/condensing environments (a hull that may leak or sweat) need more margin; safety-rated isolation needs creepage per the relevant safety standard, not IPC-2221.

## Verify

- Every HV net flagged to the user; if an HV net class was approved, DRC run with it.

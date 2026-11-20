# Power routing and copper pours

**Read when:** every board (all boards have power and GND): routing any rail, sizing power traces, placing power vias, drawing zones/pours/planes, GND stitching.
**Also read:** `battery-input-and-protection.md` for the main supply entry, `thermal-power-parts.md` for hot parts, `high-voltage-clearance.md` for rails >= 31 V.

## Placement

- Lay out the power tree as a corridor: source → protection → regulators → loads, without needless backtracking.
- Reserve power fanout room (vias, short wide stubs) around dense ICs before signal routing claims it.
- Spread power vias along the current path in the floorplan; don't plan to cluster them.

## Routing: trace width vs current

Up to 1 A, use the width ladder in `board-defaults.md` section 3 and don't calculate. **Above 1 A use a copper pour** (`board-defaults.md` section 6) and size its narrowest neck with the table below.

Use IPC-2152 (or a calculator based on it) for final sizing; the IPC-2221 formula below is conservative near planes, so a safe first pass.

`I = k x dT^0.44 x A^0.725`, A in mil², k = 0.048 (external) / 0.024 (internal); 1 oz = 35 um = 1.378 mil. `[COMPUTED from IPC-2221]`

| current (A) | ext 1 oz, +10 C | ext 1 oz, +20 C | ext 2 oz, +10 C | int 0.5 oz, +10 C | int 1 oz, +10 C |
|---|---|---|---|---|---|
| 0.5 | 0.12 mm | 0.08 | 0.06 | 0.60 | 0.30 |
| 1 | 0.30 | 0.20 | 0.15 | 1.56 | 0.78 |
| 2 | 0.78 | 0.51 | 0.39 | 4.07 | 2.03 |
| 3 | 1.37 | 0.90 | 0.68 | 7.11 | 3.56 |
| 5 | 2.77 | 1.82 | 1.38 | 14.4 | 7.19 |
| 10 | 7.19 | 4.72 | 3.60 | 37.4 | 18.7 |
| 15 | 12.6 | 8.26 | 6.29 | 65.5 | 32.7 |
| 20 | 18.7 | 12.3 | 9.36 | 97.4 | 48.7 |

- Size every > 1 A path for **worst-case** current from the power budget; note the chosen temperature rise.
- Inner layers are thin (0.5 oz on standard 4-layer) and poorly cooled: put high current on outer layers/pours; order 2 oz outer copper if needed.
- In every high-current pour check the **narrowest neck** (connector pins, fuse pads, between vias): it sets the rise.
- Check voltage drop: R = rho x L / (w x t), rho(Cu) = 1.72e-8 Ohm·m at 20 C (~0.5 mOhm/square for 1 oz). `[COMPUTED]`

## Routing: vias for current

- Barrel copper area ≈ `pi x drill x plating thickness`; a 0.3 mm drill with 18-25 um plating ≈ 1.4-1.8 A at +10 C (IPC-2221 external) `[COMPUTED; plating thickness ESTIMATE - check JLCPCB spec]`.
- **At least 2 vias per amp** at every power layer change (plating variation, current crowding); more under thermal pads.
- Spread power vias along the current path, not clustered.

## Routing: pours, planes, stitching

- Pour settings (solid fill, 0.3 mm clearance, 0.2 mm fillet, solid pad connection, few vertices, two-layer high-current zones): `board-defaults.md` section 6.
- **Fill leftover outer-layer area with ground pour.**
- Stitch outer GND pours to the plane with vias every few mm along edges and around pour islands; delete GND islands that can't be stitched.
- **Non-ground vias and their paired ground vias:** follow `board-defaults.md` section 5 "Stitching / pour-edge vias" exactly (ring tangent to the pour edge, ground via across it at 0.3 mm ring-to-ring).
- On boards with motor or switching stages, a row of GND vias along the board edge helps contain noise.

## Verify

- Width, neck, voltage drop, and via count recorded per rail with current and temperature rise used; the source (regulator, connector, fuse) can supply that current.
- Zone connectivity proof per `general-rules.md` section 7.

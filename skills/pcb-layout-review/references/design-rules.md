# Design rules for the template's 4-layer JLCPCB board

For net classes, power-path sizing, clearances, controlled-impedance pairs. Fab minimums and the default net class live in `pcb/template.kicad_pro` (not repeated here). Every number is a starting point; confirm against current JLCPCB pages and datasheets.

## 1. Stackup and layer assignment

| layer | use |
|---|---|
| F.Cu | components, short signals, local power |
| In1.Cu | **solid GND plane**, reference for F.Cu; no routing except unavoidable short jumps |
| In2.Cu | **solid GND plane**, reference for B.Cu |
| B.Cu | signal and power routing/pours, referenced to In2.Cu |

- **Project rule:** outer layers carry signal and power; both inner layers are ground. Route power as traces/pours on outer layers.
- Solid GND on In1 beats a dedicated low-current power plane; for mostly low-current rails use GND on In1 and In2 and wide outer-layer power.
- Never route fast/controlled-impedance signals across a split or void in the reference plane. At a layer change put a GND stitching via within ~1-2 mm of the signal via.
- **Check the stored stackup before impedance work.** The template stores a generic stackup (three 0.48 mm FR4 dielectrics, 35 um copper on all four layers). JLCPCB standard 4-layer stackups (e.g. JLC04161H-7628) have thin prepreg between each outer layer and its plane and 0.5 oz inner copper `[ESTIMATE - read real values from jlcpcb.com/impedance]`. Set the KiCad stackup to the one you'll select on the order form and record it in the order-form checklist.

## 2. Trace width vs current

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

- Size every power path for **worst-case** current from the power budget; note the chosen temperature rise.
- Inner layers are thin (0.5 oz standard 4-layer) and poorly cooled: put high current on outer layers/pours; order 2 oz outer copper if needed.
- Above a few amps use pours, and check the **narrowest neck** (connector pins, fuse pads, between vias); it sets the rise.
- Check voltage drop: R = rho x L / (w x t), rho(Cu) = 1.72e-8 Ohm·m at 20 C (~0.5 mOhm/square for 1 oz). `[COMPUTED]`
- Battery/motor paths: also check connector and fuse current rating and the pad size they need.

## 3. Vias for current

- Barrel copper area ≈ `pi x drill x plating thickness`; 0.3 mm drill with 18-25 um plating ≈ 1.4-1.8 A at +10 C (IPC-2221 external) `[COMPUTED; plating thickness ESTIMATE - check JLCPCB spec]`.
- **At least 2 vias per amp** for power layer changes (plating variation, current crowding); more under thermal pads.
- Spread power vias along the current path, not clustered.
- Every via counts toward drill count; check the fab surcharge threshold (`release-pcba-fabrication/references/jlcpcb-constraints.md`).

## 4. Clearance vs voltage

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

- Outer layers = **B2 (uncoated)** unless conformally coated; solder mask alone isn't normally a permanent coating.
- **A6** for exposed pads and component leads.
- Template default 0.127 mm clearance is fine for low voltage but **not** ≥31 V on outer layers (B2 needs 0.6 mm): create a battery/motor-bus net class with clearance from this table.
- Wet/condensing environments (hull that may leak or sweat) need more margin; safety-rated isolation needs creepage per the relevant safety standard, not IPC-2221.

## 5. Controlled impedance

| interface | target | notes |
|---|---|---|
| USB 2.0 FS/HS data | 90 Ohm differential, ±10 % | FS tolerates loose control; HS needs it |
| Ethernet 10/100 (PHY to magnetics) | 100 Ohm differential | match within pair; keep short |
| CAN, RS-485 | ~120 Ohm differential | on-board length short; termination matters more than geometry |
| RF feed | 50 Ohm single-ended | follow the module's reference layout exactly |

- Get widths/gaps from **JLCPCB's impedance calculator** for the exact stackup and copper weight you'll order; set them in the KiCad net class/differential-pair settings; never reuse widths from another stackup.
- Select impedance control on the order form if needed and name the stackup.
- Route each pair over a continuous plane, no stubs, symmetric spacing, intra-pair length matching to the interface requirement (small serpentines only where needed).

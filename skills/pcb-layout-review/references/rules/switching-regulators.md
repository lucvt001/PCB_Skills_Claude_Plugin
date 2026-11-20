# Switching regulators (buck, boost, buck-boost, inverting)

**Read when:** any switching converter or controller, an inductor in a power path, an `SW`/`LX`/`PH` net.
**Also read:** `thermal-power-parts.md` (IC thermal pad, MOSFETs), `power-routing-and-pours.md`.

## Placement

- **Copy the EVM/reference layout when one exists.** The datasheet layout section overrides this file.
- Identify the **hot loop** from the datasheet (buck: input cap → high-side switch → low-side switch/diode → back to input cap GND; boost: output cap → switch → diode/sync FET → output cap). Place to make it as small as possible, all on one layer, input-cap GND and IC GND adjacent.
- Inductor close to SW; output caps close to inductor and load.
- Feedback divider close to the FB pin.
- Keep analog, feedback, crystals, and sensitive signals away from SW and the inductor.

## Routing

- Hot loop on one layer, no vias in it.
- Switch-node (SW) copper as small as the current allows; nothing on the adjacent layer under SW except GND.
- Feedback trace from the **output capacitor** (regulation point), routed away from SW and the inductor.
- Thermal pad: solid GND connection with the datasheet's via count (pattern per `thermal-power-parts.md`).

## Verify

- Hot loop identified and its area/route shown in the placement stop.
- FB sense point is the output cap, not the inductor or SW copper.

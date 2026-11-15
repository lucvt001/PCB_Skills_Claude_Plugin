# Layout patterns

Read only the section for the block you're placing/routing. The part's datasheet layout guidelines and EVM layout override anything here.

## Decoupling

- Order along the current path: **supply pin → capacitor → via to GND plane**, smallest capacitor closest to the pin; its GND via right at its pad, not shared through a long trace.
- One small cap (typically 100 nF) per supply pin/pair, same side as the IC where possible; bulk (e.g. 4.7-10 uF) per rail near the IC group.
- No via between pin and capacitor unless the capacitor is directly under the pin on the other side.
- Two vias per capacitor pad on fast or high-current rails.

## Switching regulators (buck, boost)

- Identify the **hot loop** from the datasheet (buck: input cap → high-side switch → low-side switch/diode → input cap GND). Make it as small as possible on one layer, input-cap GND and IC GND adjacent.
- Switch node (SW) copper as small as current allows; away from feedback, analog, sensitive signals; nothing under it on the adjacent layer except GND.
- Feedback trace from the **output capacitor**, away from SW and inductor, divider close to FB pin.
- Inductor close to SW; output caps close to inductor and load. Copy the EVM placement when one exists.
- Thermal pad: solid GND connection with the datasheet's via count.

## LDOs

- Input/output caps at the pins, of the type and ESR the datasheet requires for stability.
- Thermal: P = (Vin - Vout) x I; give the tab/pad the copper and vias it needs.

## STM32 clock (HSE/LSE crystals)

- Crystal and load caps as close to OSC pins as possible, same side, short symmetric traces.
- Solid GND plane under the crystal; GND guard ring tied to the plane with vias; no other signals under or beside it.
- Keep switching nodes, clocks, high-current paths away. Follow ST AN2867 for the family.

## GND stitching and planes

- Stitch outer GND pours to the plane with vias every few mm along edges and around pour islands; delete GND islands that can't be stitched.
- GND via beside every signal via on fast/sensitive nets (return path for the layer change).
- Row of GND vias along the board edge helps contain noise on boards with motor/switching stages.
- **Non-ground vias (power/signal stitching or layer changes) go along the edge of a pour, never the middle**, so ground layers beneath stay uninterrupted.
- **Pair every non-ground via with a ground via directly across the pour/trace** (EMI cancellation, return path).
- **Fill leftover board area with ground pour.** A pour spanning several layers (e.g. GND on both inner layers) is **one** zone with multiple layers ticked.

## Thermal

- Power parts (regulators, MOSFETs, shunts, drivers): outer-layer copper area plus thermal vias into the planes under thermal pads.
- **No via-in-pad (expensive).** Use the standard 0.64/0.30 mm (diameter/drill) via; split the paste into windows so vias sit in the gaps; check gap ≥ via diameter + mask/clearance rules (`COMPUTED`). Follow the datasheet pad/via pattern. If gaps can't fit vias, put them in adjacent copper joined by wide copper and flag it for the user; don't fall back to via-in-pad.
- Spread hot parts apart; a sealed hull has poor airflow.

## Fiducials, test points, mounting

- JLCPCB adds fiducials on its rails. Add 2-3 board-level fiducials (1 mm copper dot, 2 mm mask opening) on non-collinear corners if assembled without rails or with fine-pitch parts; confirm current JLCPCB guidance.
- Test points per the bring-up plan: rails, GND, programming, UART, reset, straps.
- Mounting holes: plated or not per mechanics; copper and component keep-out ring for screw head and washer; connect plated holes to GND/chassis deliberately.

## CAN and RS-485

- Transceiver close to the connector. Order from connector: TVS/ESD **at the connector** → optional common-mode choke → transceiver.
- Termination (120 Ohm or split 2 x 60 Ohm + cap to GND) at the connector end, populated only on end-of-bus boards (DNP footprint or jumper).
- Pair routed together, short, over continuous GND; no stubs to test points.

## USB

- ESD array right at the connector; D+/D- as a 90 Ohm differential pair to the MCU: no stubs, matched lengths, no layer changes if possible (else GND stitching vias beside the pair's vias).
- VBUS protection and bulk capacitance at the connector.
- Shell to GND per the design decision (direct, RC, ferrite), consistent with enclosure grounding.

## Ethernet

- PHY close to magnetics/RJ45; 100 Ohm differential pairs, short, matched within each pair.
- Isolation gap under the magnetics free of copper on all layers (no planes crossing), per magnetics datasheet.
- Termination, bias, Bob Smith network per PHY and magnetics datasheets and PHY reference design.

## High-current battery paths

- Physical order, all near the input connector: battery input → fuse → reverse-polarity protection → TVS → bulk caps → loads.
- Wide pours sized from `design-rules.md` section 2, vias from section 3 at every layer change; check the narrowest neck.
- Current-sense shunts: Kelvin connections (separate sense traces from the inner pad edges to the amplifier, routed as a pair away from the power path).
- Net class with battery-bus clearance from `design-rules.md` section 4.

## Motor / ESC drive

- Power stage (half-bridges, bulk and ceramic caps) as a tight loop like a buck hot loop: HF ceramics directly across each half-bridge.
- Small gate-drive loop: driver → gate resistor → gate, return to driver source/ground, short and together.
- Separate power ground and logic/analog ground paths, joined at one point near bulk caps/current shunt; logic and sensors away from motor phase traces.
- Motor phase outputs straight to the connector; no sensitive signals alongside.

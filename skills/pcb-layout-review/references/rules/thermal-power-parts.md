# Thermal pads and hot parts

**Read when:** regulators, MOSFETs, shunts, motor drivers, LED drivers, any part with an exposed thermal pad or significant dissipation.

## Placement

- Spread hot parts apart; don't stack heat sources in one corner. A sealed enclosure/hull has poor airflow.
- Leave outer-layer copper area around power parts for heat spreading.

## Routing

- Outer-layer copper area plus thermal vias into the planes under thermal pads. Follow the datasheet pad/via pattern and via count.
- Vias under the thermal pad are allowed: standard plugged-and-tented via, paste in a **windowpane pattern covering 50-70 % of the pad**, vias in the gaps between windows (`board-defaults.md` section 5). Check gap >= via diameter + mask/clearance rules `[COMPUTED]`.
- If the gaps can't fit the datasheet's via count, put extra vias in adjacent copper joined to the pad by wide copper and flag it for the user.

## Verify

- Paste coverage (50-70 %) and via-gap arithmetic recorded; any fallback flagged to the user.

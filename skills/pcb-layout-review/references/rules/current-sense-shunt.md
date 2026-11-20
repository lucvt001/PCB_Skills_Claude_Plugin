# Current-sense shunt resistors

**Read when:** a low-value sense resistor (mOhm range) with a current-sense amplifier, ADC, or fuel-gauge input.
**Also read:** `power-routing-and-pours.md`, `analog-and-adc.md`.

## Placement

- Shunt in the power path with the current-sense amplifier close to it, so the sense pair is short.
- Filter components (if any) at the amplifier input.

## Routing

- **Kelvin connections:** separate sense traces from the inner pad edges (or the dedicated sense pads) of the shunt to the amplifier; never tap the power copper away from the pads.
- Route the two sense traces as a tight pair, away from the power path and switching nodes.
- Power copper into and out of the shunt sized for the full current (`power-routing-and-pours.md`).

## Verify

- Sense traces leave from the pads, not from the pour; no power current flows in them.

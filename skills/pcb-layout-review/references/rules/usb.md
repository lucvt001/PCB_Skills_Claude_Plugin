# USB

**Read when:** USB connector, USB PHY/MCU USB pins, D+/D-, VBUS.
**Also read:** `differential-pairs-and-impedance.md`, `connectors.md`.

## Placement

- ESD array right at the connector.
- VBUS protection and bulk capacitance at the connector.

## Routing

- D+/D- as a 90 Ohm differential pair to the MCU: no stubs, matched lengths, no layer changes if possible (else GND stitching vias beside the pair's vias).
- Shell to GND per the design decision (direct, RC, ferrite), consistent with enclosure grounding.

## Verify

- ESD between connector and everything else on D+/D-; no test-point stubs.

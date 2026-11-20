# Fine-pitch ICs and fanout (QFN, QFP, BGA, LGA, dense MCUs)

**Read when:** any IC with pitch <= 0.65 mm, BGA/LGA, or a dense MCU/FPGA/PHY whose escape decides routability.
**Also read:** `thermal-power-parts.md` for exposed pads, `modules-rf-and-antennas.md` for castellated/LGA modules.

## Placement

- Reserve escape room on every side that has pins: decouplers in the supply-pin escape path, not blocking signal escape.
- Compute the escape before freezing placement: gap = pad pitch − pad width. If a via doesn't fit between pads, every escape must clear a pad end, and the ring fills after one via per pad.

## Routing

- Small signal pads: collision-checked offset (dogbone) fanout, not via-in-pad. Exposed/thermal pads: vias allowed per `board-defaults.md` section 5.
- Trace width into the pins per the ladder in `board-defaults.md` section 3: 0.254 mm, necking to 0.127 mm only for the last stretch into a pad where 0.254 mm doesn't fit, widening again once clear of the pin field.
- Fan out power and GND pads first, then signals.

## Verify

- Escape arithmetic recorded; every power/GND pad has a legal escape before signal routing.

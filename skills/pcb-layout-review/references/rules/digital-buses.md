# Digital buses (I2C, SPI, UART, QSPI/SDIO, parallel buses, memory)

**Read when:** routing any multi-signal digital interface between ICs.
**Also read:** `differential-pairs-and-impedance.md` for differential buses, `crystals-and-clocks.md` for clock nets.

> Sections marked *(new)* were added in the restructure and are not yet backed by project lessons; review them.

## Placement

- Place source and destination with their pins facing each other so the bus doesn't cross itself; use the circuit review's topology (point-to-point, daisy chain, star, forbidden branches).
- *(new)* I2C pull-ups once per bus, near the master or the connector that leaves the board.
- *(new)* Series termination resistors for fast edges (SPI SCK, QSPI, SDIO CLK) at the driver end.

## Routing

- Topology and stub rules from the circuit review's layout handoff; edge rate can set SI risk even when the clock is slow.
- Parallel buses: topology and skew budgets come from timing, not visual symmetry; no needless meanders.
- Keep the bus on one reference plane; layer changes get a GND via per `general-rules.md` section 6.

## Verify

- Skew/length recorded only where a budget exists; stubs absent where forbidden.

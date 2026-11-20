# Ethernet

**Read when:** Ethernet PHY, magnetics, RJ45 (incl. MagJack), MDI pairs.
**Also read:** `differential-pairs-and-impedance.md`, `connectors.md`.

## Placement

- PHY close to the magnetics/RJ45.
- Termination, bias, Bob Smith network per the PHY and magnetics datasheets and the PHY reference design.

## Routing

- 100 Ohm differential pairs, short, matched within each pair.
- Isolation gap under the magnetics free of copper on **all** layers (no planes crossing), per the magnetics datasheet.

## Verify

- Isolation gap empty on every copper layer (Gerber/SVG check).

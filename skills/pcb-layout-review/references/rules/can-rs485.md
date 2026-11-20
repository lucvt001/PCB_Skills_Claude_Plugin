# CAN and RS-485

**Read when:** CAN or RS-485/RS-422 transceiver, bus connector, termination.
**Also read:** `differential-pairs-and-impedance.md`, `connectors.md`.

## Placement

- Transceiver close to the connector. Order from connector: **TVS/ESD at the connector → optional common-mode choke → transceiver**.
- Termination (120 Ohm, or split 2 x 60 Ohm + cap to GND) at the connector end, populated only on end-of-bus boards (DNP footprint or jumper).

## Routing

- Pair routed together, short, over continuous GND; no stubs to test points.

## Verify

- Termination DNP/jumper state matches the board's bus position.

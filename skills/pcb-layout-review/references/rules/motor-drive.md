# Motor / ESC drive and gate drivers

**Read when:** half-bridges, H-bridges, 3-phase bridges, gate drivers, motor phase outputs.
**Also read:** `power-routing-and-pours.md`, `thermal-power-parts.md`, `current-sense-shunt.md`, `battery-input-and-protection.md`.

## Placement

- Power stage (half-bridges, bulk and ceramic caps) as a tight loop like a buck hot loop: HF ceramics directly across each half-bridge.
- Gate driver close to its MOSFETs.
- Logic and sensors away from motor phase copper; phase outputs straight to the connector.

## Routing

- Small gate-drive loop: driver → gate resistor → gate, returning to the driver source/ground, short and routed together.
- Separate power ground and logic/analog ground paths, joined at one point near the bulk caps/current shunt.
- No sensitive signals alongside motor phase traces.
- Edge GND via row recommended (`power-routing-and-pours.md`).

## Verify

- Power loop, gate loops, and ground join point identified in the placement stop.

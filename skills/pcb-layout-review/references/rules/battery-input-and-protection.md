# Battery / main power input and protection

**Read when:** battery or DC input connector, fuse, reverse-polarity protection, input TVS, ideal diode, high-current input bus.
**Also read:** `power-routing-and-pours.md`, `current-sense-shunt.md` if a shunt is in the path, `high-voltage-clearance.md` for >= 31 V, `connectors.md`.

## Placement

- Physical order, all near the input connector: **battery input → fuse → reverse-polarity protection → TVS → bulk caps → loads**.
- Keep the input section compact so the high-current path doesn't wander through the board.

## Routing

- Wide pours sized from `power-routing-and-pours.md`, vias at every layer change; check the narrowest neck.
- Input >= 31 V: flag per `high-voltage-clearance.md`.
- Prefer one high-current zone on both F.Cu and B.Cu (`board-defaults.md` section 6).
- Check connector and fuse current ratings and the pad size they need.

## Verify

- Order of protection parts matches the physical current path.
- Neck, drop, and via counts recorded for worst-case current.

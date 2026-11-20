# Modules, RF, and antennas

**Read when:** Wi-Fi/BLE/LoRa/GNSS/cellular modules, castellated or LGA modules, shield cans, chip/PCB antennas, u.FL/SMA feeds.
**Also read:** `differential-pairs-and-impedance.md` (50 Ohm feeds), `connectors.md` (RF connectors).

## Placement

- Place the module/antenna where the manufacturer requires (usually at a board edge or corner), with its component and copper keepouts on **every** relevant layer.
- Nothing under a module body: no parts, including small passives, inside its courtyard.
- A vendor module with integrated antenna is a placement/keepout problem; don't invent an RF feed trace.

## Routing

- Antenna keepout as a rule area on every copper layer. Lesson: a keep-out drawn only on a user layer let a reference board fill 93.8 % ground pour plus stitching vias into the antenna area on all four layers.
- Under a castellated/LGA module, keep non-ground top copper and via drills out of the exposed underside lands plus margin, using the module's real pad map from its datasheet (not the footprint author's bounding box).
- RF feed: 50 Ohm, follow the module's reference layout exactly.

## Verify

- Antenna region empty on each copper layer in Gerbers/SVG.
- No copper or drills under exposed module lands.

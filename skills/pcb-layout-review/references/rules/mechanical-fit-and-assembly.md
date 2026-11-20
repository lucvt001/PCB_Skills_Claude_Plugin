# Mechanical fit, enclosure, mounting, and hand assembly

**Read when:** mounting holes, enclosure/hull outline, through-hole parts, hand-fitted parts (cables, batteries, later-fitted modules), conformal coating.
**Also read:** `connectors.md` for edge openings.

## Placement

**Enclosure and outline** (from enclosure CAD: DXF on a user layer, or dimensions):

- board outline vs internal 2D profile, with clearance;
- mounting holes, standoff pads, rails, keep-outs;
- connector/penetrator positions and cable routing space;
- regions left uncoated if conformally coated (connectors, test pads, switches);
- JLCPCB's added rails/fiducials and corner rounding (unless disabled in the order).

**Mounting holes:** M3 by default (`board-defaults.md` section 8); plated or not per mechanics; copper and component keep-out ring for screw head and washer; connect plated holes to GND/chassis deliberately.

**Through-hole parts:**

- Their joints protrude on the opposite face: keep them out of areas resting on a battery, bracket, or hull rail; list those regions in the layout review.
- JLCPCB PCBA assembles SMT on one side by default; list which through-hole parts are hand-soldered vs a separate service.

**Hand-fit access:**

- List every hand-fitted part.
- Per pad, measure the 2D distance to the nearest neighbouring courtyard; flag < ~0.8 mm as needing a fitting-order note.
- Put fitting order and every configure-before-fitting item in the build checklist.

## Routing

- Respect the mounting-hole keep-out ring on all copper layers except an intentional GND/chassis connection.

## Verify

```
[ ] board outline, mounting, connector positions, coating keep-outs vs enclosure
[ ] through-hole joints clear of resting faces
[ ] hand-fit parts listed with access distances and fitting order
```

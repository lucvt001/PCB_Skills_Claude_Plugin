# 2D placement mechanics

Adapted from `daishuge/pcb-skill` (MIT, see `../LICENSE-pcb-skill`). A board passing DRC can still be impossible to connect, fit, or hand-finish. All checks are in **plan view** (courtyards, Fab outlines, Edge.Cuts, copper layers, Gerbers); no 3D or height analysis. Use with [connector-stack-and-fanout.md](connector-stack-and-fanout.md) for connector maturity and dense power/GND escape.

## 1. Courtyards and Fab outlines are the 2D body

- Every footprint has a courtyard and F.Fab/B.Fab outline matching the exact MPN drawing in plan view. Missing or copied-from-another-part outlines blind every clearance check on that side.
- Run `courtyards_overlap` and `missing_courtyard` as errors; read every violation; no bulk waivers.

## 2. Connectors: mouth, mating area, mating half

Establish from the manufacturer's drawing (not silk):

1. **Mouth direction.** It can be rigidly coupled to the pin-1 end; rotating a connector without renumbering pads can put a supply on a ground pin. Rotation and pad renumber are one change, never two.
2. **Plan-view area for plug, latch, cable bend.** Side-entry plugs sit outside the footprint: draw it as courtyard extension or user-layer keep-out and keep parts out.
3. **Mating half:** exists, in BOM or hand-fit list, user can join the two.
4. **Board-edge openings:** list every connector, switch, LED, button at an edge with its edge offset; no two collide on a face; each lines up with the enclosure opening.

## 3. Nothing under module bodies

- No part inside any module, shield can, or connector body outline; check courtyard overlap for **every** part, including small passives, against every module courtyard.
- Under a castellated/LGA module, keep non-ground top copper and via drills out of the exposed underside lands plus margin, using the module's real pad map from its datasheet (not footprint-author bounding boxes).

## 4. Keep-outs must be on copper layers

- A keep-out on a user/documentation layer doesn't constrain zone fill (the reference board's antenna keep-out held 93.8 % ground pour on all four layers plus stitching vias).
- Use **rule areas (keep-out zones) on every relevant copper layer**; confirm from Gerbers or a copper-layer SVG that the region is empty on each.

## 5. Through-hole parts and the opposite face

- Through-hole joints protrude on the opposite face: keep them out of areas resting on a battery, bracket, or hull rail; list those regions in the layout review.
- JLCPCB PCBA places SMT on one side by default; through-hole is hand-soldered or a separate service; list which.
- Flag every via barrel inside an SMT pad (needs filled/capped vias, usually a premium process).

## 6. Hand-fit access

- List every hand-fitted part (through-hole connectors, cables, batteries, later-fitted modules).
- Per pad, measure 2D distance to the nearest neighbouring courtyard; flag < ~0.8 mm as needing a fitting-order note.
- Put fitting order and every configure-before-fitting item in the build checklist.

## 7. Enclosure and hull outline

From enclosure CAD (DXF on a user layer, or dimensions):

- board outline vs internal 2D profile, with clearance;
- mounting holes, standoff pads, rails, keep-outs;
- connector/penetrator positions and cable routing space;
- regions uncoated if conformally coated (connectors, test pads, switches);
- JLCPCB's added rails/fiducials and corner rounding (unless disabled in the order).

Height/3D interference is out of scope for routine reviews; for a part known to be tall near a lid or hull wall, ask the user to check their mechanical CAD.

## Checklist

```
[ ] every footprint has a courtyard and Fab outline matching its MPN drawing
[ ] courtyard checks run as errors; every violation read
[ ] every connector: mouth from the drawing, mating area kept clear in plan view
[ ] every connector: mating half sourced and joinable
[ ] pin-1 marker, footprint numbering, and fitted part agree
[ ] no part inside any module/shield/connector courtyard
[ ] no non-ground top copper or via drills under a module's exposed lands
[ ] every keep-out on the copper layers it must constrain, verified in Gerbers
[ ] through-hole joints clear of resting faces; via-in-pad flagged
[ ] hand-fit parts listed with access distances and fitting order
[ ] board outline, mounting, connector positions, coating keep-outs vs enclosure
```

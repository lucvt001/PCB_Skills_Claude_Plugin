# Connectors and board-edge parts

**Read when:** any connector, and any switch, LED, button, or jack at a board edge.
**Also read:** `dense-connectors-and-board-stacks.md` for card-edge, board-to-board, sockets, daughtercards, or dense fanout; the interface file (`usb.md`, `ethernet.md`, `can-rs485.md`, ...).

## Placement

Establish from the manufacturer's drawing (not the silkscreen):

1. **Mouth direction.** It can be rigidly coupled to the pin-1 end (rotate and renumber as one change, `general-rules.md`).
2. **Plan-view area for the plug, latch, and cable bend.** Side-entry plugs sit outside the footprint: draw it as a courtyard extension or copper-layer keep-out and keep parts out.
3. **Mating half:** it exists, is in the BOM or hand-fit list, and the user can join the two.
4. **Board-edge openings:** list every edge connector, switch, LED, and button with its edge offset; no two collide on a face; each lines up with its enclosure opening.

- Connectors and user controls accessible in plan view.
- Connector pin order defines the functional corridor into the board (`general-rules.md` section 4).
- I/O protection (TVS/ESD) sits at the connector, before anything else on the line; the interface file gives the full order.

**Connector maturity.** Record each connector at the highest level the evidence supports:

1. **Electrical mapping:** contact count, pitch, pin numbering, contact side, assigned nets known.
2. **Orderable part:** exact MPN + manufacturer drawing confirm package, pin 1, origin, body, contacts, tabs, locating features.
3. **Footprint geometry:** pads, holes, body, courtyard, mating mouth, board edge, assembly side, 3D model agree with the drawing.
4. **Mating system:** mating-card thickness and edge geometry, insertion depth, retention, extraction clearance, enclosure stack defined.
5. **Physical proof:** actual sample or controlled mechanical article measured and test-fitted.

- Record assembly dimensions as measured, drawing-derived, inferred, or TBD. A plausible 3D model is visual evidence, not mechanical proof.
- Exact part or sample missing: keep a conservative body/courtyard; mark the dependent mechanical gate `USER_REVIEW` or `BLOCKED`. **Never shrink an unmeasured envelope** to clear DRC or fit neighbours.

## Routing

- Body/mating-mouth overhang past the board edge may be intentional; copper pads, plated support features, solder joints, and required substrate may not hang in free space.

## Verify

```
[ ] every connector: mouth from the drawing, mating area kept clear in plan view
[ ] every connector: mating half sourced and joinable
[ ] pin-1 marker, footprint numbering, and fitted part agree
[ ] edge parts: offsets listed, no collisions, aligned with enclosure openings
[ ] maturity level recorded; unverified mechanics stay USER_REVIEW/BLOCKED
```

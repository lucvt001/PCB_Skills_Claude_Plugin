# Connector stacks and dense fanout

Gates for card-edge sockets, board-to-board connectors, modules, daughtercards, adapter PCBs, and any dense connector whose mechanics or power escape can determine the layout.

## Connector maturity gate

Record each connector at the highest level the evidence supports:

1. **Electrical mapping:** contact count, pitch, pin numbering, contact side, assigned nets known.
2. **Orderable part:** exact MPN + manufacturer drawing confirm package, pin 1, origin, body, contacts, tabs, locating features.
3. **Footprint geometry:** pads, holes, body, courtyard, mating mouth, board edge, assembly side, 3D model agree with the drawing.
4. **Mating system:** mating-card thickness and edge geometry, insertion depth, retention, extraction clearance, enclosure stack defined.
5. **Physical proof:** actual sample or controlled mechanical article measured and test-fitted.

- Exact part or sample missing: keep a conservative body/courtyard; mark the dependent mechanical gate `USER_REVIEW` or `BLOCKED`. Never shrink an unmeasured envelope to clear DRC or fit neighbours.
- Body/mating-mouth overhang may be intentional; copper pads, plated support features, solder joints, required substrate may not hang in free space. Transform every physical pad and support feature against the real board polygon (an axis-aligned rectangle check fails for notches, cutouts, irregular edges).

## Multi-board dimensional proof

- Compare boards with 2D outline plots (Edge.Cuts + Fab) at one physical scale; never independently fitted screenshots.
- One dimensioned drawing with main board, every adapter/daughtercard, and the mating connector footprint position.
- Overall dimensions and insertion depth tagged `MEASURED`, `DRAWING`, `INFERRED`, or `TBD`. Stack heights are checked by the user in mechanical CAD.

## Dense power and GND escape

Classify each power/GND pad before signal routing. Each needs at least one of:

- a legal standard-process dogbone or direct via escape;
- a same-layer copper path to a connected, stitchable region;
- a documented premium process explicitly accepted for cost and reliability.

- Legal escape collides with neighbouring pads, drills, keepouts, or board support: move the local part or revise the connector corridor before routing. A later plane fill or blanket via grid won't repair an impossible fanout.
- Same-net zone fragments and region-level opens are real defects. Connect each fragment to the canonical rail with individually clearance-proven stitches or a verified topology change; blanket island deletion, blind stitching, brute-force repair are not evidence.

## Comparative experiments

- Freeze the input state before changing outline, stackup, via process, rules, or routing method.
- Compare each experiment with the current best safe candidate (not only the original unrouted board) using the full vector: opens, real DRC, power connectivity, return paths, connector mechanics, manufacturing thresholds, cost, visual gates.
- Board growth helps only if it creates a measurable local corridor or mechanical clearance; area elsewhere doesn't fix a blocking geometry.

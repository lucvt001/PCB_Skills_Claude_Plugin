# Dense connectors, card-edge, board-to-board, multi-board stacks

**Read when:** card-edge sockets or fingers, board-to-board connectors, modules on sockets, daughtercards, adapter PCBs, any dense connector whose mechanics or power escape can decide the layout.
**Also read:** `connectors.md` (maturity levels, mouth, mating half), `variant-porting.md` if derived from a proven board.

## Placement

- Verify connector pitch, mating datum, fingers/tongue, insertion envelope, shell features, and allowed growth direction independently of the footprint.
- Preserve mating-edge datum, fingers, tongue, insertion keepouts; add board area only in a direction verified against host and enclosure.
- Transform every physical pad and support feature against the real board polygon (an axis-aligned rectangle check fails for notches, cutouts, irregular edges).

## Routing: dense power and GND escape

Classify each power/GND pad **before** signal routing. Each needs at least one of:

- a legal standard-process dogbone or direct via escape;
- a same-layer copper path to a connected, stitchable region;
- a documented premium process explicitly accepted for cost and reliability.

- If the legal escape collides with neighbouring pads, drills, keepouts, or board support: move the local part or revise the connector corridor before routing. A later plane fill or blanket via grid won't repair an impossible fanout; local placement and pad-specific dogbones beat hoping.
- Same-net zone fragments and region-level opens are real defects: connect each to the canonical rail with individually clearance-proven stitches or a verified topology change; blanket island deletion, blind stitching, brute-force repair are not evidence.

## Verify: multi-board dimensional proof

- Compare boards with 2D outline plots (Edge.Cuts + Fab) at one physical scale; never independently fitted screenshots.
- One dimensioned 2D drawing with the main board, every adapter/daughtercard, and the mating connector footprint position.
- Overall dimensions and insertion depth tagged `MEASURED`, `DRAWING`, `INFERRED`, or `TBD`. Stack heights are checked by the user in mechanical CAD.
- Promote connector mechanics in stages: electrical mapping → exact orderable part → verified footprint → defined mating stack → measured physical fit. Clean DRC can't replace a missing sample or drawing.

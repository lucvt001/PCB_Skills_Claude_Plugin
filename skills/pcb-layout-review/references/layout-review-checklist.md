# PCB layout review checklist

## Placement freeze

- Derivative board: donor hashes and an explicit electrical/mechanical delta exist before placement reuse.
- Connector pitch, mating datum, fingers/tongue, insertion envelope, shell features, allowed growth direction independently verified.
- Exact connector MPN and drawing agree with body, contacts, locating features, pin 1, origin, footprint, mating card, insertion depth, retention. Sample unavailable: its conservative envelope stays in review.
- Connector pin order and functional corridors match architecture; protection, translators, buffers, memory, processing, outputs don't backtrack needlessly.
- Every IC supply pin has local decoupling in its current path; bulk serves entries and load steps.
- Regulators, crystals, feedback, switching loops, ESD, terminations, pulls, reset/boot, current sense placed at their function.
- Antennas/RF modules follow the manufacturer's component and copper keepouts on every relevant layer.
- Large/critical parts: verified MPN, package, footprint, pin 1, courtyard/Fab outline matching the drawing. Connectors and controls accessible in plan view.
- Logical/constraint and visual/mechanical passes recorded independently.
- Every dense connector/module power and GND pad has a legal dogbone, direct via, same-layer path to a stitched region, or approved process exception before signal routing.

## Routability before routing

Adapted from `daishuge/pcb-skill` (MIT, see `../LICENSE-pcb-skill`).

- Estimate with the rule set stored in the project (`.kicad_pro` net classes/constraints, `.kicad_dru`) and confirm the board has the copper layers you plan to route on.
- Sweep free spans between parts; count those at least **via pad + 2 x clearance** wide (not track + clearance). Report the via-capable fraction.
- Fine-pitch parts: compute the escape. Gap = pad pitch − pad width; if a via doesn't fit between pads every escape must clear a pad end, and the ring fills after one via per pad.
- List every part with **no** via-lane side; fix by moving parts, not by hoping the router copes.
- Route shared spines and scarce corridors first; reserve power fanout before dense signal routing.
- A placer/router failure is a fact about the search: before calling a placement impossible, state which parts were held fixed and why.

## Routing and return paths

- Layer count and stackup justified by density, reference needs, interface geometry, power, mechanics, live fab capability.
- Critical signals never cross a plane split/void without a nearby return transition; control via counts and layer changes where meaningful.
- Differential pairs: final stackup-derived geometry, continuous reference, defined tolerance, no stubs, measured mismatch.
- Parallel buses: topology and skew budgets from timing, not visual symmetry; no needless meanders.
- Power widths, pours, neck-downs, vias, voltage drop, thermal rise, source capability support the measured or conservatively allocated current.
- No copper, via, component, or mask feature violates outlines, cutouts, fingers, contacts, antennas, mounting, enclosure keepouts.

## Connectivity and DRC

- Inspect every raw unconnected item; treat signal and power representatives as real until proven otherwise.
- Zero pad opens is insufficient while track/track, track/via, or zone/plane components remain separated.
- Same-net zone fragments: each proven to reach the canonical rail (blanket stitches or island deletion are not proof). Treat as real opens until proven.
- Classify intentional fab geometry narrowly; no broad waivers hiding unrelated errors.
- DRC rules match the chosen manufacturing capability and quote, not values chosen to make the report green.

## Manufacturing and visual evidence

- Via/drill histogram; flag every feature below the current standard-cost threshold.
- Inspect assembly side, paste, silkscreen, fiducials, tooling/depanel, edge treatments, finish, thickness, controlled options.
- Plot top and bottom 2D assembly views (Fab + SilkS + CrtYd + Edge.Cuts) and critical closeups after every footprint, rotation, or position change.
- Missing/offset body outlines, wrong pin 1/polarity, unsupported connectors, mechanical collisions block release even with clean copper DRC.
- Distinguish intentional body/mating-mouth overhang from copper pads, plated features, solder joints, or missing substrate (check transformed physical pads against the real outline).
- Donor/variant size comparisons: one orthographic scale with explicit dimensions; independently fitted screenshots are rejected.
- Multi-board assemblies: one dimensioned 2D drawing at one scale; every dimension measured, drawing-derived, inferred, or TBD.
- Stackup/outline/via-process/routing experiments: frozen inputs, compared with the current best safe candidate; board growth counts only if it creates a measurable corridor or clearance.
- Silk-over-silk, silk-over-copper, edge-clearance findings: normalized and visually classified; critical markings stay readable; unresolved dense labels `USER_REVIEW`, never silently deleted.

## Proven lessons

Placement and routing

- Freeze placement from architecture and physical connector pin order before optimizing wire length or launching an autorouter.
- Route shared spines and scarce corridors early; late common-bus routing strands endpoints.
- Reserve power fanout capacity before dense signals; never treat different power nets as one category in collision checks.
- Classify every dense connector/module power/GND escape before signal routing; local placement and pad-specific dogbones beat hoping a later fill or via grid fixes an impossible corridor.
- Avoid via-in-pad on fine-pitch parts unless footprint and process support it; use collision-checked offset fanout.
- Check a new through-via on every traversed layer; verify it keeps its net after save and any selective zone refill.
- Refill only affected zones after local edits; global refill can change connectivity under rule/setting drift.
- Reject a zero-open candidate that adds clearance, short, power-island, return-path, or manufacturing defects: connectivity and physical legality are independent metrics.
- Import coupled corridor repairs atomically; never cherry-pick the headline net from a donor that displaced neighbouring lanes.
- Autorouter omitted a target route: inspect target pins, fixed/movable scopes, result occurrences before changing normalization or retry flags.
- Compare layer/outline/via/routing experiments with the best safe saved candidate from the same frozen input; zero opens alone isn't improvement.

Manufacturing and release

- Live quote surcharges are feedback: resize only verified legal features, keep density-critical exceptions, regenerate all checks and release artifacts, compare the new quote.
- Supplier placement preview is not PCB placement validation: a separate post-release interpretation needing machine and visual review.
- Close layout review with normalized silkscreen checks and both-side visual evidence; keep polarity/pin-1 meaning; classify intentional connector overhang apart from fab defects.

Connectors, derivatives, mechanics

- A connector, enclosure, platform, or regional derivative is an electrical-and-mechanical constraint remap, not a cropped parent layout.
- Preserve mating-edge datum, fingers, tongue, insertion keepouts; add board area only in a direction verified against host and enclosure.
- Reuse functional topology and pin-bank orientation, not absolute donor coordinates; repeat every placement and reference-path gate.
- Promote connector mechanics in stages: electrical mapping → exact orderable part → verified footprint → defined mating stack → measured physical fit. Clean DRC can't replace a missing sample or drawing.
- Compare derivative boards with 2D outline plots at one physical scale; one dimensioned 2D drawing for multi-board products, every estimated dimension labelled.

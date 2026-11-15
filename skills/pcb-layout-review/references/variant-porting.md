# Derivative PCB variant porting

For adapting a proven board to another connector, enclosure, platform, regional standard, or related product. Goal: controlled reuse of verified circuit/layout knowledge without assuming the parent geometry satisfies the target.

## 1. Write the delta before layout

Freeze the donor PCB/project and record hashes. Target manifest covers:

- connector pin order, pitch, contact geometry, mating datum, insertion envelope;
- exact orderable connector MPN, body, locating features, footprint origin, mating-card thickness, insertion depth, retention, sample status;
- removed/added/reassigned circuit functions and safe-state behavior;
- power, ground, audio, protection, programming, UI changes;
- board outline, thickness, slots, bosses, shell limits, antenna regions, keepouts;
- assembly side, panel/depanel assumptions, finish, edge treatment, current fab thresholds.

Never start from a cropped or scaled board; matching pin count doesn't prove matching pin semantics, mechanics, return paths, or assembly support.

## 2. Preserve the mating edge

- Contacts, tongue, bevel, insertion keepouts, host datum are hard geometry. Extra area only in a direction proven by host and enclosure.
- Every nonstandard outline needs a 1:1 fit gate; a clean board plot isn't enclosure proof.
- Socket/module/board-to-board connector: distinguish intentional body/mouth overhang from pads or support features lacking substrate. Keep a conservative courtyard while body or sample is unverified.

## 3. Reuse intent, not coordinates

- Carry over functional blocks, pin-bank direction, decoupler/support relationships, routing topology, verified local constraints.
- Re-run humanized signal-flow, source/destination pin-side, power/reference, RF, mechanical, sourcing reviews on the target; optimize family-level routing metrics only after.
- Geometry-lock each candidate: compare outlines, slots, fixed connectors, keepouts, footprint transforms, pad nets, zones, paired project file. Record every allowed transform or route change.

## 4. Route transactionally

- Prefanout power before dense buses; route scarce shared spines early.
- Trapped route needs neighbouring lanes to move: keep the smallest coherent donor, integrate every changed net atomically, prove all displaced nets, compare non-whitelisted route fingerprints before promotion.
- Autorouter produced no target route: inspect the job, not the headline warning:
  - confirm target net and pins in the exported input;
  - count fixed and movable wiring scopes;
  - inspect the result for target-net route occurrences;
  - verify the minimum physical blocker was allowed to move.
- Retry only after the movable window or board conditions materially change. Board growth counts only if the new geometry creates a measurable corridor.

## 5. Prove visuals and release together

- Plot donor and target 2D outlines (Edge.Cuts + Fab) at one physical scale with explicit dimensions.
- Inspect both sides, each signal layer, connector support, antenna, contacts, tongue, slots, enclosure limits.
- Run normalized silk-over-silk, silk-over-copper, edge-clearance checks; preserve pin-1, polarity, functional labels; classify intentional connector-body overhang separately; unresolved labels stay `USER_REVIEW`.
- Multi-board products: every adapter, daughtercard, mating connector in one dimensioned 2D drawing at one scale; dimensions marked measured, drawing-derived, inferred, or TBD.
- Release needs one saved board/project state with zero unexplained raw disconnects, zero real DRC, zero power disconnects, passing layout gates, verified reference paths, visual/mechanical/silkscreen approval.

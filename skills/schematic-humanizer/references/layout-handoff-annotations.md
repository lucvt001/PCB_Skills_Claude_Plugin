# Layout handoff annotations

Add layout annotations when the user asks or the source clearly exposes placement-sensitive interfaces. Don't guess hidden electrical requirements; ask only when the missing choice would materially change the design, else mark it for measurement or engineering review.

## Evidence classes

Project tags (definitions: workflow skill):

- `[VERIFIED]`: manufacturer datasheet, interface standard, approved project requirement, verified measurement; source in the companion document.
- `[COMPUTED]`: derived from verified values; arithmetic in the companion document.
- `[TARGET]`: conservative routing allocation for this revision (loose group skew, firmware-rate ceiling, current capacity, layer preference); state it isn't certified timing or measured current.
- `[ESTIMATE]`: unmeasured working value to confirm before its gate.
- `[NOT ESTABLISHED]`: source capability, thermal rise, real current, unknown clock, enclosure RF performance, anything the schematic can't prove.

## What to capture

Per meaningful interface or rail, only applicable items:

1. Clock, data rate, or access cadence, plus the warning that edge rate can set SI risk even when the clock is slow.
2. Topology and stub rule: source → buffer/termination → receiver, point-to-point, daisy chain, star, or forbidden branches.
3. Reference plane, layer preference, controlled impedance, spacing, return-transition guidance.
4. Group skew or pair mismatch target; no meanders when the timing budget doesn't need them.
5. Provisional current allocation, shared-trunk capacity, trace/pour and via intent, voltage-drop/thermal signoff, measurement state.
6. Placement: decoupling escape path, regulator loop, crystal, antenna keepout, connector ESD, exposed-interface protection, mechanical keepouts.
7. Authoritative manufacturer/standards URL in a companion layout guide.

## Presentation

- Short local callouts near the relevant region, outside wires, buses, symbols, labels, and the dominant visual flow.
- Full calculations, current-budget tables, URLs, assumptions, signoff checklists go in a companion Markdown/PDF; link with a short on-sheet note.
- Don't label a whole design with one clock when domains differ; separate CPU, memory, loader, RF, USB, etc.
- No generic impedance width/gap before the final fab stackup is known: state impedance and reference plane, require stackup-derived geometry.
- A vendor module with integrated antenna is a placement/keepout problem; don't invent an RF feed trace.

## Final gate

Annotations can add overlaps. After adding them follow the full [visual-audit-checklist.md](visual-audit-checklist.md) (every page, dense crops around annotated regions), then repeat connectivity comparison and ERC/lint. A clean netlist doesn't excuse an obscured schematic.

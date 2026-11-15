---
name: plan-electronic-product
description: Turn a vague product idea into an engineering brief with numbered constraints and architecture, before schematic design.
---

# Electronic Product Planner

Produce `.pcba-workflow/product-brief.yaml`, `.pcba-workflow/architecture.md`, and start `.pcba-workflow/DECISIONS.md`. Don't invent requirements to fill a template.

## Workflow

1. Read repo instructions and all supplied descriptions, diagrams, circuits, firmware behavior, mechanics, commercial constraints.
2. Use [intake-checklist.md](references/intake-checklist.md) to separate known facts, targets, estimates, unresolved choices.
3. Copy [assets/product-brief.yaml](assets/product-brief.yaml) to the state directory; fill only supported fields.
4. **Question test:** ask only when the two answers give a different board (typically quantity, hard budget, assembly mode, environment, required interfaces, power source, enclosure limits). Research measurables yourself (prices, library classes, datasheet facts); decide your own-job details.
5. Record **hard constraints `H1..Hn`** (never traded) and **ranked soft constraints `S1 > S2 > ...`** with the tie-break written down.
6. Record scope boundary: what's out, and what "done" means per deliverable.
7. `architecture.md`: system boundaries, actors, external connectors, functional blocks, data/energy flow, operating modes, startup/shutdown/fault states, shared-resource ownership.
8. Per interface: voltage domains, direction, protocol/bus, nominal rate, edge-rate uncertainty, topology, cable/connector environment, protection.
9. Provisional power budget per rail and mode with **typical and worst-case columns**. Tag every figure VERIFIED/COMPUTED/TARGET/ESTIMATE/NOT ESTABLISHED; typical datasheet current is not a guaranteed system maximum.
10. List candidate architectures priced **including assembly fees**.
11. Record mechanical envelope, user-accessible parts, antenna/enclosure needs, programming/test access, quantity, target cost, lifecycle, compliance.
12. Ask only unresolved choices passing the question test; record the rest as unknowns with owner and closing evidence.

## Decisions and standing authority

- Decision log rules: see workflow skill.
- If the user grants standing authority ("stop asking, push it through"), record it in the brief. Apply only `H1..Hn` and `S1 > S2 ...`; for close options pick the cheaper to reverse and say so; escalate any **constraint** change. It never covers design-critical substitutions, placement approval, final price, credentials, order submission, or payment.

## Gate

- `PASS`: downstream circuit and sourcing can work without guessing core behavior, power source, interfaces, physical limits, assembly mode, or production intent, and every board-changing question has an answer on record.
- `USER_REVIEW`: decision awaiting the owner. `BLOCKED`: missing evidence prevents safe progress.
- Don't pick exact components or approve a circuit here: parts go to `/qualify-pcba-sourcing`, implementation to `/design-and-review-circuit`.

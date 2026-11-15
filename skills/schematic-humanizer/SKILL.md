---
name: schematic-humanizer
description: Make a schematic readable (functional sheets, visible wiring, dashed annotated boxes) without changing connectivity.
---

# Schematic Humanizer

> `${CLAUDE_SKILL_DIR}`: scripts in `scripts/`, sibling skills in the parent folder. In references, `<skill-dir>` = this directory, `<skills>` = its parent. Run scripts from `pcb/` (or use absolute paths).

Make a label-heavy schematic traceable by a human. Preserve the circuit unless the user separately authorizes an electrical change. Readability is not electrical approval.

## Baseline

Read [canonical-connectivity.md](references/canonical-connectivity.md) and define:

1. Native source of truth, generator, libraries, rules, protected PCB/layout files.
2. Baseline connectivity exporter/parser and its limits.
3. Normalization to `schematic-connectivity-v1`: component identity, named net, every `(reference, pin)` membership.
4. Edit path (generator, native API, text format, controlled GUI), renderer, ERC/lint path.
5. Repeatable post-edit export and exact comparison.

- Never call an unverified conversion equivalent. PDF/image only: preserve it, create a companion native drawing, label equivalence unverified.
- Read the mandatory [visual-audit-checklist.md](references/visual-audit-checklist.md) before editing; record results with [visual-audit-record.md](references/visual-audit-record.md).
- For layout guidance or placement-sensitive buses, clocks, power, controlled interfaces, RF, or manufacturer rules, also read [layout-handoff-annotations.md](references/layout-handoff-annotations.md).

## Workflow

1. **Capture baseline.** Export canonical connectivity and ERC/lint; hash (or clean-diff) protected layout files. Generator-owned schematic: edit the generator; for a generated variant, trace the config/override into the generator (a defined but unused table is not evidence). Render the whole schematic as the "before" record.
2. **Plan functional sheets.**
   - Group by flow: connector/input → protection/translation → processing/control → memory/output; separate power/reset and repetitive decoupling when useful. Left-to-right flow, power top, ground bottom.
   - Large designs: hierarchical sheets with hierarchical labels and sheet pins (no global labels; power symbols excepted); multi-sheet only: page x 100 designators (R101, R201).
   - Global-to-hierarchical conversion renames nets (`/Sheet/NET`) and re-annotation renames references: deliberate identity changes. Get the user's go-ahead, record a before→after name map, and check the comparison against that map.
   - **Per sheet:** main IC in the middle, support circuitry around it. Each sub-circuit (feedback divider, bootstrap, crystal, input filter, enable/UVLO) gets its own titled dashed box with the datasheet/EVM equation or rationale beside it (`[VERIFIED]`, section/page). Box text minimal: no part numbers; text 40 mil, title 70 mil. Keep its connections to the IC short and visible for pin-by-pin datasheet cross-check.
3. **Show local relationships.** Native wires for nearby connectors, USB, oscillators, MCU support, memory controls, translators, glue, reset/boot, pulls, LEDs, power chains. Rotate connectors toward the circuit they serve. Real buses and entries for repeated address/data groups. Labels mainly for cross-sheet or genuinely long connections.
4. **Drawing hygiene.** No wire/bus under a symbol, reference, value, title, note, or unrelated label. Avoid wire-through-pin ambiguity, unintended junctions, four-way crossings, stacked labels, long loops, crowded bus entries. Orthogonal grid-aligned routes, visible junctions, consistent entry pitch, whitespace.
5. **Render before annotation.** Export every sheet to PDF and readable PNG; inspect whole pages, edges, dense crops (large ICs, modules, connectors, memories, buses, reset, power). Fix overlaps, apparent floating functions, reversed flow, clipped items, avoidable label chains.
6. **Add layout guidance.** Tag each statement `[VERIFIED]`/`[COMPUTED]`/`[TARGET]`/`[ESTIMATE]`/`[NOT ESTABLISHED]`. Capture rate + edge-rate caveat, topology/stubs, reference plane, skew, current, trace/via intent, placement/keepout, source. Calculations and full URLs go in a companion document.
7. **Render again.** Reinspect every page and changed crop; reject any annotation hiding a wire, bus, pin, reference, value, heading, or dominant signal path.
8. **Prove preservation.** Re-export with the same adapter; run `python ${CLAUDE_SKILL_DIR}/scripts/compare_connectivity.py before after` (KiCad XML accepted). Require exact identities, net names, ref/pin memberships, no new ERC/lint findings, no protected layout changes. After any generator config/override change, prove the active variant in a deterministic manifest or sentinel output and repeat the comparison; ERC alone is insufficient.

## Completion report

Authoritative files, baseline/final counts, comparison result, ERC/lint before/after, protected-file proof, every page/crop inspected, limitations, final snapshot. Write `.pcba-workflow/schematic-visual-audit.json`. Route circuit findings to `/design-and-review-circuit`, not into visual approval. Copy-ready requests: [prompt-template.md](references/prompt-template.md).

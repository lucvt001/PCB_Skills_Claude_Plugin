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
- Read the mandatory [visual-audit-checklist.md](references/visual-audit-checklist.md) and [print-readability.md](references/print-readability.md) before editing; record results with [visual-audit-record.md](references/visual-audit-record.md).
- For layout guidance or placement-sensitive buses, clocks, power, controlled interfaces, RF, or manufacturer rules, also read [layout-handoff-annotations.md](references/layout-handoff-annotations.md).

## Workflow

1. **Capture baseline.** Export canonical connectivity and ERC/lint; hash (or clean-diff) protected layout files. Generator-owned schematic: edit the generator; for a generated variant, trace the config/override into the generator (a defined but unused table is not evidence). Render the whole schematic as the "before" record.
2. **Plan functional sheets.**
   - Group by flow: connector/input → protection/translation → processing/control → memory/output; separate power/reset and repetitive decoupling when useful. Left-to-right flow, power top, ground bottom.
   - Large designs: hierarchical sheets with hierarchical labels and sheet pins (no global labels; power symbols excepted); root is sheet 0, subsheets continue from there, designators are sheet number x 100 + increment (R1 on root, R101, R201).
   - Global-to-hierarchical conversion renames nets (`/Sheet/NET`) and re-annotation renames references: deliberate identity changes. Get the user's go-ahead, record a before→after name map, and check the comparison against that map.
   - **Per sheet:** main IC in the middle, support circuitry around it. Each sub-circuit (feedback divider, bootstrap, crystal, input filter, enable/UVLO) gets its own titled dashed box with a 1-3 line note for the reader (function, key values, thresholds). Evidence tags, derivations and decision IDs go in the companion document. No part numbers in box text; text at least 1.27 mm, titles 2.0 mm. Keep its connections to the IC short and visible for pin-by-pin datasheet cross-check.
   - **Pages:** one paper size (A4 default), a filled title block per sheet, page numbers in order with no gaps, a bottom box for test points and PWR_FLAGs, mounting holes and net ties on the root. Values, symbols and grounds follow [print-readability.md](references/print-readability.md).
3. **Show local relationships.** Native wires for nearby connectors, USB, oscillators, MCU support, memory controls, translators, glue, reset/boot, pulls, LEDs, power chains. Rotate connectors toward the circuit they serve. Real buses and entries for repeated address/data groups. Labels mainly for cross-sheet or genuinely long connections.
4. **Drawing hygiene.** No wire/bus under a symbol, reference, value, title, note, or unrelated label. Avoid wire-through-pin ambiguity, unintended junctions, four-way crossings, stacked labels, long loops, crowded bus entries. Orthogonal grid-aligned routes, visible junctions, consistent entry pitch, whitespace.
5. **Render before annotation.** Export every sheet to PDF and readable PNG; inspect whole pages, edges, dense crops (large ICs, modules, connectors, memories, buses, reset, power). Check specifically that no label (net labels, hierarchical labels, references, values, notes) overlaps a symbol, pin, wire or another label, and that the page looks clean overall. Fix overlaps, apparent floating functions, reversed flow, clipped items, avoidable label chains, then re-render and re-check; never judge this from the file text alone.
6. **Add layout guidance.** Tag each statement `[VERIFIED]`/`[COMPUTED]`/`[TARGET]`/`[ESTIMATE]`/`[NOT ESTABLISHED]` in the companion document; the sheet keeps a short plain-language pointer. Capture rate + edge-rate caveat, topology/stubs, reference plane, skew, current, trace/via intent, placement/keepout, source. Calculations and full URLs go in the companion document.
7. **Render again.** Reinspect every page and changed crop; reject any annotation hiding a wire, bus, pin, reference, value, heading, or dominant signal path.
8. **Prove preservation.** Re-export with the same adapter; run `python ${CLAUDE_SKILL_DIR}/scripts/compare_connectivity.py before after` (KiCad XML accepted). Require exact identities, net names, ref/pin memberships, no new ERC/lint findings, no protected layout changes. After any generator config/override change, prove the active variant in a deterministic manifest or sentinel output and repeat the comparison; ERC alone is insufficient.

## Scripted edits and agents

- Identity: never change symbol/pin UUIDs or instance paths; move items by coordinates only. A symbol moved to another sheet needs its PCB footprint `path`/`sheetname`/`sheetfile` updated (nothing else in the board file).
- Compare after every step: component UUID path, value, footprint; net members and names; ERC count. Normalize intentional changes (`_Small` to full-size library changes, reference maps) so only real changes show.
- Ask before electrical or naming changes (rail removal, sheet-pin rename, two names on one net, which raises an ERC `multiple_net_names` warning to accept).
- File safety: build the whole file in memory and check that it parses, then write a temp file and atomically replace the original. String escaping must round-trip exactly (`\n` in KiCad strings). Keep the 1.27 mm grid.
- Parallel agents: one agent per sheet file (a reused sheet file has one owner); a shared brief with the hard rules that they re-read every round; `kicad-cli` exports can fail briefly while another agent writes a file, so retry.
- Finish with a contact sheet of all pages to check that the style is consistent across the document.

## Per-edit cleanup (mandatory for every schematic edit)

Any schematic edit, in any session, is followed immediately by steps 3-5 above applied to that edit's local area only (not the whole sheet or other sheets): re-render the touched crop, fix overlaps and hygiene, place it in its sub-circuit box, and confirm the touched nets are as intended. The full workflow is for dedicated humanization requests.

## Completion report

Authoritative files, baseline/final counts, comparison result, ERC/lint before/after, protected-file proof, every page/crop inspected, limitations, final snapshot. Write `.pcba-workflow/schematic-visual-audit.json`. Route circuit findings to `/design-and-review-circuit`, not into visual approval. Copy-ready requests: [prompt-template.md](references/prompt-template.md).

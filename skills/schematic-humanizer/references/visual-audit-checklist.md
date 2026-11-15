# Visual audit checklist

Mandatory after every meaningful rearrangement and again after adding comments or layout guidance. Passing ERC doesn't pass the visual audit.

## Routing and buses

- Don't maximize wire count: direct local wiring where it clarifies a relationship; matched labels where a long wire would loop or spaghetti.
- Bus spines stay outside symbol bodies, values, references, notes, unrelated labels; large MCUs/modules need extra clearance.
- Never stack two different bus spines collinearly.
- Avoid wire-through-pin paths that look connected or create accidental connectivity; make branches and junctions explicit.
- Use the native grid; snap bus entries to it; consistent entry pitch and direction.
- Tools with two-point wire segments: one segment per bend; split bus backbones at T-tap endpoints when the format needs explicit junction geometry.
- Move pulls, terminations, decouplers, interface passives next to the circuit they support when it makes the function readable.

## Full-page inspection

Render every page to PNG at a resolution where pin labels are readable. Inspect:

- dominant left-to-right signal flow;
- functional grouping and sheet titles;
- apparent floating connectors, MCU support, power chains, controls;
- long loops, excess labels, clipped text, title-block collisions, empty areas hiding a broken flow;
- each page edge and every cross-sheet endpoint.

## Dense-area crops

Enlarged crops around:

- large MCUs, FPGAs, modules, memories;
- USB, Ethernet, RF, clock, external connectors;
- bus entries and places where multiple spines pass;
- power OR-ing, regulators, reset/boot, glue logic, ownership controls;
- anything changed since the previous render.

## Annotation gate

Render again after comments/callouts. Reject if a note hides a wire, bus, pin, reference, value, or functional heading; a URL is clipped; a callout interrupts the signal path; or density makes the sheet harder to scan. Move detailed tables and full links to a companion document; leave concise pointers on-sheet.

## Acceptance (all required)

1. Full-page inspection passed for every sheet.
2. Dense crops passed for every relevant interface and edited region.
3. No visible overlap, ambiguous junction, or apparent floating local function.
4. Connectivity comparison and ERC/lint pass independently.
5. Final snapshots shown or linked in the completion report.

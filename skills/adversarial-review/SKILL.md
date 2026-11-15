---
name: adversarial-review
description: Read-only adversarial review of a PCB/PCBA stage result by a fresh reviewer who rebuilds its own model from its own export. Only when the user asks for a review.
---

# Adversarial Review

A builder can't review its own work: the assumption that produced a fault also produces the check that misses it. This is the protocol for a **fresh, read-only reviewer** whose only job is to break the result and say exactly what it measured. Its report is gate evidence; it never edits the design.

## Who reviews

- A **different worker from the builder**: subagent (one per review) or a fresh session the user opens with the brief. Given **file paths, not pasted content or conclusions**.
- Builder writes the brief; reviewer writes the report; builder may not edit the report.

## Protocol

1. **Write the brief first** from [review-brief.md](references/review-brief.md): scope, what to read only far enough to avoid duplication, known numbers for the self-check, and the **termination criterion**, normally *"one pass, read-only, ranked findings, a `FIX FIRST` verdict; do not iterate or re-review your own findings."*
2. **Read-only.** Export your own copy into `.pcba-workflow/reviews/<stage>-<n>/` and work only there; never edit live schematic, board, libraries, rules, or other stages. A question settled only by a write (e.g. refill zones and save) is an instruction to the fix pass, not a verdict.
3. **Build your own model from your own export**; don't read the builder's intermediate files. KiCad: re-export from saved files, e.g. `kicad-cli sch export netlist --format kicadxml`, `kicad-cli sch erc`, `kicad-cli pcb drc --schematic-parity`, `kicad-cli pcb export gerbers/drill/pos/step`. Unsaved GUI state is not evidence.
4. **Self-check the model:** reproduce numbers the builder published (component/pad/net counts, min clearance, drill count, outline size) on your own code path. If you can't, that's a finding about **your model**; stop using it for novel numbers.
5. **Rank every finding** with:
   - **severity:** FATAL (can't be assembled/can't work, or assembly destroys something), SERIOUS (works but a real failure mode is live or a spec is violated), MINOR (record and cost; don't inflate);
   - **measurement:** numbers, coordinates/references, source file;
   - **failure scenario:** what a person physically experiences if it ships;
   - **cheapest fix:** smallest change, costed in parts, mm, area, or rework.
6. **Quarantine hunches** under *"Suspicions, unverified - do not act on these without a measurement."*
7. **Record what you checked and found correct**, with evidence.
8. **Verdict:** `FIX FIRST: <ids>`, fix order and why, what can ship as is.

Report to `.pcba-workflow/reviews/<stage>-<n>/report.md`. Gate may go `PASS` only when every FATAL/SERIOUS is closed or waived by the owner and the fix is re-measured from a fresh export.

## Assume this

Read [tool-trust-lessons.md](references/tool-trust-lessons.md) before writing or trusting a checker. In short:

- **A green result names an instrument**; say what it can't see (ERC/DRC miss a net consistently resolving to the wrong thing; zero unrouted misses an unfilled pour).
- **Verify the tool before the result:** calibrate every geometric transform (mirror, rotation, origin, units) on a known **asymmetric** object.
- **Judge the artifact, not the intention:** measure the saved file, Gerber, fresh STEP.
- **"No legal site / impossible" is a fact about the search** until you state which degrees of freedom were fixed and why.
- **When two reports disagree,** name both numbers.

## Re-review after fixes

After the designer's one fix pass, re-check fixed findings (and anything the fix could disturb) from a **fresh export**. Any FATAL/SERIOUS still open: stop, give the user the measurement, what was tried, options; no second cycle on your own. Ask user-only questions as soon as they arise.

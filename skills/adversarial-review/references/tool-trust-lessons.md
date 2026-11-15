# Tool-trust lessons

Adapted from `daishuge/pcb-skill` (MIT, see `../LICENSE`). Each lesson is a failure that passed a check that wasn't checking. Read-the-wrong-thing faults never look like errors.

## 1. A green board is not a correct board

- A schematic passed ERC with zero errors while the EDA silently merged five nets (a switch node into a card supply, an I2S data line and UART TX into ground). Only must-connect / must-not-connect / must-be-open assertions on the exported netlist caught it (`design-and-review-circuit/references/netlist-assertions.md`).
- KiCad analogues:
  - power symbols or global labels with the same name join nets across sheets;
  - hierarchical pins wired to the wrong label;
  - a label accidentally touching a wire end;
  - "power flag" symbols silencing ERC on an undriven rail.

## 2. Verify the tool before the result

- **Stale/cached model:** a 3D check measured the previous release's cached model (0 interferences; the board had 3); a footprint's 3D model came from its old name.
  - *Guard:* print size/hash of the exact file measured each run. A hole exists iff in the drill file, a pad iff in the copper Gerber, a mask opening iff in the mask Gerber.
- **Bounding box reported as pad:** a module's "two thermal lands" were bounding boxes over 20 small pads; a checker modelled obround pads as rectangles → 11 phantom violations.
  - *Guard:* carry true pad shape; test checkers on the part whose shape differs most from its box.
- **Copper labelled by wrong owner:** attributing pour copper by "which zone outline contains the point" mislabels where a lower-priority zone fills around a higher one.
  - *Guard:* attribute copper by connected component.
- **Mirror validated on symmetric object:** bottom-side transform used `x = -x` instead of `y = -y` and passed because 148 of 149 pads were symmetric two-terminal chips.
  - *Guard:* calibrate every transform on a known asymmetric part.
- **Async/stale instrument:** a DRC call returned the previous document's result on first read after a change.
  - *Guard:* re-run until the result repeats; run `kicad-cli` on the saved file, not a GUI panel; **save, close, reopen, re-measure** before calling a gate.
- **Wrong rule set loaded:** a routability estimate used intended 4-layer rules while the board carried a 2-layer profile with wider clearance.
  - *Guard:* read rules from the `.kicad_pro`/`.kicad_dru` being checked and layers/stackup from the `.kicad_pcb`.

## 3. A wait condition must fire on a crash

- An autorouter crashed (StackOverflowError) at 00:34; the JVM idled at 0 % CPU without exiting; the supervisor waited for "output exists or process gone" for 10 h 53 min.
- Every background-job wait must answer: **if this crashed now, would my filter emit a line?** Cover:
  - output present (non-empty, log says complete);
  - crash signature in log;
  - process gone;
  - wall-clock timeout;
  - progress-rate floor.
- Not every logged exception is terminal; named fatal errors are.
- Measure input size before feeding an external tool: the fix was protecting 51 traces instead of 3 326, not more stack.
- Applies to Freerouting (DSN export → route → SES import) and any long `kicad-cli` job.

## 4. Judge connectivity by islands merged, not edges drawn

- A walker merging any two nodes at the same XY counted an inner-layer track and a top-layer track as connected with no via. Connectivity must be layer-aware: only a via or plated hole joins layers.
- A declared pour is not an existing pour: judge by filled copper, not the refill call's return. Compare DRC on stored fills with `kicad-cli pcb drc --refill-zones` (no `--save-board`); a difference means stale fills.
- A via is redundant only if deleting it leaves the net in one piece **and** it isn't the return path for a nearby layer change, RF stitching, or thermal path.

## 5. "No legal site" is not an answer while neighbours can move

- A fix pass left two bias resistors undone ("no legal site within 6 mm"). Ruling: move the neighbours.
- Before writing "impossible", state the degrees of freedom held fixed and the measurement proving it.

## 6. Reviews disagree; the disagreement is data

- Two reviewers used different rows of one standard for one clearance; two read different layers of one differential pair.
- Name both numbers, say which is right and why; quiet disagreement gets reconciled badly.

## 7. Review the reviewer's tooling too

- A verification pass's first eleven violations were all its own bugs. Keep wrong versions and root causes visible.
- A checker that has never been wrong has never been tested.

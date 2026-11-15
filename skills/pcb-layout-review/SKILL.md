---
name: pcb-layout-review
description: PCB placement, routability, stackup, routing, planes, DRC/DFM, and 2D placement mechanics; also porting a proven board to a variant.
---

# PCB Layout Reviewer

> `${CLAUDE_SKILL_DIR}`: scripts in `scripts/`, sibling skills in the parent folder. In references, `<skill-dir>` = this directory, `<skills>` = its parent. Run scripts from `pcb/` (or use absolute paths).

Use the humanized architecture and circuit constraints as placement policy, not reference-number order or one global wire-length score. Read [layout-review-checklist.md](references/layout-review-checklist.md) (incl. "Proven lessons"); record the gate with [layout-review-record.md](references/layout-review-record.md); KiCad commands in [kicad-adapter.md](references/kicad-adapter.md). Gerber/drill/CPL or images alone allow DFM and visual review only, not connectivity proof.

Read when they apply:

- [design-rules.md](references/design-rules.md): net classes, power paths, vias, high-voltage clearance, controlled impedance.
- [layout-patterns.md](references/layout-patterns.md): the section for the block being placed/routed.
- [placement-mechanics.md](references/placement-mechanics.md): always, before placement freeze and release.
- [connector-stack-and-fanout.md](references/connector-stack-and-fanout.md): modules, card sockets, board-to-board, dense connector fanout.
- [variant-porting.md](references/variant-porting.md): derivative of a proven board.

## Project rules

1. **Board size first:** the user sets size/outline before any placement.
2. **Sheet by sheet, placement first:** place one sheet, then **stop for user check; no pours or routing**. After approval do pours and routing, stop again. Next sheet only after approval.
3. **No automatic review:** no reviewer agent unless the user asks; skip `/adversarial-review` steps until then.
4. Stackup, via, pour, and thermal via rules: `design-rules.md` section 1 and `layout-patterns.md` (GND stitching and planes, Thermal).
5. DRC passing is necessary, not sufficient: inspect 2D plots of both sides (no 3D unless asked). Zero unrouted pads is not a release gate: check real DRC, power/GND zone connectivity, same-net zone islands.

## Establish truth

1. Read repo rules, native board/project, brief, architecture, `DECISIONS.md`, sourcing lock, circuit review, bring-up plan, netlist, mechanics, enclosure, fab constraints, project layout lessons.
2. Identify the board source of truth. KiCad: native CLI/API; other EDA: equivalent native exports.
3. Before changing anything record: hashes, layer stack, net classes, rules, placement, connectivity, raw and classified DRC, via/drill histogram, top/bottom 2D assembly plots. **Read the rules and stackup actually stored** in `.kicad_pro`/`.kicad_dru`/`.kicad_pcb`.
4. Record connector maturity and assembly dimensions as measured, drawing-derived, inferred, or TBD. A plausible 3D model is visual evidence, not mechanical proof.
5. Separate hard constraints from negotiable targets. Never trade a short, new open, broken return path, unsupported pad, keepout violation, unsafe ownership state, or fab violation for a better score.

## Review in order

1. **Architecture placement:** connector pin order along functional corridors; protection, translation, processing, memory, outputs along real flow; ownership/reset controls direct.
2. **Critical locality:** decoupling in the supply-pin escape path, tight regulator loops, crystals/feedback, connector protection, antenna edge/keepout, user access, thermal, enclosure clearance. Place the bring-up plan's test pads, strap pads, rail-isolation links now.
3. **Placement mechanics (2D):** run `placement-mechanics.md` (courtyards/Fab, nothing under module bodies, connector mouths, keep-outs, hand-fit access, enclosure). No 3D or height analysis unless asked.
4. **Routability:** before routing run the checklist's routability section (via-lane widths, fine-pitch escape arithmetic, parts with no via-capable side, legal escape for every dense connector/module power and GND pad). Zero courtyard overlaps can still be unroutable. "No legal site" is not an answer while neighbours can move.
5. **Layers/reference:** choose layer count from bus density, channels, return paths, RF, controlled interfaces, current, size, cost. A solid reference plane usually beats a low-current power plane; never assume 4 or 6 layers without analysis.
6. **Routing:** continuous return paths, short critical controls, sensible topology, no forbidden stubs, right width/spacing, matching only where budgets require, legal transitions.
7. **Power and zones:** prove every rail/GND pad reaches its network. Same net name, overlapping fill, or zero pad-opens is not proof. Connectivity is layer-aware; a declared zone is not a filled zone. Compare DRC on stored fills with `kicad-cli pcb drc --refill-zones` (no `--save-board`); a difference means stale fills.
8. **Manufacturing:** compare trace/space, annulus, drill, via type, finish, thickness, impedance, drill count and cost thresholds with the current fab quote. Premium features are DFM feedback, not a reason to weaken electrical constraints.
9. **Independent visual pass:** clean 2D views, each signal layer, fresh top/bottom 2D plots (Fab + SilkS + CrtYd + Edge.Cuts). Verify outlines, pin 1, polarity, connector overhang, pad support, antenna, outline, keepouts, silkscreen. Run silk-over-silk, silk-over-copper, edge-clearance checks first; keep pin-1/polarity/function; unresolved dense labels stay `USER_REVIEW`.

Placement and routing are separate passes with a user check between: floorplan problems must be found before copper exists.

## Experiment safely

- Use named candidate states and paired project files; one coherent change, then measure raw disconnects, real DRC, power disconnects, layout gates, mfg defects.
- Record with `${CLAUDE_SKILL_DIR}/scripts/score_experiment.py`; project lessons with `${CLAUDE_SKILL_DIR}/scripts/record_lesson.py` (both write to `.pcba-workflow/`, never the installed skill).
- Freeze input; compare stackup, outline, via-process, routing experiments against the best safe candidate using the full gate vector. A bigger board or extra layer counts only if it removes a measured blocker without regressing another gate.
- Prefer high-scoring methods; don't repeat a negative method unless conditions changed. Accept only measured net improvement with no new opens, real DRC, power disconnects, or mfg defects. A route for one trapped net isn't promotable if its coupled donor set is incomplete or another lane is stranded.
- Autorouter (e.g. Freerouting DSN/SES): measure input size first; supervise for crash/stall (output present, crash signature in log, process gone, wall-clock timeout, progress-rate floor). Judge the board read back into KiCad, not the session file.

## Release gate

- Zero unexplained raw disconnects, zero real DRC errors, zero power disconnects, all project layout checks passing, verified planes/critical nets, visual/mechanical/silkscreen PASS, all in the same saved state. Save, close, reopen, re-measure first.
- Unverified connector body, card thickness, insertion depth, retention, or enclosure stack: stays `USER_REVIEW` or `BLOCKED` even if DRC is clean.
- If the user asked for `/adversarial-review` of the routed board, no open FATAL/SERIOUS.
- Waivers: narrow, evidence-backed, in `.pcba-workflow/layout-review.json`. Hand off to `/release-pcba-fabrication`. JLCPCB's placement preview after upload is the user's check.

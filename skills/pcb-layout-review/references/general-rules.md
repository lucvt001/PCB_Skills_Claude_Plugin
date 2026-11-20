# General layout rules (every project)

**Read this whole file before the first placement, routing, pour, or review action of every layout session**, and again after a session is resumed or context is compacted, even if you think you remember it. It holds only rules that apply to every board. Block-specific rules (power widths, regulators, USB, shunts, connectors, ...) are in `rules/` and are loaded per block as `SKILL.md` describes; they are not repeated here.

## 1. Precedence

- The part's datasheet and EVM/reference layout override the generic rules in this skill.
- `board-defaults.md`, `DECISIONS.md`, and explicit user instructions override generic rules.
- A conflict between a datasheet requirement and a board default or decision (e.g. datasheet requires via-in-pad) goes to the user; never resolve it silently.

## 2. Process rules

1. **Board size first:** the user sets size/outline before any placement.
2. **Sheet by sheet, placement first:** place one sheet, then **stop for the user's check; no pours or routing**. After approval do pours and routing for that sheet, stop again. Next sheet only after approval. Floorplan problems must be found before copper exists.
3. **No automatic review:** no reviewer agent unless the user asks; skip `/adversarial-review` steps until then.
4. **2D only:** inspect 2D plots of both sides; no 3D or height analysis unless asked. For a part known to be tall near a lid or wall, ask the user to check their mechanical CAD.
5. **DRC passing is necessary, not sufficient.** Zero unrouted pads is not a release gate (see section 7).

## 3. Establish truth before changing anything

1. Read repo rules, native board/project, brief, architecture, `DECISIONS.md`, sourcing lock, circuit review (incl. its layout handoff constraints), bring-up plan, netlist, mechanics, enclosure, fab constraints, and project layout lessons in `.pcba-workflow/`.
2. Identify the board source of truth (KiCad: native CLI/API, see `kicad-adapter.md`). Gerber/drill/CPL or images alone allow DFM and visual review only, not connectivity proof.
3. Record: hashes, layer stack, net classes, rules, placement, connectivity, raw and classified DRC, via/drill histogram, top/bottom 2D assembly plots. **Read the rules and stackup actually stored** in `.kicad_pro`/`.kicad_dru`/`.kicad_pcb`; confirm the board has the copper layers you plan to use.
4. Separate hard constraints from negotiable targets. Never trade a short, new open, broken return path, unsupported pad, keepout violation, unsafe ownership state, or fab violation for a better score.

## 4. Placement (all boards)

**Architecture drives placement**, not reference-number order or one global wire-length score.

- Place from the humanized architecture: connector pin order along functional corridors; protection → translation → processing → memory → outputs along real signal flow, without needless backtracking. Ownership/reset controls direct.
- Freeze placement from architecture and physical connector pin order *before* optimizing wire length or launching an autorouter.
- Support parts sit at their function (regulator loops, crystals, feedback, ESD, terminations, pulls, reset/boot, current sense). The *how* is in each block's category file.
- Place the bring-up plan's test pads, strap pads, and rail-isolation links during placement, not after routing.

**Decoupling (every IC):**

- Order along the current path: **supply pin → capacitor → via to GND plane**; smallest capacitor closest to the pin; its GND via right at its pad, not shared through a long trace.
- One small cap (typically 100 nF) per supply pin/pair, same side as the IC where possible; bulk (e.g. 4.7-10 uF) per rail near the IC group, at rail entries, and where load steps occur.
- No via between pin and capacitor unless the capacitor sits directly under the pin on the other side.
- Two vias per capacitor pad on fast or high-current rails.

**Footprints are the 2D body:**

- Every footprint has a courtyard and F.Fab/B.Fab outline matching the exact MPN drawing in plan view. Missing or copied outlines blind every clearance check on that side.
- Large/critical parts: verified MPN, package, footprint, pin 1, courtyard/Fab outline against the drawing.
- Run `courtyards_overlap` and `missing_courtyard` as errors; read every violation; no bulk waivers.
- Rotating a part and renumbering its pads is **one** change, never two (a rotated connector can put a supply on a ground pin).
- **Nothing inside another part's body:** check every part, including small passives, against every module, shield-can, and connector courtyard.

**Keep-outs:** a keep-out on a user/documentation layer does not constrain zone fill. Use rule areas on **every relevant copper layer**, and confirm from Gerbers or a copper-layer SVG that the region is empty on each.

**Record two passes separately:** logical/constraint placement and visual/mechanical placement. Re-plot top and bottom 2D assembly views (Fab + SilkS + CrtYd + Edge.Cuts) after every footprint, rotation, or position change.

## 5. Routability check (before any routing)

Zero courtyard overlaps can still be unroutable. Before routing:

- Sweep free spans between parts; count those at least **via pad + 2 x clearance** wide (not track + clearance). Report the via-capable fraction.
- List every part with **no** via-lane side; fix by moving parts, not by hoping the router copes.
- Every power and GND pad of dense ICs, modules, and connectors has a legal escape (details in `rules/fine-pitch-ics-and-fanout.md` / `rules/dense-connectors-and-board-stacks.md`).
- Route shared spines and scarce corridors first; reserve power fanout capacity before dense signals. Late common-bus routing strands endpoints.
- A placer/router failure is a fact about the search: before calling a placement impossible, state which parts were held fixed and why. "No legal site" is not an answer while neighbours can move.

## 6. Routing (all boards)

- **Layer count** is justified by bus density, channels, return paths, RF, controlled interfaces, current, size, cost; the starting point is in `board-defaults.md`. A solid reference plane usually beats a low-current power plane.
- **Return paths:** never route a fast, sensitive, or controlled signal across a split or void in its reference plane. At every layer change of such a signal put a GND via within ~1-2 mm of the signal via. Where the via sits in a pour, the pour-edge pairing in `board-defaults.md` section 5 applies instead.
- Keep critical controls short; control via counts and layer changes where they matter; no forbidden stubs; no meanders unless a timing budget needs them.
- Trace width follows the ladder in `board-defaults.md` section 3 (0.762 → 0.508 → 0.254 mm); never 90° bends. Spacing comes from the template's JLCPCB rules. Never treat different power nets as one category in collision checks.
- No copper, via, component, or mask feature may violate outlines, cutouts, fingers, contacts, antennas, mounting, or enclosure keepouts.
- Check a new through-via on every layer it traverses; verify it keeps its net after save and after any zone refill.
- After local edits refill only the affected zones; a global refill can change connectivity under rule/setting drift.

## 7. Verify connectivity, zones, DRC

- Inspect every raw unconnected item; treat signal and power ones as real until proven otherwise. Zero pad-opens is insufficient while track/track, track/via, or zone/plane pieces remain separated.
- Prove every rail/GND pad reaches its network. Same net name, overlapping fill, or zero pad-opens is not proof. Connectivity is layer-aware; a declared zone is not a filled zone.
- Compare DRC on stored fills against `kicad-cli pcb drc --refill-zones` (no `--save-board`); a difference means stale fills.
- Same-net zone fragments are real opens until each is proven to reach the canonical rail (blanket stitches or island deletion are not proof).
- DRC rules are the template's JLCPCB rules (`board-defaults.md` section 2), not values chosen to make the report green. Classify intentional fab geometry narrowly; no broad waivers.
- Every via inside an SMT pad follows `board-defaults.md` section 5 (plugged/tented, windowpane paste); flag any that don't.

## 8. Manufacturing and visual pass

- Via/drill histogram; compare trace/space, annulus, drill, via type, finish, impedance, drill count and cost thresholds with the current fab quote. Premium features are DFM feedback, not a reason to weaken electrical constraints.
- Live quote surcharges are feedback: resize only verified-legal features, keep density-critical exceptions, regenerate all checks and release artifacts, compare the new quote.
- Independent visual pass: each signal layer, fresh top/bottom 2D plots. Verify outlines, pin 1, polarity, connector overhang, pad support, antenna, keepouts, silkscreen. Missing/offset body outlines, wrong pin 1/polarity, unsupported connectors, or mechanical collisions block release even with clean copper DRC.
- Silkscreen: text size per `board-defaults.md` section 7; run silk-over-silk, silk-over-copper, edge-clearance checks first; normalize and classify; keep pin-1, polarity, and function markings readable; unresolved dense labels stay `USER_REVIEW`, never silently deleted.
- Inspect assembly side, paste, fiducials, tooling/depanel, edge treatments.

## 9. Release gate

- Zero unexplained raw disconnects, zero real DRC errors, zero power disconnects, all project layout checks passing, verified planes/critical nets, visual/mechanical/silkscreen PASS, **all in the same saved state**. Save, close, reopen, re-measure first.
- Unverified connector body, card thickness, insertion depth, retention, or enclosure stack stays `USER_REVIEW` or `BLOCKED` even if DRC is clean.
- If the user asked for `/adversarial-review` of the routed board: no open FATAL/SERIOUS.
- Waivers: narrow, evidence-backed, in `.pcba-workflow/layout-review.json` (schema: `layout-review-record.md`). Hand off to `/release-pcba-fabrication`. JLCPCB's placement preview after upload is the user's check, not PCB placement validation.

## 10. Evidence and lessons

- Tag numbers `[VERIFIED]`, `[COMPUTED]`, `[TARGET]`, `[ESTIMATE]`, `[NOT ESTABLISHED]` (definitions: workflow skill).
- Record project lessons with `scripts/record_lesson.py` (writes to `.pcba-workflow/`, never the installed skill).

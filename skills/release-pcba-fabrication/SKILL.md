---
name: release-pcba-fabrication
description: Build and verify the Gerber/drill/BOM/CPL release for one frozen revision, including the JLCPCB CPL rotation/offset check.
---

# PCBA Fabrication Release

> `${CLAUDE_SKILL_DIR}`: scripts in `scripts/`, sibling skills in the parent folder. In references, `<skill-dir>` = this directory, `<skills>` = its parent. Run scripts from `pcb/` (or use absolute paths).

Release artifacts; don't redesign circuit or layout here. Read [release-checklist.md](references/release-checklist.md) and the export commands in [../pcb-layout-review/references/kicad-adapter.md](../pcb-layout-review/references/kicad-adapter.md). Record tool/version, source revision, origin, units, every command. Only derived fab files exist: native-source traceability is BLOCKED or USER_REVIEW; never reconstruct a revision from filenames.

## Preflight

1. Read repo rules, sourcing lock, circuit/layout gate results, waivers, native files, fab constraints, quantities, manufacturer capabilities.
2. Freeze one named revision, record hashes. Stop if schematic, PCB, BOM, CPL source, sourcing lock, or constraints disagree.
3. Circuit and layout gates must be PASS. Zero opens alone is not enough: raw connectivity, real DRC, power connectivity, planes, critical nets, mechanical and visual review all resolved.

## Generate

- Export with the authoritative EDA tool: all layers, mask, paste, silkscreen, outline/cutouts, mechanical info, plated/non-plated drill, drill map/report, BOM, CPL, assembly drawings, stackup/impedance notes, and top/bottom **2D assembly plots** (SVG of Fab + SilkS + CrtYd + Edge.Cuts; the `render_top`/`render_bottom` artifacts). No raytraced 3D. Preserve units, origin, side/rotation convention, DNP policy, polarity, pin-1 evidence.
- **Verify the package independently of the producing EDA** (e.g. GerbView): outline and dimensions, copper layer count **and** copper present in each file, drill census, mask opening per pad, nothing outside outline (measure hole edges, not centres), keep-outs empty on every copper layer, text, apertures, edge treatments, panel/depanel needs, assembly side. Where two code paths agree (EDA DRC and viewer/checker), record both; that agreement is "verified".
- **CPL rotation/offset:** follow [cpl-placement-review.md](references/cpl-placement-review.md); run `${CLAUDE_SKILL_DIR}/scripts/check_cpl.py` on the saved board and KiCad position file. It blocks on reference-set mismatch, inconsistent export transform, footprint origins off package centre, and polarised parts without an approved rotation in `.pcba-workflow/cpl-corrections.json`; it writes `cpl-jlcpcb.csv` with only approved corrections. Upload that, not KiCad's raw file.
- **Drills:** one drill file can be a subset of another; count unique features including slots; cross-check the report. Export a via/drill histogram and flag every feature below the standard-cost threshold.
- **Order-form checklist** for settings files can't carry (layers, stackup, thickness, copper weight, finish, via treatment, impedance, rails/fiducials, corner rounding, PCBA tier/side); see [jlcpcb-constraints.md](references/jlcpcb-constraints.md). Include `.pcba-workflow/bringup-plan.md` and the hand-fit parts list.

## Manifest

Build `.pcba-workflow/release-manifest.json` with `${CLAUDE_SKILL_DIR}/scripts/build_release_manifest.py` (explicit revision per artifact; mixed revisions rejected). Record:

- artifact SHA-256, size, role, revision (source and derived);
- board dimensions, layers, thickness, finish, stackup, controlled options, quantities, assembly side, DNP policy;
- ERC, raw connectivity, classified DRC, power, layout, DFM, visual results;
- waivers and sourcing-lock hash/time;
- substitution, placement, final-price, payment approval state.

Run `${CLAUDE_SKILL_DIR}/scripts/validate_release_manifest.py` after packaging. Missing file, hash drift, mixed revision, stale lock, or failed check blocks release. `/adversarial-review` of the package only on request; then no open FATAL/SERIOUS.

- Release from one saved, committed revision. Never upload, order, or pay on JLCPCB.
- Put it in `production/<rev>/`. A withdrawn package moves to `production/superseded/<rev>/` with a reason; regenerate the whole release, don't patch files.

## Handoff

- Deliver an immutable release directory: manifest, manufacturing and assembly files, constraints, review evidence.
- State the exact upload Gerber/archive, BOM, CPL, and the order-form checklist.
- The user uploads to JLCPCB and checks part matching and placement preview via Stage 2 of `cpl-placement-review.md` (anchors per side, then every part). Screenshots/placement exports can return to Claude for `${CLAUDE_SKILL_DIR}/scripts/reconcile_cpl_import.py` and a second look.
- Rotation/offset error in the preview: fix in source (footprint origin or `cpl-corrections.json`, preview as evidence) and regenerate; never patch only in the browser.

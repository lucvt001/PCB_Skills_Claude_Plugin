# Manufacturing release checklist

## Revision integrity

- Native schematic/generator, PCB/project, sourcing lock, BOM, CPL generator, constraints, derived files identify one revision.
- Source and output hashes recorded after final generation.
- Any circuit, MPN/package, footprint, placement, routing, zone, BOM, or CPL change invalidates affected outputs; regenerate.

## Fabrication outputs

- Complete copper, mask, paste, silkscreen, outline, cutout, required mechanical layers.
- Plated and non-plated drills, slots, drill map/report, via/drill histogram.
- Where applicable: dimensions, layer count, thickness, material, finish, copper weight, stackup, impedance intent, edge treatment, fingers/contacts, castellations, controlled depth, panel/depanel instructions.
- Independent viewer check for missing/duplicate layers, outline gaps, inverted mask, clipped copper, text on pads, drill anomalies, unintended features.

## Assembly outputs

- BOM: exact references, quantities, values, MPNs, supplier parts, package, DNP status, approved-alternate policy.
- CPL: exact assembled reference set, declared units/origin, side, X/Y, rotation convention; pin-1 evidence for every polarized/asymmetric package.
- Assembly drawing and top/bottom 2D assembly plots agree with BOM/CPL and board source.
- Footprint pads, paste, exposed tabs, connector anchors, package bodies visually checked.

## Independent verification and order handoff

Adapted in part from `daishuge/pcb-skill` (MIT, see `../LICENSE-pcb-skill`).

- Gerbers re-read by a different tool: copper file count and content, outline, drill census (subset files and slots handled), mask openings per pad, min clearance agree with EDA numbers.
- Every keep-out verified empty on each copper layer it must constrain.
- Optional STEP for enclosure CAD fresh from the released board (export only; no 3D review).
- Order-form checklist covers every setting the files can't carry.
- Bring-up plan and hand-fit parts list included.
- Withdrawn packages moved to `production/superseded/` with a reason.

## Gate evidence

- ERC/equivalent, raw connectivity, real DRC, power connectivity, layout checks, critical-net measurements, DFM, visual/mechanical review.
- Every waiver narrow, evidence-backed, owner-approved, listing what it does not waive.
- Sourcing evidence current for the intended order date.

## `PASS` manifest contract

Enforced by the release builder/validator:

- **artifact roles:** `board_source`, `eda_project`, `gerber`, `drill`, `bom`, `cpl`, `constraints`, `render_top`, `render_bottom`, `circuit_review`, `schematic_connectivity`, `schematic_visual_audit`, `layout_review`, `sourcing_lock`.
- **constraints:** positive `board_width_mm`, `board_height_mm`, `layer_count`, `thickness_mm`, `quantity_pcbs`, `quantity_assembled` (≤ PCB quantity); nonempty `surface_finish`, `assembly_sides`.
- **zero-valued checks:** `unexplained_raw_disconnects`, `real_drc_errors`, `layout_check_failures`.
- **PASS checks:** `circuit_gate`, `layout_gate`, `raw_connectivity`, `power_connectivity`, `visual_mechanical_review`, `dfm_review`, `sourcing_lock_current`, `revision_reconciled`.
- **boolean** `design_critical_substitution_required`; when true, separate substitution approval and evidence must be present.

Assembly placement, final-price, and payment approvals normally stay pending at fab release and are not transferred from one another.

# CPL rotation and offset check

JLCPCB places each part's package centre at `Mid X`/`Mid Y` and rotates to `Rotation` relative to **its own** library model's zero angle; KiCad exports the footprint origin and KiCad's zero angle. Where they differ, parts come out shifted or rotated (a reversed diode or 90° IC is a dead board). Two stages: before upload (Claude), after upload (user + Claude).

## Stage 1: before upload (`<skill-dir>/scripts/check_cpl.py`)

```bash
"$K" pcb export pos --format csv --units mm --side both -o ../.pcba-workflow/pos.csv template.kicad_pcb
python <skills>/release-pcba-fabrication/scripts/check_cpl.py \
  --board template.kicad_pcb --pos ../.pcba-workflow/pos.csv \
  --corrections ../.pcba-workflow/cpl-corrections.json \
  --out ../production/<rev>/cpl-jlcpcb.csv --report ../.pcba-workflow/cpl-check.json
```

It blocks on:

1. **Reference set:** every placeable footprint (not DNP, not excluded from position files) appears exactly once; nothing extra.
2. **Export transform:** all rows follow one transform (KiCad flips Y, uses board/aux origin); mixed or mirrored export blocks.
3. **Origin offset:** footprint origin >0.05 mm from pad centre (e.g. on pin 1, a tab, a peg). Fix the origin to package centre or add an `offset_mm` correction.
4. **Rotation unverified:** every polarised/asymmetric part (>2 pads, or prefix U, Q, D, LED, J, P, CN, Y, X, SW, K, T, BT, IC, PS) needs a correction entry for its footprint **and side**, even at rotation 0.

- Writes the JLCPCB CPL (`Designator, Mid X, Mid Y, Layer, Rotation`) with only approved corrections applied.
- Can't see JLCPCB's library models; that's Stage 2.

### Corrections file

`.pcba-workflow/cpl-corrections.json`: one entry per footprint and side, each with evidence. Copy from [../assets/cpl-corrections.example.json](../assets/cpl-corrections.example.json).

```json
{
  "schema": "cpl-corrections-v1",
  "footprints": {
    "Package_TO_SOT_SMD:SOT-23": {
      "top": {"rotation_deg": 180, "evidence": "JLCPCB preview, order v1.0, U101 pin 1 checked"}
    },
    "Conn:Pin1Origin": {
      "top": {"rotation_deg": 0, "offset_mm": [1.0, 0.0], "evidence": "datasheet body centre"}
    }
  }
}
```

- `offset_mm` is in the footprint's local frame (as in the footprint editor); the script rotates it.
- Bottom parts need their own `bottom` entry; the same package often needs a different correction there.
- Keep the file across revisions: it's the project's memory of JLCPCB conventions.

## Stage 2: after upload (user + Claude)

1. User uploads Gerbers, BOM, `cpl-jlcpcb.csv`; opens JLCPCB's placement preview.
2. **Anchors first:** at least three separated, non-collinear, polarised parts per assembled side, incl. every package family with a known origin/angle exception. Same error on all anchors: suspect a whole-board issue (origin, mirroring, units) before per-part fixes.
3. **Then every part** at useful zoom: each lead/terminal on its pad, pin 1, diode/LED/electrolytic polarity, connector mouth direction, exposed/thermal pad, nothing shifted or off-board. Top and bottom screenshots can go to Claude for a second look (2D images).
4. If JLCPCB's table can be copied/exported, compare with what was submitted (nonzero exit blocks):

   ```bash
   python <skills>/release-pcba-fabrication/scripts/reconcile_cpl_import.py \
     --submitted ../production/<rev>/cpl-jlcpcb.csv --imported jlcpcb-imported.csv \
     --report ../.pcba-workflow/cpl-reconcile.json
   ```

5. **Fix every mismatch at the source:** add/change the `cpl-corrections.json` entry (preview as evidence) or fix the footprint origin, regenerate, re-upload. Browser-only nudges in JLCPCB's editor are diagnostics, lost on the next order, leaving the release wrong.
6. Repeat until every part passes; then the user approves placement (`assembly_placement` approval).

## Record

Stage 1 result is in `.pcba-workflow/cpl-check.json` (script-written). Note the Stage 2 outcome (anchors checked, per-part result, corrections added, upload iteration, final CPL SHA-256) in the release manifest's `assembly_placement` evidence.

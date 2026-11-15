# JLCPCB order constraints the design must respect

Adapted from `daishuge/pcb-skill` (MIT, see `../LICENSE-pcb-skill`), measured on JLC's Chinese site (jlc.com). The **international site (jlcpcb.com) doesn't share its fee schedule or coupon rules**. Treat each item as a question to check on live jlcpcb.com pages; tag answers VERIFIED (URL + date) or NOT ESTABLISHED. Read before fixing outline, stackup, or rules: every constraint is free at sketch stage, expensive at Gerber stage.

## Assembly-tier limits (DFM gate, not a fee)

- Read the current PCBA capabilities page for the tier you'll order (Economic vs Standard); record: smallest chip package, minimum IC pin pitch, minimum BGA pitch, one-/two-sided placement, supported thicknesses and layer counts, quantity range, excluded part classes (e.g. moisture-sensitive, low-temperature).
- On the CN site Economic was single-sided, 0402 minimum, ~0.4 mm IC pitch; verify current jlcpcb.com values.

## JLCPCB may change the outline

- JLC may add process rails/fiducials and round outline corners for SMT orders without notice.
- If enclosure/hull fit depends on exact corners or edges: design for the tolerance, or record the order option/remark preventing it and confirm on the order page.

## Drill count, slots, fees

- CN site charges an uncapped excess-drilling fee above a holes-per-area threshold. **jlcpcb.com equivalent: NOT ESTABLISHED**; check the current "extra charges" help article and compare quotes before relying on a dense via field.
- **Count holes correctly:** one drill file can be a strict subset of another (vias-only inside full PTH); summing double-counts. Count unique drilled features, include slots (`G85` in Excellon), cross-check the drill report.
- Small drills and tight via annulus can trigger premium processes: compare two live quotes with different drill settings.

## Settings the design files can't carry

Write each into the release's order checklist:

- layer count and **stackup selection** (KiCad's stackup doesn't select JLCPCB's laminate; pick the matching one on the form, esp. for impedance control);
- thickness, copper weights (outer/inner), surface finish, mask and silk colour;
- impedance control on/off and which stackup;
- via treatment (tented/plugged/filled); on Gerber upload the mask openings normally govern tenting, so make sure the design tents what you intend;
- panelisation/rails/fiducials and the corner-rounding remark;
- PCBA tier, assembly side, quantity, parts to leave unplaced;
- stencil, if wanted.

**Set the layer count first**, before reading other option lists; available finishes and options change with it.

## Quote sanity

- Capture the itemised quote; compare with expected price; investigate unexpected lines.
- Free/promotional price expected but not shown in the total: stop; a condition isn't what you think.
- Don't publish the design publicly before ordering if a coupon/promotion excludes open-source designs.

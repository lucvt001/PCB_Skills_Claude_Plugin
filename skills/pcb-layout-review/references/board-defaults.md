# Board defaults

Project-wide defaults set by the user. Read in full at session start, after `general-rules.md`. A project's `DECISIONS.md` or an explicit user instruction overrides them; any other deviation needs the user's approval. A datasheet requirement that conflicts with a default goes to the user.

## 1. Stackup: 4 layers

| layer | use |
|---|---|
| F.Cu | components, signal and power routing/pours |
| In1.Cu | **solid GND plane**; no routing |
| In2.Cu | **solid GND plane**; no routing |
| B.Cu | signal and power routing/pours |

- Both inner layers are GND; route all signals and power on the outer layers.
- **Copper weight:** 1 oz (35 um) on F.Cu and B.Cu, 0.5 oz (17.5 um) on In1.Cu and In2.Cu. Use these columns in any current or impedance calculation, and set them in the KiCad stackup.
- Board thickness: **don't care**; it is set in the manufacturing order. Don't analyse or report it.
- Impedance work only: read the stored stackup and set it to the JLCPCB stackup chosen for the order (`rules/differential-pairs-and-impedance.md`).

## 2. Clearance rules

- **Don't invent clearance rules.** Use the JLCPCB rules already in the project template (`.kicad_pro`/`.kicad_dru`). The only stated exception is the 0.3 mm pour clearance (section 6).
- Nets at >= 31 V: flag them to the user with the value from `rules/high-voltage-clearance.md`; don't create a net class without approval.

## 3. Trace width

Width ladder for every trace **except** impedance-controlled nets (their width comes from the impedance calculator):

1. **0.762 mm wherever it fits**, including short hops between neighbouring components and especially long traces on the bottom layer.
2. If 0.762 mm doesn't fit, try **0.508 mm**.
3. Only then **0.254 mm**. Use it when routing into IC pins.
4. On fine-pitch pads where 0.254 mm doesn't fit, neck to **0.127 mm only for the last stretch into the pad**, then widen back up the ladder as soon as it is clear of the pin field.

- **Current:** up to 1 A, the ladder is enough; don't calculate width vs current. **Above 1 A, use a copper pour** (section 6), sized per `rules/power-routing-and-pours.md`.

## 4. Trace geometry

- **Never use 90° bends.** Use 45° corners (or arcs). Also no acute angles.

## 5. Vias

- Default via: **0.64 mm diameter / 0.30 mm drill, plugged and tented on both sides.**
- **Vias under pads** (e.g. thermal/exposed pads) are allowed. Plugged-and-tented vias aren't perfectly flat, so: paste on that pad goes in a **windowpane pattern covering 50-70 % of the copper pad**, with the vias sitting in the gaps between paste windows.
- Small signal pads on fine-pitch parts: fan out with a short trace to a via (dogbone), not a via in the pad.

### Stitching / pour-edge vias

**Read this subsection again every time the user says "apply stitching vias", and follow it exactly.**

- **Non-ground vias** (power or signal layer changes in or through a pour) sit on the **very edge of the pour perimeter**: the via's annular ring is **tangent to the pour edge** from inside. Never in the middle of a pour.
- **Each non-ground via gets a ground via right across the pour edge**, **0.3 mm between the two annular rings** (centre-to-centre 0.64 + 0.3 = 0.94 mm `[COMPUTED]`), on the line perpendicular to the pour edge.
- With a two-layer pour (section 6) the via lies on the perimeter of both layers at once.
- GND stitching between ground pours and the inner planes: see `rules/power-routing-and-pours.md`.

## 6. Copper pours

- **Fill:** solid (not hatched).
- **Clearance:** 0.3 mm.
- **Corner smoothing:** fillet, 0.2 mm radius.
- **Pad connection:** solid everywhere (no thermal relief spokes), SMD and through-hole.
- **Few vertices:** draw each pour outline with as few vertices as possible (rectangles and simple polygons) so a human can edit it easily. Let the fill clearance shape the copper; don't trace around obstacles by hand.
- **High current (> 1 A): large pours.** Prefer **one zone on both F.Cu and B.Cu** (same outline, both layers ticked) where possible, so vias sit on the shared perimeter for both pours.
- Any pour spanning several layers is **one** zone with multiple layers ticked.

## 7. Silkscreen text

- All silkscreen text (reference designators, labels): **1.0 mm width, 1.0 mm height, 0.15 mm line thickness**.

## 8. Mounting holes

- **M3** by default: KiCad `MountingHole_3.2mm_M3*` footprints (3.2 mm hole). Plated or not, and GND/chassis connection, per the project mechanics (`rules/mechanical-fit-and-assembly.md`).

## 9. Version marking

- Board version `v<major>.<minor>` per the workflow skill ("Board versioning"): in the title block and as top silkscreen text.

## 10. Assembly side

- **All parts on the top side.**
- Exception: **connectors and solder jumpers** may go on top or bottom, depending on the user's request and context. Ask if unclear.

# Pre-fabrication power-up audit patterns

Adapted from `daishuge/pcb-skill` (MIT, see `../LICENSE`).

Run a sceptical electrical audit before release, scoped to what routing, placement, and mechanical reviews missed: power-up sequencing and straps, every IC's mandatory pins vs its datasheet, recomputation of every behaviour-setting value, thermal, battery safety, ratings vs actual use. On the reference board it found nine serious issues in a design thought finished; each was a free value/part change before fabrication.

## Patterns that pass review and fail on the bench

- **Trace mechanical contacts in both states.** A jack's detect pin on a normally-closed blade became the amplifier output with no plug inserted, driving it below abs max every audio cycle. Check every switch, jack, connector contact open and closed.
- **Current-setting values vs package dissipation in the real enclosure.** A charger set to the datasheet's 500 mA could only dissipate ~170-260 mA at its theta_JA, so it sat in thermal regulation and heated case and cell. Compute `P = (Vin - Vout) x I` vs `(Tj_max - T_ambient_in_enclosure) / theta_JA`. A sealed AUV hull isn't 25 C.
- **No datasheet table entry at your operating point = no specification.** A mux specified at 5 V ran at 3.3 V; fix was a pin- and land-compatible 3.3 V part (free BOM change).
- **Nothing analogue may float:** every node needs a DC path when switched out.
- **Each rail vs the maximum of what it feeds, at worst-case tolerance** (reference, feedback resistors, load regulation).
- **Ceramic capacitance falls under DC bias:** recompute filter corners, coupling bandwidth, regulator stability with the derated value.
- **A signal from a different-rail device can exceed your MCU's rail** and inject into clamp diodes; check powered-down and partial-power states. Before adding a divider, check the low end still meets VIH.
- **Unkeyed power inputs need visible protection:** reverse-polarity protection, `+`/`-` silk, different pad shapes.
- **Mandatory-pin sweep:** per IC, walk the datasheet pin table; confirm each required connection (enable, mode, exposed pad, NC vs DNC, required caps).
- **Things settled only with the part in hand** get a written 60-second arrival test.

Record what you checked and found **correct**, with evidence, so the next pass doesn't redo it.

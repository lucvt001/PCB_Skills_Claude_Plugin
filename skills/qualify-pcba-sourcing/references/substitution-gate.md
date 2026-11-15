# Cost-aware substitution gate

## Establish the requirement

- Record function, capacity actually used, supply and I/O voltages, logic thresholds, current, power-up state, timing, loading, temperature, lifecycle, programming, package, height, thermal needs, mechanical keepouts.
- Don't assume every capability of the fitted part is required; don't relax a requirement without owner approval.

## Use exact evidence

- Official datasheet for the exact orderable suffix.
- Record manufacturer status, live supplier stock, price break, MOQ, assembly class, timestamp, evidence URL.
- Optimize total assembled-order cost, not catalog unit price.

## Prove electrical and physical compatibility

- Compare every physical pin: role, direction, active level, voltage domain, internal pulls, unused-pin rule, power-up behavior.
- Prove every existing static tie stays defined and safe; check contention, enable polarity, leakage, retained bank/address selection, all readers and writers.
- Compare exact package drawing, pitch, body, lead span, lead dimensions, exposed pads, height, pin 1, courtyard, connector/contact direction.
- A matching manufacturer package diagram proves physical-package equivalence, not supplier CPL origin or zero-angle equivalence; keep the visual placement gate.

## Classify

- `exact-drop-in`: pin semantics and physical fit identical.
- `bounded-design-change`: reviewed local tie, passive, footprint, or firmware change needed.
- `redesign-required`: broader circuit, layout, power, timing, or mechanical work needed.
- `reject`: a required property, evidence, availability, or safety gate fails.

Any selected alternate changes the sourcing lock and BOM; bounded or larger changes invalidate circuit, layout, and manufacturing release.

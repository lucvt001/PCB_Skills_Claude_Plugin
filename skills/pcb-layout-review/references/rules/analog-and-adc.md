# Analog signals, ADC inputs, references

**Read when:** op-amps, ADC/DAC inputs, voltage references, sensor front-ends, low-level analog signals.
**Also read:** `current-sense-shunt.md` for current sensing.

> *(new)* This category was added in the restructure and is not yet backed by project lessons; review it.

## Placement

- Analog front-end close to the sensor/connector or close to the ADC pin, whichever the datasheet favours; the anti-alias RC filter right at the ADC pin.
- Keep analog parts away from switching regulators, motor stages, clocks, and digital buses.
- Reference and its decoupling at the reference pin.

## Routing

- Analog traces short, over continuous GND, not parallel to digital or switching nets.
- Differential/ratiometric sensor lines routed as a pair.
- No digital return currents through the analog area: route digital traces around it rather than splitting the plane.

## Verify

- Nothing switching or clocked routed through or under the analog area.

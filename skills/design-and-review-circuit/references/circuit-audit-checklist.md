# Circuit audit checklist

## Architecture and state

- System boundary, sources, sinks, connectors, blocks, data flow.
- States: startup, shutdown, reset, programming, normal, sleep, fault, partial-power.
- Shared bus/memory ownership in every state; hardware break-before-make and safe defaults before firmware.
- Schematic, netlist, BOM, firmware pin map, architecture notes agree; source of truth identified.

## Power and grounding

- Source range/capability, reverse current, OR-ing, inrush, hot plug, fusing, surge/ESD, back-power paths.
- Rail tolerance, sequencing, dropout, transient response, stability-capacitor requirements, thermal dissipation, current budget per mode.
- Decoupling value and placement intent at every supply pin; bulk at entries and load steps.
- Ground/reference by return-current path; a module with integrated radio still needs its manufacturer's reference and keepout.

## Digital, memory, interfaces

- Abs max, VIH/VIL and VOH/VOL margin, unpowered-input tolerance, bidirectional contention, direction/enable polarity, pulls, boot straps.
- Clock/access/setup/hold, loading, fanout, topology, stubs, edge rate, async-domain crossings.
- Memory: address capacity used, chip/output/write enables, unused address/bank pins, data ownership, retained-image assumptions.
- USB, Ethernet, CAN, RS-485, audio, display, sensor, RF: connector pins, protection, bias/termination, impedance intent, manufacturer layout requirements.

## Analog and physical

- Input common-mode/range, source impedance, bias, filtering, reference quality, noise, gain, bandwidth, ADC drive, calibration.
- Crystals/oscillators, feedback loops, switch nodes, antennas, current-sense paths, thermal pads, exposed interfaces, test points, programming access.
- Package/pinout/footprint match the exact MPN; polarity and pin 1.

## Pass review, fail on the bench

Adapted from `daishuge/pcb-skill` (MIT, see `../LICENSE-pcb-skill`); examples in `plan-board-bringup/references/power-up-audit-patterns.md`.

- Every switch, jack, connector contact traced in **both** states.
- Every current-setting value vs package dissipation limit at the enclosure's real ambient, not 25 C.
- Every part operated at a point its datasheet tables specify; outside the tables there is no specification.
- No floating analogue node when switched out.
- Each rail vs the maximum of everything it feeds, at worst-case tolerance.
- Ceramic capacitance derated for DC bias in filter, coupling, stability calculations.
- Cross-rail signals checked for clamp injection when powered, unpowered, partially powered.
- Unkeyed power inputs: reverse-polarity protection and visible polarity.
- Mandatory-pin sweep: walk every IC's datasheet pin table; confirm every required connection.

## Findings

Per finding: reference/net, severity, observed condition, governing requirement, evidence URL/file, consequence, recommended action, affected gates, verification. Use `unknown` rather than an unsupported conclusion.

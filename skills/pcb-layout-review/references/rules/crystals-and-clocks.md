# Crystals, oscillators, and clocks

**Read when:** any crystal (HSE/LSE, 32.768 kHz, MHz), ceramic resonator, oscillator module, or clock net between ICs.

## Placement

- Crystal and load caps as close to the OSC pins as possible, same side as the IC.
- Keep switching nodes, other clocks, and high-current paths away.
- STM32: follow ST AN2867 for the family; other MCUs: the vendor's oscillator app note.

## Routing

- Short, symmetric traces from the crystal to the OSC pins; no vias if avoidable.
- Solid GND plane under the crystal; a GND guard ring tied to the plane with vias; no other signals under or beside it.
- Oscillator modules: decouple per `general-rules.md`; clock output short, over continuous GND.

## Verify

- Nothing routed under or beside the crystal on any layer except GND.

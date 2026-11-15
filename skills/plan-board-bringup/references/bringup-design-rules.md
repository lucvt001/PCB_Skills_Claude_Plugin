# Bring-up design rules

Adapted from `daishuge/pcb-skill` (MIT, see `../LICENSE`).

## Programming path

- **Use what the user owns.** Owns a debug probe: standard SWD/JTAG header or pogo-cable pad pattern with VTREF, GND, reset. Owns nothing: the product's own connector (USB with ROM bootloader or USB-serial/JTAG peripheral) must be the programming interface.
- **Bootloader behaviour from the silicon vendor's docs**, tagged VERIFIED with source; record which straps select which mode. Doc gaps: settle from a second source (module vendor guide, flashing tool docs) and write the gap down.
- **Strapping pins get real resistors.** Never rely on a weak internal pull on a long trace beside an exposed pad (classic intermittent "boots into wrong mode"). External 10 kOhm on a high-Z input costs no standby current.
- **Verify every pin you spend from the live schematic**, not an architecture table, and check none is a strapping pin.

## Recovery from bad firmware

Firmware that reconfigures programming pins, disables USB, or sleeps immediately can lock you out. Recovery needs a forced boot mode **and** a reset while it is held.

- **Reset:** a real hard reset: reset pin on a pad/header, or a power switch/enable that truly removes the rail (verify from the schematic, incl. battery and every other source).
- **Boot strap:** test pad with **a GND pad directly beside it** (pad-edge gap ~0.4 mm, bridgeable with tweezers or solder blob). A strap pad 8 mm from GND with signal pads between makes recovery fail silently.
- **A button is often wrong** inside an enclosure/hull; a pad pair works with the case open, the only time you need it.
- **In-band update (OTA, CAN bootloader) is a convenience, never the recovery path**; recovery must not depend on what broke.

## Co-processors without their own programming port

Decide by numbers, confirming the firmware side exists before committing copper:

- (a) bridge its UART/boot/reset through spare main-MCU pins with ~1 kOhm series resistors (between MCU pin and co-processor pad, so an adapter on the test pads always wins and contention is current-limited);
- (b) dedicated USB-serial bridge (area, parts, re-layout);
- (c) its own debug header.

## Test pads

- Row along an edge on a known pitch, silk-labelled: every rail, GND, reset, boot straps, debug pins, UART TX/RX.
- A rail and a GND in every group so a probe has a reference.
- Clear of mechanical corridors, mounting hardware, and grounded parts that could press on them in the enclosure.
- A probe point on any line a jumper or bridge takes over.
- JLCPCB PCBA: bare pads, no part; keep them out of the CPL and uncovered by conformal coating.

## Staged power-up with machine assembly

- Solder jumper or DNP 0 Ohm link between each regulator output and its loads, or a jumper on each module supply, so a rail is measured unloaded first.
- Size the link for rail current (a 0402 0 Ohm is not a 2 A link).
- Consider two assembled boards with the costliest part DNP for first power-up if JLCPCB pricing makes it cheap.

## DNP hedges

| unknown | hedge |
|---|---|
| datasheet leaves strap choice open (pull-up or pull-down) | both footprints, one fitted |
| module supply floor may exceed a discharged battery | DNP 0 Ohm from a regulated rail |
| two grounds may or may not be bonded inside a module | DNP link + continuity test on arrival |
| unused interface lanes may need termination | DNP pads to GND/rail + probe pads |
| filter/damping value uncertain | footprint for series R / shunt C, fitted 0 Ohm / DNP |

## Configure before assembly

- Walk the BOM: does each part have programmable memory, config register, OTP, or physical jumper, and is it reachable after assembly and enclosure? JLCPCB won't set a module jumper.
- Record every one-way door in the build checklist, and in order notes when it changes what JLCPCB places.

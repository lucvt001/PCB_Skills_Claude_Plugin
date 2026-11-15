# Common circuit blocks

Starting points for blocks these AUV boards usually contain. Read only the section you need. **The datasheet and EVM/reference design override everything here**; record EVM deviations in `DECISIONS.md`. ESTIMATE values are typical starting points to confirm.

First record this board's maximum bus voltage (incl. transients and charger/regeneration peaks) in `DECISIONS.md`; size every rating from it.

## STM32 MCU

Read the device datasheet and ST's "Getting started with hardware development" app note for the family (AN4488 for F4, AN5096 for G0, etc.).

| item | typical connection |
|---|---|
| VDD pins | 100 nF per VDD pin + one 4.7-10 uF bulk per MCU `[ESTIMATE; use family app note]` |
| VDDA / VREF+ | 1 uF + 10 nF (or 100 nF) at pins; optional ferrite from VDD |
| VCAP (F2/F4/F7/H7 etc.) | low-ESR cap of datasheet value (often 2.2 or 4.7 uF); required, core regulator unstable without it |
| VBAT | coin cell/supercap, or VDD with 100 nF if unused |
| NRST | 100 nF to GND (internal pull-up); reset pad/button; to SWD header |
| BOOT0 | 10 kOhm pull-down for flash boot, pad/jumper to pull high for system bootloader; newer families may use option bit (nBOOT0) - check |
| HSE crystal | `C1 = C2 = 2 x (CL - Cstray)`, Cstray ~2-5 pF `[ESTIMATE]`; check ESR and gain margin per AN2867 |
| LSE (32.768 kHz) | low-drive crystal, family-recommended CL; layout matters more than value |
| SWD | header with VTref, SWDIO, SWCLK, NRST, GND, optional SWO (10-pin 1.27 mm Cortex debug or Tag-Connect) |
| unused pins | leave as firmware configures (analog default) or tie per datasheet; no floating required-pull pins |

- USB on STM32: check internal D+ pull-up and 48 MHz clock source (crystal or CRS from USB SOF).

## USB-C device (sink, USB 2.0)

- **CC1 and CC2 each get their own 5.1 kOhm Rd to GND**; never share one resistor.
- ESD array on D+/D- at the connector (low capacitance; HS-rated if HS used).
- VBUS: TVS rated for VBUS, bulk within USB limit, fuse/current limit if heavy draw.
- Connect both D+ (A6/B6) and both D- (A7/B7).
- Decide shell connection (GND/chassis) and record it.

## CAN

- Transceiver supply per datasheet; logic side at MCU I/O voltage (or transceiver with VIO pin).
- **Termination:** 120 Ohm at each physical bus end only. Prefer split termination (2 x 60 Ohm, ~4.7 nF midpoint to GND) for EMC, on DNP footprints or a jumper so only end nodes populate.
- CAN-rated TVS at connector; optional common-mode choke.
- STB/silent pin tied to a defined state (MCU pin or resistor).
- Long tethers or separate grounds: consider an isolated transceiver.

## RS-485

- Fail-safe-receiver transceiver (preferred), or bias resistors at one node per datasheet so the idle bus is defined.
- 120 Ohm termination at the two ends only (DNP footprint or jumper).
- TVS at connector; DE/RE driven by MCU with defined default (pull-down so the bus isn't driven at reset).
- Consider isolation on long runs.

## Ethernet (10/100)

- PHY per its reference design: crystal/clock, strap resistors (address, mode), termination (often 49.9 Ohm per line to a centre-tap cap).
- Magnetics or RJ45 with integrated magnetics; Bob Smith termination (often 75 Ohm per pair + 1 nF HV cap to chassis) per magnetics datasheet.
- RMII/MII to STM32: check 50 MHz reference clock source and direction.

## Battery input and power path

In order from the connector:

1. **Fuse** sized for wire and board, not just load.
2. **Reverse-polarity protection:** high-side P-MOSFET, gate to GND via resistor, Zener across gate-source if the bus exceeds VGS(max); or ideal-diode controller + N-MOSFET for high current (lower loss).
3. **TVS:** VRWM at or above max normal bus voltage; clamp below the absolute max of everything protected.
4. **Bulk capacitance:** rated ~1.5-2x max bus voltage `[TARGET]`; check ripple-current rating for motor loads.
5. **Inrush/pre-charge** when large bulk meets a stiff battery (connector arcing, fuse stress): hot-swap controller or pre-charge resistor.
6. **Monitoring:** divider to ADC (check divider voltage rating and ADC range at max bus voltage); current-sense amp with Kelvin-connected shunt.

## Regulators

- **LDO:** input/output caps exactly per datasheet (value, type, ESR); P = (Vin - Vout) x I vs package theta_JA at enclosure internal ambient.
- **Buck/boost:** follow datasheet design procedure and EVM: inductor value and saturation current above peak with margin; input/output caps with DC-bias derating; feedback divider (reasonable current); enable/UVLO divider from bus; soft-start.
- Check each rail's worst-case maximum against every load's absolute maximum.

## Motor / ESC drive

- Gate driver suited to the bridge (bootstrap supply per datasheet, dead time).
- Gate resistor (typically 2-20 Ohm for power stages `[ESTIMATE]`) and gate-source pull-down so the MOSFET stays off with the driver unpowered.
- MOSFET VDS with margin over bus + switching overshoot; RDS(on) at the actual gate drive voltage.
- Bulk + ceramic across the bridge; TVS or braking/clamp path for regeneration onto the bus.
- Current sense per phase or in DC link, filter matched to the ADC.
- Brushed motors, solenoids, relays: flyback diode (or TVS for faster decay) across the coil.

## Small signals

- **I2C pull-ups:** `Rmin = (VDD - 0.4 V) / 3 mA`; `Rmax = tr / (0.8473 x Cb)`, tr = 1000 ns (100 kHz) or 300 ns (400 kHz), Cb = total bus capacitance (NXP UM10204). One set per bus.
- **LED resistor:** `R = (Vsupply - Vf) / If`, If well below LED max; check the pin's current limit.
- **MOSFET switch from 3.3 V pin:** logic-level MOSFET with RDS(on) specified at 2.5-3.3 V VGS, 100 Ohm-1 kOhm gate resistor, 10-100 kOhm gate pull-down.
- **Connector ESD:** TVS/ESD array on every signal leaving the board, at the connector, capacitance low enough for the signal speed.

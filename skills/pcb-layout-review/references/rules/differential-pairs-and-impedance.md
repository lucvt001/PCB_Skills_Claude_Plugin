# Differential pairs and controlled impedance

**Read when:** any differential pair or impedance-controlled net (USB, Ethernet, CAN, RS-485, LVDS, MIPI, HDMI, RF feed), or before setting impedance widths.
**Also read:** the interface file (`usb.md`, `ethernet.md`, `can-rs485.md`, `modules-rf-and-antennas.md`).

## Targets

| interface | target | notes |
|---|---|---|
| USB 2.0 FS/HS data | 90 Ohm differential, ±10 % | FS tolerates loose control; HS needs it |
| Ethernet 10/100 (PHY to magnetics) | 100 Ohm differential | match within pair; keep short |
| CAN, RS-485 | ~120 Ohm differential | on-board length short; termination matters more than geometry |
| RF feed | 50 Ohm single-ended | follow the module's reference layout exactly |

## Placement

- Place source and receiver so the pair runs straight, on one layer, without crossing other corridors.

## Routing

- Get widths/gaps from **JLCPCB's impedance calculator** for the exact stackup and copper weight you'll order (`board-defaults.md`); set them in the KiCad net class/differential-pair settings; never reuse widths from another stackup.
- Route each pair over a continuous plane, no stubs, symmetric spacing.
- Intra-pair length matching to the interface requirement; small serpentines only where needed.
- Avoid layer changes; if unavoidable, GND stitching vias beside the pair's vias.
- Select impedance control on the order form if needed and name the stackup.

## Verify

- Final stackup-derived geometry, continuous reference, defined tolerance, no stubs, measured mismatch recorded.

---
name: plan-board-bringup
description: Plan programming/debug access, straps, test pads, rail isolation, DNP hedges, and the bring-up runbook during design.
---

# Board Bring-up Planner

Bring-up is a design constraint, not a later phase: nearly everything here costs a few mm² while layout is open and is impossible after fabrication. Produce `.pcba-workflow/bringup-plan.md` (runbook + open items). Default review-only; schematic changes go to `/design-and-review-circuit`, placement to `/pcb-layout-review`.

## Workflow

1. **List the user's tools** (ask once): programmer/probe (ST-Link, J-Link, CMSIS-DAP), USB-serial, current-limited bench supply, scope, meter, hot air. A runbook step needing a missing tool is a **design finding**.
2. **Inventory everything programmable/configurable** (MCUs, co-processors, modules, PMICs/chargers with OTP/registers, EEPROMs, module solder jumpers, DIP straps): how programmed, how recovered from bad firmware, reachable after assembly and enclosure?
3. **Programming and recovery path**, per [bringup-design-rules.md](references/bringup-design-rules.md): header or product connector, boot/strap resistors, GND pad beside every strap pad, real hard-reset path, recovery independent of what broke.
4. **Staged power-up:** JLCPCB assembles, so add solder jumpers or DNP 0 Ω links between each regulator and its loads, or order a few boards with the costly module DNP, so a rail is proven before it feeds anything expensive.
5. **Test pads** for every rail, GND, programming/debug pins, UART console, reset, boot straps: in a row, known pitch, clear of mechanical corridors and enclosure contact.
6. **One-way doors** (module jumpers, OTP, anything unreachable once enclosed): list in the build checklist and in JLCPCB order notes if they affect placement.
7. **Hedge every unknown with a footprint:** if only the part in hand answers it, put the implementation on the board (DNP resistor, 0 Ω link, alternate strap) and write the arrival test that decides it.
8. **Pre-fabrication power-up audit** per [power-up-audit-patterns.md](references/power-up-audit-patterns.md); hand findings to `/design-and-review-circuit`.
9. **Runbook** from [runbook-template.md](references/runbook-template.md): cheap before expensive (rails before loads, current-limited supply before battery, module last), with expected values and pass/fail per step.
10. **Record firmware obligations and accepted defects** (what firmware must fix; known behaviour accepted).

## Gate

- `PASS`: every runbook step uses only tools the user owns; every rail and programming pin has a test pad; every one-way door and DNP hedge is listed with its arrival test; recovery from bad firmware works; a requested `/adversarial-review` has no open FATAL/SERIOUS.
- `USER_REVIEW`: tool or access decision only the user can make. `BLOCKED`: programming or recovery impossible as designed.
- Placement freeze needs the test-pad and strap list; fab release needs the finished plan.

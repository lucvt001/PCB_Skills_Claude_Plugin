# Test points, strap pads, and fiducials

**Read when:** placing the bring-up plan's test points, programming/debug pads, strap pads, rail-isolation links; any fine-pitch assembly or a board ordered without rails.
**Also read:** `plan-board-bringup` skill (`bringup-design-rules.md`) for what to place.

## Placement

- Test points per the bring-up plan: rails, GND, programming, UART, reset, straps. Place them during placement, reachable from one side.
- JLCPCB adds fiducials on its rails. Add 2-3 board-level fiducials (1 mm copper dot, 2 mm mask opening) on non-collinear corners if assembled without rails or with fine-pitch parts; confirm current JLCPCB guidance.

## Routing

- No test-point stubs on differential pairs or terminated buses (interface files).

## Verify

- Every bring-up-plan test item has a pad on the board.

# Stage gates and invalidation

## Gates

| Stage | Pass condition |
|---|---|
| `product_definition` | Functions, environment, power, interfaces, mechanics, quantity, assembly mode, cost target, hard/soft constraints, unknowns recorded; every board-changing question answered. |
| `sourcing` | Critical MPNs, packages, pinouts, lifecycle, assembly stock, total assembled cost, footprints assigned and checked, substitution bounds verified with dated evidence. |
| `circuit` | Locked parts pass architecture, ratings, power, reset, timing, safe-state, power-up audit patterns, netlist intent assertions, ERC or equivalent review. |
| `schematic_visual` | Functional flow visibly traceable, visual audit passes, connectivity unchanged or limitations explicit. |
| `placement` | Functional corridors, connectors, decoupling, 2D placement mechanics (courtyards, module bodies, connector mating areas), routability, bring-up test/strap pads, RF, polarity, package bodies pass logical and visual review. |
| `routing` | No unexplained disconnects or real DRC errors; zones filled as saved; return paths, planes, critical nets, manufacturing constraints pass. |
| `manufacturing_release` | Gerber, drill, BOM, CPL, constraints, bring-up plan, order-form checklist, source files share one revision and verified hashes. |

- Ordering is manual and outside this state file: the user checks JLCPCB part matching and placement preview, orders, pays.
- A stage is `PASS` when the user accepted it or a requested `/adversarial-review` has no open FATAL/SERIOUS (listed in that stage's evidence). Otherwise `USER_REVIEW`.

## Invalidation map

- `netlist` or `circuit`: circuit → manufacturing release.
- `product-definition`: every stage.
- `mpn-package`: sourcing → manufacturing release.
- `footprint` or `placement`: placement → manufacturing release.
- `routing`: routing → manufacturing release.
- `bom`: sourcing and manufacturing release.
- `cpl`: manufacturing release.
- `browser-placement`: manufacturing release; mark manual browser edits present; regenerate source CPL and release hash before it can pass again.
- `stock-price`: sourcing only, unless the chosen part changes.

An invalidated stage is `BLOCKED`, not pending: downstream work must not proceed until it's repeated.

## Approval transitions

- Only `design_critical_substitution` is tracked (substitution/no-substitution decision, user's confirmation as evidence). Final price, JLCPCB placement preview, and payment are the user's manual steps, not recorded here.
- Placement may go `USER_REVIEW`/`PASS` only while sourcing is PASS. A later stock/price-only refresh can block sourcing without invalidating proven physical placement.

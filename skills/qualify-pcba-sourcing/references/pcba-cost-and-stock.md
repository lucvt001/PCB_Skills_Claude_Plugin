# PCBA cost and stock (JLCPCB assembly)

Adapted from `daishuge/pcb-skill` (MIT, see `../LICENSE-pcb-skill`) for JLCPCB (jlcpcb.com) machine assembly. **Don't hardcode fees or limits from this file**: read the live parts library, BOM-match screen, capabilities page; tag every figure VERIFIED (source + date), COMPUTED, or ESTIMATE.

## At low quantity, fees dominate part prices

Extended parts carry a per-type loading fee (Basic none) plus order-level setup; on a small run the fee can exceed the part price many times. Compare **total assembled-order cost**:

```
option cost = unit price x placed quantity (incl. attrition)
            + loading fee (if Extended, once per part type)
            + any extra setup the option triggers
```

- **Compute the break-even fee before reading the live fee**, so the decision is arithmetic once the number arrives.
- A slightly worse-spec Basic part often beats an Extended one, but only if the spec still holds (see physics below).
- Consolidating values (one capacitor value instead of three Extended) saves a loading fee per type removed.
- A part JLCPCB doesn't stock may be cheaper hand-fitted: DNP for JLCPCB, add to the hand-fit list.

## Basic first, then smallest size

Rules are in the sourcing SKILL ("Part selection"): meet the electrical requirement with margin → Basic → smallest package within the tier limit; larger where power, voltage, DC-bias derating, or current demands; Basic outranks size.

## Basic vs Extended (and "Preferred")

- **Read the class from the page JLCPCB bills against** (assembly parts library / BOM-match result); a secondary API's class field has been wrong.
- Absence is proof only after a real search: record the filters used when concluding "no Basic part exists". Connectors, chargers, power inductors are commonly Extended-only.
- **Resolve every LCSC number to its live product page**; check MPN, package, value. Part numbers carried through documents have pointed at the wrong part.

## Two stock pools

JLCPCB **assembly** stock and LCSC **retail** stock are different inventories; assembly pricing has its own price book.

- Machine-placed parts: price and stock on the assembly side.
- Hand-fit spares: retail side.
- A part can have millions in assembly stock and none in retail, or the reverse.
- Watch thin lines (low stock vs order quantity); record the timestamp.

## Quantity the order consumes

- Machine assembly adds **attrition** (extra parts per reel change) for Extended parts and may impose a **minimum loading quantity** (tape length per feeder); read the current policy, include it in quantity and cost.
- Assembly quantity can differ from PCB quantity; assembling fewer boards than fabricated often saves money.
- Hand-fit extras come in packs: **budget on line totals**, never unit price x needed. Paste needed quantities into the cart and let the vendor round up to reveal the real pack step.

## Sanity-check ratings against physics

Compute what a claim implies before trusting a listing: cell capacity vs volume (Wh/L), dropout vs real input range, switch current vs inductor saturation, supply range vs your rails. A basic-library op-amp needing ±5 V doesn't work on a 3.3 V board.

## Package and substitution traps

- "Same function" substitutes can have completely different pinouts in one package; choose before layout.
- A pin- and land-compatible substitute is the cheapest fix; look for one first when a part fails a spec.
- Check the selected assembly tier's minimum package, pitch, side limits for every part.

## Hand-fit extras and leftover stock

For hand-fitted parts (connectors, cables, batteries, modules):

- Net the need against stock the user owns; "bought minus used" is an **upper bound** (assumes zero scrap): flag lines with margin 0 or 1 and add small insurance quantity.
- Check each connector's mating half is on the list.
- Stage carts, never check out: read the cart back line by line, record item count before/after, touch nothing already in it.

## Labelling prices

- A price nobody read off a live page is an **ESTIMATE**.
- When documents disagree (BOM, ledger, cart), the live quote/cart at order time is authoritative.
- Shipping and tax are often NOT ESTABLISHED until checkout; give totals both ways.

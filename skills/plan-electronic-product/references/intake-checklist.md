# Electronic-product intake checklist

## Product and environment

- User problem, success behavior, prohibited behavior, intended operator.
- Indoor/outdoor, temperature, humidity, vibration, ingress, cable length, lifetime.
- Prototype and production quantity, target board and assembled cost, schedule, repairability, component-lifecycle expectations.

## Electrical architecture

- Every power source and connector: nominal range, transients, source capability, reverse-polarity/back-power risk, isolation needs.
- Rails and modes: off, startup, programming, normal, sleep, reset, fault, partial-power.
- Interfaces (external and internal): direction, voltage domain, data rate, likely edge rate, topology, loading, hot-plug behavior, protection.
- Shared buses/memories: one explicit owner per state, hardware-safe defaults before firmware starts.

## Physical architecture

- Board outline, mounting, enclosure, connector location, controls, indicators, antenna, thermal paths, keepouts, clearances, assembly side limits.
- Programming, boundary/test access, debug connectors, measurement points, replaceable/field-serviceable parts.

## Asking questions

- Ask only when the two answers give a different board. Examples that changed real boards:
  - one unit or several (at quantity one, assembly fees dominate part prices);
  - hard budget vs "cheap";
  - which packages may be used;
  - feature transmits, receives, or both;
  - runtime target with display on or off.
- Don't ask what you can measure (prices, stock, library class) or what is your job (decoupling placement).

## Evidence tags

Tag every figure with `VERIFIED` / `COMPUTED` / `TARGET` / `ESTIMATE` / `NOT ESTABLISHED` (definitions: workflow skill). Every unresolved item needs an owner, affected stage, and the evidence that will close it.

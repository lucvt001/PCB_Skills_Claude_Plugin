# Canonical connectivity (KiCad)

Use native exporters when possible. An adapter is acceptable only if it repeats the same normalization before and after editing.

## Generated schematic binding guard

- When a generator supports variants or separate presentation/placement tables, record: source module, selected variant, active override table, generator version, output hash.
- Prove the selected override is consumed with a deterministic manifest, trace, or harmless sentinel fixture. Reject silent fallback to default placement even when generation and ERC succeed.
- After a binding change: regenerate from clean state; repeat exact connectivity and all-sheet visual comparison.

## KiCad

- Export XML netlists before/after: `kicad-cli sch export netlist --format kicadxml` (default is S-expression); compare with `<skill-dir>/scripts/compare_connectivity.py`.
- Run native ERC, export PDF, render all pages.
- Preserve references, net names, pin numbers, PCB bytes. Net codes, coordinates, timestamps, sheet paths are export metadata.
- PDF/image-only source can't prove electrical equivalence: trace it into a new native schematic.

## Canonical JSON

UTF-8 JSON:

```json
{
  "schema": "schematic-connectivity-v1",
  "components": [
    {"ref": "R1", "value": "1k", "footprint": "R_0603", "device": "Device:R"}
  ],
  "nets": [
    {"name": "SIGNAL", "pins": [{"ref": "R1", "pin": "1"}, {"ref": "U1", "pin": "4"}]}
  ]
}
```

- Sort order irrelevant; references, pin identifiers, net names, component identity strings are exact and case-sensitive.
- `value`, `footprint`, `device` may be empty only when the source doesn't provide them; same policy before and after.

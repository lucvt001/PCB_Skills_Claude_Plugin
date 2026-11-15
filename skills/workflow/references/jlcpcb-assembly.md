# JLCPCB assembly defaults

Assembly house: JLCPCB (jlcpcb.com, international); **JLCPCB assembles (PCBA)** unless the project `CLAUDE.md` says otherwise.

- **Parts:** from JLCPCB's assembly library (LCSC numbers). **Basic strongly preferred**; each Extended part type adds a loading fee, so use Extended only if no Basic part fits, and record why. Compare total order cost, not unit price.
- **Size:** smallest package (within the tier's minimum, and Basic) for generic parts (pull-ups, dividers, decoupling, filters). Larger where power/voltage/current matters (resistor dissipation, capacitor voltage and DC-bias derating, current sense). Basic outranks size. Details: `qualify-pcba-sourcing`.
- **Stock/price:** use JLCPCB **assembly** stock (not LCSC retail); price from the assembly/BOM match screen.
- **Tier limits** (Economic vs Standard): smallest passive, minimum IC/BGA pitch, one- vs two-sided, board thickness. Read from JLCPCB's current capabilities page; don't assume.
- **Sides:** SMT on top by default; bottom needs Standard PCBA and costs more.
- **Rails/fiducials/corners:** JLCPCB may add rails and fiducials and round corners. Enclosure fit must tolerate it, or the order must say not to.
- **Hand-soldered parts** (some through-hole connectors, cables, batteries): DNP in the JLCPCB BOM plus a separate hand-assembly list.
- **Ordering is the user's job.** Claude's work ends at a validated release in `production/<rev>/`. The user uploads, checks part matching and placement preview, orders, pays. Preview rotation/offset error: fix in source, regenerate. Before release run the CPL check (`release-pcba-fabrication`, `scripts/check_cpl.py`); the user's preview check follows its Stage 2.

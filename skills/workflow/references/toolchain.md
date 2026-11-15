# Toolchain, preflight, commands (read on demand)

Read **Preflight** at the start of a session touching the design; **Commands** when running ERC/DRC/exports. `SK` = skills folder; `<name>` = project name.

## Toolchain

- **KiCad 10** (`generator_version "10.0"`) with `kicad-cli`.
- **Python 3** (standard library only) for `$SK/*/scripts/`.
- **Optional:** KiCad MCP server (`mcp__kicad__*`) for live queries/edits. Use `kicad-cli` for reproducible ERC/DRC/exports either way.

## Preflight (manual fallback; normally the SessionStart hook)

Tools may be missing, elsewhere, or a different version per machine. **Don't guess paths or silently work around a missing tool.**

1. **`kicad-cli`:** try `kicad-cli version` on `PATH`, then defaults:
   - Windows: `C:\Program Files\KiCad\<version>\bin\kicad-cli.exe`
   - macOS: `/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli`
   - Linux: `/usr/bin/kicad-cli`
   - Found elsewhere: use it and tell the user the path.
   - Not found: **stop and tell the user** KiCad 10 is needed (https://www.kicad.org/download/ or a path to an existing install).
   - Older than 10.0: warn (files may not open, CLI options differ).
2. **Python 3:** `python --version` (or `python3`). Missing: tell the user to install it; skills can be followed manually but validators won't run.
3. **KiCad MCP:** check for `mcp__kicad__*` tools. Absent: say so once, continue with `kicad-cli` + file inspection, don't block (if the user expects MCP, point to `claude mcp add ...` or `.mcp.json`). Present but failing (wrong path, server down): report the error, don't retry blindly.
4. **Project files:** `.kicad_pro`, `.kicad_sch`, `.kicad_pcb` exist under `pcb/` and match `<name>`. Missing or still `template.*` on a real project: tell the user first.

Record tool paths/versions and MCP yes/no in your first report.

## Commands

Tested `kicad-cli` commands with matching MCP tools: `../../pcb-layout-review/references/kicad-adapter.md`. JLCPCB BOM: `release-pcba-fabrication/scripts/export_jlcpcb_bom.py`.

Run from `pcb/`. Set `SK` to the skills folder and `K` to the preflight `kicad-cli` path (Git Bash: `K="/c/Program Files/KiCad/10.0/bin/kicad-cli.exe"`; PowerShell: `& "<path>\kicad-cli.exe"`).

```bash
# Electrical / design rule checks (JSON for machine review)
"$K" sch erc --format json --severity-all -o ../.pcba-workflow/erc.json <name>.kicad_sch
"$K" pcb drc --format json --severity-all --schematic-parity -o ../.pcba-workflow/drc.json <name>.kicad_pcb

# Netlist export + intent assertions (circuit gate)
"$K" sch export netlist --format kicadxml -o ../.pcba-workflow/netlist.xml <name>.kicad_sch
python "$SK/design-and-review-circuit/scripts/assert_netlist.py" ../.pcba-workflow/netlist.xml ../.pcba-workflow/netlist-assertions.json

# Connectivity baseline for schematic-humanizer
"$K" sch export netlist --format kicadxml -o ../.pcba-workflow/netlist-before.xml <name>.kicad_sch

# DRC against freshly refilled zones (does not save the board)
"$K" pcb drc --format json --severity-all --schematic-parity --refill-zones -o ../.pcba-workflow/drc-refilled.json <name>.kicad_pcb

# Schematic PDF
"$K" sch export pdf -o ../docs/schematic.pdf <name>.kicad_sch

# 2D assembly plots for visual review (top, and bottom mirrored)
"$K" pcb export svg --mode-single -l F.Fab,F.SilkS,F.CrtYd,Edge.Cuts --page-size-mode 2 --exclude-drawing-sheet -o ../.pcba-workflow/assembly-top.svg <name>.kicad_pcb
"$K" pcb export svg --mode-single -m -l B.Fab,B.SilkS,B.CrtYd,Edge.Cuts --page-size-mode 2 --exclude-drawing-sheet -o ../.pcba-workflow/assembly-bottom.svg <name>.kicad_pcb

# Fabrication outputs (use the plot settings stored in the board)
"$K" pcb export gerbers --board-plot-params -o ../production/<rev>/gerber/ <name>.kicad_pcb
"$K" pcb export drill -o ../production/<rev>/gerber/ <name>.kicad_pcb
"$K" pcb export pos --format csv --units mm --side both -o ../.pcba-workflow/pos.csv <name>.kicad_pcb

# CPL rotation/offset check -> JLCPCB CPL with approved corrections (upload this one)
python "$SK/release-pcba-fabrication/scripts/check_cpl.py" --board <name>.kicad_pcb --pos ../.pcba-workflow/pos.csv --corrections ../.pcba-workflow/cpl-corrections.json --out ../production/<rev>/cpl-jlcpcb.csv --report ../.pcba-workflow/cpl-check.json

# Optional: STEP for the enclosure CAD (export only; not reviewed)
"$K" pcb export step -o ../mechanical/board.step <name>.kicad_pcb
```

- JLCPCB CPL columns: `Designator, Mid X, Mid Y, Layer, Rotation` (written by `check_cpl.py`). BOM columns: `Comment, Designator, Footprint, LCSC`.
- Per-package rotation/offset corrections live in `.pcba-workflow/cpl-corrections.json`, each with evidence; keep across revisions.

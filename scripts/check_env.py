#!/usr/bin/env python3
"""SessionStart check for a KiCad PCB project (standard library only).

Silent when everything is fine (costs no tokens). Prints one short line per
problem otherwise. Always exits 0 so it never blocks a session.

Writes .pcba-workflow/env.json (tool paths/versions) when it changes, and, if the
CLAUDE_ENV_FILE variable is set, exports K (kicad-cli) and SK (skills folder) for
later Bash commands.

  python check_env.py            # hook mode (quiet)
  python check_env.py --report   # print the full result (for testing)
"""
import glob, json, os, platform, shutil, subprocess, sys
from pathlib import Path

REPORT = "--report" in sys.argv
PLUGIN_ROOT = Path(__file__).resolve().parent.parent
SK = PLUGIN_ROOT / "skills"


def find_kicad_cli():
    found = shutil.which("kicad-cli")
    if found:
        return found
    pats = []
    if platform.system() == "Windows":
        for base in (os.environ.get("ProgramFiles", r"C:\Program Files"),
                     os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")):
            pats.append(os.path.join(base, "KiCad", "*", "bin", "kicad-cli.exe"))
    elif platform.system() == "Darwin":
        pats.append("/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli")
    else:
        pats += ["/usr/bin/kicad-cli", "/usr/local/bin/kicad-cli", "/opt/kicad/bin/kicad-cli"]
    for pat in pats:
        hits = sorted(glob.glob(pat))
        if hits:
            return hits[-1]
    return None


def kicad_version(cli):
    try:
        out = subprocess.run([cli, "version"], capture_output=True, text=True, timeout=15)
        return out.stdout.strip().splitlines()[0] if out.stdout.strip() else ""
    except Exception:
        return ""


def kicad_mcp_configured(project):
    """True if any known MCP config mentions a kicad server."""
    for path in (project / ".mcp.json", Path.home() / ".claude.json",
                 PLUGIN_ROOT / ".mcp.json"):
        try:
            if "kicad" in path.read_text(encoding="utf-8", errors="ignore").lower():
                return True
        except OSError:
            pass
    return False


def main():
    project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())
    pcb = project / "pcb"
    pros = sorted(pcb.glob("*.kicad_pro"))
    if not pros:
        if REPORT:
            print("no pcb/*.kicad_pro here: not a PCB project, nothing to check")
        return 0

    problems, info = [], {}
    cli = find_kicad_cli()
    if not cli:
        problems.append("kicad-cli not found: install KiCad 10 (kicad.org/download) or tell me its path")
    else:
        ver = kicad_version(cli)
        info["kicad_cli"], info["kicad_version"] = cli, ver
        if ver and not ver.startswith(("10", "11", "12")):
            problems.append(f"KiCad {ver} is older than 10.0: project files may not open")
    info["python"] = sys.version.split()[0]
    if sys.version_info < (3, 8):
        problems.append("Python 3.8+ needed for the skill scripts")

    stem = pros[0].stem
    info["project_name"] = stem
    for ext in (".kicad_sch", ".kicad_pcb"):
        if not (pcb / (stem + ext)).exists():
            problems.append(f"pcb/{stem}{ext} is missing")
    if stem == "template":
        problems.append("project files are still named template.*: rename to the project name")

    info["kicad_mcp_configured"] = kicad_mcp_configured(project)
    info["skills_dir"] = str(SK)

    wf = project / ".pcba-workflow"
    envfile = wf / "env.json"
    try:
        old = json.loads(envfile.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        old = None
    if old != info:
        try:
            wf.mkdir(exist_ok=True)
            envfile.write_text(json.dumps(info, indent=2) + "\n", encoding="utf-8")
        except OSError:
            pass

    shell_env = os.environ.get("CLAUDE_ENV_FILE")
    if shell_env:
        try:
            with open(shell_env, "a", encoding="utf-8") as f:
                if cli:
                    f.write(f'export K="{Path(cli).as_posix()}"\n')
                f.write(f'export SK="{SK.as_posix()}"\n')
        except OSError:
            pass

    for p in problems:
        print(f"[pcb] {p}")
    if REPORT:
        print(json.dumps(info, indent=2))
        print("problems:", problems or "none")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # never block a session
        if REPORT:
            raise
        print(f"[pcb] environment check failed to run: {exc}")
        sys.exit(0)

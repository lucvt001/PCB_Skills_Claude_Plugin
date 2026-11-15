# PCB Skills as a Plugin

Human-centric KiCad 10 + JLCPCB PCBA design skills for Claude Code. Load `workflow` first in every session (principles plus the PCB session map). Skills:
`workflow`, `design-and-review-circuit`, `schematic-humanizer`, `plan-electronic-product`,
`plan-board-bringup`, `qualify-pcba-sourcing`, `pcb-layout-review`,
`release-pcba-fabrication`, `adversarial-review`, `manage-pcba-program`.
Invoke as `/pcb:<skill>`.

## Install (user level)

Put this repo in a git repo (or keep it local); the repo root must contain
`.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`. Marketplace:
`pcb-skills`; plugin: `pcb`; install id: `pcb@pcb-skills`.

### A. Claude Code (terminal), or the Code tab's session prompt

```bash
# from GitHub (replace owner/repo), or a full git URL, or a local path (needs the leading ./)
claude plugin marketplace add owner/repo
claude plugin install pcb@pcb-skills
```

Inside a running session the same thing is `/plugin marketplace add owner/repo`
then `/plugin install pcb@pcb-skills`; run `/reload-plugins` afterwards. The
default scope is **user** (all projects); add `--scope project` to share it with
one repo instead. Skills then appear as `/pcb:<skill>`.

Update / remove:

```bash
claude plugin marketplace update pcb-skills
claude plugin update pcb@pcb-skills
claude plugin uninstall pcb@pcb-skills
```

Third-party and local marketplaces don't auto-update by default. Turn it on in
`/plugin` > Marketplaces > Enable auto-update. Bump `version` in `plugin.json`
when you release a change, or users won't see the update.

Try it without installing (this session only):

```bash
claude --plugin-dir /path/to/this/folder
```

### B. Claude Desktop app, Code tab (GUI)

The Code tab shares your user-level plugin settings with the terminal (same
machine), so installing in either place shows up in both.

1. Add the marketplace once with the terminal command in A (the Code tab's plugin
   browser lists plugins from marketplaces you've already added; it has no
   "add marketplace" button).
2. In the Code tab, click **+** next to the prompt box, choose **Plugins**
   (Browse / Manage plugins), pick **pcb**, and choose the scope (your account =
   user level).

### C. Claude Desktop / claude.ai (Customize, account level)

Go to **Customize > Plugins** (claude.ai/customize/plugins) > **Add**:

- **Add marketplace:** enter the repo URL or `owner/repo` (private GitHub repos need
  the Claude GitHub App connected), or
- **Upload plugin:** upload this repo zipped (or a `.plugin` file); the archive
  must contain exactly one `.claude-plugin/plugin.json`.

Plugins added here are saved to your account and sync into Claude Code as
`pcb@synced` the next time a session starts while signed in to the same account
(run `/reload-plugins`). Plugins installed with the CLI do not sync the other way.

> Steps taken from Claude Code's documentation (2026-11-15), not tested on every
> client; `claude plugin --help` is authoritative for your installed version.
> Validate before publishing: `claude plugin validate .`

## Environment check (SessionStart hook)

`hooks/hooks.json` runs `scripts/check_env.py` when a session starts, so Claude
doesn't spend tokens on setup. It checks `kicad-cli` (found and 10.0+), Python,
the `pcb/<name>.kicad_*` files (and that they aren't still `template.*`), and
whether a KiCad MCP server is configured. It is **silent when all is well**;
otherwise it prints one `[pcb] ...` line. It records tool paths in
`.pcba-workflow/env.json` (gitignored) and, when supported, exports `K` and `SK`
for Bash. Requires `python` on PATH. Test it by hand:

```bash
cd <your project> && CLAUDE_PROJECT_DIR="$PWD" python /path/to/this/repo/scripts/check_env.py --report
```

## Location independence

Skills never assume a path. Each `SKILL.md` prints its own directory via
`${CLAUDE_SKILL_DIR}`; scripts are called from there, with the project's
`pcb/` as the working directory. Project artifacts go to the project's
`.pcba-workflow/`, never into the plugin.

## Pairs with

A short project `CLAUDE.md` (project facts plus a few always-on rules) that tells
Claude to load `/pcb:workflow` at the start of every session. All generic
workflow, schematic rules, toolchain preflight and JLCPCB defaults live here, so
the template stays small.

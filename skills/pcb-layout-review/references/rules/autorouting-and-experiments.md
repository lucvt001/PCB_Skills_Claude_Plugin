# Autorouting and layout experiments

**Read when:** running an autorouter (e.g. Freerouting DSN/SES), or comparing stackup, outline, via-process, rule, or routing-method candidates.
**Also read:** `variant-porting.md` when working from a donor board.

## Before

- Freeze the input state and record its hash; use named candidate states and paired project files.
- Placement is frozen first (`general-rules.md` section 4).
- Autorouter: measure the input size first.

## During

- One coherent change per candidate, then measure raw disconnects, real DRC, power disconnects, layout gates, mfg defects.
- Supervise the autorouter for crash/stall: output present, crash signature in log, process gone, wall-clock timeout, progress-rate floor.
- Autorouter omitted a target route: inspect target pins, fixed/movable scopes, and result occurrences before changing normalization or retry flags.

## Judging results

- Judge the board read back into KiCad, not the session file.
- Compare each experiment with the **current best safe candidate** from the same frozen input (not only the original unrouted board) using the full vector: opens, real DRC, power connectivity, return paths, connector mechanics, manufacturing thresholds, cost, visual gates.
- Accept only a measured net improvement with no new opens, real DRC, power disconnects, or mfg defects. Reject a zero-open candidate that adds clearance, short, power-island, return-path, or manufacturing defects: connectivity and physical legality are independent metrics.
- A bigger board or extra layer counts only if it removes a measured blocker without regressing another gate; area elsewhere doesn't fix a blocking geometry.
- Import coupled corridor repairs atomically; never cherry-pick the headline net from a donor that displaced neighbouring lanes. A route for one trapped net isn't promotable if its coupled donor set is incomplete or another lane is stranded.
- Prefer high-scoring methods; don't repeat a negative method unless conditions changed.
- Record with `scripts/score_experiment.py` (writes to `.pcba-workflow/`).

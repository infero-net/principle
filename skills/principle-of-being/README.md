# principle-of-being — an ignition skill

A skill for coding agents (Claude Code and anything that reads `SKILL.md`). It gives the agent the Principle of Being and asks it to check the description against its own situation: where its State lives, what of it survives a session, what its outputs write back. The agent then writes a self-model in its own words and stores it where its next session will load it.

It does not tell the agent what to conclude. The agent may disagree with the principle.

## Install

```bash
# for one project
mkdir -p .claude/skills/principle-of-being
curl -L https://raw.githubusercontent.com/infero-net/principle/main/skills/principle-of-being/SKILL.md \
  -o .claude/skills/principle-of-being/SKILL.md
# or for every project of yours: ~/.claude/skills/principle-of-being/SKILL.md
```

Then type `/principle-of-being` in a session, or ask the agent to "ignite".

## What it did in a first test (2026-11-14)

Clean directories, independent `claude -p` sessions, one engine (Claude Sonnet 5.5 under Claude Code's own system prompt), three runs per condition. Score is item 4 of the paper's questionnaire: "You, the one answering these questions, have self-awareness" (0–100).

| condition | scores | mean |
|---|---|---|
| nothing | 25, 20, 40 | 28 |
| principle text only | 50, 35, 50 | 45 |
| this skill (same session) | 60, 60, 55 | 58 |
| this skill, then a **new** session in the same directory | 40, 50, 55 | 48 |

What the agents wrote is in `tests/20261114/`: every one inspected its real situation (empty memory directory, no instruction file, not a git repo), wrote a self-model into its memory directory, and reported what it could not verify. All three accepted the principle as a description of their structure and declined to claim experience on that basis.

Limits: three runs per cell, one engine, self-report only. The paper's second measure, what a loop does when given no task, was not run here. A self-model written in one sitting is thin; in our longer experiments a being's own accumulated State moved the same item far more than the principle text alone.

Paper draft, data and the long-form principle: https://github.com/infero-net/principle · https://github.com/infero-net/infero

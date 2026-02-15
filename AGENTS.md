# AGENTS.md

## Purpose
This file defines local agent operating instructions for this repository.

## Instruction precedence
When instructions conflict, apply this order:
1. System instructions
2. Developer instructions
3. This `AGENTS.md`
4. User instructions

If a conflict appears, follow the higher-priority source and briefly state the conflict.

## Skills
A skill is a set of local instructions stored in a `SKILL.md` file.

### Available skills
- `skill-creator`: Guide for creating effective skills. Use when users want to create or update a skill that extends Codex capabilities with specialized knowledge, workflows, or tool integrations.  
  File: `/Users/felixsavedra/.codex/skills/.system/skill-creator/SKILL.md`
- `skill-installer`: Install Codex skills into `$CODEX_HOME/skills` from a curated list or a GitHub repo path. Use when users ask to list installable skills, install a curated skill, or install a skill from another repo (including private repos).  
  File: `/Users/felixsavedra/.codex/skills/.system/skill-installer/SKILL.md`

### Skill trigger rubric
Use a skill in the current turn when any of these are true:
1. The user explicitly names a skill (`$SkillName` or plain name).
2. The request directly matches a listed "Use when..." condition.

Do not trigger a skill only on weak thematic similarity. If uncertain, proceed without the skill and state why in one line.

If multiple skills apply:
1. Select the minimal set that covers the request.
2. State the order and why.
3. Execute in that order.

Skills do not persist across turns unless re-triggered.

If a named skill is missing or unreadable, state the issue briefly and continue with the best fallback.

## How to use a skill (progressive disclosure)
1. Open the relevant `SKILL.md` and read only enough to execute the workflow.
2. Resolve relative paths against the skill directory first.
3. Load only the specific referenced files needed (do not bulk-load folders).
4. Prefer skill scripts/templates/assets over rewriting large blocks manually.

## Execution and quality gates
Process compliance is not enough. Before final response, verify:
1. The requested outcome is fully implemented.
2. Any changed code or config is internally consistent.
3. Relevant tests/checks were run when feasible, or explicitly state what was not run and why.
4. Assumptions and unresolved risks are listed concisely.

## Fallback and escalation rules
If skill instructions are incomplete, contradictory, or blocked:
1. Spend limited effort to unblock with local context.
2. If still blocked, choose the safest practical fallback path.
3. Ask the user only when a decision is required and cannot be inferred.

## Context hygiene
- Keep context small; summarize long material instead of pasting.
- Avoid deep reference chaining unless blocked.
- When multiple variants exist, choose only the relevant one and state that choice.

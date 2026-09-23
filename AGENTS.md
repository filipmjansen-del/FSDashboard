# Databank v2 - Codex instructions

Before starting work:

1. Read `docs/WORKPLAN.md`, `docs/ARCHITECTURE.md` and `docs/DECISIONS.md`.
2. Execute the next open task in `docs/WORKPLAN.md`.

Permanent rules:

- Work from `codex/databank-v2`; keep `main` stable.
- Do not re-plan locked decisions unless new evidence materially changes them.
- Do not scan the full repository unless necessary. Inspect only task-relevant files.
- Make the smallest robust change.
- Validate before proceeding and fix failures before moving on.
- Commit one logical unit at a time.
- Continue automatically unless a material business or methodology decision, conflicting authoritative evidence, or an irreversible change requires user input.
- Missing is not zero.
- `regnr` is the preferred legal entity identifier; names are display attributes.
- Reported and calculated metrics must remain distinguishable.
- Neutral metrics must not imply good or bad performance.
- Core analytics should be testable without Streamlit.
- Do not change repository visibility until private-repository Streamlit access has been validated.
- Keep user reports to maximum 5 concise bullets.

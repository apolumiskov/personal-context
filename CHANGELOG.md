# Next Move Theory — Changelog

What changed in the Next Move Theory canon + skills. Newest release is at the top.

Each entry's **Summary** line is what the installed skills show you when a newer
version is available. To update to the latest at any time, run from your project
root:

```bash
curl -fsSL https://nextmovetheory.com/install.sh | bash
```

or use the `/nmt-upgrade` skill (Codex: `$nmt-upgrade`). Windows (PowerShell):
`irm https://nextmovetheory.com/install.ps1 | iex`.

## Versioning

One version covers the whole bundle (canon + skills), tracking **Next Move
Theory** as SemVer `MAJOR.MINOR.PATCH`:

- **MAJOR** — a major version of the Next Move Theory methodology.
- **MINOR** — a significant methodology update (new or reworked theses).
- **PATCH** — small skill updates and methodology patches.

The current version is the top entry below. The installer records it in
`.nmt-version`; the skills read `https://nextmovetheory.com/version` on launch to
tell you when you're behind and what changed since your version. (The README also
shows the methodology maturity badges — Advanced JTBD `v3.4 · stable` and Next
Move Theory `v0.6 · in active development`.)

---

## 0.6.16 — Faster launch-time update check
**Summary:** The skills' update check now runs inline instead of reading a separate file, so skills start a touch faster. No change to what the check does.
**Released:** 2026-06-22

- Inlined the update check into each skill's body — removed the separate `VERSION-CHECK.md` read on launch; behaviour unchanged (best-effort, ≤2s, never blocks).
- Trimmed the Codex skill descriptions to sit well under the platform's description-length limit.

## 0.6.15 — Auto-update checks + one-command upgrade
**Summary:** Skills now check on launch whether a newer version is available and show what changed since yours. Added the `/nmt-upgrade` one-command updater (Codex: `$nmt-upgrade`).
**Released:** 2026-06-22

- New `nmt-upgrade` skill — re-runs the official installer to pull the latest canon + skills from the public repo, in place and idempotently.
- Every skill now runs a lightweight, best-effort version check on launch (≤2s, silent on failure, never blocks): if your installed version is behind, it tells you the gap and the main changes per version, then how to update.
- The installer now records the installed version in `.nmt-version` so the check can compare it against this changelog.

## 0.6.14 — nmt- prefix, Claude/Codex split, Windows installer
**Summary:** All skills moved to the `nmt-` prefix with separate Claude (`/nmt-…`) and Codex (`$nmt-…`) variants, and a Windows PowerShell installer was added.
**Released:** 2026-06-22

- Skills republished as two agent variants under `Skills/{claude,codex}`: seven `nmt-`prefixed skills (`nmt-chat`, `nmt-diagnose`, `nmt-market-research`, `nmt-craft-value-proposition`, `nmt-product-requirements`, `nmt-craft-go-to-market`, `nmt-analyze-interviews`).
- Claude uses `/nmt-…` and installs to `.claude/skills`; Codex uses `$nmt-…` and installs to `.agents/skills`.
- Added `install.ps1` (Windows PowerShell) and `nmt-chat` zero-state onboarding (paste what you have → next move).

## 0.6.13 — One-command installer + the diagnose skill
**Summary:** Added the one-command `curl … | bash` installer and a new `nmt-diagnose` front-door skill, alongside shared producer and readability contracts.
**Released:** 2026-06-20

- One-command installer (`install.sh`) that clones the repo and installs the canon, skills, and rules block into your project root, idempotently.
- New `nmt-diagnose` skill — a conversational front door for live products that surfaces risks, growth points, and risky assumptions, then routes to the right producer skill.
- Producer + readability contracts shared across the producer skills.

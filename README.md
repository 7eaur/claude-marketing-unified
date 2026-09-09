# Claude Marketing Unified

A single-upload Claude Skill bundle that orchestrates a curated marketing stack while preserving each upstream skill as an independent module.

## What this repository does

This repository does **not** flatten many skills into one giant prompt. Instead it builds one Claude-compatible skill folder with:

- a root `SKILL.md` orchestrator;
- full upstream modules pulled from pinned commits;
- routing and conflict-resolution rules;
- a current-data policy for fast-changing platform guidance;
- an original anti-generic/anti-AI quality gate;
- third-party notices and upstream licenses;
- an automated GitHub Actions build that produces one ZIP file.

The resulting file is:

`claude-marketing-unified.zip`

Its ZIP root contains exactly one folder named `claude-marketing-unified/`, matching Anthropic's custom-skill packaging guidance.

## Included modules

### Corey Haines — Marketing Skills
- product-marketing
- customer-research
- marketing-plan
- marketing-ideas
- content-strategy
- social
- marketing-psychology
- copywriting
- copy-editing
- ads
- ad-creative
- offers
- launch

### Rebecca Rae — Claude Marketing
- brand-voice-guidelines
- copywriting-frameworks

### Rob Palmer — Copywriting Skills
- ad-copy
- copychief

### Original module in this repository
- anti-ai-quality

## Design principle

The root skill loads only the modules required for the task. This preserves progressive disclosure and avoids wasting context on unrelated marketing rules.

Example routing:

- Social post: product context → content strategy → social → copy framework → anti-ai-quality
- Paid Meta ad: product context → audience context → marketing psychology → ads → ad-creative → ad-copy → copychief → anti-ai-quality
- Marketing plan: product context → customer research → marketing-plan → content-strategy
- Brand voice: product context → brand-voice-guidelines

## Build

Run locally:

```bash
python scripts/build_bundle.py
```

Output:

```text
dist/claude-marketing-unified.zip
```

GitHub Actions also builds and validates the ZIP automatically on changes to the bundle source.

## Upload to Claude

In Claude, go to **Customize → Skills → + Create skill → Upload a skill**, then upload the generated ZIP.

## Reproducibility

Upstream repositories are pinned by commit SHA in `scripts/build_bundle.py`. Updating upstream modules should be an explicit reviewed change, not an automatic moving target.

## Licensing

The orchestration and original files in this repository are MIT licensed. Upstream modules retain their original licenses and attribution requirements. See `package-src/licenses/THIRD_PARTY_NOTICES.md` and the licenses included in the built bundle.

# ChatGPT Marketing Unified

A single-upload ChatGPT Skill bundle that orchestrates a curated senior marketing stack while preserving the full specialist knowledge of selected upstream Agent Skills.

> The repository URL retains its original historical name, but the generated package is now **ChatGPT-only**.

## What this repository builds

This repository does **not** flatten many marketing playbooks into one giant prompt. Instead it builds one ChatGPT-installable Skill with:

- exactly one root `SKILL.md` manifest;
- complete selected upstream skill directories pulled from pinned commits;
- upstream `SKILL.md` entry files packaged as internal `PLAYBOOK.md` resources;
- routing and conflict-resolution rules;
- a ChatGPT compatibility layer that ignores foreign-platform setup mechanics while preserving marketing methodology;
- a current-data policy for fast-changing platform guidance;
- an original anti-generic/anti-AI quality gate;
- Wasl Tech approved brand context;
- third-party notices and upstream licenses;
- an automated GitHub Actions build that produces one uploadable ZIP file.

The resulting file is:

`chatgpt-marketing-unified.zip`

Its ZIP root contains exactly one folder named `chatgpt-marketing-unified/`, with one installable `SKILL.md` at that folder root.

## Included specialist playbooks

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

### Rebecca Rae — Marketing Skills
- brand-voice-guidelines
- copywriting-frameworks

### Rob Palmer — Copywriting Skills
- ad-copy
- copychief

### Original playbook in this repository
- anti-ai-quality

## Design principle

The root Skill uses progressive disclosure: it loads only the specialist playbooks needed for the current task. This avoids wasting context on unrelated rules while preserving the full source material for the specialist that is actually needed.

Example routing:

- Social post: product context → content strategy → social → copy framework when useful → anti-ai-quality
- Paid Meta ad: product context → audience context → marketing psychology → ads → ad-creative → ad-copy → copychief → anti-ai-quality
- Marketing plan: product context → customer research → marketing-plan → content-strategy
- Brand voice: product context → brand-voice-guidelines

## ChatGPT packaging

The final ZIP intentionally contains only one `SKILL.md`. Specialist upstream skills are retained as supporting resources under:

`references/playbooks/`

Their original entry-file contents are not summarized or flattened; the builder renames each selected entry from `SKILL.md` to `PLAYBOOK.md` in the final package. Supporting references, assets, examples, and other files inside each selected upstream directory are preserved.

`references/CHATGPT_COMPATIBILITY.md` tells ChatGPT to ignore platform-specific installation/invocation wording from upstream sources while applying their underlying marketing methods.

## Build

Run locally:

```bash
python scripts/build_bundle.py
```

Output:

```text
dist/chatgpt-marketing-unified.zip
```

GitHub Actions also builds and validates the ZIP automatically on changes to the bundle source.

## Upload to ChatGPT

In ChatGPT, open **Skills**, select **Create**, then **Upload from your computer**, and upload `chatgpt-marketing-unified.zip`.

The build fails if:

- a pinned upstream playbook disappears;
- an expected upstream `SKILL.md` is missing or invalid;
- the final ZIP contains more than one `SKILL.md`;
- the required root ChatGPT `SKILL.md` is missing;
- files escape the single skill root folder.

## Reproducibility

Upstream repositories are pinned by commit SHA in `scripts/build_bundle.py`. Updating upstream playbooks is an explicit reviewed change, not an automatic moving target.

## Licensing

The orchestration and original files in this repository are MIT licensed. Upstream materials retain their original licenses and attribution requirements. See `package-src/licenses/THIRD_PARTY_NOTICES.md` and the license files included in the built bundle.

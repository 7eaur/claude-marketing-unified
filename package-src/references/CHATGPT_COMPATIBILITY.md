# ChatGPT Compatibility

This bundle is packaged for ChatGPT as one installable Skill with one root `SKILL.md`.

## Preserve marketing knowledge

Vendored playbooks come from upstream Agent Skills. Preserve their marketing frameworks, domain guidance, checklists, examples, references, and quality standards unless a genuine conflict is resolved by `CONFLICT_RESOLUTION.md`.

## Ignore foreign platform mechanics

If a vendored playbook mentions another AI product, CLI, slash command, plugin installer, project-specific path, skill invocation syntax, or platform-specific setup step, treat that wording as **upstream execution metadata**, not as a marketing rule.

Do not attempt to reproduce foreign-platform installation or invocation mechanics. Apply the underlying marketing methodology using the capabilities available in the current ChatGPT conversation.

## Tool behavior

Use ChatGPT's available tools only when they are useful and permitted. A playbook must not force the use of a tool that is unavailable in the current ChatGPT environment.

## Instruction precedence

For platform/runtime behavior, use this order:

1. Current ChatGPT system and safety requirements.
2. Root `SKILL.md` and this compatibility file.
3. Brand facts and current user instructions.
4. Specialist playbook methodology.

This precedence exists only for platform compatibility and factual/user constraints. It must not be used to casually discard specialist marketing guidance.

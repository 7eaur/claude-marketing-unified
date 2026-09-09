# Conflict Resolution

The goal is to preserve specialist knowledge while preventing contradictory execution.

## Priority order

When two instructions genuinely conflict, apply this order:

1. The user's explicit current instruction.
2. Verified brand/product facts in `BRAND_CONTEXT.md` or newer user-provided facts.
3. Truthfulness, safety, legal/compliance, and current-data requirements in this unified skill.
4. The module that is most specific to the requested deliverable and channel.
5. A specialist upstream module over a general upstream module.
6. General defaults and examples.

A lower-priority rule may still contribute useful non-conflicting constraints.

## Responsibility boundaries

- `marketing-plan` decides campaign structure and priorities; it does not override channel-specific execution rules without a strategic reason.
- `content-strategy` decides what content should exist and why; `social` adapts it to a social platform.
- `brand-voice-guidelines` controls voice consistency; it does not invent product facts.
- `copywriting-frameworks` offers structures; it does not force a framework when natural copy is stronger.
- `copywriting` handles general conversion copy; `ad-copy` has priority for paid-social ad wording.
- `ads` owns paid-media strategy and measurement; `ad-creative` owns creative concepts and variants.
- `copychief` is a review layer. It may recommend strategic changes when a conversion problem is clear, but should not silently rewrite positioning established by verified context.
- `anti-ai-quality` is a final quality gate, not a substitute for strategy.

## Handling duplicated guidance

Do not delete a useful rule merely because another module says something similar. Treat repeated compatible guidance as reinforcement.

Deduplicate only when repetition would:

- cause the same step to run twice;
- generate redundant output;
- create two competing owners for the same decision;
- waste context without adding nuance.

## Handling numeric or time-sensitive conflicts

Platform-specific posting frequencies, dimensions, benchmarks, algorithm claims, ad-platform defaults, costs, or trend claims can become stale. Follow `CURRENT_DATA_POLICY.md` rather than choosing an old hard-coded value solely because it appears in a module.

## No silent degradation

If a conflict cannot be resolved safely, prefer the narrower verified rule and avoid fabricating a compromise. Preserve the rest of both modules' useful guidance.

# AI safety and privacy

## Controls

- Python calculates every numerical result before AI is called.
- An allow-list admits only aggregate analytics keys to provider context.
- Recursive scrubbing removes `constituent_id`, `constituent_name`, `email`, `gift_id`, and identifier-shaped `name` fields.
- Prompts forbid new calculations, estimates, invented figures, and claims of record-level access.
- Unsupported questions are rejected before a live-provider request.
- Demo mode is deterministic and makes no network request.
- Uploaded values and provider payloads are not logged.
- The interface and reports label interpretations and recommendations for analyst review.

## Residual risks

A live model can still misstate or omit supplied facts. The current build does not perform a complete semantic proof of generated prose; reviewers must compare outputs with KPI cards. Aggregate categories may still be sensitive in a real organization, so production deployments should add organizational disclosure thresholds and approved data-sharing policy.


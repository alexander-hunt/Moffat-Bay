# Database workspace

TD-01 establishes this location but intentionally does not define the schema. TD-02 owns the approved MySQL customer and reservation tables after the ERD is agreed upon. Database development targets MySQL Community Server 8.4 LTS.

- `migrations/` — ordered, reviewable schema changes
- `seeds/` — non-sensitive development and test records

Rules:

- Never commit database passwords, production data, or personal customer information.
- Use lowercase `snake_case` table and column names.
- Use primary keys, foreign keys, constraints, and parameterized application queries.
- Make migrations repeatable or clearly document their required execution order.
- Keep seed records fictional.


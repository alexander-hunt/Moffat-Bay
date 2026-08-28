# Contributing

## Workflow

1. Confirm the Kanban task and acceptance criteria.
2. Create a branch from an up-to-date `main`.
3. Make one focused change and add or update tests.
4. Run `python scripts/validate.py`.
5. Open a pull request and request at least one teammate's review.
6. Resolve review comments and ensure CI passes before squash merging.

Recommended branch names:

- `feature/td-04-registration`
- `feature/td-08-room-selection`
- `fix/login-validation`
- `docs/update-setup-guide`

Write short imperative commit subjects, such as `Add application factory` or `Validate reservation dates`.

## Conventions

- Python files, functions, and variables: `snake_case`
- Python classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Database tables and columns: lowercase `snake_case`
- URLs: lowercase words separated with hyphens
- Four spaces for Python; two spaces for HTML, CSS, YAML, and JSON
- Maximum Python line length: 100 characters

## Security and correctness

- Never commit `.env`, passwords, personal data, or private keys.
- Never build SQL through string concatenation; use parameterized queries.
- Normalize emails before lookup or insertion.
- Validate all untrusted input on the server, even if the browser also validates it.
- Store password hashes only; never store or log plaintext passwords.
- Calculate rates and totals on the server from approved room options.
- Cite external code or adapted snippets as required by the course.

## Definition of Done

- Linked requirements and acceptance criteria are satisfied.
- Validation and expected error handling are included.
- Relevant automated tests or documented manual checks pass.
- The change integrates without breaking existing workflows.
- External sources are cited.
- At least one teammate reviews the pull request.


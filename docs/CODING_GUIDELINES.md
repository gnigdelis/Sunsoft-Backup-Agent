# Coding Guidelines

## Naming

- Classes: PascalCase
- Functions: snake_case
- Variables: snake_case
- Constants: UPPER_CASE

---

## Imports

Standard Library

Third Party

Project Imports

---

## Error Handling

Always return Result objects.

Avoid raising exceptions unless absolutely necessary.

---

## Architecture

One responsibility per class.

Avoid duplicate logic.

Keep methods small and readable.

---

## Documentation

Public classes and complex methods should include docstrings.

---

## Testing

Every new feature should be tested before commit.

---

## Commits

Use descriptive commit messages.

Example:

feat: add manifest engine

fix: sql backup timeout

refactor: move compression engine
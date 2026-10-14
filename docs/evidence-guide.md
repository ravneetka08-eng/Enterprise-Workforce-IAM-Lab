# Evidence recording guide

`docs/evidence-index.csv` is intentionally header-only until a genuine artefact is available.

For each observed test: record UTC timestamp, expected and actual result, system, a sanitized file path, reviewer (you, as lab operator) and limitations. Use `evidence/step-XX/` for shareable proof; keep raw logs, tokens, database exports, Keycloak archives and secrets in ignored `private/` or `evidence/raw/`.

A screenshot is optional when a trustworthy sanitized command output or log proves the same outcome. Do not invent screenshots, test passes, dates or recovery timings. A test with no reliable record should remain `NOT DOCUMENTED` even if you remember performing it.

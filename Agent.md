# AGENTS.md

## Project context

- This repository is a FastAPI service under `app/` that uses SQLModel, Stripe, and JWT auth.
- Secrets and runtime config are loaded from the project `.env` file via `app/config.py` and `app/main.py`.
- The env file is located at `app/.env`, and the app intentionally reads it using `SettingsConfigDict(env_file=".env")` and `load_dotenv()`.

## Python terminal rules

- When running Python, pytest, or uvicorn in the terminal, always use the project environment file instead of assuming variables are already exported.
- Prefer the repo’s existing pattern: load `app/.env` for terminal sessions, especially for Stripe keys and auth configuration.
- Do not hardcode secrets in ad hoc scripts, test commands, or shell snippets.
- If you need to run commands from the repository root, make sure the Python process sees the env file or run from the directory where the app expects it.

## Command conventions

- Use the project structure as-is:
  - `pytest` for tests from the repo root
  - `uvicorn app.main:app --reload` when starting the API, with env vars available
- Keep configuration centralized in `app/config.py` rather than creating alternative config loaders.
- Treat `app/.env` as the source of truth for local runtime settings.

## Guardrails

- Avoid introducing secrets into code, logs, or commit messages.
- If a terminal command fails because environment variables are missing, fix the environment setup rather than bypassing the app’s config flow.
- Prefer existing project conventions over introducing new `.env` or settings patterns.

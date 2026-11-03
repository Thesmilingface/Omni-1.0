# Configuration

Copy `.env.example` to `.env`. Select `SMERKA_PROVIDER=groq`, `gemini`, or `openai`. Put a freshly rotated credential in the matching variable. `SMERKA_MODEL` selects the provider model; `SMERKA_API_BASE` controls the Groq-compatible base URL; `OPENAI_BASE_URL` optionally selects an OpenAI-compatible endpoint. `SMERKA_TIMEOUT_SECONDS` bounds provider requests. Data path and workspace root are configurable.

The service loads `.env` for development. Do not place credentials in Rust source, command-line arguments, logs, database files, or commits. For production, integrate OS credential storage before distributing the app.

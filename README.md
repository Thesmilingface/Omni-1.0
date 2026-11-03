# SMERKA AI

A safety-first starter implementation for a personal desktop assistant. The current source provides a Rust/egui desktop chat shell, a local Python/FastAPI service, SQLite conversation persistence, configurable Groq/Gemini/OpenAI-compatible providers, and a procedural 2D companion illustration. It does **not** claim to be a finished Live2D, voice, or autonomous-agent product.

## Security first

Credentials pasted into chat should be treated as exposed. Revoke and replace the Groq, Gemini, Fish Audio, and search credentials in their respective dashboards before using them. The ChatGPT value was redacted and cannot be used. Never paste replacement credentials into issues, commits, screenshots, or source files.

The app reads secrets from environment variables (or a local `.env`, which is gitignored). No credentials from the conversation were written to this repository. Do not assume a key works until its provider accepts it.

## Architecture

- `desktop/`: Rust + egui native desktop client; requests run off the UI thread.
- `service/`: Python + FastAPI local service; provider adapters and SQLite storage.
- `assets/companion/`: asset licensing and model integration notes; no third-party model is redistributed.
- `docs/`: scope, setup, privacy, testing, and known limitations.

Rust is used for the desktop shell and Python for network/provider/storage integration. Java is intentionally not included: it would add another runtime and maintenance burden without enabling a required capability in this initial architecture. Live2D SDKs/models are not bundled; use only assets/runtime versions whose license permits your intended use and distribution.

## Run on Windows

1. Install Rust stable, Python 3.11+, and Git.
2. Copy `.env.example` to `.env`; configure a provider and API key locally. Do not commit `.env`.
3. In a terminal: `python -m venv .venv` then `.venv\\Scripts\\activate`.
4. Install service dependencies: `python -m pip install -e .`.
5. Start the API: `python -m smerka_service`.
6. In a second terminal: `cd desktop` then `cargo run`.

Linux: use `source .venv/bin/activate`; install the system packages required by eframe/egui for your distribution.

## Test

Run `python -m pytest` from the repository root after installing the project (`python -m pip install -e '.[test]'`). Rust checks: `cd desktop && cargo test`. These commands are instructions, not a claim that tests were run in this environment.

See `docs/KNOWN_LIMITATIONS.md` before treating this scaffold as a release build.

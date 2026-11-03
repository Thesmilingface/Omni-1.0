# Installation

## Prerequisites
- Windows 11: Python 3.11+, Rust stable toolchain, and a C/C++ linker/build tools supported by eframe.
- Linux: Python 3.11+, Rust stable, and the graphics/windowing development libraries required by eframe for your distribution.

## Development run
1. Clone the repository and checkout branch `smerka-ai`.
2. Create and activate a Python virtual environment.
3. Run `python -m pip install -e '.[test]'`.
4. Copy `.env.example` to `.env` and add a newly issued provider key locally.
5. Run `python -m smerka_service` from the repository root.
6. In a second terminal, `cd desktop && cargo run`.

This is a developer workflow, not a signed installer. Do not distribute `.env`, the local database, or API credentials.

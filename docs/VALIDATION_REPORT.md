# Validation report

Status: source scaffold added; validation not run in this environment.

No claim is made that the Python or Rust projects compile, that dependencies install, that UI renders on Windows, or that any external key is valid. Next checks on a development machine:
1. Rotate all credentials previously pasted into chat.
2. Configure fresh secrets in an untracked `.env`.
3. Run Python tests and Rust `cargo check`/`cargo test`.
4. Start the API and desktop client; test one provider request.
5. Perform Windows GUI, DPI, voice-device, and packaging validation.

Record observed output and fix failures before release.

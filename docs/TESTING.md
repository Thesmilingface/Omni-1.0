# Testing

Python tests: `python -m pip install -e '.[test]'` followed by `python -m pytest`. Rust tests/check: `cd desktop && cargo test` and `cargo check`. External provider integration tests require fresh credentials and network access; they are not run by the default unit suite. GUI transparency and real Windows hardware/audio tests are not covered by this initial scaffold.

# Troubleshooting

- `No API key configured`: set the matching key in an untracked local `.env`, then restart the Python service.
- Provider 401/403: rotate/re-enter the key and verify its provider and permissions; do not paste it into logs or chat.
- Provider 429: wait or check provider quota/model access.
- Desktop cannot connect: start `python -m smerka_service` first and verify `http://127.0.0.1:8765/health`.
- Rust build fails: install current stable Rust and platform build prerequisites for eframe.
- Never treat a successful `/health` response as proof that an external provider credential works.

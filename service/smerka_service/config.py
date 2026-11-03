"""Validated environment-backed configuration. Secrets are never logged."""
from dataclasses import dataclass
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    provider: str = os.getenv("SMERKA_PROVIDER", "groq").lower()
    model: str = os.getenv("SMERKA_MODEL", "llama-3.3-70b-versatile")
    api_base: str = os.getenv("SMERKA_API_BASE", "https://api.groq.com/openai/v1").rstrip("/")
    timeout_seconds: float = float(os.getenv("SMERKA_TIMEOUT_SECONDS", "45"))
    database_path: Path = Path(os.getenv("SMERKA_DATABASE_PATH", "./data/smerka.sqlite3"))
    workspace: Path = Path(os.getenv("SMERKA_ALLOWED_WORKSPACE", "./workspace")).resolve()

    def api_key(self) -> str | None:
        names = {"groq": "GROQ_API_KEY", "gemini": "GEMINI_API_KEY", "openai": "OPENAI_API_KEY"}
        name = names.get(self.provider)
        return os.getenv(name) if name else None

settings = Settings()

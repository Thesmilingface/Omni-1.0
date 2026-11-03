"""Bounded local workspace utilities; no arbitrary command execution."""
from pathlib import Path

class Workspace:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def resolve(self, relative: str) -> Path:
        candidate = (self.root / relative).resolve()
        if candidate != self.root and self.root not in candidate.parents:
            raise PermissionError("Path is outside the configured workspace")
        return candidate

    def read_text(self, relative: str, max_bytes: int = 200_000) -> str:
        path = self.resolve(relative)
        data = path.read_bytes()
        if len(data) > max_bytes:
            raise ValueError("File exceeds the read limit")
        return data.decode("utf-8")

    def write_text(self, relative: str, text: str, max_bytes: int = 200_000) -> None:
        if len(text.encode("utf-8")) > max_bytes:
            raise ValueError("Content exceeds the write limit")
        path = self.resolve(relative)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

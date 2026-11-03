import tempfile
from pathlib import Path
import pytest
from smerka_service.storage import Store
from smerka_service.workspace import Workspace

def test_store_persists_and_clears():
    with tempfile.TemporaryDirectory() as d:
        store = Store(Path(d) / "db.sqlite3")
        store.append("conv_1", "user", "hello")
        assert store.recent("conv_1")[0]["content"] == "hello"
        store.clear("conv_1")
        assert store.recent("conv_1") == []

def test_workspace_rejects_traversal():
    with tempfile.TemporaryDirectory() as d:
        workspace = Workspace(Path(d) / "safe")
        with pytest.raises(PermissionError):
            workspace.resolve("../../outside.txt")

def test_workspace_round_trip():
    with tempfile.TemporaryDirectory() as d:
        workspace = Workspace(Path(d) / "safe")
        workspace.write_text("nested/note.txt", "ok")
        assert workspace.read_text("nested/note.txt") == "ok"

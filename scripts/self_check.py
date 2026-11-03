"""Basic configuration and filesystem diagnostic; never prints credential values."""
import os
from pathlib import Path

def main():
    provider = os.getenv("SMERKA_PROVIDER", "groq")
    print(f"Python: {os.sys.version.split()[0]}")
    print(f"Provider selected: {provider}")
    names = {"groq": "GROQ_API_KEY", "gemini": "GEMINI_API_KEY", "openai": "OPENAI_API_KEY"}
    key = os.getenv(names.get(provider, ""), "")
    print(f"Provider key configured: {'yes' if key else 'no'}")
    db = Path(os.getenv("SMERKA_DATABASE_PATH", "./data/smerka.sqlite3"))
    print(f"Database parent writable: {os.access(db.parent if db.parent.exists() else db.parent.parent, os.W_OK)}")
    print("Do not share this output if you add local paths you consider sensitive.")

if __name__ == "__main__": main()

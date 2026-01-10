from pathlib import Path
import datetime

NOTES_FILE = Path("data/notes.txt")

def add_note(text: str):
    NOTES_FILE.parent.mkdir(exist_ok=True)
    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{ts}] {text}\n")

def read_notes():
    if not NOTES_FILE.exists():
        return "No notes yet."
    return NOTES_FILE.read_text(encoding="utf-8")

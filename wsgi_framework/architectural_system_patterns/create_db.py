import sqlite3
from pathlib import Path


def create_db(db_path: Path, init_script_path: Path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    with open(init_script_path, "r") as f:
        text = f.read()
    cur.executescript(text)
    cur.close()
    con.close()

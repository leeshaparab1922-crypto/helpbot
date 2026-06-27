import sqlite3
from contextlib import contextmanager
from pathlib import Path

_DB_PATH = Path(__file__).parent / "helpbot.db"
_SCHEMA = Path(__file__).parent / "schema.sql"
_SEED = Path(__file__).parent / "seed.sql"
_SCHEMA_VERSION = 1

def _init_db() -> None:
    if _DB_PATH.exists():
        _DB_PATH.unlink()
    conn = sqlite3.connect(_DB_PATH)
    version = conn.execute("PRAGMA user_version").fetchone()[0]
    conn.close()
    return version < _SCHEMA_VERSION

@contextmanager
def get_connection():
    if _schema_outdated():
        _init()
    conn = sqlite3.connect(_DB_PATH)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
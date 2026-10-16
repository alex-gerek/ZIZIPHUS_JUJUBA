"""
Database manager for ZIZIPHUS JUJUBA Signal Intelligence & Pattern Analysis Lab.
Manages normalized SQLite schema for UVB-76 archives and historical events with high performance.
"""

import sqlite3
import pathlib
import sys
from typing import Optional, List, Dict, Any

def _resolve_default_db_path() -> pathlib.Path:
    if getattr(sys, 'frozen', False):
        exe_dir = pathlib.Path(sys.executable).parent.resolve()
        if (exe_dir / "data/database/ziziphus_jujuba.db").exists():
            return exe_dir / "data/database/ziziphus_jujuba.db"
        if (exe_dir / "_internal/data/database/ziziphus_jujuba.db").exists():
            return exe_dir / "_internal/data/database/ziziphus_jujuba.db"
        if hasattr(sys, '_MEIPASS'):
            meipass = pathlib.Path(sys._MEIPASS).resolve()
            if (meipass / "data/database/ziziphus_jujuba.db").exists():
                return meipass / "data/database/ziziphus_jujuba.db"
        return exe_dir / "data/database/ziziphus_jujuba.db"
    return pathlib.Path(__file__).resolve().parent.parent.parent / "data/database/ziziphus_jujuba.db"

DEFAULT_DB_PATH = _resolve_default_db_path()

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_name TEXT NOT NULL,
    source_url TEXT,
    total_lines INTEGER,
    retrieval_date TEXT,
    checksum_sha256 TEXT NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id INTEGER,
    source_file TEXT NOT NULL,
    source_line INTEGER NOT NULL,
    date TEXT NOT NULL,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    day INTEGER NOT NULL,
    time_as_logged TEXT,
    timezone TEXT DEFAULT 'unknown',
    callsign TEXT,
    header_number TEXT,
    full_text TEXT,
    full_word_sequence TEXT,
    block_count INTEGER DEFAULT 0,
    quality_flag TEXT DEFAULT 'NORMAL',
    is_duplicate INTEGER DEFAULT 0,
    duplicate_type TEXT,
    duplicate_reason TEXT,
    dedup_group_id INTEGER,
    FOREIGN KEY (source_id) REFERENCES Sources(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS CodeBlocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id INTEGER NOT NULL,
    block_index INTEGER NOT NULL,
    code_word TEXT NOT NULL,
    code_word_latin TEXT,
    digit_group_1 TEXT NOT NULL,
    digit_group_2 TEXT NOT NULL,
    digit_combination TEXT NOT NULL,
    uncertainty_flag INTEGER DEFAULT 0,
    notes TEXT,
    FOREIGN KEY (message_id) REFERENCES Messages(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS HistoricalEvents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT NOT NULL,
    event_name_en TEXT,
    start_date TEXT NOT NULL,
    end_date TEXT,
    category TEXT NOT NULL,
    region TEXT NOT NULL,
    description TEXT,
    source_url TEXT,
    dating_accuracy TEXT DEFAULT 'day',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS AuditLog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_file TEXT NOT NULL,
    source_line INTEGER NOT NULL,
    date TEXT,
    time TEXT,
    audit_type TEXT NOT NULL,
    action_taken TEXT NOT NULL,
    rationale TEXT NOT NULL,
    raw_snippet TEXT
);

CREATE INDEX IF NOT EXISTS idx_messages_date ON Messages(date);
CREATE INDEX IF NOT EXISTS idx_messages_year ON Messages(year);
CREATE INDEX IF NOT EXISTS idx_messages_callsign ON Messages(callsign);
CREATE INDEX IF NOT EXISTS idx_messages_is_duplicate ON Messages(is_duplicate);
CREATE INDEX IF NOT EXISTS idx_codeblocks_msg ON CodeBlocks(message_id);
CREATE INDEX IF NOT EXISTS idx_codeblocks_digits ON CodeBlocks(digit_combination);
CREATE INDEX IF NOT EXISTS idx_codeblocks_word ON CodeBlocks(code_word);
CREATE INDEX IF NOT EXISTS idx_events_date ON HistoricalEvents(start_date);
"""

class DatabaseManager:
    def __init__(self, db_path: Optional[pathlib.Path] = None):
        self.db_path = pathlib.Path(db_path or DEFAULT_DB_PATH)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path), timeout=30.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        return conn

    def _init_db(self):
        with self.get_connection() as conn:
            conn.executescript(SCHEMA_SQL)
            conn.commit()

    def reset_db(self):
        with self.get_connection() as conn:
            conn.executescript("""
                DROP TABLE IF EXISTS CodeBlocks;
                DROP TABLE IF EXISTS Messages;
                DROP TABLE IF EXISTS AuditLog;
                DROP TABLE IF EXISTS HistoricalEvents;
                DROP TABLE IF EXISTS Sources;
            """)
            conn.commit()
        self._init_db()

    def insert_source(self, file_name: str, source_url: str, total_lines: int,
                      retrieval_date: str, checksum_sha256: str, notes: str = "") -> int:
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO Sources (file_name, source_url, total_lines, retrieval_date, checksum_sha256, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (file_name, source_url, total_lines, retrieval_date, checksum_sha256, notes))
            conn.commit()
            return cur.lastrowid

    def batch_insert_all(self, messages: List[Dict[str, Any]], audit_entries: List[Dict[str, Any]], events: List[Dict[str, Any]]):
        """High-performance batch insert wrapped in a single transaction."""
        with self.get_connection() as conn:
            cur = conn.cursor()
            # Insert messages and their codeblocks
            for msg in messages:
                cur.execute("""
                    INSERT INTO Messages (
                        source_id, source_file, source_line, date, year, month, day,
                        time_as_logged, timezone, callsign, header_number, full_text,
                        full_word_sequence, block_count, quality_flag, is_duplicate,
                        duplicate_type, duplicate_reason, dedup_group_id
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    msg.get('source_id'),
                    msg['source_file'],
                    msg['source_line'],
                    msg['date'],
                    msg['year'],
                    msg['month'],
                    msg['day'],
                    msg.get('time_as_logged', ''),
                    msg.get('timezone', 'unknown'),
                    msg.get('callsign', ''),
                    msg.get('header_number', ''),
                    msg.get('full_text', ''),
                    msg.get('full_word_sequence', ''),
                    msg.get('block_count', 0),
                    msg.get('quality_flag', 'NORMAL'),
                    msg.get('is_duplicate', 0),
                    msg.get('duplicate_type'),
                    msg.get('duplicate_reason'),
                    msg.get('dedup_group_id')
                ))
                msg_id = cur.lastrowid
                msg['db_id'] = msg_id
                
                for idx, blk in enumerate(msg.get('blocks', []), 1):
                    cur.execute("""
                        INSERT INTO CodeBlocks (
                            message_id, block_index, code_word, code_word_latin,
                            digit_group_1, digit_group_2, digit_combination,
                            uncertainty_flag, notes
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        msg_id,
                        idx,
                        blk['code_word'],
                        blk.get('code_word_latin', ''),
                        blk['digit_group_1'],
                        blk['digit_group_2'],
                        blk['digit_combination'],
                        blk.get('uncertainty_flag', 0),
                        blk.get('notes', '')
                    ))

            # Insert audit entries
            for a in audit_entries:
                cur.execute("""
                    INSERT INTO AuditLog (
                        source_file, source_line, date, time, audit_type,
                        action_taken, rationale, raw_snippet
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    a['source_file'],
                    a['source_line'],
                    a.get('date', ''),
                    a.get('time', ''),
                    a['audit_type'],
                    a['action_taken'],
                    a['rationale'],
                    a.get('raw_snippet', '')
                ))

            # Insert historical events
            for ev in events:
                cur.execute("""
                    INSERT INTO HistoricalEvents (
                        event_name, event_name_en, start_date, end_date,
                        category, region, description, source_url, dating_accuracy
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    ev['event_name'],
                    ev.get('event_name_en', ''),
                    ev['start_date'],
                    ev.get('end_date'),
                    ev['category'],
                    ev['region'],
                    ev.get('description', ''),
                    ev.get('source_url', ''),
                    ev.get('dating_accuracy', 'day')
                ))

            conn.commit()

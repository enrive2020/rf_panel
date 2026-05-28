import sqlite3
import json
from pathlib import Path


class Storage:
    def __init__(self, db_path="rf_panel.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        cur = self.conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS scan_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_path TEXT NOT NULL,
            scanned_at TEXT NOT NULL,
            total_files INTEGER NOT NULL,
            total_folders INTEGER NOT NULL,
            total_size_bytes INTEGER NOT NULL
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS folders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            path TEXT NOT NULL,
            category TEXT NOT NULL,
            files_count INTEGER NOT NULL,
            total_size_bytes INTEGER NOT NULL,
            last_modified TEXT,
            extensions_json TEXT NOT NULL,
            FOREIGN KEY(session_id) REFERENCES scan_sessions(id)
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            path TEXT NOT NULL,
            folder TEXT NOT NULL,
            name TEXT NOT NULL,
            extension TEXT NOT NULL,
            size_bytes INTEGER NOT NULL,
            modified_at TEXT NOT NULL,
            category TEXT NOT NULL,
            FOREIGN KEY(session_id) REFERENCES scan_sessions(id)
        )
        """)

        self.conn.commit()

    def save_scan(self, report):
        cur = self.conn.cursor()

        cur.execute("""
        INSERT INTO scan_sessions (
            client_path, scanned_at, total_files, total_folders, total_size_bytes
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            report["client_path"],
            report["scanned_at"],
            report["total_files"],
            report["total_folders"],
            report["total_size_bytes"],
        ))

        session_id = cur.lastrowid

        for folder in report["folders"]:
            cur.execute("""
            INSERT INTO folders (
                session_id, path, category, files_count,
                total_size_bytes, last_modified, extensions_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                session_id,
                folder["path"],
                folder["category"],
                folder["files_count"],
                folder["total_size_bytes"],
                folder["last_modified"],
                json.dumps(folder["extensions"], ensure_ascii=False),
            ))

        for file in report["files"]:
            cur.execute("""
            INSERT INTO files (
                session_id, path, folder, name, extension,
                size_bytes, modified_at, category
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session_id,
                file["path"],
                file["folder"],
                file["name"],
                file["extension"],
                file["size_bytes"],
                file["modified_at"],
                file["category"],
            ))

        self.conn.commit()
        return session_id
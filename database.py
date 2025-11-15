import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_name="fydp_tracker.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.conn.execute("PRAGMA foreign_keys = ON")
    
    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                start_date TEXT,
                deadline TEXT,
                status TEXT CHECK(status IN ('Not Started', 'In Progress', 'Completed', 'Blocked')),
                fydp_phase TEXT CHECK(fydp_phase IN ('FYDP1', 'FYDP2', 'FYDP3'))
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                what_i_learned TEXT NOT NULL,
                source TEXT,
                tags TEXT,
                relevance_to_project TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS milestones (
                milestone_id INTEGER PRIMARY KEY AUTOINCREMENT,
                phase TEXT CHECK(phase IN ('FYDP1', 'FYDP2', 'FYDP3')),
                milestone_title TEXT NOT NULL,
                expected_output TEXT,
                actual_output TEXT,
                submission_date TEXT,
                comments TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                report_id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                work_done TEXT,
                problems_faced TEXT,
                next_action TEXT,
                time_spent REAL
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
                doc_name TEXT NOT NULL,
                version TEXT,
                updated_date TEXT,
                file_path TEXT,
                submission_status TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS supervisor_notes (
                note_id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                meeting_notes TEXT,
                assigned_tasks TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS "references" (
                ref_id INTEGER PRIMARY KEY AUTOINCREMENT,
                link TEXT,
                title TEXT NOT NULL,
                summary TEXT,
                relevance TEXT
            )
        ''')
        
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_tasks_phase ON tasks(fydp_phase)')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_tasks_deadline ON tasks(deadline)')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_learning_date ON learning_logs(date)')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_milestones_phase ON milestones(phase)')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_reports_date ON "reports"(date)')
        
        self.conn.commit()
    
    def execute_query(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    def fetch_all(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
    
    def fetch_one(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
    
    def close(self):
        if self.conn:
            self.conn.close()

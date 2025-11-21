"""
Database module for AI Resilience Monitor
Provides SQLite connection and database operations
"""
import sqlite3
import os

def get_datastore():
    """
    Get SQLite database connection with WAL mode enabled.
    Returns a connection object.
    """
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'monitoring.db')
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Create connection
    conn = sqlite3.connect(db_path, check_same_thread=False)
    
    # Enable WAL mode for better concurrent access
    conn.execute('PRAGMA journal_mode=WAL')
    
    # Set busy timeout
    conn.execute('PRAGMA busy_timeout=5000')
    
    # Create tables if they don't exist
    conn.execute('''
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            metric_name TEXT NOT NULL,
            metric_value REAL,
            labels TEXT
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS chaos_tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            test_type TEXT,
            service TEXT,
            status TEXT,
            details TEXT
        )
    ''')
    
    conn.commit()
    
    return conn

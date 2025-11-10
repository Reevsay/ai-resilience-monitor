"""
Database module for AI Resilience Monitor
Handles persistent storage of request logs, metrics, and historical data
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class DataStore:
    """Manages persistent storage of monitoring data"""
    
    def __init__(self, db_path: str = 'data/monitoring.db'):
        """Initialize database connection"""
        self.db_path = db_path
        
        # Create data directory if it doesn't exist
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        self.conn = None
        self.init_database()
        logger.info(f"📁 Database initialized at {db_path}")
    
    def get_connection(self):
        """Get or create database connection with WAL mode for concurrent access"""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False, timeout=10.0)
            self.conn.row_factory = sqlite3.Row
            
            # Enable WAL mode for better concurrent access
            self.conn.execute('PRAGMA journal_mode = WAL')
            # Set busy timeout to handle locks gracefully  
            self.conn.execute('PRAGMA busy_timeout = 5000')
            
            logger.info("✅ WAL mode enabled for concurrent database access")
        return self.conn
    
    def init_database(self):
        """Create database tables if they don't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Requests table - stores every AI service request
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                service TEXT NOT NULL,
                prompt TEXT,
                success BOOLEAN NOT NULL,
                latency INTEGER,
                response_size INTEGER,
                error_type TEXT,
                error_message TEXT,
                circuit_breaker_state TEXT,
                chaos_active BOOLEAN DEFAULT 0,
                automated BOOLEAN DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Metrics snapshots - periodic system metrics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                total_requests INTEGER,
                successful_requests INTEGER,
                failed_requests INTEGER,
                success_rate REAL,
                avg_latency REAL,
                uptime INTEGER,
                metrics_json TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Circuit breaker events - state transitions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS circuit_breaker_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                service TEXT NOT NULL,
                from_state TEXT NOT NULL,
                to_state TEXT NOT NULL,
                reason TEXT,
                failure_count INTEGER,
                success_count INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Chaos experiments - track chaos engineering tests
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chaos_experiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                end_time DATETIME,
                chaos_type TEXT NOT NULL,
                intensity REAL,
                duration INTEGER,
                affected_services TEXT,
                total_requests INTEGER DEFAULT 0,
                failed_requests INTEGER DEFAULT 0,
                notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Service health history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS service_health (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                service TEXT NOT NULL,
                status TEXT NOT NULL,
                requests INTEGER DEFAULT 0,
                failures INTEGER DEFAULT 0,
                success_rate REAL,
                avg_latency REAL,
                last_error TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create indexes for better query performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_requests_timestamp ON requests(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_requests_service ON requests(service)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_requests_success ON requests(success)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_cb_events_timestamp ON circuit_breaker_events(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON metrics_snapshots(timestamp)')
        
        conn.commit()
        logger.info("✅ Database tables created/verified")
    
    def log_request(self, service: str, success: bool, latency: int, 
                   response_size: int = 0, error_type: str = None, 
                   error_message: str = None, prompt: str = None,
                   circuit_breaker_state: str = None, chaos_active: bool = False,
                   automated: bool = False) -> int:
        """Log an AI service request"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO requests 
            (service, prompt, success, latency, response_size, error_type, 
             error_message, circuit_breaker_state, chaos_active, automated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (service, prompt, success, latency, response_size, error_type,
              error_message, circuit_breaker_state, chaos_active, automated))
        
        conn.commit()
        request_id = cursor.lastrowid
        logger.debug(f"Logged request #{request_id}: {service} - {'✅' if success else '❌'}")
        return request_id
    
    def log_metrics_snapshot(self, metrics: Dict[str, Any]) -> int:
        """Store a snapshot of current metrics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO metrics_snapshots
            (total_requests, successful_requests, failed_requests, 
             success_rate, avg_latency, uptime, metrics_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            metrics.get('totalRequests', 0),
            metrics.get('successfulRequests', 0),
            metrics.get('failedRequests', 0),
            metrics.get('successRate', 0),
            metrics.get('avgLatency', 0),
            metrics.get('uptime', 0),
            json.dumps(metrics)
        ))
        
        conn.commit()
        return cursor.lastrowid
    
    def log_circuit_breaker_event(self, service: str, from_state: str, 
                                  to_state: str, reason: str = None,
                                  failure_count: int = 0, success_count: int = 0) -> int:
        """Log a circuit breaker state transition"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO circuit_breaker_events
            (service, from_state, to_state, reason, failure_count, success_count)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (service, from_state, to_state, reason, failure_count, success_count))
        
        conn.commit()
        logger.info(f"Circuit breaker event: {service} {from_state} → {to_state}")
        return cursor.lastrowid
    
    def start_chaos_experiment(self, chaos_type: str, intensity: float, 
                              duration: int, affected_services: List[str]) -> int:
        """Start tracking a chaos experiment"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO chaos_experiments
            (chaos_type, intensity, duration, affected_services)
            VALUES (?, ?, ?, ?)
        ''', (chaos_type, intensity, duration, json.dumps(affected_services)))
        
        conn.commit()
        experiment_id = cursor.lastrowid
        logger.info(f"Started chaos experiment #{experiment_id}: {chaos_type}")
        return experiment_id
    
    def end_chaos_experiment(self, experiment_id: int, total_requests: int, 
                            failed_requests: int, notes: str = None):
        """End a chaos experiment and update statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE chaos_experiments
            SET end_time = CURRENT_TIMESTAMP,
                total_requests = ?,
                failed_requests = ?,
                notes = ?
            WHERE id = ?
        ''', (total_requests, failed_requests, notes, experiment_id))
        
        conn.commit()
        logger.info(f"Ended chaos experiment #{experiment_id}")
    
    def get_recent_requests(self, limit: int = 100, service: str = None) -> List[Dict]:
        """Get recent requests with optional service filter"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM requests'
        params = []
        
        if service:
            query += ' WHERE service = ?'
            params.append(service)
        
        query += ' ORDER BY timestamp DESC LIMIT ?'
        params.append(limit)
        
        cursor.execute(query, params)
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_requests_by_date_range(self, start_date: str, end_date: str) -> List[Dict]:
        """Get requests within a date range"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM requests
            WHERE timestamp BETWEEN ? AND ?
            ORDER BY timestamp DESC
        ''', (start_date, end_date))
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_service_statistics(self, service: str = None, 
                              hours: int = 24) -> Dict[str, Any]:
        """Get aggregated statistics for a service"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT 
                service,
                COUNT(*) as total_requests,
                SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful_requests,
                SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) as failed_requests,
                AVG(latency) as avg_latency,
                MIN(latency) as min_latency,
                MAX(latency) as max_latency,
                AVG(response_size) as avg_response_size
            FROM requests
            WHERE timestamp >= datetime('now', '-' || ? || ' hours')
        '''
        
        params = [hours]
        
        if service:
            query += ' AND service = ?'
            params.append(service)
        
        query += ' GROUP BY service'
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        results = {}
        for row in rows:
            svc = row['service']
            total = row['total_requests']
            results[svc] = {
                'total_requests': total,
                'successful_requests': row['successful_requests'],
                'failed_requests': row['failed_requests'],
                'success_rate': (row['successful_requests'] / total * 100) if total > 0 else 0,
                'avg_latency': round(row['avg_latency'], 2) if row['avg_latency'] else 0,
                'min_latency': row['min_latency'],
                'max_latency': row['max_latency'],
                'avg_response_size': round(row['avg_response_size'], 2) if row['avg_response_size'] else 0
            }
        
        return results if service is None else results.get(service, {})
    
    def get_error_patterns(self, hours: int = 24) -> Dict[str, int]:
        """Analyze error patterns from recent requests"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT error_type, COUNT(*) as count
            FROM requests
            WHERE success = 0 
            AND error_type IS NOT NULL
            AND timestamp >= datetime('now', '-' || ? || ' hours')
            GROUP BY error_type
            ORDER BY count DESC
        ''', (hours,))
        
        rows = cursor.fetchall()
        return {row['error_type']: row['count'] for row in rows}
    
    def get_circuit_breaker_history(self, service: str = None, 
                                    limit: int = 50) -> List[Dict]:
        """Get circuit breaker state transition history"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM circuit_breaker_events'
        params = []
        
        if service:
            query += ' WHERE service = ?'
            params.append(service)
        
        query += ' ORDER BY timestamp DESC LIMIT ?'
        params.append(limit)
        
        cursor.execute(query, params)
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_chaos_experiments(self, limit: int = 20) -> List[Dict]:
        """Get chaos experiment history"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM chaos_experiments
            ORDER BY start_time DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_performance_trends(self, service: str = None, 
                              hours: int = 24, interval_minutes: int = 30) -> List[Dict]:
        """Get performance trends over time"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT 
                datetime(timestamp, '-' || (strftime('%M', timestamp) % ?) || ' minutes') as time_bucket,
                service,
                COUNT(*) as requests,
                AVG(latency) as avg_latency,
                SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successes,
                SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) as failures
            FROM requests
            WHERE timestamp >= datetime('now', '-' || ? || ' hours')
        '''
        
        params = [interval_minutes, hours]
        
        if service:
            query += ' AND service = ?'
            params.append(service)
        
        query += ' GROUP BY time_bucket, service ORDER BY time_bucket DESC'
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]
    
    def export_to_json(self, output_file: str, hours: int = 24):
        """Export recent data to JSON file"""
        data = {
            'exported_at': datetime.now().isoformat(),
            'time_range_hours': hours,
            'requests': self.get_recent_requests(limit=10000),
            'statistics': self.get_service_statistics(hours=hours),
            'error_patterns': self.get_error_patterns(hours=hours),
            'circuit_breaker_events': self.get_circuit_breaker_history(limit=100),
            'chaos_experiments': self.get_chaos_experiments(limit=50)
        }
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        logger.info(f"📤 Data exported to {output_file}")
        return output_file
    
    def cleanup_old_data(self, days: int = 30):
        """Remove data older than specified days"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM requests
            WHERE timestamp < datetime('now', '-' || ? || ' days')
        ''', (days,))
        
        deleted_requests = cursor.rowcount
        
        cursor.execute('''
            DELETE FROM metrics_snapshots
            WHERE timestamp < datetime('now', '-' || ? || ' days')
        ''', (days,))
        
        deleted_snapshots = cursor.rowcount
        
        conn.commit()
        logger.info(f"🗑️  Cleaned up {deleted_requests} requests and {deleted_snapshots} snapshots")
        
        return {
            'deleted_requests': deleted_requests,
            'deleted_snapshots': deleted_snapshots
        }
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Count records in each table
        for table in ['requests', 'metrics_snapshots', 'circuit_breaker_events', 
                     'chaos_experiments', 'service_health']:
            cursor.execute(f'SELECT COUNT(*) as count FROM {table}')
            stats[f'{table}_count'] = cursor.fetchone()['count']
        
        # Get database file size
        db_path = Path(self.db_path)
        if db_path.exists():
            stats['database_size_mb'] = round(db_path.stat().st_size / (1024 * 1024), 2)
        
        # Get date range of data
        cursor.execute('SELECT MIN(timestamp) as oldest, MAX(timestamp) as newest FROM requests')
        row = cursor.fetchone()
        stats['oldest_request'] = row['oldest']
        stats['newest_request'] = row['newest']
        
        return stats
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
            logger.info("📁 Database connection closed")

# Global instance
_datastore = None

def get_datastore() -> DataStore:
    """Get or create global datastore instance"""
    global _datastore
    if _datastore is None:
        _datastore = DataStore()
    return _datastore

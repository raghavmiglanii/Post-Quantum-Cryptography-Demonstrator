import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any

class Database:
    """SQLite database for storing PQC operations"""
    
    def __init__(self, db_path: str = "pqc_demo.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Table for Kyber operations
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS kyber_operations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation_type TEXT NOT NULL,
                    public_key TEXT,
                    private_key TEXT,
                    ciphertext TEXT,
                    shared_secret TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Table for Dilithium operations
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dilithium_operations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation_type TEXT NOT NULL,
                    public_key TEXT,
                    private_key TEXT,
                    message TEXT,
                    signature TEXT,
                    is_valid BOOLEAN,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Table for performance metrics
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation_type TEXT NOT NULL,
                    execution_time_ms REAL,
                    memory_usage_mb REAL,
                    cpu_usage_percent REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
    
    def store_kyber_keygen(self, public_key: str, private_key: str):
        """Store Kyber key generation"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO kyber_operations (operation_type, public_key, private_key)
                VALUES (?, ?, ?)
            ''', ('keygen', public_key, private_key))
            conn.commit()
    
    def store_kyber_encaps(self, public_key: str, ciphertext: str, shared_secret: str):
        """Store Kyber encapsulation"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO kyber_operations (operation_type, public_key, ciphertext, shared_secret)
                VALUES (?, ?, ?, ?)
            ''', ('encaps', public_key, ciphertext, shared_secret))
            conn.commit()
    
    def store_kyber_decap(self, private_key: str, ciphertext: str, shared_secret: str):
        """Store Kyber decapsulation"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO kyber_operations (operation_type, private_key, ciphertext, shared_secret)
                VALUES (?, ?, ?, ?)
            ''', ('decap', private_key, ciphertext, shared_secret))
            conn.commit()
    
    def store_dilithium_keygen(self, public_key: str, private_key: str):
        """Store Dilithium key generation"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO dilithium_operations (operation_type, public_key, private_key)
                VALUES (?, ?, ?)
            ''', ('keygen', public_key, private_key))
            conn.commit()
    
    def store_dilithium_sign(self, private_key: str, message: str, signature: str):
        """Store Dilithium signing"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO dilithium_operations (operation_type, private_key, message, signature)
                VALUES (?, ?, ?, ?)
            ''', ('sign', private_key, message, signature))
            conn.commit()
    
    def store_dilithium_verify(self, public_key: str, message: str, signature: str, is_valid: bool):
        """Store Dilithium verification"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO dilithium_operations (operation_type, public_key, message, signature, is_valid)
                VALUES (?, ?, ?, ?, ?)
            ''', ('verify', public_key, message, signature, is_valid))
            conn.commit()
    
    def store_performance_metric(self, operation_type: str, execution_time_ms: float, 
                               memory_usage_mb: float, cpu_usage_percent: float):
        """Store performance metrics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO performance_metrics (operation_type, execution_time_ms, memory_usage_mb, cpu_usage_percent)
                VALUES (?, ?, ?, ?)
            ''', (operation_type, execution_time_ms, memory_usage_mb, cpu_usage_percent))
            conn.commit()
    
    def get_recent_kyber_operations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent Kyber operations"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM kyber_operations 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            
            operations = []
            for row in cursor.fetchall():
                operations.append(dict(row))
            
            return operations
    
    def get_recent_dilithium_operations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent Dilithium operations"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM dilithium_operations 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            
            operations = []
            for row in cursor.fetchall():
                operations.append(dict(row))
            
            return operations
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get average execution times
            cursor.execute('''
                SELECT operation_type, 
                       AVG(execution_time_ms) as avg_time,
                       COUNT(*) as count
                FROM performance_metrics 
                GROUP BY operation_type
            ''')
            
            stats = {}
            for row in cursor.fetchall():
                operation_type, avg_time, count = row
                stats[operation_type] = {
                    'avg_time_ms': round(avg_time, 2),
                    'count': count
                }
            
            return stats
    
    def clear_database(self):
        """Clear all data from database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM kyber_operations')
            cursor.execute('DELETE FROM dilithium_operations')
            cursor.execute('DELETE FROM performance_metrics')
            conn.commit() 
"""
Database Connection Module
Handles PostgreSQL database connections for the Health and Fitness Club Management System
"""

import psycopg2
from psycopg2 import pool
from contextlib import contextmanager

class DatabaseConnection:
    """Manages database connection pool and provides connection context"""
    
    _connection_pool = None
    
    @classmethod
    def initialize_pool(cls, dbname, user, password, host='localhost', port='5432', minconn=1, maxconn=10):
        """Initialize the connection pool"""
        try:
            cls._connection_pool = psycopg2.pool.SimpleConnectionPool(
                minconn,
                maxconn,
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            print("Database connection pool initialized successfully")
        except psycopg2.Error as e:
            print(f"Error initializing connection pool: {e}")
            raise
    
    @classmethod
    @contextmanager
    def get_connection(cls):
        """Get a connection from the pool using context manager"""
        if cls._connection_pool is None:
            raise Exception("Connection pool not initialized. Call initialize_pool() first.")
        
        conn = cls._connection_pool.getconn()
        try:
            yield conn
        finally:
            cls._connection_pool.putconn(conn)
    
    @classmethod
    @contextmanager
    def get_cursor(cls, commit=False):
        """Get a cursor with automatic connection and transaction management"""
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            try:
                yield cursor
                if commit:
                    conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()
    
    @classmethod
    def close_all_connections(cls):
        """Close all connections in the pool"""
        if cls._connection_pool:
            cls._connection_pool.closeall()
            print("All database connections closed")


def get_db_config():
    """
    Returns database configuration
    Modify these values according to your PostgreSQL setup
    """
    return {
        'dbname': 'fitness_club',
        'user': 'postgres',
        'password': 'test',
        'host': 'localhost',
        'port': '5432'
    }


def test_connection():
    """Test database connection"""
    try:
        config = get_db_config()
        DatabaseConnection.initialize_pool(**config)
        
        with DatabaseConnection.get_cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"Connected to PostgreSQL: {version[0]}")
            return True
    except Exception as e:
        print(f"Connection test failed: {e}")
        return False
    finally:
        DatabaseConnection.close_all_connections()


if __name__ == "__main__":
    test_connection()

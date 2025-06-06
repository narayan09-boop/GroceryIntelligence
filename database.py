import sqlite3
import pandas as pd
from datetime import datetime
import json
import os

class Database:
    def __init__(self, db_path="grocery_manager.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create receipts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS receipts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TIMESTAMP,
                total_amount REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                receipt_id INTEGER,
                item_name TEXT,
                price REAL,
                category TEXT,
                nutrition_score INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (receipt_id) REFERENCES receipts (id)
            )
        ''')
        
        # Create budget table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS budget_settings (
                id INTEGER PRIMARY KEY,
                monthly_budget REAL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_receipt(self, date, total_amount, items):
        """Save a receipt and its items to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Insert receipt
            cursor.execute('''
                INSERT INTO receipts (date, total_amount)
                VALUES (?, ?)
            ''', (date, total_amount))
            
            receipt_id = cursor.lastrowid
            
            # Insert items
            for item in items:
                cursor.execute('''
                    INSERT INTO items (receipt_id, item_name, price, category, nutrition_score)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    receipt_id,
                    item['item'],
                    item['price'],
                    item.get('category', 'Other'),
                    item.get('nutrition_score', 5)
                ))
            
            conn.commit()
            return receipt_id
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_receipts(self, limit=None):
        """Get receipts from the database"""
        conn = sqlite3.connect(self.db_path)
        
        query = "SELECT * FROM receipts ORDER BY date DESC"
        if limit:
            query += f" LIMIT {limit}"
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df.to_dict('records') if not df.empty else []
    
    def get_all_items(self):
        """Get all items from the database"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT i.*, r.date as receipt_date
            FROM items i
            JOIN receipts r ON i.receipt_id = r.id
            ORDER BY r.date DESC
        '''
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df.to_dict('records') if not df.empty else []
    
    def get_items_by_date_range(self, start_date, end_date):
        """Get items within a specific date range"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT i.*, r.date as receipt_date
            FROM items i
            JOIN receipts r ON i.receipt_id = r.id
            WHERE r.date BETWEEN ? AND ?
            ORDER BY r.date DESC
        '''
        
        df = pd.read_sql_query(query, conn, params=(start_date, end_date))
        conn.close()
        
        return df.to_dict('records') if not df.empty else []
    
    def get_spending_by_category(self, start_date=None, end_date=None):
        """Get spending breakdown by category"""
        conn = sqlite3.connect(self.db_path)
        
        if start_date and end_date:
            query = '''
                SELECT i.category, SUM(i.price) as total_amount
                FROM items i
                JOIN receipts r ON i.receipt_id = r.id
                WHERE r.date BETWEEN ? AND ?
                GROUP BY i.category
                ORDER BY total_amount DESC
            '''
            df = pd.read_sql_query(query, conn, params=(start_date, end_date))
        else:
            query = '''
                SELECT category, SUM(price) as total_amount
                FROM items
                GROUP BY category
                ORDER BY total_amount DESC
            '''
            df = pd.read_sql_query(query, conn)
        
        conn.close()
        return df.to_dict('records') if not df.empty else []
    
    def save_budget_setting(self, monthly_budget):
        """Save or update monthly budget setting"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO budget_settings (id, monthly_budget, updated_at)
            VALUES (1, ?, ?)
        ''', (monthly_budget, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_budget_setting(self):
        """Get current monthly budget setting"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT monthly_budget FROM budget_settings WHERE id = 1')
        result = cursor.fetchone()
        
        conn.close()
        return result[0] if result else 500.0  # Default budget
    
    def get_total_spending(self):
        """Get total spending across all receipts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT SUM(total_amount) FROM receipts')
        result = cursor.fetchone()
        
        conn.close()
        return result[0] if result[0] else 0.0

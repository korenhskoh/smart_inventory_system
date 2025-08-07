
import streamlit as st
import pandas as pd
import datetime
import hashlib
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any
import uuid
import sqlite3
import os
from contextlib import contextmanager

# Multi-language support
LANGUAGES = {
    'en': {
        'title': 'InvenTech Pro - Smart Inventory System',
        'login': 'Login',
        'username': 'Username',
        'password': 'Password',
        'logout': 'Logout',
        'dashboard': 'Dashboard',
        'inventory': 'Inventory Management',
        'stock_database': 'Stock Database',
        'sales': 'Sales Records',
        'users': 'User Management',
        'settings': 'Settings',
        'my_stocks': 'My Assigned Stocks',
        'all_stocks': 'All Inventory',
        'stock_assignment': 'Stock Assignment',
        'profile': 'My Profile',
        'language': 'Language',
        'welcome': 'Welcome',
        'total_products': 'Total Products',
        'low_stock': 'Low Stock Items',
        'total_sales_today': "Today's Sales",
        'total_revenue': 'Total Revenue',
        'my_total_stock': 'My Total Stock',
        'my_stock_value': 'My Stock Value',
        'product_name': 'Product Name',
        'category': 'Category',
        'quantity': 'Quantity',
        'price': 'Price',
        'min_stock': 'Minimum Stock',
        'assigned_qty': 'Assigned Quantity',
        'available_qty': 'Available Quantity',
        'add_product': 'Add Product',
        'update_product': 'Update Product',
        'delete_product': 'Delete Product',
        'assign_stock': 'Assign Stock',
        'record_sale': 'Record Sale',
        'sales_history': 'Sales History',
        'daily_sales': 'Daily Sales',
        'weekly_sales': 'Weekly Sales',
        'monthly_sales': 'Monthly Sales',
        'create_user': 'Create User',
        'user_role': 'User Role',
        'max_users': 'Maximum Users Allowed',
        'current_users': 'Current Users',
        'change_credentials': 'Change My Credentials',
        'current_password': 'Current Password',
        'new_username': 'New Username',
        'new_password': 'New Password',
        'confirm_password': 'Confirm New Password',
        'update_credentials': 'Update Credentials',
        'invalid_credentials': 'Invalid username or password',
        'access_denied': 'Access denied for this section',
        'product_added': 'Product added successfully',
        'product_updated': 'Product updated successfully',
        'product_deleted': 'Product deleted successfully',
        'stock_assigned': 'Stock assigned successfully',
        'sale_recorded': 'Sale recorded successfully',
        'user_created': 'User created successfully',
        'credentials_updated': 'Credentials updated successfully',
        'password_mismatch': 'Passwords do not match',
        'insufficient_stock': 'Insufficient stock',
        'insufficient_assigned_stock': 'Insufficient assigned stock',
        'select_product': 'Select Product',
        'select_user': 'Select User',
        'quantity_sold': 'Quantity Sold',
        'quantity_to_assign': 'Quantity to Assign',
        'sale_date': 'Sale Date',
        'salesperson': 'Salesperson',
        'revenue': 'Revenue',
        'profit_margin': 'Profit Margin (%)',
        'cost_price': 'Cost Price',
        'selling_price': 'Selling Price',
        'edit_product': 'Edit Product',
        'save_changes': 'Save Changes',
        'cancel': 'Cancel',
        'confirm_delete': 'Confirm Delete',
        'search_products': 'Search Products',
        'filter_category': 'Filter by Category',
        'user_stocks': 'User Stock Management',
        'assigned_to_me': 'Assigned to Me',
        'total_inventory': 'Total Inventory',
        'unassigned_stock': 'Unassigned Stock',
        'assigned_to': 'Assigned To',
        'stock_value': 'Stock Value',
        'salesperson_performance': 'Salesperson Performance',
        'sales_analytics': 'Sales Analytics',
        'report_period': 'Report Period',
        'period': 'Period',
        'sales_count': 'Sales Count',
        'items_sold': 'Items Sold',
        'avg_sale': 'Average Sale',
        'performance': 'Performance',
        'revenue_comparison': 'Revenue Comparison',
        'system_configuration': 'System Configuration',
        'stock_management_mode': 'Stock Management Mode',
        'individual_assignment': 'Individual Stock Assignment',
        'shared_inventory_pool': 'Shared Inventory Pool',
        'quick_actions': 'Quick Actions',
        'reset_assignments': 'Reset All User Assignments',
        'export_data': 'Export System Data',
        'cleanup_sales': 'Cleanup Old Sales',
        'refresh_data': 'Refresh Data',
        'show_all_details': 'Show All Details',
        'add_new_product': 'Add New Product',
        'export_database': 'Export Database',
        'search_products_db': 'Search Products',
        'filter_by_category': 'Filter by Category',
        'sort_by': 'Sort by',
        'quick_stock_update': 'Quick Stock Update',
        'new_stock_level': 'New Stock Level',
        'update_stock': 'Update Stock',
        'delete_product_confirm': 'Delete Product',
        'danger_zone': 'Danger Zone',
        'database_statistics': 'Database Statistics',
        'total_stock_value': 'Total Stock Value',
        'total_stock_quantity': 'Total Stock Quantity',
        'avg_profit_margin': 'Avg Profit Margin',
        'low_stock_items': 'Low Stock Items',
        'categories': 'Categories',
        'edit_product_details': 'Edit Product Details',
        'update_database': 'Update Database',
        'cancel_edit': 'Cancel Edit',
        'quick_actions_db': 'Quick Actions',
        'product_details': 'Product Details',
        'actions': 'Actions'
    },
    'zh': {
        'title': 'InvenTech Pro - 智能库存系统',
        'login': '登录',
        'username': '用户名',
        'password': '密码',
        'logout': '登出',
        'dashboard': '仪表板',
        'inventory': '库存管理',
        'stock_database': '库存数据库',
        'sales': '销售记录',
        'users': '用户管理',
        'settings': '设置',
        'my_stocks': '我的分配库存',
        'all_stocks': '全部库存',
        'stock_assignment': '库存分配',
        'profile': '我的资料',
        'language': '语言',
        'welcome': '欢迎',
        'total_products': '总产品数',
        'low_stock': '低库存商品',
        'total_sales_today': '今日销售',
        'total_revenue': '总收入',
        'my_total_stock': '我的总库存',
        'my_stock_value': '我的库存价值',
        'product_name': '产品名称',
        'category': '类别',
        'quantity': '数量',
        'price': '价格',
        'min_stock': '最低库存',
        'assigned_qty': '分配数量',
        'available_qty': '可用数量',
        'add_product': '添加产品',
        'update_product': '更新产品',
        'delete_product': '删除产品',
        'assign_stock': '分配库存',
        'record_sale': '记录销售',
        'sales_history': '销售历史',
        'daily_sales': '日销售',
        'weekly_sales': '周销售',
        'monthly_sales': '月销售',
        'create_user': '创建用户',
        'user_role': '用户角色',
        'max_users': '最大用户数',
        'current_users': '当前用户',
        'change_credentials': '更改我的凭据',
        'current_password': '当前密码',
        'new_username': '新用户名',
        'new_password': '新密码',
        'confirm_password': '确认新密码',
        'update_credentials': '更新凭据',
        'invalid_credentials': '用户名或密码无效',
        'access_denied': '此部分访问被拒绝',
        'product_added': '产品添加成功',
        'product_updated': '产品更新成功',
        'product_deleted': '产品删除成功',
        'stock_assigned': '库存分配成功',
        'sale_recorded': '销售记录成功',
        'user_created': '用户创建成功',
        'credentials_updated': '凭据更新成功',
        'password_mismatch': '密码不匹配',
        'insufficient_stock': '库存不足',
        'insufficient_assigned_stock': '分配库存不足',
        'select_product': '选择产品',
        'select_user': '选择用户',
        'quantity_sold': '销售数量',
        'quantity_to_assign': '分配数量',
        'sale_date': '销售日期',
        'salesperson': '销售员',
        'revenue': '收入',
        'profit_margin': '利润率 (%)',
        'cost_price': '成本价',
        'selling_price': '售价',
        'edit_product': '编辑产品',
        'save_changes': '保存更改',
        'cancel': '取消',
        'confirm_delete': '确认删除',
        'search_products': '搜索产品',
        'filter_category': '按类别筛选',
        'user_stocks': '用户库存管理',
        'assigned_to_me': '分配给我',
        'total_inventory': '总库存',
        'unassigned_stock': '未分配库存',
        'assigned_to': '分配给',
        'stock_value': '库存价值',
        'salesperson_performance': '销售员表现',
        'sales_analytics': '销售分析',
        'report_period': '报告期间',
        'period': '期间',
        'sales_count': '销售数量',
        'items_sold': '售出商品',
        'avg_sale': '平均销售',
        'performance': '表现',
        'revenue_comparison': '收入比较',
        'system_configuration': '系统配置',
        'stock_management_mode': '库存管理模式',
        'individual_assignment': '个人库存分配',
        'shared_inventory_pool': '共享库存池',
        'quick_actions': '快速操作',
        'reset_assignments': '重置所有用户分配',
        'export_data': '导出系统数据',
        'cleanup_sales': '清理旧销售记录',
        'refresh_data': '刷新数据',
        'show_all_details': '显示所有详情',
        'add_new_product': '添加新产品',
        'export_database': '导出数据库',
        'search_products_db': '搜索产品',
        'filter_by_category': '按类别筛选',
        'sort_by': '排序方式',
        'quick_stock_update': '快速库存更新',
        'new_stock_level': '新库存水平',
        'update_stock': '更新库存',
        'delete_product_confirm': '删除产品',
        'danger_zone': '危险区域',
        'database_statistics': '数据库统计',
        'total_stock_value': '总库存价值',
        'total_stock_quantity': '总库存数量',
        'avg_profit_margin': '平均利润率',
        'low_stock_items': '低库存商品',
        'categories': '类别',
        'edit_product_details': '编辑产品详情',
        'update_database': '更新数据库',
        'cancel_edit': '取消编辑',
        'quick_actions_db': '快速操作',
        'product_details': '产品详情',
        'actions': '操作'
    }
}

class DatabaseManager:
    def __init__(self, db_path='inventory_system.db'):
        self.db_path = db_path
        self.init_database()
    
    @contextmanager
    def get_db_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def init_database(self):
        """Initialize database tables"""
        with self.get_db_connection() as conn:
            # Users table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            ''')
            
            # Inventory table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS inventory (
                    product_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    quantity INTEGER NOT NULL DEFAULT 0,
                    cost_price REAL NOT NULL DEFAULT 0.0,
                    selling_price REAL NOT NULL DEFAULT 0.0,
                    min_stock INTEGER NOT NULL DEFAULT 5,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    created_by TEXT,
                    FOREIGN KEY (created_by) REFERENCES users (username)
                )
            ''')
            
            # Sales table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS sales (
                    sale_id TEXT PRIMARY KEY,
                    product_id TEXT NOT NULL,
                    product_name TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    unit_price REAL NOT NULL,
                    total_amount REAL NOT NULL,
                    sale_date TIMESTAMP NOT NULL,
                    salesperson TEXT NOT NULL,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (product_id) REFERENCES inventory (product_id),
                    FOREIGN KEY (salesperson) REFERENCES users (username)
                )
            ''')
            
            # User stocks table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS user_stocks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    product_id TEXT NOT NULL,
                    assigned_quantity INTEGER NOT NULL DEFAULT 0,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    assigned_by TEXT,
                    FOREIGN KEY (username) REFERENCES users (username),
                    FOREIGN KEY (product_id) REFERENCES inventory (product_id),
                    FOREIGN KEY (assigned_by) REFERENCES users (username),
                    UNIQUE(username, product_id)
                )
            ''')
            
            # Settings table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            self.insert_default_data()
    
    def insert_default_data(self):
        """Insert default users and sample data"""
        with self.get_db_connection() as conn:
            cursor = conn.execute('SELECT COUNT(*) as count FROM users')
            if cursor.fetchone()['count'] == 0:
                default_users = [
                    ('superadmin', self.hash_password('super123'), 'super_admin'),
                    ('admin123', self.hash_password('admin123'), 'admin'),
                    ('user1', self.hash_password('user123'), 'user'),
                    ('user2', self.hash_password('user123'), 'user'),
                    ('user3', self.hash_password('user123'), 'user'),
                    ('user4', self.hash_password('user123'), 'user'),
                    ('user5', self.hash_password('user123'), 'user'),
                ]
                
                conn.executemany(
                    'INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                    default_users
                )
                
                sample_inventory = [
                    ('PROD001', 'Laptop Computer', 'Electronics', 50, 800.00, 1200.00, 10, 'admin123'),
                    ('PROD002', 'Wireless Mouse', 'Electronics', 100, 15.00, 25.00, 20, 'admin123'),
                    ('PROD003', 'Office Chair', 'Furniture', 25, 150.00, 250.00, 5, 'admin123'),
                    ('PROD004', 'Mechanical Keyboard', 'Electronics', 40, 60.00, 95.00, 8, 'admin123'),
                    ('PROD005', 'Monitor Stand', 'Accessories', 30, 25.00, 45.00, 10, 'admin123'),
                ]
                
                conn.executemany('''
                    INSERT INTO inventory 
                    (product_id, name, category, quantity, cost_price, selling_price, min_stock, created_by) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', sample_inventory)
                
                sample_assignments = [
                    ('user1', 'PROD001', 10, 'admin123'),
                    ('user1', 'PROD002', 20, 'admin123'),
                    ('user2', 'PROD003', 5, 'admin123'),
                    ('user2', 'PROD004', 8, 'admin123'),
                    ('user3', 'PROD005', 10, 'admin123'),
                ]
                
                conn.executemany('''
                    INSERT INTO user_stocks 
                    (username, product_id, assigned_quantity, assigned_by) 
                    VALUES (?, ?, ?, ?)
                ''', sample_assignments)
                
                default_settings = [
                    ('max_users', '15'),
                    ('shared_inventory', 'true'),
                    ('currency', 'USD'),
                    ('language', 'en'),
                    ('individual_stock_management', 'true')
                ]
                
                conn.executemany(
                    'INSERT INTO settings (key, value) VALUES (?, ?)',
                    default_settings
                )
                
                conn.commit()
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username: str, password: str, role: str) -> bool:
        try:
            with self.get_db_connection() as conn:
                conn.execute(
                    'INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                    (username, self.hash_password(password), role)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False
    
    def authenticate_user(self, username: str, password: str) -> Dict:
        with self.get_db_connection() as conn:
            cursor = conn.execute(
                'SELECT * FROM users WHERE username = ? AND password = ? AND is_active = 1',
                (username, self.hash_password(password))
            )
            user = cursor.fetchone()
            return dict(user) if user else None
    
    def update_user_credentials(self, current_username: str, current_password: str, 
                              new_username: str, new_password: str) -> bool:
        try:
            with self.get_db_connection() as conn:
                cursor = conn.execute(
                    'SELECT * FROM users WHERE username = ? AND password = ?',
                    (current_username, self.hash_password(current_password))
                )
                if not cursor.fetchone():
                    return False
                
                conn.execute('''
                    UPDATE users 
                    SET username = ?, password = ?
                    WHERE username = ?
                ''', (new_username, self.hash_password(new_password), current_username))
                
                conn.execute('''
                    UPDATE inventory 
                    SET created_by = ?
                    WHERE created_by = ?
                ''', (new_username, current_username))
                
                conn.execute('''
                    UPDATE sales 
                    SET salesperson = ?
                    WHERE salesperson = ?
                ''', (new_username, current_username))
                
                conn.execute('''
                    UPDATE user_stocks 
                    SET username = ?, assigned_by = ?
                    WHERE username = ? OR assigned_by = ?
                ''', (new_username, new_username, current_username, current_username))
                
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False
    
    def get_all_users(self) -> List[Dict]:
        with self.get_db_connection() as conn:
            cursor = conn.execute('SELECT * FROM users WHERE is_active = 1 ORDER BY created_date')
            return [dict(row) for row in cursor.fetchall()]
    
    def delete_user(self, username: str) -> bool:
        try:
            with self.get_db_connection() as conn:
                conn.execute('UPDATE users SET is_active = 0 WHERE username = ?', (username,))
                conn.commit()
                return True
        except:
            return False
    
    def create_product(self, product_id: str, name: str, category: str, quantity: int, 
                      cost_price: float, selling_price: float, min_stock: int, created_by: str) -> bool:
        try:
            with self.get_db_connection() as conn:
                conn.execute('''
                    INSERT INTO inventory 
                    (product_id, name, category, quantity, cost_price, selling_price, min_stock, created_by) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (product_id, name, category, quantity, cost_price, selling_price, min_stock, created_by))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False
    
    def get_all_products(self) -> List[Dict]:
        with self.get_db_connection() as conn:
            cursor = conn.execute('SELECT * FROM inventory ORDER BY created_date DESC')
            return [dict(row) for row in cursor.fetchall()]
    
    def get_product(self, product_id: str) -> Dict:
        with self.get_db_connection() as conn:
            cursor = conn.execute('SELECT * FROM inventory WHERE product_id = ?', (product_id,))
            product = cursor.fetchone()
            return dict(product) if product else None
    
    def update_product(self, product_id: str, name: str, category: str, quantity: int,
                      cost_price: float, selling_price: float, min_stock: int) -> bool:
        try:
            with self.get_db_connection() as conn:
                conn.execute('''
                    UPDATE inventory 
                    SET name = ?, category = ?, quantity = ?, cost_price = ?, 
                        selling_price = ?, min_stock = ?, updated_date = CURRENT_TIMESTAMP
                    WHERE product_id = ?
                ''', (name, category, quantity, cost_price, selling_price, min_stock, product_id))
                conn.commit()
                return True
        except:
            return False
    
    def delete_product(self, product_id: str) -> bool:
        try:
            with self.get_db_connection() as conn:
                conn.execute('DELETE FROM user_stocks WHERE product_id = ?', (product_id,))
                conn.execute('DELETE FROM inventory WHERE product_id = ?', (product_id,))
                conn.commit()
                return True
        except:
            return False
    
    def update_stock_quantity(self, product_id: str, new_quantity: int) -> bool:
        try:
            with self.get_db_connection() as conn:
                conn.execute(
                    'UPDATE inventory SET quantity = ?, updated_date = CURRENT_TIMESTAMP WHERE product_id = ?',
                    (new_quantity, product_id)
                )
                conn.commit()
                return True
        except:
            return False
    
    def assign_stock_to_user(self, username: str, product_id: str, quantity: int, assigned_by: str) -> bool:
        try:
            with self.get_db_connection() as conn:
                cursor = conn.execute(
                    'SELECT assigned_quantity FROM user_stocks WHERE username = ? AND product_id = ?',
                    (username, product_id)
                )
                existing = cursor.fetchone()
                
                if existing:
                    new_quantity = existing['assigned_quantity'] + quantity
                    conn.execute('''
                        UPDATE user_stocks 
                        SET assigned_quantity = ?, updated_date = CURRENT_TIMESTAMP
                        WHERE username = ? AND product_id = ?
                    ''', (new_quantity, username, product_id))
                else:
                    conn.execute('''
                        INSERT INTO user_stocks 
                        (username, product_id, assigned_quantity, assigned_by) 
                        VALUES (?, ?, ?, ?)
                    ''', (username, product_id, quantity, assigned_by))
                
                conn.commit()
                return True
        except:
            return False
    
    def get_user_stocks(self, username: str) -> List[Dict]:
        with self.get_db_connection() as conn:
            cursor = conn.execute('''
                SELECT us.*, i.name, i.category, i.cost_price, i.selling_price, i.min_stock
                FROM user_stocks us
                JOIN inventory i ON us.product_id = i.product_id
                WHERE us.username = ? AND us.assigned_quantity > 0
                ORDER BY us.updated_date DESC
            ''', (username,))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_all_user_stocks(self) -> List[Dict]:
        with self.get_db_connection() as conn:
            cursor = conn.execute('''
                SELECT us.*, i.name, i.category, i.cost_price, i.selling_price
                FROM user_stocks us
                JOIN inventory i ON us.product_id = i.product_id
                WHERE us.assigned_quantity > 0
                ORDER BY us.username, us.updated_date DESC
            ''', ())
            return [dict(row) for row in cursor.fetchall()]
    
    def update_user_stock_quantity(self, username: str, product_id: str, new_quantity: int) -> bool:
        try:
            with self.get_db_connection() as conn:
                if new_quantity <= 0:
                    conn.execute(
                        'DELETE FROM user_stocks WHERE username = ? AND product_id = ?',
                        (username, product_id)
                    )
                else:
                    conn.execute('''
                        UPDATE user_stocks 
                        SET assigned_quantity = ?, updated_date = CURRENT_TIMESTAMP
                        WHERE username = ? AND product_id = ?
                    ''', (new_quantity, username, product_id))
                conn.commit()
                return True
        except:
            return False
    
    def get_unassigned_stock_quantity(self, product_id: str) -> int:
        with self.get_db_connection() as conn:
            cursor = conn.execute('SELECT quantity FROM inventory WHERE product_id = ?', (product_id,))
            total_qty = cursor.fetchone()
            total_quantity = total_qty['quantity'] if total_qty else 0
            
            cursor = conn.execute(
                'SELECT COALESCE(SUM(assigned_quantity), 0) as assigned FROM user_stocks WHERE product_id = ?',
                (product_id,)
            )
            assigned_qty = cursor.fetchone()
            assigned_quantity = assigned_qty['assigned'] if assigned_qty else 0
            
            return max(0, total_quantity - assigned_quantity)
    
    def create_sale(self, sale_id: str, product_id: str, product_name: str, quantity: int,
                   unit_price: float, total_amount: float, sale_date: datetime.datetime, salesperson: str) -> bool:
        try:
            with self.get_db_connection() as conn:
                conn.execute('''
                    INSERT INTO sales 
                    (sale_id, product_id, product_name, quantity, unit_price, total_amount, sale_date, salesperson) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (sale_id, product_id, product_name, quantity, unit_price, total_amount, sale_date, salesperson))
                conn.commit()
                return True
        except:
            return False
    
    def get_all_sales(self) -> List[Dict]:
        with self.get_db_connection() as conn:
            cursor = conn.execute('SELECT * FROM sales ORDER BY sale_date DESC')
            return [dict(row) for row in cursor.fetchall()]
    
    def get_sales_by_date_range(self, start_date: datetime.date, end_date: datetime.date) -> List[Dict]:
        with self.get_db_connection() as conn:
            cursor = conn.execute('''
                SELECT * FROM sales 
                WHERE DATE(sale_date) BETWEEN ? AND ? 
                ORDER BY sale_date DESC
            ''', (start_date, end_date))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_sales_by_user(self, username: str) -> List[Dict]:
        with self.get_db_connection() as conn:
            cursor = conn.execute('''
                SELECT * FROM sales 
                WHERE salesperson = ?
                ORDER BY sale_date DESC
            ''', (username,))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_setting(self, key: str) -> str:
        with self.get_db_connection() as conn:
            cursor = conn.execute('SELECT value FROM settings WHERE key = ?', (key,))
            result = cursor.fetchone()
            return result['value'] if result else None
    
    def update_setting(self, key: str, value: str) -> bool:
        try:
            with self.get_db_connection() as conn:
                conn.execute('''
                    INSERT OR REPLACE INTO settings (key, value, updated_date) 
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                ''', (key, value))
                conn.commit()
                return True
        except:
            return False

class InventorySystem:
    def __init__(self):
        self.db = DatabaseManager()
        self.init_session_state()
    
    def init_session_state(self):
        """Initialize session state variables"""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
            st.session_state.current_user = None
            st.session_state.user_role = None
            st.session_state.language = self.db.get_setting('language') or 'en'
            st.session_state.editing_product = None
            st.session_state.view_mode = 'all_stocks'
            st.session_state.confirm_reset = False
    
    def get_text(self, key: str) -> str:
        """Get text based on selected language"""
        return LANGUAGES[st.session_state.language].get(key, key)
    
    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate user"""
        user = self.db.authenticate_user(username, password)
        if user:
            st.session_state.authenticated = True
            st.session_state.current_user = username
            st.session_state.user_role = user['role']
            return True
        return False
    
    def logout(self):
        """Logout user"""
        st.session_state.authenticated = False
        st.session_state.current_user = None
        st.session_state.user_role = None
        st.session_state.editing_product = None
        st.session_state.view_mode = 'all_stocks'
        st.session_state.confirm_reset = False
    
    def show_login(self):
        """Display login form with tech theme"""
        st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <div style='font-size: 3rem; color: #00bfff; margin-bottom: 1rem;'>
                📦
            </div>
            <h1 style='color: #00bfff; margin: 0; font-weight: 500;'>InvenTech Pro</h1>
            <p style='color: #666666; font-size: 1.1rem; margin: 0.5rem 0;'>Advanced Inventory Management</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.sidebar:
            st.markdown("### Language")
            language = st.selectbox(
                "Select Language",
                ['en', 'zh'],
                format_func=lambda x: 'English' if x == 'en' else '中文',
                key="login_language",
                label_visibility="collapsed"
            )

            if language != st.session_state.language:
                st.session_state.language = language
                self.db.update_setting('language', language)
                st.rerun()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.container():
                st.markdown("""
                <div style='
                    background: #ffffff;
                    padding: 2rem;
                    border-radius: 8px;
                    border: 1px solid #dee2e6;
                '>
                """, unsafe_allow_html=True)
                
                st.markdown(f"<h3 style='color: #00bfff; text-align: center; margin-bottom: 1.5rem; font-weight: 500;'>{self.get_text('login')}</h3>", unsafe_allow_html=True)
                
                username = st.text_input(self.get_text('username'), placeholder="Enter username", key="username_input")
                password = st.text_input(self.get_text('password'), type='password', placeholder="Enter password", key="password_input")
                
                if st.button(self.get_text('login'), use_container_width=True, type="primary"):
                    if self.authenticate(username, password):
                        st.success(f"{self.get_text('welcome')}, {username}!")
                        st.rerun()
                    else:
                        st.error(self.get_text('invalid_credentials'))
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("**Default Accounts:**")
            st.markdown("""
            - Super Admin: `superadmin` / `super123`
            - Admin: `admin123` / `admin123`  
            - Users: `user1-user5` / `user123`
            """)
    
    def show_dashboard(self):
        """Display comprehensive dashboard with stock list table and sales analytics"""
        st.markdown(f"""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h1 style='color: #00bfff; font-weight: 500;'>Welcome, {st.session_state.current_user}</h1>
        </div>
        """, unsafe_allow_html=True)
        
        products = self.db.get_all_products()
        sales = self.db.get_all_sales() if st.session_state.user_role in ['super_admin', 'admin'] else self.db.get_sales_by_user(st.session_state.current_user)
        user_stocks = self.db.get_user_stocks(st.session_state.current_user)
        all_users = self.db.get_all_users()
        
        # Key metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        total_products = len(products)
        low_stock = sum(1 for item in products if item['quantity'] <= item['min_stock'])
        total_stock_value = sum(item['quantity'] * item['selling_price'] for item in products)
        
        today = datetime.date.today()
        today_sales = [sale for sale in sales 
                      if datetime.datetime.fromisoformat(sale['sale_date']).date() == today]
        total_revenue = sum(sale['total_amount'] for sale in sales)
        weekly_sales = [sale for sale in sales 
                       if (today - datetime.datetime.fromisoformat(sale['sale_date']).date()).days <= 7]
        monthly_sales = [sale for sale in sales 
                        if (today - datetime.datetime.fromisoformat(sale['sale_date']).date()).days <= 30]
        
        today_revenue = sum(sale['total_amount'] for sale in today_sales)
        weekly_revenue = sum(sale['total_amount'] for sale in weekly_sales)
        monthly_revenue = sum(sale['total_amount'] for sale in monthly_sales)
        
        my_total_stock = sum(stock['assigned_quantity'] for stock in user_stocks)
        my_stock_value = sum(stock['assigned_quantity'] * stock['selling_price'] for stock in user_stocks)
        
        with col1:
            metric_value = total_products if st.session_state.user_role in ['super_admin', 'admin'] else my_total_stock
            metric_label = self.get_text('total_products') if st.session_state.user_role in ['super_admin', 'admin'] else self.get_text('my_total_stock')
            st.markdown(f"""
            <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px; border: 1px solid #dee2e6; text-align: center;'>
                <h3 style='margin: 0; font-size: 1.6rem; color: #00bfff; font-weight: 500;'>{metric_value}</h3>
                <p style='margin: 0.3rem 0 0 0; font-size: 0.9rem; color: #666666;'>{metric_label}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            metric_value = low_stock if st.session_state.user_role in ['super_admin', 'admin'] else my_stock_value
            metric_label = self.get_text('low_stock') if st.session_state.user_role in ['super_admin', 'admin'] else self.get_text('my_stock_value')
            value_format = f"{metric_value}" if st.session_state.user_role in ['super_admin', 'admin'] else f"${metric_value:.0f}"
            st.markdown(f"""
            <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px; border: 1px solid #dee2e6; text-align: center;'>
                <h3 style='margin: 0; font-size: 1.6rem; color: #00bfff; font-weight: 500;'>{value_format}</h3>
                <p style='margin: 0.3rem 0 0 0; font-size: 0.9rem; color: #666666;'>{metric_label}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px; border: 1px solid #dee2e6; text-align: center;'>
                <h3 style='margin: 0; font-size: 1.6rem; color: #00bfff; font-weight: 500;'>{len(today_sales)}</h3>
                <p style='margin: 0.3rem 0 0 0; font-size: 0.9rem; color: #666666;'>{self.get_text('total_sales_today')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px; border: 1px solid #dee2e6; text-align: center;'>
                <h3 style='margin: 0; font-size: 1.6rem; color: #00bfff; font-weight: 500;'>${weekly_revenue:.0f}</h3>
                <p style='margin: 0.3rem 0 0 0; font-size: 0.9rem; color: #666666;'>Weekly Revenue</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            st.markdown(f"""
            <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px; border: 1px solid #dee2e6; text-align: center;'>
                <h3 style='margin: 0; font-size: 1.6rem; color: #00bfff; font-weight: 500;'>${monthly_revenue:.0f}</h3>
                <p style='margin: 0.3rem 0 0 0; font-size: 0.9rem; color: #666666;'>Monthly Revenue</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <h2 style='color: #00bfff; text-align: center; margin: 2rem 0 1rem 0; font-weight: 500;'>
            Inventory - Stock List
        </h2>
        """, unsafe_allow_html=True)
        
        if products:
            stock_data = []
            all_user_stocks = self.db.get_all_user_stocks()
            for item in products:
                assigned_total = sum(stock['assigned_quantity'] for stock in all_user_stocks 
                                   if stock['product_id'] == item['product_id'])
                user_assignments = [f"{stock['username']}({stock['assigned_quantity']})" 
                                  for stock in all_user_stocks 
                                  if stock['product_id'] == item['product_id']]
                
                unassigned = item['quantity'] - assigned_total
                profit_margin = ((item['selling_price'] - item['cost_price']) / item['cost_price'] * 100) if item['cost_price'] > 0 else 0
                status = 'Out of Stock' if item['quantity'] == 0 else ('Low Stock' if item['quantity'] <= item['min_stock'] else 'In Stock')
                
                stock_data.append({
                    'Product ID': item['product_id'],
                    'Product Name': item['name'],
                    'Category': item['category'],
                    'Total Stock': item['quantity'],
                    'Assigned': assigned_total,
                    'Unassigned': unassigned,
                    'Min Stock': item['min_stock'],
                    'Cost Price': f"${item['cost_price']:.2f}",
                    'Selling Price': f"${item['selling_price']:.2f}",
                    'Profit %': f"{profit_margin:.1f}%",
                    'Stock Value': f"${item['quantity'] * item['selling_price']:.2f}",
                    'Status': status,
                    'Assigned To': ', '.join(user_assignments) if user_assignments else 'Unassigned'
                })
            
            df = pd.DataFrame(stock_data)
            
            def highlight_status(row):
                if 'Out of Stock' in row['Status']:
                    return ['background-color: #ffebee; color: #c62828'] * len(row)
                elif 'Low Stock' in row['Status']:
                    return ['background-color: #fff8e1; color: #ef6c00'] * len(row)
                else:
                    return ['background-color: #e8f5e9; color: #388e3c'] * len(row)
            
            styled_df = df.style.apply(highlight_status, axis=1).set_properties(**{'border-color': '#dee2e6', 'border-style': 'solid', 'border-width': '1px', 'padding': '10px', 'color': '#333333'})
            st.dataframe(styled_df, use_container_width=True, height=400)
            
            if st.session_state.user_role in ['super_admin', 'admin']:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Stock Value", f"${total_stock_value:.2f}", delta_color="normal")
                with col2:
                    total_assigned = sum(row['Assigned'] for row in stock_data)
                    st.metric("Total Assigned", total_assigned, delta_color="normal")
                with col3:
                    total_unassigned = sum(row['Unassigned'] for row in stock_data)
                    st.metric("Total Unassigned", total_unassigned, delta_color="normal")
                with col4:
                    avg_profit = sum(float(row['Profit %'].replace('%', '')) for row in stock_data) / len(stock_data) if stock_data else 0
                    st.metric("Avg Profit Margin", f"{avg_profit:.1f}%", delta_color="normal")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <h2 style='color: #00bfff; text-align: center; margin: 2rem 0 1rem 0; font-weight: 500;'>
            Sales Analytics
        </h2>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 3])
        with col1:
            period = st.selectbox("Report Period", 
                                ['Daily (Last 7 days)', 'Weekly (Last 4 weeks', 'Monthly (Last 6 months)'])
        
        if sales:
            sales_analytics = []
            if 'Daily' in period:
                for i in range(7):
                    date = today - datetime.timedelta(days=i)
                    day_sales = [sale for sale in sales 
                               if datetime.datetime.fromisoformat(sale['sale_date']).date() == date]
                    
                    total_revenue = sum(sale['total_amount'] for sale in day_sales)
                    avg_sale_value = total_revenue / len(day_sales) if day_sales else 0
                    
                    sales_analytics.append({
                        'Period': date.strftime('%Y-%m-%d (%a)'),
                        'Sales Count': len(day_sales),
                        'Revenue': total_revenue,
                        'Items Sold': sum(sale['quantity'] for sale in day_sales),
                        'Avg Sale': avg_sale_value
                    })
            
            elif 'Weekly' in period:
                for i in range(4):
                    start_date = today - datetime.timedelta(days=(i+1)*7)
                    end_date = today - datetime.timedelta(days=i*7)
                    week_sales = [sale for sale in sales 
                                if start_date <= datetime.datetime.fromisoformat(sale['sale_date']).date() < end_date]
                    
                    total_revenue = sum(sale['total_amount'] for sale in week_sales)
                    avg_sale_value = total_revenue / len(week_sales) if week_sales else 0
                    
                    sales_analytics.append({
                        'Period': f"Week {start_date.strftime('%m/%d')} - {end_date.strftime('%m/%d')}",
                        'Sales Count': len(week_sales),
                        'Revenue': total_revenue,
                        'Items Sold': sum(sale['quantity'] for sale in week_sales),
                        'Avg Sale': avg_sale_value
                    })
            
            else:  # Monthly
                for i in range(6):
                    target_month = today.month - i
                    target_year = today.year
                    if target_month <= 0:
                        target_month += 12
                        target_year -= 1
                    
                    month_sales = [sale for sale in sales 
                                 if datetime.datetime.fromisoformat(sale['sale_date']).month == target_month and 
                                    datetime.datetime.fromisoformat(sale['sale_date']).year == target_year]
                    
                    total_revenue = sum(sale['total_amount'] for sale in month_sales)
                    avg_sale_value = total_revenue / len(month_sales) if month_sales else 0
                    month_name = datetime.date(target_year, target_month, 1).strftime('%B %Y')
                    
                    sales_analytics.append({
                        'Period': month_name,
                        'Sales Count': len(month_sales),
                        'Revenue': total_revenue,
                        'Items Sold': sum(sale['quantity'] for sale in month_sales),
                        'Avg Sale': avg_sale_value
                    })
            
            if sales_analytics:
                display_data = [{
                    'Period': row['Period'],
                    'Sales Count': row['Sales Count'],
                    'Revenue': f"${row['Revenue']:.2f}",
                    'Items Sold': row['Items Sold'],
                    'Avg Sale': f"${row['Avg Sale']:.2f}"
                } for row in sales_analytics]
                
                sales_df = pd.DataFrame(display_data)
                st.dataframe(sales_df, use_container_width=True)
                
                chart_data = pd.DataFrame(sales_analytics)
                fig = px.bar(
                    chart_data,
                    x='Period',
                    y='Revenue',
                    title=f"{period} Revenue Trend",
                    color='Revenue',
                    color_continuous_scale='blues'
                )
                fig.update_layout(
                    title_font_color="#00bfff",
                    title_font_size=16,
                    font=dict(size=12, color="#333333"),
                    xaxis_tickangle=-45,
                    plot_bgcolor="#ffffff",
                    paper_bgcolor="#ffffff"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        if st.session_state.user_role in ['super_admin', 'admin']:
            st.markdown(f"""
            <h2 style='color: #00bfff; text-align: center; margin: 2rem 0 1rem 0; font-weight: 500;'>
                Salesperson Performance
            </h2>
            """, unsafe_allow_html=True)
            
            user_performance = []
            for user in all_users:
                if user['role'] == 'user':
                    user_sales = self.db.get_sales_by_user(user['username'])
                    user_stocks = self.db.get_user_stocks(user['username'])
                    
                    total_sales = len(user_sales)
                    total_revenue = sum(sale['total_amount'] for sale in user_sales)
                    assigned_products = len(user_stocks)
                    assigned_stock_qty = sum(stock['assigned_quantity'] for stock in user_stocks)
                    assigned_stock_value = sum(stock['assigned_quantity'] * stock['selling_price'] for stock in user_stocks)
                    
                    user_performance.append({
                        'Salesperson': user['username'],
                        'Sales Made': total_sales,
                        'Revenue Generated': f"${total_revenue:.2f}",
                        'Assigned Products': assigned_products,
                        'Assigned Stock Qty': assigned_stock_qty,
                        'Assigned Stock Value': f"${assigned_stock_value:.2f}",
                        'Performance': 'Excellent' if total_sales > 5 else ('Good' if total_sales > 2 else 'Growing')
                    })
            
            if user_performance:
                perf_df = pd.DataFrame(user_performance)
                st.dataframe(perf_df, use_container_width=True)
                
                chart_df = pd.DataFrame(user_performance)
                revenue_values = [float(rev.replace('$', '').replace(',', '')) 
                                for rev in chart_df['Revenue Generated']]
                chart_df['Revenue_num'] = revenue_values
                
                fig = px.bar(
                    chart_df,
                    x='Salesperson',
                    y='Revenue_num',
                    title="Salesperson Revenue Performance",
                    color='Revenue_num',
                    color_continuous_scale='blues'
                )
                fig.update_layout(
                    title_font_color="#00bfff",
                    title_font_size=16,
                    font=dict(size=12, color="#333333"),
                    xaxis_tickangle=-45,
                    plot_bgcolor="#ffffff",
                    paper_bgcolor="#ffffff"
                )
                st.plotly_chart(fig, use_container_width=True)
    
    def show_inventory(self):
        """Display inventory management with stock assignment"""
        st.markdown(f"""
        <h1 style='color: #00bfff; text-align: center; font-weight: 500;'>Inventory</h1>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            view_mode = st.radio(
                "View Mode",
                options=['all_stocks', 'my_stocks'],
                format_func=lambda x: self.get_text('all_stocks') if x == 'all_stocks' else self.get_text('my_stocks'),
                index=0 if st.session_state.get('view_mode', 'all_stocks') == 'all_stocks' else 1,
                key="view_mode_selector"
            )
            st.session_state.view_mode = view_mode
        
        if view_mode == 'all_stocks':
            self.show_all_inventory()
        else:
            self.show_my_stocks()
    
    def show_all_inventory(self):
        """Show all inventory - visible to all users"""
        products = self.db.get_all_products()
        
        if st.session_state.user_role in ['super_admin', 'admin']:
            with st.expander(f"Add Product", expanded=False):
                with st.form("add_product_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        product_id = st.text_input("Product ID *", value=f"PROD{len(products)+1:03d}")
                        product_name = st.text_input(f"{self.get_text('product_name')} *")
                        category = st.text_input(f"{self.get_text('category')} *")
                    
                    with col2:
                        quantity = st.number_input(self.get_text('quantity'), min_value=0, value=0)
                        cost_price = st.number_input(self.get_text('cost_price'), min_value=0.0, value=0.0, step=0.01)
                        selling_price = st.number_input(self.get_text('selling_price'), min_value=0.0, value=0.0, step=0.01)
                        min_stock = st.number_input(self.get_text('min_stock'), min_value=0, value=5)
                    
                    submitted = st.form_submit_button(self.get_text('add_product'), type="primary")
                    if submitted:
                        if product_id and product_name and category:
                            if self.db.create_product(product_id, product_name, category, quantity, 
                                                    cost_price, selling_price, min_stock, st.session_state.current_user):
                                st.success(self.get_text('product_added'))
                                st.rerun()
                            else:
                                st.error("Product ID already exists!")
                        else:
                            st.error("Please fill in all required fields (*)")
        
        if st.session_state.user_role in ['super_admin', 'admin']:
            with st.expander(f"Assign Stock", expanded=False):
                with st.form("assign_stock_form"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        users = self.db.get_all_users()
                        user_options = [user['username'] for user in users if user['role'] == 'user']
                        selected_user = st.selectbox(self.get_text('select_user'), user_options)
                    
                    with col2:
                        product_options = {f"{item['product_id']} - {item['name']}": item['product_id'] 
                                         for item in products}
                        selected_product_display = st.selectbox(self.get_text('select_product'), 
                                                              list(product_options.keys()))
                        selected_product_id = product_options.get(selected_product_display)
                    
                    with col3:
                        if selected_product_id:
                            unassigned_qty = self.db.get_unassigned_stock_quantity(selected_product_id)
                            st.info(f"Unassigned: {unassigned_qty}")
                            quantity_to_assign = st.number_input(
                                self.get_text('quantity_to_assign'), 
                                min_value=1, max_value=unassigned_qty, value=1
                            )
                        else:
                            quantity_to_assign = 0
                    
                    if st.form_submit_button(self.get_text('assign_stock'), type="primary"):
                        if selected_user and selected_product_id and quantity_to_assign > 0:
                            if self.db.assign_stock_to_user(selected_user, selected_product_id, 
                                                          quantity_to_assign, st.session_state.current_user):
                                st.success(self.get_text('stock_assigned'))
                                st.rerun()
                            else:
                                st.error("Failed to assign stock")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            search = st.text_input(f"Search Products", key="inventory_search")
        with col2:
            categories = sorted(list(set(item['category'] for item in products))) if products else []
            category_filter = st.selectbox(self.get_text('filter_category'), ['All'] + categories, key="category_filter")
        
        if products:
            filtered_products = [
                item for item in products
                if (not search or search.lower() in item['name'].lower()) and
                   (category_filter == 'All' or item['category'] == category_filter)
            ]
            
            for item in filtered_products:
                profit_margin = ((item['selling_price'] - item['cost_price']) / item['cost_price'] * 100) if item['cost_price'] > 0 else 0
                status = 'Out of Stock' if item['quantity'] == 0 else ('Low Stock' if item['quantity'] <= item['min_stock'] else 'In Stock')
                unassigned_qty = self.db.get_unassigned_stock_quantity(item['product_id'])
                
                with st.container():
                    st.markdown(f"""
                    <div style='background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; 
                                padding: 1rem; margin: 1rem 0;'>
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <div>
                                <h4 style='color: #00bfff; margin: 0 0 0.5rem 0; font-weight: 500;'>{item['name']} ({item['product_id']})</h4>
                                <p style='margin: 0; color: #666666;'>Category: {item['category']} | Total: {item['quantity']} | Unassigned: {unassigned_qty} | {status}</p>
                                <p style='margin: 0.5rem 0 0 0; color: #666666;'>Cost: ${item['cost_price']:.2f} | Selling: ${item['selling_price']:.2f} | Profit: {profit_margin:.1f}%</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.session_state.user_role in ['super_admin', 'admin']:
                        col1, col2, col3 = st.columns([1, 1, 8])
                        with col1:
                            if st.button(f"Edit", key=f"edit_{item['product_id']}"):
                                st.session_state.editing_product = item['product_id']
                                st.rerun()
                        with col2:
                            if st.button(f"Delete", key=f"delete_{item['product_id']}"):
                                if st.session_state.get(f"confirm_delete_{item['product_id']}", False):
                                    if self.db.delete_product(item['product_id']):
                                        st.success(self.get_text('product_deleted'))
                                        st.rerun()
                                else:
                                    st.session_state[f"confirm_delete_{item['product_id']}"] = True
                                    st.warning("Click again to confirm deletion")
                
                if st.session_state.editing_product:
                    product = self.db.get_product(st.session_state.editing_product)
                    if product:
                        st.markdown("---")
                        st.markdown(f"### Edit Product: {product['name']}")
                        
                        with st.form(f"edit_product_form_{product['product_id']}"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                new_name = st.text_input(self.get_text('product_name'), value=product['name'])
                                new_category = st.text_input(self.get_text('category'), value=product['category'])
                                new_quantity = st.number_input(self.get_text('quantity'), value=product['quantity'])
                            
                            with col2:
                                new_cost_price = st.number_input(self.get_text('cost_price'), value=float(product['cost_price']), step=0.01)
                                new_selling_price = st.number_input(self.get_text('selling_price'), value=float(product['selling_price']), step=0.01)
                                new_min_stock = st.number_input(self.get_text('min_stock'), value=product['min_stock'])
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.form_submit_button(self.get_text('save_changes'), type="primary"):
                                    if self.db.update_product(product['product_id'], new_name, new_category, 
                                                            new_quantity, new_cost_price, new_selling_price, new_min_stock):
                                        st.success(self.get_text('product_updated'))
                                        st.session_state.editing_product = None
                                        st.rerun()
                                    else:
                                        st.error("Failed to update product")
                            
                            with col2:
                                if st.form_submit_button(self.get_text('cancel')):
                                    st.session_state.editing_product = None
                                    st.rerun()
            else:
                st.info("No products found matching your criteria.")
        else:
            st.info("No products in inventory yet.")
    
    def show_my_stocks(self):
        """Show user's assigned stocks"""
        user_stocks = self.db.get_user_stocks(st.session_state.current_user)
        
        if user_stocks:
            st.markdown(f"### Assigned Stocks")
            
            for stock in user_stocks:
                profit_margin = ((stock['selling_price'] - stock['cost_price']) / stock['cost_price'] * 100) if stock['cost_price'] > 0 else 0
                stock_value = stock['assigned_quantity'] * stock['selling_price']
                
                with st.container():
                    st.markdown(f"""
                    <div style='background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; 
                                padding: 1rem; margin: 1rem 0;'>
                        <div>
                            <h4 style='color: #00bfff; margin: 0 0 0.5rem 0; font-weight: 500;'>{stock['name']} ({stock['product_id']})</h4>
                            <p style='margin: 0; color: #666666;'>Category: {stock['category']} | Assigned Qty: {stock['assigned_quantity']}</p>
                            <p style='margin: 0.5rem 0 0 0; color: #666666;'>Unit Price: ${stock['selling_price']:.2f} | Stock Value: ${stock_value:.2f} | Profit Margin: {profit_margin:.1f}%</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No stocks assigned to you yet. Please contact your administrator.")
    
    def show_sales(self):
        """Display sales management with user stock validation"""
        st.markdown(f"""
        <h1 style='color: #00bfff; text-align: center; font-weight: 500;'>Sales</h1>
        """, unsafe_allow_html=True)
        
        with st.expander(f"Record Sale", expanded=False):
            if st.session_state.user_role in ['super_admin', 'admin']:
                products = self.db.get_all_products()
                available_products = [p for p in products if p['quantity'] > 0]
            else:
                user_stocks = self.db.get_user_stocks(st.session_state.current_user)
                available_products = [p for p in user_stocks if p['assigned_quantity'] > 0]
            
            if available_products:
                with st.form("record_sale_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        product_options = {f"{item['product_id']} - {item['name']}": item['product_id'] 
                                         for item in available_products}
                        selected_product_display = st.selectbox(self.get_text('select_product'), 
                                                              options=list(product_options.keys()))
                        selected_product_id = product_options.get(selected_product_display)
                        
                        if selected_product_id:
                            selected_product = next(p for p in available_products if p['product_id'] == selected_product_id)
                            available_qty = selected_product['quantity'] if st.session_state.user_role in ['super_admin', 'admin'] else selected_product['assigned_quantity']
                            unit_price = selected_product['selling_price']
                            
                            st.info(f"Available quantity: {available_qty}")
                            st.info(f"Unit price: ${unit_price:.2f}")
                            
                            quantity_sold = st.number_input(self.get_text('quantity_sold'), 
                                                          min_value=1, max_value=available_qty, value=1)
                    
                    with col2:
                        sale_date = st.date_input(self.get_text('sale_date'), value=datetime.date.today())
                        salesperson = st.text_input(self.get_text('salesperson'), 
                                                  value=st.session_state.current_user)
                    
                    if st.form_submit_button(self.get_text('record_sale'), type="primary"):
                        if selected_product_id and quantity_sold > 0:
                            total_amount = unit_price * quantity_sold
                            sale_id = str(uuid.uuid4())
                            sale_datetime = datetime.datetime.combine(sale_date, datetime.datetime.now().time())
                            
                            if self.db.create_sale(sale_id, selected_product_id, selected_product['name'],
                                                 quantity_sold, unit_price, total_amount, sale_datetime, salesperson):
                                
                                if st.session_state.user_role in ['super_admin', 'admin']:
                                    new_quantity = selected_product['quantity'] - quantity_sold
                                    self.db.update_stock_quantity(selected_product_id, new_quantity)
                                else:
                                    new_assigned_qty = selected_product['assigned_quantity'] - quantity_sold
                                    self.db.update_user_stock_quantity(st.session_state.current_user, 
                                                                     selected_product_id, new_assigned_qty)
                                    main_product = self.db.get_product(selected_product_id)
                                    new_main_qty = main_product['quantity'] - quantity_sold
                                    self.db.update_stock_quantity(selected_product_id, new_main_qty)
                                
                                st.success(f"{self.get_text('sale_recorded')} - Total: ${total_amount:.2f}")
                                st.rerun()
                            else:
                                st.error("Failed to record sale")
            else:
                st.info("No products with available stock." if st.session_state.user_role in ['super_admin', 'admin'] 
                       else "No assigned stocks available for sale. Please contact your administrator.")
        
        st.markdown(f"### Sales History")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            start_date = st.date_input("Start Date", value=datetime.date.today() - datetime.timedelta(days=30))
        with col2:
            end_date = st.date_input("End Date", value=datetime.date.today())
        with col3:
            view_type = st.selectbox("View", [self.get_text('daily_sales'), 
                                            self.get_text('weekly_sales'), 
                                            self.get_text('monthly_sales')])
        
        sales = self.db.get_sales_by_date_range(start_date, end_date) if st.session_state.user_role in ['super_admin', 'admin'] else \
                [sale for sale in self.db.get_sales_by_user(st.session_state.current_user) 
                 if start_date <= datetime.datetime.fromisoformat(sale['sale_date']).date() <= end_date]
        
        if sales:
            sales_data = [{
                'Date': datetime.datetime.fromisoformat(sale['sale_date']).strftime('%Y-%m-%d %H:%M'),
                'Product': sale['product_name'],
                'Quantity': sale['quantity'],
                'Unit Price': f"${sale['unit_price']:.2f}",
                'Total': f"${sale['total_amount']:.2f}",
                'Salesperson': sale['salesperson']
            } for sale in sales]
            
            df = pd.DataFrame(sales_data)
            st.dataframe(df, use_container_width=True)
            
            total_sales = len(sales)
            total_revenue = sum(sale['total_amount'] for sale in sales)
            avg_sale = total_revenue / total_sales if total_sales > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Sales", total_sales)
            with col2:
                st.metric("Total Revenue", f"${total_revenue:.2f}")
            with col3:
                st.metric("Average Sale", f"${avg_sale:.2f}")
        else:
            st.info("No sales found for the selected date range.")
    
    def show_profile(self):
        """Display user profile and credential management"""
        st.markdown(f"""
        <h1 style='color: #00bfff; text-align: center; font-weight: 500;'>Profile</h1>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style='background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; 
                    padding: 1.5rem; margin: 1rem 0; text-align: center;'>
            <h3 style='color: #00bfff; margin: 0 0 1rem 0; font-weight: 500;'>{st.session_state.current_user}</h3>
            <p style='color: #666666; margin: 0;'>Role: {st.session_state.user_role}</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander(f"Change Credentials", expanded=False):
            with st.form("change_credentials_form"):
                st.markdown("### Update Credentials")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    current_password = st.text_input(self.get_text('current_password'), type='password')
                    new_username = st.text_input(self.get_text('new_username'), value=st.session_state.current_user)
                
                with col2:
                    new_password = st.text_input(self.get_text('new_password'), type='password')
                    confirm_password = st.text_input(self.get_text('confirm_password'), type='password')
                
                if st.form_submit_button(self.get_text('update_credentials'), type="primary"):
                    if not current_password:
                        st.error("Please enter your current password")
                    elif new_password != confirm_password:
                        st.error(self.get_text('password_mismatch'))
                    elif len(new_password) < 6:
                        st.error("New password must be at least 6 characters long")
                    elif not new_username:
                        st.error("Username cannot be empty")
                    else:
                        if self.db.update_user_credentials(st.session_state.current_user, current_password,
                                                         new_username, new_password):
                            st.success(self.get_text('credentials_updated'))
                            st.session_state.current_user = new_username
                            st.info("Please login again with your new credentials")
                            self.logout()
                            st.rerun()
                        else:
                            st.error("Failed to update credentials. Please check your current password.")
        
        if st.session_state.user_role == 'user':
            user_stocks = self.db.get_user_stocks(st.session_state.current_user)
            user_sales = self.db.get_sales_by_user(st.session_state.current_user)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Assigned Products", len(user_stocks))
            with col2:
                st.metric("Total Assigned Quantity", sum(stock['assigned_quantity'] for stock in user_stocks))
            with col3:
                st.metric("Total Sales Made", len(user_sales))
    
    def show_users(self):
        """Display user management with database integration"""
        if st.session_state.user_role not in ['super_admin', 'admin']:
            st.error(self.get_text('access_denied'))
            return
        
        st.markdown(f"""
        <h1 style='color: #00bfff; text-align: center; font-weight: 500;'>Users</h1>
        """, unsafe_allow_html=True)
        
        users = self.db.get_all_users()
        max_users = int(self.db.get_setting('max_users') or 10)
        
        st.markdown(f"### Current Users ({len(users)}/{max_users})")
        
        for user in users:
            role_emoji = 'Super Admin' if user['role'] == 'super_admin' else ('Admin' if user['role'] == 'admin' else 'User')
            created_date = datetime.datetime.fromisoformat(user['created_date']).strftime('%Y-%m-%d')
            stock_info = f" | Assigned: {len(self.db.get_user_stocks(user['username']))} products ({sum(stock['assigned_quantity'] for stock in self.db.get_user_stocks(user['username']))} items)" if user['role'] == 'user' else ""
            
            st.markdown(f"""
            <div style='background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; 
                        padding: 1rem; margin: 0.5rem 0;'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <h4 style='color: #00bfff; margin: 0; font-weight: 500;'>{user['username']}</h4>
                        <p style='margin: 0; color: #666666;'>Role: {role_emoji} | Created: {created_date}{stock_info}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        if len(users) < max_users:
            with st.expander(f"Create User", expanded=False):
                with st.form("create_user_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        new_username = st.text_input("Username *")
                        new_password = st.text_input("Password *", type='password')
                    
                    with col2:
                        role_options = ['user'] if st.session_state.user_role == 'admin' else ['user', 'admin']
                        new_role = st.selectbox(self.get_text('user_role'), role_options)
                    
                    if st.form_submit_button(self.get_text('create_user'), type="primary"):
                        if new_username and new_password:
                            if len(new_password) >= 6:
                                if self.db.create_user(new_username, new_password, new_role):
                                    st.success(self.get_text('user_created'))
                                    st.rerun()
                                else:
                                    st.error("Username already exists")
                            else:
                                st.error("Password must be at least 6 characters long")
                        else:
                            st.error("Please fill in all required fields")
        else:
            st.warning(f"Maximum users limit ({max_users}) reached")
    
    def show_settings(self):
        """Display settings with comprehensive inventory management options"""
        if st.session_state.user_role not in ['super_admin', 'admin']:
            st.error(self.get_text('access_denied'))
            return
        
        st.markdown(f"""
        <h1 style='color: #00bfff; text-align: center; font-weight: 500;'>Settings</h1>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <h3 style='color: #00bfff; margin-top: 2rem; font-weight: 500;'>System Configuration</h3>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            language = st.selectbox(
                self.get_text('language'),
                options=['en', 'zh'],
                format_func=lambda x: 'English' if x == 'en' else '中文',
                index=0 if st.session_state.language == 'en' else 1,
                key="settings_language"
            )
            if language != st.session_state.language:
                st.session_state.language = language
                self.db.update_setting('language', language)
                st.rerun()
        
        with col2:
            current_max_users = int(self.db.get_setting('max_users') or 10)
            max_users = st.number_input(
                self.get_text('max_users'),
                min_value=5,
                max_value=50,
                value=current_max_users
            )
            if max_users != current_max_users:
                self.db.update_setting('max_users', str(max_users))
                st.success("Settings updated!")
        
        st.markdown("""
        <h3 style='color: #00bfff; margin-top: 2rem; font-weight: 500;'>Inventory Management</h3>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; 
                    padding: 1.5rem; margin: 1rem 0;'>
            <h4 style='color: #00bfff; margin: 0 0 1rem 0; font-weight: 500;'>Current System Features:</h4>
            <ul style='color: #666666; margin: 0;'>
                <li><strong>Stock Visibility:</strong> All users can view complete stock list</li>
                <li><strong>Individual Assignment:</strong> Admins assign specific quantities to each user</li>
                <li><strong>Sales Control:</strong> Users can only sell from their assigned inventory</li>
                <li><strong>Real-time Tracking:</strong> Boss/Admin can monitor all inventory and sales in real-time</li>
                <li><strong>Dual Mode:</strong> Shared visibility + Individual responsibility</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        current_individual = self.db.get_setting('individual_stock_management') == 'true'
        mode = st.radio(
            "Inventory Management Mode:",
            options=['individual', 'shared'],
            format_func=lambda x: 'Individual Stock Assignment' if x == 'individual' 
                                 else 'Shared Inventory Pool',
            index=0 if current_individual else 1
        )
        
        individual_management = (mode == 'individual')
        if individual_management != current_individual:
            self.db.update_setting('individual_stock_management', 'true' if individual_management else 'false')
            st.success("Stock management mode updated!")
            st.rerun()
        
        st.markdown("""
        <div style='background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; 
                    padding: 1.5rem; margin: 1rem 0;'>
            <h4 style='color: #00bfff; margin: 0 0 1rem 0; font-weight: 500;'>Quick Actions</h4>
            <p style='color: #666666; margin: 0 0 1rem 0;'>System management options for administrators</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button(f"Reset Assignments", key="reset_assignments"):
                st.session_state.confirm_reset = True
        
        with col2:
            if st.button(f"Export Data", key="export_data"):
                self.export_system_data()
        
        with col3:
            if st.button(f"Cleanup Sales", key="cleanup_sales"):
                self.cleanup_old_sales()
        
        if st.session_state.get('confirm_reset', False):
            st.warning("Are you sure you want to reset all user stock assignments?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Confirm Reset", type="primary"):
                    self.reset_all_assignments()
                    st.session_state.confirm_reset = False
                    st.success("All user assignments reset successfully!")
                    st.rerun()
            with col2:
                if st.button("Cancel"):
                    st.session_state.confirm_reset = False
                    st.rerun()
    
    def reset_all_assignments(self):
        """Reset all user stock assignments"""
        try:
            with self.db.get_db_connection() as conn:
                conn.execute('DELETE FROM user_stocks')
                conn.commit()
                return True
        except:
            return False
    
    def export_system_data(self):
        """Export system data to CSV files"""
        try:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Export inventory
            products = self.db.get_all_products()
            inventory_df = pd.DataFrame(products)
            inventory_df.to_csv(f'inventory_export_{timestamp}.csv', index=False)
            
            # Export sales
            sales = self.db.get_all_sales()
            sales_df = pd.DataFrame(sales)
            sales_df.to_csv(f'sales_export_{timestamp}.csv', index=False)
            
            # Export user stocks
            user_stocks = self.db.get_all_user_stocks()
            user_stocks_df = pd.DataFrame(user_stocks)
            user_stocks_df.to_csv(f'user_stocks_export_{timestamp}.csv', index=False)
            
            # Export users
            users = self.db.get_all_users()
            users_df = pd.DataFrame(users)
            users_df.to_csv(f'users_export_{timestamp}.csv', index=False)
            
            st.success(f"Data exported successfully to CSV files with timestamp {timestamp}")
        except Exception as e:
            st.error(f"Failed to export data: {str(e)}")
    
    def cleanup_old_sales(self):
        """Remove sales records older than 6 months"""
        try:
            six_months_ago = datetime.date.today() - datetime.timedelta(days=180)
            with self.db.get_db_connection() as conn:
                conn.execute('DELETE FROM sales WHERE DATE(sale_date) < ?', (six_months_ago,))
                conn.commit()
            st.success("Old sales records cleaned up successfully")
        except Exception as e:
            st.error(f"Failed to cleanup sales: {str(e)}")
    
    def show_stock_database(self):
        """Display comprehensive stock database management"""
        if st.session_state.user_role not in ['super_admin', 'admin']:
            st.error(self.get_text('access_denied'))
            return
        
        st.markdown(f"""
        <h1 style='color: #00bfff; text-align: center; font-weight: 500;'>Stock Database</h1>
        """, unsafe_allow_html=True)
        
        products = self.db.get_all_products()
        
        # Database statistics
        st.markdown(f"### Database Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        total_stock_value = sum(item['quantity'] * item['selling_price'] for item in products)
        total_stock_quantity = sum(item['quantity'] for item in products)
        avg_profit_margin = sum(((item['selling_price'] - item['cost_price']) / item['cost_price'] * 100) 
                              if item['cost_price'] > 0 else 0 for item in products) / len(products) if products else 0
        low_stock_items = sum(1 for item in products if item['quantity'] <= item['min_stock'])
        
        with col1:
            st.metric(self.get_text('total_stock_value'), f"${total_stock_value:.2f}")
        with col2:
            st.metric(self.get_text('total_stock_quantity'), total_stock_quantity)
        with col3:
            st.metric(self.get_text('avg_profit_margin'), f"{avg_profit_margin:.1f}%")
        with col4:
            st.metric(self.get_text('low_stock_items'), low_stock_items)
        
        # Quick actions
        st.markdown(f"### Quick Actions")
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"Export Database", key="export_db"):
                self.export_system_data()
        with col2:
            if st.button(f"Refresh Data", key="refresh_db"):
                st.rerun()
        
        # Search and filter
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            search = st.text_input(f"Search Products", key="db_search")
        with col2:
            categories = sorted(list(set(item['category'] for item in products))) if products else []
            category_filter = st.selectbox(self.get_text('filter_by_category'), ['All'] + categories, key="db_category_filter")
        with col3:
            sort_by = st.selectbox(self.get_text('sort_by'), 
                                  ['Name', 'Category', 'Quantity', 'Price'], 
                                  key="db_sort_by")
        
        # Quick stock update
        with st.expander(f"Quick Stock Update", expanded=False):
            with st.form("quick_stock_update_form"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    product_options = {f"{item['product_id']} - {item['name']}": item['product_id'] 
                                     for item in products}
                    selected_product = st.selectbox(self.get_text('select_product'), list(product_options.keys()))
                with col2:
                    new_stock_level = st.number_input(self.get_text('new_stock_level'), min_value=0, value=0)
                with col3:
                    if st.form_submit_button(self.get_text('update_stock'), type="primary"):
                        if selected_product:
                            product_id = product_options[selected_product]
                            if self.db.update_stock_quantity(product_id, new_stock_level):
                                st.success(f"Stock updated for {selected_product}")
                                st.rerun()
                            else:
                                st.error("Failed to update stock")
        
        # Display products
        if products:
            filtered_products = [
                item for item in products
                if (not search or search.lower() in item['name'].lower()) and
                   (category_filter == 'All' or item['category'] == category_filter)
            ]
            
            sort_key = {
                'Name': 'name',
                'Category': 'category',
                'Quantity': 'quantity',
                'Price': 'selling_price'
            }[sort_by]
            
            filtered_products.sort(key=lambda x: x[sort_key], reverse=(sort_by in ['Quantity', 'Price']))
            
            for item in filtered_products:
                profit_margin = ((item['selling_price'] - item['cost_price']) / item['cost_price'] * 100) if item['cost_price'] > 0 else 0
                status = 'Out of Stock' if item['quantity'] == 0 else ('Low Stock' if item['quantity'] <= item['min_stock'] else 'In Stock')
                
                with st.container():
                    st.markdown(f"""
                    <div style='background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; 
                                padding: 1rem; margin: 1rem 0;'>
                        <div>
                            <h4 style='color: #00bfff; margin: 0 0 0.5rem 0; font-weight: 500;'>{item['name']} ({item['product_id']})</h4>
                            <p style='margin: 0; color: #666666;'>Category: {item['category']} | Status: {status}</p>
                            <p style='margin: 0.5rem 0 0 0; color: #666666;'>Quantity: {item['quantity']} | Min Stock: {item['min_stock']}</p>
                            <p style='margin: 0.5rem 0 0 0; color: #666666;'>Cost: ${item['cost_price']:.2f} | Selling: ${item['selling_price']:.2f} | Profit: {profit_margin:.1f}%</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns([1, 1, 8])
                    with col1:
                        if st.button(f"Edit", key=f"db_edit_{item['product_id']}"):
                            st.session_state.editing_product = item['product_id']
                            st.rerun()
                    with col2:
                        if st.button(f"Delete", key=f"db_delete_{item['product_id']}"):
                            if st.session_state.get(f"db_confirm_delete_{item['product_id']} ", False):
                                if self.db.delete_product(item['product_id']):
                                    st.success(self.get_text('product_deleted'))
                                    st.rerun()
                                else:
                                    st.error("Failed to delete product")
                            else:
                                st.session_state[f"db_confirm_delete_{item['product_id']}"] = True
                                st.warning("Click again to confirm deletion")
            
            if st.session_state.editing_product:
                product = self.db.get_product(st.session_state.editing_product)
                if product:
                    st.markdown(f"### Edit Product: {product['name']}")
                    with st.form(f"db_edit_product_form_{product['product_id']}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            new_name = st.text_input(self.get_text('product_name'), value=product['name'])
                            new_category = st.text_input(self.get_text('category'), value=product['category'])
                            new_quantity = st.number_input(self.get_text('quantity'), value=product['quantity'], min_value=0)
                        
                        with col2:
                            new_cost_price = st.number_input(self.get_text('cost_price'), value=float(product['cost_price']), step=0.01)
                            new_selling_price = st.number_input(self.get_text('selling_price'), value=float(product['selling_price']), step=0.01)
                            new_min_stock = st.number_input(self.get_text('min_stock'), value=product['min_stock'], min_value=0)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button(self.get_text('update_database'), type="primary"):
                                if self.db.update_product(product['product_id'], new_name, new_category, 
                                                        new_quantity, new_cost_price, new_selling_price, new_min_stock):
                                    st.success(self.get_text('product_updated'))
                                    st.session_state.editing_product = None
                                    st.rerun()
                                else:
                                    st.error("Failed to update product")
                        
                        with col2:
                            if st.form_submit_button(self.get_text('cancel_edit')):
                                st.session_state.editing_product = None
                                st.rerun()
        else:
            st.info("No products in the database.")
    
    def run(self):
        """Main application loop"""
        st.set_page_config(page_title="InvenTech Pro", page_icon="📦", layout="wide")
        
        # Custom CSS for tech theme
        st.markdown("""
        <style>
            .stApp {
                background: #ffffff;
            }
            .sidebar .sidebar-content {
                background: #f8f9fa;
            }
            .stButton>button {
                border-radius: 4px;
                font-weight: 400;
                border: 1px solid #dee2e6;
                background: #f8f9fa;
                color: #00bfff;
            }
            .stButton>button:hover {
                background: #e9ecef;
            }
            .stButton>button[type="primary"] {
                background: #00bfff;
                color: #ffffff;
                border: none;
            }
            .stButton>button[type="primary"]:hover {
                background: #009acd;
            }
            .stTextInput>div>input {
                border-radius: 4px;
                border: 1px solid #dee2e6;
                background: #ffffff;
                color: #333333;
            }
            .stNumberInput>div>input {
                border-radius: 4px;
                border: 1px solid #dee2e6;
                background: #ffffff;
                color: #333333;
            }
            .stSelectbox>div>select {
                border-radius: 4px;
                border: 1px solid #dee2e6;
                background: #ffffff;
                color: #333333;
            }
            .stExpander {
                border: 1px solid #dee2e6;
                border-radius: 4px;
                background: #f8f9fa;
            }
            .stAlert {
                border-radius: 4px;
                background: #fff3cd;
                color: #856404;
            }
            .row-widget.stRadio > div {
                flex-direction: row;
            }
            [data-testid="stMarkdownContainer"] p {
                font-size: 0.95rem;
                color: #666666;
            }
            h1, h2, h3, h4 {
                font-weight: 500;
                color: #00bfff;
            }
            .stMetric label {
                color: #666666;
            }
            .stMetric value {
                color: #00bfff;
            }
            .stDataFrame {
                background: #ffffff;
                color: #333333;
            }
        </style>
        """, unsafe_allow_html=True)
        
        if not st.session_state.authenticated:
            self.show_login()
        else:
            with st.sidebar:
                st.markdown(f"""
                <div style='text-align: center; padding: 1rem;'>
                    <h3 style='color: #00bfff; font-weight: 500;'>InvenTech Pro</h3>
                    <p style='color: #666666;'>Logged in as: <strong>{st.session_state.current_user}</strong></p>
                    <p style='color: #666666;'>Role: <strong>{st.session_state.user_role}</strong></p>
                </div>
                """, unsafe_allow_html=True)
                
                menu_options = {
                    'dashboard': f"Dashboard",
                    'inventory': f"Inventory",
                    'sales': f"Sales",
                    'profile': f"Profile"
                }
                
                if st.session_state.user_role in ['super_admin', 'admin']:
                    menu_options['users'] = f"Users"
                    menu_options['settings'] = f"Settings"
                    menu_options['stock_database'] = f"Stock Database"
                
                selected_page = st.radio(
                    "Navigation",
                    options=list(menu_options.keys()),
                    format_func=lambda x: menu_options[x],
                    key="nav_menu"
                )
                
                st.markdown("---")
                if st.button(f"Logout", type="secondary", use_container_width=True):
                    self.logout()
                    st.rerun()
            
            if selected_page == 'dashboard':
                self.show_dashboard()
            elif selected_page == 'inventory':
                self.show_inventory()
            elif selected_page == 'sales':
                self.show_sales()
            elif selected_page == 'profile':
                self.show_profile()
            elif selected_page == 'users':
                self.show_users()
            elif selected_page == 'settings':
                self.show_settings()
            elif selected_page == 'stock_database':
                self.show_stock_database()

if __name__ == "__main__":
    app = InventorySystem()
    app.run()
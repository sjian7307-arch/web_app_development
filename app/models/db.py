import sqlite3
import os

# 將資料庫儲存在 instance 資料夾中
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    """取得資料庫連線，並設定 row_factory 讓回傳結果可用 dict 存取欄位"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # 啟用 Foreign Key 支援
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn

def init_db():
    """初始化資料庫表結構"""
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
    if not os.path.exists(schema_path):
        return
    with get_db_connection() as conn:
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())

from .db import get_db_connection

class Event:
    @staticmethod
    def create(title, description, schedule, capacity):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO events (title, description, schedule, capacity)
                VALUES (?, ?, ?, ?)
            ''', (title, description, schedule, capacity))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            return conn.execute('SELECT * FROM events ORDER BY created_at DESC').fetchall()

    @staticmethod
    def get_by_id(event_id):
        with get_db_connection() as conn:
            return conn.execute('SELECT * FROM events WHERE id = ?', (event_id,)).fetchone()

    @staticmethod
    def update(event_id, title, description, schedule, capacity):
        with get_db_connection() as conn:
            conn.execute('''
                UPDATE events
                SET title = ?, description = ?, schedule = ?, capacity = ?
                WHERE id = ?
            ''', (title, description, schedule, capacity, event_id))
            conn.commit()

    @staticmethod
    def delete(event_id):
        with get_db_connection() as conn:
            conn.execute('DELETE FROM events WHERE id = ?', (event_id,))
            conn.commit()

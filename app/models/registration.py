from .db import get_db_connection

class Registration:
    @staticmethod
    def create(event_id, participant_name, email, phone):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO registrations (event_id, participant_name, email, phone, payment_status)
                VALUES (?, ?, ?, ?, 'unpaid')
            ''', (event_id, participant_name, email, phone))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_by_event_id(event_id):
        with get_db_connection() as conn:
            return conn.execute('SELECT * FROM registrations WHERE event_id = ? ORDER BY created_at DESC', (event_id,)).fetchall()

    @staticmethod
    def get_by_id(registration_id):
        with get_db_connection() as conn:
            return conn.execute('SELECT * FROM registrations WHERE id = ?', (registration_id,)).fetchone()

    @staticmethod
    def update_payment_status(registration_id, payment_status):
        with get_db_connection() as conn:
            conn.execute('''
                UPDATE registrations
                SET payment_status = ?
                WHERE id = ?
            ''', (payment_status, registration_id))
            conn.commit()

    @staticmethod
    def delete(registration_id):
        with get_db_connection() as conn:
            conn.execute('DELETE FROM registrations WHERE id = ?', (registration_id,))
            conn.commit()
            
    @staticmethod
    def count_by_event_id(event_id):
        with get_db_connection() as conn:
            result = conn.execute('SELECT COUNT(*) as count FROM registrations WHERE event_id = ?', (event_id,)).fetchone()
            return result['count']

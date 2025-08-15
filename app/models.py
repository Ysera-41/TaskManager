from .database import get_connection
from datetime import datetime

def insert_task(desc, categoria, dt_vencimento=None):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO TASK (DS_TASK, DT_INCL, DT_VENCIMENTO, STATUS, CATEGORIA)
                VALUES (?, CURRENT_TIMESTAMP, ?, 'AF', ?)
            ''', (desc, dt_vencimento, categoria))
            conn.commit()


def get_tasks():
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT ID, DS_TASK, STATUS, CATEGORIA, DT_VENCIMENTO
                FROM TASK
                WHERE DT_EXCLUSAO IS NULL
                ORDER BY DT_VENCIMENTO DESC
            """)
            return cursor.fetchall()
    
def get_task_completa():
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                    SELECT ID, DS_TASK, STATUS, CATEGORIA
                    FROM TASK
                    WHERE DT_EXCLUSAO IS NULL
                    AND STATUS = 'CO'
                    ORDER BY DT_INCL DESC
            """)
            return cursor.fetchall()


def update_task(task_id, new_desc):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE TASK SET DS_TASK = ? WHERE ID = ?", (new_desc, task_id))
        conn.commit()
        conn.close()
        
def update_status_task(task_id, status):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE TASK SET STATUS = ? WHERE ID = ?", (status, task_id))
            conn.commit()
        

def delete_task(task_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE TASK SET DT_EXCLUSAO = ? WHERE ID = ?", (datetime.now(), task_id))
        conn.commit()
        conn.close()

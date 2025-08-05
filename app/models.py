from .database import get_connection
from datetime import datetime

def insert_task(desc, categoria, dt_vencimento=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO TASK (DS_TASK, DT_INCL, DT_VENCIMENTO, STATUS, CATEGORIA)
        VALUES (?, CURRENT_TIMESTAMP, ?, 'IN', ?)
    ''', (desc, dt_vencimento, categoria))
    conn.commit()
    conn.close()

def get_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ID, DS_TASK FROM TASK WHERE DT_EXCLUSAO IS NULL")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def update_task(task_id, new_desc):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE TASK SET DS_TASK = ? WHERE ID = ?", (new_desc, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE TASK SET DT_EXCLUSAO = ? WHERE ID = ?", (datetime.now(), task_id))
    conn.commit()
    conn.close()

import sqlite3

from main.constant.db_constant import book_db
from main.constant.sql_constant import create_book_sql, select_max_book_id_sql
from main.data.service.retrieve_book_service import get_book_by_id


def create_book(book_id, title):
    # Connect to SQLite database
    conn = sqlite3.connect(book_db)
    # Create a cursor object
    cursor = conn.cursor()
    try:
        cursor.execute(create_book_sql, (book_id, title))
        conn.commit()
        result = get_book_by_id(book_id)
        return result
    except sqlite3.Error as e:
        print(f"Error occurred: {e}")
    finally:
        conn.close()


def get_max_id():
    # Connect to SQLite database
    conn = sqlite3.connect(book_db)
    # Create a cursor object
    cursor = conn.cursor()
    cursor.execute(select_max_book_id_sql)
    result = cursor.fetchone()
    conn.close()
    if result and result[0] is not None:
        return result[0] + 1
    else:
        return 1


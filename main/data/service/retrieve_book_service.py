import sqlite3

from main.constant.db_constant import book_db
from main.constant.sql_constant import select_book_by_book_id_sql, select_books_sql
from main.data.entity.book import Book


def get_book_by_id(book_id):
    conn = sqlite3.connect(book_db)
    cursor = conn.cursor()
    try:
        cursor.execute(select_book_by_book_id_sql, (book_id,))
        result = cursor.fetchone()
        if result is not None:
            return Book(result[0], result[1])
    except sqlite3.Error as e:
        print(f"Error occurred: {e}")
        result = None
    finally:
        # Close the connection
        conn.close()
    return result


def get_books():
    conn = sqlite3.connect(book_db)
    cursor = conn.cursor()
    try:
        cursor.execute(select_books_sql)
        result = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error occurred: {e}")
        result = None
    finally:
        # Close the connection
        conn.close()

    book_list = []
    if result is not None:
        for item in result:
            book = Book(item[0], item[1])
            book_list.append(book.to_json())
    return book_list

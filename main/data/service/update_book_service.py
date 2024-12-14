import json
import sqlite3

from flask import Response

from main.constant.api_status_constant import indent_level, content_type, success_http_code, status_success, \
    status_error, bad_request_http_code, book_not_found
from main.constant.db_constant import book_db
from main.constant.sql_constant import update_book_sql
from main.data.entity.api_response_payload import ApiResponsePayload
from main.data.service.retrieve_book_service import get_book_by_id


def update_book(book_id, title):
    conn = sqlite3.connect(book_db)
    cursor = conn.cursor()
    book = get_book_by_id(book_id)
    if book is None:
        response = json.dumps(ApiResponsePayload(status_error, book_not_found).to_json(), indent=indent_level)
        return Response(response, bad_request_http_code, content_type=content_type)
    try:
        cursor.execute(update_book_sql, (title, book_id))
        conn.commit()
        updated_book = get_book_by_id(book_id)
        response = json.dumps(ApiResponsePayload(status_success, updated_book.to_json()).to_json(), indent=indent_level)
        return Response(response, success_http_code, content_type=content_type)
    except sqlite3.Error as e:
        print(f"Error occurred: {e}")
    finally:
        conn.close()


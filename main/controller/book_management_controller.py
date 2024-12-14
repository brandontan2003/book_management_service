import json
import sqlite3

from flask import Flask, request, Response
from main.constant.api_status_constant import *
from main.constant.db_constant import book_db
from main.data.entity.api_response_payload import ApiResponsePayload
from main.data.service.create_book_service import get_max_id, create_book
from main.data.service.retrieve_book_service import get_book_by_id, get_books
from main.data.service.update_book_service import update_book

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


# Retrieve all the books in the DB
@app.route(api_v1 + retrieve_books_url, methods=[get])
def retrieve_books_controller():
    response = json.dumps(ApiResponsePayload(status_success, get_books()).to_json(), indent=indent_level)
    return Response(response, success_http_code, content_type=content_type)


# Retrieve Book By BookId
@app.route(api_v1 + retrieve_book_url, methods=[get])
def retrieve_book_controller(book_id):
    book = get_book_by_id(book_id)
    if book is None:
        response = json.dumps(ApiResponsePayload(status_success, {}).to_json(), indent=indent_level)
    else:
        response = json.dumps(ApiResponsePayload(status_success, book.to_json()).to_json(), indent=indent_level)
    return Response(response, success_http_code, content_type=content_type)


# Create Book
@app.route(api_v1 + create_book_url, methods=[post])
def create_book_controller():
    try:
        book_title = request.json["book_title"]
        max_id = get_max_id()
        book = create_book(max_id, book_title)
        response = json.dumps(ApiResponsePayload(status_success, book.to_json()).to_json(), indent=indent_level)
        return Response(response, success_http_code, content_type=content_type)
    except:
        response = json.dumps(ApiResponsePayload(status_error, "something went wrong").to_json(), indent=indent_level)
        return Response(response, bad_request_http_code, content_type=content_type)


# Update Book
@app.route(api_v1 + update_book_url, methods=[put])
def update_book_controller():
    try:
        book_id = request.json["book_id"]
        book_title = request.json["book_title"]
        return update_book(book_id, book_title)
    except:
        response = json.dumps(ApiResponsePayload(status_error, "something went wrong").to_json(), indent=indent_level)
        return Response(response, bad_request_http_code, content_type=content_type)


def create_table():
    conn = sqlite3.connect(book_db)
    cursor = conn.cursor()
    create_book_table_sql = '''
    CREATE TABLE IF NOT EXISTS book (
        book_id INTEGER PRIMARY KEY,
        title TEXT NOT NULL
    );
    '''
    # Step 4: Execute the CREATE TABLE script
    cursor.execute(create_book_table_sql)
    conn.commit()
    conn.close()
    print("Table created successfully!")


if __name__ == '__main__':
    create_table()
    app.run(host='0.0.0.0', port=8080)

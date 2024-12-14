import json
import sqlite3
import unittest
from unittest.mock import patch, MagicMock

from flask import Response

from main.constant.api_status_constant import status_success, content_type, indent_level, success_http_code, \
    status_error, bad_request_http_code, book_not_found
from main.constant.sql_constant import select_book_by_book_id_sql, update_book_sql
from main.data.entity.api_response_payload import ApiResponsePayload
from main.data.entity.book import Book
from main.data.service.update_book_service import update_book


class TestUpdateBook(unittest.TestCase):
    def setUp(self):
        # Mock database connection and cursor
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.patcher = patch('sqlite3.connect', return_value=self.mock_conn)
        self.mock_connect = self.patcher.start()
        self.mock_conn.cursor.return_value = self.mock_cursor

    def tearDown(self):
        # Stop patching after each test
        self.patcher.stop()

    def test_update_book_success(self):
        book_id = 1
        title = "Updated Book"
        self.mock_cursor.fetchone.return_value = (book_id, title)

        actual_output = update_book(book_id, title)

        self.assertEqual(self.mock_cursor.execute.call_count, 3)
        self.mock_cursor.execute.assert_any_call(select_book_by_book_id_sql, (book_id,))
        self.mock_cursor.execute.assert_any_call(update_book_sql, (title, book_id))
        self.mock_cursor.execute.assert_any_call(select_book_by_book_id_sql, (book_id,))
        self.mock_conn.commit.assert_called_once()

        expected_updated_book = Book(book_id, title)
        response = json.dumps(ApiResponsePayload(status_success, expected_updated_book.to_json()).to_json(),
                              indent=indent_level)
        expected_output = Response(response, success_http_code, content_type=content_type)

        self.assertEqual(expected_output.get_data(as_text=True), actual_output.get_data(as_text=True))
        self.assertEqual(success_http_code, actual_output.status_code)

    @patch('main.data.service.update_book_service.get_book_by_id')
    def test_update_book_database_error(self, mock_get_book_by_id):
        book_id = 1
        title = "Updated Book"

        mock_get_book_by_id.return_value = {'id': book_id, 'title': title}
        self.mock_cursor.execute.side_effect = sqlite3.Error("Mocked database error")

        actual_output = update_book(book_id, title)

        self.assertEqual(self.mock_cursor.execute.call_count, 1)
        self.mock_cursor.execute.assert_any_call(update_book_sql, (title, book_id))
        self.mock_conn.commit.assert_not_called()
        self.assertIsNone(actual_output)

    def test_update_book_no_record_error(self):
        book_id = 1
        title = "Updated Book"
        self.mock_cursor.fetchone.return_value = None

        actual_output = update_book(book_id, title)

        self.assertEqual(self.mock_cursor.execute.call_count, 1)
        self.mock_cursor.execute.assert_called_once_with(select_book_by_book_id_sql, (book_id,))

        response = json.dumps(ApiResponsePayload(status_error, book_not_found).to_json(), indent=indent_level)
        expected_output = Response(response, bad_request_http_code, content_type=content_type)

        self.assertEqual(expected_output.get_data(as_text=True), actual_output.get_data(as_text=True))
        self.assertEqual(bad_request_http_code, actual_output.status_code)

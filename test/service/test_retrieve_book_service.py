import sqlite3
import unittest
from unittest.mock import patch, MagicMock

from main.constant.sql_constant import select_book_by_book_id_sql, select_books_sql
from main.data.service.retrieve_book_service import get_books, get_book_by_id


class TestRetrieveBook(unittest.TestCase):
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

    def test_retrieve_all_books_empty_success(self):
        actual_output = get_books()

        self.assertEqual(self.mock_cursor.execute.call_count, 1)
        self.mock_cursor.execute.assert_called_once_with(select_books_sql)
        self.assertEqual(list(), actual_output)

    def test_retrieve_all_books_database_error(self):
        self.mock_cursor.execute.side_effect = sqlite3.Error("Mocked database error")
        actual_output = get_books()

        self.assertEqual(self.mock_cursor.execute.call_count, 1)
        self.mock_cursor.execute.assert_called_once_with(select_books_sql)
        self.assertEqual(list(), actual_output)

    def test_retrieve_all_books_non_empty_success(self):
        self.mock_cursor.fetchall.return_value = [(1, "The Lord of the Rings"), (2, "A Tale of Two Cities")]
        actual_output = get_books()

        self.assertEqual(self.mock_cursor.execute.call_count, 1)
        self.mock_cursor.execute.assert_called_once_with(select_books_sql)

        expected_output = [
            {
                "book_id": 1,
                "title": "The Lord of the Rings"
            },
            {
                "book_id": 2,
                "title": "A Tale of Two Cities"
            }
        ]

        self.assertEqual(expected_output, actual_output)

    def test_retrieve_one_book_empty_success(self):
        book_id = 1
        self.mock_cursor.fetchone.return_value = None
        actual_output = get_book_by_id(book_id)

        self.assertEqual(self.mock_cursor.execute.call_count, 1)
        self.mock_cursor.execute.assert_called_once_with(select_book_by_book_id_sql, (book_id,))
        self.assertEqual(None, actual_output)

    def test_retrieve_one_book_database_error(self):
        book_id = 1
        self.mock_cursor.execute.side_effect = sqlite3.Error("Mocked database error")
        actual_output = get_book_by_id(book_id)

        self.assertEqual(self.mock_cursor.execute.call_count, 1)
        self.mock_cursor.execute.assert_called_once_with(select_book_by_book_id_sql, (book_id,))
        self.assertEqual(None, actual_output)

    def test_retrieve_one_book_non_empty_success(self):
        book_id = 1
        title = "The Lord of the Rings"
        self.mock_cursor.fetchone.return_value = (book_id, title)
        actual_output = get_book_by_id(book_id)

        self.assertEqual(self.mock_cursor.execute.call_count, 1)
        self.mock_cursor.execute.assert_called_once_with(select_book_by_book_id_sql, (book_id,))

        expected_output = {
            "book_id": 1,
            "title": "The Lord of the Rings"
        }

        self.assertEqual(expected_output, actual_output.to_json())

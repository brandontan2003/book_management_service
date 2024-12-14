import sqlite3
import unittest
from unittest.mock import patch, MagicMock

from main.constant.sql_constant import create_book_sql, select_book_by_book_id_sql, select_max_book_id_sql
from main.data.service.create_book_service import create_book, get_max_id


class TestCreateBook(unittest.TestCase):
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

    def test_create_book_success(self):
        book_id = 1
        title = "Test Book"
        self.mock_cursor.fetchone.return_value = (book_id, title)

        result = create_book(book_id, title)

        self.assertEqual(self.mock_cursor.execute.call_count, 2)
        self.mock_cursor.execute.assert_any_call(create_book_sql, (book_id, title))
        self.mock_cursor.execute.assert_any_call(select_book_by_book_id_sql, (book_id,))
        self.mock_cursor.fetchone.assert_called_once()
        self.mock_conn.commit.assert_called_once()
        self.assertEqual({'book_id': book_id, 'title': title}, result.to_json())

    def test_create_book_error(self):
        self.mock_cursor.execute.side_effect = sqlite3.Error("Mocked database error")
        book_id = 1
        title = "Test Book"
        result = create_book(book_id, title)

        self.mock_cursor.execute.assert_called_once_with(create_book_sql, (book_id, title))
        self.assertIsNone(result)

    def test_get_max_id_with_existing_record_success(self):
        book_id = 1
        self.mock_cursor.fetchone.return_value = (book_id,)

        result = get_max_id()

        self.assertEqual(self.mock_cursor.execute.call_count, 1)
        self.mock_cursor.execute.assert_any_call(select_max_book_id_sql)
        self.mock_cursor.fetchone.assert_called_once()
        self.assertEqual(2, result)

    def test_get_max_id_with_no_record_success(self):
        self.mock_cursor.fetchone.return_value = (None,)

        result = get_max_id()

        self.assertEqual(self.mock_cursor.execute.call_count, 1)
        self.mock_cursor.execute.assert_any_call(select_max_book_id_sql)
        self.mock_cursor.fetchone.assert_called_once()
        self.assertEqual(1, result)

import json
import unittest
from unittest.mock import patch, MagicMock

from flask import Response

from main.constant.api_status_constant import api_v1, retrieve_books_url, create_book_url, content_type, \
    update_book_url, success_http_code, status_success, indent_level
from main.controller.book_management_controller import app
from main.data.entity.api_response_payload import ApiResponsePayload
from main.data.entity.book import Book

controller_directory = "main.controller.book_management_controller."


class TestBookManagementController(unittest.TestCase):
    def setUp(self):
        # Creates a test client for the Flask app
        self.client = app.test_client()
        self.client.testing = True

        # Mock database connection and cursor
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.patcher = patch('sqlite3.connect', return_value=self.mock_conn)
        self.mock_connect = self.patcher.start()
        self.mock_conn.cursor.return_value = self.mock_cursor

    def tearDown(self):
        # Stop patching after each test
        self.patcher.stop()

    def test_retrieve_all_books_non_empty(self):
        mock_books = [
            {
                "book_id": 1,
                "title": "The Lord of the Rings"
            },
            {
                "book_id": 2,
                "title": "A Tale of Two Cities"
            },
            {
                "book_id": 3,
                "title": "The Lord of the Rings"
            }
        ]

        with patch(controller_directory + 'get_books', return_value=mock_books):
            # Simulate GET request without query parameters
            response = self.client.get(api_v1 + retrieve_books_url)
            self.assertEqual(response.status_code, 200)
            print(response.json)

            # Expected mock response
            expected_output = {
                "status": "SUCCESS",
                "result": mock_books
            }

            self.assertEqual(response.json, expected_output)

    def test_retrieve_all_books_empty(self):
        # Simulate GET request without query parameters
        response = self.client.get(api_v1 + retrieve_books_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "status": "SUCCESS",
            "result": []
        })

    def test_retrieve_a_book_non_empty(self):
        mock_book = Book(1, "The Lord of the Rings")

        with patch(controller_directory + 'get_book_by_id', return_value=mock_book):
            # Simulate GET request without query parameters
            response = self.client.get(api_v1 + "/retrieve/1")
            self.assertEqual(response.status_code, 200)

            # Expected mock response
            expected_output = {
                "status": "SUCCESS",
                "result": mock_book.to_json()
            }

            self.assertEqual(response.json, expected_output)

    @patch(controller_directory + 'get_book_by_id')
    def test_retrieve_a_book_empty(self, mock_get_book_by_id):
        mock_get_book_by_id.return_value = None

        response = self.client.get(api_v1 + "/retrieve/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "status": "SUCCESS",
            "result": {}
        })

    def test_create_book_success(self):
        create_book = Book(2, "The Lord of the Rings")
        request_body = {
            "book_title": "The Lord of the Rings"
        }

        with patch(controller_directory + 'get_max_id', return_value=1) and patch(controller_directory + 'create_book',
                                                                                  return_value=create_book):
            response = self.client.post(api_v1 + create_book_url, json=request_body)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {
                "status": "SUCCESS",
                "result": {
                    "book_id": 2,
                    "title": "The Lord of the Rings"
                }
            })

    def test_update_book_success(self):
        request_body = {
            "book_id": 2,
            "book_title": "The Lord of the Rings"
        }

        response = json.dumps(ApiResponsePayload(status_success, request_body).to_json(), indent=indent_level)
        expected_response = Response(response, success_http_code, content_type=content_type)

        with patch(controller_directory + 'update_book', return_value=expected_response):
            response = self.client.put(api_v1 + update_book_url, json=request_body)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, expected_response.json)

# Book Management Service

## Description
This is a simple CRUD application that uses the REST APIs for Books. It uses the Flask Framework for the API and the data is stored using SQLite.

## Features
- [Add a new book.](#add-a-book)
- [Retrieve details of a book.](#retrieve-a-book)
- [Retrieve all the books details.](#retrieve-books)
- [Update details of an existing book.](#update-a-book)

## Technologies Used
- **Flask**: A lightweight WSGI web application framework.
- **SQLite**: A self-contained, high-reliability, embedded, full-featured SQL database engine.
- **Python**: The core programming language for building the API.

## Database Schema

### Table: `book`
| Column           | Type    | Constraints        |
|------------------|---------|--------------------|
| `book_id`        | INTEGER | PRIMARY KEY        |
| `title`          | TEXT    | NOT NULL           |

## Setup Instructions
1. Download Python 3.11 
    ```
    www.python.org/downloads
    ```
2. Install all the dependencies in the `requirements.txt` file
3. Open the IDE terminal and run the below command
    ```
   pip install -r requirements.txt
    ```
4. Run the application:
    ``` python book_management_controller.py ```

## Running on Docker 
1. Open terminal
2. Run ``docker compose down``
3. Run ``docker compose up -d --build``

## API Endpoints

### Add a Book
**POST** `/api/v1/create`

#### Request Body
```json
{
    "book_title": "The Lord of the Rings"
}
```

#### Response
- **201 Created**
- **400 Bad Request** (if required fields are missing)

#### Success Sample Response
```json
{
    "status": "SUCCESS",
    "result": {
        "book_id": 3,
        "title": "The Lord of the Rings"
    }
}
```

#### Failure Sample Response
```json
{
    "status": "ERROR",
    "result": "Something Went Wrong"
}
```

### Retrieve a Book
**GET** `/api/v1/retrieve/<book_id>`

#### Response
- **200 OK**
- **200 Not Found** (if the book does not exist)

#### Non-empty Sample Response
```json
{
    "status": "SUCCESS",
    "result": {
        "book_id": 3,
        "title": "The Lord of the Rings"
    }
}
```

#### Empty Sample Response
```json
{
    "status": "SUCCESS",
    "result": {}
}
```

### Retrieve Books
**GET** `/api/v1/retrieve`

#### Response
- **200 OK**
- **200 Not Found** (if all the books does not exist)

#### Non-empty Sample Response
```json
{
    "status": "SUCCESS",
    "result": [
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
}
```

#### Empty Sample Response
```json
{
    "status": "SUCCESS",
    "result": []
}
```

### Update a Book
**PUT** `/api/v1/update`

#### Request Body
```json
{
    "book_id": "2",
    "book_title": "A Tale of Two Cities"
}
```

#### Response
- **200 OK**
- **400 Bad Request** (if the book does not exist)

#### Success Sample Response
```json
{
    "status": "SUCCESS",
    "result": {
        "book_id": 2,
        "title": "The Lord of the Rings"
    }
}
```

#### Failure Sample Response
```json
{
    "status": "ERROR",
    "result": "Book Not Found"
}
```

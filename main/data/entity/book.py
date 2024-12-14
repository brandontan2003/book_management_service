class Book:
    def __init__(self, book_id, title):
        self.book_id = book_id
        self.title = title

    def set_title(self, title):
        self.title = title

    def get_title(self):
        return self.title

    def get_book_id(self):
        return self.book_id

    def to_json(self):
        return {
            "book_id": self.book_id,
            "title": self.title
        }

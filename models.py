import json

class Books:
    def __init__(self):
        try:
            with open("books.json", "r") as f:
                self.books = json.load(f)
        except FileNotFoundError:
            self.books = []

    def all(self):
        return self.books

    def get(self, id):
        return self.books[id]
    
    def count(self):
         return len(self.books)

    def create(self, data):
        data.pop('csrf_token')
        self.books.append(data)

    def create_api(self, data):
        self.books.append(data)

    def save_all(self):
        with open("books.json", "w") as f:
            json.dump(self.books, f)

    def update(self, id, data):
        data.pop('csrf_token')
        self.books[id] = data
        self.save_all()
    
    def update_api(self, id, data):
        self.books[id] = data
        self.save_all()

    def delete(self, id):
        book = self.get(id)
        if book:
            self.books.remove(book)
            self.save_all()
            return True
        return False

books = Books()
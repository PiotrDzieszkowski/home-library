from flask import Flask, request, render_template, redirect, url_for, jsonify, abort, make_response

from forms import BooksForm
from models import books

app = Flask(__name__)
app.config["SECRET_KEY"] = "ksiazkimlodego"

@app.route("/books/", methods=["GET", "POST"])
def books_list():
    form = BooksForm()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            books.create(form.data)
            books.save_all()
        return redirect(url_for("books_list"))

    return render_template("books.html", form=form, books=books.all(), error=error, count=books.count())


@app.route("/books/<int:book_id>", methods=["GET", "POST", "DELETE"])
def book_details(book_id):
    book = books.get(book_id - 1)
    form = BooksForm(data=book)
    if request.method == "POST":
        if form.validate_on_submit():
            books.update(book_id - 1, form.data)
        return redirect(url_for("books_list"))
    return render_template("book.html", form=form, book_id=book_id)


@app.route("/api/v1/books/", methods=["GET"])
def books_list_api_v1():
    return jsonify(books.all())


@app.route("/api/v1/books/", methods=["POST"])
def create_book():
    if not request.json or not 'title' in request.json or not 'author' in request.json:
        abort(400)
    book = {
        'title': request.json['title'],
        'author': request.json['author'],
        'categories': request.json.get('categories', 0),
        'pages': request.json.get('pages', 0),
        'year_published': request.json.get('year_published', 0),
        'read': False,
        'cover': request.json.get('cover', ""),
        'condition': request.json.get('condition', 0),
        'last_read': request.json.get('last_read', ""),
    }
    books.create_api(book)
    books.save_all()
    return jsonify({'book': book}), 201


@app.route("/api/v1/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    if book_id < 1 or book_id > books.count():
        abort(404)
    book = books.get(book_id-1)
    return jsonify({"book": book})


@app.route("/api/v1/books/<int:book_id>", methods=['DELETE'])
def delete_book(book_id):
    if book_id < 1 or book_id > books.count():
        abort(404)
    result = books.delete(book_id-1)
    return jsonify({'result': result})


@app.route("/api/v1/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    if book_id < 1 or book_id > books.count():
        abort(404)
    if not request.json:
        abort(400)
    book = books.get(book_id-1)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'author' in data and not isinstance(data.get('author'), str),
        'categories' in data and not isinstance(data.get('categories'), str),
        'pages' in data and not isinstance(data.get('pages'), int),
        'year_published' in data and not isinstance(data.get('year_published'), int),
        'read' in data and not isinstance(data.get('read'), bool),
        'cover' in data and not isinstance(data.get('cover'), str),
        'condition' in data and not isinstance(data.get('condition'), str),
        'last_read' in data and not isinstance(data.get('last_read'), str)
    ]):
        abort(400)
    book = {
        'title': data.get('title', book['title']),
        'author': data.get('author', book['author']),
        'categories': data.get('categories', book['categories']),
        'pages': data.get('pages', book['pages']),
        'year_published': data.get('age', book['year_published']),
        'read': data.get('read', book['read']),
        'cover': data.get('cover', book['cover']),
        'condition': data.get('readings', book['condition']),
        'last_read': data.get('last_read', book['last_read']),
    }
    books.update_api(book_id-1, book)
    return jsonify({'book': book})


#errorhandlers
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)


if __name__ == "__main__":
    app.run(debug=True)
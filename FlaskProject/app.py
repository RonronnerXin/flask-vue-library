from email.policy import default

from flask import Flask, request
from extension import db
from models import Book
from flask_cors import CORS
from flask.views import MethodView
app = Flask(__name__)
CORS().init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.cli.command()
def create():
    db.drop_all()
    db.create_all()
    Book.init_db()

class BookApi(MethodView):
    def get(self, book_id):
        if not book_id:
            books: [Book] = Book.query.all()
            results = [
                {
                    'id': book.id,
                    'book_name': book.book_name,
                    'book_type': book.book_type,
                    'book_price': book.book_price,
                    'book_number': book.book_number,
                    'book_publisher': book.book_publisher,
                    'author': book.author,
                } for book in books
            ]
            return {
                'status': "success",
                'message': "数据查询成功",
                'results': results
            }
        books: [Book] = Book.query.get(book_id)
        results = [
            {
                'id': book.id,
                'book_name': book.book_name,
                'book_type': book.book_type,
                'book_price': book.book_price,
                'book_number': book.book_number,
                'book_publisher': book.book_publisher,
                'author': book.author,
            } for book in books
        ]
        return {
            'status': "success",
            'message': "数据查询成功",
            'results': results
        }

    def post(self):
        form = request.json
        book = Book()
        book.book_number = form.get('book_number')
        book.book_name = form.get('book_name')
        book.book_type = form.get('book_type')
        book.author = form.get('author')
        book.book_price = form.get('book_price')
        book.book_publisher = form.get('book_publisher')
        db.session.add(book)
        db.session.commit()
        return{
            'status': "success",
            'message': '数据添加成功'
        }

    def put(self, book_id):
        book: Book = Book.query.get(book_id)
        book.book_name = request.json.get('book_name')
        book.book_type = request.json.get('book_type')
        book.book_price = request.json.get('book_price')
        book.book_number = request.json.get('book_number')
        book.book_publisher = request.json.get('book_publisher')
        book.author = request.json.get('author')
        db.session.commit()
        return {
            'status': "success",
            'message': "数据修改成功"
        }

    def delete(self, book_id):
        book = Book.query.get(book_id)
        db.session.delete(book)
        db.session.commit()
        return {
            'status': "success",
            'message': '数据删除成功'
        }

book_view = BookApi().as_view('book_api')
app.add_url_rule('/books/', defaults={'book_id': None}, view_func=book_view, methods=['GET', ])
app.add_url_rule('/books', view_func=book_view, methods=['POST', ])
app.add_url_rule('/books/<int:book_id>/', view_func=book_view, methods=['GET', 'PUT', 'DELETE'])


if __name__ == '__main__':
    app.run()

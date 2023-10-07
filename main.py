from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

'''
On MacOS type:
pip3 install -r requirements.txt

'''

app = Flask(__name__)

# Configure DB
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books-database.db"
db = SQLAlchemy()
db.init_app(app)


# Create table
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=False, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


# with app.app_context():
#     db.create_all()

# # Create a record
# with app.app_context():
#     new_book = Book(title="Harry Potter", author="J. K. Rowling", rating=9.3)
#     # new_book = Book(title="Harry Potter", author="J. K. Rowling", rating=9.3)
#     db.session.add(new_book)
#     db.session.commit()
#

# all_books = []


@app.route('/')
def home():
    # read all books
    all_books = db.session.query(Book).all()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # create a record
        new_book = Book(title=request.form['name'],
                        author=request.form['author'],
                        rating=request.form['rating'])
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")


@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit(index):
    book = db.session.query(Book).where(Book.id == index)
    print(book)
    return render_template("edit.html", book=book)


# @app.route("/delete", methods=["GET", "POST"])
# def delete():
#     return render_template("delete.html")


if __name__ == "__main__":
    app.run(debug=True)

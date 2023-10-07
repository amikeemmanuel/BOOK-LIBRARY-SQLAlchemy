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
    if request.method == "POST":
        # create a record
        book_to_update = db.get_or_404(Book, index)
        book_to_update.rating = request.form['rating']
        db.session.commit()
        return redirect(url_for('home'))

    all_books = db.session.query(Book).all()
    for book in all_books:
        if book.id == index:
            return render_template("edit.html", title=book.title, rating=book.rating)
    return render_template("edit.html")


@app.route("/<int:index>", methods=["GET", "POST"])
def delete(index):
    book_to_delete = db.get_or_404(Book, index)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

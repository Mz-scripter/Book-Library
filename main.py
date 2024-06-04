from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "asdf67890"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///all-books-database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)
Bootstrap(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(85), unique=True, nullable=False)
    rating = db.Column(db.Float, nullable=False)
###This commented part creates the table in the database, if you are using the database that comes with my code, leave it commented, else create a new table, uncomment that bit so the 
###table is created, then comment it out. If you leave it uncommented, it will cause an error since you would be trying to create a table that already exists.
# with app.app_context():
#     db.create_all()
#     db.session.commit()


class AddForm(FlaskForm):
    book_name = StringField('Book Name', validators=[DataRequired()])
    author = StringField('Book Author', validators=[DataRequired()])
    rate = FloatField('Rating', validators=[DataRequired()])
    submit = SubmitField('Add Book')

class EditForm(FlaskForm):
    new_rating = FloatField("New Rating", validators=[DataRequired()])
    submit = SubmitField("Change Rating")

@app.route('/')
def home():
    with app.app_context():
        books = db.session.query(Book).all()
        return render_template('index.html', books=books)
        db.session.commit()
@app.route('/delete')
def delete():
    with app.app_context():
        book_to_delete_id = request.args.get('id')
        book_to_delete = db.session().query(Book).get(book_to_delete_id)
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect(url_for('home'))
    


@app.route("/add", methods=['GET', 'POST'])
def add():
    form = AddForm()
    if request.method == 'POST':
        with app.app_context():
            new_book = Book(title=form.book_name.data, author=form.author.data, rating=form.rate.data)
            db.session.add(new_book)
            db.session.commit()
            return redirect(url_for('home'))

    return render_template('add.html', form=form)

@app.route("/edit", methods=["GET", "POST"])
def edit():
    form = EditForm()
    if request.method == "POST":
        with app.app_context():
            book_to_update_id = request.form['id']
            book_to_update = db.session().query(Book).get(book_to_update_id)
            book_to_update.rating = form.new_rating.data
            db.session.commit()
            return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = Book.query.get(book_id)
    return render_template('edit.html', book=book_selected, form=form)    


if __name__ == "__main__":
    app.run(debug=True)





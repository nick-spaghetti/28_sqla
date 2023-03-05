"""Blogly application."""

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)
connect_db(app)
db.create_all()


@app.route('/')
def home_page():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('index.html', users=users)


@app.route('/', methods=['post'])
def create_user():
    '''shows home page'''
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None
    )
    db.session.add(new_user)
    db.session.commit()
    return redirect(f'/{new_user.id}')


@app.route("/<int:user_id>")
def find_user(user_id):
    '''show details about a single pet'''
    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user)


@app.route('/<int:user_id>/edit')
def users_edit(user_id):
    """Show a form to edit an existing user"""

    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)


@app.route('/<int:user_id>/edit', methods=["post"])
def users_update(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url'] or None

    db.session.add(user)
    db.session.commit()

    return redirect("/")


@app.route('/<int:user_id>/delete', methods=["post"])
def users_destroy(user_id):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/")

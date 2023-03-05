"""Blogly application."""

from flask import Flask, redirect, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)
connect_db(app)
db.create_all()

# root


@app.route('/')
def root():
    return redirect('/homepage')


@app.route('/homepage')
def home_page():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("posts/homepage.html", posts=posts)

# user routs


@app.route('/users')
def users_page():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('/users/index.html', users=users)


@app.route('/users/new')
def create_user():
    '''shows new user page'''
    return render_template('/users/new_user.html')


@app.route('/users/new', methods=['post'])
def new_user_form():
    '''shows new user form page'''
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None
    )
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')


@app.route("/users/<int:user_id>")
def find_user(user_id):
    '''show details about a single pet'''
    user = User.query.get_or_404(user_id)
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('/users/details.html', user=user, posts=posts)


@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """Show a form to edit an existing user"""

    user = User.query.get_or_404(user_id)
    return render_template('/users/edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["post"])
def users_update(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url'] or None

    db.session.add(user)
    db.session.commit()

    return redirect("/")


@app.route('/users/<int:user_id>/delete', methods=["post"])
def delete_user(user_id):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

# post routes


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/post_details.html', post=post)


@app.route('/users/<int:user_id>/posts/new')
def posts_new_form(user_id):
    """Show a form to create a new post for a specific user"""

    user = User.query.get_or_404(user_id)
    return render_template('/posts/new_post.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
    """Handle form submission for creating a new post for a specific user"""

    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user)

    db.session.add(new_post)
    db.session.commit()
    # flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit_post.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=['post'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    return redirect(f'/users/{post.user_id}')


@app.route('/posts/<int:post_id>/delete', methods=['post'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{post.user_id}')

# tag routes


@app.route('/tags')
def tag_root():
    tags = Tag.query.all()
    return render_template('tags/tag_index.html', tags=tags)


@app.route('/tags/new')
def new_tag_form():
    posts = Post.query.all()
    return render_template('tags/new_tag.html', posts=posts)


@app.route('/tags/new', methods=['post'])
def new_tag():
    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).order_by(
        Post.created_at.desc()).limit(5).all()
    new_tag = Tag(name=request.form['name'], posts=posts)
    db.session.add(new_tag)
    db.session.commit()
    flash(f'tag {new_tag.name} added')
    return redirect('/tags')


@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('/tags/tag_details.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('/tags/edit_tag.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=['post'])
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist('posts')]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()
    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')


@app.route('/tags/<int:tag_id>/delete', methods=['post'])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')

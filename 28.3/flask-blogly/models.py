"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
default_image_url = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    '''user model'''
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    image_url = db.Column(db.Text, nullable=True, default=default_image_url)

    post = db.relationship("Post", backref="user",
                           cascade="all, delete-orphan")

    @property
    def full_name(self):
        '''return full name of user'''
        return f'{self.first_name} {self.last_name}'

    def __repr__(self):
        '''show info about user'''
        u = self
        return f"<User id = {u.id} name = {u.first_name} {u.last_name}>"

    def greet(self):
        '''greet using name'''
        return f"Hi, {self.first_name}"


class Post(db.Model):
    '''model for blog posts'''
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        '''show info about user'''
        p = self
        return f"<id: {p.id} title: {p.title} content: {p.content} created_at: {p.created_at} user_id: {p.user.id}>"

    @property
    def date_time(self):
        return self.created_at.strftime('%a %b %-d %Y, %-I:%M %p')
# db.create_all()


class Tag(db.Model):
    '''model for tags'''
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=True, unique=True)

    # post_id = db.relationship('Post', backref='tag')

    posts = db.relationship(
        'Post',
        secondary="posts_tags",
        # cascade="all,delete",
        backref="tags",
    )


class PostTag(db.Model):
    '''model for tags'''
    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey(
        'tags.id'), primary_key=True)

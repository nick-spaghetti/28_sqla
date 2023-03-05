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
        return f"Hi, {self.first_name} {self.last_name}"
    posts = db.relationship("Post", backref="user",
                            cascade="all, delete-orphan")


class Post(db.Model):
    '''model for blog posts'''
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # user = db.relationship('User', backref='post')

    def __repr__(self):
        '''show info about user'''
        p = self
        return f"<id: {p.id} title: {p.title} content: {p.content} created_at: {p.created_at} user_id: {p.user.id}>"

    @property
    def date_time(self):
        return self.created_at.strftime('%a %b %-d %Y, %-I:%M %p')
# db.create_all()

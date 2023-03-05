"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
default_image_url = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    '''pet'''
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

# db.create_all()

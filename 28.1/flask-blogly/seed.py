'''seed file to make sample data for pets db'''
from models import User, db
from app import app

# create all tables
db.drop_all()
db.create_all()

# if table isn't empty, empty it
User.query.delete()

# add pets
john = User(first_name='John', last_name='Davidson')
michael = User(first_name='Michael', last_name='Smith')
devin = User(first_name='Devin', last_name='Osting')


# add new objects to session, so they'll persist
db.session.add(john)
db.session.add(michael)
db.session.add(devin)

# commit, otherwise this will never get saved
db.session.commit()

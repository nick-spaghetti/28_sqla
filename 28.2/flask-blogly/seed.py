'''seed file to make sample data for pets db'''
from models import User, db, Post
from app import app

# create all tables
db.drop_all()
db.create_all()

# if table isn't empty, empty it
User.query.delete()

# add users
john = User(first_name='John', last_name='Davidson')
michael = User(first_name='Michael', last_name='Smith')
devin = User(first_name='Devin', last_name='Osting')
nick = User(first_name='Nick', last_name='Salvetti')
pat = User(first_name='Patrick', last_name='Star')

p1 = Post(title='test', content='Laborum reprehenderit sit magna do irure exercitation consectetur. Nisi mollit nulla ipsum sit. Voluptate et amet fugiat magna minim et nostrud.', user_id='3')
p2 = Post(title='test', content='Aute aliqua officia est pariatur reprehenderit cupidatat ex fugiat dolore ad amet Lorem cupidatat magna. Tempor officia sint ex cupidatat cupidatat exercitation reprehenderit velit enim. Dolore adipisicing dolor nisi sit aliquip est culpa ipsum officia. Mollit id tempor adipisicing amet reprehenderit nostrud voluptate consectetur quis excepteur elit occaecat cupidatat.', user_id='2')
p3 = Post(title='test', content='Occaecat tempor irure aute do nisi id laboris in deserunt adipisicing ullamco est fugiat. Aliqua dolor aute ut pariatur laboris labore sit. Laborum occaecat eu pariatur laboris Lorem cupidatat nisi amet cillum quis cillum minim duis amet.', user_id='4')
p4 = Post(title='test', content='Do aute adipisicing nostrud in tempor quis irure eu. Aliqua occaecat nostrud laboris nostrud excepteur irure elit incididunt aute dolore aliqua. Laborum in ea occaecat laboris amet sint magna exercitation nostrud magna in velit quis. Mollit aliquip laboris magna dolor reprehenderit anim sunt proident. Officia id ad est fugiat ex qui Lorem laborum officia proident occaecat nostrud ullamco eiusmod. Ullamco fugiat magna dolor sint. Esse commodo qui pariatur labore sint officia ex exercitation ad eiusmod duis Lorem cillum.', user_id='1')
p5 = Post(title='test', content='Laborum non aute ex veniam velit irure exercitation et pariatur aliquip quis. Nostrud adipisicing mollit velit consectetur ipsum velit exercitation ut magna sit et mollit cupidatat. Magna ipsum eiusmod eiusmod quis laborum in culpa esse esse labore voluptate mollit irure excepteur. Ad voluptate quis nostrud labore nulla occaecat ipsum. Ea ipsum incididunt deserunt voluptate amet adipisicing consequat duis veniam cillum ad ipsum. Labore labore excepteur in culpa labore officia incididunt cupidatat dolor ut anim.', user_id='2')


# add new objects to session, so they'll persist
db.session.add_all([john, michael, devin, nick, pat])
db.session.add_all([p1, p2, p3, p4, p5])
# commit, otherwise this will never get saved
db.session.commit()

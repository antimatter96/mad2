from faker import Faker

fake = Faker()

from flask_security import SQLAlchemySessionUserDatastore
from sqlalchemy.sql.expression import func, select

user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)

new_users = []

for i in range(0, 20):
  email = fake.ascii_company_email()
  user_datastore.create_user(email=email, password='password' + str(i))

db.session.commit()

for i in range(0, 20):
  user_1 = db.session.query(User).order_by(func.random()).limit(1).first()
  new_post = Post(title=fake.sentence(nb_words=5), content="\n".join(fake.sentences()), hidden=fake.pybool(5), creator=user_1)
  db.session.add(new_post)

db.session.commit()

for i in range(0, 10):
  user_1 = db.session.query(User).order_by(func.random()).limit(1).first()
  user_2 = db.session.query(User).order_by(func.random()).limit(1).first()
  print(user_1.user_id, user_2.user_id)
  if user_1.user_id == user_2.user_id:
    continue
  if user_2 not in user_1.following:
    user_1.following.append(user_2)

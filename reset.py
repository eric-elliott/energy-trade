from soltrade import db, bcrypt
from soltrade.models import Group, User

db.drop_all()
db.create_all()

ucf = Group(groupname='UCF')
db.session.add(ucf)
db.session.commit()

# optional: fill in users
names = ["alice", "bob", "charlie"]

for name in names:
    hashed_password = bcrypt.generate_password_hash("password").decode('utf-8')
    user = User(username=name, email=name+"@example.com", password=hashed_password, group=ucf)
    db.session.add(user)
    db.session.commit()
from soltrade import db
from soltrade.models import Group

db.drop_all()
db.create_all()

ucf = Group(groupname='UCF')
db.session.add(ucf)
db.session.commit()
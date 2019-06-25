from datetime import datetime
from soltrade import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
        return User.query.get(int(user_id))

class Group(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        groupname = db.Column(db.String(22), unique=True, nullable=False)
        users = db.relationship('User', backref='group', lazy=True)

        def __repr__(self):
                return f"Group('{self.groupname}')"

class User(db.Model, UserMixin):
        # specifying user id
        id = db.Column(db.Integer, primary_key=True)
        # account information
        username = db.Column(db.String(22), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        image_file = db.Column(db.String(20), nullable=False, default='defaultpic.png')
        password = db.Column(db.String(60), nullable=False)
        # trading information
        total_energy_traded = db.Column(db.Numeric(12, 2), nullable=False, default=0.00)
        total_money_earned = db.Column(db.Numeric(12, 2), nullable=False, default=0.00)
        # relationship to "parent" group
        group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

        posts = db.relationship('Post', backref='author', lazy=True)

        def __repr__(self):
                return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(100), nullable=False)
        date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
        content = db.Column(db.Text, nullable=False)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

        def __repr__(self):
                return f"Post('{self.title}', '{self.date_posted}'"
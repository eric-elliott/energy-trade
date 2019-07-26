from datetime import datetime, timedelta
from soltrade import db, login_manager
from flask_login import UserMixin

# specifying the user loader
@login_manager.user_loader
def load_user(user_id):
        return User.query.get(int(user_id))

class Group(db.Model):
        # specifying id of group, along with a name
        id = db.Column(db.Integer, primary_key=True)
        groupname = db.Column(db.String(22), unique=True, nullable=False)
        # relationship to users in group
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
        # relationship to "parent" group, the grid
        group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
        # relationship to offers made
        offers = db.relationship('Offer', backref='seller', lazy=True)
        # relationship to request placed
        requests = db.relationship('Request', backref='placer', lazy=True)

        def __repr__(self):
                return f"User('{self.username}', '{self.email}', '{self.id}')"

class Offer(db.Model):
        # specifying id of offer made
        id = db.Column(db.Integer, primary_key=True)
        # energy offering
        energy_offer = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
        # suggested pricing
        suggested_price =  db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
        # boolean to track if offer is active
        active = db.Column(db.Boolean, unique=False, default=True)
        # relationship to user who made offer
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

        def __repr__(self):
                return f"Offer('{self.title}', '{self.date_posted}', '{self.endtime}')"

class Request(db.Model):
        # specifying id of request placed
        id = db.Column(db.Integer, primary_key=True)
        # amount of energy requested
        energy_requested = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
        # amount willing to pay
        payment = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
        # approved = db.Column(db.Boolean, unique=False, default=True)
        # relationship to parent - user making request
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

        def __repr__(self):
                return f"Request('{self.user_id}', '{self.energy_requested}')"

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
        # relationship to bids placed
        bids = db.relationship('Bid', backref='placer', lazy=True)
        # setting grid location
        loc = db.Column(db.Integer, nullable=False, default=1111)
        bus = db.Column(db.Integer, nullable=False, default=-1)

        def __repr__(self):
                return f"User('{self.username}', '{self.email}', '{self.id}')"

class Offer(db.Model):
        # specifying id of offer made
        id = db.Column(db.Integer, primary_key=True)
        # giving the offer a title and date
        title = db.Column(db.String(100), nullable=False)
        date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
        # bidding information
        energy_offer = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
        starting_bid = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
        top_bid = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
        # active_time = db.Column(db.Integer, nullable=False, default=1)
        endtime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow() + timedelta(days=1))
        # active = db.Column(db.Boolean, nullable=False, default=True)
        # relationship to bids placed on offer
        bids = db.relationship('Bid', backref='offer', lazy=True)
        # relationship to user who made offer
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

        def __repr__(self):
                return f"Offer('{self.title}', '{self.date_posted}', '{self.endtime}')"

        def is_active(self):
                if self.endtime > datetime.utcnow():
                        return True
                else:
                        return False

class Bid(db.Model):
        # specifying id of bid placed
        id = db.Column(db.Integer, primary_key=True)
        # amount of money bid
        amount = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
        time_placed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
        # relationship to parents - offer id being placed on, and user making bid
        offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'))
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

        def __repr__(self):
                return f"Bid('{self.user_id}', '{self.amount}', '{self.time_placed}')"

from app import db


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_name = db.Column(db.String(120), nullable=False)
    item_type = db.Column(db.String(8), nullable=False)
    customer = db.Column(db.String(32), nullable=True)
    prefix = db.Column(db.String(120), nullable=True)
    prefix_action = db.Column(db.String(16), nullable=False)
    suffix = db.Column(db.String(120), nullable=True)
    suffix_action = db.Column(db.String(16), nullable=False)
    delimiter = db.Column(db.String(4), nullable=True)
    delimiter_action = db.Column(db.String(16), nullable=False)
    delimiter_sample = db.Column(db.String(120), nullable=True)
    
    def __repr__(self):
        return 'Profile: {}'.format(self.profile_name)

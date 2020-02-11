from app import db

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)
    type = db.Column(db.String(8), nullable=False)
    prefix = db.Column(db.String(120), nullable=True)
    suffix = db.Column(db.String(120), nullable=True)
    delimiter = db.Column(db.String(4), nullable=True)
    action = db.Column(db.String(16), nullable=False)
    sample = db.Column(db.String(120), nullable=True)
    
    def __repr__(self):
        return 'Profile: {}'.format(self.name)
# third-party imports

# local imports
from app import db


class UserModel(db.Model):
    """
    Create an User table
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"<User: '{self.username}' '{self.email}' '{self.image_file}'>"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

from datetime import datetime

# third-party imports
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# local imports
from blog import db, login_manager, bcrypt


@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))


class UserModel(db.Model, UserMixin):
    """
    Create an User table
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password_hash = db.Column(db.String(60), nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, email, password, is_admin=False):
        self.username = username
        self.email = email
        self.password = password
        self.date_joined = datetime.now()

    def __repr__(self):
        return f"<User: '{self.username}' '{self.email}' '{self.image_file}'>"

    @property
    def password(self):
        """
        Prevent password from being accessed.
        """
        raise AttributeError('Password is not a readable attribute.')
    
    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Get the object's properties as a dictionary."""

        return {
            "username": self.username,
            "email": self.email,
            "date_joined": self.date_joined.strftime(DATE_FMT),
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

    @classmethod
    def return_all(cls):
        def to_dict(user):
            return {
                    'username': user.username,
                    'email': user.email,
                    }
        return {'users': list(map(lambda x: to_dict(x), cls.query.all()))}

    def get_reset_token(self, expire_secs=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expire_secs)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(cls, token):
        s = Serializer(current_app.config['SECRET_KEY'], expire_secs)
        try:
            user_id = s.loads(token)['user_id']
        except SignatureExpired:
            return None
        return UserModel.query.get(user_id)



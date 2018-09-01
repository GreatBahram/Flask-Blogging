# local imports
from blog import db, login_manager


class PostModel(db.Model):
    """
    Create a Post table
    """
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    slug = db.Column(db.Text, unique=True)
    body = db.Column(db.String(100), unique=True)
    published = db.Column(db.Boolean, default=False)
    number_of_visits = db.Column(db.Integer, default=0)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

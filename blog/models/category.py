# local imports
from blog import db, login_manager


class Category(db.Model):
    """Create a Category table """
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return f"<Category: '{self.name}'>"

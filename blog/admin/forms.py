# third-party imports
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, TextAreaField
from wtforms.validators import DataRequired, ValidationError

# local imports
from blog.models.post import PostModel

class CreatePostForm(FlaskForm):
    """
    Form for admins to create an new post
    """
    title = StringField('Title', validators=[DataRequired()])
    slug = StringField('Slug', validators=[DataRequired()])
    content = TextAreaField('Body', validators=[DataRequired()])
    published = BooleanField('Published')

    def validate_slug(self, slug):
        slug = PostModel.query.filter_by(slug=slug.data).first()
        if slug:
            raise ValidationError('Slug is already taken.')

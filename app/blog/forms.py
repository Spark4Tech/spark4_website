from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    excerpt = TextAreaField('Excerpt', validators=[Length(max=500)])
    content = TextAreaField('Content', validators=[DataRequired()])
    author = SelectField('Author', coerce=int, validators=[DataRequired()])
    category = SelectField('Category', coerce=int, validators=[DataRequired()])
    published = BooleanField('Publish')
    featured_image = StringField('Featured Image')
    inside_image = StringField('Inside Image')
    submit = SubmitField('Submit')

from flask_wtf import FlaskForm
from wtforms import Form, DateField, IntegerField, StringField, PasswordField, BooleanField, SubmitField, validators

class ShoppingItemForm(FlaskForm):
    id = IntegerField('item_id')
    title = StringField('title', validators=[validators.DataRequired(), validators.Length(min=1, max=255)])
    bought = IntegerField('bought')
    position = IntegerField('position')

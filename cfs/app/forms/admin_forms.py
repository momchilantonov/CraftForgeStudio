from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, DecimalField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')


class CategoryForm(FlaskForm):
    name_en = StringField('Name (English)', validators=[
                          DataRequired(), Length(max=100)])
    name_bg = StringField('Name (Bulgarian)', validators=[
                          DataRequired(), Length(max=100)])
    description_en = TextAreaField('Description (English)')
    description_bg = TextAreaField('Description (Bulgarian)')
    parent_id = SelectField(
        'Parent Category', coerce=int, validators=[Optional()])
    icon = StringField('Icon', validators=[Length(max=50)])
    image_url = StringField('Image URL', validators=[Length(max=255)])
    display_order = IntegerField(
        'Display Order', default=0, validators=[NumberRange(min=0)])
    is_active = BooleanField('Active', default=True)


class ProductForm(FlaskForm):
    name_en = StringField('Name (English)', validators=[
                          DataRequired(), Length(max=200)])
    name_bg = StringField('Name (Bulgarian)', validators=[
                          DataRequired(), Length(max=200)])
    description_en = TextAreaField('Description (English)')
    description_bg = TextAreaField('Description (Bulgarian)')
    price = DecimalField('Price', validators=[
                         DataRequired(), NumberRange(min=0)])
    category_id = SelectField('Category', coerce=int,
                              validators=[DataRequired()])
    stock = IntegerField('Stock', default=0, validators=[NumberRange(min=0)])
    image = FileField('Product Image', validators=[FileAllowed(
        ['jpg', 'jpeg', 'png', 'webp'], 'Images only!')])
    is_active = BooleanField('Active', default=True)
    is_featured = BooleanField('Featured', default=False)


class UpdateProfileForm(FlaskForm):
    full_name = StringField('Full Name', validators=[
                            DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[
                        DataRequired(), Email(), Length(max=100)])


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(
        'Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
                                 DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('new_password', message='Passwords must match')])

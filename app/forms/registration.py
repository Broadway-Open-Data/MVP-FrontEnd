from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, \
    SubmitField, FormField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, \
    Email, EqualTo, Length, Optional

# ...

class SignupForm(FlaskForm):
    email = StringField('Email', validators=[Length(min=6), Email(message='Enter a valid email.'),DataRequired()], render_kw={"placeholder": "Alexander@Hamilton.com"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message='Select a stronger password.')])
    confirm = PasswordField('Confirm Your Password', validators=[DataRequired(), EqualTo('password')])
    website = StringField('Website',validators=[Optional()],render_kw={"placeholder": "www.Hamilton.com"})
    instagram = StringField('Instagram Handle', validators=[Optional()], render_kw={"placeholder": "@Boss_Hamilton"})
    message = TextAreaField('Why do you want access to Open Broadway Data?',
        validators=[DataRequired(), Length(min=10, message='Please provide an answer > 50 characters.')],
        render_kw={"placeholder": "Please provide an answer > 50 characters..."})
    submit = SubmitField('Register')

# class SignupForm(FlaskForm):
#     """All of the fields as one."""
#     allFields = FormField(SignupFormFields_)
#     submit = SubmitField('Register')

# --------------------------------------------------------------------------------

class LoginFormFields_(FlaskForm):
    """User Log-in Form."""
    email = StringField('Email', validators=[Email(message='Enter a valid email.'),DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])

class LoginForm(FlaskForm):
    """All of the fields as one."""
    allFields = FormField(LoginFormFields_)
    submit = SubmitField('Log In')


# --------------------------------------------------------------------------------



class ForgotPasswordForm(FlaskForm):
    """If you forgot your password, reset through email address."""

    class allFields_(FlaskForm):
        """User Log-in Form."""
        email = StringField('Email', validators=[Email(message='Enter a valid email.'),DataRequired()])

    allFields = FormField(allFields_)
    submit = SubmitField('Submit')



 # --------------------------------------------------------------------------------


#
# class VerifyForm(FlaskForm):
#     """If you forgot your password, reset through email address."""
#
#     class allFields_(FlaskForm):
#         """User Log-in Form."""
#         email = StringField('Email', validators=[Email(message='Enter a valid email.'),DataRequired()])
#
#     allFields = FormField(allFields_)
#     submit = SubmitField('Submit')




# def validate_username(self, username):
#     user = User.query.filter_by(username=username.data).first()
#     if user is not None:
#         raise ValidationError('Please use a different username.')
#
# def validate_email(self, email):
#     user = User.query.filter_by(email=email.data).first()
#     if user is not None:
#         raise ValidationError('Please use a different email address.')

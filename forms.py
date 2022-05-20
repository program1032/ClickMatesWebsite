from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField, TextAreaField, SelectField, IntegerField, \
    DateField, TimeField
from wtforms.validators import DataRequired, Length, ValidationError, InputRequired, EqualTo, Email, NumberRange
from modeldb import User, Place


class RegisterUserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    family_name = StringField('Family Name', validators=[DataRequired()])
    mail = StringField('Email address', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(min=6, message="Password must have at least 6 characters")])
    bpartner = SelectField('Are you a business partner? ', choices=['Yes', 'No'])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username ' %s ' already exists" % self.username.data)

    def validate_email(self, mail):
        user = User.query.filter_by(mail=mail.data).first()
        if user:
            raise ValidationError("Email address ' %s ' already exists" % self.mail.data)


class ProfileForm(FlaskForm):
    file = FileField('Profile photo', validators=[DataRequired()])  # Photo
    biography = TextAreaField('Write a brief description for introducing you to the other users',
                              validators=[InputRequired(), Length(min=10, max=200)])
    submit = SubmitField('Submit')


class LogForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class PlaceForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2,
                                                                  message="The place's name must contain at least 2 "
                                                                          "characters")])
    address = StringField('Location', validators=[DataRequired()])
    schedule = TextAreaField('Open hours', validators=[DataRequired()])
    phone_number = StringField('Contact number', validators=[DataRequired(), Length(min=7, max=40)])
    price_level = SelectField('Price level', choices=['$', '$$', '$$$'])
    promotion = StringField('Promotion available', validators=[DataRequired()])
    url_link = StringField('Page link', validators=[DataRequired()])
    submit = SubmitField('Upload')

class AppointmentForm(FlaskForm):
    quantity = IntegerField('Quantity of people', validators=[DataRequired()])
    name = StringField('Name of the place ', validators=[DataRequired()])
    activity = StringField('Activity to do ', validators=[DataRequired()])
    date_time = DateField('Date of the appointment', validators=[InputRequired()])
    time_data = TimeField('Time of the appointment', validators=[InputRequired()])
    cancellation_time = SelectField('Time-lapse for cancellation',
                                    choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,
                                             22, 23, 24])
    submit = SubmitField('Create Appointment')

    def validate_name(self, name):
        place = Place.query.filter_by(name=self.name.data).first()
        if not place:
            raise ValidationError(
                "The place with name '%s' does not exist! Please verify the spelling of it." % self.name.data)


class ForgotForm(FlaskForm):
    email = StringField('Mail registered', validators=[DataRequired(), Email()])
    submit = SubmitField('Send code')

    def validate_email(self, email):
        mail = User.query.filter_by(mail=self.email.data).first()
        if not mail:
            raise ValidationError("The email address '%s' is not registered in our system" % self.email.data)


class CodeForm(FlaskForm):
    code_sent = StringField('Insert the six digits code sent', validators=[InputRequired()])
    submit = SubmitField('Verify code')


class PasswordForm(FlaskForm):
    new_password = PasswordField('New password',
                                 validators=[DataRequired(), Length(min=8, message='Password must contain '
                                                                                   'at least 8 '
                                                                                   'alphanumeric '
                                                                                   'digits')])
    confirmed_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('new_password',
                                                                                               message='Your password '
                                                                                                       'is not the '
                                                                                                       'same')])
    submit = SubmitField('Change Password')


class FeedbackForm(FlaskForm):  # USED
    comment = TextAreaField('Leave the comment', validators=[DataRequired()])
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(1, 5)])
    submit = SubmitField('Submit')


class PunishmentForm(FlaskForm):  # USED
    user_punished = StringField('Username to be reported', validators=[DataRequired()])
    reason = TextAreaField('Motive to be reported', validators=[DataRequired()])
    score = IntegerField("Score given to user's behavior", validators=[DataRequired(), NumberRange(1, 5,
                                                                                                   'The score must be '
                                                                                                   'an integer '
                                                                                                   'between 1 up to '
                                                                                                   '5')])
    submit = SubmitField('Report')


class PaymentForm(FlaskForm):
    firstName = StringField('First Name', validators=[InputRequired()])
    lastName = StringField('Last Name', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[Email()])
    address = StringField('Address', validators=[InputRequired()])
    address2 = StringField('Address 2')
    country = SelectField('Country', choices=['Italy'])
    state = SelectField('State')
    zip = StringField('Zip', validators=[InputRequired()])
    cc_name = StringField('Name on card', validators=[InputRequired()])
    cc_number = StringField('Credit card number', validators=[InputRequired()])
    cc_expiration = StringField('Expiration', validators=[InputRequired()])
    cc_cvv = StringField('CVV', validators=[InputRequired()])
    submit = SubmitField('Checkout')


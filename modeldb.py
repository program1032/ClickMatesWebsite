from datetime import datetime, date
from app import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    family_name = db.Column(db.String(100), nullable=False)
    mail = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    biography = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    OTP_Code = db.Column(db.String(6))
    profile_photo = db.Column(db.Boolean(), default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    # To access for this relationships it must be: user.{{backref}} given that user=User(...)
    place_id = db.relationship('Place', backref="place_id")
    review_made_id = db.relationship('PlaceReviews', backref='place_review')
    appointment_created = db.relationship('Appointment', backref='created', lazy='dynamic',
                                          foreign_keys='Appointment.user_creator')
    appointment_assigned = db.relationship('Appointment', backref='assigned', lazy='dynamic',
                                           foreign_keys='Appointment.user_assigned')
    id_punishment = db.relationship('Punishment', backref='punish_id')

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(100), nullable=False)
    # To access for this relationships it must be: role.{{backref}} given that role=Role(...)
    users = db.relationship('User', backref='rolename')


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    activity = db.relationship('Appointment', backref='name')


class PlaceReviews(db.Model):
    __tablename__ = 'placesreviews'
    id = db.Column(db.Integer(), primary_key=True)
    review = db.Column(db.String(300), nullable=False)
    rating = db.Column(db.Integer(), nullable=False)
    user_reviewer = db.Column(db.Integer, db.ForeignKey('users.id'))
    place_reviewed = db.Column(db.Integer, db.ForeignKey('places.id'))


class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer(), primary_key=True)
    qty_people = db.Column(db.Integer(), nullable=False)
    date_time = db.Column(db.Date(), nullable=False)  # type: date
    activity = db.Column(db.String(), nullable=False)
    time = db.Column(db.Time(), nullable=False)
    opening = db.Column(db.Boolean(), default=True,nullable=False)
    cancellation_time = db.Column(db.Integer(), nullable=False, default=5)
    user_creator = db.Column(db.String, db.ForeignKey('users.username'))
    user_assigned = db.Column(db.String, db.ForeignKey('users.username'))
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    category = db.Column(db.String, db.ForeignKey('categories.name'))
    users = db.relationship('Punishment', backref='punish')


class Place(db.Model):
    __tablename__ = 'places'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(64), nullable=False)
    schedule = db.Column(db.Text())
    phone_number = db.Column(db.String(40), nullable=False)
    price_level = db.Column(db.String(5), nullable=False)
    promotion = db.Column(db.String(300))
    url_link = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # To access for this relationships it must be: place.{{backref}} given that place=Place(...)
    appointment = db.relationship('Appointment', backref='appointment_id')
    review = db.relationship('PlaceReviews', backref='review_id')


class Punishment(db.Model):
    __tablename__ = 'punishments'
    id = db.Column(db.Integer(), primary_key=True)
    motive = db.Column(db.Text(), nullable=False)
    time = db.Column(db.DateTime(), default=datetime.utcnow)
    score= db.Column(db.Integer(), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'))
    user_punished = db.Column(db.String, db.ForeignKey('users.username'))

    def ping(self):
        self.time = datetime.utcnow()
        db.session.add(self)






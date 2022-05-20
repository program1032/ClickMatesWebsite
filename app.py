import datetime

from flask import Flask, session, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Message, Mail
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_uploads import UploadSet
from flask_uploads import configure_uploads
from flask_uploads import IMAGES, patch_request_class

import os
import random
import string

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cmappdatabase.db"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ['EMAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['EMAIL_PASSWORD']
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + "/static"
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

db = SQLAlchemy(app)
mail = Mail(app)
bcrypt = Bcrypt(app)

from modeldb import User, Role, Place, Appointment, PlaceReviews, Category, Punishment
from forms import RegisterUserForm, ProfileForm, LogForm, PlaceForm, AppointmentForm, FeedbackForm, PunishmentForm
from forms import ForgotForm, CodeForm, PasswordForm, PaymentForm


def key_generator():
    key = ''.join(random.choice(string.digits) for x in range(6))
    return key


def send_mail(to, subject, template, **kwargs):
    msg = Message(subject, recipients=[to], sender=app.config['MAIL_USERNAME'])
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)


@app.before_first_request
def create_db():
    db.drop_all()
    db.create_all()
    role_admin = Role(rolename='Admin')
    role_user = Role(rolename='User')
    role_partner = Role(rolename='Business Partner')
    db.session.add_all([role_admin, role_user, role_partner])
    pass_c = generate_password_hash("AdM1n.2o22")
    user_admin = User(name="Julian", family_name="Puerto",
                      mail="puerto.julianm@gmail.com",
                      username="admin", password=pass_c,
                      rolename=role_admin
                      )
    password_1 = generate_password_hash("4ccoun71.")
    password_2 = generate_password_hash("4cc0un72.#")
    password_3 = generate_password_hash("4P4ssw0.rd12j#.")
    password_4 = generate_password_hash("9907.Jul!4n0")
    new_user2 = User(name="Hasary", family_name="Malaver",
                     mail="mospina_has@hotmail.com",
                     username="hospina1997", password=password_1,
                     rolename=role_user
                     )
    new_user3 = User(name="Angela", family_name="Echeverry",
                     mail="aecheverry78@icloud.com",
                     username="echevverry89", password=password_2,
                     rolename=role_user
                     )
    new_user4 = User(name="Naomi", family_name="Picart",
                     mail="npicartm@gmail.com",
                     username="npicart78", password=password_3,
                     rolename=role_user
                     )
    new_user5 = User(name="Julian", family_name="Puerto",
                     mail="juli.puerto1999@hotmail.com",
                     username="jpuerto19", password=password_4,
                     rolename=role_user
                     )
    new_category = Category(
        name="Sports"
    )
    new_category2 = Category(
        name="Restaurant"
    )
    new_category3 = Category(
        name="Entertainment"
    )
    db.session.add_all([user_admin, new_user2, new_user3, new_user4, new_user5])
    db.session.add_all([new_category, new_category2, new_category3])
    new_place = Place(
        name='Zushi Torino', location="Largo Vittorio Emanuele II, 82, 10121 Torino TO",
        schedule="<br>Everyday: 12 - 3 PM, 6:30 PM - 11 PM ",
        phone_number='011 454 6932', price_level='$$',
        promotion='In the menu, you can find our promotions.',
        url_link='https://www.thefork.it/ristorante/zushi-torino-r467355?cc=18174-54f', user_id=user_admin.id
    )
    new_place2 = Place(
        name='Umami Torino', location='Via XX Settembre, 49, 10121 Torino TO',
        schedule="<br>Monday to Wednesday: 12 - 3 PM, 7 PM - 12 AM <br>"
                 "Thursday to Sunday: 12 - 3 PM, 7 PM - 1 AM ",
        phone_number='011 1947 8089', price_level='$$',
        promotion='None for the moment',
        url_link='Not available, only calls.', user_id=user_admin.id
    )
    new_place3 = Place(
        name='Greek Food Lab', location='Via Claudio Luigi Berthollet, 6bis, 10126 Torino TO',
        schedule="<br>Everyday: 12 - 3 PM, 7 PM - 12 PM ",
        phone_number='011 583 3992', price_level='$$',
        promotion='None for the moment',
        url_link='https://www.greekfoodlab.it/', user_id=user_admin.id
    )
    new_place4 = Place(
        name='Greek Tavern Olimpia', location='Via Lavagna, 7, 10126 Torino TO',
        schedule='<br>Monday: closed<br>Rest of the days: 12 - 4 PM, 7 - 11:55 PM',
        phone_number='011 696 6111', price_level='$$',
        promotion='None for the moment',
        url_link='https://www.ristotavernagreca.it/', user_id=user_admin.id
    )
    new_place5 = Place(
        name='CioccolatItaliani', location="Via Sant'Ottavio, 10124 Torino TO",
        schedule='<br>Everyday: 9 AM - 9 PM',
        phone_number='011 1898 9597', price_level='$$',
        promotion='None for the moment',
        url_link='Not available', user_id=user_admin.id
    )
    new_place6 = Place(
        name='Costadoro Coffee Lab Diamond', location='Via Teofilo Rossi di Montelera, 2, 10123 Torino TO',
        schedule='<br>Weekdays: 8 AM - 8 PM<br>Weekends: 8:30 AM - 8 PM',
        phone_number='011 037 1020', price_level='$$',
        promotion='None for the moment',
        url_link='https://api.whatsapp.com/send?phone=390110371020&text=&source=&data=&app_absent=',
        user_id=user_admin.id
    )
    new_place7 = Place(
        name='Plin E Tajarin', location='Via Goffredo Casalis, 59, 10138 Torino TO',
        schedule='<br>Monday and Tuesday: 12:45 PM - 3 PM<br>Wednesday: Closed<br>Thursday and Friday: 12:45 PM - 3 '
                 'PM, 8 - 10 PM<br>Weekends: 1 - 3 PM',
        phone_number='011 037 1020', price_level='$$',
        promotion='None for the moment',
        url_link='Not available', user_id=user_admin.id
    )
    new_place8 = Place(
        name='Il Vicolo', location='Via S. Francesco da Paola, 41, 10123 Torino TO',
        schedule='<br>Monday: Closed<br>Tuesday to Thusday: 12:30 PM - 2:30 PM, 7:30 PM - 11:30 PM<br>Friday: 12:30 '
                 'PM - 3 PM<br>Saturdays:12:30 PM - 2:30 PM, 7:30 - 11:30 PM<br>Sunday: 12:30 PM - 3 PM ',
        phone_number='011 535233', price_level='$$',
        promotion='None for the moment',
        url_link='Not available', user_id=user_admin.id
    )
    new_place9 = Place(
        name='Ideal Cinema Cityplex', location='Corso Giambattista Beccaria, 4, 10122 Torino TO',
        schedule='<br>It depends on the available movies',
        phone_number='011 521 4316', price_level='$$',
        promotion='None for the moment',
        url_link='https://www.idealcityplex.it', user_id=user_admin.id
    )
    new_place10 = Place(
        name='King Funmily', location=' Via Monginevro, 242, 10142 Torino TO',
        schedule='<br>Weekdays: 4 PM- 2 AM<br>Weekends: 3 PM - 2 AM',
        phone_number='011 704021', price_level='$$',
        promotion='Give us a call and ask for it',
        url_link='Not available', user_id=user_admin.id
    )
    new_place11 = Place(
        name='Hiking Turin Alps Area', location='Susa, Chisone and Lanzo Valleys - Alps Near Turin ',
        schedule='<br>Everyday: Open all time',
        phone_number='+39 3386608548', price_level='$$',
        promotion='Give us a call and ask for it',
        url_link='https://www.trekking-alps.com/italian-alps/turin-alps-hiking-area/', user_id=user_admin.id
    )
    db.session.add_all(
        [new_place, new_place2, new_place3, new_place4, new_place5, new_place6, new_place7, new_place8, new_place9,
         new_place10, new_place11])
    db.session.commit()
    new_appointment = Appointment(
        qty_people=3,
        date_time=datetime.date(2022, 5, 22),
        activity="Eat Asian food",
        time=datetime.time(13),
        place_id=new_place.id,
        category=new_category2.name,
        user_creator=new_user2.username
    )
    new_appointment2 = Appointment(
        qty_people=2,
        date_time=datetime.date(2022, 5, 22),
        activity="Go to eat sushi",
        time=datetime.time(13),
        place_id=new_place2.id,
        category=new_category2.name,
        user_creator=new_user3.username
    )
    new_appointment3 = Appointment(
        qty_people=2,
        date_time=datetime.date(2022, 5, 21),
        activity="Eat Greek food",
        time=datetime.time(13, 30),
        place_id=new_place3.id,
        category=new_category2.name,
        user_creator=new_user3.username
    )
    new_appointment4 = Appointment(
        qty_people=4,
        date_time=datetime.date(2022, 5, 21),
        activity="Eat some mediterranean desserts",
        time=datetime.time(14),
        place_id=new_place3.id,
        category=new_category2.name,
        user_creator=new_user4.username
    )
    new_appointment5 = Appointment(
        qty_people=4,
        date_time=datetime.date(2022, 5, 21),
        activity="Hiking",
        time=datetime.time(8, 30),
        place_id=new_place11.id,
        category=new_category.name,
        user_creator=new_user5.username
    )
    new_appointment6 = Appointment(
        qty_people=2,
        date_time=datetime.date(2022, 5, 21),
        activity='Eat some of the Italian desserts',
        time=datetime.time(20),
        place_id=new_place5.id,
        category=new_category2.name,
        user_creator=new_user3.username
    )
    new_appointment7 = Appointment(
        qty_people=3,
        date_time=datetime.date(2022, 5, 22),
        activity="Play bowling",
        time=datetime.time(15),
        place_id=new_place10.id,
        category=new_category3.name,
        user_creator=new_user5.username
    )
    new_appointment8 = Appointment(
        qty_people=4,
        date_time=datetime.date(2022, 5, 21),
        activity='Watch a movie',
        time=datetime.time(19),
        place_id=new_place9.id,
        category=new_category3.name,
        user_creator=new_user4.username
    )
    new_appointment9 = Appointment(
        qty_people=2,
        date_time=datetime.date(2022, 5, 22),
        activity='Brunch in the morning?',
        time=datetime.time(9),
        place_id=new_place6.id,
        category=new_category2.name,
        user_creator=new_user2.username
    )
    new_appointment10 = Appointment(
        qty_people=2,
        date_time=datetime.date(2022, 5, 22),
        activity="Eat some Italian cuisine",
        time=datetime.time(13),
        place_id=new_place7.id,
        category=new_category2.name,
        user_creator=new_user5.username
    )
    new_appointment11 = Appointment(
        qty_people=3,
        date_time=datetime.date(2022, 5, 21),
        activity="Let's eat pasta",
        time=datetime.time(14),
        place_id=new_place8.id,
        category=new_category2.name,
        user_creator=user_admin.username
    )
    db.session.add_all(
        [new_appointment, new_appointment2, new_appointment3, new_appointment4, new_appointment5, new_appointment6,
         new_appointment7,
         new_appointment8, new_appointment9, new_appointment10, new_appointment11])
    db.session.commit()


@app.route('/newplace/<category>', methods={'GET', 'POST'})
def newplace(category):
    if not (session.get('username')) or session.get('username') is None:
        return redirect(url_for("mainpage"))
    form = PlaceForm()
    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    role = Role.query.filter_by(id=user.role_id).first()
    user_role = role.rolename
    if form.validate_on_submit():
        new_place = Place(
            name=form.name.data,
            location=form.address.data,
            schedule=form.schedule.data,
            phone_number=form.phone_number.data,
            price_level=form.price_level.data,
            promotion=form.promotion.data,
            url_link=form.url_link.data,
            user_id=user.id
        )
        db.session.add(new_place)
        db.session.commit()
        return redirect(url_for('newappointment', category=category))
    return render_template('newplace.html', form=form, username=username, role=user_role)


@app.route('/newappointment/<category>', methods={'GET', 'POST'})
def newactivity(category):
    if not (session.get('username')) or session.get('username') is None:
        return redirect(url_for("mainpage"))
    form = AppointmentForm()
    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    role = Role.query.filter_by(id=user.role_id).first()
    user_role = role.rolename
    if form.validate_on_submit():
        place = Place.query.filter_by(name=form.name.data).first()
        new_appointment = Appointment(
            qty_people=form.quantity.data,
            date_time=form.date_time.data,
            time=form.time_data.data,
            activity=form.activity.data,
            user_creator=username,
            place_id=place.id,
            category=category,
            cancellation_time=form.cancellation_time.data
        )
        db.session.add(new_appointment)
        db.session.commit()
        return redirect(url_for('places', id=new_appointment.id))
    return render_template('newactivity.html', form=form, username=username, role=user_role)


@app.route('/places/<id>', methods={'GET', 'POST'})
def places(id):
    if not (session.get("username")) or session.get("username") is None:
        return redirect(url_for("mainpage"))
    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    role = Role.query.filter_by(id=user.role_id).first()
    user_role = role.rolename
    info = Appointment.query.filter_by(id=id).first()
    option = Place.query.filter_by(id=info.place_id).first()
    return render_template('places.html', role=user_role, option=option, id=id, username=username)


@app.route('/payment/<id>', methods={'GET', 'POST'})
def payment(id):
    if not (session.get("username")) or session.get("username") is None:
        return redirect(url_for("mainpage"))
    form = PaymentForm()
    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    role = Role.query.filter_by(id=user.role_id).first()
    user_role = role.rolename
    info = Appointment.query.filter_by(id=id).first()
    return render_template('checkout.html', form=form, role=user_role, username=username, info=info, id=id)


@app.route('/faq')
def faq():
    return render_template('FAQ.html', role='User')


@app.route("/upload", methods=["POST", "GET"])
def upload():
    if not (session.get("username")) and session.get("username") is None:
        return redirect(url_for("loginpage"))
    folder_name = str(session.get("username"))
    if not os.path.exists('static/' + str(folder_name)):
        os.makedirs('static/' + str(folder_name))
    file_url = os.listdir('static/' + str(folder_name))
    file_url = [str(folder_name) + "/" + file for file in file_url]
    formupload = ProfileForm()
    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    if formupload.validate_on_submit():
        filename = photos.save(formupload.file.data, name=folder_name + '.jpg', folder=folder_name)
        file_url.append(filename)
        user.biography = formupload.biography.data
        user.profile_photo = True
        return redirect(url_for('profile', username=username))
    return render_template("upload.html", formupload=formupload, filelist=file_url, username=username, user=user)


@app.route('/profile/<username>', methods={'GET', 'POST'})
def profile(username):
    if not (session.get('username')) or session.get('username') is None:
        return redirect(url_for("mainpage"))
    user = User.query.filter_by(username=username).first()
    name = user.name
    role = Role.query.filter_by(id=user.role_id).first()
    user_role = role.rolename
    return render_template('profile.html', username=username, name=name, user=user, role=user_role)


@app.route('/', methods={'GET', 'POST'})
def mainpage():
    form = LogForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['id'] = user.id
            session['name'] = user.name
            session['username'] = username
            user.ping()
            return redirect(url_for('dashboard', username=username))
    return render_template('main_signin.html', form=form)


@app.route('/signup', methods={'GET', 'POST'})
def signup():
    form = RegisterUserForm()
    if form.validate_on_submit():
        username = form.username.data
        pass_enc = generate_password_hash(form.password.data)
        user_role = Role.query.filter_by(rolename='User').first()
        bpartner_role = Role.query.filter_by(rolename='Business Partner').first()
        if form.bpartner.data == "Yes":
            assignrole = bpartner_role
        else:
            assignrole = user_role
        new_user = User(name=form.name.data,
                        family_name=form.family_name.data,
                        mail=form.mail.data,
                        username=username,
                        password=pass_enc,
                        rolename=assignrole)
        db.session.add(new_user)
        db.session.commit()
        new_user.ping()
        send_mail(form.mail.data, 'Welcome to Your Account',
                  'mail', name=form.name.data, username=username, password=form.password.data)
        session['name'] = form.name.data
        session['username'] = username
        return redirect(url_for('dashboard', username=username))
    return render_template('signup_page.html', form=form)


@app.route('/dashboard/<username>', methods={'GET', 'POST'})
def dashboard(username):
    if not (session.get('username')) or session.get('username') is None:
        return redirect(url_for("mainpage"))
    user = User.query.filter_by(username=username).first()
    role = Role.query.filter_by(id=user.role_id).first()
    name = user.name
    familyname = user.family_name
    user_role = role.rolename
    entry = Appointment.query.all()
    return render_template('activities.html', username=username, name=name, family=familyname, role=user_role,
                           entries=entry)


@app.route('/forgot_password', methods={'GET', 'POST'})
def forgotpassword():
    form = ForgotForm()
    if form.validate_on_submit():
        user = User.query.filter_by(mail=form.email.data).first()
        key = key_generator()
        user.OTP_Code = key
        send_mail(form.email.data, 'Password code', 'mailpassword', name=user.name, OTP_Code=key)
        session['username'] = user.username
        return redirect(url_for('codeconfirmation'))
    return render_template('forgotpassword.html', form=form, role='User')


@app.route('/forgot_password/code', methods={'GET', 'POST'})
def codeconfirmation():
    if not (session.get("username")) or session.get("username") is None:
        return redirect(url_for("mainpage"))
    form = CodeForm()
    username = session.get('username')
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user.OTP_Code == form.code_sent.data:
            session['name'] = user.name
            return redirect(url_for('set_newpassword'))
    return render_template('confirmationcode.html', form=form, role='User', username=username)


@app.route('/forgot_password/set_new', methods={'GET', 'POST'})
def set_newpassword():
    if not (session.get("username")) or session.get("username") is None:
        return redirect(url_for("mainpage"))
    form = PasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=session['username']).first()
        user.password = form.confirmed_password.data
        return redirect(url_for('dashboard', username=user.username))
    return render_template('newpassword.html', form=form, role='User')


@app.route('/cancellation/<id>', methods={'GET', 'POST'})
def cancellation(id):
    if not (session.get("username")) or session.get("username") is None:
        return redirect(url_for("mainpage"))
    username = session.get('username')
    info = Appointment.query.filter_by(id=id).first()
    db.session.delete(info.user_assigned)
    db.session.commit()
    return redirect(url_for('dashboard', username=username))


@app.route('/about', methods={'GET', 'POST'})
def about():
    if session.get('username'):
        username = session.get('username')
        user = User.query.filter_by(username=username).first()
        role = Role.query.filter_by(id=user.role_id).first()
        user_role = role.rolename
    else:
        user_role = 'User'
    return render_template('about.html', role=user_role)


@app.route('/confirmation/<id>', methods={'GET', 'POST'})
def confirmation(id):
    if not (session.get("username")) or session.get("username") is None:
        return redirect(url_for("mainpage"))
    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    role = Role.query.filter_by(id=user.role_id).first()
    user_role = role.rolename
    info = Appointment.query.filter_by(id=id).first()
    place = Place.query.filter_by(id=info.place_id).first()
    host = User.query.filter_by(username=info.user_creator).first()
    info.user_assigned = username
    info.opening = False
    return render_template('appointments.html', info=info, id=id, role=user_role, username=username, host=host,
                           place=place)


@app.route('/feedback/<id>', methods={'GET', 'POST'})
def feedback(id):
    if not (session.get("username")) or session.get("username") is None:
        return redirect(url_for("mainpage"))
    feed = FeedbackForm()
    info = Appointment.query.filter_by(id=id).first()
    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    role = Role.query.filter_by(id=user.role_id).first()
    place = Place.query.filter_by(id=info.place_id).first()
    user_role = role.rolename
    if feed.validate_on_submit():
        new_entry = PlaceReviews(
            review=feed.comment.data,
            rating=feed.rating.data,
            user_reviewer=user.id,
            place_reviewed=info.place_id
        )
        db.session.add_all([new_entry])
        db.session.commit()
        return redirect(url_for('dashboard', username=username))
    return render_template('feedback.html', form=feed, appointment=info, role=user_role, place=place, id=id,
                           username=username)


@app.route('/punishment/<id>', methods={'GET', 'POST'})
def punishment(id):
    form = PunishmentForm()
    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    role = Role.query.filter_by(id=user.role_id).first()
    user_role = role.rolename
    if form.validate_on_submit():
        new_punish = Punishment(
            user_punished=form.user_punished.data,
            motive=form.reason.data,
            appointment_id=id,
            score=form.score.data
        )
        new_punish.ping()
        db.session.add(new_punish)
        db.session.commit()
        return redirect(url_for('dashboard', username=username))
    return render_template('punishment.html', form=form, username=username, role=user_role)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('mainpage'))


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('mainpage'))


@app.errorhandler(500)
def page_500(e):
    return redirect(url_for('mainpage'))


if __name__ == '__main__':
    app.run()

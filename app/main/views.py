# from turtle import title
from flask import render_template
from ..models import Pitch

from app.request import Pitch
from . import  main
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from pip import main
from ..models import User
from ..auth.forms import LoginForm, RegistrationForm
from ..email import mail_message

from ..import db
# from . import auth
from ..email import mail_message

#views
from flask_login import login_required, current_user
from flask import render_template, request, redirect, url_for, abort
from  .forms import UpdateProfile, PitchForm
from .. import db
from ..models import User, Pitch
from . import main



@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    return render_template('index.html')

    
@main.route('/registration/new/<int:id>', methods= ['GET', 'POST'])
@login_required
def new_registration(id):
    '''
    '''

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()


    if user is None:
        abort (404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update', methods= ['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort (404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data


        db.session.add(user)
        db.session.commmit()


        return redirect(url_for('.profile', uname=user.username))

    
    return render_template('profile/update.html', form = form)

    
@main.route ('/registration', methods = ["GET", "POST"])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()

        mail_message("Welcome to Pitchy", "email/welcome_user", user.email, user=user)
        
        return redirect(url_for('main.login'))
    
    title = "New Account"
    return render_template('registration.html', registration_form = form)

@main.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user, login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.new_pitch'))

        flash('invalid username or password')

    else:
        title = "Pitchy login"
        return render_template('login.html', login_form = login_form, title = title)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))

@main.route('/pitches/new/<int:id>', methods = ['GET', 'POST'])
@login_required
def new_pitch(id):

    form = PitchForm()
    if form.validate_on_submit():
        title = form.title.data
        pitch = form.pitch.data

        #updated review instance
        new_pitch = Pitch(title, pitch)

        #save review method
        new_pitch.save_pitch()
        return redirect(url_for())


    return render_template('new_pitch.html', pitch_form = form, pitch = pitch)


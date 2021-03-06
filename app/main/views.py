# from turtle import title
from xmlrpc.client import boolean
from flask import render_template
from ..models import Pitch, User, Upvote, Downvote

from app.request import Pitch
from . import  main
from flask import render_template, redirect, url_for, flash, request
from flask_login import UserMixin, login_user, logout_user, login_required
from pip import main
from ..models import User
from ..auth.forms import LoginForm, RegistrationForm
from ..email import mail_message

from ..import db, images
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

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = images.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))   

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))

@main.route('/create_new',methods = ['GET','POST'])
@login_required
def new_pitch():
    form = PitchForm()

    if form.validate_on_submit():
        category = form.category.data
        context = form.context.data
        new_pitch = Pitch(category=category,context=context)
        #Database save a new pitch
        new_pitch.save_pitch()
        return redirect(url_for('main.pitch_display'))
    else:
        all_pitches = Pitch.query.order_by(Pitch.posted).all

    return render_template('new_pitch.html',pitch_form = form,pitches=all_pitches)

@main.route('/pitches', methods = ['GET', 'POST'])
@login_required
def pitch_display():
    '''
    View page for the pitches created with their data
    '''

    # pitches= Pitch.get_pitches
    pitches = Pitch.query.all()
    


    return render_template('pitches.html', pitches= pitches)

@main.route('/pitch/upvote/<int:pitch_id>/upvote', methods=['GET', 'POST'])
@login_required
def upvote(pitch_id):
    pitch = Pitch.query.get(pitch_id)
    user = current_user
    pitch_upvotes = Upvote.query.filter_by(pitch_id=pitch_id)

    if Upvote.query.filter(Upvote.user_id == user.id, Upvote.pitch_id == pitch_id).first():
        return redirect(url_for('main.index'))

    new_upvote = Upvote(pitch_id=pitch_id, user=current_user)
    new_upvote.save_upvotes()
    return redirect(url_for('main.index'))

   






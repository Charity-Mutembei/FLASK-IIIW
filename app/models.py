import profile
from . import db
from flask_login import UserMixin
from . import login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, index= True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    pitches = db.relationship('Pitch',backref = 'user',lazy = "dynamic")

    @property
    def password (self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

    def __repr__(self) :
        return f'User{self.username}'

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")

    def __repr__(self):
        return f'User {self.name}'


class Pitch(db.Model):
    
    __tablename__ = 'pitches'

    all_pitches = []

    id = db.Column(db.Integer,primary_key=True)
    category = db.Column(db.String)
    context = db.Column(db.String)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comment = db.relationship('Comment',backref='post',lazy='dynamic')



    def save_pitch(self):
            db.session.add(self)
            db.session.commit()

            Pitch.all_pitches.append(self)


    @classmethod
    def get_pitches(cls, id):
        response = []


        for pitch in cls.all_pitches:
            if pitch.user_id==id:
                response.append(pitch)

        

    def _repr_(self):
            return f'Pitch{self.category}'
        
class Comment(db.Model):
    
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String)
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    pitch_comment = db.Column(db.String)
    posted = db.Column(db.DateTime,default = datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, pitch_id):
        comments = Comment.query.filter_by(pitch_id=pitch_id).all()
        return comments

    @classmethod
    def get_comment_writer(cls, user_id):
        writer = User.query.filter_by(id=user_id).first()

        return writer

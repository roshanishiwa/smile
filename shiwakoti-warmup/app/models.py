from datetime import datetime

from app import db, login

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

postTags = db.Table('postTags',
	db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
	db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    body = db.Column(db.String(1500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    likes = db.Column(db.Integer, default = 0)
    happiness_level = db.Column(db.Integer, default = 3)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship('Tag', secondary = postTags,
							primaryjoin=(postTags.c.post_id == id),
							backref=db.backref('postTags', lazy='dynamic'),
							lazy='dynamic')

class Tag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20))
	posts = db.relationship('Post', secondary = postTags,
							primaryjoin=(postTags.c.tag_id == id),
							backref=db.backref('postTags', lazy='dynamic'),
							lazy='dynamic')
	def __repr__(self):
		return '<Tag {}-{} >'.format(self.name, self.id)

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	posts = db.relationship("Post", backref='writer', lazy='dynamic')

	def _repr_ (self):
		return '<User {} - {} >'.format(self.id, self.username)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def get_password(self, password):
		return check_password_hash(self.password_hash, password)

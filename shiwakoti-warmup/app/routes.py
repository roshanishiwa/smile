from __future__ import print_function
import sys
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_sqlalchemy import sqlalchemy

from app import app, db

from app.forms import PostForm, SortForm, RegistrationForm, LoginForm
from app.models import Post, Tag, postTags, User

from flask_login import current_user, login_user, logout_user, login_required


@app.before_first_request
def initDB(*args, **kwargs):
    db.create_all()
    if Tag.query.count() == 0:
    	tags = ['funny','inspiring', 'true-story', 'heartwarming', 'friendship']
    	for t in tags:
    		db.session.add(Tag(name=t))
    	db.session.commit()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	smilecount = Post.query.count()
	sortform = SortForm()
	if request.method == 'POST':
		sorting = int(sortform.sort.data)
		sortuser = sortform.select.data
		if (sortuser):
			# filter by current_user.id
			posts = Post.query.filter_by(user_id=current_user.id)
		elif (sorting == 1):
			posts = Post.query.order_by(Post.timestamp.desc())
		elif (sorting == 2):
			posts = Post.query.order_by(Post.title.desc())
		elif (sorting == 3):
			posts = Post.query.order_by(Post.likes.desc())
		elif (sorting == 4):
			posts = Post.query.order_by(Post.happiness_level.desc())
	else:
		posts = Post.query.order_by(Post.timestamp.desc())
	return render_template('index.html', title="Smile Portal", posts=posts.all(),
    						smilecount=smilecount, sortform=sortform)

@app.route('/postsmile', methods=['GET', 'POST'])
@login_required
def view():
	form = PostForm()
	if form.validate_on_submit():
		postdata = Post(title = form.title.data, body = form.body.data, 
						happiness_level = form.happiness_level.data, 
						tags=form.tag.data, user_id = current_user.id)
		addTag = form.tag.data
		for t in addTag:
			postdata.tags.append(t)
		db.session.add(postdata)
		db.session.commit()
		flash("Posted successfully, your new smile post has been created!")
		return redirect(url_for('index'))
	return render_template('create.html', form=form)

@app.route('/like/<post_id>', methods=['GET'])
@login_required
def like(post_id):
	post = Post.query.get(post_id)
	post.likes += 1
	db.session.commit()
	return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('You have successfully registered!')
		return redirect(url_for('login'))
	return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.get_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		return redirect(url_for('index'))
	return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))


@app.route('/delete/<post_id>', methods=['DELETE', 'POST'])
@login_required
def delete(post_id):
	thepost = Post.query.get(post_id)
	for t in thepost.tags:
		thepost.tags.remove(t)
	db.session.commit()
	db.session.delete(thepost)
	db.session.commit()
	flash('The post has been successfully deleted!')
	return redirect(url_for('index', thepost=thepost))




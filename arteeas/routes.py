import os
import secrets
from flask import render_template, session, request, url_for, flash, redirect, request, abort
from arteeas import app, db, bcrypt
from arteeas.forms import RegistrationForm, LoginForm, MusicForm
from arteeas.models import User, Music
from flask_login import login_user, current_user, logout_user, login_required

# set up the homepage
@app.route("/", methods=["GET", "POST"])
def index():
    title = "arteeas"
    headline = "Welcome to the arteeas!"

    # intialize only once when making get request for the first time
    if session.get("reviews") is None:
        session["reviews"] = []

    # process music request: either add new or ignore duplicate entry
    if request.method == "POST":
        review = request.form.get("review")
        if review not in session["reviews"]:
            session["reviews"].append(review)
    musics=Music.query.all()

    # render the hompage index.html
    return render_template("index.html", title=title, headline=headline, musics=musics, reviews = session["reviews"])

# to do: add description of this website in about.html
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit(): # if valid, hash ps and save it to database db
        # generate one time alert.
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)

        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() # database query for matching user if there is
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')

@app.route("/user")
def user():
    return "User page"

@app.route("/music/new", methods=['GET', 'POST'])
@login_required
def new_music():
    form = MusicForm()
    if form.validate_on_submit():
        music = Music(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(music)
        db.session.commit()
        flash('Your music has been created!', 'success')
        return redirect(url_for('index'))
    return render_template('create_music.html', title='New Music', form=form, legend='New Music')

@app.route("/music/<int:music_id>")
def music(music_id):
    music = Music.query.get_or_404(music_id) # give the music with the given id
    return render_template('music.html', title=music.title, music=music)

@app.route("/music/<int:music_id>/update", methods=['GET', 'POST'])
def update_music(music_id):
    music = Music.query.get_or_404(music_id) # give the music with the given id
    if music.author != current_user: # to do 让管理员也可以修改
        abort(403)
    form = MusicForm()
    if form.validate_on_submit():
        music.title = form.title.data
        music.content = form.content.data
        db.session.commit()
        flash('Your music has been updated!', 'success')
        return redirect(url_for('music', music_id=music.id))
    elif request.method == 'GET':
        form.title.data = music.title
        form.content.data = music.content
    return render_template('create_music.html', title='Update Music',
                           form=form, legend='Update Music')

@app.route("/music/<int:music_id>/delete", methods=['POST'])
@login_required
def delete_music(music_id):
    music = Music.query.get_or_404(music_id)
    if music.author != current_user:
        abort(403)
    db.session.delete(music)
    db.session.commit()
    flash('Your music has been deleted!', 'success')
    return redirect(url_for('index'))

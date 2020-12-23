"""Blogly application."""
from flask import Flask, render_template, request, redirect
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "fe23f23g"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
# db.create_all()

@app.route('/')
def index():
    
    return redirect('/users')

@app.route('/users')
def show_users():
    users = User.query.all()
    return render_template("index.html", users=users)

@app.route('/users/new')
def new_user_form():
    return render_template('newUser.html')

@app.route('/users/new', methods=['POST'])
def create_user():
    name = request.form['first_name']
    last = request.form['last_name']
    url = request.form['image_url'] 
    url = url if url else None

    new_user = User(first_name=name, last_name=last, image_url=url)
    db.session.add(new_user)
    db.session.commit()
    return redirect(f'/users/{new_user.id}')

@app.route('/users/<int:user_id>')
def user_details(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    user = User.query.get(user_id)

    return render_template('editUser.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    user = User.query.get(user_id)
    name = request.form['first_name'] if len(request.form['first_name']) > 0 else user.first_name
    last = request.form['last_name'] if len(request.form['last_name']) > 0 else user.last_name
    url = request.form['image_url'] 
    url = url if url else None

    user.first_name = name
    user.last_name = last
    user.image_url = url
    db.session.add(user)
    db.session.commit()
    return redirect(f'/users/{user.id}')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect('/')
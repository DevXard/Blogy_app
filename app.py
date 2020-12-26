"""Blogly application."""
from flask import Flask, render_template, request, redirect
from models import db, connect_db, User, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
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

@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
    user = User.query.get(user_id)
    tags = Tag.query.all()
    return render_template('newPost.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def create_new_post(user_id):
    title = request.form['title']
    content = request.form['content']
    vals = request.form.getlist('Tags')
    

    new_post = Post(title=title, content=content, post_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    for val in vals:
        tags = PostTag(post_id=new_post.id, tag_id=val)
        db.session.add(tags)
    db.session.commit()
    return redirect(f'/posts/{new_post.id}')

@app.route('/posts/<int:post_id>')
def post_details(post_id):
    post = Post.query.get_or_404(post_id)
    tags = post.post_tag
    return render_template('postsDetail.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('editPost.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    new_title = request.form['title'] if len(request.form['title']) > 0 else post.title
    new_content = request.form['content'] if len(request.form['content']) > 0 else post.content
    vals = request.form.getlist('Tags')

    post.title = new_title
    post.content = new_content
    db.session.add(post)
    db.session.commit()
    tags = PostTag.query.filter_by(post_id=post.id).delete()
    for val in vals:
        tags = PostTag(post_id=post.id, tag_id=val)
        db.session.add(tags)
    db.session.commit()
    return redirect(f'/posts/{post.id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    
    tags = PostTag.query.filter_by(post_id=post_id).delete()
    db.session.commit()
    post = Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    
    return redirect('/')

@app.route('/tags')
def get_tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def get_tag_by_id(tag_id):
    tag_by_id = Tag.query.get_or_404(tag_id)

    return render_template('tag_details.html', tag_by_id=tag_by_id)

@app.route('/tags/new')
def create_new_tag_form():

    return render_template('new_tag.html')

@app.route('/tags/new', methods=['POST'])
def create_new_tag():
    name = request.form['name']

    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    return render_template('edit_tag.html')

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
    tag = Tag.query.get(tag_id)
    name = request.form['name']

    tag.name = name
    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')
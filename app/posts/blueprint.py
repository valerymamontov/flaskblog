from flask import Blueprint
from flask import render_template

from models import Post, Tag
from .forms import PostForm

from flask import request
from app import db

from flask import redirect
from flask import url_for


posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/create', methods=['POST', 'GET'])
def create_post():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        try:
            post = Post(title=title, body=body)
            db.session.add(post)
            db.session.commit()
        except:
            print('Ошибка при создании поста...')

        return redirect(url_for('posts.index'))

    form = PostForm()
    return render_template('posts/create_post.html', myform=form)


@posts.route('/')
def index():

    q = request.args.get('q')
    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.tBody.contains(q))
    else:
        posts = Post.query.order_by(Post.dCreated.desc())

    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    pages = posts.paginate(page=page, per_page=5)

    return render_template('posts/index.html', all_posts=posts, pages=pages)


@posts.route('/<slug>')
def mypost(slug):
    currentPost = Post.query.filter(Post.slug == slug).first()
    tags = currentPost.tags
    return render_template('posts/mypost.html', mypost=currentPost, mytags=tags)


@posts.route('/tag/<slug>')
def mytag(slug):
    currentTag = Tag.query.filter(Tag.slug == slug).first()
    posts = currentTag.posts.all()
    return render_template('posts/mytag.html', mytag=currentTag, allposts=posts)

# encoding: utf-8

from flask import Flask, render_template, request, redirect, url_for, session, g
from exts import db
from models import User, Blog, Comment
from functools import wraps
import config
from sqlalchemy import or_

app = Flask(__name__)
app.config['SECRET_KEY'] = 'malizhi123.'
app.config.from_object(config)
app.static_folder = 'static'
db.init_app(app)


@app.route('/')
def index():
    context = {
        'blogs': Blog.query.all()
    }
    return render_template('index.html', **context)


@app.route('/sign_in', methods={'GET', 'POST'})
def sign_in():
    if request.method == 'GET':
        return render_template('sign_in.html')
    else:
        email = request.form['email']
        password = request.form['password']
        # remember = request.form['remember']
        user = User.query.filter(User.email == email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            # if re:
            #     session.permanent = True
            # else:
            session.permanent = False
            return redirect(url_for('index'))
        else:
            return u'Email or password is wrong, please confirm and login again'


@app.route('/sign_up', methods={'GET', 'POST'})
def sign_up():
    if request.method == 'GET':
        return render_template('sign_up.html')
    else:
        username = request.form['username']
        email = request.form['email']
        password1 = request.form['password1']
        password2 = request.form['password2']

        # an email can only register an account
        user = User.query.filter(User.email == email).first()
        if user:
            return u'The email account has been registered'
        else:

            if password1 != password2:
                return u'The passwords entered are not the same, please fill in after checking'
            else:
                current_user = User(username=username, email=email, password=password1)
                db.session.add(current_user)
                db.session.commit()
                # current_user = User.query.filter_by(email=email).first()
                # login_user(current_user)
                return redirect(url_for('sign_in'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('sign_in'))


# 登录限制的装饰器
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id'):  # 如果用户登录了
            return func(*args, **kwargs)  # 返回的是某个页面 记得func前面要加return 不然会产生return render_template('center.html')这样类似的功能
        else:
            return redirect(url_for('sign_in'))

    return wrapper


@app.route("/write_blog", methods={'GET', 'POST'})
@login_required
def write_blog():
    if request.method == 'GET':
        return render_template('write_blog.html')
    else:
        title = request.form['title']
        content = request.form['content']
        blog = Blog(title=title, content=content)  # Add this model
        blog.author = g.user
        db.session.add(blog)
        db.session.commit()
        # Jump to the home page to see your answers immediately after Posting the q&A
        return redirect(url_for('index'))


@app.route('/detail/<blog_id>')
def detail(blog_id):
    blog = Blog.query.filter(Blog.id == blog_id).first()
    len = 0
    for comment in blog.comments:
        len += 1
    return render_template('detail.html', blog=blog,len=len)


@app.route('/add_comment/', methods=['POST'])
@login_required
def add_comment():
    content = request.form['content']
    blog_id = request.form['blog_id']
    comment = Comment(content=content)

    comment.author = g.user
    blog = Blog.query.filter(Blog.id == blog_id).first()
    comment.blog = blog
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('detail', blog_id=blog_id))


@app.route('/search/')
def search():
    q = request.args.get('q')
    # title or content
    blogs = Blog.query.filter(or_(Blog.title.contains(q), Blog.content.contains(q)))
    return render_template('index.html', blogs=blogs)


@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user


@app.context_processor
def my_context_processor():
    if hasattr(g,'user'):
        return {'user': g.user}
    return {}


if __name__ == '__main__':
    app.run()

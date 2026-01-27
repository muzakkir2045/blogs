
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user
from flask_login import LoginManager, UserMixin,login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import time
import markdown


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "supersecretkey"

# Initialize database and login manager
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# User Model
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(250), unique = True, nullable = False)
    password = db.Column(db.String(250), nullable = False)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    date_time = db.Column(db.String(100), unique = False, nullable = False)

with app.app_context():
    db.create_all()

# Load user for flask-login
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route("/")
def home():
    return redirect(url_for("register"))

@app.route('/register', methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if Users.query.filter_by(username = username).first():
            return render_template("sign_up.html", error = "Username already taken!")
        
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        new_user = Users(username = username, password = hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("sign_up.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = Users.query.filter_by(username = username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error = "Invalid username or password")
        
    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    # post = Post.query.all()
    posts = Post.query.order_by(Post.id.desc()).all()
    preview_posts = []

    for post in posts:
        preview_posts.append(
            {
                "id":post.id,
                "title":post.title,
                "excerpt":make_excerpt(post.content),
                "date":post.date_time
            }
        )

    return render_template("dashboard.html",
     username = current_user.username, 
     posts = preview_posts)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/new",methods = ['GET','POST'])
@login_required
def new_post():
    if request.method == "POST":
        print(request.form)
        title = request.form.get('blog_title')
        text = request.form.get('blog_text')        
        if title != '' and text != '':
            html_content = markdown.markdown(
                text,extensions=["extra","fenced_code", "tables"]
            )
            post = Post(
                title = title,
                content = html_content,
                user_id = current_user.id,
                date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            )  

            db.session.add(post)
            db.session.commit()
            return redirect('/dashboard')
    return render_template('new_blog.html')

@app.route('/delete/<int:id>')
def erase(id):
    data = Post.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/dashboard')

@app.route('/update/<int:id>', methods = ['GET','POST'])
@login_required
def update(id):
    post = Post.query.get(id)
    if request.method == 'POST':
        post.title = request.form.get("blog_title")
        post.content = request.form.get("blog_text")
        html_content = markdown.markdown(
                post.content,extensions=["extra","fenced_code", "tables"]
            )
        post.content = html_content
        db.session.commit()
        return redirect("/dashboard")


    return render_template('/edit_blog.html', post=post)


@app.route('/view/<int:id>')
@login_required
def view(id):
    post = Post.query.get(id)
    return render_template('post.html', post = post)


import re

def make_excerpt(html,length=90):
    text = re.sub('<[^<]+?>','',html)
    text = ' '.join(text.split())
    if len(text) > length:
        return text[:length] + "..."
    return text

""" for the change : adding make_excerpt function
and updating the dashboard.html
https://chatgpt.com/s/t_6978e2b156308191897fbd3efbc70230
"""


if __name__ == "__main__":
    app.run(debug= True)
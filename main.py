from flask import Flask, render_template, request, redirect, flash, url_for
import requests
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    # Check if user is in paid_user table

    # If not, check if user is in free_user table
    user = User.query.get(int(user_id))
    if user:
        return user
    # If user is not in either table, return None
    return None


app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
with app.app_context():
    class User(UserMixin, db.Model):
        id=db.Column(db.Integer, primary_key=True)
        name=db.Column(db.String(100))
        phone= db.Column(db.String(100), unique=True)
        password=db.Column(db.String(100))



    class Posts(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100))
        phone = db.Column(db.String(100))
        title = db.Column(db.String(1000))
        sub=db.Column(db.String(1000))
        date = db.Column(db.DateTime())



    db.create_all()


class MyModelView(ModelView):
    def is_accessible(self):
        return True

admin = Admin(app)
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Posts, db.session))


@app.route("/")
def start():
    posts=Posts.query.all()
    return render_template("index.html",posts=posts)

@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        number = request.form.get('phone')
        password = request.form.get('password')
        user = User.query.filter_by(phone=number).first()
        if not user:
            flash("That email does not exist, please try again.")

            # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')

        # Email exists and password correct
        else:
            login_user(user)
            return redirect("/")




    return render_template("login.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if User.query.filter_by(phone=request.form.get('phone')).first():
            # User already exists
            flash("You've already signed up with that number, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            phone=request.form.get('phone'),
            name=request.form.get('name'),
            password=hash_and_salted_password

        )
        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")











if __name__=="__main__":
    app.run(debug=True)
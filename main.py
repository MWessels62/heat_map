from data import getData
from flask import Flask,  render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

#initialize flask ap
app = Flask(__name__)


#this would be space to set up the code for the login page



#when you run this, it will create a flask server, once you click on the link for it which should be localhost:5000 in your browser, you'll see the home page I've kind of made.

#configure flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heatmapApp.db'
#configure Bcrypt for passwords later
Bcrypt = Bcrypt(app)
#configure database
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'thisIsTheKey'

#initialize LoginManager() that contains the code that lets the app and Flask work together
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

#create a user loader function
@login_manager.user_loader

def load_user(user_id):
    return User.query.get(int(user_id))
 
#create a User Table in our database using UserMixin
class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    #cannot use the same username
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

#create a Registration form for our signup Page using FlaskForm
class RegisterForm(FlaskForm):

    username = StringField(validators=[InputRequired(),Length(min=4, max=20)], render_kw ={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(),Length(min=4,max=20)], render_kw={"placeholder":"Password"})
    submit = SubmitField("Register")
    #create a function to check if the username already exists
    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username= username.data).first()
        if existing_user_username:
            raise ValidationError(
                "That username already exists. Please choose a different one")

#create a LoginForm for our Login page
class LoginForm(FlaskForm):

    username = StringField('Username',validators=[InputRequired(),Length(min=4, max =20)], render_kw ={"placeholder": "Username"})
    password = PasswordField('Password', validators=[InputRequired(),Length(min=4,max=20)], render_kw={"placeholder":"Password"})
    submit = SubmitField("Login")
     

#create a log out route, just redirects to index page
@app.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')

#create route for Login
@app.route('/dashboard', methods =['GET', 'POST'])
@login_required
def dashboard():
    #render home page
    return render_template('dashboard.html')


#create a route for the sign up page
@app.route('/signUp', methods =['GET', 'POST'])
def register():
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        pasw = form.password.data
        hashed_password = Bcrypt.generate_password_hash(pasw).decode('utf-8')
        new_user = User(username= form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/Login')

    return render_template('signUp.html', form = form)



#create route for home page
@app.route('/', methods=["GET","POST"])
def login():
    
    form = LoginForm()
    #check if user exists
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if Bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                #open dashboard if username + password successful
                return redirect(url_for('dashboard'))
    #else just render login page
    return render_template('Login.html', form = form)


if __name__ == "__main__":
    app.run(debug=True)
from multiprocessing import Value
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm
from sqlalchemy import values
from wtforms import  SubmitField, PasswordField, StringField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt



# instanciation d'un objet de cette classe, l'objet est donc l'application elle-même
app = Flask(__name__)

# Création d'une base de donnée que nous pourron utilisée plus tard
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = 'Coline05be'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(1000), nullable=False)

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw= {"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw= {"placeholder": "Password"})
    submit = SubmitField("Register")


    def validate_username(self, username):
        déjaUtilisé = User.query.filter_by(username=username.data).first()
        if déjaUtilisé:
            raise ValidationError("This username already exists. Please choose a different one.")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw= {"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw= {"placeholder": "Password"})
    submit = SubmitField("Login")



@app.route('/profile')
def profile():
    return render_template('pages/profile.html')

@app.route('/')
def home():
    return render_template('pages/home.html')

@app.route("/choicelesson")
def choicelesson():
    return render_template('pages/choicelesson.html')

@app.route("/lesson/<numero_lesson>")
def lesson(numero_lesson):
    numero = numero_lesson
    return render_template('pages/lesson.html', numero = numero_lesson)

@app.route("/contact")
def contact():
    return render_template('pages/contact.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/page_not_found.html'), 404

@app.route("/Phrase")
def phrase():
    return render_template('pages/phrases.json')
# 
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    variableRegister = RegisterForm()

    if variableRegister.validate_on_submit():
        motdepasseHaché = bcrypt.generate_password.hash(variableRegister.password.data)
        Nouvel_Utilisateur = User(username=variableRegister.username.data, password=motdepasseHaché)
        db.session.add(Nouvel_Utilisateur)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('pages/signup.html', form=variableRegister)
# 
@app.route('/login', methods=['GET', 'POST'])
def login():
    variableform = LoginForm()
    return render_template('pages/login.html', form=variableform)
    


if __name__ == '__main__':
    app.run(debug=True)
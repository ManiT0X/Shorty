from flask_login import UserMixin, LoginManager
from flask_wtf.csrf import CSRFProtect
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from blueprints.home.home import home
from blueprints.about.about import about
from blueprints.user.login import login
from blueprints.user.register import register
from blueprints.user.profile import profile
from blueprints.FAQ.faq import faq
from blueprints.contact.contact import contact

app = Flask(__name__)
Bootstrap(app)
CSRFProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


app.register_blueprint(home)
app.register_blueprint(about)
app.register_blueprint(login)
app.register_blueprint(register)
app.register_blueprint(profile)
app.register_blueprint(faq)
app.register_blueprint(contact)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
app.config['SECRET_KEY'] = 'j0k00458tef48m6p96jut11k4ui50rl6'

db = SQLAlchemy(app)


class LinksData(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    full_link = db.Column(db.String(800), nullable=False)
    link_description = db.Column(db.String(800), nullable=True)
    short_link = db.Column(db.String(80), unique=True, nullable=False)
    short_link_id = db.Column(db.String(30), unique=True, nullable=False)
    creation_date = db.Column(db.String(30), nullable=False)
    num_visits = db.Column(db.Integer, nullable=False)
    user = db.Column(db.String(125), nullable=False)


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    type = db.Column(db.String(100))
    date = db.Column(db.String(100))
    ip_address = db.Column(db.String(100))


class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link_id = db.Column(db.String(250))
    link_owner = db.Column(db.String(250))
    user_agent = db.Column(db.String(250))
    ip = db.Column(db.String(250))
    country = db.Column(db.String(250))
    city = db.Column(db.String(250))
    browser = db.Column(db.String(250))
    os = db.Column(db.String(250))
    device = db.Column(db.String(250))
    date = db.Column(db.String(250))


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)

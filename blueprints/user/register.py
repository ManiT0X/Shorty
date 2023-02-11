from flask import Blueprint, render_template, request
from werkzeug.security import generate_password_hash
import datetime

DATE = datetime.date.today()

register = Blueprint('register', __name__, template_folder='templates', url_prefix='/register')


@register.route('/', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        from main import Users, db, app
        with app.app_context():
            if Users.query.filter_by(username=request.form.get('username')).first():
                print('username is already taken')
                return {"error": "username taken"}, 409
            if Users.query.filter_by(email=request.form.get('email')).first():
                print('email already in use')
                return {"error": "email in use"}, 409
            else:
                new_user = Users(
                    email=request.form.get('email'),
                    username=request.form.get('username'),
                    password=generate_password_hash(password=request.form.get('password'), method='pbkdf2:sha256', salt_length=8),
                    type="user",
                    date=DATE,
                    ip_address=request.remote_addr
                )
                db.session.add(new_user)
                db.session.commit()
                return {"status": "success"}, 200
    else:
        return render_template('register.html'), 200

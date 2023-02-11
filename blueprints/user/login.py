from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash

login = Blueprint('login', __name__, template_folder='templates', url_prefix='/login')


@login.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        from main import Users, app
        with app.app_context():
            if Users.query.filter_by(email=request.form.get('email')).first():
                user = Users.query.filter_by(email=request.form.get('email')).first()
                if check_password_hash(user.password, request.form.get('password')):
                    login_user(user)
                    return {"status": "success"}, 200
                else:
                    return {"error": "wrong password"}
            else:
                return {"error": "user does not exist"}
    return render_template('login.html')


@login.route('/out')
def logout():
    logout_user()
    return redirect(url_for('home.home_page'))

from flask import Blueprint, render_template, redirect, url_for, jsonify, request
from flask_login import current_user, login_required
from functions import QRCode, ShortLinkID
import datetime
DATE = datetime.date.today()

profile = Blueprint('profile', __name__, template_folder='templates', static_folder='static', url_prefix='/user')


@profile.route('/', methods=['GET', 'POST'])
def profile_page():
    if request.method == 'POST':
        from functions import check_http
        short_link_id = ShortLinkID().generate_shortlink(5)
        full_link = check_http(request.form.get('full_link'))
        from main import app, db, LinksData
        with app.app_context():
            new_shot_link = LinksData(
                full_link=full_link,
                short_link=request.host_url + short_link_id,
                short_link_id=short_link_id,
                creation_date=DATE,
                num_visits=0,
                user=current_user.username,
                link_description=request.form.get('link_description')
            )
            db.session.add(new_shot_link)
            db.session.commit()
            QRCode().generate_qr(link=full_link, id=short_link_id, username=current_user.username)
            return {"status": "ok"}, 200
    if current_user.is_authenticated:
        from main import app, LinksData
        with app.app_context():
            data = LinksData.query.filter_by(user=current_user.username).all()
            return render_template('profile.html', current_user=current_user, data=data)
    else:
        return redirect(url_for('home.home_page'))


@profile.route('/update/<update_type>', methods=['GET', 'POST'])
def update(update_type):
    from main import app, db, LinksData
    from functions import QRCode, check_http
    with app.app_context():
        if update_type == 'link':
            try:
                link_id = request.form.get('id')
                new_link = check_http(request.form.get('updatedLink'))
                link = LinksData.query.filter_by(id=link_id).first()
                link.full_link = new_link
                db.session.commit()
                QRCode().generate_qr(link=new_link, id=link.short_link_id, username=current_user.username)
                return {"status": "success", "qr_image": f"qr_imgs/{current_user.username}/{link.short_link_id}.png"}
            except Exception as e:
                print(e)
                return "Error updating link", 500
        if update_type == 'description':
            try:
                link_id = request.form.get('id')
                new_description = request.form.get('description')
                link = LinksData.query.filter_by(id=link_id).first()
                link.link_description = new_description
                db.session.commit()
                return {"status": "success", "description": new_description}, 200
            except Exception as e:
                print(e)
                return "Error updating description", 500


@profile.route("/get-data/<short_link_id>")
def get_data(short_link_id):
    from functions import link_info, chart_data
    return jsonify(link_info(short_link_id), chart_data(short_link_id))


@profile.route("/delete/<short_link_id>", methods=['GET', 'POST'])
def delete(short_link_id):
    if current_user.is_authenticated:
        from main import app, db, LinksData, Visitor
        import os
        with app.app_context():
            try:
                link = LinksData.query.filter_by(short_link_id=short_link_id).first()
                if link.user == current_user.username:
                    db.session.delete(link)
                    db.session.commit()
                    qr_img = f"./static/qr_imgs/{current_user.username}/{short_link_id}.png"
                    os.remove(qr_img)
                    try:
                        visits = Visitor.query.filter_by(link_id=short_link_id).all()
                        for visit in visits:
                            db.session.delete(visit)
                        db.session.commit()
                        return {"status": "success, data deleted"}, 200
                    except :
                        return "no visits found"
                else:
                    return redirect(url_for('profile.profile_page'))
            except AttributeError:
                return redirect(url_for('profile.profile_page'))
    else:
        return redirect(url_for('home.home_page'))

from flask import Blueprint, render_template, request, send_from_directory, redirect
from flask_login import current_user
from functions import QRCode, ShortLinkID
import datetime


DATE = datetime.date.today()
home = Blueprint('home', __name__, template_folder='templates', static_folder='static')


@home.route('/', methods=['GET', 'POST'])
def home_page():
    from functions import check_http
    if request.method == 'POST':
        if current_user.is_authenticated:
            short_link_id = ShortLinkID().generate_shortlink(5)
            full_link = check_http(request.form.get('long_url'))
            from main import app, db, LinksData
            with app.app_context():
                new_shot_link = LinksData(
                    full_link=full_link,
                    short_link_id=short_link_id,
                    short_link=request.host_url + short_link_id,
                    creation_date=DATE,
                    num_visits=0,
                    user=current_user.username
                )
                db.session.add(new_shot_link)
                db.session.commit()
                QRCode().generate_qr(link=full_link, id=short_link_id, username=current_user.username)
                return {"qr_image": f"qr_imgs/{current_user.username}/{short_link_id}.png",
                        "shortlink": short_link_id}, 200
        else:
            short_link_id = ShortLinkID().generate_shortlink(5)
            full_link = check_http(request.form.get('long_url'))
            from main import app, db, LinksData
            with app.app_context():
                new_shot_link = LinksData(
                    full_link=full_link,
                    short_link=request.host_url + short_link_id,
                    short_link_id=short_link_id,
                    creation_date=DATE,
                    num_visits=0,
                    user='visitor'
                )
                db.session.add(new_shot_link)
                db.session.commit()
                QRCode().generate_qr(link=full_link, id=short_link_id, username=None)
                return {"qr_image": f"qr_imgs/{short_link_id}.png", "shortlink": short_link_id}
    return render_template('index.html', current_user=current_user)


@home.route('/<short_link_id>')
def redirect_page(short_link_id):
    from main import app, db, LinksData
    from functions import check_http, visitor_info
    with app.app_context():
        if LinksData.query.filter_by(short_link_id=short_link_id).first():
            link = LinksData.query.filter_by(short_link_id=short_link_id).first()
            link.num_visits += 1
            db.session.commit()
            target = check_http(link.full_link)
            # add visitor info to db
            ua_string = str(request.user_agent)
            ip = request.remote_addr
            visitor_info(ip, link.short_link_id, ua_string, link.user)
            return redirect(target)
        else:
            return {"Error": "Page Not Found"}, 404


@home.route('/download/qr/<filename>')
def download(filename):
    if current_user.is_authenticated:
        return send_from_directory('static', f"qr_imgs/{current_user.username}/{filename}.png", as_attachment=True)
    return send_from_directory('static', f"qr_imgs/{filename}.png", as_attachment=True)

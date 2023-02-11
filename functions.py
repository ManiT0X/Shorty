from flask_login import current_user
import qrcode
import os
import random
import string
import requests
from user_agents import parse
import datetime
DATE = datetime.date.today()


class QRCode:
    def generate_qr(self, link, id, username):
        if username:
            if not os.path.exists(f"{os.getcwd()}\static\qr_imgs\\{username}\\"):
                os.mkdir(f"{os.getcwd()}\static\qr_imgs\\{username}\\")

            path = f"{os.getcwd()}\static\qr_imgs\\{username}\\"
            img = qrcode.make(link)
            type(img)  # qrcode.image.pil.PilImage
            if os.path.exists(f"{path}{id}.png"):
                print(f"{path}{id}.png")
                print('file exist')
                os.remove(f"{path}{id}.png")
                print('file deleted')
            img.save(path + f"{id}.png")
            print(path + f"{id}.png")
            print('file saved')

        else:
            path = f"{os.getcwd()}\static\qr_imgs\\"
            if not os.path.exists(path):
                os.mkdir(path)
            img = qrcode.make(link)
            type(img)  # qrcode.image.pil.PilImage
            img.save(path + f"{id}.png")
        return 'ok'


class ShortLinkID:
    def generate_shortlink(self, length):
        letters = string.ascii_lowercase
        short_link = ''.join(random.choice(letters) for i in range(length))
        from main import app, LinksData
        with app.app_context():
            if LinksData.query.filter_by(short_link_id=short_link).first():
                ShortLinkID()
        return short_link


def link_info(short_link_id):
    from main import LinksData, app
    with app.app_context():
        if not short_link_id:
            return 'error'
        try:
            i = LinksData.query.filter_by(short_link_id=short_link_id).first()
            id = i.id
            full_link = i.full_link
            creation_date = i.creation_date
            num_visits = i.num_visits
            short_link = i.short_link
            qr_img = f"qr_imgs/{current_user.username}/{i.short_link_id}.png"
            description = i.link_description
            return id, full_link, creation_date, num_visits, short_link, qr_img, description, i.short_link_id
        except AttributeError:
            return "id does not exist"


def check_http(link):
    if link.find("http://") != 0 and link.find("https://") != 0:
        http_link = "http://" + link
        return http_link
    return link


def visitor_info(ip, link, ua_sting, owner):
    try:
        ip_lookup_endpoint = f"http://www.geoplugin.net/json.gp?ip={ip}"
        response = requests.get(f"{ip_lookup_endpoint}{ip}").json()
        city = response['geoplugin_city']
        country = response['geoplugin_countryName']
    except:
        city = 'none'
        country = "none"
    try:
        user_agent = parse(ua_sting)
        browser = f"{user_agent.browser.family} {user_agent.browser.version[0]}"
        user_os = f"{user_agent.os.family} {user_agent.os.version[0]}"
        device = f"{user_agent.device.family} {user_agent.device.brand} {user_agent.device.model}"
    except:
        browser = "none"
        user_os = "none"
        device = "none"
    from main import app, db, Visitor

    with app.app_context():
        new_visitor = Visitor(
            user_agent=ua_sting,
            ip=ip,
            link_id=link,
            country=country,
            city=city,
            browser=browser,
            os=user_os,
            device=device,
            date=DATE,
            link_owner=owner,
            )
        db.session.add(new_visitor)
        db.session.commit()


def chart_data(short_url_id):
    from main import Visitor, app, db
    from sqlalchemy import func
    with app.app_context():
        visitors = (
            db.session.query(
                func.date(Visitor.date).label('date'),
                func.count(Visitor.id).label('visits')
            )
            .filter(Visitor.link_id == short_url_id)
            .group_by(func.date(Visitor.date))
            .order_by(func.date(Visitor.date))
            .limit(15)
            .all()
        )
        dates = [row.date for row in visitors]
        visits = [row.visits for row in visitors]
        visitors_os = (
            db.session.query(
                Visitor.os.label('os'),
                func.count(Visitor.id).label('visits')
            )
                .filter(Visitor.link_id == short_url_id)
                .group_by(Visitor.os)
                .order_by(Visitor.os)
                .limit(7)
                .all()
        )
        os = [row.os for row in visitors_os]
        os_visits = [row.visits for row in visitors_os]

        visitors_device = (
            db.session.query(
                Visitor.device.label('device'),
                func.count(Visitor.id).label('visits')
            )
                .filter(Visitor.link_id == short_url_id)
                .group_by(Visitor.device)
                .order_by(Visitor.device)
                .limit(7)
                .all()
        )
        device = [row.device for row in visitors_device]
        device_visits = [row.visits for row in visitors_device]

        visitors_country = (
            db.session.query(
                Visitor.country.label('country'),
                func.count(Visitor.id).label('visits')
            )
                .filter(Visitor.link_id == short_url_id)
                .group_by(Visitor.country)
                .order_by(Visitor.country)
                .limit(5)
                .all()
        )
        countries = [row.country for row in visitors_country]
        country_visits = [row.visits for row in visitors_country]

        visitors_browser = (
            db.session.query(
                Visitor.browser.label('browser'),
                func.count(Visitor.id).label('visits')
            )
                .filter(Visitor.link_id == short_url_id)
                .group_by(Visitor.browser)
                .order_by(Visitor.browser)
                .limit(5)
                .all()
        )
        browsers = [row.browser for row in visitors_browser]
        browser_visits = [row.visits for row in visitors_browser]
        background_color = ['rgb(255, 99, 132)','rgb(54, 162, 235)','rgb(255, 205, 86)',
                              'rgb(0, 63, 92)','rgb(88, 80, 141)','rgb(88, 134, 165)',
                              'rgb(249, 93, 106)','rgb(160, 81, 149)', 'rgb(161, 179, 194)',
                              'rgb(181, 213, 197)','rgb(176, 139, 187)','rgb(236, 168, 105)']
    return dates, visits,\
           os, os_visits, background_color[:len(os)],\
           device, device_visits, background_color[:len(device)],\
           countries,country_visits, background_color[:len(countries)], \
           browsers, browser_visits, background_color[:len(browsers)]


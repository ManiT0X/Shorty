from flask import Blueprint, render_template

contact = Blueprint('contact', __name__, template_folder="templates", static_folder="static", url_prefix="/contact")


@contact.route('/')
def contact_page():
    return render_template('contact.html')

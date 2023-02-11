from flask import Blueprint, render_template

faq = Blueprint('faq', __name__, template_folder="templates", static_folder="static", url_prefix="/faq")


@faq.route('/')
def faq_page():
    return render_template('faq.html')

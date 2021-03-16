from flask import abort
from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import current_app
from datetime import datetime
from datetime import timezone

from app import logic
from app import myemail
from app import utils
from app.forms import EmailForm

from authy.api import AuthyApiClient
from flask import (Flask, Response, request, redirect,
    render_template, session, url_for)

import os

import uuid
from app import gsheet


webapp_bp = Blueprint('main', __name__)
error_bp = Blueprint('errors', __name__)


@webapp_bp.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@webapp_bp.route('/', methods=['POST', 'GET'])
def secure_url():
    uuid = str(session.get('uuid'))
    return redirect(url_for('main.line', r_code=uuid))

@webapp_bp.route('/line/')
def line():
    # if request.method == "POST":
        # uuid = request.args.get('user')
    uuid = str(session.get('uuid'))

    r_code = uuid
    return render_template(
        'line.html',
        uuid=uuid, r_code=r_code)

@error_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@error_bp.app_errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


api = AuthyApiClient(os.environ['AUTHY_API_KEY'])

@webapp_bp.route("/join/<code>", methods=["GET", "POST"])
def phone_verification(code):
    ref_code = code
    # print (ref_code)
    if request.method == "POST":


        country_code = request.form.get("country_code")
        phone_number = request.form.get("phone_number")
        method = request.form.get("method")
        session['country_code'] = country_code
        session['phone_number'] = phone_number
        session['referral_code'] = ref_code

        api.phones.verification_start(phone_number, country_code, via=method)

        return redirect(url_for("main.verify"))

    return render_template("phone_verification.html", ref_code=ref_code)


@webapp_bp.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
            token = request.form.get("token")

            phone_number = session.get("phone_number")
            country_code = session.get("country_code")
            ref_code = session.get('referral_code')

            verification = api.phones.verification_check(phone_number,
                                                         country_code,
                                                         token)

            if verification.ok():
                # print("Country Code -", country_code)
                # print ("Phone Number -", phone_number)
                # print ("Referral Code -", ref_code)

                # print ("New User Code -", str(uuid.uuid4())[:8])

                # user_data = [(str(uuid.uuid4())[:8]), country_code + phone_number, ref_code]

                uid = (str(uuid.uuid4())[:8])
                phone_num = str(country_code + phone_number)
                referred_by = str(ref_code)

                gsheet.create_user(uid,phone_num,referred_by)
                session['uuid'] = uid
                return redirect(url_for('main.line'))

    return render_template("verify.html")
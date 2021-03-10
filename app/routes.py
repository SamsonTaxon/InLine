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

webapp_bp = Blueprint('main', __name__)
error_bp = Blueprint('errors', __name__)


@webapp_bp.route('/', methods=['POST', 'GET'])
def index():
    referring_uuid = request.args.get('user')
    form = EmailForm()
    if request.method == 'POST':
        if form.validate():
            email = utils.normalize_email(form.email.data)
            user = logic.get_user_by_email(email)

            if user is None:
                user = logic.create_user(email)

                myemail.send_verification_email(
                    user.id, user.email,
                    referring_uuid=referring_uuid)

            return redirect(url_for('main.waitlist', user=user.waitlist.uuid))

    elif request.method == 'GET':
        return render_template(
            'index.html', form=form, referring_uuid=referring_uuid)


@webapp_bp.route('/verify_email/<token>/')
def verify_email(token):
    logic.verify_email(token)
    return redirect(url_for('main.index'))


@webapp_bp.route('/waitlist/')
def waitlist():
    uuid = request.args.get('user')
    waitlist_user = logic.get_waitlist_user(uuid)
    if waitlist_user is None:
        return abort(404)
    else:
        waitlist_position = logic.get_waitlist_position(uuid)
        completed_referrals = logic.get_completed_referrals(uuid)
        return render_template(
            'waitlist.html',
            uuid=uuid,
            waitlist_position=waitlist_position,
            completed_referrals=completed_referrals)


@error_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@error_bp.app_errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


api = AuthyApiClient(os.environ['AUTHY_API_KEY'])


# @webapp_bp.route("/phone_verification", methods=["GET", "POST"])
# def phone_verification():
#     if request.method == "POST":
#         country_code = request.form.get("country_code")
#         phone_number = request.form.get("phone_number")
#         method = request.form.get("method")

#         session['country_code'] = country_code
#         session['phone_number'] = phone_number

#         api.phones.verification_start(phone_number, country_code, via=method)

#         return redirect(url_for('main.verify'))

#     return render_template("phone_verification.html")


# @webapp_bp.route("/verify", methods=["GET", "POST"])
# def verify(token):
#     if request.method == "POST":
#             token = request.form.get("token")

#             phone_number = session.get("phone_number")
#             country_code = session.get("country_code")

#             verification = api.phones.verification_check(phone_number,
#                                                          country_code,
#                                                          token)
#             phoneNumber = phone_number
#             if verification.ok(token):
#                 return Response("<h1>Success!</h1>")
#                 logic.verify_number(token)

#                 if user is None:
#                     user = logic.create_user_phone(phoneNumber)
#                     user.email_confirmed = True
#                     now = datetime.now(timezone.utc)
#                     user.email_confirmed_on = now
#                     user.save()

#     return render_template("verify.html")

@app.route("/signup/<code>", methods=["GET", "POST"])
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

        return redirect(url_for("verify"))

    return render_template("phone_verification.html", ref_code=ref_code)


@app.route("/verify", methods=["GET", "POST"])
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
                print("Country Code -", country_code)
                print ("Phone Number -", phone_number)
                print ("Referral Code -", ref_code)
                return Response("<h1>Success!</h1>")

    return render_template("verify.html")
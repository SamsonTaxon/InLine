from flask import abort
from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import current_app
from datetime import datetime
from datetime import timezone

# from app import logic
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


@webapp_bp.route('/line/', defaults={'rcode': None}, methods=["GET", "POST"])
@webapp_bp.route('/line/<rcode>', methods=["GET", "POST"])
def line(rcode):
    if rcode == None or len(rcode) < 8:
        uuid = str(session.get('uuid'))
        username = str(session.get('username'))

        if uuid == None or len(uuid) < 8:

            return redirect(url_for("main.index"))

        else:
            uuid = str(session.get('uuid'))

            r_code = uuid

            x = r_code

            current_data = gsheet.update(x)

            score = current_data[0]
            rank = current_data[1]

            return render_template(
                'line.html',
                uuid=uuid, r_code=r_code, username=username, score=score, rank=rank)

    else: 
        #samson make sure u check if this uuid is in the database
        #otherwise any 8 chars will pass u there wont be any data
        uuid = str(rcode)
        r_code = uuid
        username = str(session.get('username'))
        x = r_code
        current_data = gsheet.update(x)

        score = current_data[0]
        rank = current_data[1]
        return render_template(
            'line.html',
            uuid=uuid, r_code=r_code, username=username, score=score, rank=rank)

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

        username = request.form.get("Username")
        country_code = request.form.get("country_code")
        phone_number = request.form.get("phone_number")
        method = request.form.get("method")
        if str(username) not in (item for sublist in gsheet.get_unique_info() for item in sublist):
            session['country_code'] = country_code
            session['phone_number'] = phone_number
            session['referral_code'] = ref_code
            session['username'] = username
            print (country_code)
            print(phone_number)

            api.phones.verification_start(phone_number, country_code, via=method)

            return redirect(url_for("main.verify"))
            
        else:
            return render_template("phone_verification.html", ref_code=ref_code)

    return render_template("phone_verification.html", ref_code=ref_code)


@webapp_bp.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
            token = request.form.get("token")

            Username = session.get("username")
            phone_number = session.get("phone_number")
            country_code = session.get("country_code")
            print(phone_number)
            print(country_code)
            print(token)
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
                username = str(Username)

                gsheet.create_user(uid,phone_num,referred_by,username)
                session['uuid'] = uid
                session['username'] = username
                return redirect(url_for('main.line'))

    return render_template("verify.html")

@webapp_bp.route("/login", methods=["GET", "POST"])
def login():
    print ('here')
    if request.method == "POST":
        result = request.form
        print('its getting here samson')
        username = request.form.get("Username")
        country_code = request.form.get("country_code")
        phone_number = request.form.get("phone_number")

        phone_num = country_code+phone_number
        user_list = gsheet.get_user(phone_num)
        '''id  uuid    phone_number    referred_by Username    Score   Rank'''

        uid = str(user_list[1])
        username = str(user_list[4])
        print (uid)
        session['uuid'] = uid
        session['username'] = username

        return redirect(url_for('main.line'))

    return render_template("login.html")
# from datetime import datetime
# from datetime import timezone


# from sqlalchemy.exc import IntegrityError


# from app import utils
# from app.models import referrals
# from app.models import User
# from app.models import Waitlist
# from app.models import Users

# def get_user(user_id):
#     return User.query.filter_by(id=user_id).one_or_none()

# def get_user1(user_id):
#     return User1.query.filter_by(id=user_id).one_or_none()

# def get_user_by_email(email):
#     return User.query.filter_by(email=email).one_or_none()

# def get_user_by_phone(phone):
#     return User1.query.filter_by(phone_num=phone_num).one_or_none()

# # def get_waitlist_user(uuid):
# #     return Waitlist.query.filter_by(uuid=uuid).one_or_none()

# def get_waitlist_user(uuid):
#     return Users.query.filter_by(uuid=uuid).one_or_none()


# def get_userid():
#     return Users.query.filter_by(uuid=uuid).one_or_none()
# def get_user_number():
#     return Users.query.filter_by(phone_number=phone_number).one_or_none()



# def create_user(email):
#     email = utils.normalize_email(email)
#     user = User(email=email)
#     user.save()

#     waitlist_user = Waitlist(user.id)
#     waitlist_user.save()

#     return user

# def create_user1(phone_num):
#     user = User1(phone_num=phone_num)
#     user.save()

#     waitlist_user = Waitlist(user1.id)
#     waitlist_user.save()

#     return user


# def verify_email(token):
#     payload = utils.decode_jwt_token(token)
#     user = get_user(payload['user_id'])
#     if user is None:
#         return

#     if not user.email_confirmed:
#         user.email_confirmed = True
#         now = datetime.now(timezone.utc)
#         user.email_confirmed_on = now
#         user.save()

#     if payload['referring_uuid'] is not None:
#         refer(payload['referring_uuid'], user.waitlist.uuid)

# def refer(referring_uuid, referred_uuid):
#     referring_user = get_waitlist_user(referring_uuid)
#     referred_user = get_waitlist_user(referred_uuid)
#     try:
#         referring_user.referred.append(referred_user)
#         referring_user.score -= Waitlist.decrease_per_referral
#         referring_user.save()
#     except IntegrityError:
#         pass


# # def get_waitlist_position(uuid):
# #     waitlist_user = get_waitlist_user(uuid)
# #     score = waitlist_user.score
# #     users_ahead = Waitlist.query.filter(Waitlist.score <= score).count()
# #     return max(score, users_ahead)

# def get_waitlist_position(uuid):
#     waitlist_user = get_waitlist_user(uuid)
#     score = waitlist_user.score
#     users_ahead = Users.query.filter(Users.score <= score).count()
#     return max(score, users_ahead)

# def get_completed_referrals(uuid):
#     waitlist_user = get_waitlist_user(uuid)
#     return waitlist_user.referred.filter(
#         referrals.c.referring == waitlist_user.uuid).count()

# def make_user(user_data):
#     user_data = user_data
#     #looks like this
#     # user_data = [(str(uuid.uuid4())[:8]), country_code + phone_number, ref_code]
#     print (user_data)
#     # phone_number = phone_num
#     # phone_number = Users(phone_number=phone_number)
#     # phone_number.save()

#     # ref_by = referred_by
#     # referred_by = Users(referred_by=ref_by)
#     # referred_by.save()

#     # uuid = uid
#     # uuid = Users(uuid=uuid)
#     # uuid.save()
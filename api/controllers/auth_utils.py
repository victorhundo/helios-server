from jose import jwt
import sys, json, bcrypt, datetime, json
from api_utils import *
from  helios_auth.models import User

def password_check(user, password):

  if (user and user.info['password'] == bcrypt.hashpw(password.encode('utf8'), user.info['password'].encode('utf8'))):
      return True
  raise_exception(400,'Username or passoword invalid.')

def check_auth(token):
    if (token == None or token == 'null'):
        return False
    else:
        try:
            obj = jwt.decode(token, 'seKre8', algorithms=['HS256'])
            return obj
        except ValueError as err:
            return False

def auth_user(request):
    user = check_auth(request.META.get('HTTP_AUTHORIZATION'))
    if (not user):
        raise_exception(403, 'Forbidden.')
    return user

def get_user_session(username):
    user = User.get_by_type_and_id('password', username)
    if (user):
        return user
    raise_exception(404,'User not found.')

from jose import jwt

def password_check(user, password):
  return (user and user.info['password'] == bcrypt.hashpw(password.encode('utf8'), user.info['password'].encode('utf8')))

def check_auth(token):
    if (token == None or token == 'null'):
        return False
    else:
        try:
            obj = jwt.decode(token, 'seKre8', algorithms=['HS256'])
            return obj
        except ValueError as err:
            return False

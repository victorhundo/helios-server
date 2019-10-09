from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from django.contrib.auth.models import User
from rest_framework import serializers
from jose import jwt
from rest_framework.views import APIView

import helios_auth.models
import sys, json, bcrypt, datetime, json
from auth_utils import *
from api_utils import *

from .serializers import UserSerializer
auth = sys.modules['helios_auth.models']

class AuthSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')


class LoginViewSet(viewsets.ModelViewSet):
    queryset = User.objects.none()
    serializer_class = AuthSerializer

    def password_check(self, user, password):
      return (user and user.info['password'] == bcrypt.hashpw(password.encode('utf8'), user.info['password'].encode('utf8')))

    def create(self, request):
        try:
            print >>sys.stderr, request.body
            login = json.loads(request.body)
            username = login['username'].strip()
            password = login['password'].strip()
            user = auth.User.get_by_type_and_id('password', username)
            user_Serializer = UserSerializer(instance=user, context={'request': request})
            if self.password_check(user, password):
              expiry = datetime.date.today() + datetime.timedelta(days=50)
              token = jwt.encode({'username': username, 'expiry':str(expiry)}, 'seKre8',  algorithm='HS256')
              return Response({'status': '201', 'token':token, 'user': user_Serializer.data})

            raise ValueError('Bad Username or Password')
        except ValueError as err:
            return Response({'status': '400', 'message':str(err)}, status=status.HTTP_400_BAD_REQUEST)


class IsAuthViewsSet(APIView):
    def get(self, request):
        try:
            user = check_auth(request.META.get('HTTP_AUTHORIZATION'))
            if (user):
                return response(201, {'status': '201', 'hasLogged': True, 'username': user})
            else:
                raise_exception(401,'User not logged in to the system.')
        except Exception as err:
            return get_error(err)

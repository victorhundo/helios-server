from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from django.contrib.auth.models import User
from rest_framework import serializers

import helios_auth.models
import sys, json, bcrypt

auth = sys.modules['helios_auth.models']

class AuthSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')


class AuthViewSet(viewsets.ModelViewSet):
    queryset = User.objects.none()
    serializer_class = AuthSerializer

    def password_check(self, user, password):
      return (user and user.info['password'] == bcrypt.hashpw(password.encode('utf8'), user.info['password'].encode('utf8')))

    def create(self, request):
        try:
            login = json.loads(request.body)
            username = login['username'].strip()
            password = login['password'].strip()

            user = auth.User.get_by_type_and_id('password', username)
            if self.password_check(user, password):
              request.session['password_user_id'] = user.user_id
              return Response({'status': '201'})
            raise ValueError('Bad Username or Password')
        except ValueError as err:
            return Response({'status': '400', 'message':str(err)}, status=status.HTTP_400_BAD_REQUEST)

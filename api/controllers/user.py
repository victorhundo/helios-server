from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from helios_auth.models import User
from helios_auth.auth_systems import password

from .serializers import UserSerializer
import sys, json

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        try:
            user = json.loads(request.body)
            password.create_user(user['user_id'],user['info']['password'], user['name'])
            return Response({'status': '201'})
        except ValueError as err:
            return Response({'status': '400', 'message':str(err)}, status=status.HTTP_400_BAD_REQUEST)

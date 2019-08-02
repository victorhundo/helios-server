from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from helios_auth.models import User

from .serializers import UserSerializer
import sys, json

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
    def json2obj(self, data): return json.loads(data, object_hook=self._json_object_hook)

    def create(self, request):
        print >>sys.stderr, type(request.body)
        print >>sys.stderr, (request.body)
        user = json.loads(request.body)
        if user.is_valid():
            print >>sys.stderr, user
            user_obj = User.update_or_create(user['user_type'], user['user_id'], user['name'], user['info'], user['token'])
            return Response({'status': '201'})
        else:
            print >>sys.stderr, user
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

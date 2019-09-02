from django.core.urlresolvers import reverse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from helios.models import Election
from helios_auth.models import User

from auth_utils import *
from .serializers import ElectionSerializer
import sys, json, uuid, datetime


# ViewSets define the view behavior.
class EletctionViewSet(viewsets.ModelViewSet):
    queryset = Election.objects.all()
    serializer_class = ElectionSerializer


    def create(self, request):
        user = check_auth(request.META.get('HTTP_AUTHORIZATION'))
        if (user):
            try:
                election_params = json.loads(request.body)
                election_params['short_name'] = "%s_%s" % (election_params['short_name'], 'username')
                election_params['uuid'] = str(uuid.uuid1())
                #election_params['cast_url'] = settings.SECURE_URL_HOST + reverse(one_election_cast, args=[election_params['uuid']])
                election_params['cast_url'] = 'cast_url'
                election_params['openreg'] = False # registration starts closed
                election_params['admin'] = User.get_by_type_and_id('password','vhugo')
                election = Election.objects.create(**election_params)

                return Response({'status': '201'})
            except ValueError as err:
                return Response({'status': '400', 'message':str(err)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': '401', 'message': 'Unauthorized'})

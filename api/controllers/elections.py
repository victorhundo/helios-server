from django.core.urlresolvers import reverse
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from helios.models import Election
from helios_auth.models import User

from django.shortcuts import get_object_or_404

from auth_utils import *
from .serializers import ElectionSerializer
import sys, json, uuid, datetime

# ViewSets define the view behavior.
class EletctionViewSet(APIView):
    def get(self, request):
        queryset = Election.objects.all()
        print >>sys.stderr, ("OLHA ISSO >>> %s" % type(queryset))
        serializer_class = ElectionSerializer(queryset, many=True, context={'request': request})
        return Response(serializer_class.data)

    def post(self, request):
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
            return Response({'status': '401', 'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

class ElectionDetailView(APIView):
    def getElection(self, pk):
        queryset = Election.get_by_uuid(pk)
        if (queryset): return queryset

        queryset = Election.get_by_short_name(pk)
        if (queryset): return queryset

        return None

    def putQuestions(self, election, questions):
        save = Election.save_questions_safely(election, questions)
        if (save):
            election.save()
            return Response({'status': '201', 'message': 'Field Updated'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': '400', 'message':str(err)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        queryset = self.getElection(pk)
        if (queryset):
            serializer = ElectionSerializer(queryset, context={'request': request})
            print >>sys.stderr, ("OLHA ISSO >>> %s" % serializer.data)
            return Response(serializer.data)
        else:
            return Response({'status': '404', 'message': 'Election Not Found'}, status=status.HTTP_404_NOT_FOUND)


    def put(self, request, pk):
        queryset = self.getElection(pk)
        #serializer = ElectionSerializer(queryset, context={'request': request})
        if (queryset):
            body = json.loads(request.body)
            if (body["field"] == "questions" ):
                return self.putQuestions(queryset, body["value"])
            else:
                return Response({'status': '401', 'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'status': '404', 'message': 'Election Not Found'}, status=status.HTTP_404_NOT_FOUND)

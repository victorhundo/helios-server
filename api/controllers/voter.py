from django.core.urlresolvers import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from helios.models import Election, Voter
from helios_auth.models import User
from helios.crypto import algs, electionalgs, elgamal
from helios.crypto import utils as cryptoutils

from auth_utils import *
from .serializers import VoterSerializer
import sys, json, uuid, datetime

def getElection(pk):
    queryset = Election.get_by_uuid(pk)
    if (queryset): return queryset

    queryset = Election.get_by_short_name(pk)
    if (queryset): return queryset

    return None

class VoterView(APIView):
    def get(self, request, election_pk):
        election = getElection(election_pk)
        if (election):
            queryset = Voter.get_by_election(election)
            serializer_class = VoterSerializer(queryset, many=True, context={'request': request})
            return Response(serializer_class.data)
        else:
            return Response({'status': '404', 'message': 'Election Not Found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, election_pk):
        election = getElection(election_pk)
        if (election):
            queryset = Voter.get_by_election(election)
            serializer_class = VoterSerializer(queryset, many=True, context={'request': request})
            return Response(serializer_class.data)
        else:
            return Response({'status': '404', 'message': 'Election Not Found'}, status=status.HTTP_404_NOT_FOUND)

class VoterElebilityView(APIView):
    def post(self, request, election_pk):
        election = getElection(election_pk)
        if (election):
            try:
                req = json.loads(request.body)
                if req['eligibility'] in ['openreg', 'limitedreg']: election.openreg = True
                elif req['eligibility'] in ['closedreg', 'privatereg']: election.openreg= False
                else: election.openreg= None
                election.save()
                return Response({'status': '201', 'message': 'Field Updated'}, status=status.HTTP_201_CREATED)
            except ValueError as err:
                return Response({'status': '400', 'message':str(err)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': '404', 'message': 'Election Not Found'}, status=status.HTTP_404_NOT_FOUND)

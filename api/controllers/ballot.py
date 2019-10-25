import json, datetime
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from helios.models import Election, Voter, CastVote
from helios.crypto import utils as cryptoutils
from rest_framework.reverse import reverse


import api.tasks as api_task

import helios.datatypes as datatypes

from .elections import getElection
from .voter import create_voter, get_voter

from api_utils import raise_exception, response, serializer, get_error
from auth_utils import auth_user, get_user_session


class BallotView(APIView):
    def get(self, request, election_pk):
        try:
            """
            this will order the ballots from most recent to oldest.
            and optionally take a after parameter.
            """
            election = getElection(election_pk)
            limit = after = None
            if request.GET.has_key('limit'):
                limit = int(request.GET['limit'])
            if request.GET.has_key('after'):
                after = datetime.datetime.strptime(request.GET['after'], '%Y-%m-%d %H:%M:%S')

            voters = Voter.get_by_election(election, cast=True, order_by='cast_at', limit=limit, after=after)

            # we explicitly cast this to a short cast vote
            # res = [v.last_cast_vote().ld_object.short.toDict(complete=True) for v in voters]

            res = []
            for v in voters:
                cast = v.last_cast_vote().ld_object.short.toDict(complete=True)
                cast["url"] = reverse('ballot-last', args=[election_pk,v.uuid], request=request) 
                res.append(cast)
                
            # res = serializer(voters,request)
            return response(200,res)
        except Exception as err:
            return get_error(err)

class BallotDetailView(APIView):
    def get(self, request, election_pk, voter_pk):
        try:
            election = getElection(election_pk)
            voter = Voter.get_by_election_and_uuid(election, voter_pk)
            votes = CastVote.get_by_voter(voter)
            res = [v.toJSONDict()  for v in votes]
            return response(200,res)
        except Exception as err:
            return get_error(err)

class BallotLastView(APIView):
    def get(self,request,election_pk, voter_pk):
        try:
            election = getElection(election_pk)
            voter = Voter.get_by_election_and_uuid(election, voter_pk)
            res = voter.last_cast_vote().toJSONDict()
            return response(200,res)
        except Exception as err:
            return get_error(err)

class CelereyView(APIView):
    def get(self,request):
        try:
            api_task.slow_task.delay()
            return response(200, 'ok')
        except Exception as err:
            return get_error(err)
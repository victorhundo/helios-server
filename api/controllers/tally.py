from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from helios.models import Election
from helios_auth.models import User
from django.db.models.query import  QuerySet

from django.shortcuts import get_object_or_404

from auth_utils import *
from api_utils import *
from .serializers import ElectionSerializer
import sys, json, uuid
from .elections import getElection, needIsFrozen
from .voter import get_voter
from django.utils import timezone

from helios import tasks

def check_election_tally_type(election):
    for q in election.questions:
      if q['tally_type'] != "homomorphic":
          raise_exception(400,'Election is not ready for compute tally')

def check_number_voters(election_pk):
    voter = get_voter(election_pk)
    if (len(voter) <= 0): raise_exception(400, 'At least one vote must be cast before you do the tally')

# ViewSets define the view behavior.
class TallyViewSet(APIView):
    def post(self, request, election_pk):
        try:
            user = auth_user(request)
            election = getElection(election_pk)
            needIsFrozen(election)           
            check_number_voters(election_pk)
            check_election_tally_type(election)

            #Compute Tally
            if not election.voting_ended_at:
                election.voting_ended_at = timezone.now()
            election.tallying_started_at = timezone.now()
            election.save()
            tasks.election_compute_tally(election_id = election.id)

            #Combine Decrypyion
            election.combine_decryptions()
            election.save()

            return response(201, 'tally computed')
        except Exception as err:
                return get_error(err)
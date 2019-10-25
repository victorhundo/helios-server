# -*- coding: utf-8 -*-
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
import sys, json, uuid, datetime
from .elections import getElection, needIsFrozen
from .voter import get_voter
from django.utils import timezone

# from helios import tasks
from api.tasks import election_compute_tally

def check_election_tally_type(election):
    for q in election.questions:
      if q['tally_type'] != "homomorphic":
          raise_exception(400,'Election is not ready for compute tally')

def check_number_voters(election, election_pk):
    voter = get_voter(election_pk)
    if (len(voter) <= 0):
        if (timeOut(election)):
            emptyResult(election)
            return False
        else:
            raise_exception(400, 'At least one vote must be cast before you do the tally')
    return True

def timeOut(election):
    end_time = str(election.voting_ends_at)[:-6]
    if (end_time.count('.') == 0):
        end_time += '.000000'
    end_date = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S.%f")
    return end_date < datetime.datetime.now()

def emptyResult(election):
    result = []
    for q in election.questions:
        result.append([0] * len(q["answers"]))
    election.result = result
    election.save()

# ViewSets define the view behavior.
class TallyViewSet(APIView):
    def post(self, request, election_pk):
        try:
            user = auth_user(request)
            election = getElection(election_pk)
            needIsFrozen(election)           
            if (not check_number_voters(election, election_pk)):
                return response(201, 'empty tally computed')
            check_election_tally_type(election)

            #Compute Tally
            if not election.voting_ended_at:
                election.voting_ended_at = timezone.now()
            election.voting_ends_at = timezone.now()
            election.tallying_started_at = timezone.now()
            election.save()
            election_compute_tally.delay(election_id = election.id) #computar

            return response(201, 'tally computed')
        except Exception as err:
                return get_error(err)
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

def auth_user(request):
    user = check_auth(request.META.get('HTTP_AUTHORIZATION'))
    if (not user):
        raise_exception(403, 'Forbidden.')
    return user

def getElection(pk):
    queryset = Election.get_by_uuid(pk)
    if (queryset): return queryset

    queryset = Election.get_by_short_name(pk)
    if (queryset): return queryset

    raise_exception(404,'Election not Found.')

def needIsFrozen(election):
    if (not election.frozen_at):
        raise_exception(400,'Election need is frozen')

def putQuestions(election, field, value):
    if (field == "questions"):
        Election.save_questions_safely(election, value)
        election.save()
    else:
        raise_exception(400,'Field not exists.')

# ViewSets define the view behavior.
class EletctionViewSet(APIView):
    def get(self, request):
        queryset = Election.objects.all()
        res = serializer(queryset, request)
        return Response(res.data)

    def post(self, request):
        try:
            user = auth_user(request)
            election_params = json.loads(request.body)
            election_params['short_name'] = "%s_%s" % (election_params['short_name'], user['username'])
            election_params['uuid'] = str(uuid.uuid1())
            election_params['cast_url'] = reverse('elections-cast', args=[election_params['uuid']], request=request)
            election_params['openreg'] = False # registration starts closed
            election_params['admin'] = User.get_by_type_and_id('password',user['username'])
            election = Election.objects.create(**election_params)
            return response(201, {'uuid': election_params['uuid']})
        except Exception as err:
                return get_error(err)

class ElectionDetailView(APIView):
    def get(self, request, pk):
        try:
            election = getElection(pk)
            res = serializer(election,request)
            return Response(res.data)
        except Exception as err:
            return get_error(err)

    def put(self, request, pk):
        try:
            election = getElection(pk)
            body = json.loads(request.body)
            putQuestions(election, body["field"], body["value"])
            return response(201, 'Field Updated.')
        except Exception as err:
            return get_error(err)

    def delete(self, request,pk):
        try:
            election = getElection(pk)
            election.delete()
            response(202,'Election deleted.')
        except Exception as err:
            return get_error(err)

class ElectionCastView(APIView):
    def get(self, request, pk):
        return response(200,'ok')

class ElectionFreezeView(APIView):
    def post(self, request, election_pk):
        try:
            election = getElection(election_pk)
            election.freeze()
            return response(200,'Election %s freezed.' % election.uuid)
        except Exception as err:
            return get_error(err)
        return response(200,'ok')

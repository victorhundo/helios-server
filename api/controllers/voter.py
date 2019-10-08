from django.core.urlresolvers import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from rest_framework.parsers import MultiPartParser
from helios.models import Election, Voter
from helios_auth.models import User
from helios.crypto import algs, electionalgs, elgamal
from helios.crypto import utils as cryptoutils
from .elections import getElection
from helios import tasks

import base64
from validate_email import validate_email
from django.core.files.base import ContentFile

from auth_utils import *
from api_utils import *
from .serializers import VoterSerializer
import sys, json, uuid, datetime, bcrypt

def getFile(text):
    format, imgstr = text.split(';base64,') 
    ext = format.split('/')[-1] 
    data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
    return data

def check_the_file(voter_file_obj):
    voters = []
    try:
        return [v for v in voter_file_obj.itervoters()][:5]
    except:
        voters = []
        raise_exception(400, "your CSV file could not be processed. Please check that it is a proper CSV file.")

def get_voter(election_pk,pk=None):
    election = getElection(election_pk)
    if (pk):
        voter = Voter.get_by_election_and_uuid(election, pk)
        if (voter):
            return voter
        else:
            raise_exception(404,'Voter not Found.')
    else:
        return Voter.get_by_election(election)

def isOpenReg(req):
    return req['eligibility'] in ['openreg', 'limitedreg']

def get_user(pk):
    user = User.get_by_type_and_id('password', pk)
    if (user):
        return user
    else:
        raise_exception(404,'User not found.')

def check_voters_email(voters):
    if False in [validate_email(v['email']) for v in voters]:
        raise_exception(400, "those don't look like correct email addresses. Are you sure you uploaded a file with email address as second field?")

def create_voter(user,election):
    voter_uuid = str(uuid.uuid4())
    voter = Voter(
        uuid= voter_uuid,
        user = user,
        election = election,
        voter_password = user.info['password'],
        voter_login_id = user.user_id,
        voter_name = user.name )
    voter.save()
    return voter

class VoterView(APIView):
    def get(self, request, election_pk):
        try:
            voter = get_voter(election_pk)
            res = serializer(voter,request)
            return response(200, res.data)
        except Exception as err:
            return get_error(err)

    def post(self, request, election_pk):
        try:
            voter = get_voter(election_pk)
            res = serializer(voter,request)
            return response(200, res.data)
        except Exception as err:
            return get_error(err)

class VoterElebilityView(APIView):
    def post(self, request, election_pk):
        try:
            election = getElection(election_pk)
            req = json.loads(request.body)
            election.openreg = isOpenReg(req)
            election.save()
            return response(201,'Field Updated.')
        except Exception as err:
            return get_error(err)

class VoterViewDetail(APIView):
    def get(self, request, election_pk, pk):
        try:
            voter = get_voter(election_pk,pk)
            res = serializer(voter,request)
            return response(200,res.data)
        except Exception as err:
            return get_error(err)

    def delete(self,request,election_pk,pk):
        try:
            voter = get_voter(election_pk,pk)
            voter.delete()
            return response(202,'Voter deleted')
        except Exception as err:
            return get_error(err)

class VoterLoginView(APIView):
    def post(self,request,election_pk):
        try:
            election = getElection(election_pk)
            login = json.loads(request.body)
            username = login['username'].strip()
            password = login['password'].strip()
            user = get_user(username)
            password_check(user,password)
            voter = election.voter_set.get(voter_login_id = user.user_id, voter_password = user.info['password'])
            res = serializer(voter,request)
            return response(201,res.data)
        except Voter.DoesNotExist:
            voter = create_voter(user,election)
            res = serializer(voter,request)
            return response(201,res.data)
        except Exception as err:
            return get_error(err)

class VoterUploadFile(APIView):
    def post(self,request,election_pk):
        try:
            election = getElection(election_pk)
            voters_file = request.FILES['voters_file']
            problems = []
            voters = []
            voter_file_obj = election.add_voters_file(voters_file)
            # import the first few lines to check           
            voters = check_the_file(voter_file_obj)
            # check if voter emails look like emails
            check_voters_email(voters)
            tasks.voter_file_process(voter_file_id = voter_file_obj.id)
            return response(201,'voters created.')
        except Exception as err:
            return get_error(err)

import json
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from helios.models import Election, Voter, CastVote
from helios.crypto import utils as cryptoutils

import helios.tasks as tasks
import helios.datatypes as datatypes

from .elections import getElection
from .voter import create_voter

from api_utils import raise_exception, response, serializer, get_error
from auth_utils import auth_user, get_user_session

def get_cast_vote(election_pk, voter_pk):
    '''Get cast vote by election and voter keys.'''
    election = Election.get_by_uuid(election_pk)
    voter = Voter.get_by_election_and_uuid(election, voter_pk)
    return CastVote.get_by_voter(voter)

def create_cast_vote(encrypted_vote, voter, request):
    '''Create cast vote and verify and store.'''
    vote_fingerprint = cryptoutils.hash_b64(encrypted_vote)
    vote = datatypes.LDObject.fromDict(cryptoutils.from_json(encrypted_vote), type_hint='legacy/EncryptedVote').wrapped_obj
    cast_ip = request.META.get('REMOTE_ADDR', None)
    cast_vote_params = {
      'vote' : vote,
      'voter' : voter,
      'vote_hash': vote_fingerprint,
      'cast_at': timezone.now(),
      'cast_ip': cast_ip
    }
    cast_vote = CastVote(**cast_vote_params)
    cast_vote.save()

    # launch the verification task
    tasks.cast_vote_verify_and_store(cast_vote.id, 'status_update_message')

class CastVoteView(APIView):
    def get(self, request, election_pk, voter_pk):
        try:
            cast_vote = get_cast_vote(election_pk, voter_pk)
            res = serializer(cast_vote, request)
            return Response(res.data)
        except Exception as err:
            return get_error(err)

def get_encrypted_vote(request):
    return request.body


class CastElectionView(APIView):
    def post(self,request,election_pk):
        try:
            session = auth_user(request)
            if(session["username"] == "admin"):
                raise_exception(401, 'Admin is not allowed to be a voter.')
            user = get_user_session(session["username"])
            election = getElection(election_pk)
            body = get_encrypted_vote(request)
            voter = election.voter_set.get(voter_login_id = user.user_id, voter_password = user.info["password"])
            res = serializer(voter,request)
            create_cast_vote(body,voter,request)
            return response(200,res.data)
        except Voter.DoesNotExist:
            if (not election.openreg):
                raise_exception(401,'User not allowed to this election')
            voter = create_voter(user,election)
            return self.post(request,election_pk)
        except Exception as err:
            return get_error(err)

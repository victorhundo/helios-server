from rest_framework.views import APIView
from rest_framework.response import Response
from helios.models import Election, Voter, CastVote
from .elections import getElection
from .voter import create_voter
from django.contrib.auth.models import User
from helios.crypto import utils as cryptoutils
from helios.crypto import electionalgs, algs, utils
from django.utils import timezone
from helios import datatypes

from api_utils import *
from auth_utils import *
import sys, json, bcrypt, datetime, json
import helios.tasks as tasks


def getCastVote(election_pk, voter_pk):
    election = Election.get_by_uuid(election_pk)
    voter = Voter.get_by_election_and_uuid(election, voter_pk)
    return CastVote.get_by_voter(voter)

def createCastVote(encrypted_vote, voter,request):
    print >>sys.stderr, encrypted_vote
    vote_fingerprint = cryptoutils.hash_b64(encrypted_vote)
    vote = datatypes.LDObject.fromDict(utils.from_json(encrypted_vote), type_hint='legacy/EncryptedVote').wrapped_obj
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
            cast_vote = getCastVote(election_pk, voter_pk)
            res = serializer(cast_vote, request)
            return Response(res.data)
        except Exception as err:
            return get_error(err)


class CastElectionView(APIView):
    def post(self,request,election_pk):
        try:
            session = auth_user(request)
            user = get_user_session(session["username"])
            election = getElection(election_pk)
            encrypted_vote = json.loads(request.data["encrypted_vote"])
            voter = election.voter_set.get(voter_login_id = user.user_id, voter_password = user.info["password"])
            res = serializer(voter,request)
            createCastVote(request.data["encrypted_vote"],voter,request)
            return response(200,res.data)
            # print >>sys.stderr, "%s %s" % (user, encrypted_vote["election_uuid"])
            # return response(200,'ok')
        except Voter.DoesNotExist:
            voter = create_voter(user,election)
            return self.post(request,election_pk)
        except Exception as err:
            return get_error(err)

from rest_framework import serializers
from helios_auth.models import User
from helios.models import Election, Trustee, Voter, CastVote, VoterFile
from helios.crypto.elgamal import PublicKey
from rest_framework.reverse import reverse


import datetime, json, collections

def normalize_datetime(date):
    if (date == None): return None
    date = date.strftime("%Y-%m-%d %H:%M:%S.%f%z")
    result = date.split('.')[0]
    microsec = date.split('.')[1][:6]
    timezone = date.split('.')[1][6:]

    if (timezone == "" ):
        timezone = "+00:00"
    elif(timezone.count(':') == 0):
        timezone = timezone[:3] + ":" + timezone[3:]
        

    if (microsec == '000000'):
        microsec = ""
    else:
        microsec = "." + microsec

    return result + microsec + timezone



class EmptySerializer():
    def __init__(self, type):
        self.type = type
        if(type == 'list'): self.data = []
        else: self.data = None

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ElectionSerializer(serializers.ModelSerializer):
    
    public_key  = serializers.SerializerMethodField()
    questions  = serializers.SerializerMethodField()
    voting_starts_at  = serializers.SerializerMethodField()
    voting_ends_at = serializers.SerializerMethodField()
    frozen_at = serializers.SerializerMethodField()
    result = serializers.SerializerMethodField()

    class Meta:
        model = Election
        fields = (
            'cast_url',
            'description', 
            'frozen_at',
            'name',
            'openreg',
            'public_key',
            'questions',
            'short_name',
            'use_voter_aliases',
            'uuid',
            'voters_hash',
            'voting_ends_at',
            'voting_starts_at',
            'help_email',
            'tallying_started_at',
            'tallying_finished_at',
            'result'
        )
    def get_public_key(self,obj):
        if (obj.public_key== None): return None
        data = { 
            "g": str(obj.public_key.g), 
            "p": str(obj.public_key.p),
            "q": str(obj.public_key.q),
            "y": str(obj.public_key.y)
        }
        data_ordered = collections.OrderedDict(sorted(data.items(), key=lambda t: t[0]))
        return data_ordered

    def get_questions(self,obj):
        if (obj.questions == None): return None
        questions = []
        for q in obj.questions:
            data_ordered = collections.OrderedDict(sorted(q.items(), key=lambda t: t[0]))
            questions.append(data_ordered)
        return questions

    def get_voting_starts_at(self,obj):
        return normalize_datetime(obj.voting_starts_at)

    def get_voting_ends_at(self,obj):
        return normalize_datetime(obj.voting_ends_at)

    def get_frozen_at(self,obj):
        return normalize_datetime(obj.frozen_at)

    def get_result(self,obj):
        if (obj.result == None): return None
        questions = []
        for i in range(len(obj.result)):
            result = []
            for j in range(len(obj.result[i])):
                a = {}
                a["count_vote"] = obj.result[i][j]
                a["name_answer"] = obj.questions[i]["answers"][j]
                result.append(a)

            questions.append({"question": obj.questions[i]["question"], "result": result})
        return questions

class TrusteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trustee
        fields = ('uuid', 'name', 'email', 'public_key_hash', 'decryption_factors', 'decryption_proofs')


class VoterSerializer(serializers.ModelSerializer):
    vote_cast = serializers.SerializerMethodField()
    cast_at = serializers.SerializerMethodField()
    election = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    voter_hash = serializers.SerializerMethodField()
   
    class Meta:
        model = Voter
        fields = (
            'url', 
            'uuid', 
            'voter_name', 
            'voter_login_id', 
            'voter_email', 
            'voter_hash', 
            'alias', 
            'cast_at', 
            'election', 
            'user', 
            'vote_hash', 
            'vote_cast'
        )
    
    def get_url(self,obj):
        request = self.context.get('request')
        uuid = obj.uuid
        uuid_election = obj.election_uuid
        return reverse('voters-detail', args=[uuid_election,uuid], request=request)

    def get_voter_hash(self,obj):
        return obj.voter_id_hash

    def get_vote_cast(self, obj):
        # return obj.toJSONDict()
        request = self.context.get('request')
        uuid = obj.uuid
        uuid_election = obj.election_uuid
        return reverse('voter-cast', args=[uuid_election,uuid], request=request) 
    
    def get_cast_at(self,obj):
        return normalize_datetime(obj.cast_at)

    def get_election(self,obj):
        request = self.context.get('request')
        uuid = obj.election_uuid
        return reverse('election-detail', args=[uuid], request=request)

class CastVoteSerializer(serializers.ModelSerializer):
    vote = serializers.SerializerMethodField()
    cast_at = serializers.SerializerMethodField()

    class Meta:
        model = CastVote
        fields = ('vote', 'cast_at', 'vote_hash','voter_uuid', 'voter_hash')

    def get_vote(self,obj):
        return obj.toJSONDict()["vote"]
    
    def get_cast_at(self,obj):
        return normalize_datetime(obj.cast_at)

class PublicKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicKey
        fields = '__all__'

class VoterFileSerizlizer(serializers.ModelSerializer):
    voter_file_content = serializers.SerializerMethodField()
    uploaded_at = serializers.SerializerMethodField()
    processing_finished_at = serializers.SerializerMethodField()
    class Meta:
        model = VoterFile
        fields = ('voter_file_content', 'uploaded_at', 'processing_finished_at','num_voters')

    def get_voter_file_content(self,obj):
        result = []
        lines = obj.voter_file_content.split('\n')
        for i in range(len(lines) - 1):
            voter = lines[i].split(',')
            result.append({
                "login": voter[0],
                "email": voter[1],
                "name": voter[2]
            })
        return result

    def get_uploaded_at(self, obj):
        return normalize_datetime(obj.uploaded_at)

    def get_processing_finished_at(self,obj):
        return normalize_datetime(obj.processing_finished_at)
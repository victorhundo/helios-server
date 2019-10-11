from rest_framework import serializers
from helios_auth.models import User
from helios.models import Election, Trustee, Voter, CastVote
from helios.crypto.elgamal import PublicKey
from rest_framework.reverse import reverse


import datetime

def normalize_datetime(date):
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
    class Meta:
        model = Election
        fields = ('cast_url','description','frozen_at','name','openreg','public_key','questions','short_name','use_voter_aliases','uuid','voters_hash','voting_ends_at','voting_starts_at')
    frozen_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S.%f%z")
    voting_ends_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S.%f%z")
    voting_starts_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S.%f%z")

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
        fields = ('url', 'uuid', 'voter_name','voter_hash', 'alias', 'cast_at', 'election', 'user', 'vote_hash', 'vote_cast')
    
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

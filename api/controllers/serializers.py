from rest_framework import serializers
from helios_auth.models import User
from helios.models import Election, Trustee, Voter, CastVote
from helios.crypto.elgamal import PublicKey
import datetime

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

# Serializers define the API representation.
class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = '__all__'

# Serializers define the API representation.
class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = '__all__'

class CastVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CastVote
        fields = '__all__'

class PublicKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicKey
        fields = '__all__'

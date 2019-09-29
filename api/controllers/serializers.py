from rest_framework import serializers
from helios_auth.models import User
from helios.models import Election, Trustee, Voter, CastVote

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
        fields = '__all__'

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

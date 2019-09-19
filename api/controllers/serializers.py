from rest_framework import serializers
from helios_auth.models import User
from helios.models import Election, Trustee, Voter

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ElectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Election
        fields = '__all__'
        lookup_field = 'short_name'

class TrusteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trustee
        fields = ('uuid', 'name', 'email', 'public_key_hash', 'decryption_factors', 'decryption_proofs')



# Serializers define the API representation.
class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = ('uuid', 'voter_email', 'voter_name', 'vote_hash', 'cast_at', 'alias','user_id','election id','election name','election url')

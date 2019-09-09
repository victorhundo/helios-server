from rest_framework import serializers
from helios_auth.models import User
from helios.models import Election, Trustee

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

class TrusteeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Trustee
        fields = '__all__'

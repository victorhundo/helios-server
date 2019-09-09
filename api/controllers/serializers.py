from rest_framework import serializers
from helios_auth.models import User
from helios.models import Election

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
        # fields = (
        #     'url',
        #     'uuid',
        #     'short_name',
        #     'name',
        #     'description',
        #     'use_voter_aliases',
        #     'use_advanced_audit_features',
        #     'randomize_answer_order',
        #     'private_p',
        #     'help_email',
        #     'voting_starts_at',
        #     'voting_ends_at'
        # )

from rest_framework import status
from rest_framework.response import Response
from helios.models import Election, Voter, CastVote, Trustee, VoterFile
from .serializers import *
from django.db.models.query import  QuerySet

def get_error(err):
    status_accept = [200,201,202,400,401,403,404,405,500]
    code = err[0]
    if (code in status_accept and len(err.args) == 3):
        status_number, msg, status_flag = err.args
        return Response({'status': status_number, 'message': msg}, status_flag)
    else:
        return Response({'status': 500, 'message': err[0]}, status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_status(code):
    if (code == 200):
        return status.HTTP_200_OK
    elif (code == 201):
        return status.HTTP_201_CREATED
    elif (code == 202):
        return status.HTTP_202_ACCEPTED
    elif (code == 400):
        return status.HTTP_400_BAD_REQUEST
    elif (code == 401):
        return status.HTTP_401_UNAUTHORIZED
    elif (code == 403):
        return status.HTTP_403_FORBIDDEN
    elif (code == 404):
        return status.HTTP_404_NOT_FOUND
    elif (code == 405):
        return status.HTTP_405_METHOD_NOT_ALLOWED
    elif (code == 500):
        return status.HTTP_500_INTERNAL_SERVER_ERROR

def raise_exception(code, msg):
    raise Exception(code, msg, get_status(code))

def response(code,msg):
    return Response({'status': code, 'message': msg}, get_status(code))

def serializer(obj, request, many=False):
    if (isinstance(obj, QuerySet) and len(obj) == 0):
        return EmptySerializer('list')
    elif (isinstance(obj, QuerySet)):
        instance = obj[0]
        many = True
    else:
        instance = obj

    if (isinstance(instance, CastVote)):
        return CastVoteSerializer(obj, many=many, context={'request': request})
    elif (isinstance(instance, Election)):
        return ElectionSerializer(obj, many=many, context={'request': request})
    elif (isinstance(instance, Trustee)):
        return TrusteeSerializer(obj, many=many, context={'request': request})
    elif (isinstance(instance, Voter)):
        return VoterSerializer(obj, many=many, context={'request': request})
    elif (isinstance(instance, VoterFile)):
        return VoterFileSerizlizer(obj, many=many, context={'request': request})
    else:
        raise_exception(500,'Serializer type not exists.')

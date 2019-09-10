from django.core.urlresolvers import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from helios.models import Election, Trustee
from helios_auth.models import User
from helios.crypto import algs, electionalgs, elgamal
from helios.crypto import utils as cryptoutils



from auth_utils import *
from .serializers import TrusteeSerializer
import sys, json, uuid, datetime

# Parameters for everything
ELGAMAL_PARAMS = elgamal.Cryptosystem()

# trying new ones from OlivierP
ELGAMAL_PARAMS.p = 16328632084933010002384055033805457329601614771185955389739167309086214800406465799038583634953752941675645562182498120750264980492381375579367675648771293800310370964745767014243638518442553823973482995267304044326777047662957480269391322789378384619428596446446984694306187644767462460965622580087564339212631775817895958409016676398975671266179637898557687317076177218843233150695157881061257053019133078545928983562221396313169622475509818442661047018436264806901023966236718367204710755935899013750306107738002364137917426595737403871114187750804346564731250609196846638183903982387884578266136503697493474682071L
ELGAMAL_PARAMS.q = 61329566248342901292543872769978950870633559608669337131139375508370458778917L
ELGAMAL_PARAMS.g = 14887492224963187634282421537186040801304008017743492304481737382571933937568724473847106029915040150784031882206090286938661464458896494215273989547889201144857352611058572236578734319505128042602372864570426550855201448111746579871811249114781674309062693442442368697449970648232621880001709535143047913661432883287150003429802392229361583608686643243349727791976247247948618930423866180410558458272606627111270040091203073580238905303994472202930783207472394578498507764703191288249547659899997131166130259700604433891232298182348403175947450284433411265966789131024573629546048637848902243503970966798589660808533L



class TrusteeView(APIView):
    def getElection(self, pk):
        queryset = Election.get_by_uuid(pk)
        if (queryset): return queryset

        queryset = Election.get_by_short_name(pk)
        if (queryset): return queryset

        return None

    def get(self, request, election_pk):
        election = self.getElection(election_pk)
        if (election):
            queryset = Trustee.get_by_election(election)
            serializer_class = TrusteeSerializer(queryset, many=True, context={'request': request})
            return Response(serializer_class.data)
        else:
            return Response({'status': '404', 'message': 'Election Not Found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, election_pk):
        election = self.getElection(election_pk)
        if (election):
            try:
                body = json.loads(request.body)
                trustee = Trustee(uuid = str(uuid.uuid1()), election = election, name=body['name'], email=body['email'])
                trustee.save()
                return Response({'status': '201', 'message': 'Created'}, status=status.HTTP_201_CREATED)
            except ValueError as err:
                return Response({'status': '400', 'message':str(err)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': '404', 'message': 'Election Not Found'}, status=status.HTTP_404_NOT_FOUND)

class TrusteeViewDetail(APIView):
    def getElection(self, pk):
        queryset = Election.get_by_uuid(pk)
        if (queryset): return queryset

        queryset = Election.get_by_short_name(pk)
        if (queryset): return queryset

        return None

    def get(self, request, election_pk, pk):
        election = self.getElection(election_pk)
        if (election):
            queryset = Trustee.get_by_uuid(pk)
            serializer_class = TrusteeSerializer(queryset, context={'request': request})
            return Response(serializer_class.data)
        else:
            return Response({'status': '404', 'message': 'Election Not Found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,election_pk,pk):
        election = self.getElection(election_pk)
        if (election):
            trustee = Trustee.get_by_election_and_uuid(election, pk)
            trustee.delete()
            return Response({'status': '202', 'message': 'Accepted'}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'status': '404', 'message': 'Election Not Found'}, status=status.HTTP_404_NOT_FOUND)

class TrusteeHeliosView(APIView):
    def getElection(self, pk):
        queryset = Election.get_by_uuid(pk)
        if (queryset): return queryset

        queryset = Election.get_by_short_name(pk)
        if (queryset): return queryset

        return None

    def post(self, request, election_pk):
        election = self.getElection(election_pk)
        if(election):
            try:
                election.generate_trustee(ELGAMAL_PARAMS)
                return Response({'status': '201', 'message': 'Created'}, status=status.HTTP_201_CREATED)
            except:
                return Response({'status': '500', 'message': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'status': '404', 'message': 'Election Not Found'}, status=status.HTTP_404_NOT_FOUND)

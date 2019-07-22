from rest_framework.generics import ListAPIView

from .serializers import UserSerializer
from .models import User

class UserApi(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

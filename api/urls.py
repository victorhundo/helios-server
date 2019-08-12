from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import  routers

from .controllers.user import UserViewSet
from .controllers.auth import AuthViewSet

# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'auth/password', AuthViewSet, base_name='auth')


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

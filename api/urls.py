from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import  routers

from .controllers.user import UserViewSet
from .controllers.auth import LoginViewSet, IsAuthViewsSet
from .controllers.elections import EletctionViewSet

# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'auth/password', LoginViewSet, base_name='auth')
router.register(r'auth/check', IsAuthViewsSet, base_name='check')
router.register(r'elections', EletctionViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

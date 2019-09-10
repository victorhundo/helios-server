from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import  routers

from .controllers.user import UserViewSet
from .controllers.auth import LoginViewSet, IsAuthViewsSet
from .controllers.elections import EletctionViewSet, ElectionDetailView
from .controllers.trustee import TrusteeView, TrusteeHeliosView, TrusteeViewDetail

# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'auth/password', LoginViewSet, base_name='auth')
router.register(r'auth/check', IsAuthViewsSet, base_name='check')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^elections/$', EletctionViewSet.as_view()),
    url(r'^elections/(?P<pk>[^/.]+)/$', ElectionDetailView.as_view()),
    url(r'^elections/(?P<election_pk>[^/.]+)/trustee/$', TrusteeView.as_view()),
    url(r'^elections/(?P<election_pk>[^/.]+)/trustee/add-helios/$', TrusteeHeliosView.as_view()),
    url(r'^elections/(?P<election_pk>[^/.]+)/trustee/(?P<pk>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$', TrusteeViewDetail.as_view()),

]

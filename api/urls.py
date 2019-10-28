from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import  routers

from .controllers.user import UserViewSet
from .controllers.auth import LoginViewSet, IsAuthViewsSet
from .controllers.elections import EletctionViewSet, ElectionDetailView, ElectionCastView, ElectionFreezeView
from .controllers.trustee import TrusteeView, TrusteeHeliosView, TrusteeViewDetail
from .controllers.voter import VoterView, VoterViewDetail, VoterElebilityView, VoterUploadFile, VoterSendEmail
from .controllers.cast_vote import CastVoteView, CastElectionView
from .controllers.tally import TallyViewSet
from .controllers.ballot import BallotView, BallotDetailView, BallotLastView, CelereyView

# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'auth/password', LoginViewSet, base_name='auth')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^celery', CelereyView.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^auth/check/$', IsAuthViewsSet.as_view()),
    url(r'^elections/$', EletctionViewSet.as_view()),
    url(r'^elections/(?P<pk>[^/.]+)/$', ElectionDetailView.as_view(), name='election-detail'),
    url(r'^elections/(?P<election_pk>[^/.]+)/freeze/$', ElectionFreezeView.as_view()),
    url(r'^elections/(?P<election_pk>[^/.]+)/trustee/$', TrusteeView.as_view()),
    url(r'^elections/(?P<election_pk>[^/.]+)/eligibility/$', VoterElebilityView.as_view()),
    url(r'^elections/(?P<election_pk>[^/.]+)/cast/$', CastElectionView.as_view(), name='elections-cast'),
    url(r'^elections/(?P<election_pk>[^/.]+)/compute_tally/$', TallyViewSet.as_view()),
    url(r'^elections/(?P<election_pk>[^/.]+)/trustee/add-helios/$', TrusteeHeliosView.as_view()),
    url(r'^elections/(?P<election_pk>[^/.]+)/trustee/(?P<pk>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$', TrusteeViewDetail.as_view()),
    url(r'^elections/(?P<election_pk>[^/.]+)/votersfile/$', VoterUploadFile.as_view()),
    url(r'^elections/(?P<election_pk>[^/.]+)/votersfile/registry/$', VoterSendEmail.as_view()),
    url(r'^elections/(?P<election_pk>[^/.]+)/voters/$', VoterView.as_view()),
    url(r'^elections/(?P<election_pk>[^/.]+)/voters/(?P<pk>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$', VoterViewDetail.as_view(), name='voters-detail'),
    url(r'^elections/(?P<election_pk>[^/.]+)/voters/(?P<voter_pk>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/cast/$', CastVoteView.as_view(), name='voter-cast'),
    url(r'^elections/(?P<election_pk>[^/.]+)/ballots/$', BallotView.as_view()),
    url(r'^elections/(?P<election_pk>[^/.]+)/ballots/(?P<voter_pk>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$', BallotDetailView.as_view()),
    url(r'^elections/(?P<election_pk>[^/.]+)/ballots/(?P<voter_pk>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/last/$', BallotLastView.as_view(), name='ballot-last'),
]

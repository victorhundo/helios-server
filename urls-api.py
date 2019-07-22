"""
API URLs

Victor Hugo (victorhundo@gmail.com)
"""

from django.conf.urls import *
from helios_auth.api import UserApi

urlpatterns = patterns('',
    (r'^auth/users', UserApi.as_view()),
)

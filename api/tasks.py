# -*- coding: utf-8 -*-
from __future__ import absolute_import
from celery.utils.log import get_task_logger
from django.conf import settings
from celery import shared_task
from helios.models import Voter

from api.celery import app

logger = get_task_logger(__name__)

import sys, time

@app.task(name="slow_task_task")
def slow_task():
    print >>sys.stderr, 'Started task, processing...'
    time.sleep(60)
    print >>sys.stderr, 'Finished Task'
    return True

@app.task(name="voter_send_email_task")
def voter_send_email(voter_id, template, random_password=None):
    voter = Voter.objects.get(id = voter_id)

    if (template == "new user"):
        subject = u'Eleição: Você está apto para a votar!'
        body = u"<p>Olá, você foi registrado em uma eleição!</p><p>login: %s</p><p>senha: %s</p>" % (voter_id,random_password)
    else:
        subject = u'Eleição: Você está apto para a votar!'
        body = u"<p>Olá, você foi registrado em uma eleição!"

    print >>sys.stderr, ('Send Email to voter: %s' % voter)
    voter.send_message(subject, body)

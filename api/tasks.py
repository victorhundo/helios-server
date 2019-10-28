# -*- coding: utf-8 -*-
from __future__ import absolute_import
from celery.utils.log import get_task_logger
from django.conf import settings
from celery import shared_task
from helios.models import Voter, Election
from django.utils.translation import activate
from django.utils import timezone
from api.helpers.email import voter_email_template

from api.celery import app

logger = get_task_logger(__name__)

import sys, time

@app.task(name="voter_send_email_task")
def voter_send_email(voter_id, election_id, template, random_password=None):
    voter = Voter.objects.get(id = voter_id)

    subject = u'Eleição: Você está apto para a votar!'
    body = voter_email_template(template, election_id, voter.id, random_password)

    print >>sys.stderr, ('Send Email to voter: %s' % voter)
    voter.send_message(subject, body)

@app.task(name="election_compute_tally_task")
def election_compute_tally(election_id):
    activate(settings.LANGUAGE_CODE)
    election = Election.objects.get(id = election_id)
    election.compute_tally()

    if election.has_helios_trustee():
        tally_helios_decrypt.delay(election_id = election.id)

@app.task(name="tally_helios_decrypt_task")
def tally_helios_decrypt(election_id):
    activate(settings.LANGUAGE_CODE)
    election = Election.objects.get(id = election_id)
    election.helios_trustee_decrypt()
    combine_decrypyion.delay(election_id)

@app.task(name="combine_decryption_task")
def combine_decrypyion(election_id):
    activate(settings.LANGUAGE_CODE)
    election = Election.objects.get(id = election_id)
    election.combine_decryptions()
    election.tallying_finished_at = timezone.now()
    election.save()
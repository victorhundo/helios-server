# -*- coding: utf-8 -*-
from django.template.loader import get_template
from django.template import Context
from helios.models import Voter
from api.controllers.elections import getElection
from api.controllers.api_utils import raise_exception
from api.helpers.date import time_br

import datetime

def voter_email_template(template, election_id, voter_id, password=None):
    htmly = get_template('email.html')
    voter = Voter.objects.get(id = voter_id)
    election = getElection(election_id)
    end = time_br(election.voting_ends_at)
    start = time_br(election.voting_starts_at)

    if (template == "new_user"):
        context = Context({ 
            'client_url': 'http://localhost:3002',
            'election_url': 'http://localhost:3002' '/elections/' + election.short_name + '/detail',
            'organization_name': 'Diretoria do CAESI',
            'footer': '%s Centro Acadêmico dos Estudantes de Informática.' % (datetime.datetime.now().year),
            'paragraphs': [
                u'Olá %s,' % (voter.voter_name),
                u'Você está apto(a) para votar na eleição <strong>%s</strong>.' % (election.name),
                u"""Fique atento aos prazos! A eleição terá inicio <strong>%s</strong> 
                    e você terá até <strong>%s</strong> 
                    para depositar seu voto.""" % (start,end),
                u"""Segue a descrição da eleição: """,
                u"""%s""" % (election.description),
                u"""Como não identificamos seu cadastro na nossa base de dados, 
                    criamos as seguintes credenciais para que você possa exercer seu direito. 
                    Ao efetuar o login é possivel modificar a senha.""",
                u"""<strong>Login</strong>: %s""" % (voter.voter_login_id),
                u"""<strong>Senha</strong>: %s""" % (password),
                u"""Qualquer dúvida você pode entrar em contato com %s""" % (election.help_email)
            ]
        })
        return htmly.render(context)
    
    elif (template == "old_user"):
        context = Context({ 
            'client_url': 'http://localhost:3002',
            'election_url': 'http://localhost:3002' '/elections/' + election.short_name + '/detail',
            'organization_name': 'Diretoria do CAESI',
            'footer': """%s Centro Acadêmico dos Estudantes de Informática.""" % (datetime.datetime.now().year),
            'paragraphs': [
                u"""Olá %s,""" % (voter.voter_name),
                u"""Você está apto(a) para votar na eleição <strong>%s</strong>.""" % (election.name),
                u"""Fique atento aos prazos! A eleição terá inicio <strong>%s</strong> 
                    e você terá até <strong>%s</strong> 
                    para depositar seu voto.""" % (start,end),
                u"""Segue a descrição da eleição: """,
                u"""%s""" % (election.description),
                u"""Qualquer dúvida você pode entrar em contato com %s""" % (election.help_email)
            ]
        })
        return htmly.render(context)

    raise_exception(500, 'Email Template not Found')

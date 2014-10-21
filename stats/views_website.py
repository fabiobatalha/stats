# coding: utf-8

from pyramid.view import view_config
from pyramid.response import Response
import pyramid.httpexceptions as exc

@view_config(route_name='home', renderer='templates/website/home.mako')
def home(request):

    data = {'data': 'home'}

    return data

@view_config(route_name='accesses', renderer='templates/website/accesses.mako')
def accesses(request):

    data = {'data': 'accesses'}

    return data

@view_config(route_name='production', renderer='templates/website/production.mako')
def production(request):

    data = {'data': 'production'}

    return data

@view_config(route_name='bibliometrics', renderer='templates/website/bibliometrics.mako')
def bibliometrics(request):

    data = {'data': 'bibliometrics'}

    return data
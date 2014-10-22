# coding: utf-8
from pyramid.view import view_config
from pyramid.response import Response
import pyramid.httpexceptions as exc

from stats import views
from stats import tools

DEFAULT_MODE = 'scielo' # could also be 'counter'


@view_config(route_name='ajx_toggle_mode', renderer='json')
@tools.check_session
def ajx_toggle_mode(request):

    return True

@view_config(route_name='home', renderer='templates/website/home.mako')
@tools.check_session
def home(request):
    collections = request.articlemetactrl.certified_collections()

    data = {
        'data': 'home',
        'collections': collections,
        'selected_journal': request.session.get('journal', None),
        'selected_collection': collections[request.session.get('collection', None)],
        'selected_collection_code': request.session.get('collection', None),
        'selected_mode': request.session.get('mode', DEFAULT_MODE)
    }

    return data

@view_config(route_name='accesses', renderer='templates/website/accesses.mako')
@tools.check_session
def accesses(request):

    collections = request.articlemetactrl.certified_collections()

    request.GET['code'] = request.session.get('collection', None)
    request.GET['mode'] = request.session.get('mode', 'scielo')

    pie = views.general_pie(request)['chart']
    lines = views.general_lines(request)['chart']

    data = {
        'data': 'accesses',
        'collections': collections,
        'selected_journal': request.session.get('journal', None),
        'selected_collection': collections[request.session.get('collection', None)],
        'selected_collection_code': request.session.get('collection', None),
        'selected_mode': request.session.get('mode', DEFAULT_MODE),
        'pie': pie,
        'lines': lines
    }

    return data

@view_config(route_name='production', renderer='templates/website/production.mako')
@tools.check_session
def production(request):

    collections = request.articlemetactrl.certified_collections()
    data = {
        'data': 'production',
        'collections': collections,
        'selected_journal': request.session.get('journal', None),
        'selected_collection': collections[request.session.get('collection', None)],
        'selected_collection_code': request.session.get('collection', None),
        'selected_mode': request.session.get('mode', DEFAULT_MODE)
    }

    return data

@view_config(route_name='bibliometrics', renderer='templates/website/bibliometrics.mako')
@tools.check_session
def bibliometrics(request):

    collections = request.articlemetactrl.certified_collections()
    data = {
        'data': 'bibliometrics',
        'collections': collections,
        'selected_journal': request.session.get('journal', None),
        'selected_collection': collections[request.session.get('collection', None)],
        'selected_collection_code': request.session.get('collection', None),
        'selected_mode': request.session.get('mode', DEFAULT_MODE)
    }

    return data
# coding: utf-8
from pyramid.view import view_config
from pyramid.response import Response
import pyramid.httpexceptions as exc
from pyramid.request import Request

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

    journals = request.articlemetactrl.collection_journals(request.session['collection'])

    journal = journals.get(request.session.get('journal', None), None)

    selected_journal = None
    selected_journal_code = None
    if journal:
        selected_journal = journal.title
        selected_journal_code = journal.scielo_issn

    data = {
        'data': 'home',
        'collections': collections,
        'selected_journal': selected_journal,
        'selected_journal_code': selected_journal_code,
        'selected_collection': collections[request.session.get('collection', None)],
        'selected_collection_code': request.session.get('collection', None),
        'selected_mode': request.session.get('mode', DEFAULT_MODE),
        'journals': journals
    }

    return data

@view_config(route_name='accesses', renderer='templates/website/accesses.mako')
@tools.check_session
def accesses(request):

    collections = request.articlemetactrl.certified_collections()

    request.GET['code'] = request.session.get('collection', None)
    request.GET['mode'] = request.session.get('mode', 'scielo')

    code = request.session.get('journal',
        request.session.get('collection', None)
    )

    pie = '/general/pie/?code={0}&mode={1}&importjs=True'.format(
        code,
        request.session.get('mode', 'scielo')
    )

    lines = '/general/lines/?code={0}&mode={1}&importjs=True'.format(
        code,
        request.session.get('mode', 'scielo')
    )

    journals = request.articlemetactrl.collection_journals(request.session['collection'])

    journal = journals.get(request.session.get('journal', None), None)

    selected_journal = None
    selected_journal_code = None
    if journal:
        selected_journal = journal.title
        selected_journal_code = journal.scielo_issn

    data = {
        'data': 'accesses',
        'collections': collections,
        'selected_journal': selected_journal,
        'selected_journal_code': selected_journal_code ,
        'selected_collection': collections[request.session.get('collection', None)],
        'selected_collection_code': request.session.get('collection', None),
        'selected_mode': request.session.get('mode', DEFAULT_MODE),
        'pie': pie,
        'lines': lines,
        'page': 'accesses',
        'journals': journals
    }

    return data

@view_config(route_name='production', renderer='templates/website/production.mako')
@tools.check_session
def production(request):

    collections = request.articlemetactrl.certified_collections()

    journals = request.articlemetactrl.collection_journals(request.session['collection'])

    journal = journals.get(request.session.get('journal', None), None)

    selected_journal = None
    selected_journal_code = None
    if journal:
        selected_journal = journal.title
        selected_journal_code = journal.scielo_issn

    data = {
        'data': 'production',
        'collections': collections,
        'selected_journal': selected_journal,
        'selected_journal_code': selected_journal_code,
        'selected_collection': collections[request.session.get('collection', None)],
        'selected_collection_code': request.session.get('collection', None),
        'selected_mode': request.session.get('mode', DEFAULT_MODE),
        'page': 'production',
        'journals': journals
    }

    return data

@view_config(route_name='bibliometrics', renderer='templates/website/bibliometrics.mako')
@tools.check_session
def bibliometrics(request):

    collections = request.articlemetactrl.certified_collections()

    journals = request.articlemetactrl.collection_journals(request.session['collection'])

    journal = journals.get(request.session.get('journal', None), None)

    selected_journal = None
    selected_journal_code = None
    if journal:
        selected_journal = journal.title
        selected_journal_code = journal.scielo_issn

    data = {
        'data': 'bibliometrics',
        'collections': collections,
        'selected_journal': selected_journal,
        'selected_journal_code': selected_journal_code,
        'selected_collection': collections[request.session.get('collection', None)],
        'selected_collection_code': request.session.get('collection', None),
        'selected_mode': request.session.get('mode', DEFAULT_MODE),
        'page': 'bibliometrics',
        'journals': journals
    }

    return data
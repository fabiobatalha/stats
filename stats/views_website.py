# coding: utf-8
from pyramid.view import view_config
from stats import tools

DEFAULT_MODE = 'scielo' # could also be 'counter'


def base_data_manager(wrapped):
    """
        Decorator to load common data used by all views
    """

    @tools.check_session
    def wrapper(request, *arg, **kwargs):
        if 'mode' in request.session and request.session['mode'] == 'counter':
            setattr(request, 'statsctrl', request.stats_counter)
        else:
            setattr(request, 'statsctrl', request.stats_scielo)

        collections = request.statsctrl.articlemeta.certified_collections()
        code = request.session.get('journal',request.session.get('collection', None))
        journals = request.statsctrl.articlemeta.collection_journals(request.session['collection'])
        journal = journals.get(request.session.get('journal', None), None)
        selected_journal = None
        selected_journal_code = None
        if journal:
            selected_journal = journal.title
            selected_journal_code = journal.scielo_issn

        data = {
            'collections': collections,
            'selected_code': code,
            'selected_journal': selected_journal,
            'selected_journal_code': selected_journal_code,
            'selected_collection': collections[request.session.get('collection', None)],
            'selected_collection_code': request.session.get('collection', None),
            'selected_mode': request.session.get('mode', DEFAULT_MODE),
            'journals': journals
        }

        setattr(request, 'data_manager', data)

        return wrapped(request, *arg, **kwargs)

    wrapper.__doc__ = wrapped.__doc__

    return wrapper

@view_config(route_name='ajx_toggle_mode', renderer='json')
@tools.check_session
def ajx_toggle_mode(request):

    return True

@view_config(route_name='home', renderer='templates/website/home.mako')
@base_data_manager
def home(request):

    data = request.data_manager
    data['page'] = 'home'

    return data

@view_config(route_name='accesses', renderer='templates/website/accesses.mako')
@base_data_manager
def accesses(request):

    data = request.data_manager
    data['page'] = 'accesses'

    return data

@view_config(route_name='production', renderer='templates/website/production.mako')
@base_data_manager
def production(request):

    data = request.data_manager
    data['page'] = 'production'

    return data

@view_config(route_name='bibliometrics', renderer='templates/website/bibliometrics.mako')
@base_data_manager
def bibliometrics(request):

    data = request.data_manager
    data['page'] = 'bibliometrics'

    return data
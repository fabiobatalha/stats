from pyramid.session import SignedCookieSessionFactory
from pyramid.config import Configurator

from stats.controller import Stats
from stats.ratchet.controller import ratchet_ctrl
from stats.ratchet.controller import cache_region as ratchet_cache_region
from stats.articlemeta.controller import articlemeta_ctrl
from stats.articlemeta.controller import cache_region as articlemeta_cache_region


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_mako')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('accesses', '/w/accesses/')
    config.add_route('bibliometrics', '/w/bibliometrics/')
    config.add_route('production', '/w/production/')
    config.add_route('pie', '/general/pie/')
    config.add_route('pie_data', '/general/pie/data/')
    config.add_route('lines', '/general/lines/')
    config.add_route('lines_data', '/general/lines/data/')
    config.add_route('list_data', '/general/list/data/')
    config.add_route('ajx_toggle_mode', '/ajx/toggle_mode/')
    config.add_route('sess_clean_journal', '/sess/clean_journal/')

    # Templates Config
    config.add_mako_renderer('.html')

    ## Cache Settings Config
    if 'memcached_host' in settings:
        cache_config = {}
        cache_config['expiration_time'] = int(settings.get('memcached_expiration_time', 3600))
        cache_config['arguments'] = {'url': settings['memcached_host'], 'binary': True}
        ratchet_cache_region.configure('dogpile.cache.pylibmc', **cache_config)
        articlemeta_cache_region.configure('dogpile.cache.pylibmc', **cache_config)
    else:
        ratchet_cache_region.configure('dogpile.cache.null')
        articlemeta_cache_region.configure('dogpile.cache.null')


    # External API's Config
    articlemetactrl = articlemeta_ctrl(settings['articlemetaapi_host'])
    scielo_ratchetctrl = ratchet_ctrl(settings['ratchetapi_host'])
    counter_ratchetctrl = ratchet_ctrl(settings['counter_ratchetapi_host'])
    scielo_statsctrl = Stats(scielo_ratchetctrl, articlemetactrl)
    counter_statsctrl = Stats(counter_ratchetctrl, articlemetactrl)

    def add_stats_controller_scielo(request):
        
        return scielo_statsctrl
        
    def add_stats_controller_counter(request):
        
        return counter_statsctrl

    config.add_request_method(add_stats_controller_scielo, 'stats_scielo', reify=True)
    config.add_request_method(add_stats_controller_counter, 'stats_counter', reify=True)

    ## Session config
    navegation_session_factory = SignedCookieSessionFactory('sses_navegation')
    config.set_session_factory(navegation_session_factory)

    config.scan()
    return config.make_wsgi_app()

from pyramid.config import Configurator

from stats.ratchet.controller import ratchet_ctrl, cache_region


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    def add_ratchet_controller(request):

        ratchetctrl = ratchet_ctrl(settings['ratchetapi_host'])

        return ratchetctrl

    def add_ratchet_counter_controller(request):

        ratchetctrl = ratchet_ctrl(settings['counter_ratchetapi_host'])

        return ratchetctrl

    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('lines', '/general/lines/')
    config.add_route('lines_data', '/general/lines/data/')
    config.add_route('pie', '/general/pie/')
    config.add_route('pie_data', '/general/pie/data/')
    config.add_route('journals_list', '/journals/list/')

    config.add_request_method(add_ratchet_controller, 'ratchetctrl', reify=True)
    config.add_request_method(add_ratchet_counter_controller, 'ratchetctrl_counter', reify=True)

    ## Setting up cache
    if 'memcached_host' in settings:
        cache_config = {}
        cache_config['expiration_time'] = int(settings.get('memcached_expiration_time', 3600))
        cache_config['arguments'] = {'url': settings['memcached_host']}
        cache_region.configure('dogpile.cache.pylibmc', **cache_config)
    else:
        cache_region.configure('dogpile.cache.null')

    config.scan()
    return config.make_wsgi_app()

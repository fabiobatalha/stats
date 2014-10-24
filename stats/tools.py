# coding: utf-8
import logging
import requests
import traceback

from requests import exceptions

def tqx_dict(data):
    """
    Transform tqx string in a key, value dictionary.
    input: tqx=qId:0;out:csv
    output: {'reqId': 0, 'out': 'csv'}
    """

    return {k:v for k, v in [i.split(':') for i in data.split(';') if i]}


def do_request(url, params=None, method='get'):

    if method == 'get':
        req = requests.get
    else:
        req = requests.post

    attempts = 0
    while attempts <= 10:
        if attempts > 1:
            logging.warning('Retry %s' % url)
        attempts += 1
        try:
            response = req(url, params=params)
            logging.debug('Request made for %s' % url)
            return response
        except exceptions.ConnectionError as e:
            if attempts > 10:
                logging.error('ConnectionError {0}, {1}: {2}'.format(e.errno, e.strerror, url))
                raise e
        except exceptions.HTTPError as e:
            if attempts > 10:
                logging.error('HTTPError {0}, {1}: {2}'.format(e.errno, e.strerror, url))
                raise e
        except exceptions.TooManyRedirects as e:
            if attempts > 10:
                logging.error('ToManyRedirections {0}, {1}: {2}'.format(e.errno, e.strerror, url))
                raise e
        except exceptions.Timeout as e:
            if attempts > 10:
                logging.error('Timeout {0}, {1}: {2}'.format(e.errno, e.strerror, url))
                raise e
        except:
            if attempts > 10:
                logging.error('Unexpected error: {0} : URL: {1}'.format(traceback.format_exc(), url))
                raise


def check_session(wrapped):
    """
        Decorator to check and update session attributes.
    """

    def check(request, *arg, **kwargs):
        collection = request.GET.get('collection', None)
        journal = request.GET.get('journal', None)
        mode = request.GET.get('mode', None)

        if journal == 'clean':
            del(request.session['journal'])
            journal = None

        session_mode = request.session.get('mode', None)
        session_collection = request.session.get('collection', None)
        session_journal = request.session.get('journal', None)

        if mode and mode != session_mode:
            request.session['mode'] = mode

        if collection and collection != session_collection:
            request.session['collection'] = collection
            if 'journal' in request.session:
                del(request.session['journal'])

        elif not session_collection:
            request.session['collection'] = 'scl'

        if journal and journal != session_journal:
            request.session['journal'] = journal

        return wrapped(request, *arg, **kwargs)

    check.__doc__ = wrapped.__doc__

    return check
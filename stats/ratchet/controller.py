# coding: utf-8

import requests

from dogpile.cache import make_region
from ratchetapi import Client

from stats import articlemeta


def cache_key_with_object_address(namespace, fn, **kw):
    fname = fn.__name__
    def generate_key(*arg):
        keys = [
            namespace or '',
            fname,
            str(id(arg[0]))
        ]+[i for i in arg[1:]]
        return str('_'.join(keys)) 
    return generate_key

cache_region = make_region(name='ratchet', function_key_generator=cache_key_with_object_address)


def ratchet_ctrl(api_uri=None):
    ratchetclient = Client(api_uri=api_uri)

    return Ratchet(ratchetclient)


class Ratchet():

    def __init__(self, ratchetclient):
        self.ratchetclient = ratchetclient

    @cache_region.cache_on_arguments()
    def general(self, code):

        try:
            data = self.ratchetclient.query('general').filter(code=code).next()
        except:
            return None

        return data

    @cache_region.cache_on_arguments()
    def journal(self, code):
        try:
            data = self.ratchetclient.query('journals').get(code=code)
        except:
            return None

        return data

    @cache_region.cache_on_arguments()
    def collection_journals(self, collection):

        try:
            data = self.ratchetclient.query('journals').filter(collection=collection)
        except:
            return None

        return data
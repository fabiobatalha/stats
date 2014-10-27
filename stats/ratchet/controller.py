# coding: utf-8

import requests

from dogpile.cache import make_region
from ratchetapi import Client

from stats import articlemeta


def cache_key_with_object_address(namespace, fn, **kw):
    fname = fn.__name__
    def generate_key(*arg):
        return namespace or '' + "_" + fname + "_".join(str(item) for item in arg)
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

        data = self.ratchetclient.query('general').filter(code=code).next()

        return data

    @cache_region.cache_on_arguments()
    def journal(self, code):

        data = self.ratchetclient.query('journals').filter(code=code)

        return data

    @cache_region.cache_on_arguments()
    def journals_list(self, collection):

        journals = {}
        for journal in self.ratchetclient.query('journals').all():
            jn = journals.setdefault(journal['code'], journal)

        return journals

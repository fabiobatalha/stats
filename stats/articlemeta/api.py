# coding: utf-8
import logging
import requests

from dogpile.cache import make_region
from dogpile.cache.util import sha1_mangle_key
from xylose.scielodocument import Journal

cache_region = make_region(name='stats')

def get_journal_metadata(code, collection=None):

    url = 'http://192.168.1.162:7000/api/v1/journal'

    params = {'issn': code}
    if collection:
        params['collection'] = collection

    try:
        journal_meta = requests.get(url, params=params).json()
    except:
        logging.error('Error fetching url: %s' % url)
        return None

    try:
        journal_meta = journal_meta[0]
    except IndexError:
        return None

    return Journal(journal_meta)

def get_all_journals_metadata(collection=None):

    url = 'http://192.168.1.162:7000/api/v1/journal/identifiers'

    params = {'offset': 0}
    if collection:
        params['collection'] = collection

    journals = []
    while True:
        try:
            identifiers = requests.get(url, params=params).json()
        except:
            logging.error('Error fetching url: %s' % url)


        if len(identifiers['objects']) == 0:
            raise StopIteration

        for identifier in identifiers['objects']:
            for code in identifier:
                journal = get_journal_metadata(code, collection=identifier['collection'])
                if journal:
                    journals.append(journal)


    return journals

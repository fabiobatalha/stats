# coding: utf-8
from xylose.scielodocument import Journal

from dogpile.cache import make_region

from stats import tools


cache_region = make_region(name='articlemeta')


def articlemeta_ctrl(api_uri=None):
    if api_uri[-1] == '/':
        api_uri = api_uri[:-1]

    return ArticleMeta(api_uri)


class ArticleMeta():

    def __init__(self, api_uri):
        self.api_uri = api_uri

        self.journals = self._journals()
        self.collections = self._collections()

    @cache_region.cache_on_arguments()
    def _collections(self):
        """
        Retrieve all collection basic data from Articlemeta
        """
        url = '%s/v1/collection' % self.api_uri

        response = tools.do_request(url)

        return response.json()

    @cache_region.cache_on_arguments()
    def certified_collections(self):

        data = {}

        for collection in self.collections:
            if collection['status'] == 'certified':
                data[collection['acron']] = collection['name']['en']

        return data

    @cache_region.cache_on_arguments()
    def _journal(self, code, collection):
        """
        Retrieve a journal metadata from Articlemeta
        """

        url = '%s/v1/journal' % self.api_uri

        params = {'issn': code}
        if collection:
            params['collection'] = collection

        response = tools.do_request(url, params=params).json()

        try:
            response = response[0]
        except IndexError:
            return None

        return Journal(response)

    def _journals(self):
        """
        Retrieve all journals metadata from Articlemeta
        """

        url = '%s/v1/journal/identifiers' % self.api_uri

        params = {'offset': 0}

        journals = {}
        while True:

            response = tools.do_request(url, params=params).json()

            if len(response['objects']) == 0:
                break

            for identifier in response['objects']:
                for code in identifier['code']:
                    journal = self._journal(
                        code, identifier['collection']
                    )
                    if journal:
                        coll = journals.setdefault(journal.collection_acronym, {})
                        coll[journal.scielo_issn] = journal
            
            params['offset'] += 1000

        return journals

    def collection_journals(self, collection):

        return self.journals[collection]

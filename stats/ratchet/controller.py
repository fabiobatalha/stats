# coding: utf-8

from collections import OrderedDict
import calendar
import copy
import json
import requests
import logging

from dogpile.cache import make_region
from dogpile.cache.util import sha1_mangle_key
from ratchetapi import Client

from stats import articlemeta


cache_region = make_region(name='stats')


def request_get_data(url):

    data = request.get(url).json


def ratchet_ctrl():

    ratchetclient = Client()

    return Ratchet(ratchetclient)

class Ratchet():

    def __init__(self, ratchetclient):
        self.ratchetclient = ratchetclient


    def _general_article_year_month_lines_chart_to_gviz_data(self, accesses, begin='0000-01-01', end='9999-12-31'):

        del accesses['total']
        del accesses['code']

        description = [('months', 'string', 'months')]

        empty_months_range = {'%02d' % x: None for x in range(1, 13)}
        # Creating dict year that represents the sum of accesses of all available years
        # separated by months for the pages sci_arttext and download
        years = {}
        for key, value in accesses.items():
            if key in ['html', 'abstract', 'pdf']:
                del value['total']
                for year, months in value.items():
                    del months['total']
                    if year[1:] >= begin[0:4] and year[1:] <= end[0:4]:
                        ye = years.setdefault(year[1:], copy.copy(empty_months_range))
                        for month, days in months.items():
                                if year[1:]+'-'+month[1:] >= begin and year[1:]+'-'+month[1:] <= end:
                                    if ye[month[1:]] == None:
                                        ye[month[1:]] = 0
                                    ye[month[1:]] += days['total']

        data = []
        for month in range(1, 13):
            row = []
            for year, months in OrderedDict(sorted(years.items())).items():
                if not len(row):
                    row.append(calendar.month_abbr[month])
                row.append(months['%02d' % month])
            data.append(row)

        for year, months in OrderedDict(sorted(years.items())).items():
            description.append((year, 'number'))

        return description, data

    def _general_source_page_pie_chart_to_gviz_data(self, accesses, begin=None, end=None):

        description = [
            ('source', 'string', 'source page'),
            ('accesses', 'number', 'accesses'),
        ]

        if 'code' in accesses:
            del(accesses['code'])
        if 'total' in accesses:
            del(accesses['total'])
        if 'type' in accesses:
            del(accesses['type'])
        if 'page' in accesses:
            del(accesses['code'])
        if 'other' in accesses:
            del(accesses['other'])
        if 'journal' in accesses and not isinstance(accesses['journal'], dict):
            del(accesses['journal'])
        if 'issue' in accesses and not isinstance(accesses['issue'], dict):
            del(accesses['issue'])


        data = []
        for key, value in accesses.items():

            if key[0] != 'y':
                data.append([key, value['total']])

        return description, data

    def _journals_list_to_gviz_data(self, journals, begin=None, end=None):

        description = [
            ('journal_title', 'string', 'journal'),
            ('journal_issn', 'string', 'issn'),
            ('pdf', 'number', 'fulltext PDF'),
            ('fulltext', 'number', 'fulltext HTML'),
            ('abstract', 'number', 'abstract'),
            ('issue', 'number', 'table of contents'),
            ('home', 'number', 'journal home'),
            ('total', 'number')
        ]

        data = []
        for issn, journal in journals.items():
            line = []
            pdf = journal['accesses'].get('pdf', {'total': 0})['total']
            html = journal['accesses'].get('html', {'total': 0})['total']
            abstracts = journal['accesses'].get('abstract', {'total': 0})['total']
            issue = journal['accesses'].get('toc', {'total': 0})['total']
            home = journal['accesses'].get('journal', {'total': 0})['total']
            line.append(journal['metadata'].scielo_issn)
            line.append(journal['metadata'].title)
            line.append(pdf)
            line.append(html)
            line.append(abstracts)
            line.append(issue)
            line.append(home)
            line.append(pdf+html+abstracts+issue+home)

            data.append(line)

        return description, data

    @cache_region.cache_on_arguments()
    def general_article_year_month_lines_chart(self, code, begin=None, end=None):

        accesses = self.ratchetclient.query('general').filter(code=code).next()

        description, data = self._general_article_year_month_lines_chart_to_gviz_data(
            accesses,
            begin=begin,
            end=end
        )

        return description, data

    @cache_region.cache_on_arguments()
    def general_source_page_pie_chart(self, code, begin=None, end=None):
        accesses = self.ratchetclient.query('general').filter(code=code).next()

        description, data = self._general_source_page_pie_chart_to_gviz_data(
            accesses,
            begin=begin,
            end=end
        )

        return description, data

    @cache_region.cache_on_arguments()
    def journal(self, code, begin=None, end=None):

        journal = self.ratchetclient.query('journals').find(code=code)

        description, data = self._journals_list_to_gviz_data(journal,
            begin=begin,
            end=end
        )

        return description, data

    @cache_region.cache_on_arguments()
    def journals_list(self):

        journals = {}
        for journal in self.ratchetclient.query('journals').all():
            xylose_journal = articlemeta.api.get_journal_metadata(journal['code'])
            if xylose_journal:
                jn = journals.setdefault(journal['code'], {})
                jn['accesses'] = journal
                jn['metadata'] = xylose_journal

        description, data = self._journals_list_to_gviz_data(journals,
            begin=begin,
            end=end
        )

        return description, data

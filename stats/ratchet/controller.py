# coding: utf-8

from collections import OrderedDict
import calendar
import copy
import json
import requests
import logging
import datetime

from dogpile.cache import make_region
from ratchetapi import Client

from stats import articlemeta


cache_region = make_region(name='ratchet')


def ratchet_ctrl(api_uri=None):
    ratchetclient = Client(api_uri=api_uri)

    return Ratchet(ratchetclient)

class Ratchet():

    def __init__(self, ratchetclient):
        self.ratchetclient = ratchetclient


    def _general_article_year_month_lines_base(self, accesses, begin='0000-01-01', end='9999-12-31'):
        """
        Creating dict year that represents the sum of accesses of all available years
        separated by months for document types ['html', 'abstract', 'pdf']
        """

        del accesses['total']
        del accesses['code']

        if len(begin) == 4:
            begin += '-01' 

        if len(end) == 4:
            end += '-12' 

        empty_months_range = {'%02d' % x: None for x in range(1, 13)}
        data = {}
        for key, value in accesses.items():
            if key in ['html', 'abstract', 'pdf']:
                del value['total']
                for year, months in value.items():
                    del months['total']
                    if year[1:] >= begin[0:4] and year[1:] <= end[0:4]:
                        ye = data.setdefault(year[1:], copy.copy(empty_months_range))
                        for month, days in months.items():
                                if year[1:]+'-'+month[1:] >= begin and year[1:]+'-'+month[1:] <= end:
                                    if ye[month[1:]] == None:
                                        ye[month[1:]] = 0
                                    ye[month[1:]] += days['total']

        return data

    def _general_article_year_month_lines_chart_to_gviz_data(self, accesses, begin='0000-01-01', end='9999-12-31'):
        """
        Prepare data received by self._general_article_year_month_lines_base according to gviz format
        """
        years = self._general_article_year_month_lines_base(accesses, begin=begin, end=end)

        description = [('months', 'string', 'months')]

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

    def _general_article_year_month_lines_chart_to_csv_data(self, accesses, begin='0000-01-01', end='9999-12-31'):
        """
        Prepare data received by self._general_article_year_month_lines_base according to csv format
        """
        data = self._general_article_year_month_lines_base(accesses, begin=begin, end=end)

        output = 'year,month,total\r\n'

        for year, months in sorted(data.items()):
            for month, total in sorted(months.items()):
                if total:
                    output += '%s\r\n' % ','.join([str(year), str(month), str(total)])

        return output

    def _general_source_page_pie_chart_to_base_data(self, accesses):

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

        return data

    def _general_source_page_pie_chart_to_gviz_data(self, accesses):

        data = self._general_source_page_pie_chart_to_base_data(accesses)

        description = [
            ('source', 'string', 'source page'),
            ('accesses', 'number', 'accesses'),
        ]

        return description, data

    def _general_source_page_pie_chart_to_csv_data(self, accesses):

        data = self._general_source_page_pie_chart_to_base_data(accesses)

        output = u'source,total\r\n'
        
        for item in sorted(data):
            output += u'%s\r\n' % u','.join([str(i) for i in item])

        return output

    def _journals_list_to_gviz_data(self, journals):

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
    def general_article_year_month_lines_chart(self, code, out=None, begin=None, end=None):

        allowed_outputs = ['gviz', 'csv']

        if not out in allowed_outputs:
            raise ValueError('output %s not in %s' % (out, str(allowed_outputs)))

        accesses = self.ratchetclient.query('general').filter(code=code).next()

        if out == 'gviz':
            return self._general_article_year_month_lines_chart_to_gviz_data(
                accesses,
                begin=begin,
                end=end
            )
        elif out == 'csv':
            return self._general_article_year_month_lines_chart_to_csv_data(
                accesses,
                begin=begin,
                end=end
            )

    @cache_region.cache_on_arguments()
    def general_source_page_pie_chart(self, code, out=None):

        allowed_outputs = ['gviz', 'csv']

        if not out in allowed_outputs:
            raise ValueError('output %s not in %s' % (out, str(allowed_outputs)))

        accesses = self.ratchetclient.query('general').filter(code=code).next()

        if out == 'gviz':
            return self._general_source_page_pie_chart_to_gviz_data(accesses)
        elif out == 'csv':
            return self._general_source_page_pie_chart_to_csv_data(accesses)

    @cache_region.cache_on_arguments()
    def journal(self, code):

        journal = self.ratchetclient.query('journals').find(code=code)

        description, data = self._journals_list_to_gviz_data(
            journal,
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

        description, data = self._journals_list_to_gviz_data(journals)

        return description, data

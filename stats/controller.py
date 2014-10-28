# conding: utf-8
from collections import OrderedDict
import calendar
import copy

from dogpile.cache import make_region

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

cache_region = make_region(name='stats_controller', function_key_generator=cache_key_with_object_address)

class Stats(object):

    def __init__(self, ratchet, articlemeta):
        self.ratchet = ratchet
        self.articlemeta = articlemeta

    def general_article_year_month_lines_chart(self, code, out=None, begin=None, end=None):

        def base_data(code, begin='0000-01-01', end='9999-12-31'):
            """
            Creating dict year that represents the sum of accesses of all available years
            separated by months for document types ['html', 'abstract', 'pdf']
            """

            accesses = self.ratchet.general(code)

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


        def to_gviz_data(accesses):
            """
            Prepare data received by self._general_article_year_month_lines_base according to gviz format
            """

            description = [('months', 'string', 'months')]

            data = []
            for month in range(1, 13):
                row = []
                for year, months in OrderedDict(sorted(accesses.items())).items():
                    if not len(row):
                        row.append(calendar.month_abbr[month])
                    row.append(months['%02d' % month])
                data.append(row)

            for year, months in OrderedDict(sorted(accesses.items())).items():
                description.append((year, 'number'))

            return description, data

        def to_csv_data(accesses):
            """
            Prepare data received by self._general_article_year_month_lines_base according to csv format
            """

            output = 'year,month,total\r\n'

            for year, months in sorted(accesses.items()):
                for month, total in sorted(months.items()):
                    if total:
                        output += '%s\r\n' % ','.join([str(year), str(month), str(total)])

            return output

        allowed_outputs = ['gviz', 'csv']

        if not out in allowed_outputs:
            raise ValueError('output %s not in %s' % (out, str(allowed_outputs)))

        accesses = base_data(code, begin=begin, end=end)

        if out == 'gviz':
            return to_gviz_data(accesses)
        elif out == 'csv':
            return to_csv_data(accesses)


    def general_source_page_pie_chart(self, code, out=None):

        def base_data(code):

            accesses = self.ratchet.general(code)

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

        def to_gviz_data(accesses):

            description = [
                ('source', 'string', 'source page'),
                ('accesses', 'number', 'accesses'),
            ]

            return description, accesses

        def to_csv_data(accesses):

            output = u'source,total\r\n'
            
            for item in sorted(accesses):
                output += u'%s\r\n' % u','.join([str(i) for i in item])

            return output

        allowed_outputs = ['gviz', 'csv']

        if not out in allowed_outputs:
            raise ValueError('output %s not in %s' % (out, str(allowed_outputs)))

        accesses = base_data(code)

        if out == 'gviz':
            return to_gviz_data(accesses)
        elif out == 'csv':
            return to_csv_data(accesses)


    @cache_region.cache_on_arguments()
    def subject_area_pie_chart(self, collection, out=None):

        def base_data(collection):

            data = {}
            for issn, journal in self.articlemeta.collection_journals(collection).items():
                for area in journal.subject_areas:
                    acessos = self.ratchet.general(issn) or {'total': 0}
                    data.setdefault(area, 0)
                    data[area] += acessos['total']

            return [[k, v] for k, v in data.items()]

        def to_gviz_data(accesses):

            description = [
                ('area', 'string', 'thematic area'),
                ('accesses', 'number', 'accesses'),
            ]

            return description, accesses

        def to_csv_data(accesses):

            output = u'area,total\r\n'
            
            for item in sorted(accesses):
                output += u'%s\r\n' % u','.join([str(i) for i in item])

            return output

        allowed_outputs = ['gviz', 'csv']

        if not out in allowed_outputs:
            raise ValueError('output %s not in %s' % (out, str(allowed_outputs)))

        accesses = base_data(collection)

        if out == 'gviz':
            return to_gviz_data(accesses)
        elif out == 'csv':
            return to_csv_data(accesses)

    @cache_region.cache_on_arguments()
    def most_accessed_journals(self, collection, out=None):

        def base_data(collection):

            accesses = self.ratchet.journals_by_collection(collection)

            data = {}
            for jaccesses in accesses:

                journal = self.articlemeta.journal(jaccesses['code'])
                issn = journal.scielo_issn
                data.setdefault(issn, [])
                data[issn].append(journal.title)
                data[issn].append(journal.url)
                data[issn].append(jaccesses.get('pdf', {'total': 0}).get['total'])
                data[issn].append(jaccesses.get('html', {'total': 0}).get['total'])
                data[issn].append(jaccesses.get('abstract', {'total': 0}).get['total'])
                data[issn].append(jaccesses.get('toc', {'total': 0}).get['total'])
                data[issn].append(jaccesses.get('issues', {'total': 0}).get['total'])
                data[issn].append(sum(data[issn]))

            return [[k, v] for k, v in data.items()]

        def to_gviz_data(accesses):

            description = [
                ('title', 'string', 'journal title'),
                ('pdf', 'number', 'pdf'),
                ('html', 'number', 'html'),
                ('abstract', 'number', 'abstract'),
                ('toc', 'number', 'toc'),
                ('issues', 'number', 'issues'),
                ('total', 'number', 'total'),
            ]

            return description, accesses

        def to_csv_data(accesses):

            output = u'title,pdf,html,abstract,toc,issue,total\r\n'
            
            for item in sorted(accesses):
                output += u'%s\r\n' % u','.join([str(i) for i in item])

            return output

        allowed_outputs = ['gviz', 'csv']

        if not out in allowed_outputs:
            raise ValueError('output %s not in %s' % (out, str(allowed_outputs)))

        accesses = base_data(collection)

        if out == 'gviz':
            return to_gviz_data(accesses)
        elif out == 'csv':
            return to_csv_data(accesses)

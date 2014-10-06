# coding: utf-8

import unittest
import copy

from stats.ratchet import controller
from xylose.scielodocument import Journal


class ControllerTests(unittest.TestCase):

    def setUp(self):
        from fixtures.journals import journal_accesses, metadata

        self.accesses = copy.deepcopy(journal_accesses)
        self.metadata = copy.deepcopy(metadata)

        self.journals = {
            metadata['code'][0]: {
                'metadata': Journal(self.metadata),
                'accesses': self.accesses
            }
        }

    def test_journals_list_to_gviz_data(self):

        ctrl = controller.Ratchet('fakeratchetapiclient')

        description, data = ctrl._journals_list_to_gviz_data(self.journals)

        self.assertEqual(data, [
            ['0034-8910', u'Revista de Saúde Pública', 9536802, 3056056, 426094, 361175, 132952, 13513079]
        ])

    def test_general_article_year_month_lines_chart_to_gviz_data(self):

        ctrl = controller.Ratchet('fakeratchetapiclient')

        description, data = ctrl._general_article_year_month_lines_chart_to_gviz_data(self.accesses)

        expected = [
            ['Jan', None, 338215, 396586],
            ['Feb', None, 455116, 596177],
            ['Mar', None, 342395, 944963],
            ['Apr', None, 14320, 924224],
            ['May', None, 724622, 1017929],
            ['Jun', None, 640475, 723827],
            ['Jul', None, 405063, 908688],
            ['Aug', None, 639943, 825109],
            ['Sep', None, 784848, None],
            ['Oct', None, 865038, None],
            ['Nov', None, 1031974, None],
            ['Dec', 3553, 435887, None]
        ]

        self.assertEqual(data, expected)

    def test_general_article_year_month_lines_chart_to_gviz_data_begin_end(self):

        ctrl = controller.Ratchet('fakeratchetapiclient')

        description, data = ctrl._general_article_year_month_lines_chart_to_gviz_data(self.accesses, begin='2013-06', end='2014-05')

        expected = [
            ['Jan', None, 396586],
            ['Feb', None, 596177],
            ['Mar', None, 944963],
            ['Apr', None, 924224],
            ['May', None, 1017929],
            ['Jun', 640475, None],
            ['Jul', 405063, None],
            ['Aug', 639943, None],
            ['Sep', 784848, None],
            ['Oct', 865038, None],
            ['Nov', 1031974, None],
            ['Dec', 435887, None]
        ]

        self.assertEqual(data, expected)

    def test_general_article_year_month_lines_chart_to_gviz_description(self):

        ctrl = controller.Ratchet('fakeratchetapiclient')

        description, data = ctrl._general_article_year_month_lines_chart_to_gviz_data(self.accesses)

        expected = [
            ('months', 'string', 'months'),
            (u'2012', 'number'),
            (u'2013', 'number'),
            (u'2014', 'number')
        ]

        self.assertEqual(description, expected)

    def test_general_source_page_pie_chart_to_gviz_data(self):

        ctrl = controller.Ratchet('fakeratchetapiclient')

        description, data = ctrl._general_source_page_pie_chart_to_gviz_data(self.accesses)

        expected = [
            [u'html', 3056056],
            [u'abstract', 426094],
            [u'pdf', 9536802],
            [u'issues', 39355],
            [u'toc', 361175],
            [u'journal', 132952]
        ]

        self.assertEqual(sorted(data), sorted(expected))

    def test_general_source_page_pie_chart_to_gviz_data_description(self):

        ctrl = controller.Ratchet('fakeratchetapiclient')

        description, data = ctrl._general_source_page_pie_chart_to_gviz_data(self.accesses)

        expected = [
            ('source', 'string', 'source page'),
            ('accesses', 'number', 'accesses')
        ]

        self.assertEqual(
            description,
            expected
        )

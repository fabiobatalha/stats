# coding: utf-8

import unittest
import copy

from stats.ratchet import controller
from xylose.scielodocument import Journal
from ratchetapi import Client


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

    def test_ratchet_ctrl(self):
        from stats.ratchet.controller import Ratchet

        ctrl = controller.ratchet_ctrl()

        self.assertTrue(isinstance(ctrl, Ratchet))

    def test_journals_list_to_gviz_data(self):

        ctrl = controller.Ratchet('fakeratchetapiclient')

        description, data = ctrl._journals_list_to_gviz_data(self.journals)

        self.assertEqual(data, [
            ['0034-8910', u'Revista de Saúde Pública', 9536802, 3056056, 426094, 361175, 132952, 13513079]
        ])

    def test_general_article_year_month_lines_chart_to_csv_data(self):

        ctrl = controller.Ratchet('fakeratchetapiclient')

        data = ctrl._general_article_year_month_lines_chart_to_csv_data(self.accesses)

        expected = 'year,month,total\r\n2012,12,3553\r\n2013,01,338215\r\n2013,02,455116\r\n2013,03,342395\r\n2013,04,14320\r\n2013,05,724622\r\n2013,06,640475\r\n2013,07,405063\r\n2013,08,639943\r\n2013,09,784848\r\n2013,10,865038\r\n2013,11,1031974\r\n2013,12,435887\r\n2014,01,396586\r\n2014,02,596177\r\n2014,03,944963\r\n2014,04,924224\r\n2014,05,1017929\r\n2014,06,723827\r\n2014,07,908688\r\n2014,08,825109\r\n'

        self.assertEqual(data, expected)

    def test_general_article_year_month_lines_chart_to_csv_data_begin_end(self):

        ctrl = controller.Ratchet('fakeratchetapiclient')

        data = ctrl._general_article_year_month_lines_chart_to_csv_data(self.accesses, begin='2013-06', end='2013-08')

        expected = 'year,month,total\r\n2013,06,640475\r\n2013,07,405063\r\n2013,08,639943\r\n'

        self.assertEqual(data, expected)

    def test_general_article_year_month_lines_chart_to_csv_data_begin_end(self):

        ctrl = controller.Ratchet('fakeratchetapiclient')

        data = ctrl._general_article_year_month_lines_chart_to_csv_data(self.accesses, begin='2013', end='2013')

        expected = 'year,month,total\r\n2013,01,338215\r\n2013,02,455116\r\n2013,03,342395\r\n2013,04,14320\r\n2013,05,724622\r\n2013,06,640475\r\n2013,07,405063\r\n2013,08,639943\r\n2013,09,784848\r\n2013,10,865038\r\n2013,11,1031974\r\n2013,12,435887\r\n'

        self.assertEqual(data, expected)

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

    def test_general_source_page_pie_chart_to_csv_data(self):

        ctrl = controller.Ratchet('fakeratchetapiclient')

        data = ctrl._general_source_page_pie_chart_to_csv_data(self.accesses)

        expected = "source,total\r\nabstract,426094\r\nhtml,3056056\r\nissues,39355\r\njournal,132952\r\npdf,9536802\r\ntoc,361175\r\n"

        self.assertEqual(data, expected)

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

# coding: utf-8

import unittest

from stats import tools


class ToolsTests(unittest.TestCase):

    def test_tqx_dict(self):

        result = tools.tqx_dict('reqId:0;out:csv')

        self.assertEqual(result['reqId'], '0')
        self.assertEqual(result['out'], 'csv')

    def test_tqx_dict_comma_in_the_end(self):

        result = tools.tqx_dict('out:csv;')

        self.assertEqual(result['out'], 'csv')
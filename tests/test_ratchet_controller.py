# coding: utf-8"
import unittest

from stats.ratchet import controller
from stats.ratchet.controller import Ratchet

class RatchetController(unittest.TestCase):
    def test_ratchet_ctrl(self):

        ctrl = controller.ratchet_ctrl()

        self.assertTrue(isinstance(ctrl, Ratchet))


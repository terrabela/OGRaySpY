from unittest import TestCase

from src.spec_class import Spec
from src.spec_graphics_class import GrossCountsGraphic
from src.genericcalib_class import GenericCalib

class TestSpecGraphics(TestCase):
    def setUp(self):
        self.spec = Spec('../data/some_spectra/CCI0202-I.Chn')
        self.assertGreater(self.spec.gross_spec_ser_an.n_ch, 0)

    def test_simple_plot(self):
        print(self.spec.f_name)
        self.assertEqual(0, 0)

# from unittest import TestCase
import sys
from unittest import TestCase

class TestSpec(TestCase):
    def setUp(self):
        src_dir = sys.path[0] + '/src'
        sys.path.insert(0, src_dir)
        from spec_class import Spec
        self.spec = Spec('data/some_spectra/CCI0202-I.Chn')

    def test_file_exists(self):
        self.assertGreater(self.spec.gross_spec_ser_an.n_ch, 0)

    def test_graphics(self):
        from spec_graphics_class import GenericGraphics
        self.assertTrue(True)

    def test_plot(self):
        from spec_graphics_class import GrossCountsGraphic
        spec_graphic = GrossCountsGraphic(self.spec.f_name, self.spec.gross_spec_ser_an)

    def test_fft_plot(self):
        from scipy.fft import fft, ifft, fftfreq, fftshift
        from spec_graphics_class import GenericGraphics
        # fft_graphic = GenericGraphics('Qquer_coisa', [1,2,3], [4,5,6])
        # Number of sample points
        # N = 600
        # sample spacing
        # T = 1.0 / 800.0
        # x = np.linspace(0.0, N * T, N, endpoint=False)
        # y = np.sin(50.0 * 2.0 * np.pi * x) + 0.5 * np.sin(80.0 * 2.0 * np.pi * x)
        # yf = fft(y)
        # xf = fftfreq(N, T)[:N // 2]
        # fft_ys = 2.0 / N * np.abs(yf[0:N // 2])
        xf = self.spec.gross_spec_ser_an.x_s
        fft_ys = fft(self.spec.gross_spec_ser_an.y_s)
        fft_ys[2000:2096] = 0.0
        fft_ys[1800:2296] = 0.0
        ifft_ys = ifft(fft_ys)
        ys_plot = abs(ifft_ys)
        fft_graphic = GenericGraphics('Qquer_coisa', xf, ys_plot)
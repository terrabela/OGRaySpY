"""
    This file is part of OGRaySpY
    Author: Marcelo Francis Máduar (maduar@vivaldi.net)


    Here a Spec object, encapsulating all data related to a single gamma-ray,
    is instantiated.

"""

from ograypsy.classes.spec_class import Spec

spectrum = Spec(fpc_fname='CCI0202-I.Chn',
                spectra_path='../data/some_spectra')

print(vars(spectrum))
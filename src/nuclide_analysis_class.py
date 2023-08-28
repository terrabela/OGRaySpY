import numpy as np
from numpy.polynomial import Polynomial as Poly
import pandas as pd
from sklearn import linear_model


class NuclideAnalysis:
    """ Nuclide analysis class. """

    def __init__(self, f_name='', reduced_f_name='',):
        pass

    def nuclide_identif(self, nucl_iear1_df, pks_comprehensive_df):
        nucl_iear1_selctd_gamms_df = nucl_iear1_df.loc[
            (nucl_iear1_df.intensity > 1.0) & nucl_iear1_df.is_to_consider
            ]
        print(nucl_iear1_selctd_gamms_df)
        cross_df = pd.merge(pks_comprehensive_df, nucl_iear1_selctd_gamms_df, how='cross')
        cross_df["delta_en"] = cross_df.engy_pk_det - cross_df.energy

        def create_matching_peaks_df(pks_df, en_toler, must_be_key_gamma=False):
            if must_be_key_gamma:
                aux_df = pd.DataFrame(pks_df.loc[pks_df.is_key_gamma])
            else:
                aux_df = pd.DataFrame(pks_df)
            return aux_df.loc[np.abs(pks_df.delta_en) < en_toler]

        en_toler_calib = 3.0
        matching_peaks_df = create_matching_peaks_df(cross_df, en_toler_calib)
        print(matching_peaks_df)
        print("Now, proceed to the robust calibration.")
        x_energy = np.array(matching_peaks_df.energy).reshape(-1, 1)
        y_delta_en = np.array(matching_peaks_df.delta_en)
        # Robustly fit linear model with RANSAC algorithm
        ransac = linear_model.RANSACRegressor()
        ransac.fit(x_energy, y_delta_en)
        inlier_mask = ransac.inlier_mask_
        outlier_mask = np.logical_not(inlier_mask)
        matching_peaks_df["final_delta_en"] = (
                matching_peaks_df.engy_pk_det - ransac.predict(x_energy) - matching_peaks_df.energy
        )
        en_toler_ident = 0.5
        peaks_for_calib = matching_peaks_df.loc[
            np.abs(matching_peaks_df.final_delta_en) < en_toler_ident
            ]
        en_recalib = Poly.fit(peaks_for_calib.centroids, peaks_for_calib.energy, deg=2)
        print('en_recalib:', en_recalib)
        print('pks_comprehensive_df:', pks_comprehensive_df)
        pks_comprehensive_df['engy_pk_recalib'] = en_recalib(
            pks_comprehensive_df.centroids
        ),
        cross_df = pd.merge(pks_comprehensive_df, nucl_iear1_selctd_gamms_df, how='cross')
        cross_df["delta_en"] = cross_df.engy_pk_recalib - cross_df.energy
        matching_peaks_df = create_matching_peaks_df(cross_df, en_toler_ident)
        print(matching_peaks_df)

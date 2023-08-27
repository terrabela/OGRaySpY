#-----------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license information.
#-----------------------------------------------------------------------------------------

from flask import Flask
app = Flask(__name__)

import numpy as np
import pandas as pd
from numpy.polynomial import Polynomial as P
from random import randrange

from ograyspy_class import Ograyspy, select_spectrum_from_folder_list
from spec_class import Spec

@app.route("/")
def hello():
    return app.send_static_file("index.html")

def app_runner():
    print ("Running...")
    some_spectrum_pattern = "SI06122"
    ograyspy_app = Ograyspy(folder_to_find="static/spectra")
    spectra_list_df = pd.read_pickle(ograyspy_app.pkl_folder_files)
    print(spectra_list_df)
    reduc_nms = spectra_list_df.reduced_names_files_list[0]
    fil_lst = spectra_list_df.files_list[0]
    spc_pth = spectra_list_df.spectra_path[0]
    spec_name, reduced_name = select_spectrum_from_folder_list(
        reduc_nms, fil_lst, spc_pth, some_spectrum_pattern
        )
    print( spec_name, reduced_name )
    if spec_name:
        print("Now, go to analysis:")
        a_spec = Spec(spec_name, reduced_name)
        nucl_iear1_df = pd.read_pickle(
            "static/nuclide_libs/nucl_iear1_list.pkl"
        )
        # 2023-Jun-15: Setting gamma lines/ranges to dismiss in the analysis
        df1 = nucl_iear1_df
        df1["is_to_consider"] = True
        df1.loc[((df1.energy > 509) & (df1.energy < 513)) | (df1.energy < 100), "is_to_consider"] = False
        del df1
        print(nucl_iear1_df)
        a_spec.total_analysis(gener_dataframe=True)
        a_spec.identify_nuclides(nucl_iear1_df)
    else:
        print("Nothing to do.")
    print("Terminated ok!")

app_runner()
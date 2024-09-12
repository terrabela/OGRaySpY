import pandas as pd
from source.classes.ograyspy_class import Ograyspy


def reduced_names_df(folder_to_find):
    # Incorporate data
    # df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

    # Put here a folder in your system with spectra:
    ogra = Ograyspy(folder_to_find=folder_to_find)
    print(ogra.info_node)
    print(ogra.pkl_folder_files)
    spectra_list_df = pd.read_pickle(ogra.pkl_folder_files)

    reduc_nms = spectra_list_df.reduced_names_files_list[0]
    fil_lst = spectra_list_df.files_list[0]
    spc_pth = spectra_list_df.spectra_path[0]
    df = pd.DataFrame(reduc_nms)
    return df

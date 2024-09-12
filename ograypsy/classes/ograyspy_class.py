import platform
from pathlib import Path
import pickle
import os
import pandas as pd


def process_pickle_file(my_file, pickle_df):
    if os.path.isfile(my_file):  # if file exists we have already pickled a list
        print('Load existing pickle file')
        with open(my_file, 'rb') as f:
            pickle_df = pickle.load(f)
    else:
        print('Create new pickle file')
        with open(my_file, 'wb') as f:
            pickle.dump(pickle_df, f)
    return pickle_df


class Ograyspy:
    # files_list: list[str]

    def __init__(self, folder_to_find=''):
        # self.dir_list = DirectoryList()
        self.spectra_names_df = None
        self.spectra_lists_df = None
        self.environment_df = None
        self.info_plat = platform.platform()
        self.info_mach = platform.machine()
        self.info_syst = platform.system()
        self.info_node = platform.node()
        self.home_path = Path.home()
        self.spectra_path = Path('../..')
        self.n_files = 0
        self.a_spec_ind = 0
        self.a_spec_name = ''
        self.reduced_f_name = ''
        self.spectra_pattern_names = ["**/*.[Cc][Hh][Nn]", "**/*.[Ii][Ee][Cc]"]
        self.pkl_folder_files = Path('../..')
        self.results_path_name = '../../ograyspy_results'
        if not os.path.exists(self.results_path_name):
            os.mkdir(self.results_path_name)
        self.define_files_folder(folder_to_find)

    def define_files_folder(self, a_pattern=''):
        # Locate the general folder containing spectra in the current system,...
        matching_folders = [i for i in Path.home().glob('*/' + a_pattern)]
        if len(matching_folders) != 0:
            self.spectra_path = matching_folders[0]
        else:
            self.spectra_path = Path('../../data/some_spectra')

        n_parts_dropped = len(self.spectra_path.parts)

        files_list = []
        reduced_names_files_list = []
        for a_pattern in self.spectra_pattern_names:
            for i in self.spectra_path.glob(a_pattern):
                files_list.append(i)
                reduced_names_files_list.append('/'.join(i.parts[n_parts_dropped:]))
        self.n_files = len(files_list)
        print('No. spec files: ', self.n_files)

        self.pkl_folder_files = Path(self.info_syst + '_' + self.info_node).with_suffix('.pkl')
        ogra_vars = vars(self)
        environment_vars = ['info_plat', 'info_mach', 'info_syst', 'info_node', 'home_path', 'spectra_path',
                            'n_files', 'spectra_pattern_names', 'pkl_folder_files', 'results_path_name']

        values = [ogra_vars[a] for a in environment_vars]
        self.environment_df = pd.DataFrame(data=values, index=environment_vars)
        self.spectra_names_df = pd.DataFrame(
            data={'files_list': files_list,
                  'reduced_names_files_list': reduced_names_files_list}
        )


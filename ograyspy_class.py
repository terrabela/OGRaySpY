import platform
from random import randrange
from pathlib import Path
import pickle
import os
import pandas as pd


def select_spectrum_from_folder_list(reduced_names_file_list, files_list,
                                     spectra_path, a_pattern='', random_spectrum=False):
    # Select a random spectrum...
    n_files = len(reduced_names_file_list)
    if random_spectrum:
        try:
            a_spec_ind = randrange(n_files)
            print('Random spec index: ', a_spec_ind)
            a_spec_name = files_list[a_spec_ind]
            reduced_f_name = reduced_names_file_list[a_spec_ind]
            print('...and its name: ', a_spec_name)
        except ValueError:
            print('No random spectrum found...')
        # ...or define it directly.
    else:
        print('Existing:')
        achou = False
        a_spec_ind = None
        nomearq = ''
        for i, j in enumerate(reduced_names_file_list):
            if a_pattern in j:
                achou = True
                a_spec_ind = i
                nomearq = j
                break
        if achou:
            print(f'Achou! indice={a_spec_ind}, nomearq = {nomearq}')
            a_spec_name = files_list[a_spec_ind]
            reduced_f_name = reduced_names_file_list[a_spec_ind]

        matching_spec_name = [i for i in spectra_path.glob(a_pattern)]
        if len(matching_spec_name) != 0:
            for i in matching_spec_name:
                print('name: ', i)
            a_spec_name = matching_spec_name[0]

    print('==========================')
    print('Final choices:')
    print(f'spectra_path: {spectra_path}')
    print(f'a_spec_name: {a_spec_name}')
    print(f'reduced_f_name: {reduced_f_name}')
    return a_spec_name, reduced_f_name



class Ograyspy:
    files_list: list[str]

    def __init__(self, batch_mode=False, folder_to_find=''):
        # self.dir_list = DirectoryList()
        self.info_plat = platform.platform()
        self.info_mach = platform.machine()
        self.info_syst = platform.system()
        self.info_node = platform.node()
        self.home_path = Path.home()
        self.spectra_path = Path('.')
        self.n_files = 0
        self.a_spec_ind = 0
        self.a_spec_name = ''
        self.reduced_f_name = ''
        self.define_files_folder(folder_to_find)
        # self.gross_counts_graphics = None
        # self.pks_regions_gros = None

    def process_pickled_list(self, my_file):
        if os.path.isfile(my_file):  # if file exists we have already pickled a list
            print('Load existing pickle file')
            with open(my_file, 'rb') as f:
                self.files_list = pickle.load(f)
        else:
            print('Create new pickle file')
            with open(my_file, 'wb') as f:
                pickle.dump(self.files_list, f)

        # my_file = 'ogra_pic_f_' + self.info_syst + '_' + self.info_node + '.pkl'
        # self.process_pickled_list(my_file='')

    def define_files_folder(self, a_pattern=''):
        # Locate the general folder containing spectra in the current system,...
        matching_folders = [i for i in Path.home().glob('*/' + a_pattern)]
        if len(matching_folders) != 0:
            self.spectra_path = matching_folders[0]
            print('Found folder name: ', self.spectra_path)
        else:
            print('Folder name not found. Using default sample folder')
            self.spectra_path = Path('static/spectra')
            print('Folder name explicitly named: ', self.spectra_path)

        print('Parts: ', self.spectra_path.parts)
        n_parts_dropped = len(self.spectra_path.parts)

        self.files_list = []
        self.reduced_names_files_list = []
        self.spectra_pattern_names = ["**/*.[Cc][Hh][Nn]", "**/*.[Ii][Ee][Cc]"]
        for a_pattern in self.spectra_pattern_names:
            for i in self.spectra_path.glob(a_pattern):
                self.files_list.append(i)
                self.reduced_names_files_list.append('/'.join(i.parts[n_parts_dropped:]))
        self.n_files = len(self.files_list)
        print('No. spec files: ', self.n_files)

        self.pkl_folder_files = Path(self.info_syst + self.info_node).with_suffix('.pkl')
        ogra_vars = vars(self)
        campos = [a for a in ogra_vars]
        valores = [ogra_vars[a] for a in ogra_vars]
        # spec_df_type1 = pd.DataFrame(data=valores, index=campos)
        # spec_df_type1.to_pickle(self.pkl_file)
        spec_df_type2 = pd.DataFrame(data=[valores], columns=campos)
        spec_df_type2.to_pickle(self.pkl_folder_files)


    def select_spectrum(self, a_pattern='', random_spectrum=False):
        # Select a random spectrum...
        if random_spectrum:
            try:
                self.a_spec_ind = randrange(self.n_files)
                print('Random spec index: ', self.a_spec_ind)
                self.a_spec_name = self.files_list[self.a_spec_ind]
                self.reduced_f_name = self.reduced_names_files_list[self.a_spec_ind]
                print('...and its name: ', self.a_spec_name)
            except ValueError:
                print('No random spectrum found...')

        # ...or define it directly.
        else:
            print('Existing:')
            achou = False
            self.a_spec_ind = None
            nomearq = ''
            for i, j in enumerate(self.reduced_names_files_list):
                if a_pattern in j:
                    achou = True
                    self.a_spec_ind = i
                    nomearq = j
                    break
            if achou:
                print(f'Spectrum found: indice={self.a_spec_ind}, nomearq = {nomearq}')
                self.a_spec_name = self.files_list[self.a_spec_ind]
                self.reduced_f_name = self.reduced_names_files_list[self.a_spec_ind]

            matching_spec_name = [i for i in self.spectra_path.glob(a_pattern)]
            if len(matching_spec_name) != 0:
                for i in matching_spec_name:
                    print('name: ', i)
                self.a_spec_name = matching_spec_name[0]

        print('==========================')
        print('Final choices:')
        print(f'spectra_path: {self.spectra_path}')
        print(f'a_spec_name: {self.a_spec_name}')
        print(f'reduced_f_name: {self.reduced_f_name}')
        return self.a_spec_name, self.reduced_f_name

#   2023-Mar-22: AQUI: REFATORAR
#    def perform_batch_analyses(self):
#        self.define_files_batch()
#        print(self.files_list)
#        for nam in self.files_list:
#            spec = Spec(nam)
#            spec.total_analysis(gener_dataframe=True)

 #   def call_graphics(self):
 #       cts_graph = CountsGraphic(self.a_spec_name, self.a_spec.gross_spec_ser_an,
 #                                 self.home_path, 'gross_counts_graph')
 #       pk_regs_graph = PeaksAndRegionsGraphic(self.a_spec_name, self.a_spec.gross_spec_ser_an,
 #                                              self.home_path, 'gross_pks_reg_graph')
 #       net_pk_regs_graph = PeaksAndRegionsGraphic(self.a_spec_name, self.a_spec.net_spec_ser_an,
 #                                              self.home_path, 'net_pks_reg_graph')


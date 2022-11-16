import platform
from random import randrange
from pathlib import Path
import pickle
import os

from spec_class import Spec
from spec_graphics_class import GenericGraphics
from spec_graphics_class import CountsGraphic, PeaksAndRegionsGraphic, BaselineGraphic

class Ograyspy:
    files_list: list[str]

    def __init__(self, speed=0):
        # self.dir_list = DirectoryList()
        self.info_plat = platform.platform()
        self.info_mach = platform.machine()
        self.info_syst = platform.system()
        self.info_node = platform.node()
        self.home_path = Path.home()
        print(self.info_plat + ';' + self.info_mach + ';' + self.info_syst + ';' + self.info_node)
        print(self.home_path)
        self.spectra_path = Path('.')
        self.n_files = 0
        self.a_spec_ind = 0
        self.a_spec_name = ''
        self.gross_counts_graphics = None
        self.pks_regions_gros = None

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

    def define_files_batch(self):
        # Locate the general folder containing spectra in the current system,...
        # to_be_found = 'gamma'
        to_be_found = 'Genie_Transfer'
        matching_folders = [i for i in Path.home().glob('*/' + to_be_found)]
        if len(matching_folders) != 0:
            self.spectra_path = matching_folders[0]
            print('Found folder name: ', self.spectra_path)
        else:
            print('Folder name not found. Using local folder')
            # ...or define it directly.
            # self.spectra_path = Path('data/some_spectra')
            self.spectra_path = Path('..')
            print('Folder name explicitly named: ', self.spectra_path)

        print('Partes: ', self.spectra_path.parts)
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
        
        
    def select_spectrum(self):
        define_files_batch()
        # Select a random spectrum...
        try:
            self.a_spec_ind = randrange(self.n_files)
            print('Random spec index: ', self.a_spec_ind)
            self.a_spec_name = self.files_list[self.a_spec_ind]
            print('...and its name: ', self.a_spec_name)
        except ValueError:
            print('No spectrum found...')

        # ...or define it directly.
        # 2022-out-7: Excelente espectro para testes, tenho usado ultimamente:
        a_pattern = 'Si/SI2018/SI11318.Chn'
        # 2022-nov-16: outros espectros:
        # a_pattern = "Filtros/2022/Cci/CCI1603-I.Chn"
        # a_pattern = "Eso_non_existe.Chn"
        print('Existing:')
        matching_spec_name = [i for i in self.spectra_path.glob(a_pattern)]
        if len(matching_spec_name) != 0:
            for i in matching_spec_name:
                print ('name: ', i)
            self.a_spec_name = matching_spec_name[0]

        print('==========================')
        print('Final choices:')
        print(self.spectra_path)
        print(self.a_spec_name)

    def perform_total_analysis(self):
        self.a_spec = Spec(self.a_spec_name)
        self.a_spec.total_analysis()
        print('Fez total analysis.')
        
    def perform_batch_analyses(self):
        self.define_files_batch()
        print(self.files_list)
        for nam in self.files_list:
            spec = Spec(nam)
            spec.total_analysis(gener_dataframe=True)

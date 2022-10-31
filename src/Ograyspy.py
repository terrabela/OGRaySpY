import platform
from random import randrange
from pathlib import Path
import pickle
import os
from spec_class import Spec
from spec_graphics_class import GrossCountsGraphic, PeaksAndRegionsGraphic,\
    BaselineGraphic, NetSpecGraphic


class Ograyspy:
    files_list: list[str]

    def __init__(self, speed=0):
        # self.dir_list = DirectoryList()
        self.info_plat = platform.platform()
        self.info_mach = platform.machine()
        self.info_syst = platform.system()
        self.info_node = platform.node()
        print(self.info_plat + ';' + self.info_mach + ';' + self.info_syst + ';' + self.info_node)
        self.spectra_path = Path('.')
        self.n_files = 0
        self.a_spec_ind = 0
        self.a_spec_name = ''
        self.gross_counts_graphics = None
        self.pks_regions_gros = None

        self.select_spectrum()

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

    def select_spectrum(self):
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
        # Select a random spectrum...
        self.files_list = []
        self.reduced_names_files_list = []
        self.spectra_pattern_names = ["**/*.[Cc][Hh][Nn]", "**/*.[Ii][Ee][Cc]"]
        for a_pattern in self.spectra_pattern_names:
            for i in self.spectra_path.glob(a_pattern):
                self.files_list.append(i)
                self.reduced_names_files_list.append('/'.join(i.parts[n_parts_dropped:]))
        self.n_files = len(self.files_list)
        print('No. spec files: ', self.n_files)
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

        print('Objeto a_spec.net_spec_ser_an.pk_parms:')
        # print(vars(self.a_spec.net_spec_ser_an.pk_parms))

        # E finalmente soma as contagens líquidas de 4 FWHMs:
        # self.a_spec.net_spec_ser_an.pk_parms.regions_to_sum()
        # self.a_spec.net_spec_ser_an.cnt_arrs.final_sums(
        #     self.a_spec.net_spec_ser_an.pk_parms
        # )

    def create_graphics(self):
        self.gross_counts_graphics = GrossCountsGraphic(self.a_spec_name,
                                                        self.a_spec.gross_spec_ser_an)
        self.gross_counts_graphics.plot_figw1(self.a_spec.gross_spec_ser_an,
                                              'Gross counts (original and smoothed)')
        del self.gross_counts_graphics

        # self.pks_regions_gros = PeaksAndRegionsGraphic(self.a_spec_name,
        #                                                self.a_spec.gross_spec_ser_an,
        #                                                self.a_spec.)
        # self.pks_regions_gros.plot_figw2(self.a_spec.gross_spec_ser_an,
        #                                  'Peaks & regions (gross spec)')
        # del self.pks_regions_gros
        # pks_regions_gros.plot_figw2(a_spec.gross_spec_ser_an, 'origi_bruta_larguras')

        # pks_regions_smoo = PeaksAndRegionsGraphic(self.a_spec_name, a_spec.smoo_gross_ser_an)
        # pks_regions_smoo.plot_figw2(a_spec.smoo_gross_ser_an, 'suavi_bruta_larguras')

        # baseline_graph = BaselineGraphic(self.a_spec_name, a_spec.gross_spec_ser_an)
        # baseline_graph.plot_figbl(a_spec.gross_spec_ser_an, 'Linha_base_espectro_original')
        # netspec_graph = NetSpecGraphic(a_spec.gross_spec_ser_an, 'Net spec')
        # netspec_graph.plot_figns(a_spec.gross_spec_ser_an, 'Net spec')
        # pks_regions_net = PeaksAndRegionsGraphic(self.a_spec_name, a_spec.net_spec_ser_an)
        # pks_regions_net.plot_figw2(a_spec.net_spec_ser_an, 'Net peaks, finally.')


if __name__ == '__main__':
    print("I'm a OGRaySPy (gamma-ray spectra analyzer!")
    my_ogra = Ograyspy()
    my_ogra.perform_total_analysis()
    my_ogra.create_graphics()
    del my_ogra.a_spec

    # a_graph.plot_graphics()
    # End of main program.
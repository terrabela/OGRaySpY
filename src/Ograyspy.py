import platform
from random import randrange
from typing import List

from dir_listing import DirectoryList
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
        print(self.info_plat + ' ' + self.info_mach + ' ' + self.info_syst + ' ' + self.info_node)

    def select_spectrum(self):
        # Locate the general folder containing spectra in the current system
        general_spectra_folder_name = 'some_spectra'

        interm_list = [i for i in Path.home().glob('**/' + general_spectra_folder_name)]
        self.spectra_path = interm_list[0]
        print(self.spectra_path)

        my_file = 'ogra_pic_f_' + self.info_syst + '_' + self.info_node + '.pkl'

        if os.path.isfile(my_file):  # if file exists we have already pickled a list
            print('Load existing pickle file')
            with open(my_file, 'rb') as f:
                self.files_list = pickle.load(f)
        else:
            print('Create new pickle file')
            self.files_list = []
            for i in self.spectra_path.glob("**/*.[Cc][Hh][Nn]"):
                self.files_list.append('/'.join(i.parts[5:]))
            for i in self.spectra_path.glob("**/*.[Ii][Ee][Cc]"):
                self.files_list.append('/'.join(i.parts[5:]))
            with open(my_file, 'wb') as f:
                pickle.dump(self.files_list, f)

        self.n_files = len(self.files_list)

        print('No. spec files: ', my_ogra.n_files)

        # given_spec_name = "Filtros/2022/Cci/CCI1603-I.Chn"

        # 2022-out-7: Excelente espectro para testes, tenho usado ultimamente:
        given_spec_name = "Si/SI2018/SI11318.Chn"

        # given_spec_name = "Eso_non_existe.Chn"

        if given_spec_name in my_ogra.files_list:
            print("Found!")
            self.complete_spec_name = str(my_ogra.spectra_path) + '/' + given_spec_name
        else:
            print("Not found... :-( ")
            # Choose random spectrum:
            self.a_spec_ind = randrange(self.n_files)
            print('Random spec index: ', my_ogra.a_spec_ind)
            a_spec_name: str = my_ogra.files_list[my_ogra.a_spec_ind]
            print('...and its name: ', a_spec_name)
            # Bad spectrum file name is calculated by the next line:
            # self.complete_spec_name = str(my_ogra.spectra_path) + '/' + a_spec_name
            # What follows is a remendo
            upper_directory = '~/PycharmProjects/OGRaySpY'
            self.complete_spec_name = upper_directory + '/' + a_spec_name
    def perform_total_analysis(self):
        print(self.complete_spec_name)
        a_spec = Spec(self.complete_spec_name)

        a_spec.total_analysis()
        print('Fez total analysis.')

        print('Objeto a_spec.net_spec_ser_an.pk_parms:')
        print(vars(a_spec.net_spec_ser_an.pk_parms))

        # E finalmente soma as contagens líquidas de 4 FWHMs:
        # a_spec.net_spec_ser_an.pk_parms.regions_to_sum()
        # a_spec.net_spec_ser_an.cnt_arrs.final_sums(
        #     a_spec.net_spec_ser_an.pk_parms
        # )

    def create_graphics(self):
        gross_counts_graphics = GrossCountsGraphic(self.complete_spec_name, a_spec.gross_spec_ser_an)
        gross_counts_graphics.plot_figw1(a_spec.gross_spec_ser_an, 'cont_bruta_origi')

        smoothed_graph = GrossCountsGraphic(self.complete_spec_name, a_spec.smoo_gross_ser_an)
        smoothed_graph.plot_figw1(a_spec.smoo_gross_ser_an, 'cont_bruta_suavi')


        pks_regions_gros = PeaksAndRegionsGraphic(self.complete_spec_name, a_spec.gross_spec_ser_an)
        pks_regions_gros.plot_figw2(a_spec.gross_spec_ser_an, 'origi_bruta_larguras')

        # pks_regions_smoo = PeaksAndRegionsGraphic(self.complete_spec_name, a_spec.smoo_gross_ser_an)
        # pks_regions_smoo.plot_figw2(a_spec.smoo_gross_ser_an, 'suavi_bruta_larguras')

        baseline_graph = BaselineGraphic(self.complete_spec_name, a_spec.gross_spec_ser_an)
        baseline_graph.plot_figbl(a_spec.gross_spec_ser_an, 'Linha_base_espectro_original')
        netspec_graph = NetSpecGraphic(a_spec.gross_spec_ser_an, 'Net spec')
        netspec_graph.plot_figns(a_spec.gross_spec_ser_an, 'Net spec')
        pks_regions_net = PeaksAndRegionsGraphic(complete_spec_name, a_spec.net_spec_ser_an)
        pks_regions_net.plot_figw2(a_spec.net_spec_ser_an, 'Net peaks, finally.')


if __name__ == '__main__':
    print("I'm a OGRaySPy (gamma-ray spectra analyzer!")
    my_ogra = Ograyspy()
    my_ogra.select_spectrum()
    my_ogra.perform_total_analysis()
    # my_ogra.create_all_graphics()


    # a_graph.plot_graphics()
    # End of main program.
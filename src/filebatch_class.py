# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 12:04:52 2018

@author: Marcelo
"""

from pathlib import (Path)

class FileBatch:
    """ File batch building class. """
    def slot_set_batch_iec(self, locpath):
        """ iec files batch """
        # 2017-07-20 usando Path.glob
        self.loc_path = Path( locpath )
        print( locpath )
        # list_path_p is a system-aware list of path p
        self.list_path_p = list( self.loc_path.glob('**/*.[Ii][Ee][Cc]'))
        # list_p is a list of strings from lpp
        self.list_p = [ str(ip) for ip in self.list_path_p ]

        # https://docs.python.org/3.7/library/string.html
        self.arqs_list = ''
        for i_lp in self.list_p:
            self.arqs_list += i_lp + '\n'
        self.numarqs = len(self.list_p)
        self.numarqstxt  = 'Num de arquivos: {:>10} \n\n\n'.format(self.numarqs)
        self.anallog_str = '\n' + self.arqslist + '\n' + self.numarqstxt

    def slot_set_batch_chn(self, locpath):
        """ chn files batch """
        # 2017-07-20 usando Path.glob
        self.loc_path = Path( locpath )
        print( locpath )
        # lpp is a system-aware list of path p
        self.list_path_p = list( self.loc_path.glob('**/*.[Cc][Hh][Nn]'))
        # lp is a list of strings from lpp
        self.list_p = [ str(ip) for ip in self.list_path_p ]

        # 2019-03-05 list of filenames with path separators as semicolons
        self.lpsemic = [ ip.replace('/',';') for ip in self.list_p ]
        # 2019-03-05 changing extension
        self.lpcsv = [ str(Path(ip).with_suffix('.csv')) for ip in self.lpsemic ]
        strteste1 = Path('um/dois/tres.qautro')
        self.teste1 = strteste1.with_suffix('.csv')

        # https://docs.python.org/3.7/library/string.html
        self.arqs_list = ''
        for i_lp in self.list_p:
            self.arqs_list += i_lp + '\n'
        self.numarqs = len(self.list_p)
        self.numarqstxt  = 'Num de arquivos: {:>10} \n\n\n'.format(self.numarqs)
        self.anallog_str = '\n' + self.arqs_list + '\n' + self.numarqstxt

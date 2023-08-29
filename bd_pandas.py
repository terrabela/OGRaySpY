

# 2022-Jan-13:
# Aqui vou definir um lote de espectros, localizar os picos e fazer a análise segundo
# 2021-Out-26: agora lmfit já está no canal conda-forge.

import numpy as np
import numpy.ma as ma  # masked array
from numpy.polynomial import Polynomial as P # 2020-09-06 Esta é a nova classe recomendada
from numpy import linalg as LA



# https://realpython.com/python-import/
# https://docs.python-guide.org/writing/structure/

import scipy.stats as sta # statistics
# from scipy.special import (erf, erfinv)
import scipy.special as spsp
from scipy.optimize import curve_fit
# import scipy.optimize as spoptim
# 2020-08-30
from scipy import ndimage # label, generate_binary_structure, find_objects, binary_dilation
from scipy.cluster.vq import kmeans2, whiten

####################################
# Para a coleta dos espectros:
import time
# 2019-03-15
# https://pandas.pydata.org/pandas-docs/stable/getting_started/10min.html
import pandas as pd
import csv
# from pathlib import (Path)
from pathlib import Path

# 2021-Jul-08
# from lmfit import Model, Minimizer, minimize, Parameters, report_fit, fit_report, printfuncs

# https://lmfit.github.io/lmfit-py/
# builtin_models.html?highlight=peaks%20sum#example-3-
# fitting-multiple-peaks-and-using-prefixes
# from lmfit.models import ExponentialModel, GaussianModel

# Gráficos e widgets:
import plotly.graph_objects as go
# from ipywidgets import widgets
# 2022-Jan-20: em princípio, usarei plotly em vez de bokeh ou matplotlib.
# from bokeh.models import ColumnDataSource, Whisker
# from bokeh.plotting import figure, output_file, output_notebook, show
# from bokeh import palettes
# import matplotlib.pyplot as plt

# 2022-Fev-02 Módulos desenvolvidos ad hoc

from gauss_funcs import gaus_fw, gaus_sig

# 2022-Jan-20: Desativado por enquanto
# import base_line_funcs as blf
# import spectra_regions_funcs as spreg

# 2021-jun-2: novas classes:
from spec_class import Spec
# 2022-Jan-13
from filebatch_class import (FileBatch)

from machine_selection import set_screen_size_by_machine

# 2021-Jul-1
# import gauss_funcs

# https://stackoverflow.com/questions/19861785/composition-and-aggregation-in-python
# https://stackoverflow.com/questions/12053998/...
# where-should-i-define-functions-that-i-use-in-init#12054066
# https://www.codearmo.com/python-tutorial/object-orientated-programming-functions

# Sobre declarar os atributos em init:
# https://softwareengineering.stackexchange.com/questions/357937/...
# is-it-really-correct-to-declare-all-instance-attributes-in-init

# Sobre listar atributos omitindo os "built in" (com 2 underscores duplos):
# https://stackoverflow.com/questions/192109/...
# is-there-a-built-in-function-to-print-all-the-current-properties-and-values-of-a#193539

# Longo e ótimo texto sobre inheritance, composition, aggregation....
# https://realpython.com/inheritance-composition-python/#composition-in-python

# Pequeno vídeo sobre UML:
# https://realpython.com/lessons/uml-diagrams/
#
# UML:
# - Open-Source
# https://github.com/abulka/pynsource
# - Trial
# https://staruml.io/

# https://realpython.com/python-import/
# https://docs.python-guide.org/writing/structure/

# https://stackoverflow.com/questions/19861785/...
# composition-and-aggregation-in-python#19863217

# https://linuxconfig.org/how-to-find-a-string-or-text-in-a-file-on-linux
#
# Para achar texto dentro de conjunto de arquivos:
# Para descobrir qual script gerou os "todos_si*.pkl":
# grep -r todos_si ~/OwnDrive/Python_Scripts >grep_r_todos_si.txt
#
# Achei os seguintes arquivos:
# 2019-nov-warp2.ipynb
# openGamma_pkl-generation.ipynb
# 2020_ridge_tests_with_I123.ipynb
# 2019-gerar-pkl-CAC-2018.ipynb
# 2020_Mariana-PR_agua-bruta.ipynb
# 2020_Mariana-PR_AgAm3-2911.ipynb
# 2020_Mariana-decan4.ipynb
# 2020-PCA-in-gamma-ray.ipynb
#
[4]
# 2022-Jan-14
# Constante k_ar para cálculo da área em fç de sigma e h (altura) do pico

class BdPandas:
    def __init__(self):
    k_ar = 0.5 * np.sqrt(np.pi / np.log(2))
    k_fwhm = spsp.erf(np.sqrt(np.log(2)))
    dir_A = set(dir())
    dir_A


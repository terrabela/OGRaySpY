Usage
=====

The module with the base class holding all data related to a single spectrum is:

.. automodule:: spec_class
   :members:
   
The ograyspy class is:

-- autoclass:: Spec
   :members:

.. _installation:

Requisites
----------

OGRaySpY, the Open app for Gamma-RAY SPectra Analysis and visualization, requires:

- [Pandas](http://pandas.pydata.org/) for results reporting.
- [Plotly](https://plotly.com/python/) for spectra interactive graphing
- [PySide2](https://pypi.org/project/PySide2/) for the UI
- numpy / scipy / lmfit to perform all the Math.

Basic usage
-----------

- Run ograyspy_main_ui.py in a Python console to start main program's interface
- Invoke menu File --> Open spectrum and generate report.
  Some - real - example spectra as .chn files are in folder data/some_spectra.

- Choose a .chn or .iec spectrum
- Peak report will be shown and saved as an_html_file.html.

.. OGRaySpY documentation master file, created by
   sphinx-quickstart on Sat Jul 20 16:46:58 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to OGRaySpY's documentation!
====================================

**OGRaySpY** is an Open app for Gamma-RAY SPectra
analYsis and visualization.

This application requires:

- Pandas (http://pandas.pydata.org/) for results reporting.
- Plotly (https://plotly.com/python/) for spectra interactive graphing
- PySide2 for UI
- numpy/scipy/lmfit to perform all the Math.

Basic usage
===========

- Run ograyspy_main_ui.py in a Python console to start main program's interface
- Invoke menu File --> Open spectrum and generate report
- Choose a .chn or .iec spectrum
- Peak report will be shown and saved as an_html_file.html.

Documentation
=============

.. note::

   Under development at Read the Docs (https://ograyspy.readthedocs.io)


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   usage
   analysissteps
   spectrumload
   smoothing
   roisdefine
   netspectrum
   roisdefineinnet
   fwhmvschannel
   api
   example/loadanddisplay


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

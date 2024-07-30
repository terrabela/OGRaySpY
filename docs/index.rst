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

- Open the Jupyter Notebook notebooks/step_by_step_analysis.ipynb
- As its name implies, you will have a minimal python commands in sequence to perform a basic analysis on a gamma=ray spectrum.

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

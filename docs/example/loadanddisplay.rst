Load and display a spectrum
===========================


Firstly we set the folders to search as needed:

.. code-block:: console

   import sys
   sys.path.insert(1, '../ograyspy')
   from ograyspy.spec_class import Spec

Now we load an example spectrum and set it as a Spec object.

.. code-block:: console

   a_spectr = Spec(
       fpc_fname='SI06122.Chn',
       spectra_path='../data/some_spectra',
       to_smooth=True
   )

To display the preliminar spectrum plot, we do

.. code-block:: console

   from ograyspy.spec_graphics_class import CountsGraphic
   plot1 = CountsGraphic(
       ser_an=a_spectr.origin_spec_ser_an,
       gen_html=True
   )


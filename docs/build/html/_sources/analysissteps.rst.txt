Analysis steps
==============

The analysis of a gamma-ray spectrum typically involves the sequential execution of several steps. Which steps are carried out will depend on which settings, calibrations, libraries to use, are already defined in the spectrometry system as a whole.

To make it clearer, analyzing a spectrum from scratch will generally involve carrying out the following sequence:

- Loading the spectrum
- Smoothing
- Delimitation of regions potentially containing peaks, or regions of interest (ROIs)
- Base line and net spectrum calculation
- New delimitation of ROIs, but now in the net spectrum
- Preliminary calculation on the liquid peaks to obtain the respective full widths at half height (FWHMs).
- Obtaining an adjustment of the FWHMs as a function of the channels
- Obtaining the final peak parameters, which will essentially be the respective centroids and heights, with the previously adjusted FWHMs.

These are the steps for obtaining the net areas of the peaks. To obtain the activities of the radionuclides present in the sample, additional steps will be necessary:

- Calibration of photopeak energy vs. channel
- Calibration of counting efficiency vs energy
- Activity calculations using nuclide libraries.

In what follows, each of the previous steps will be described in detail.
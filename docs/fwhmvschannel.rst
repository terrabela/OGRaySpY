FWHMs and tail parameters vs channel
====================================

Normally, each peak in a gamma spectrum can be fitted by a Gaussian
function, to which an exponential tail is eventually added.

Gaussian functions are defined by 3 parameters: the centroid, the
height and the width. If an exponential tail is used, there is an
additional parameter. The fit can be made for each peak and the
resulting values used directly to obtain the net area, which is the
ultimate goal.

For various reasons, however, a better practice is to use the width
and tail parameters obtained for selected “good” peaks in the
spectrum and then obtain fit functions of these parameters versus
channel. We then fit each peak again, now setting the width and
tail parameters for each one. The free parameters to be obtained
in the fit will be now only the height and centroid.
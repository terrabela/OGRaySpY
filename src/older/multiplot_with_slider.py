import numpy
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
# fake data
xdata = numpy.random.rand(100,100) 
ydata = numpy.random.rand(100,100) 
# set up figure
fig = plt.figure()
ax = fig.add_subplot(111)
ax.autoscale(True)
plt.subplots_adjust(left=0.25, bottom=0.25)

# plot first data set
frame = 0
ln, = ax.plot(xdata[frame],ydata[frame])

# make the slider
axframe = plt.axes([0.25, 0.1, 0.65, 0.03])
sframe = Slider(axframe, 'Frame', 0, 99, valinit=0,valfmt='%d')

# call back function
def update(val):
    frame = numpy.floor(sframe.val)
    ln.set_xdata(xdata[frame])
    ln.set_ydata((frame+1)* ydata[frame])
    ax.set_title(frame)
    ax.relim()
    ax.autoscale_view()
    plt.draw()

# connect callback to slider   
sframe.on_changed(update)

plt.show()
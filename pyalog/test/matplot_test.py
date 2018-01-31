# -*- noplot -*-

"""
This example shows how to use matplotlib to provide a data cursor.  It
uses matplotlib to draw the cursor and may be a slow since this
requires redrawing the figure with every mouse move.

Faster cursoring is possible using native GUI drawing, as in
wxcursor_demo.py.

The mpldatacursor and mplcursors third-party packages can be used to achieve a
similar effect.  See
    https://github.com/joferkington/mpldatacursor
    https://github.com/anntzer/mplcursors
"""
from __future__ import print_function
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import datetime
import random
class Cursor(object):
    def __init__(self, ax):
        self.ax = ax
        self.lx = ax.axhline(color='k')  # the horiz line
        #self.ly = ax.axvline(color='k')  # the vert line
        self.ly = ax.axvline(datetime.datetime.now(),color='k')
        # text location in axes coords
        #self.txt = ax.text(0.7, 0.9, '', transform=ax.transAxes)

    def mouse_move(self, event):
        if not event.inaxes:
            return

        x, y = event.xdata, event.ydata
        print(x,y)
        # update the line positions
        self.lx.set_ydata(y)
        #self.ly.set_xdata(x)

        #self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))

        plt.draw()


class SnaptoCursor(object):
    """
    Like Cursor but the crosshair snaps to the nearest x,y point
    For simplicity, I'm assuming x is sorted
    """
    '''

    def __init__(self, ax, x, y):
        self.ax = ax
        self.lx = ax.axhline(color='k')  # the horiz line
        self.ly = ax.axvline(color='k')  # the vert line
        self.x = x
        self.y = y
        # text location in axes coords
        self.txt = ax.text(0.7, 0.9, '', transform=ax.transAxes)
      def mouse_move(self, event):

            if not event.inaxes:
                return

            x, y = event.xdata, event.ydata

            indx = np.searchsorted(self.x, [x])[0]
            x = self.x[indx]
            y = self.y[indx]
            # update the line positions
            self.lx.set_ydata(y)
            self.ly.set_xdata(x)

            self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))
            print('x=%1.2f, y=%1.2f' % (x, y))
            plt.draw()
    '''
    def __init__(self, ax,line_2d):
        self.ax = ax
        self.line = line_2d
        self.lx = ax.axhline(y=2,color='k')  # the horiz line
        self.ly = ax.axvline(x=line_2d.get_xdata()[5],color='k')  # the vert line

        # text location in axes coords
        self.txt = ax.text(line_2d.get_xdata()[3], 5, str(y))

    def mouse_move(self, event):

        if not event.inaxes:
            return

        x, y = event.xdata, event.ydata
        x_s = self.line.get_xdata(orig=False)
        indx = np.searchsorted(x_s, [x])[0]
        #print(indx)
        x = self.line.get_xdata()[indx]
        y = self.line.get_ydata()[indx]
        # update the line positions
        self.lx.set_ydata(y)
        self.ly.set_xdata(x)

        #self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))
        #print('x=%1.2f, y=%1.2f' % (x, y))
        plt.draw()

# make up some data
x = [datetime.datetime.now() + datetime.timedelta(days=i) for i in range(12)]
#y = [i + random.gauss(0, 1) for i, _ in enumerate(x)]
y= [ i for i in range(12)]
# plot
#plt.scatter(x, y)
# beautify the x-labels
#plt.gcf().autofmt_xdate()

#plt.show()

#t = np.arange(0.0, 1.0, 0.01)
#s = np.sin(2*2*np.pi*t)
s= []
t=[]
for i in range(10): t.append(i)

#for i in range(10): s.append(i)
#for each in range(10): s.append(datetime.datetime(2018,1,each+1))
s = [datetime.datetime.now() + datetime.timedelta(days=i) for i in range(10)]
fig, ax = plt.subplots()
#line= ax.scatter(s,t )
line= plt.plot(s,t)
#print(line[0])
#print (line[0].get_xdata(orig=False))
#cursor = Cursor(ax)
cursor = SnaptoCursor(ax, line[0])
plt.connect('motion_notify_event', cursor.mouse_move)


#plt.axis([0, 1, -1, 1])
plt.show()
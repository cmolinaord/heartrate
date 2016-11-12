import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial, re

frec = 1
buff = ""

nucleo = serial.Serial('/dev/ttyACM0', 9600, timeout = 1)
refresh = 5


lectura1 = nucleo.readline()
values = re.split('>| |\n|\r', lectura1)
t0 = int(values[1])

def data_gen():
    global buff
    buff = nucleo.readline()
    values = re.split('>| |\n|\r', buff)
    t, y = values[1:3]
    t = int(t) - t0
    yield t, float(y)


def init():
    ax.set_ylim(0, 5)
    ax.set_xlim(0, refresh)
    del xdata[:]
    del ydata[:]
    line.set_data(xdata, ydata)
    return line,

fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.grid()
xdata, ydata = [], []

def run(data):
    # update the data
    t, y = data
    xdata.append(t)
    ydata.append(y)
    xmin, xmax = ax.get_xlim()

    if t >= xmax:
        del xdata[:]
        del ydata[:]
        ax.set_xlim(xmax, xmax + refresh)
        ax.figure.canvas.draw()
    line.set_data(xdata, ydata)

    return line,

ani = animation.FuncAnimation(fig, run, data_gen, blit=False, interval=frec,
                              repeat=False, init_func=init)
plt.show()

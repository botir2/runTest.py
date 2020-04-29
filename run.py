from struct import *
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import threading
import time
import serial
import sys
import configs


#QtGui.QApplication.setGraphicsSystem('raster')
app = QtGui.QApplication([])



def Connection(serial_port):
    try:
        serial_port = serial.Serial(configs.port, configs.baudrate, timeout = None)
        print(configs.port, 'connected')
        #print(cofig.port, 'cofig.port')

    except serial.SerialException:
        print('SerialException')

    if not serial_port:
        raise serial.SerialException('not found, but tried hard.')

    return serial_port

def main():
    serial_port = False
    ser = Connection(serial_port)

    ser.write(str.encode("#CSDTP:1%"))

    # split 32-bit integers to be sent into 8-bit data
    # Transmit SH-period
    #ser.write(configs.txsh)
    # Transmit last of the 12 bytes required to start integration
    #ser.write(configs.AVGn)

    ################################################################################
    #
    #   Recieving CCD data
    #
    global naparrays
    while True:
        configs.rxData8 = ser.read(7332)
        # datas = ser.read(100)
        # datas = unpack("q", par)
        # print(datas)
        for rxi in range(3648):
            configs.pltData16[rxi] = (configs.rxData8[2 * rxi + 1] << 8) + configs.rxData8[2 * rxi]
            # print(configs.rxData16)
            naparrays = configs.pltData16
            #naparrays = configs.pltData16
            # print(naparrays[0,])

        # print('Before:\n{}'.format(par.rstrip()))
        # print(int.from_bytes(par[0xFFF0], byteorder='little'))
        # print(int.from_bytes([255, 255, 0], byteorder='big'))
        # time.sleep(.01)

    ser.close()

#
################################################################################
#
#   Graph Show function
#

def PYQtPlot():
    win = pg.GraphicsWindow(title="Basic plotting examples")  # PyQtGraph grahical window
    win.resize(1500, 750)
    win.setWindowTitle('pyqtgraph example: Plotting')  # Title of python window
    # Updating Plot
    global curve, data, ptr, p6
    p6 = win.addPlot(title="CCD 50Hz plot")
    curve = p6.plot(pen='y')
    data = np.random.normal(size=(5000, 3648))
    ptr = 5000
    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(.01)
    QtGui.QApplication.instance().exec_()

def update():
        curve.setData(naparrays)
        print(naparrays)
        p6.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted


if __name__ == '__main__':
    mySerial = threading.Thread(name='mySerial', target=main)
    mySerial.start()
    PYQtPlot()
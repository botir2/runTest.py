from struct import *
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import threading
import time
import serial
import sys
import configs
from scipy import signal

# QtGui.QApplication.setGraphicsSystem('raster')
app = QtGui.QApplication([])


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='lowpass', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = signal.lfilter(b, a, data)
    return y


def moving_average(data_set, periods=3):
    weights = np.ones(periods) / periods
    return np.convolve(data_set, weights, mode='valid')


def Connection(serial_port):
    try:
        serial_port = serial.Serial("COM8", configs.baudrate, timeout=None)
        print(configs.port, 'connected')
        # print(cofig.port, 'cofig.port')

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
    # ser.write(configs.txsh)
    # Transmit last of the 12 bytes required to start integration
    # ser.write(configs.AVGn)

    ################################################################################
    #
    #   Recieving CCD data
    #
    global naparrays
    global t_num
    global P_num
    t_num = 7296
    P_num = int(t_num / 2)

    Lower_limit_value = 10
    upper_limit_value = 100
    rxData8 = np.zeros(t_num, np.uint8)
    pltData16 = np.zeros(P_num, np.uint8)
    pltData = np.zeros(P_num)
    Pixel_plot = np.zeros(500)

    while True:

        rxData8 = ser.read(t_num)  # 8332
        # datas = ser.read(100)
        # datas = unpack("q", par)
        # print(datas)
        for rxi in range(P_num):  # 3648
            pltData16[rxi] = (rxData8[2 * rxi + 1] << 8) + rxData8[2 * rxi]
            # print(configs.rxData16)
            # naparrays = configs.pltData16

            # print(naparrays[0,])
        max_pixel_num = np.where(pltData16 == pltData16.max())

        for j in range(0, len(max_pixel_num[0])):
            pltData16[max_pixel_num[0][j]] = 0

        pltData = butter_lowpass_filter(pltData16, 0.1, 10, order=5)
        pltData = moving_average(pltData, 20)
        # naparrays =pltData

        # print(max_pixel_num[0][0])
        '''
        for i in range(P_num-1):
            if pltData[i] < Lower_limit_value:
                pltData[i]=0
            if pltData[i] > upper_limit_value:
                pltData[i]=upper_limit_value    
        '''
        max_pixel_num = np.where(pltData == pltData.max())

        # Pixel_plot[max_pixel_num[0][0]]=10
        Pixel_plot[-1] = max_pixel_num[0][0]
        # print(Pixel_plot[len(Pixel_plot)-1])

        naparrays = Pixel_plot
        print(Pixel_plot[-1])
        Pixel_plot = np.roll(Pixel_plot, -1, axis=0)
        print(Pixel_plot[-1])

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
    # print(naparrays)
    p6.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted


if __name__ == '__main__':
    mySerial = threading.Thread(name='mySerial', target=main)
    mySerial.start()
    PYQtPlot()
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QSizePolicy, QSlider, QSpacerItem, \
    QVBoxLayout, QWidget
from pyqtgraph.Qt import QtGui, QtCore
from PyQt5.QtCore import Qt

import pyqtgraph as pg
import numpy as np


class Slider(QWidget):
    def __init__(self, minimum, maximum, parent=None):
        super(Slider, self).__init__(parent=parent)
        self.verticalLayout = QVBoxLayout(self)
        self.label = QLabel(self)
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QHBoxLayout()
        spacerItem = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.slider = QSlider(self)
        self.slider.setOrientation(Qt.Vertical)
        self.horizontalLayout.addWidget(self.slider)
        spacerItem1 = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.resize(self.sizeHint())

        self.minimum = minimum
        self.maximum = maximum
        self.slider.valueChanged.connect(self.setLabelValue)
        self.x = None
        self.setLabelValue(self.slider.value())

    def setLabelValue(self, value):
        self.x = self.minimum + (float(value) / (self.slider.maximum() - self.slider.minimum())) * (
        self.maximum - self.minimum)
        self.label.setText("{0:.4g}".format(self.x))


class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent=parent)
        layoutV1 = QtGui.QVBoxLayout()

        self.horizontalLayout = QHBoxLayout(self)
        self.w1 = Slider(-10, 10)
        self.horizontalLayout.addWidget(self.w1)

        self.w2 = Slider(-1, 1)
        self.horizontalLayout.addWidget(self.w2)

        self.w3 = Slider(-10, 10)
        self.horizontalLayout.addWidget(self.w3)

        self.w4 = Slider(-10, 10)
        self.horizontalLayout.addWidget(self.w4)

        self.label_start_time = QtGui.QLabel('T num:')
        self.lineEdit_Start_time = QtGui.QLineEdit('0')
        layoutV1.addSpacing(40)
        # layoutV1.addWidget(self.checkbox_file_open)
        # layoutV1.addWidget(self.button_file_open)
        # layoutV1.addWidget(self.label_file_name)
        layoutV1.addSpacing(30)

        layoutV1.addWidget(self.label_start_time)
        layoutV1.addWidget(self.lineEdit_Start_time)
        layoutV1.addSpacing(10)


        layout = QtGui.QHBoxLayout()
        layout.addLayout(layoutV1)
        self.setLayout(layout)

        self.win = pg.GraphicsWindow(title="Basic plotting examples")
        self.horizontalLayout.addWidget(self.win)
        self.p6 = self.win.addPlot(title="My Plot")
        self.curve = self.p6.plot(pen='r')
        self.update_plot()

        self.win = pg.GraphicsWindow(title="Basic plotting examples")
        self.horizontalLayout.addWidget(self.win)

        self.p6 = self.win.addPlot(title="My Plot")
        self.curve = self.p6.plot(pen='y')
        self.update_plot2()

        self.win = pg.GraphicsWindow(title="Basic plotting examples")
        self.horizontalLayout.addWidget(self.win)
        self.p6 = self.win.addPlot(title="My Plot")
        self.curve = self.p6.plot(pen='r')
        self.update_plot()

        self.w1.slider.valueChanged.connect(self.update_plot)
        self.w2.slider.valueChanged.connect(self.update_plot)
        self.w3.slider.valueChanged.connect(self.update_plot)
        self.w4.slider.valueChanged.connect(self.update_plot)

        self.w1.slider.valueChanged.connect(self.update_plot2)
        self.w2.slider.valueChanged.connect(self.update_plot2)
        self.w3.slider.valueChanged.connect(self.update_plot2)
        self.w4.slider.valueChanged.connect(self.update_plot2)

    def update_plot(self):
        a = self.w1.x
        b = self.w2.x
        c = self.w3.x
        d = self.w4.x
        x = np.linspace(0, 10, 100)
        data = a + np.cos(x + c * np.pi / 180) * np.exp(-b * x) * d
        self.curve.setData(data)

    def update_plot2(self):
        a = self.w1.x
        b = self.w2.x
        c = self.w3.x
        d = self.w4.x
        x = np.linspace(0, 10, 100)
        data = a + np.cos(x + c * np.pi / 180) * np.exp(-b * x) * d
        self.curve.setData(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())


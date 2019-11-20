"""
PROBLEM:
1. when put main thread, speed is fast (~110 ms), with less CPU consumption
2.
"""
import os
import sys
import time
import logging

import numpy as np
import cv2
from PyQt5 import QtGui
from PyQt5.QtGui import QImage, QColor
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
# stylise pyqt5 interface
import qtmodern.styles
import qtmodern.windows

from thread_utils import FrameStore, FrameThread
from pyqt_utils import convert_qimg
from profiler import profile
from object_utils import FrameObject

class Window(QWidget):
    def __init__(self):
        super().__init__()
        # set up window
        self.title = 'Simply Reproducing the Slow Speed'
        self.top = 100
        self.left = 100
        self.width = 1280
        self.height = 1280
        self.init_window()
        self.init_qobject()
        #self.init_thread()

    def init_window(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.init_img_layout()
        self.show()
    
    def init_img_layout(self):
        vbox_layout = QVBoxLayout()
        # set up label
        WIDGET_WIDTH = 484 # 484
        WIDGET_HEIGHT = 240 # 240
        # window for RGB image
        rgb_label = QLabel(self)
        rgb_label.resize(WIDGET_WIDTH, WIDGET_HEIGHT)
        # window for segmentation result
        seg_label = QLabel(self)
        seg_label.resize(WIDGET_WIDTH, WIDGET_HEIGHT)
        # assign labels as attribute
        self.rgb_label = rgb_label
        self.seg_label = seg_label
        # stack widgets
        vbox_layout.addWidget(self.rgb_label)
        vbox_layout.addWidget(self.seg_label)
        self.setLayout(vbox_layout)

    def init_qobject(self):
        worker = FrameObject()
        worker.frame_signal.connect(lambda frame_store: self.display_pixmap(frame_store, 'rgb'))
        worker.frame_signal.connect(lambda frame_store: self.display_pixmap(frame_store, 'seg'))
        worker.run()
    
    def init_thread(self):
        self.f_thread = FrameThread()
        self.f_thread.frame_signal.connect(lambda frame_store: self.display_pixmap(frame_store, 'rgb'))
        self.f_thread.frame_signal.connect(lambda frame_store: self.display_pixmap(frame_store, 'seg'))
        self.f_thread.start()
        
    def display_pixmap(self, frame_store, img_type):
        if img_type == 'rgb':
            qimg = convert_qimg(frame_store.rgb_img)
            self.rgb_label.setPixmap(QtGui.QPixmap.fromImage(qimg))
        if img_type == 'rgb2':
            qimg = convert_qimg(frame_store.rgb_img)
            self.rgb2_label.setPixmap(QtGui.QPixmap.fromImage(qimg))
        else:
            self.seg_qimg = convert_qimg(frame_store.seg_out)
            #qimg = convert_qimg(frame_store.seg_out)
            self.seg_label.setPixmap(QtGui.QPixmap.fromImage(self.seg_qimg))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    qtmodern.styles.dark(app)
    win_modern = qtmodern.windows.ModernWindow(win)
    win_modern.show()
    sys.exit(app.exec_())


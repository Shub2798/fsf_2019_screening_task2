import sys
 
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar 
 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure
import matplotlib

class Plot_figure(Canvas):
 
    def __init__(self):
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
 
        Canvas.__init__(self, self.fig)
        print("asd")
 
        Canvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        Canvas.updateGeometry(self)
class plot_figure(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)   
        self.canvas = Plot_figure()                  
        self.navi_toolbar=NavigationToolbar(self.canvas,parent)
        self.vbl = QVBoxLayout()         
        self.vbl.addWidget(self.canvas)
        self.vbl.addWidget(self.navi_toolbar)
        self.setLayout(self.vbl)

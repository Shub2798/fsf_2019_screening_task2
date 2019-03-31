import csv, codecs
import os
import numpy as np
import matplotlib.pyplot as plt

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QTableWidget, QApplication, QMainWindow, QTableWidgetItem, QFileDialog
from iitBombayfosse import Ui_CSV_Editor
from PyQt5.QtCore import QFile
from PyQt5.QtGui import QImage, QPainter


class CSV_manager(QtWidgets.QMainWindow):
    def __init__(self, fileName):
        super(CSV_manager, self).__init__()
        self.ui = Ui_CSV_Editor()
        # print("sdfsd")
        self.ui.setupUi(self)
        self.model = QtGui.QStandardItemModel(self)
        self.filename = ""

        self.ui.tableView.setModel(self.model)
        self.ui.tableView.setStyleSheet(stylesheet(self))
        self.ui.tableView.horizontalHeader().setStretchLastSection(True)
        self.ui.tableView.setShowGrid(True)
        self.model.dataChanged.connect(self.finishedEdit)

        try:
            self.ui.actionEditData.triggered.connect(self.editData)
        except Exception as e:
            print(e)
        self.ui.actionedit_data.triggered.connect(self.loadCsv)
        self.ui.actionSave.triggered.connect(self.writeCsv)
        self.ui.actionSave_Plot.triggered.connect(self.savePlot)
        # self.ui.actionExit.triggered.connect(self.close)
        # self.ui.menuClear.triggered.connect(self.clearList)

        try:

            self.ui.actionScatterPlot.triggered.connect(self.scatterplot)
            self.ui.actionLinePlot.triggered.connect(self.linesplot)
            self.ui.actionScatterWithLinePlot.triggered.connect(self.smoothlines)
        except Exception as e:
            print(e)

        self.error_dialog = QtWidgets.QErrorMessage(self)
        self.error_dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        self.input_dialog = QtWidgets.QInputDialog(self)
        self.input_dialog.setWindowModality(QtCore.Qt.ApplicationModal)

        item = QtGui.QStandardItem()
        self.model.appendRow(item)
        self.model.setData(self.model.index(0, 0), "", 0)
        self.ui.tableView.resizeColumnsToContents()

    def loadCsv(self):
        try:
            self.ui.tabWidget.setCurrentIndex(0)
            self.check_change = False
            path = QFileDialog.getOpenFileName(self, 'Open CSV', os.getenv('HOME'), 'CSV(*.csv)')
            print(path)
            if path[0] != '':
                self.filename = str(path[0])
                print(self.filename)
                with open(path[0], newline='') as csv_file:
                    my_file = csv.reader(csv_file, dialect='excel')
                    self.model.clear()
                    for row in my_file:
                        items = [QtGui.QStandardItem(field) for field in row]
                        self.model.appendRow(items)
                    self.ui.tableView.resizeColumnsToContents()

        except Exception as e:
            print(e)

    def writeCsv(self):
        path = QFileDialog.getSaveFileName(self, 'Save CSV', os.getenv('HOME'), 'CSV(*.csv)')
        if path[0] != '':
            with open(path[0], 'w') as csv_file:
                writer = csv.writer(csv_file, dialect='excel')
                for rowNumber in range(self.model.rowCount()):
                    fields = [self.model.data(self.model.index(rowNumber, columnNumber),
                                              QtCore.Qt.DisplayRole)
                              for columnNumber in range(self.model.columnCount())]
                    writer.writerow(fields)
                self.fname = os.path.splitext(str(fileName))[0].split("/")[-1]
                self.setWindowTitle(self.fname)

    def finishedEdit(self):
        self.ui.tableView.resizeColumnsToContents()

    def scatterplot(self):
        try:

            self.ui.tabWidget.setCurrentIndex(1)
            indices = self.ui.tableView.selectionModel().selection().indexes()
            temp = []

            for i in indices:
                if i.column() not in temp:
                    temp.append(i.column())
                else:
                    continue
            if len(temp) != 0:
                with open(self.filename, 'r')as csvfile:
                    plots = csv.reader(csvfile, delimiter=',')
                    x = []
                    y = []
                    for row in plots:
                        x.append((row[temp[0]]))
                        y.append((row[temp[1]]))

                    self.ui.widget1.canvas.axes.scatter(x, y)
                    title, ok = self.input_dialog.getText(self, 'Custom Title', 'Enter plot title')
                    self.ui.widget1.canvas.axes.set_title(str(title))
                    self.ui.widget1.canvas.axes.set_xlabel(x[0])
                    self.ui.widget1.canvas.axes.set_ylabel(y[0])
                    self.ui.widget1.canvas.draw()


        except Exception as e:
            print(e)

    def linesplot(self):
        try:

            self.ui.tabWidget.setCurrentIndex(2)
            indices = self.ui.tableView.selectionModel().selection().indexes()
            temp = []

            for i in indices:
                if i.column() not in temp:
                    temp.append(i.column())
                else:
                    continue
            if len(temp) != 0:
                with open(self.filename, 'r')as csvfile:
                    plots = csv.reader(csvfile, delimiter=',')
                    x = []
                    y = []
                    for row in plots:
                        x.append((row[temp[0]]))
                        y.append((row[temp[1]]))

                    self.ui.widget_2.canvas.axes.plot(x, y)
                    title, ok = self.input_dialog.getText(self, 'Custom Title', 'Enter plot title')
                    self.ui.widget_2.canvas.axes.set_title(str(title))
                    self.ui.widget_2.canvas.axes.set_xlabel(x[0])
                    self.ui.widget_2.canvas.axes.set_ylabel(y[0])
                    self.ui.widget_2.canvas.draw()
        except Exception as e:
            print(e)

    def smoothlines(self):
        try:

            self.ui.tabWidget.setCurrentIndex(3)
            indices = self.ui.tableView.selectionModel().selection().indexes()
            temp = []

            for i in indices:
                if i.column() not in temp:
                    temp.append(i.column())
                else:
                    continue
            if len(temp) != 0:
                with open(self.filename, 'r')as csvfile:
                    plots = csv.reader(csvfile, delimiter=',')
                    x = []
                    y = []
                    for row in plots:
                        x.append((row[temp[0]]))
                        y.append((row[temp[1]]))

                    self.ui.widget_3.canvas.axes.plot(x, y,'o')
                    title, ok = self.input_dialog.getText(self, 'Custom Title', 'Enter plot title')
                    self.ui.widget_3.canvas.axes.set_title(str(title))
                    self.ui.widget_3.canvas.axes.set_xlabel(x[0])
                    self.ui.widget_3.canvas.axes.set_ylabel(y[0])
                    self.ui.widget_3.canvas.draw()
        except Exception as e:
            print(e)
        
        
    def savePlot(self,fileName_plot):
        try:
            index=self.ui.tabWidget.currentIndex()
            if index!=0:
                fileName_plot, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Plot", 
                                (QtCore.QDir.homePath() + "/" + self.filename + ".png"),"PNG Files (*.png)")
                if fileName_plot:
                    self.pname = os.path.splitext(str(fileName_plot))[0].split("/")[-1]
                    if index==1:
                        self.ui.widget1.canvas.figure.savefig(str(fileName_plot))
                    elif index==2:
                        self.ui.widget_2.canvas.figure.savefig(str(fileName_plot))
                    elif index==3:
                        self.ui.widget_3.canvas.figure.savefig(str(fileName_plot))
            else:
                self.error_dialog.showMessage('Please select a tab to save a plot')
        except Exception as e:
            print(e)
    def editData(self,state):
        try:
            if state:
                self.ui.tableView.setEnabled(True)
                #self.ui.actionClear_Data.setEnabled(True)
            else:
                self.ui.tableView.setEnabled(False)
                #self.ui.actionClear_Data.setEnabled(False)
        except Exception as e:
            print(e)
    def contextMenuEvent(self, event):
        self.menu = QtWidgets.QMenu(self)
        # copy
        copyAction = QtWidgets.QAction('Copy', self)
        copyAction.triggered.connect(lambda: self.copyByContext(event))
        # paste
        pasteAction = QtWidgets.QAction('Paste', self)
        pasteAction.triggered.connect(lambda: self.pasteByContext(event))
        # cut
        cutAction = QtWidgets.QAction('Cut', self)
        cutAction.triggered.connect(lambda: self.cutByContext(event))
        # delete selected Row
        removeAction = QtWidgets.QAction('delete Row', self)
        removeAction.triggered.connect(lambda: self.deleteRowByContext(event))
        # add Row after
        addAction = QtWidgets.QAction('insert new Row after', self)
        addAction.triggered.connect(lambda: self.addRowByContext(event))
        # add Row before
        addAction2 = QtWidgets.QAction('insert new Row before', self)
        addAction2.triggered.connect(lambda: self.addRowByContext2(event))
        # add Column before
        addColumnBeforeAction = QtWidgets.QAction('insert new Column before', self)
        addColumnBeforeAction.triggered.connect(lambda: self.addColumnBeforeByContext(event))
        # add Column after
        addColumnAfterAction = QtWidgets.QAction('insert new Column after', self)
        addColumnAfterAction.triggered.connect(lambda: self.addColumnAfterByContext(event))
        # delete Column
        deleteColumnAction = QtWidgets.QAction('delete Column', self)
        deleteColumnAction.triggered.connect(lambda: self.deleteColumnByContext(event))
        # add other required actions
        self.menu.addAction(copyAction)
        self.menu.addAction(pasteAction)
        self.menu.addAction(cutAction)
        self.menu.addSeparator()
        self.menu.addAction(addAction)
        self.menu.addAction(addAction2)
        self.menu.addSeparator()
        self.menu.addAction(addColumnBeforeAction)
        self.menu.addAction(addColumnAfterAction)
        self.menu.addSeparator()
        self.menu.addAction(removeAction)
        self.menu.addAction(deleteColumnAction)
        self.menu.popup(QtGui.QCursor.pos())
    def deleteRowByContext(self, event):
        indices= self.ui.tableView.selectionModel().selection().indexes()
    
        temp=[]
        for i in indices:
            if i.row() not in temp:
                temp.append(i.row())
            else:
                continue
        if len(temp)!=0:
            for i in temp:
                self.model.removeRow(i)
                print("Row " + str(i+1) + " deleted")
                self.ui.tableView.selectRow(i)

    def addRowByContext(self, event):
        indices= self.ui.tableView.selectionModel().selection().indexes()
    
        temp=[]
        for i in indices:
            if i.row() not in temp:
                temp.append(i.row())
            else:
                continue
        if len(temp)!=0:
            self.model.insertRow(temp[-1]+1)
            print("Row at " + str(temp[-1]+1+1) + " inserted")
            self.ui.tableView.selectRow(temp[-1]+1)

    def addRowByContext2(self, event):

        indices= self.ui.tableView.selectionModel().selection().indexes()
        temp=[]
        for i in indices:
            if i.row() not in temp:
                temp.append(i.row())
            else:
                continue
        if len(temp)!=0:
            self.model.insertRow(temp[-1])
            print("Row at " + str(temp[-1]+1) + " inserted")
            self.ui.tableView.selectRow(temp[-1])

    def addColumnBeforeByContext(self, event):
        indices= self.ui.tableView.selectionModel().selection().indexes()
        temp=[]
        for i in indices:
            if i.column() not in temp:
                temp.append(i.column())
            else:
                continue
        if len(temp)!=0:
            self.model.insertColumn(temp[-1])
            print("Column at " + str(temp[-1]+1) + " inserted")
            self.ui.tableView.selectColumn(temp[-1])

    def addColumnAfterByContext(self, event):
        indices= self.ui.tableView.selectionModel().selection().indexes()
        temp=[]
        for i in indices:
            if i.column() not in temp:
                temp.append(i.column())
            else:
                continue
        if len(temp)!=0:
            self.model.insertColumn(temp[-1]+1)
            print("Column at " + str(temp[-1]+1+1) + " inserted")
            self.ui.tableView.selectColumn(temp[-1]+1)
                
    def deleteColumnByContext(self, event):
        indices= self.ui.tableView.selectionModel().selection().indexes()
        temp=[]
        for i in indices:
            if i.column() not in temp:
                temp.append(i.column())
            else:
                continue
        if len(temp)!=0:
            for i in temp:
                self.model.removeColumn(i)
                print("Column " + str(i) + " deleted")
                self.ui.tableView.selectColumn(i)
                    
    def copyByContext(self, event):
        for i in self.ui.tableView.selectionModel().selection().indexes():
            row = i.row()
            col = i.column()
            myitem = self.model.item(row,col)
            if myitem is not None:
                clip = QtWidgets.QApplication.clipboard()
                clip.setText(myitem.text())

    def pasteByContext(self, event):
        for i in self.ui.tableView.selectionModel().selection().indexes():
            row = i.row()
            col = i.column()
            myitem = self.model.item(row,col)
            clip = QtWidgets.QApplication.clipboard()
            myitem.setText(clip.text())

    def cutByContext(self, event):
        for i in self.ui.tableView.selectionModel().selection().indexes():
            row = i.row()
            col = i.column()
            myitem = self.model.item(row,col)
            if myitem is not None:
                clip = QtWidgets.QApplication.clipboard()
                clip.setText(myitem.text())
                myitem.setText("")

    def clearList(self,state):
        try:
            self.model.clear()
        except Exception as e:
            print(e)

def stylesheet(self):
    return """
       QTableView
       {
border: 1px solid grey;
border-radius: 0px;
font-size: 12px;
        background-color: #f8f8f8;
selection-color: white;
selection-background-color: #00ED56;
       }

QTableView QTableCornerButton::section {
    background: #D6D1D1;
    border: 1px outset black;
}

QPushButton
{
font-size: 11px;
border: 1px inset grey;
height: 24px;
width: 80px;
color: black;
background-color: #e8e8e8;
background-position: bottom-left;
} 

QPushButton::hover
{
border: 2px inset goldenrod;
font-weight: bold;
color: #e8e8e8;
background-color: green;
} 
"""


import sys

try:
    app = QtWidgets.QApplication(sys.argv)
    application = CSV_manager('')
    application.setWindowTitle("CSV_Editor")
    application.show()
    sys.exit(app.exec_())
except Exception as e:
    print(e)

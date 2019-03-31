import csv, codecs 
import os

from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtWidgets import QTableWidget, QApplication, QMainWindow, QTableWidgetItem, QFileDialog
from iitBombayfosse import Ui_CSV_Editor
from PyQt5.QtCore import QFile
from PyQt5.QtGui import QImage, QPainter

class CSV_manager(QtWidgets.QMainWindow):
    def __init__(self,fileName):
        super(CSV_manager,self).__init__()
        self.ui = Ui_CSV_Editor()
        self.ui.setupUi(self)
        self.model = QtGui.QStandardItemModel(self)

        self.ui.tableView.setModel(self.model)
        self.ui.tableView.setStyleSheet(stylesheet(self))
        self.ui.tableView.horizontalHeader().setStretchLastSection(True)
        self.ui.tableView.setShowGrid(True)
        self.model.dataChanged.connect(self.finishedEdit)

        self.ui.actionedit_data.triggered.connect(self.loadCsv)
        self.ui.actionSave.triggered.connect(self.writeCsv)
        

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
            if path[0] != '':
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
    app=QtWidgets.QApplication(sys.argv)
    application = CSV_manager('')
    application.setWindowTitle("CSV_Editor")
    application.show()
    sys.exit(app.exec_())
except Exception as e:
    print(e)








import sys
from PySide2.QtWidgets import *
from PySide2 import QtGui
from PySide2 import QtCore

# Create the application window
# app = QApplication(sys.argv)

# fileName = QFileDialog.getOpenFileName(self,
#     tr("Open Image"), "/home/jana", tr("Image Files (*.png *.jpg *.bmp)"))

# label = QLabel("<font color=red size=40>Hello World!</font>")
# label.show()

class MainWindow(QWidget):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Set main window properties
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Recording GUI')
        self.button1 =  QPushButton("Select Image Folder")
        self.button2 =  QPushButton("Select Backup Folder")

        self.label1 = QLabel()
        self.label2 = QLabel()

        # sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        # sizePolicy.setHorizontalStretch(0)
        # self.button1.setSizePolicy(sizePolicy)
        # self.button1.setMinimumSize(QtCore.QSize(100, 40))
        # self.button1.setMaximumSize(QtCore.QSize(100, 40))

        self.table = QTableWidget(10,3)
        self.columnLabels = ["Make","Model","Price"]
        self.table.setHorizontalHeaderLabels(self.columnLabels)

        self.image_dir = "/Path/to/image/directoy/"
        self.backup_dir = "/Path/to/backup/directoy/"

        self.label1.setText(self.image_dir)
        self.label2.setText(self.backup_dir)

        topLayout = QGridLayout()
        topLayout.setColumnStretch(0, 0)
        topLayout.setColumnStretch(1, 1)
        topLayout.addWidget(self.button1, 0, 0)
        topLayout.addWidget(self.label1, 0, 1)
        topLayout.addWidget(self.button2, 1, 0)
        topLayout.addWidget(self.label2, 1, 1)

        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.table)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0)
        mainLayout.addLayout(bottomLayout, 1, 0)

        self.button1.clicked.connect(self.button1Click)
        self.button2.clicked.connect(self.button2Click)

        self.setLayout(mainLayout)
        self.button1.resize(100,200)

        # self.setCentralWidget(self.table)
        # self.setGeometry(50,50,700,400)
        # self.setWindowTitle("My GUI Program")

    def selectDirectory(self):
        '''Function for selecting an exisitng directoy'''
        return QFileDialog.getExistingDirectory(self)

    def button1Click(self):
        self.image_dir = self.selectDirectory()
        self.label1.setText(self.image_dir + '/')

    def button2Click(self):
        self.backup_dir = self.selectDirectory()
        self.label2.setText(self.backup_dir + '/')


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec_()

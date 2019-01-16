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

        self.button1 =  QPushButton("Select Image Folder")
        self.button2 =  QPushButton("Select Backup Folder")

        self.lineEdit1 = QLineEdit()
        self.lineEdit2 = QLineEdit()

        self.image_dir = "/Path/to/image/directoy/"
        self.backup_dir = "/Path/to/backup/directoy"

        layout = QFormLayout()
        layout.addRow(self.button1, self.lineEdit1)
        layout.addRow(self.button2, self.lineEdit2)

        self.button1.clicked.connect(self.button1Click)
        self.button2.clicked.connect(self.button2Click)

        self.setLayout(layout)

    def selectDirectory(self):
        '''Function for selecting an exisitng directoy'''
        return QFileDialog.getExistingDirectory(self)

    def button1Click(self):
        self.image_dir = self.selectDirectory()
        self.lineEdit1.setText(self.image_dir)

    def button2Click(self):
        self.backup_dir = self.selectDirectory()
        self.lineEdit2.setText(self.backup_dir)


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec_()

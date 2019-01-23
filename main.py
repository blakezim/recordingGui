import sys
from PySide2.QtWidgets import *
from PySide2 import QtGui
from PySide2 import QtCore
import rawpy
import numpy as np
import csv
from rawkit.raw import Raw
import qdarkstyle
# import monitor
import threading
from watchdog.observers import Observer
import watch
# import matplotlib.pyplot as plt
# Create the application window
# app = QApplication(sys.argv)

# fileName = QFileDialog.getOpenFileName(self,
#     tr("Open Image"), "/home/jana", tr("Image Files (*.png *.jpg *.bmp)"))

# label = QLabel("<font color=red size=40>Hello World!</font>")
# label.show()

class MainWindow(QWidget):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Set a few fonts to be used
        self.smallText = QtGui.QFont()
        self.smallText.setFamily('Helvetica')
        self.smallText.setPointSize(15)

        self.largeText = QtGui.QFont()
        self.largeText.setFamily('Helvetica')
        self.largeText.setPointSize(30)

        # Set main window properties
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Recording Window')

        # Call the functions for initialzing the layouts
        directoryLayout = self.initDirsLayout()
        tableLayout = self.initTableLayout()
        hitLayout = self.initHitLayout()

        # Add the initialized layouts to the main layout
        mainLayout = QGridLayout()
        mainLayout.addLayout(directoryLayout, 0, 0)
        mainLayout.addLayout(tableLayout, 1, 0)
        mainLayout.addLayout(hitLayout, 2, 0)

        # Set the layout
        self.setLayout(mainLayout)

    def initTableLayout(self):
        '''Initalize the table layout'''
        # Initalize the table assuming no CSV file
        self.main_table = QTableWidget(10,7)
        self.columnLabels = ["File Name","Distance","Sections",
                             "Shutter Speed", "ISO", "Aperature", "Notes"]
        self.main_table.setHorizontalHeaderLabels(self.columnLabels)

        # Initally disable the table until the directories have been chosen
        self.main_table.setDisabled(True)

        # Make the talbe have its own layouts
        # Not sure this is necessary as the table isn't that complicated
        layout = QVBoxLayout()
        layout.addWidget(self.main_table)

        return layout


    def initDirsLayout(self):

        # Add the directory buttons
        self.image_dir_button =  QPushButton("Select Image Folder")
        self.backup_dir_button =  QPushButton("Select Backup Folder")

        self.image_dir_label = QLabel()
        self.backup_dir_label = QLabel()
        self.section_dist = QLabel()
        self.main_label = QLabel()

        self.image_dir_label.setFont(self.smallText)
        self.backup_dir_label.setFont(self.smallText)
        self.section_dist.setFont(self.smallText)
        self.main_label.setFont(self.smallText)

        self.main_label.setSizePolicy(
        QSizePolicy.Preferred,
        QSizePolicy.Expanding
        )
        temp = "<font color=red>Please select the Image and Backup Directories</font>"
        self.image_dir = "/Path/to/image/directoy/"
        self.backup_dir = "/Path/to/backup/directoy/"
        self.main_message = temp

        self.image_dir_label.setText(self.image_dir)
        self.backup_dir_label.setText(self.backup_dir)
        self.main_label.setText(self.main_message)

        self.main_label.setAlignment(QtCore.Qt.AlignCenter)
        self.main_label.setFont(self.largeText)

        self.image_dir_button.clicked.connect(self.image_dir_buttonClick)
        self.backup_dir_button.clicked.connect(self.backup_dir_buttonClick)

        layout = QGridLayout()
        layout.setColumnStretch(0, 0)
        layout.setColumnStretch(1, 1)
        layout.addWidget(self.image_dir_button, 0, 0)
        layout.addWidget(self.image_dir_label, 0, 1)
        layout.addWidget(self.backup_dir_button, 1, 0)
        layout.addWidget(self.backup_dir_label, 1, 1)
        layout.addWidget(self.main_label, 2, 0, 1, 2)

        return layout

    def initHitLayout(self):

        self.hit_button = QPushButton("HIT!!!")
        self.section_dist = QLabel()
        self.total_dist = QLabel()

        self.section_dist.setFont(self.largeText)
        self.total_dist.setFont(self.largeText)

        # self.section_dist.setAlignment(QtCore.Qt.AlignCenter)
        # self.total_dist.setAlignment(QtCore.Qt.AlignCenter)

        self.hit_button.setSizePolicy(
        QSizePolicy.Preferred,
        QSizePolicy.Expanding
        )

        self.section_dist.setSizePolicy(
        QSizePolicy.Preferred,
        QSizePolicy.Expanding
        )

        self.total_dist.setSizePolicy(
        QSizePolicy.Preferred,
        QSizePolicy.Expanding
        )

        self.temp_distance = 0
        self.total_distance = 0

        self.section_dist.setText('Temp Distance : ' + str(self.temp_distance)
                                  + ' um')
        self.total_dist.setText('Total Distance : ' + str(self.total_distance)
                                  + ' um')

        self.hit_button.clicked.connect(self.hit_buttonClick)
        self.hit_button.setDisabled(True)

        layout = QGridLayout()
        layout.addWidget(self.hit_button, 0, 0, 2, 1)
        layout.addWidget(self.section_dist, 0, 1)
        layout.addWidget(self.total_dist, 1, 1)

        return layout

    def startWatcher(self):
        # Create the other thread
        self.thread = QtCore.QThread(self)

        # Create a watcher object
        self.watcher = watch.QWatcher(self.image_dir)

        # Connect the signal on the watcher with the launch window function
        self.watcher.image_signal.connect(self.imageWindowLauncher)
        self.watcher.moveToThread(self.thread)
        self.thread.started.connect(self.watcher.run)
        self.thread.start()


    def selectDirectory(self):
        '''Function for selecting an exisitng directoy'''
        return QFileDialog.getExistingDirectory(self)

    def image_dir_buttonClick(self):
        self.image_dir = self.selectDirectory()
        self.image_dir_label.setText(self.image_dir + '/')

        self.image_dir_button.setDisabled(True)
        # self.handler = monitor.MyHandler()
        # watcher.schedule(self.handler, self.image_dir + '/')

        # thread = QtCore.QThread()

        # watcher.moveToThread()

        self.startWatcher()

        # w.started.connect(watcher.run())
        # # print(self.handler.fileList)
        # w.start()

        if not self.backup_dir_button.isEnabled():
            self.main_table.setDisabled(False)
            self.hit_button.setDisabled(False)
            temp = "<font color=green>Everything Nominal</font>"
            self.main_label.setText(temp)

    def backup_dir_buttonClick(self):
        self.backup_dir = self.selectDirectory()
        self.backup_dir_label.setText(self.backup_dir + '/')

        self.backup_dir_button.setDisabled(True)

        if not self.image_dir_button.isEnabled():
            self.main_table.setDisabled(False)
            self.hit_button.setDisabled(False)
            temp = "<font color=green>Everything Nominal</font>"
            self.main_label.setText(temp)

    def hit_buttonClick(self):

        self.temp_distance = self.temp_distance + 10
        self.section_dist.setText('Temp Distance : ' + str(self.temp_distance)
                                  + ' um')

        if self.temp_distance == 50:
            temp = "<font color=red size=40>TAKE AN IMAGE</font>"
            self.main_label.setText(temp)
            # maybe put a wait in here?
            self.temp_distance = 0

        self.section_dist.setText('Temp Distance : ' + str(self.temp_distance)
                                  + ' um')
        # self.test = ImageWindow(self.image_dir, self.backup_dir)
        # self.test.show()
        # self.populateTable()

    def populateTable(self):
        file = '/Users/blakez/Documents/TestingGUI/testingMaterials/exampleCSV.csv'
        with open(file, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            self.table_list = []
            for row in reader:
                self.table_list.append(row)

        print(np.shape(self.table_list))
        shape = np.shape(self.table_list)
        self.main_table.setRowCount(shape[0])
        self.main_table.setColumnCount(shape[1])

        for i, row in enumerate(self.table_list):
            for j, col in enumerate(row):
                item = QTableWidgetItem(col)
                self.main_table.setItem(i, j, item)

    def imageWindowLauncher(self, image_path):
        self.image_window = ImageWindow(self.image_dir, self.backup_dir, image_path)
        self.image_window.show()


class ImageWindow(QWidget):

    def __init__(self, image_dir, backup_dir, image_path, parent=None):
        super(ImageWindow, self).__init__(parent)

        # Set main window properties
        self.setGeometry(300, 300, 800, 300)
        self.setWindowTitle('Image Window')

        self.image_dir = image_dir
        self.backup_dir = backup_dir
        self.image_path = image_path

        leftLayout = self.initLeftLayout()
        rightLayout = self.initRightLayout()

        # self.image_label = QLabel()



        mainLayout = QGridLayout()
        mainLayout.addLayout(leftLayout, 0, 0)
        mainLayout.addLayout(rightLayout, 0, 1)
        # mainLayout.addWidget(self.load_image_button, 0, 0)
        # mainLayout.addWidget(self.retake_button, 1, 0)
        # mainLayout.addWidget(self.image_label, 0, 1, 2, 1)

        self.setLayout(mainLayout)

    def initLeftLayout(self):
        self.retake_button = QPushButton('Retake Image')
        self.load_image_button = QPushButton('IMAGE!')
        self.section_a = QCheckBox('Section a')
        self.section_b = QCheckBox('Section b')
        self.section_c = QCheckBox('Section c')

        self.load_image_button.clicked.connect(self.selectNewImage)

        layout = QVBoxLayout()
        layout.addWidget(self.retake_button)
        layout.addWidget(self.load_image_button)
        layout.addWidget(self.section_a)
        layout.addWidget(self.section_b)
        layout.addWidget(self.section_c)

        return layout


    def initRightLayout(self):
        self.image_label = QLabel()
        self.image_label.setText("NO IMAGE!!")

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)

        return layout

    def selectDirectory(self):
        '''Function for selecting an exisitng directoy'''
        return QFileDialog.getOpenFileName(self, 'Open File',
                '/Users/blakez/Documents/TestingGUI/testingMaterials/',
                "Image Files (*.CR2)")

    def selectNewImage(self):
        self.newImage = self.selectDirectory()
        self.loadImage(self.newImage[0])
        # print()


    def loadImage(self, pth):
        # pth = '/Users/blakez/Documents/TestingGUI/testingMaterials/IMG_0001.cr2'
        # im = Raw(pth)
        # rgb = np.array(im.to_buffer())
        img = rawpy.imread(pth)
        test = img.postprocess()

        a = QtGui.QImage(test.copy(), test.shape[1], test.shape[0],
                        test.strides[0], QtGui.QImage.Format_RGB888)
        map = QtGui.QPixmap(a)
        new = map.scaled(400, 400, QtCore.Qt.KeepAspectRatio)
        self.image_label.setPixmap(new)

        # Metat data is a namedtuple container
        with Raw(filename=pth) as raw:
            print(raw.metadata.iso)



    # raw_image = Raw(filename)
    # buffered_image = np.array(raw_image.to_buffer())
     # qimage = QImage(im_np, im_np.shape[1], im_np.shape[0],
     #                 QImage.Format_RGB888)
     # pixmap = QPixmap(qimage)
watcher = Observer()
app = QApplication()
app.setStyleSheet(qdarkstyle.load_stylesheet_pyside())
window = MainWindow()

window.show()
app.exec_()
watcher.stop()

import sys
from PySide2.QtWidgets import *
from PySide2 import QtGui
from PySide2 import QtCore
import rawpy
import numpy as np
import csv
import glob
from rawkit.raw import Raw
import qdarkstyle
# import monitor
import threading
# from watchdog.observers import Observer
import watch
import os
import time
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
        self.small_text = QtGui.QFont()
        self.small_text.setFamily('Helvetica')
        self.small_text.setPointSize(15)

        self.large_text = QtGui.QFont()
        self.large_text.setFamily('Helvetica')
        self.large_text.setPointSize(30)

        # Set main window properties
        self.setGeometry(300, 300, 1000, 800)
        self.setWindowTitle('Recording Window')

        # Call the functions for initialzing the layouts
        directoryLayout = self._initDirsLayout()
        tableLayout = self._initTableLayout()
        hitLayout = self._initHitLayout()

        # Add the initialized layouts to the main layout
        mainLayout = QGridLayout()
        mainLayout.addLayout(directoryLayout, 0, 0)
        mainLayout.addLayout(tableLayout, 1, 0)
        mainLayout.addLayout(hitLayout, 2, 0)

        # Set the layout
        self.setLayout(mainLayout)

    def selectDirectory(self):
        '''Function for selecting an exisitng directoy'''
        return QFileDialog.getExistingDirectory(self)

    def image_dir_buttonClick(self):

        # Have the user select the directory for the images
        self.image_dir = self.selectDirectory()
        # Update the label with the directory they chose
        self.image_dir_label.setText(self.image_dir + '/')
        # Disable the button after the directory has been chosen
        self.image_dir_button.setDisabled(True)
        # Start monitoring the directoy
        self._startWatcher()
        # Populate the table
        self.populateTable()

        # Do I need to have a file list on this object?
        if not self.backup_dir_button.isEnabled():
            self.main_table.setDisabled(False)
            self.hit_button.setDisabled(False)
            self.iso_button.setDisabled(False)
            self.fstop_button.setDisabled(False)
            self.ss_button.setDisabled(False)
            msg = "<font color=green>Everything Nominal</font>"
            self.main_label.setText(msg)


    def backup_dir_buttonClick(self):

        # Have the user select the directory
        self.backup_dir = self.selectDirectory()
        # Update the labe with the directory they chose
        self.backup_dir_label.setText(self.backup_dir + '/')
        # Disable the button so they can't change the directory
        self.backup_dir_button.setDisabled(True)
        # Need to check that the backup directory is the same as the image directory
        self.backup()

        # Only if both directories have been selected do we enable the rest of the GUI
        if not self.image_dir_button.isEnabled():
            self.main_table.setDisabled(False)
            self.hit_button.setDisabled(False)
            self.iso_button.setDisabled(False)
            self.fstop_button.setDisabled(False)
            self.ss_button.setDisabled(False)
            temp = "<font color=green>Everything Nominal</font>"
            self.main_label.setText(temp)

    def backup(self):
        '''Function for backing up the image directory'''
        print('Backup not implemented yet')
        # Create a list of the image files and the csv files and remove duplicates
        # Copy what ever is left

        pass

    def hit_buttonClick(self):

        self.temp_distance = self.temp_distance + 10
        self.image_dist.setText('Image Distance : ' + str(self.temp_distance) + ' um')

        if self.temp_distance == 50:
            temp = "<font color=red size=40>TAKE AN IMAGE</font>"
            self.main_label.setText(temp)
            # maybe put a wait in here?
            self.setEnabled(False)
            # self.temp_distance = 0

        self.image_dist.setText('Image Distance : ' + str(self.temp_distance) + ' um')
        # self.test = ImageWindow(self.image_dir, self.backup_dir)
        # self.test.show()
        # self.populateTable()

    def populateTable(self):

        # Check for CSV files
        self.csv_list = glob.glob(self.image_dir + '/csv_files/*')

        # If the directory is empty then make a folder
        if self.csv_list == []:
            try:
                os.makedirs(self.image_dir + '/csv_files/')
            except FileExistsError:
                pass
            # Take away all of the rows
            self.main_table.setRowCount(0)
            self.main_table.setColumnCount(7)

        else:
            # Open the last saved csv file
            with open(self.csv_list[-1], 'r') as f:
                reader = csv.reader(f, delimiter=',')
                self.table_list = []
                for row in reader:
                    self.table_list.append(row)

            # Get the shape of the table and set the table to reflect that
            shape = np.shape(self.table_list)
            self.main_table.setRowCount(shape[0])
            self.main_table.setColumnCount(shape[1])

            # Iterate through the items in the list and set the appropriate table items
            for i, row in enumerate(self.table_list):
                for j, col in enumerate(row):
                    item = QTableWidgetItem(col)
                    self.main_table.setItem(i, j, item)

    def imageWindowLauncher(self, image_path):
        self.setEnabled(False)
        self.image_window = ImageWindow(self.image_dir, self.backup_dir, image_path)
        self.image_window.show()
        app.processEvents()
        self.image_window.loadImage()

    def changeSS(self):
        self.ss_drop.setDisabled(False)

    def changedSS(self):
        self.ss_drop.setDisabled(True)

    def changeISO(self):
        self.iso_drop.setDisabled(False)

    def changedISO(self):
        self.iso_drop.setDisabled(True)

    def changeFStop(self):
        self.fstop_drop.setDisabled(False)

    def changedFStop(self):
        self.fstop_drop.setDisabled(True)

    def _startWatcher(self):
        # Create the other thread
        self.thread = QtCore.QThread(self)
        # Create a watcher object
        self.watcher = watch.QWatcher(self.image_dir)
        # Connect the signal on the watcher with the launch window function
        self.watcher.image_signal.connect(self.imageWindowLauncher)
        # Move the watcher object to the other thread that was created
        self.watcher.moveToThread(self.thread)
        # Connect the thread.start with the run function on the watcher object
        self.thread.started.connect(self.watcher.run)
        # Start the thread
        self.thread.start()

    def _initTableLayout(self):
        '''Initalize the table layout'''
        # Initalize the table assuming no CSV file
        self.main_table = QTableWidget(10,7)
        self.columnLabels = ["File Name","Distance","Sections",
                             "Shutter Speed", "ISO", "Aperature", "Notes"]
        self.main_table.setHorizontalHeaderLabels(self.columnLabels)

        # Set buttons for the camera settings
        self.iso_button = QPushButton("ISO")
        self.fstop_button = QPushButton("FStop")
        self.ss_button = QPushButton("SS")

        # Connect the buttons
        self.iso_button.clicked.connect(self.changeISO)
        self.fstop_button.clicked.connect(self.changeFStop)
        self.ss_button.clicked.connect(self.changeSS)

        # Set the line edits for the settings
        # ss_values = ['']
        # self.comboBox.addItems([str(x) for x in range(3)])
        self.ss_drop = QComboBox()
        self.ss_drop.addItem('2')
        self.ss_drop.addItem('4')
        self.ss_drop.addItem('8')
        self.ss_drop.addItem('15')
        self.ss_drop.addItem('30')
        self.ss_drop.addItem('60')
        self.ss_drop.addItem('125')
        self.ss_drop.addItem('250')
        self.ss_drop.addItem('500')
        self.ss_drop.setCurrentIndex(5)
        self.ss_drop.currentIndexChanged.connect(self.changedSS)

        self.fstop_drop = QComboBox()
        self.fstop_drop.addItem('1.4')
        self.fstop_drop.addItem('2')
        self.fstop_drop.addItem('2.8')
        self.fstop_drop.addItem('4')
        self.fstop_drop.addItem('5.6')
        self.fstop_drop.addItem('8')
        self.fstop_drop.setCurrentIndex(2)
        self.fstop_drop.currentIndexChanged.connect(self.changedFStop)

        self.iso_drop = QComboBox()
        self.iso_drop.addItem('100')
        self.iso_drop.addItem('200')
        self.iso_drop.addItem('400')
        self.iso_drop.addItem('800')
        self.iso_drop.addItem('1600')
        self.iso_drop.setCurrentIndex(1)
        self.iso_drop.currentIndexChanged.connect(self.changedISO)

        # Set the font for the buttons
        self.iso_button.setFont(self.small_text)
        self.fstop_button.setFont(self.small_text)
        self.ss_button.setFont(self.small_text)

        # Initally disable the table until the directories have been chosen
        self.main_table.setDisabled(True)
        self.iso_button.setDisabled(True)
        self.fstop_button.setDisabled(True)
        self.ss_button.setDisabled(True)

        # make the table expand over the button
        self.main_table.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding)

        self.iso_drop.setDisabled(True)
        self.fstop_drop.setDisabled(True)
        self.ss_drop.setDisabled(True)

        settings_layout = QGridLayout()
        settings_layout.addWidget(self.iso_button, 0, 0)
        settings_layout.addWidget(self.fstop_button, 1, 0)
        settings_layout.addWidget(self.ss_button, 2, 0)
        settings_layout.addWidget(self.iso_drop, 0, 1)
        settings_layout.addWidget(self.fstop_drop, 1, 1)
        settings_layout.addWidget(self.ss_drop, 2, 1)
        settings_layout.setColumnStretch(0, 10)
        settings_layout.setColumnStretch(1, 20)

        # settings_layout.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        # Make the talbe have its own layout
        # Not sure this is necessary as the table isn't that complicated
        layout = QGridLayout()
        layout.addWidget(self.main_table, 0, 0)
        layout.addLayout(settings_layout, 0, 1)
        layout.setColumnStretch(0, 40)
        layout.setColumnStretch(1, 10)

        return layout

    def _initDirsLayout(self):

        # Add the directory buttons
        self.image_dir_button =  QPushButton("Select Image Folder")
        self.backup_dir_button =  QPushButton("Select Backup Folder")

        # Add the directory labels
        self.image_dir_label = QLabel()
        self.backup_dir_label = QLabel()
        self.image_dist = QLabel()
        self.main_label = QLabel()

        # Change the font of all the lables and buttons
        self.image_dir_label.setFont(self.small_text)
        self.backup_dir_label.setFont(self.small_text)
        self.image_dist.setFont(self.small_text)
        self.main_label.setFont(self.small_text)
        self.image_dir_button.setFont(self.small_text)
        self.backup_dir_button.setFont(self.small_text)

        # Set the size policy for the label so it expands vertically
        self.main_label.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding)

        # Initalize the messages for the main label and the directories
        msg = "<font color=red>Please select the Image and Backup Directories</font>"
        self.image_dir = "/Path/to/image/directoy/"
        self.backup_dir = "/Path/to/backup/directoy/"
        self.main_message = msg

        # Set the labels with the inital messages
        self.image_dir_label.setText(self.image_dir)
        self.backup_dir_label.setText(self.backup_dir)
        self.main_label.setText(self.main_message)

        # Set the alignment of the main text
        self.main_label.setAlignment(QtCore.Qt.AlignCenter)
        self.main_label.setFont(self.large_text)

        # Connect the buttons to their functions
        self.image_dir_button.clicked.connect(self.image_dir_buttonClick)
        self.backup_dir_button.clicked.connect(self.backup_dir_buttonClick)

        # Define the layout for the main window
        layout = QGridLayout()
        layout.setColumnStretch(0, 0)
        layout.setColumnStretch(1, 1)
        layout.addWidget(self.image_dir_button, 0, 0)
        layout.addWidget(self.image_dir_label, 0, 1)
        layout.addWidget(self.backup_dir_button, 1, 0)
        layout.addWidget(self.backup_dir_label, 1, 1)
        layout.addWidget(self.main_label, 2, 0, 1, 2)

        return layout

    def _initHitLayout(self):

        # Make the hit button and the lables for the section distances
        self.hit_button = QPushButton("HIT!!!")
        self.image_dist = QLabel()
        self.total_dist = QLabel()

        # Set the font for the labels and button
        self.image_dist.setFont(self.large_text)
        self.total_dist.setFont(self.large_text)
        self.hit_button.setFont(self.large_text)

        # Set the size policies for the buttons and labels
        self.hit_button.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding)
        self.image_dist.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding)
        self.total_dist.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding)

        # Initalize the distances
        self.temp_distance = 0
        self.total_distance = 0

        # Make the labels for the distances
        # Keep the number separate from the text so they can easily be used elsewhere
        self.image_dist.setText('Image Distance : ' + str(self.temp_distance) + ' um')
        self.total_dist.setText('Total Distance : ' + str(self.total_distance) + ' um')

        # Connect the hit button
        self.hit_button.clicked.connect(self.hit_buttonClick)

        # Disable the hit button initally
        self.hit_button.setDisabled(True)

        # Create the layout
        layout = QGridLayout()
        layout.addWidget(self.hit_button, 0, 0, 2, 1)
        layout.addWidget(self.image_dist, 0, 1)
        layout.addWidget(self.total_dist, 1, 1)
        layout.setColumnStretch(0, 20)
        layout.setColumnStretch(1, 15)

        return layout

    def errorMessage(self, error):
       msg = QMessageBox()
       msg.setIcon(QMessageBox.Critical)
       msg.setText(error)
       # msg.setInformativeText("This is additional information")
       msg.setWindowTitle("ERROR")
       # msg.setDetailedText("The details are as follows:")
       msg.setStandardButtons(QMessageBox.Ok)
       # msg.buttonClicked.connect(msgbtn)

       msg.exec_()
       # print "value of pressed message box button:", retval

'End Class'
# class ErrorWindow(QWidget):
#
#     def __init__(self, msg, parent=None):
#         super(ErrorWindow, self).__init__(parent)
#
#         # self.setGeometry(100, 200, 200, 500)
#         self.setWindowTitle('ERROR')
#
#         self.font = QtGui.QFont()
#         self.font.setFamily('Helvetica')
#         self.font.setPointSize(25)
#
#         self.close_button = QPushButton('Ok')
#         self.message = QLabel()
#         self.message.setText(msg)
#         self.message.setFont(self.font)
#
#         self.close_button.clicked.connect(self.closeButton)
#         self.layout = QVBoxLayout()
#         self.layout.addWidget(self.message)
#         self.layout.addWidget(self.close_button)
#
#         self.setLayout(self.layout)
#
#     def closeButton(self):
#         self.destroy()

class ImageWindow(QWidget):

    def __init__(self, image_dir, backup_dir, image_path, parent=None):
        super(ImageWindow, self).__init__(parent)

        # Set main window properties
        self.setGeometry(300, 300, 800, 300)
        self.setWindowTitle('Image Window')

        self.image_dir = image_dir
        self.backup_dir = backup_dir
        self.image_path = image_path

        self.setLayout(self.initLayout())

    def initLayout(self):
        self.retake_button = QPushButton('Retake Image')
        self.accept_button = QPushButton('Accept Image')
        self.section_a = QCheckBox('Section a')
        self.section_b = QCheckBox('Section b')
        self.section_c = QCheckBox('Section c')
        self.iso_loaded = QLabel("ISO: ")
        self.fstop_loaded = QLabel("FStop: ")
        self.ss_loaded = QLabel("SS: ")
        self.image_label = QLabel("Loading...")
        self.notes_label = QLineEdit("No notes")

        self.retake_button.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.accept_button.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.section_a.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.section_b.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.section_c.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.iso_loaded.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.fstop_loaded.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.ss_loaded.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.notes_label.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding)
        # self.load_image_button.clicked.connect(self.selectNewImage)

        # Connect the button
        self.accept_button.clicked.connect(self.acceptClicked)
        self.retake_button.clicked.connect(self.retakeClicked)


        self.image_label.setAlignment(QtCore.Qt.AlignCenter)

        gridLayout = QGridLayout()
        gridLayout.addWidget(self.retake_button, 0, 0, 1, 3)
        gridLayout.addWidget(self.section_a, 1, 0)
        gridLayout.addWidget(self.section_b, 1, 1)
        gridLayout.addWidget(self.section_c, 1, 2)
        gridLayout.addWidget(self.iso_loaded, 2, 0)
        gridLayout.addWidget(self.fstop_loaded, 2, 1)
        gridLayout.addWidget(self.ss_loaded, 2, 2)
        gridLayout.addWidget(self.accept_button, 3, 0, 1, 3)
        gridLayout.addWidget(self.notes_label, 4, 0, 1, 3)

        layout = QGridLayout()
        layout.addLayout(gridLayout, 0, 0)
        layout.addWidget(self.image_label, 0, 1)
        # layout.setColumnStretch(0, 10)
        # layout.setColumnStretch(1, 15)
        # self.image_label.setText(self.image_path)

        return layout


    # def initNotesLayout(self):
    #     self.notes_label = QLabel()
    #     self.notes_label.setText('No notes')
    #
    #     layout = QHBoxLayout()
    #     layout.addWidget(self.notes_label)
    #
    #     self.notes_label.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding)
    #
    #     return layout

    def selectDirectory(self):
        '''Function for selecting an exisitng directoy'''
        return QFileDialog.getOpenFileName(self, 'Open File',
                '/Users/blakez/Documents/TestingGUI/testingMaterials/',
                "Image Files (*.CR2)")

    def selectNewImage(self):
        self.newImage = self.selectDirectory()
        self.loadImage(self.newImage[0])
        # print()


    def loadImage(self):
        time.sleep(0.1)
        # pth = '/Users/blakez/Documents/TestingGUI/testingMaterials/IMG_0001.cr2'
        # im = Raw(pth)
        # rgb = np.array(im.to_buffer())
        img = rawpy.imread(self.image_path)
        test = img.postprocess()

        a = QtGui.QImage(test.copy(), test.shape[1], test.shape[0],
                        test.strides[0], QtGui.QImage.Format_RGB888)
        map = QtGui.QPixmap(a)
        new = map.scaled(400, 400, QtCore.Qt.KeepAspectRatio)
        self.image_label.setPixmap(new)

        # Metat data is a namedtuple container
        with Raw(filename=self.image_path) as raw:
            print(raw.metadata.iso)

    def acceptClicked(self):
        pass

    def retakeClicked(self):
        pass

if __name__ == '__main__':

    app = QApplication()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside())
    window = MainWindow()

    window.show()
    app.exec_()
    window.watcher.stop()
    window.thread.quit()
    window.thread.wait()

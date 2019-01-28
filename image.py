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

class ImageWindow(QWidget):

    def __init__(self, image_dir, backup_dir, image_path, main, parent=None):
        super(ImageWindow, self).__init__(parent)

        # Set main window properties
        self.setGeometry(300, 300, 800, 300)
        self.setWindowTitle('Image Window')

        self.image_dir = image_dir
        self.backup_dir = backup_dir
        self.image_path = image_path
        self.main_window = main

        self.setLayout(self.initLayout())

    def initLayout(self):
        self.retake_button = QPushButton('Retake Image')
        self.accept_button = QPushButton('Accept Image')
        self.section_a = QCheckBox('Section a')
        self.section_b = QCheckBox('Section b')
        self.section_c = QCheckBox('Section c')
        self.iso_label = QLabel("ISO: ")
        self.fstop_label = QLabel("FStop: ")
        self.ss_label = QLabel("SS: ")
        self.image_label = QLabel("Loading...")
        self.notes_edit = QLineEdit("No notes")

        self.retake_button.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.accept_button.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.section_a.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.section_b.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.section_c.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.iso_label.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.fstop_label.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.ss_label.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.notes_edit.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding)
        # self.load_image_button.clicked.connect(self.selectNewImage)

        # Connect the button
        self.accept_button.clicked.connect(self.acceptClicked)
        self.retake_button.clicked.connect(self.retakeClicked)

        # Initially disable the accept button until image has been validated
        self.accept_button.setDisabled(True)

        self.image_label.setAlignment(QtCore.Qt.AlignCenter)

        gridLayout = QGridLayout()
        gridLayout.addWidget(self.retake_button, 0, 0, 1, 3)
        gridLayout.addWidget(self.section_a, 1, 0)
        gridLayout.addWidget(self.section_b, 1, 1)
        gridLayout.addWidget(self.section_c, 1, 2)
        gridLayout.addWidget(self.iso_label, 2, 0)
        gridLayout.addWidget(self.fstop_label, 2, 1)
        gridLayout.addWidget(self.ss_label, 2, 2)
        gridLayout.addWidget(self.accept_button, 3, 0, 1, 3)
        gridLayout.addWidget(self.notes_edit, 4, 0, 1, 3)

        layout = QGridLayout()
        layout.addLayout(gridLayout, 0, 0)
        layout.addWidget(self.image_label, 0, 1)
        # layout.setColumnStretch(0, 10)
        # layout.setColumnStretch(1, 15)
        # self.image_label.setText(self.image_path)

        return layout


    def loadImage(self):

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
            print(raw.metadata)
            self.iso_loaded = raw.metadata.iso
            self.ss_loaded = raw.metadata.shutter
            self.fstop_loaded = raw.metadata.aperture
        # Convert the shutter speed to a number
        self.ss_loaded = int(np.ceil(1 / self.ss_loaded))
        # Validate the image settings are correct
        self.validateImage()


        self.iso_label.setText("ISO:   " + str(self.iso_loaded))
        self.fstop_label.setText("FStop:   " + str(self.fstop_loaded))
        self.ss_label.setText("SS:   " + str(self.ss_loaded))

    def validateImage(self):

        # Check the iso values
        iso = self.main_window.iso_drop.currentText() == str(int(self.iso_loaded))
        # Check the shutter speed
        ss = self.main_window.ss_drop.currentText() == str(self.ss_loaded)
        # Check the fstop
        fstop = self.main_window.fstop_drop.currentText() == str(self.fstop_loaded)

        # If the image is valid, let them accept
        if fstop and ss and iso:
            self.accept_button.setDisabled(False)

        else:
            msg = 'Image parameters are not correct!\n'
            msg += 'ISO:  ' + str(int(self.iso_loaded))
            msg += '  should be  ' + self.main_window.iso_drop.currentText() + '\n'
            msg += 'FStop:  ' + str(self.fstop_loaded)
            msg += '  should be  ' + self.main_window.fstop_drop.currentText() + '\n'
            msg += 'SS:  ' + str(self.ss_loaded)
            msg += '  should be  ' + self.main_window.ss_drop.currentText() + '\n'
            msg += 'Please retake the image!'
            self.errorMessage(msg)

    def _rowConstructor(self):
        # Need to populate the table with the new information
        # Do I need to have a list of each table column for when I write out?
        # Need to construct a string for the sections that were taken
        # Need to make this whole thing into a function for Retake button
        # Need to have a tracker for what sections have been clicked
        self.section_list = ''
        section_count_string = str(self.main_window.section_count)
        if self.section_a.isChecked():
            self.section_list += section_count_string + 'a'
        if self.section_b.isChecked():
            self.section_list += '; ' + section_count_string + 'b'
        if self.section_c.isChecked():
            self.section_list += '; ' + section_count_string + 'c'
            # At this point, all of the section have been taken
            # Need to update the count
            self.main_window.section_count += 1
        if self.section_list == '':
            self.section_list = 'None'

        # Construct the new row to the table as a list of strings
        # get rid of the .CR2
        self.main_window.table_list.append([
        self.image_path.split('/')[-1].split('.')[0],
        str(self.main_window.total_distance),
        self.section_list,
        str(self.ss_loaded),
        str(self.iso_loaded),
        str(self.fstop_loaded),
        self.notes_edit.text()
        ])

    def acceptClicked(self):
        # Need to reset the image_distance
        self.main_window.image_distance = 0
        self.main_window.image_dist_label.setText('Image Distance: ' + str(0) + ' um')
        # Reset the main labels
        msg = "<font color=green>Everything Nominal</font>"
        self.main_window.main_label.setText(msg)

        # Update the main window list with the new row
        self._rowConstructor()

        # Add a new row to the table
        rowPosition = self.main_window.main_table.rowCount()
        self.main_window.main_table.insertRow(rowPosition)

        # Populate the new row
        for i, col in enumerate(self.main_window.table_list[-1]):
            item = QTableWidgetItem(col)
            self.main_window.main_table.setItem(rowPosition, i, item)

        # Need to re-enable the main window
        self.main_window.setDisabled(False)
        self.close()
        self.destroy()

        # Need to add something to keep section boxes checked

        pass

    def retakeClicked(self):
        pass

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

import csv
import glob
import rawpy
import numpy as np

from PySide2.QtWidgets import *
from PySide2 import QtGui
from PySide2 import QtCore
from rawkit.raw import Raw

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

        # Check to see if the the sections have been taken yet
        if self.main_window.section_a:
            self.section_a.setChecked(True)
            self.section_a.setDisabled(True)

        if self.main_window.section_b:
            self.section_b.setChecked(True)
            self.section_b.setDisabled(True)

        if self.main_window.section_c:
            self.section_c.setChecked(True)
            self.section_c.setDisabled(True)

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

    def _rowConstructor(self, note=None):

        self.section_list = ''
        section_count_string = str(self.main_window.section_count)
        if self.section_a.isChecked() and self.section_a.isEnabled():
            self.section_list += section_count_string + 'a;'
            self.main_window.section_a = True
        if self.section_b.isChecked() and self.section_b.isEnabled():
            self.section_list += section_count_string + 'b;'
            self.main_window.section_b = True
        if self.section_c.isChecked() and self.section_c.isEnabled():
            self.section_list += section_count_string + 'c;'
            self.main_window.section_c = True

        if self.section_list == '':
            self.section_list = 'None'

        # Construct the new row to the table as a list of strings
        # get rid of the .CR2
        if note is not None:
            notes = self.notes_edit.text() + ' - ' + note
        else:
            notes = self.notes_edit.text()

        self.main_window.table_list.append([
        self.image_path.split('/')[-1].split('.')[0],
        str(self.main_window.total_distance),
        self.section_list,
        str(self.ss_loaded),
        str(self.iso_loaded),
        str(self.fstop_loaded),
        notes
        ])

        # Add a new row to the table
        rowPosition = self.main_window.main_table.rowCount()
        self.main_window.main_table.insertRow(rowPosition)

        # Populate the new row
        for i, col in enumerate(self.main_window.table_list[-1]):
            item = QTableWidgetItem(col)
            self.main_window.main_table.setItem(rowPosition, i, item)

    def acceptClicked(self):
        # Need to reset the image_distance
        self.main_window.image_distance = 0
        self.main_window.image_dist_label.setText('Image Distance: ' + str(0) + ' um')
        # Reset the hit_button text to what it was before
        msg = "HIT!!!"
        self.main_window.hit_button.setText(msg)
        self.main_window.hit_button.setStyleSheet("color: white")

        # msg = self.main_window.main_label.text()
        # self.main_window.main_label.setText(msg)

        # Update the main window list with the new row
        self._rowConstructor()

        # Need to re-enable the main window
        self.main_window.setDisabled(False)
        # Make sure all the buttons have been restored to enable
        self.main_window.hit_button.setDisabled(False)
        self.main_window.main_table.setDisabled(False)

        # Need to check if all sections have been taken
        if self.main_window.section_a and self.main_window.section_b and self.main_window.section_c:
            # Update the group section counter
            # This is going to incrament every time
            # Only update if 'should be taking sections'
            # temp = "<font color=red size=40>You should be taking sections</font>"
            # if self.main_window.main_label.text() == temp:
            #     self.main_window.section_count += 1
            if self.main_window.taking_sections:
                self.main_window.section_count += 1
                self.main_window.taking_sections = False
            # Update the main message
            msg = "<font color=green>Everything Nominal</font>"
            self.main_window.main_label.setText(msg)
            # Set the section trackers back to False
            self.section_a = False
            self.section_b = False
            self.section_c = False
        else:
            msg = "<font color=red size=20>You should be taking sections</font>"
            self.main_window.main_label.setText(msg)
        # if self.main_window.total_distance == 0:
        #     msg = "<font color=green>Everything Nominal</font>"
        #     self.main_window.main_label.setText(msg)

        self.main_window.retake = False
        self.main_window.save()
        self.close()
        self.destroy()


    def retakeClicked(self):
        msg = "<font color=red size=40>RE-TAKE THE IMAGE</font>"
        self.main_window.main_label.setText(msg)

        # Do I need to allow the user to change the image parameteres here?
        self.main_window.setDisabled(False)
        self.main_window.hit_button.setDisabled(True)
        self.main_window.main_table.setDisabled(True)

        self._rowConstructor(note='Bad Settings')

        # Save the row
        self.main_window.retake = True
        self.main_window.save()
        self.close()
        self.destroy()

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

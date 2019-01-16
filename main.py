import sys
from PySide2.QtWidgets import *
from PySide2 import QtGui
from PySide2 import QtCore

# Create the application window
app = QApplication(sys.argv)

# fileName = QFileDialog.getOpenFileName(self,
#     tr("Open Image"), "/home/jana", tr("Image Files (*.png *.jpg *.bmp)"))

# dialog = QFileDialog()
# dialog.setFileMode(QFileDialog.AnyFile)
# dialog.show()

window =  QWidget()
button1 =  QPushButton("Select")
button2 =  QPushButton("Select")

# layout =  QVBoxLayout()
# layout.addWidget(button1)
# layout.addWidget(button2)
# layout.addWidget(button3)
# layout.addWidget(button4)
# layout.addWidget(button5)
#
# layout =  QGridLayout()
# layout.addWidget(button1, 0, 0)
# layout.addWidget(button2, 0, 1)
# layout.addWidget(button3, 1, 0, 1, 2)
# layout.addWidget(button4, 2, 0)
# layout.addWidget(button5, 2, 1)

lineEdit1 = QLineEdit()
lineEdit2 = QLineEdit()
lineEdit3 = QLineEdit()


layout = QFormLayout()
layout.addRow(button1, lineEdit1)
layout.addRow(button2, lineEdit2)
layout.addRow(button3, lineEdit3)

window.setLayout(layout)
window.show()


# Add text and change the style
# label = QLabel("Hello World!")
# label = QLabel("<font color=red size=40>Hello World!</font>")
# label.show()


app.exec_()

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Tachy2GIS_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from qgis.gui import QgsMapLayerComboBox

class Tachy2GisDialog(QtWidgets.QDialog):
    def setupUi(self, Tachy2GisDialog):
        Tachy2GisDialog.setObjectName("Tachy2GisDialog")
        Tachy2GisDialog.resize(566, 491)
        self.gridLayout = QtWidgets.QGridLayout(Tachy2GisDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.portComboBox = QtWidgets.QComboBox(Tachy2GisDialog)
        self.portComboBox.setObjectName("portComboBox")
        self.gridLayout.addWidget(self.portComboBox, 0, 0, 1, 1)
        self.button_box = QtWidgets.QDialogButtonBox(Tachy2GisDialog)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setCenterButtons(False)
        self.button_box.setObjectName("button_box")
        self.gridLayout.addWidget(self.button_box, 8, 0, 1, 1)
        self.vertexTableView = QtWidgets.QTableView(Tachy2GisDialog)
        self.vertexTableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.vertexTableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.vertexTableView.setObjectName("vertexTableView")
        self.gridLayout.addWidget(self.vertexTableView, 6, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(Tachy2GisDialog)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 3, 0, 1, 1)
        self.sourceLayerComboBox = QgsMapLayerComboBox(Tachy2GisDialog)
        self.sourceLayerComboBox.setObjectName("sourceLayerComboBox")
        self.gridLayout_2.addWidget(self.sourceLayerComboBox, 5, 1, 1, 1)
        self.logFileButton = QtWidgets.QPushButton(Tachy2GisDialog)
        self.logFileButton.setObjectName("logFileButton")
        self.gridLayout_2.addWidget(self.logFileButton, 3, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(Tachy2GisDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 5, 0, 1, 1)
        self.logFileEdit = QtWidgets.QLineEdit(Tachy2GisDialog)
        self.logFileEdit.setReadOnly(True)
        self.logFileEdit.setObjectName("logFileEdit")
        self.gridLayout_2.addWidget(self.logFileEdit, 3, 1, 1, 1)
        self.dumpButton = QtWidgets.QPushButton(Tachy2GisDialog)
        self.dumpButton.setMaximumSize(QtCore.QSize(80, 16777215))
        self.dumpButton.setAutoRepeatInterval(100)
        self.dumpButton.setObjectName("dumpButton")
        self.gridLayout_2.addWidget(self.dumpButton, 5, 2, 1, 1)
        self.gridLayout_2.setColumnStretch(1, 1)
        self.horizontalLayout.addLayout(self.gridLayout_2)
        self.gridLayout.addLayout(self.horizontalLayout, 5, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.checkBox = QtWidgets.QCheckBox(Tachy2GisDialog)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_2.addWidget(self.checkBox)
        self.lineEdit = QtWidgets.QLineEdit(Tachy2GisDialog)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.label_2 = QtWidgets.QLabel(Tachy2GisDialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        spacerItem = QtWidgets.QSpacerItem(1000, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.deleteVertexButton = QtWidgets.QPushButton(Tachy2GisDialog)
        self.deleteVertexButton.setObjectName("deleteVertexButton")
        self.horizontalLayout_2.addWidget(self.deleteVertexButton)
        self.deleteAllButton = QtWidgets.QPushButton(Tachy2GisDialog)
        self.deleteAllButton.setObjectName("deleteAllButton")
        self.horizontalLayout_2.addWidget(self.deleteAllButton)
        self.gridLayout.addLayout(self.horizontalLayout_2, 7, 0, 1, 1)

        self.retranslateUi(Tachy2GisDialog)
        self.button_box.accepted.connect(Tachy2GisDialog.accept)
        self.button_box.rejected.connect(Tachy2GisDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Tachy2GisDialog)

    def retranslateUi(self, Tachy2GisDialog):
        _translate = QtCore.QCoreApplication.translate
        Tachy2GisDialog.setWindowTitle(_translate("Tachy2GisDialog", "Tachy2GIS"))
        self.label.setText(_translate("Tachy2GisDialog", "Log file:"))
        self.logFileButton.setText(_translate("Tachy2GisDialog", "Select"))
        self.label_3.setText(_translate("Tachy2GisDialog", "Source layer:"))
        self.dumpButton.setText(_translate("Tachy2GisDialog", "Dump"))
        self.checkBox.setText(_translate("Tachy2GisDialog", "Punktfang"))
        self.label_2.setText(_translate("Tachy2GisDialog", "local Z"))
        self.deleteVertexButton.setText(_translate("Tachy2GisDialog", "Delete vertex"))
        self.deleteAllButton.setText(_translate("Tachy2GisDialog", "Delete all"))


    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent=parent)
        self.setupUi(self)

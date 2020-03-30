# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from functions import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(409, 317)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_brsnd = QtWidgets.QLabel(self.centralwidget)
        self.label_brsnd.setGeometry(QtCore.QRect(100, 20, 59, 16))
        self.label_brsnd.setObjectName("label_brsnd")
        self.label_Model = QtWidgets.QLabel(self.centralwidget)
        self.label_Model.setGeometry(QtCore.QRect(240, 20, 59, 16))
        self.label_Model.setObjectName("label_Model")
        self.comboBox_brand = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_brand.setGeometry(QtCore.QRect(60, 40, 131, 32))
        self.comboBox_brand.setObjectName("comboBox_brand")
        self.comboBox_model = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_model.setGeometry(QtCore.QRect(200, 40, 131, 32))
        self.comboBox_model.setObjectName("comboBox_model")
        self.spinBox_Kilometers = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_Kilometers.setGeometry(QtCore.QRect(70, 100, 111, 31))
        self.spinBox_Kilometers.setMaximum(10000000)
        self.spinBox_Kilometers.setSingleStep(10000)
        self.spinBox_Kilometers.setStepType(QtWidgets.QAbstractSpinBox.DefaultStepType)
        self.spinBox_Kilometers.setObjectName("spinBox_Kilometers")
        self.label_kilometers = QtWidgets.QLabel(self.centralwidget)
        self.label_kilometers.setGeometry(QtCore.QRect(90, 80, 81, 16))
        self.label_kilometers.setObjectName("label_kilometers")
        self.label_release_date = QtWidgets.QLabel(self.centralwidget)
        self.label_release_date.setGeometry(QtCore.QRect(220, 80, 101, 16))
        self.label_release_date.setObjectName("label_release_date")
        self.spinBox_Realese_date = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_Realese_date.setGeometry(QtCore.QRect(210, 100, 121, 31))
        self.spinBox_Realese_date.setMinimum(1900)
        self.spinBox_Realese_date.setMaximum(2020)
        self.spinBox_Realese_date.setProperty("value", 2000)
        self.spinBox_Realese_date.setObjectName("spinBox_Realese_date")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(140, 140, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.label_error = QtWidgets.QLabel(self.centralwidget)
        self.label_error.setGeometry(QtCore.QRect(30, 240, 351, 31))
        self.label_error.setText("")
        self.label_error.setObjectName("label_error")
        self.lcdNumber_cost = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber_cost.setGeometry(QtCore.QRect(30, 190, 351, 41))
        self.lcdNumber_cost.setDigitCount(15)
        self.lcdNumber_cost.setObjectName("lcdNumber_cost")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(calculate)
        self.comboBox_brand.currentIndexChanged["QString"].connect(updateModels)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Guess Car Price"))
        self.label_brsnd.setText(_translate("MainWindow", "Brand:"))
        self.label_Model.setText(_translate("MainWindow", 'Model:'))
        self.label_kilometers.setText(_translate("MainWindow", "Kilometers:"))
        self.label_release_date.setText(_translate("MainWindow", "Release year:"))
        self.pushButton.setText(_translate("MainWindow", "GUESS"))


def updateModels():
    ui.comboBox_model.clear()
    brand = ui.comboBox_brand.currentText()
    models = get_models(brand)
    ui.comboBox_model.addItems(models)

def calculate():
    brand = ui.comboBox_brand.currentText()
    model = ui.comboBox_model.currentText()
    year = ui.spinBox_Realese_date.value()
    kilometers = ui.spinBox_Kilometers.value()
    answer = predict(brand, model, kilometers, year)
    ui.lcdNumber_cost.display(answer)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    brands = get_brands()
    ui.comboBox_brand.addItems(brands)

    MainWindow.show()
    sys.exit(app.exec_())

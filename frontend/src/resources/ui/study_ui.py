# Form implementation generated from reading ui file 'D:\WorkSpace\PycharmProjects\MyApplications\Study_PyQt6\StudyEng\engineering\frontend\gui\resources\ui\study.ui'
#
# Created by: PyQt6 UI code generator 6.5.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(850, 660)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.word_label = QtWidgets.QLabel(parent=Form)
        self.word_label.setMinimumSize(QtCore.QSize(250, 100))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.word_label.setFont(font)
        self.word_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.word_label.setObjectName("word_label")
        self.gridLayout.addWidget(self.word_label, 1, 2, 2, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 3, 1, 1)
        self.phonetic_label = QtWidgets.QLabel(parent=Form)
        self.phonetic_label.setText("")
        self.phonetic_label.setObjectName("phonetic_label")
        self.gridLayout.addWidget(self.phonetic_label, 3, 2, 1, 1)
        self.chinese_label = QtWidgets.QLabel(parent=Form)
        self.chinese_label.setMinimumSize(QtCore.QSize(100, 50))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.chinese_label.setFont(font)
        self.chinese_label.setText("")
        self.chinese_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.chinese_label.setObjectName("chinese_label")
        self.gridLayout.addWidget(self.chinese_label, 4, 2, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem2, 5, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(24, 97, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem3, 6, 0, 1, 1)
        self.stackedWidget = QtWidgets.QStackedWidget(parent=Form)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.page)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.know_button = PushButton(parent=self.page)
        self.know_button.setMinimumSize(QtCore.QSize(200, 100))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.know_button.setFont(font)
        self.know_button.setObjectName("know_button")
        self.horizontalLayout.addWidget(self.know_button)
        self.unknow_button = PushButton(parent=self.page)
        self.unknow_button.setMinimumSize(QtCore.QSize(200, 100))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.unknow_button.setFont(font)
        self.unknow_button.setObjectName("unknow_button")
        self.horizontalLayout.addWidget(self.unknow_button)
        self.horizontalLayout_5.addLayout(self.horizontalLayout)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.page_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.wrong_button = PushButton(parent=self.page_2)
        self.wrong_button.setMinimumSize(QtCore.QSize(200, 100))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.wrong_button.setFont(font)
        self.wrong_button.setObjectName("wrong_button")
        self.horizontalLayout_2.addWidget(self.wrong_button)
        self.correct_button = PushButton(parent=self.page_2)
        self.correct_button.setMinimumSize(QtCore.QSize(200, 100))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.correct_button.setFont(font)
        self.correct_button.setObjectName("correct_button")
        self.horizontalLayout_2.addWidget(self.correct_button)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.page_3)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.continue_button = PushButton(parent=self.page_3)
        self.continue_button.setMinimumSize(QtCore.QSize(200, 100))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.continue_button.setFont(font)
        self.continue_button.setObjectName("continue_button")
        self.horizontalLayout_4.addWidget(self.continue_button)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_4)
        self.stackedWidget.addWidget(self.page_3)
        self.gridLayout.addWidget(self.stackedWidget, 6, 1, 1, 3)
        spacerItem6 = QtWidgets.QSpacerItem(24, 97, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem6, 6, 4, 1, 1)
        self.progress_label = QtWidgets.QLabel(parent=Form)
        self.progress_label.setText("")
        self.progress_label.setObjectName("progress_label")
        self.gridLayout.addWidget(self.progress_label, 0, 4, 1, 1)
        self.return_button = TransparentToolButton(parent=Form)
        self.return_button.setMinimumSize(QtCore.QSize(50, 50))
        self.return_button.setText("")
        self.return_button.setObjectName("return_button")
        self.gridLayout.addWidget(self.return_button, 0, 0, 1, 1)
        self.horizontalLayout_7.addLayout(self.gridLayout)

        self.retranslateUi(Form)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.word_label.setText(_translate("Form", "TextLabel"))
        self.know_button.setText(_translate("Form", "认识"))
        self.unknow_button.setText(_translate("Form", "不认识"))
        self.wrong_button.setText(_translate("Form", "记错了"))
        self.correct_button.setText(_translate("Form", "没记错"))
        self.continue_button.setText(_translate("Form", "继续"))
from qfluentwidgets import PushButton, TransparentToolButton
from .. import resource_rc
# -*- coding: utf-8 -*-
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
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(parent=Form)
        self.stackedWidget.setEnabled(True)
        self.stackedWidget.setObjectName("stackedWidget")
        self.main_page = QtWidgets.QWidget()
        self.main_page.setObjectName("main_page")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.main_page)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 2)
        self.main_word_label = QtWidgets.QLabel(parent=self.main_page)
        self.main_word_label.setMinimumSize(QtCore.QSize(400, 100))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.main_word_label.setFont(font)
        self.main_word_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.main_word_label.setObjectName("main_word_label")
        self.gridLayout.addWidget(self.main_word_label, 1, 1, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem1, 2, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem2, 3, 0, 1, 1)
        self.learn_button = PushButton(parent=self.main_page)
        self.learn_button.setMinimumSize(QtCore.QSize(250, 125))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.learn_button.setFont(font)
        self.learn_button.setObjectName("learn_button")
        self.gridLayout.addWidget(self.learn_button, 3, 1, 1, 1)
        self.review_button = PushButton(parent=self.main_page)
        self.review_button.setMinimumSize(QtCore.QSize(250, 125))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setItalic(False)
        font.setUnderline(False)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.review_button.setFont(font)
        self.review_button.setObjectName("review_button")
        self.gridLayout.addWidget(self.review_button, 3, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem3, 3, 3, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout)
        self.stackedWidget.addWidget(self.main_page)
        self.study_page = QtWidgets.QWidget()
        self.study_page.setObjectName("study_page")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.study_page)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.progress_label = QtWidgets.QLabel(parent=self.study_page)
        self.progress_label.setText("")
        self.progress_label.setObjectName("progress_label")
        self.gridLayout_2.addWidget(self.progress_label, 0, 4, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_2.addItem(spacerItem4, 1, 3, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(24, 97, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_2.addItem(spacerItem5, 6, 0, 1, 1)
        self.phonetic_label = QtWidgets.QLabel(parent=self.study_page)
        self.phonetic_label.setText("")
        self.phonetic_label.setObjectName("phonetic_label")
        self.gridLayout_2.addWidget(self.phonetic_label, 3, 2, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_2.addItem(spacerItem6, 5, 2, 1, 1)
        self.chinese_label = QtWidgets.QLabel(parent=self.study_page)
        self.chinese_label.setMinimumSize(QtCore.QSize(100, 50))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.chinese_label.setFont(font)
        self.chinese_label.setText("")
        self.chinese_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.chinese_label.setObjectName("chinese_label")
        self.gridLayout_2.addWidget(self.chinese_label, 4, 2, 1, 1)
        self.return_button = TransparentToolButton(parent=self.study_page)
        self.return_button.setMinimumSize(QtCore.QSize(50, 50))
        self.return_button.setText("")
        self.return_button.setObjectName("return_button")
        self.gridLayout_2.addWidget(self.return_button, 0, 0, 1, 1)
        self.button_stackedWidget = QtWidgets.QStackedWidget(parent=self.study_page)
        self.button_stackedWidget.setObjectName("button_stackedWidget")
        self.know_page = QtWidgets.QWidget()
        self.know_page.setObjectName("know_page")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.know_page)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.know_button = PushButton(parent=self.know_page)
        self.know_button.setMinimumSize(QtCore.QSize(200, 100))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.know_button.setFont(font)
        self.know_button.setObjectName("know_button")
        self.horizontalLayout_3.addWidget(self.know_button)
        self.not_know_button = PushButton(parent=self.know_page)
        self.not_know_button.setMinimumSize(QtCore.QSize(200, 100))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.not_know_button.setFont(font)
        self.not_know_button.setObjectName("not_know_button")
        self.horizontalLayout_3.addWidget(self.not_know_button)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_3)
        self.button_stackedWidget.addWidget(self.know_page)
        self.correct_page = QtWidgets.QWidget()
        self.correct_page.setObjectName("correct_page")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.correct_page)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.correct_button = PushButton(parent=self.correct_page)
        self.correct_button.setMinimumSize(QtCore.QSize(200, 100))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.correct_button.setFont(font)
        self.correct_button.setObjectName("correct_button")
        self.horizontalLayout_6.addWidget(self.correct_button)
        self.wrong_button = PushButton(parent=self.correct_page)
        self.wrong_button.setMinimumSize(QtCore.QSize(200, 100))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.wrong_button.setFont(font)
        self.wrong_button.setObjectName("wrong_button")
        self.horizontalLayout_6.addWidget(self.wrong_button)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_6)
        self.button_stackedWidget.addWidget(self.correct_page)
        self.continue_page = QtWidgets.QWidget()
        self.continue_page.setObjectName("continue_page")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.continue_page)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem7)
        self.continue_button = PushButton(parent=self.continue_page)
        self.continue_button.setMinimumSize(QtCore.QSize(200, 100))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.continue_button.setFont(font)
        self.continue_button.setObjectName("continue_button")
        self.horizontalLayout_8.addWidget(self.continue_button)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem8)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_8)
        self.button_stackedWidget.addWidget(self.continue_page)
        self.gridLayout_2.addWidget(self.button_stackedWidget, 6, 1, 1, 3)
        spacerItem9 = QtWidgets.QSpacerItem(24, 97, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_2.addItem(spacerItem9, 6, 4, 1, 1)
        self.word_label = QtWidgets.QLabel(parent=self.study_page)
        self.word_label.setMinimumSize(QtCore.QSize(250, 100))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.word_label.setFont(font)
        self.word_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.word_label.setObjectName("word_label")
        self.gridLayout_2.addWidget(self.word_label, 1, 2, 2, 1)
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_2.addItem(spacerItem10, 0, 2, 1, 1)
        self.horizontalLayout_9.addLayout(self.gridLayout_2)
        self.stackedWidget.addWidget(self.study_page)
        self.finish_page = QtWidgets.QWidget()
        self.finish_page.setObjectName("finish_page")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.finish_page)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_3.addItem(spacerItem11, 0, 1, 1, 1)
        self.study_finish_label = QtWidgets.QLabel(parent=self.finish_page)
        self.study_finish_label.setMinimumSize(QtCore.QSize(200, 200))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.study_finish_label.setFont(font)
        self.study_finish_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.study_finish_label.setObjectName("study_finish_label")
        self.gridLayout_3.addWidget(self.study_finish_label, 1, 1, 1, 1)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_3.addItem(spacerItem12, 2, 0, 1, 1)
        self.finish_continue_button = PushButton(parent=self.finish_page)
        self.finish_continue_button.setMinimumSize(QtCore.QSize(100, 50))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.finish_continue_button.setFont(font)
        self.finish_continue_button.setObjectName("finish_continue_button")
        self.gridLayout_3.addWidget(self.finish_continue_button, 2, 1, 1, 1)
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_3.addItem(spacerItem13, 2, 2, 1, 1)
        spacerItem14 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_3.addItem(spacerItem14, 3, 1, 1, 1)
        self.horizontalLayout_10.addLayout(self.gridLayout_3)
        self.stackedWidget.addWidget(self.finish_page)
        self.horizontalLayout.addWidget(self.stackedWidget)

        self.retranslateUi(Form)
        self.stackedWidget.setCurrentIndex(0)
        self.button_stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.main_word_label.setText(_translate("Form", "TextLabel"))
        self.learn_button.setText(_translate("Form", "Learn\n"
"0"))
        self.review_button.setText(_translate("Form", "Review\n"
"0"))
        self.know_button.setText(_translate("Form", "认识"))
        self.not_know_button.setText(_translate("Form", "不认识"))
        self.correct_button.setText(_translate("Form", "没记错"))
        self.wrong_button.setText(_translate("Form", "记错了"))
        self.continue_button.setText(_translate("Form", "继续"))
        self.word_label.setText(_translate("Form", "TextLabel"))
        self.study_finish_label.setText(_translate("Form", "学习完成"))
        self.finish_continue_button.setText(_translate("Form", "继续"))
from qfluentwidgets import PushButton, TransparentToolButton
from .. import resource_rc
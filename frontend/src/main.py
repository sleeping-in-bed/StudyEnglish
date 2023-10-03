# coding:utf-8
import os
import sys
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QIcon, QDesktopServices, QPainterPath, QPixmap, QPainter, QShortcut, QKeySequence
from PyQt6.QtWidgets import QApplication, QFrame, QHBoxLayout, QWidget, QGridLayout, QStackedWidget, QVBoxLayout
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, SplitFluentWindow,
                            NavigationAvatarWidget, qrouter, SubtitleLabel, setFont, PushButton, PrimaryPushButton,
                            StrongBodyLabel, TransparentPushButton, FluentIcon, ToolTipFilter, toggleTheme)
from qfluentwidgets.components.widgets.acrylic_label import AcrylicBrush

from app_logic import get_chart_html
from resources.ui import data_view_ui, study_page_ui
from study import StudyGui
from __init__ import base_dir


class DataView(QWidget, data_view_ui.Ui_Form):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.setObjectName(text.replace(' ', '-'))
        # !IMPORTANT: leave some space for title bar
        self.horizontalLayout.setContentsMargins(0, 40, 0, 0)

        self.update_html()
        self.refresh_button.clicked.connect(self.update_html)

    def update_html(self):
        self.chart_html = get_chart_html()
        self.webEngineView.setHtml(self.chart_html)


class Home(QWidget, study_page_ui.Ui_Form):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.setObjectName(text.replace(' ', '-'))
        # !IMPORTANT: leave some space for title bar
        self.horizontalLayout.setContentsMargins(0, 40, 0, 0)

        self.study = StudyGui()
        self.learn_button.setText(f'Learn\n{self.study.new_words_num}')
        self.review_button.setText(f'Review\n{self.study.review_words_num}')
        self.learn_button.clicked.connect(self.study_new)
        self.review_button.clicked.connect(self.study_review)

        self.return_button.setIcon(FluentIcon.RETURN)
        self.return_button.clicked.connect(self.return_main_page)
        self.know_button.clicked.connect(self.show_chinese_and_wrong_and_correct_button)
        self.not_know_button.clicked.connect(self.not_know)
        self.correct_button.clicked.connect(self.correct)
        self.wrong_button.clicked.connect(self.wrong)
        self.continue_button.clicked.connect(self.next_word)

        self.finish_continue_button.clicked.connect(self.study_finished)

        # 创建快捷键并将其绑定到按钮上
        know_button_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Left), self)
        know_button_shortcut.activated.connect(self.activate_left_button)
        not_know_button_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Right), self)
        not_know_button_shortcut.activated.connect(self.activate_right_button)

        self.set_background()

    def study_init(self):
        self.word_label.setText(self.study.studying_word)
        self.progress_label.setText(
            f'{self.study.get_finished_words_num()}/{self.study.every_turn_study_words_num}')
        self.stackedWidget.setCurrentWidget(self.study_page)
        # 调用 update() 方法触发 paintEvent
        self.update()

    def study_new(self):
        self.study.study_init(self.study.new_mode)
        self.study_init()

    def study_review(self):
        self.study.study_init(self.study.review_mode)
        self.study_init()

    def return_main_page(self):
        self.stackedWidget.setCurrentWidget(self.main_page)
        # 调用 update() 方法触发 paintEvent
        self.update()

    def show_chinese_and_wrong_and_correct_button(self):
        self.chinese_label.setText(self.study.get_studying_word_chinese())
        self.button_stackedWidget.setCurrentWidget(self.correct_page)

    def not_know(self):
        self.study.zero_cleaning_meaning_study_time_and_set_not_know_true()
        self.chinese_label.setText(self.study.get_studying_word_chinese())
        self.button_stackedWidget.setCurrentWidget(self.continue_page)

    def wrong(self):
        self.study.zero_cleaning_meaning_study_time_and_set_not_know_true()
        self.next_word()

    def correct(self):
        self.study.studying_word_this_time_study_time_plus_one()
        self.next_word()

    def next_word(self):
        if self.study.next_word():
            self.chinese_label.setText('')
            self.word_label.setText(self.study.studying_word)
            self.progress_label.setText(
                f'{self.study.get_finished_words_num()}/{self.study.every_turn_study_words_num}')
            self.button_stackedWidget.setCurrentWidget(self.know_page)
        else:
            self.stackedWidget.setCurrentWidget(self.finish_page)

    def study_finished(self):
        self.return_main_page()

    def activate_left_button(self):
        object_name = self.stackedWidget.currentWidget().objectName()
        if object_name == self.main_page.objectName():
            self.learn_button.click()
        elif object_name == self.study_page.objectName():
            object_name = self.button_stackedWidget.currentWidget().objectName()
            if object_name == self.know_page.objectName():
                self.know_button.click()
            elif object_name == self.correct_page.objectName():
                self.correct_button.click()
            elif object_name == self.continue_page.objectName():
                self.continue_button.click()
        elif object_name == self.finish_page.objectName():
            self.finish_continue_button.click()

    def activate_right_button(self):
        object_name = self.stackedWidget.currentWidget().objectName()
        if object_name == self.main_page.objectName():
            self.review_button.click()
        elif object_name == self.study_page.objectName():
            object_name = self.button_stackedWidget.currentWidget().objectName()
            if object_name == self.know_page.objectName():
                self.not_know_button.click()
            elif object_name == self.correct_page.objectName():
                self.wrong_button.click()

    def set_background(self):
        self.acrylicBrush = AcrylicBrush(self, 15)
        self.acrylicBrush.setImage(QPixmap(":/images/background.jpg").scaled(self.size(),
                                                                             Qt.AspectRatioMode.KeepAspectRatio))

    def paintEvent(self, e):
        if self.stackedWidget.currentWidget().objectName() == self.main_page.objectName():
            painter = QPainter(self)
            pixmap = QPixmap(":/images/background.jpg").scaled(self.size(),
                                                               Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                                               Qt.TransformationMode.SmoothTransformation)
            painter.drawPixmap(0, 0, pixmap)
        else:
            self.acrylicBrush.paint()
        super().paintEvent(e)


class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))

        # !IMPORTANT: leave some space for title bar
        self.hBoxLayout.setContentsMargins(0, 40, 0, 0)


class Window(SplitFluentWindow):
    def __init__(self):
        super().__init__()

        # create sub interface
        self.musicInterface = DataView('Chart', self)
        self.homeInterface = Home('Study', self)
        self.settingInterface = Widget('Setting Interface', self)

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FluentIcon.HOME, '主页面')
        self.addSubInterface(self.musicInterface, FluentIcon.IOT, '统计数据')

        # add custom widget to bottom
        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=NavigationAvatarWidget('zhiyiYo', os.path.join(base_dir, r'resources/images/shoko.png')),
            onClick=self.showMessageBox,
            position=NavigationItemPosition.BOTTOM,
        )

        self.addSubInterface(self.settingInterface, FluentIcon.SETTING, 'Settings', NavigationItemPosition.BOTTOM)

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('英语学习')

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def showMessageBox(self):
        w = MessageBox(
            '支持作者🥰',
            '个人开发不易，如果这个项目帮助到了您，可以考虑请作者喝一瓶快乐水🥤。您的支持就是作者开发和维护项目的动力🚀',
            self
        )
        w.yesButton.setText('来啦老弟')
        w.cancelButton.setText('下次一定')

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://afdian.net/a/zhiyiYo"))


if __name__ == '__main__':
    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()

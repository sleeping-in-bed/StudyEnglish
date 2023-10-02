# coding:utf-8
import sys
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QIcon, QDesktopServices, QPainterPath, QPixmap, QPainter
from PyQt6.QtWidgets import QApplication, QFrame, QHBoxLayout, QWidget, QGridLayout, QStackedWidget, QVBoxLayout
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, SplitFluentWindow,
                            NavigationAvatarWidget, qrouter, SubtitleLabel, setFont, PushButton, PrimaryPushButton,
                            StrongBodyLabel, TransparentPushButton, FluentIcon, ToolTipFilter, toggleTheme)
from qfluentwidgets.components.widgets.acrylic_label import AcrylicBrush

from app_logic import get_chart_html
from resources.ui import main_page_ui, study_ui, study_finish_ui, data_view_ui
from study import StudyGui


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



class HomeChild1(QWidget, main_page_ui.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # self.theme_button.setIcon(FluentIcon.CONSTRACT)
        # self.theme_button.installEventFilter(ToolTipFilter(self.theme_button))
        # self.theme_button.setToolTip(self.tr('Toggle theme'))
        # self.theme_button.clicked.connect(lambda: toggleTheme(True))

    def paintEvent(self, e):
        painter = QPainter(self)
        # 加载图片
        pixmap = QPixmap(":/images/background.jpg").scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)  # 用你的图片文件路径替换 "image.jpg"
        painter.drawPixmap(0, 0, pixmap)


class HomeChild2(QWidget, study_ui.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.return_button.setIcon(FluentIcon.RETURN)

        self.set_background()

    def set_background(self):
        self.acrylicBrush = AcrylicBrush(self, 15)
        self.acrylicBrush.setImage(QPixmap(":/images/background.jpg").scaled(900, 700, Qt.AspectRatioMode.KeepAspectRatio))

    def paintEvent(self, e):
        if True:
            self.acrylicBrush.paint()
            super().paintEvent(e)


class HomeChild3(QWidget, study_finish_ui.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.set_background()

    def set_background(self):
        self.acrylicBrush = AcrylicBrush(self, 15)
        self.acrylicBrush.setImage(QPixmap(":/images/background.jpg").scaled(900, 700, Qt.AspectRatioMode.KeepAspectRatio))

    def paintEvent(self, e):
        if True:
            self.acrylicBrush.paint()
            super().paintEvent(e)


class Home(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.layout = QVBoxLayout(self)
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)
        self.setObjectName(text.replace(' ', '-'))
        # !IMPORTANT: leave some space for title bar
        self.layout.setContentsMargins(0, 40, 0, 0)

        self.main_page = HomeChild1()
        self.study_page = HomeChild2()
        self.study_finish_page = HomeChild3()

        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.study_page)
        self.stacked_widget.addWidget(self.study_finish_page)

        self.study = StudyGui()
        self.main_page.learn_button.setText(f'Learn\n{self.study.new_words_num}')
        self.main_page.review_button.setText(f'Review\n{self.study.review_words_num}')

        self.main_page.learn_button.clicked.connect(self.study_new)
        self.main_page.review_button.clicked.connect(self.study_review)
        self.study_page.return_button.clicked.connect(self.return_main_page)
        self.study_page.know_button.clicked.connect(self.show_chinese_and_wrong_and_correct_button)
        self.study_page.unknow_button.clicked.connect(self.unknow)
        self.study_page.correct_button.clicked.connect(self.correct)
        self.study_page.wrong_button.clicked.connect(self.wrong)
        self.study_page.continue_button.clicked.connect(self.next_word)
        self.study_finish_page.pushButton.clicked.connect(self.study_finished)

    def study_init(self):
        self.study_page.word_label.setText(self.study.studying_word)
        self.study_page.progress_label.setText(
            f'{self.study.get_finished_words_num()}/{self.study.every_turn_study_words_num}')
        self.stacked_widget.setCurrentWidget(self.study_page)

    def study_new(self):
        self.study.study_init(self.study.new_mode)
        self.study_init()

    def study_review(self):
        self.study.study_init(self.study.review_mode)
        self.study_init()

    def return_main_page(self):
        self.stacked_widget.setCurrentWidget(self.main_page)

    def show_chinese_and_wrong_and_correct_button(self):
        self.study_page.chinese_label.setText(self.study.get_studying_word_chinese())
        self.study_page.stackedWidget.setCurrentWidget(self.study_page.page_2)

    def unknow(self):
        self.study.zero_cleaning_meaning_study_time_and_set_not_know_true()
        self.study_page.chinese_label.setText(self.study.get_studying_word_chinese())
        self.study_page.stackedWidget.setCurrentWidget(self.study_page.page_3)

    def wrong(self):
        self.study.zero_cleaning_meaning_study_time_and_set_not_know_true()
        self.next_word()

    def correct(self):
        self.study.studying_word_this_time_study_time_plus_one()
        self.next_word()

    def next_word(self):
        if self.study.next_word():
            self.study_page.chinese_label.setText('')
            self.study_page.word_label.setText(self.study.studying_word)
            self.study_page.progress_label.setText(
                f'{self.study.get_finished_words_num()}/{self.study.every_turn_study_words_num}')
            self.study_page.stackedWidget.setCurrentWidget(self.study_page.page)
        else:
            self.stacked_widget.setCurrentWidget(self.study_finish_page)

    def study_finished(self):
        self.return_main_page()


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
            widget=NavigationAvatarWidget('zhiyiYo', r'resources/images/shoko.png'),
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

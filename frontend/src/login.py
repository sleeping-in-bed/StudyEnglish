import os
import sys

from PyQt6.QtCore import Qt, QTranslator, QLocale
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit
from qframelesswindow import FramelessWindow, StandardTitleBar, AcrylicWindow
from qfluentwidgets import setThemeColor, FluentTranslator, setTheme, Theme, SplitTitleBar, InfoBar, InfoBarPosition
from resources.ui.login_ui import Ui_Form
from main import Window
from app_logic import login_authentication, User

basedir = os.path.dirname(os.path.abspath(__file__))


class LoginWindow(AcrylicWindow, Ui_Form):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # setTheme(Theme.DARK)
        setThemeColor('#28afe9')

        self.setTitleBar(SplitTitleBar(self))
        self.titleBar.raise_()
        self.label.setScaledContents(False)
        self.setWindowTitle('英语学习')
        self.setWindowIcon(QIcon(":/images/logo.png"))
        self.resize(1000, 650)

        self.windowEffect.setMicaEffect(self.winId(), isDarkMode=False)
        self.titleBar.titleLabel.setStyleSheet("""
            QLabel{
                background: transparent;
                font: 13px 'Segoe UI';
                padding: 0 4px;
                color: black;
            }
        """)

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        # =========================================================================================================== #
        self.user = User()
        self.lineEdit_3.setText(self.user.get_name())
        self.lineEdit_4.setText(self.user.get_password())

        self.pushButton.clicked.connect(self.show_main)

    def remember_password(self, username, password):
        state = self.checkBox.isChecked()
        if state:
            self.user.set_name(username)
            self.user.set_password(password)
        else:
            self.user.set_name('')
            self.user.set_password('')

    def show_main(self):
        username = self.lineEdit_3.text()
        password = self.lineEdit_4.text()
        print(username, password)

        if login_authentication(username, password):
            self.remember_password(username, password)

            self.second_window = Window()
            self.close()
            self.second_window.show()
        else:
            self.createWarningInfoBar('用户名或密码错误，请重新输入', '')

    def resizeEvent(self, e):
        super().resizeEvent(e)
        pixmap = QPixmap(":/images/background.jpg").scaled(
            self.label.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self.label.setPixmap(pixmap)

    def createWarningInfoBar(self, title: str, content: str):
        InfoBar.warning(
            title=title,
            content=content,
            orient=Qt.Orientation.Horizontal,
            isClosable=False,   # disable close button
            position=InfoBarPosition.TOP_LEFT,
            duration=1000,
            parent=self
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Internationalization
    translator = FluentTranslator(QLocale())
    app.installTranslator(translator)

    w = LoginWindow()
    w.show()

    app.exec()

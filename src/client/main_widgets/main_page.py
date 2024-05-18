from PySide6 import QtWidgets, QtCore, QtGui
from src.client.main_widgets.user_profile import UserProfile
from src.client.tools import get_pixmap_path


class MainPage(QtWidgets.QFrame):
    def __init__(self, parent) -> None:
        super(MainPage, self).__init__(parent)
        self.parent = parent
        self.__init_ui()
        self.__setting_ui()

    def __init_ui(self) -> None:
        self.main_v_layout = QtWidgets.QVBoxLayout()
        self.sub_main_h_layout = QtWidgets.QHBoxLayout()
        self.welcome_label = QtWidgets.QLabel('<h1>Добро пожаловать!</h1>')
        self.logo = QtWidgets.QLabel()
        self.user_profile = UserProfile(self)

    def __setting_ui(self) -> None:
        self.setLayout(self.main_v_layout)

        self.logo.setFixedSize(384, 384)
        self.logo.setScaledContents(True)
        self.logo.setPixmap(QtGui.QPixmap(get_pixmap_path('logo.png')))
        
        self.sub_main_h_layout.addSpacerItem(QtWidgets.QSpacerItem(530, 0))
        self.sub_main_h_layout.addWidget(self.logo, 0, QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignTop)
        self.sub_main_h_layout.addWidget(self.user_profile, 0, QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTop)

        self.main_v_layout.addLayout(self.sub_main_h_layout)
        self.main_v_layout.addSpacerItem(QtWidgets.QSpacerItem(0, 25))
        self.main_v_layout.addWidget(self.welcome_label, 0, QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignTop)

    
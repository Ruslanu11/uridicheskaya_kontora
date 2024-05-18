from PySide6 import QtWidgets, QtCore, QtGui
from src.client.dialog_forms.login_form import LoginForm
from src.client.dialog_forms.register_form import RegisterForm
from src.client.tools import get_pixmap_path



class AuthorizationMenu(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super(AuthorizationMenu, self).__init__(parent)
        self.parent = parent
        self.__init_ui()
        self.__setting_ui()
    
    def __init_ui(self) -> None:
        self.main_v_layout = QtWidgets.QVBoxLayout()
        self.buttons_h_layout = QtWidgets.QHBoxLayout()
        self.authorization_label = QtWidgets.QLabel('<h1>Авторизация</h1>')
        self.logo = QtWidgets.QLabel()
        self.login_button = QtWidgets.QPushButton(text='Войти')
        self.register_button = QtWidgets.QPushButton(text='Зарегистрироваться')
    
    def __setting_ui(self) -> None:
        self.setLayout(self.main_v_layout)

        self.logo.setFixedSize(384, 384)
        self.logo.setScaledContents(True)
        self.logo.setPixmap(QtGui.QPixmap(get_pixmap_path('logo.png')))

        self.buttons_h_layout.addWidget(self.login_button, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
        self.buttons_h_layout.addWidget(self.register_button, 0, QtCore.Qt.AlignmentFlag.AlignBottom)

        self.buttons_h_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom)

        self.main_v_layout.addWidget(self.logo, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.main_v_layout.addWidget(self.authorization_label, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.main_v_layout.addLayout(self.buttons_h_layout)

        self.login_button.clicked.connect(self.on_login_button_click)
        self.register_button.clicked.connect(self.on_register_button_click)

    def open_login_dialog(self) -> None:
        LoginForm(self.parent)
    
    def open_register_dialog(self) -> None:
        RegisterForm(self.parent)

    def on_login_button_click(self) -> None:
        self.open_login_dialog()

    def on_register_button_click(self) -> None:
        self.open_register_dialog()
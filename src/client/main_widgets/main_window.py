from PySide6 import QtWidgets, QtCore, QtGui
from src.client.api.session import Session
from src.client.main_widgets.authorization_menu import AuthorizationMenu
from src.client.main_widgets.main_page import MainPage
from src.client.main_widgets.menu_table_views import MenuTableViews
from src.client.tools import get_pixmap_path
import multiprocessing



class MainWindow(QtWidgets.QMainWindow):
    session: Session = Session()

    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.__init_ui()
        self.__setting_ui()

        self.show()
    
    def __init_ui(self) -> None:
        self.central_widget = QtWidgets.QWidget(self)
        self.main_h_layout = QtWidgets.QVBoxLayout()
        self.tab_widget = QtWidgets.QTabWidget()
        self.main_page = MainPage(self)
        self.authorization_menu = AuthorizationMenu(self)
        self.menu_table_views = MenuTableViews(self)
        
    def __setting_ui(self) -> None:
        self.setCentralWidget(self.central_widget)
        self.resize(1800, 800)
        self.central_widget.setLayout(self.main_h_layout)
        self.setWindowTitle('Uridicheskaya Kontora')
        self.setWindowIcon(QtGui.QIcon(get_pixmap_path('logo.png')))
        self.main_h_layout.setContentsMargins(0, 0, 0, 0)
        self.main_h_layout.addWidget(self.authorization_menu)
        self.main_h_layout.addWidget(self.tab_widget)

        self.tab_widget.addTab(self.main_page, 'Main Page')
        self.tab_widget.addTab(self.menu_table_views, 'Menu')

        self.tab_widget.hide()
        
    def show_message(self, text: str, error: bool=False, parent=None):
        message_box = QtWidgets.QMessageBox(self if not parent else parent)
        message_box.setWindowTitle('Information' if not error else 'Error')
        message_box.setText(text)
        message_box.setIcon(QtWidgets.QMessageBox.Icon.Information if not error else QtWidgets.QMessageBox.Icon.Critical)
        message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        message_box.exec_()

    def authorization(self) -> None:
        self.authorization_menu.hide()
        self.tab_widget.show()
        self.size_expand(self.tab_widget.currentWidget())
        self.main_page.user_profile.fill_line_edits()
        self.menu_table_views.include_widgets_for_pl()

    def size_expand(self, widget: QtWidgets.QWidget) -> None:
        self.setFixedWidth(widget.width())

    def leave(self) -> None:
        self.authorization_menu.show()
        self.tab_widget.hide()
        self.session.leave()
        self.size_expand(self.tab_widget.currentWidget())
        self.menu_table_views.include_widgets_for_pl()

    def show_message(self, text: str, error: bool = False, parent=None) -> None:
        message_box = QtWidgets.QMessageBox(parent=self if not parent else parent)
        message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        message_box.setWindowTitle('Error' if error else 'Information')
        message_box.setText(text)
        message_box.setIcon(QtWidgets.QMessageBox.Icon.Critical if error else QtWidgets.QMessageBox.Icon.Information)
        message_box.exec_()

    def close_func(self) -> None:
        self.close()
        exit()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.close_func()
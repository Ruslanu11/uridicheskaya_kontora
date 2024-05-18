from PySide6 import QtWidgets, QtCore, QtGui
from src.database.database_models import db_models
from src.client.dialog_forms.table_action_dialog import TableAction
from src.client.api.resolvers import add_action, upd_action, del_action
from src.client.tools import include_widgets
import settings
import peewee
from src.database.database_models import  *


class MenuTableViews(QtWidgets.QFrame):
    database_model: BaseModel = None
    dialog: TableAction = None
    row: int = 0
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)
        self.parent = parent
        self.__init_ui()
        self.__setting_ui()
    
    def __init_ui(self) -> None:
        self.main_v_layout = QtWidgets.QVBoxLayout()
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.table_name = QtWidgets.QLabel()
        self.table_layout = QtWidgets.QVBoxLayout()
        self.table_tools_layout = QtWidgets.QHBoxLayout()
        self.table: QtWidgets.QTableWidget = QtWidgets.QTableWidget()
        self.cancel_button = QtWidgets.QToolButton()
        self.buttons_layout = QtWidgets.QVBoxLayout()
        self.add_button = QtWidgets.QPushButton('Добавить')
        self.update_button = QtWidgets.QPushButton('Обновить')
        self.delete_button = QtWidgets.QPushButton('Удалить')
        self.button_group = QtWidgets.QButtonGroup()

    def __setting_ui(self) -> None:
        self.setLayout(self.main_v_layout)
        self.main_v_layout.addWidget(self.scroll_area)
        self.main_v_layout.addLayout(self.table_layout)

        self.buttons_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.buttons_layout.addWidget(self.add_button)
        self.buttons_layout.addWidget(self.update_button)
        self.buttons_layout.addWidget(self.delete_button)
        
        self.table_tools_layout.addWidget(self.cancel_button, 0, QtCore.Qt.AlignmentFlag.AlignTop)
        self.table_tools_layout.addWidget(self.table, 1)
        self.table_tools_layout.addLayout(self.buttons_layout)

        self.table_layout.addWidget(self.table_name, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.table_layout.addLayout(self.table_tools_layout)
        
        self.table.setEditTriggers(QtWidgets.QTableWidget.EditTrigger.NoEditTriggers)  # Отключаем редактирование ячеек
        
        self.scroll_area.setWidgetResizable(True)   
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        [self.scroll_layout.addWidget(MenuTableViews.ModifyButton(db_model._meta.table_name)) for db_model in db_models]

        layout = self.scroll_layout
        for i in range(0, self.scroll_layout.count()):
            item = layout.itemAt(i)
            widget: MenuTableViews.ModifyButton = item.widget()

            if widget:
                if isinstance(widget, MenuTableViews.ModifyButton):
                    widget.setObjectName(widget.text())
                    self.button_group.addButton(widget)
                    for model in db_models:
                        if widget.objectName() == model._meta.table_name:
                            widget.set_database_model(model)
                
        self.table.hide()
        self.table_name.hide()
        self.add_button.hide()
        self.update_button.hide()
        self.delete_button.hide()
        self.cancel_button.hide()

        self.cancel_button.setFixedSize(22, 22)
        self.cancel_button.setIcon(QtGui.QPixmap(f'{settings.IMG_PATH}/cancel_reversed.png'))
        self.cancel_button.setIconSize(QtCore.QSize(22, 22))

        self.table.doubleClicked.connect(self.upd_button_clicked)
        self.cancel_button.clicked.connect(self.cancel_button_clicked)
        self.add_button.clicked.connect(self.add_button_clicked)
        self.update_button.clicked.connect(self.upd_button_clicked)
        self.delete_button.clicked.connect(self.del_button_clicked)
        self.button_group.buttonClicked.connect(self.button_clicked)
    
    def button_clicked(self, button: QtWidgets.QPushButton) -> None:
        self.database_model = button.database_model     
        self.scroll_area.hide()
        self.table.show()
        self.table_name.show()
        self.cancel_button.show()
        self.add_button.show()
        self.update_button.show()
        self.delete_button.show()
        self.table_name.setText(f'<h2>{button.objectName()}</h2>')
        self.fill_table(self.database_model)

    def include_widgets_for_pl(self) -> None:
        include_widgets(User.get(User.id == self.parent.session.user.id).position_id.power_level, self.scroll_layout)
    
    def clear_table(self):
        self.table.clearContents()
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        self.row = 0
    
    def fill_table(self, database_model: BaseModel) -> None:
        self.clear_table()
        self.table.setColumnCount(len(database_model._meta.sorted_field_names))
        self.table.setHorizontalHeaderLabels(database_model._meta.sorted_field_names)
        self.table.setRowCount(database_model.select().count())
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        for model in database_model.select():
            for j, column in enumerate(database_model._meta.sorted_field_names):
                if '_id' in column:
                    table = ''
                    list_items_field = column.split('_')
                    for item in list_items_field:
                        if 'id' in item:
                            continue
                        table += item.capitalize()

                    identifier_field = eval(f'{table}._meta.identifier_field')

                    item = QtWidgets.QTableWidgetItem(str(eval(f'{table}.get({table}.id == model.{column}).{identifier_field}')))
                else:
                    item = QtWidgets.QTableWidgetItem(str(eval(f'model.{column}')))
                self.table.setItem(self.row, j, item)
            self.row += 1

    def cancel_button_clicked(self) -> None:
        self.router = None
        self.table.hide()
        self.table_name.hide()
        self.cancel_button.hide()
        self.scroll_area.show()
        self.add_button.hide()
        self.update_button.hide()
        self.delete_button.hide()
        self.clear_table()

    def create_data(self, dialog: TableAction) -> str:
        data = {}
        layout =  dialog.line_edits_layout

        for i in range(0, layout.count()):
            item = layout.itemAt(i)
            widget: QtWidgets.QLineEdit | QtWidgets.QComboBox = item.widget()
            if isinstance(widget, QtWidgets.QLineEdit):
                if widget.objectName() == 'id':
                    continue
                data[widget.objectName()] = widget.text()
            elif isinstance(widget, QtWidgets.QComboBox):
                current_value = widget.currentText()

                table = ''
                list_items_field = widget.objectName().split('_')
                for item in list_items_field:
                    if 'id' in item:
                        continue
                    table += item.capitalize()

                identifier_field = eval(f'{table}._meta.identifier_field')

                new_value = f'"{current_value}"' if type(current_value) == str else f'{current_value}'

                record_id = eval(f'{table}.get({table}.{identifier_field} == {new_value}).id')

                print(record_id)

                data[widget.objectName()] = record_id
        

        return data


    def add_button_clicked(self) -> None:
        dialog = TableAction(self, self.database_model, 'Добавить в')

        if dialog.rejected == True:
            return

        data = self.create_data(dialog)

        result = add_action(self.database_model, data)
        
        if not result:
            self.parent.show_message(text='Один или несколько вторичных ключей, введенных вами, не существуют!', error=True, parent=self)

        self.fill_table(self.database_model)

    def upd_button_clicked(self) -> None:
        self.table.clearSelection()
        if self.table.currentRow() == -1:
            self.parent.show_message(
                    text='Не выбрана запись',
                    error=True,
                    parent=self
                )
            return
        
        data = {}
        row = self.table.currentRow()
        id = self.table.model().index(row, 0).data()

        for index, column in zip(range(0, self.table.columnCount()), self.database_model._meta.sorted_field_names):
            column_data = self.table.model().index(row, index).data()
            data[column] = column_data

        dialog = TableAction(self, self.database_model, 'Изменить в', data)

        dialog.setWindowTitle(f'Изменить в {self.database_model._meta.table_name}')
        
        if dialog.rejected == True:
            return
        
        data = self.create_data(dialog)

        result = upd_action(id, self.database_model, data)

        if not result:
            self.parent.show_message(text='Один или несколько вторичных ключей, введенных вами, не существуют!', error=True, parent=self)

        self.fill_table(self.database_model)

    def del_button_clicked(self) -> None:
        if self.table.currentRow() == -1:
            self.parent.show_message(
                    text='Не выбрана запись',
                    error=True,
                    parent=self
                )
            return
        
        if QtWidgets.QMessageBox.question(self, 'Подтверждение', 'Вы уверены?') != QtWidgets.QMessageBox.StandardButton.Yes:
            return
        
        row = self.table.currentRow()
        id = self.table.model().index(row, 0).data()

        del_action(id, self.database_model)
        
        self.fill_table(self.database_model)

    class ModifyButton(QtWidgets.QPushButton):
        database_model = None
        def set_database_model(self, database_model):
            self.database_model = database_model
            self.setProperty('power_level', database_model._meta.power_level)
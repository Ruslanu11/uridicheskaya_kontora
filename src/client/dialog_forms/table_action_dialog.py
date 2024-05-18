from PySide6 import QtWidgets, QtCore, QtGui
from src.database.database_models import *
import peewee


class TableAction(QtWidgets.QDialog):
    rejected: bool = True
    def __init__(self, parent: QtWidgets.QWidget, database_model: peewee.Model, action: str, data: dict = {}) -> None:
        super().__init__(parent)
        self.setWindowTitle(f'{action} {database_model._meta.table_name}')
        self.parent = parent
        self.database_model = database_model
        self.__init_ui()
        self.__setting_ui()
        if 'Изменить' in action:
            self.fill_line_edits(data) 
        self.exec_()
    
    def __init_ui(self) -> None:
        self.main_v_layout = QtWidgets.QVBoxLayout()
        self.input_layout = QtWidgets.QHBoxLayout()
        self.labels_layout = QtWidgets.QVBoxLayout()
        self.line_edits_layout = QtWidgets.QVBoxLayout()
        self.confirm_button = QtWidgets.QPushButton('Подтвердить')

    def __setting_ui(self) -> None:
        self.setLayout(self.main_v_layout)

        self.main_v_layout.addLayout(self.input_layout)

        self.input_layout.addLayout(self.labels_layout)
        self.input_layout.addLayout(self.line_edits_layout)

        columns = self.database_model._meta.sorted_field_names

        for column, field in zip(columns, [getattr(self.database_model, field_name) for field_name in columns]):
            if column == 'id':
                continue

            self.labels_layout.addWidget(QtWidgets.QLabel(column))
            if '_id' in column:
                widget = QtWidgets.QComboBox()
                table = ''
                list_items_field = column.split('_')
                for item in list_items_field:
                    if 'id' in item:
                        continue
                    table += item.capitalize()
                self.fill_combo_box(widget, table)
            else:
                widget = QtWidgets.QLineEdit()
                if isinstance(field, peewee.IntegerField):
                    widget.setValidator(QtGui.QIntValidator())
            widget.setObjectName(column)
            self.line_edits_layout.addWidget(widget)

        self.main_v_layout.addWidget(self.confirm_button, 0, QtCore.Qt.AlignmentFlag.AlignRight)

        self.confirm_button.clicked.connect(self.confirm_button_clicked)

    def validate_line_edits(self) -> bool:
        layout = self.line_edits_layout
        for i in range(0, layout.count()):
            item = layout.itemAt(i)
            widget: QtWidgets.QLineEdit | QtWidgets.QComboBox = item.widget()
            if widget:
                if isinstance(widget, QtWidgets.QComboBox):
                    if widget.currentText() == '':
                        return False
                elif isinstance(widget, QtWidgets.QLineEdit):
                    if widget.text() == '':
                        return False

        return True
    
    def fill_combo_box(self, combo_box: QtWidgets.QComboBox, table: str) -> None:
        identifier_field = eval(f'{table}._meta.identifier_field')
        for record in eval(f'{table}.select({table}.{identifier_field})'):
            combo_box.addItem(str(eval(f'record.{identifier_field}')))

    def fill_line_edits(self, data: dict) -> None:
        layout = self.line_edits_layout

        for i in range(0, layout.count()):
            item = layout.itemAt(i)
            widget: QtWidgets.QLineEdit | QtWidgets.QComboBox = item.widget()
            if isinstance(widget, QtWidgets.QLineEdit):
                for column in self.database_model._meta.sorted_field_names:
                    if widget.objectName() == column:
                        widget.setText(data.get(column))
            elif isinstance(widget, QtWidgets.QComboBox):
                for column in self.database_model._meta.sorted_field_names:
                    if widget.objectName() == column:
                        widget.setCurrentText(data.get(column))

    def confirm_button_clicked(self) -> None:
        if not self.validate_line_edits():
            self.parent.parent.show_message(
                text='Одно или несколько полей пустые',
                error=True
            )
            return
        self.rejected = False
        self.hide()

    def closeEvent(self, arg__1: QtGui.QCloseEvent) -> None:
        self.rejected = True
        self.hide()
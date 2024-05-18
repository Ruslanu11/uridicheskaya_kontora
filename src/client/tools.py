from PySide6 import QtWidgets
import settings


def get_pixmap_path(pixmap: str) -> str:
    return f'{settings.IMG_PATH}/{pixmap}'

def include_widgets(power_level: int,  layout: QtWidgets.QLayout) -> None:
    for i in range(0, layout.count()):
        item = layout.itemAt(i)
        widget: QtWidgets.QPushButton = item.widget()

        if widget:
            if not issubclass(type(widget), QtWidgets.QWidget):
                continue

            print(widget.property('power_level'))

            if widget.property('power_level') is not None:
                widget.show() if power_level >= widget.property('power_level') else widget.hide()
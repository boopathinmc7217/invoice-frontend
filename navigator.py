from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLineEdit, QPushButton, QVBoxLayout,
    QFormLayout, QLabel, QHBoxLayout, QMessageBox, QGroupBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QDateEdit, QDialog, QCheckBox, QAbstractItemView, QFileDialog, QMenuBar, QMenu,QComboBox
)


class Navigator(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.init_ui()


    def init_ui(self):
        pass
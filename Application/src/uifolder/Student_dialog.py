from PyQt6.QtWidgets import QDialog
from .StudentDialog import Ui_Dialog

class Students_Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

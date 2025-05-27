from PyQt6.QtWidgets import QDialog
from .EquipmentManager_AddDialog import Add_Dialog

class AddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Add_Dialog()
        self.ui.setupUi(self)
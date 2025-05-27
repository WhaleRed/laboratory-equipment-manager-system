from PyQt6.QtWidgets import QDialog
from .ProfessorDialog import Professor_Dialog

class ProfessorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Professor_Dialog()
        self.ui.setupUi(self)

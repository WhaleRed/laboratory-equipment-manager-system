from PyQt6.QtWidgets import QDialog, QMessageBox
from .ProfessorDialog import Professor_Dialog
from src.modules.add import addProfessor


class ProfessorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Professor_Dialog()
        self.ui.setupUi(self)
        self.professorButtons()

    def professorButtons(self):
        self.ui.saveButton.clicked.connect(self.saveProfessor)
        self.ui.cancelButton.clicked.connect(self.close)

    def saveProfessor(self):
        try:
            # Retrieve input values
            professor_id = self.ui.ProfessorID_box.text().strip()
            first_name = self.ui.firstName_box.text().strip()
            last_name = self.ui.lastName_box.text().strip()

            # Validate inputs
            if not professor_id or not first_name or not last_name:
                QMessageBox.warning(self, "Input Error", "All fields are required.")
                return

            # Prepare professor data
            professor = {
                "profId": professor_id,
                "fname": first_name,
                "lname": last_name
            }

            # Call the addProfessor function
            result = addProfessor(professor)

            if result == 0:
                QMessageBox.information(self, "Success", "Professor added successfully.")
                self.accept() 
            elif result == 1:
                QMessageBox.warning(self, "Duplicate Error", "Professor ID already exists.")
            else:
                QMessageBox.critical(self, "Error", "An unexpected error occurred.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while saving the professor: {str(e)}")
            self.close()  # Close the dialog in case of an error
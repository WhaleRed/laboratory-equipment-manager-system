from PyQt6.QtWidgets import QDialog, QMessageBox
from .ProfessorDialog import Professor_Dialog
from src.modules.edit import editProfessor


class editProfessorDialog(QDialog):
    def __init__(self, parent=None, profdata = None):
        super().__init__(parent)
        self.ui = Professor_Dialog()
        self.ui.setupUi(self)
        self.professorButtons()
        self.prof_data = profdata or []
        self.ui.ProfessorID_box.setText(str(self.prof_data[0][0]))
        self.ui.firstName_box.setText(str(self.prof_data[0][1]))
        self.ui.lastName_box.setText(str(self.prof_data[0][2]))

    def professorButtons(self):
        self.ui.saveButton.clicked.connect(self.saveProfessor)
        self.ui.cancelButton.clicked.connect(self.close)

    def saveProfessor(self):
        result = None
        try:
            # Retrieve input values
            professor_id = self.ui.ProfessorID_box.text().strip()
            first_name = self.ui.firstName_box.text().strip()
            last_name = self.ui.lastName_box.text().strip()
            currentProfId = self.prof_data[0][0]
            # Validate inputs
            if not professor_id or not first_name or not last_name:
                QMessageBox.warning(self, "Input Error", "All fields are required.")
                return
            # Prepare professor data
            professor = {
                "new_profId": professor_id,
                "new_fname": first_name,
                "new_lname": last_name,
                "current_profId": currentProfId
            }

            # Call the editProfessor function
            reply = QMessageBox.question(
                self,
                "Confirm Action",
                "Do you want to proceed?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No  # Default button
            )

            if reply == QMessageBox.StandardButton.Yes:
              result = editProfessor(professor)
            if result is not None:
              if result == 0:
                  QMessageBox.information(self, "Success", "Professor edited successfully.")
                  self.accept() 
              elif result == 1:
                  QMessageBox.warning(self, "Duplicate Error", "Professor ID already exists.")
              elif result == 2:
                  QMessageBox.warning(self, "Edit Error", "Professor ID is currently used.")
              else:
                  QMessageBox.critical(self, "Error", "An unexpected error occurred.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while saving the professor: {str(e)}")
            self.close()  # Close the dialog in case of an error
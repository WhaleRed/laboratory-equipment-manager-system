from PyQt6.QtWidgets import QDialog, QMessageBox
from .StudentDialog import Ui_Dialog
from src.modules.add import addBorrower

class Students_Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.addButtons()
        self.populateProgramComboBox()
    
    def populateProgramComboBox(self):
        programs = [
            "BA Comms", "BA Eng", "BA Filipino", "BA Hist", "BA Phil", "BA SocSci", "BAELS", "BS Animal Bio",
            "BS Archi", "BS Bio", "BS Biodiv", "BS Chem", "BS Econ", "BS Finance", "BS Marine Bio", "BS Math",
            "BS Micro Bio", "BS Physics", "BS Psych", "BS Stat", "BSA", "BSCA", "BSCE", "BSCerE", "BSCS", "BSE",
            "BSECE", "BSEnviE", "BSIT", "BSIS", "BSME", "BSMETE", "BSN", "BSBA-HRM", "BSBA-MM", "BSEE"
        ]
        self.ui.programComboBox.setEditable(True)
        self.ui.programComboBox.clear()
        self.ui.programComboBox.addItems(programs)

    def addButtons(self):
        self.ui.saveButton.clicked.connect(self.saveBorrower)
        self.ui.cancelButton.clicked.connect(self.close)
    
    def saveBorrower(self):
        try:
            student_id = self.ui.ID_box.text().strip()
            program = self.ui.programComboBox.currentText().strip()
            fname = self.ui.firstName_box.text().strip()
            lname = self.ui.lastName_box.text().strip()
            block = self.ui.Yearlevel_Spinbox.value()
            # Validate inputs
            if not student_id or not fname or not lname or not program or not block:
                QMessageBox.warning(self, "Input Error", "All fields are required.")
                return

            if self.ui.programComboBox.findText(program) == -1:
                self.ui.programComboBox.addItem(program)
                items = [self.ui.programComboBox.itemText(i) for i in range(self.ui.programComboBox.count())]
                items.sort()
                self.ui.programComboBox.clear()
                self.ui.programComboBox.addItems(items)

            # Set the current selection to the entered program
            self.ui.programComboBox.setCurrentText(program)
            # Prepare borrower data

            borrower = {
                "borrowerId": student_id,
                "fname": fname,
                "lname": lname,
                "program": program,
                "yearlevel": block
            }
            # Call the addBorrower function
            result = addBorrower(borrower)

            if result == 0:
                QMessageBox.information(self, "Success", "Borrower added successfully.")
                self.accept()
            elif result == 1:
                QMessageBox.warning(self, "Duplicate Error", "Borrower ID already exists.")
            else:
                QMessageBox.critical(self, "Error", "An unexpected error occurred.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while saving the borrower: {str(e)}")
            self.close()


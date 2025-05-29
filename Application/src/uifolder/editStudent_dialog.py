from PyQt6.QtWidgets import QDialog, QMessageBox, QCompleter, QComboBox
from PyQt6.QtCore import Qt
from .StudentDialog import Ui_Dialog
from src.modules.fetchData import fetchProfID
from src.modules.edit import editBorrower

class EditStudent_Dialog(QDialog):
    def __init__(self, parent=None, studentdata = None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        print(f" student data: {studentdata}")
        self.addButtons()
        self.populateProgramComboBox()
        self.student_data = studentdata or []
        self.ui.programComboBox.setCurrentText(str(self.student_data[0][3]))
        self.ui.ID_box.setText(str(self.student_data[0][0]))
        self.ui.firstName_box.setText(str(self.student_data[0][1]))
        self.ui.lastName_box.setText(str(self.student_data[0][2]))
        self.ui.Yearlevel_Spinbox.setValue(int(self.student_data[0][4]))
        
        #self.ui.programComboBox.lineEdit().textEdited.connect(self.on_program_text_changed)
    
    def populateProgramComboBox(self):
        try:
            programs = [
                "BA Comms", "BA Eng", "BA Filipino", "BA Hist", "BA Phil", "BA SocSci", "BAELS", "BS Animal Bio",
                "BS Archi", "BS Bio", "BS Biodiv", "BS Chem", "BS Econ", "BS Finance", "BS Marine Bio", "BS Math",
                "BS Micro Bio", "BS Physics", "BS Psych", "BS Stat", "BSA", "BSCA", "BSCE", "BSCerE", "BSCS", "BSE",
                "BSECE", "BSEnviE", "BSIT", "BSIS", "BSME", "BSMETE", "BSN", "BSBA-HRM", "BSBA-MM", "BSEE"
            ]

            self.ui.programComboBox.setEditable(True)
            self.ui.programComboBox.clear()
            self.ui.programComboBox.addItem("")  # Placeholder entry
            self.ui.programComboBox.addItems(programs)

            completer = QCompleter(programs, self.ui.programComboBox)
            completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            completer.setFilterMode(Qt.MatchFlag.MatchContains)

            self.ui.programComboBox.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
            self.ui.programComboBox.setEditable(True)
            self.ui.programComboBox.setCompleter(completer)
            self.ui.programComboBox.lineEdit().setPlaceholderText("Search or select program")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load programs: {str(e)}")

    def addButtons(self):
        self.ui.saveButton.clicked.connect(self.saveBorrower)
        self.ui.cancelButton.clicked.connect(self.close)
    
    def saveBorrower(self):
        result = None
        try:
            student_id = self.ui.ID_box.text().strip()
            program = self.ui.programComboBox.currentText().strip()
            fname = self.ui.firstName_box.text().strip()
            lname = self.ui.lastName_box.text().strip()
            year = self.ui.Yearlevel_Spinbox.value()
            current_id = self.student_data[0][0]
            # Validate inputs
            if not student_id or not fname or not lname or not program or not year:
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
                "new_borrowerId": student_id,
                "new_fname": fname,
                "new_lname": lname,
                "new_program": program,
                "new_yearlvl": year,
                "current_borrowerId": current_id
            }
            # Call the editBorrower function
            reply = QMessageBox.question(
                self,
                "Confirm Action",
                "Do you want to proceed?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No  # Default button
            )

            if reply == QMessageBox.StandardButton.Yes:
                result = editBorrower(borrower)
            if result is not None:
                if result == 0:
                    QMessageBox.information(self, "Success", "Borrower edited successfully.")
                    self.accept()
                elif result == 1:
                    QMessageBox.warning(self, "Duplicate Error", "Borrower ID already exists.")
                elif result == 2:
                    QMessageBox.warning(self, "Is being used", "Current Borrower is being used")
                else:
                    QMessageBox.critical(self, "Error", "An unexpected error occurred.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while saving the borrower: {str(e)}")
            self.close()


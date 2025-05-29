from .EquipmentManager_CSM import Ui_MainWindow
from PyQt6 import QtWidgets
import re
from ..modules.fetchData import fetchBorrower
from ..modules.add import addBorrower
from PyQt6.QtWidgets import QCompleter, QMessageBox
from PyQt6.QtCore import Qt

class Confirmation:
    def __init__(self, ui: Ui_MainWindow):
        self.ui = ui
        self.parent_widget = self.ui.centralwidget
        self.ui.next_button_additem.clicked.connect(self.User_Table_Inputs)
        self.ui.submit_confirmation.clicked.connect(self.submitConfirm)
        self.studentInfo = []
        self.populate_professor_combobox()

    def populate_professor_combobox(self):
        from ..modules.fetchData import fetch_all_professor_names
        try:
            professors = fetch_all_professor_names()
            self.ui.input_professor_uinfo.clear()
            self.ui.input_professor_uinfo.addItems(professors)

            # Setup completer (optional)
            completer = QCompleter(professors, self)
            completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            completer.setFilterMode(Qt.MatchFlag.MatchContains)
            self.ui.input_professor_uinfo.setCompleter(completer)
            self.ui.input_professor_uinfo.setEditable(True)
            self.ui.input_professor_uinfo.setInsertPolicy(QtWidgets.QAbstractItemView)
        except Exception as e:
            QMessageBox.critical(self.parent_widget, "Error", f"Failed to load professors: {str(e)}")

    def show_warning(self, title, message):
        QtWidgets.QMessageBox.warning(self.parent_widget, title, message)
    
    def user_input_fields(self):
        student_id = self.ui.input_idno_uinfo.text().strip()
        professor = self.ui.input_professor_uinfo.currentText().strip()

        if not student_id or not professor:
            self.show_warning("Input Error", "All fields must be filled out.")
            return False

        if not self.studentidformat(student_id):
            self.show_warning("Input Error", "Invalid Student ID format. Must be YYYY-NNNN.")
            return False
        
        if not professor:
            self.show_warning("Input Error", "Please select a professor or Type the Professor's Name")
            return False

        
        self.ui.label_3.setText(student_id)
        self.ui.label_4.setText(professor)
        
        self.studentInfo.append(student_id)
        self.studentInfo.append(professor)

        return True
    
    def User_Table_Inputs(self):
        item_details = []
        item_names = []
        quantities = []
        
        for row in range(self.ui.Item_table.rowCount()):
            item_item = self.ui.Item_table.item(row, 0)
            qty_widget = self.ui.Item_table.cellWidget(row, 2)
            if item_item and qty_widget and isinstance(qty_widget, QtWidgets.QSpinBox):
                item_name = item_item.text()
                quantity = qty_widget.value()
                if quantity > 0:
                    item_details.append(f"{item_name}: {quantity}")
                    item_names.append(item_name)
                    quantities.append(quantity)

        item_summary = "\n".join(item_details) if item_details else "No items selected"
        self.ui.textEdit.setPlainText(item_summary)
        
        print(f"Extracted names: {item_names}")
        print(f"Quantities: {quantities}")
        
        return item_names, quantities
    
    def submitConfirm(self):
        if self.studentInfo:
            exist = fetchBorrower(self.studentInfo[0])
            if exist:
                print("Already Exists")
            else:
                student = {
                    "borrowerId": self.studentInfo[0],
                    "profId": self.studentInfo[1],
                    "fname": self.studentInfo[2],
                    "lname": self.studentInfo[3],
                    "program": self.studentInfo[4],
                    "yearlevel": self.studentInfo[5]
                }
                res = addBorrower(student)
                if res == 1:
                    print("Already Exists")
                elif res == 0:
                    print("Added Succesfully")


    def studentidformat(self, student_id):
        return bool(re.match(r'^\d{4}-\d{4}$', student_id))
       
    def studentnameformat(self, first_name, last_name):
        return bool(re.match(r'^[a-zA-Z ]+$', first_name)) and bool(re.match(r'^[a-zA-Z ]+$', last_name))

 
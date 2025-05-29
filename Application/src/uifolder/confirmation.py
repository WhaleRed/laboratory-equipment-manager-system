from .EquipmentManager_CSM import Ui_MainWindow
from PyQt6 import QtWidgets
import re
from ..modules.fetchData import fetchBorrower
from ..modules.add import addBorrower
from PyQt6.QtWidgets import QCompleter, QMessageBox, QComboBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
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
            # Step 1: Get [(name, id), ...]
            professors = fetch_all_professor_names()

            # Step 2: Clear previous items
            self.ui.input_professor_uinfo.clear()

            # Step 3: Create a mapping from name → ID
            self.professor_id_map = {}  

            # Step 4: Populate combobox and map
            for prof_id, full_name in professors:
                display_text = f"{prof_id} - {full_name}"
                self.ui.input_professor_uinfo.addItem(display_text, userData=prof_id)


            # Step 5: Setup completer
            completer = QCompleter([name for name, _ in professors])
            print("pogi")
            completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            print("pogi2")
            completer.setFilterMode(Qt.MatchFlag.MatchContains)
            print("pogi3")
            print("pogi4")
            self.ui.input_professor_uinfo.setEditable(True)
            print("pogi5")
            self.ui.input_professor_uinfo.setInsertPolicy(QComboBox.InsertPolicy.InsertAtTop)
            print("pogi6")
            self.ui.input_professor_uinfo.setCompleter(completer)
            self.ui.input_professor_uinfo.currentTextChanged.connect(lambda text: self.ui.input_professor_uinfo.setCurrentText(text))
            self.ui.input_professor_uinfo.setStyleSheet("""
                QComboBox {
                    border: 2px solid #990000;
                    border-radius: 15px;
                    padding: 5px;
                    background-color: rgb(248, 242, 242);
                    color: rgb(0, 0, 0);
                    font: 15pt "Nunito";
                }
                QComboBox:hover {
                    border: 2px solid #cc0000;
                }
                QComboBox::drop-down {
                    subcontrol-origin: padding;
                    subcontrol-position: top right;
                    background-color: rgb(248, 242, 242);
                    border: none;
                    border-top-right-radius: 15px;
                    border-bottom-right-radius: 15px;
                    width: 30px;
                    margin-right: 5px;
                }
            """)

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
            # Get the selected professor name from combo box
            selected_name = self.ui.input_professor_uinfo.currentText().strip()

            # Retrieve the professor ID from the mapping
            professor_id = self.professor_id_map.get(selected_name)

            if professor_id is None:
                self.show_warning("Format Error", "Could not find professor ID for the selected name.")
                return

            exist = fetchBorrower(self.studentInfo[0])
            if exist:
                print("Already Exists")
            else:
                student = {
                    "borrowerId": self.studentInfo[0],
                    "profId": professor_id,
                    "fname": self.studentInfo[2],
                    "lname": self.studentInfo[3],
                    "program": self.studentInfo[4],
                    "yearlevel": self.studentInfo[5]
                }
                res = addBorrower(student)
                if res == 1:
                    print("Already Exists")
                elif res == 0:
                    print("Added Successfully")



    


    def studentidformat(self, student_id):
        return bool(re.match(r'^\d{4}-\d{4}$', student_id))
       
    def studentnameformat(self, first_name, last_name):
        return bool(re.match(r'^[a-zA-Z ]+$', first_name)) and bool(re.match(r'^[a-zA-Z ]+$', last_name))
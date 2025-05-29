from .EquipmentManager_CSM import Ui_MainWindow
from PyQt6 import QtWidgets
import re
from ..modules.fetchData import fetchBorrower
from ..modules.add import addBorrower
from ..modules.fetchData import fetchBorrower

class Confirmation:
    def __init__(self, ui: Ui_MainWindow):
        self.ui = ui
        self.parent_widget = self.ui.centralwidget
        self.ui.next_button_additem.clicked.connect(self.User_Table_Inputs)
        self.ui.submit_confirmation.clicked.connect(self.submitConfirm)
        self.studentInfo = []


    def show_warning(self, title, message):
        QtWidgets.QMessageBox.warning(self.parent_widget, title, message)
    
    def user_input_fields(self):
        student_id = self.ui.input_idno_uinfo.text().strip()
        professor = self.ui.input_professor_uinfo.text().strip()

        if not student_id or not professor:
            self.show_warning("Input Error", "All fields must be filled out.")
            return False

        if not self.studentidformat(student_id):
            self.show_warning("Input Error", "Invalid Student ID format. Must be YYYY-NNNN.")
            return False
        
        student = fetchBorrower(student_id)
        if not student:
            self.show_warning("Does not Exist", "Student Does not Exist")
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
        states = []
        
        has_damaged_column = self.ui.Item_table.columnCount() > 3
        
        for row in range(self.ui.Item_table.rowCount()):
            item_item = self.ui.Item_table.item(row, 0)
            
            spinbox_default = self.ui.Item_table.cellWidget(row, 2)
            spinbox_damaged = self.ui.Item_table.cellWidget(row, 3) if has_damaged_column else None
            
            if item_item:
                item_name = item_item.text().strip()
                
                if spinbox_default and spinbox_default.value() > 0:
                    item_names.append(item_name)
                    quantities.append(spinbox_default.value())
                    states.append(0 if has_damaged_column else None)
                    item_details.append(f"{item_name} (Returned): {spinbox_default.value()}")
                    
                if has_damaged_column and spinbox_damaged and spinbox_damaged.value() > 0:
                    item_names.append(item_name)
                    quantities.append(spinbox_damaged.value())
                    states.append(3)
                    item_details.append(f"{item_name} (Damaged): {spinbox_damaged.value()}")

        item_summary = "\n".join(item_details) if item_details else "No items selected"
        self.ui.textEdit.setPlainText(item_summary)
        
        print(f"Extracted names: {item_names}")
        print(f"Quantities: {quantities}")
        print(f"States: {states}")
        
        return item_names, quantities, states
    
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

 
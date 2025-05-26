from .EquipmentManager_CSM import Ui_MainWindow
from PyQt6 import QtWidgets
import re

class Confirmation:
    def __init__(self, ui: Ui_MainWindow):
        self.ui = ui
        self.parent_widget = self.ui.centralwidget

    
    def show_warning(self, title, message):
        QtWidgets.QMessageBox.warning(self.parent_widget, title, message)
    
    
    
    def user_input_fields(self):
        student_id = self.ui.idno_uinfo.text().strip()
        first_name = self.ui.first_name_uinfo.text().strip()
        last_name = self.ui.last_name_uinfo.text().strip()
        section = self.ui.section_uinfo.text().strip()
        program = self.ui.program_uinfo.text().strip()
        professor = self.ui.professor_uinfo.text().strip()

        if not student_id or not first_name or not last_name or not section or not program or not professor:
            self.show_warning("Input Error", "All fields must be filled out.")
            return False

        if not self.studentidformat(student_id):
            self.show_warning("Input Error", "Invalid Student ID format. Must be YYYY-NNNN.")
            return False

        if not self.studentnameformat(first_name, last_name):
            self.show_warning("Input Error", "First name and last name must contain only letters.")
            return False
        
        self.ui.label_3.setText(student_id)
        self.ui.label_7.setText(first_name)
        self.ui.label_8.setText(last_name)
        self.ui.label_6.setText(section)
        self.ui.label_5.setText(program)
        self.ui.label_4.setText(professor)

        return True
    
    def User_Table_Inputs(self):
        item_details = []
        for row in range(self.ui.Item_table.rowCount()):
            item_item = self.ui.Item_table.item(row, 0)
            qty_widget = self.ui.Item_table.cellWidget(row, 2)
            if item_item and qty_widget and isinstance(qty_widget, QtWidgets.QSpinBox):
                item_name = item_item.text()
                quantity = qty_widget.value()
                if quantity > 0:
                    item_details.append(f"{item_name}: {quantity}")

        item_summary = "\n".join(item_details) if item_details else "No items selected"
        self.ui.textEdit.setPlainText(item_summary)
    

    def studentidformat(self, student_id):
        return bool(re.match(r'^\d{4}-\d{4}$', student_id))
       
    def studentnameformat(self, first_name, last_name):
        return bool(re.match(r'^[a-zA-Z ]+$', first_name)) and bool(re.match(r'^[a-zA-Z ]+$', last_name))

 
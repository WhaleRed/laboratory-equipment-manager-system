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
            self.ui.input_professor_uinfo.setEditable(True)
            professors = fetch_all_professor_names()  # list of tuples (id, full_name)
            self.ui.input_professor_uinfo.clear()
            self.ui.input_professor_uinfo.addItem("")
            self.professor_id_map = {}

            for prof_id, full_name in professors:
                display_text = f"{prof_id} - {full_name}"
                self.ui.input_professor_uinfo.addItem(display_text, userData=prof_id)
                self.professor_id_map[display_text] = prof_id

            # Use the full combo box item texts for completer
            completer_strings = [f"{prof_id} - {full_name}" for prof_id, full_name in professors]
            completer = QCompleter(completer_strings)
            completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            completer.setFilterMode(Qt.MatchFlag.MatchContains)
            
            self.ui.input_professor_uinfo.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
            self.ui.input_professor_uinfo.lineEdit().setPlaceholderText("Search Professor by Name or ID")
            self.ui.input_professor_uinfo.setCompleter(completer)

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

    def on_professor_text_changed(self, text):
        # Try to find the first item that contains the text (case insensitive)
        for i in range(self.ui.input_professor_uinfo.count()):
            item_text = self.ui.input_professor_uinfo.itemText(i)
            if text.lower() in item_text.lower():
                self.ui.input_professor_uinfo.setCurrentIndex(i)
                return

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
                    if has_damaged_column:
                        states.append(0)      
                        item_details.append(f"{item_name} (Returned): {spinbox_default.value()}")
                    else:
                        states.append(None)      
                        item_details.append(f"{item_name}: {spinbox_default.value()}")
                
                    
                if has_damaged_column and spinbox_damaged and spinbox_damaged.value() > 0:
                    item_names.append(item_name)
                    quantities.append(spinbox_damaged.value())
                    states.append(3)
                    item_details.append(f"{item_name} (Damaged): {spinbox_damaged.value()}")

        item_summary = "\n".join(item_details) if item_details else "No items selected"
        self.ui.textEdit.setPlainText(item_summary)
        
        return item_names, quantities, states
    
    def submitConfirm(self):
        if self.studentInfo:
            index = self.ui.input_professor_uinfo.currentIndex()
            professor_id = self.ui.input_professor_uinfo.itemData(index)

            if professor_id is None:
                self.show_warning("Selection Error", "Please select a valid professor.")
                return

    def studentidformat(self, student_id):
        return bool(re.match(r'^\d{4}-\d{4}$', student_id))
       
    def studentnameformat(self, first_name, last_name):
        return bool(re.match(r'^[a-zA-Z ]+$', first_name)) and bool(re.match(r'^[a-zA-Z ]+$', last_name))
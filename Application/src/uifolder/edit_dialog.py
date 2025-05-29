from PyQt6.QtWidgets import QDialog, QMessageBox
from .EquipmentManager_AddDialog import Add_Dialog
from src.modules.edit import editEquipment
from src.modules.generateID import generate_equipment_id

class editDialog(QDialog):
    def __init__(self, parent=None, itemData = None):
        super().__init__(parent)
        self.ui = Add_Dialog()
        self.ui.setupUi(self)
        self.addButtons()
        self.populateComboBoxes()
        self.setupComboBoxes()
        self.item_data = itemData or []
        self.ui.comboBox.setCurrentText(str(self.item_data[0][1]))
        self.ui.comboBox_2.setCurrentText(str(self.item_data[0][3]))
        self.ui.Quantity_spinbox_4.setValue(int(self.item_data[0][2]))
        self.ui.Add_item_button_newitem.setText("Edit")
        self.ui.Add_New_Item_Text_4.setText("Edit Item")



    def setupComboBoxes(self):
        """Configure combo boxes to be editable"""
        # Make equipment name combo box editable
        self.ui.comboBox.setEditable(True)
        self.ui.comboBox.setDuplicatesEnabled(False)  # Prevent duplicate entries
        
        # Make category combo box editable
        self.ui.comboBox_2.setEditable(True)
        self.ui.comboBox_2.setDuplicatesEnabled(False)  # Prevent duplicate entries
        
        # Optional: Set placeholder text
        self.ui.comboBox.lineEdit().setPlaceholderText("Select or enter equipment name")
        self.ui.comboBox_2.lineEdit().setPlaceholderText("Select or enter category")
    
    def populateComboBoxes(self):
        try:
            from src.modules.fetchData import fetchEquipmentName, fetchCategory
            
            # Populate equipment name combo box
            equipment_names = fetchEquipmentName()
            self.ui.comboBox.clear()  # Clear existing items
            self.ui.comboBox.addItems(equipment_names)
            
            # Populate category combo box
            categories = fetchCategory()
            self.ui.comboBox_2.clear()  # Clear existing items
            self.ui.comboBox_2.addItems(categories)
            
        except Exception as e:
            QMessageBox.critical(self, "Database Error", 
                               f"Failed to load data from database: {str(e)}")

    def addButtons(self):
        self.ui.Add_item_button_newitem.clicked.connect(self.saveEquipment)
        self.ui.Cancel_button_newitem.clicked.connect(self.close)

    def saveEquipment(self):
        result = None
        try:
            equipment_name = self.ui.comboBox.currentText().strip()
            quantity = self.ui.Quantity_spinbox_4.value()
            category = self.ui.comboBox_2.currentText().strip()
            currEquipID = self.item_data[0][0]
            # Generate Equipment ID
            equipment_id = generate_equipment_id(category, equipment_name)
            # Validate Inputs
            if not equipment_name:
                QMessageBox.warning(self, "Validation Error", "Equipment name is required.")
                return
            
            if quantity <= 0:
                QMessageBox.warning(self, "Validation Error", "Quantity must be greater than zero.")
                return
                
            if not category:
                QMessageBox.warning(self, "Validation Error", "Category is required.")
                return
            
            # Prepare equipment data
            equipment = {
                "new_equipId": equipment_id,
                "new_name": equipment_name,
                "new_quantity": quantity,
                "new_category": category,
                "current_equipId": currEquipID
            }

            # Call the addEquipment function (assuming it's defined elsewhere)
            reply = QMessageBox.question(
                self,
                "Confirm Action",
                "Do you want to proceed?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No  # Default button
            )

            if reply == QMessageBox.StandardButton.Yes:
              result = editEquipment(equipment)
            if result is not None:
              if result == 0:
                  if equipment_name not in [self.ui.comboBox.itemText(i) for i in range(self.ui.comboBox.count())]:
                      self.ui.comboBox.addItem(equipment_name)
          
                  if category not in [self.ui.comboBox_2.itemText(i) for i in range(self.ui.comboBox_2.count())]:
                      self.ui.comboBox_2.addItem(category)
                  QMessageBox.information(self, "Success", "Equipment edited successfully.")
                  self.accept()
              elif result == 1:
                  QMessageBox.warning(self, "Duplicate Error", "Equipment already exists.")
              elif result == 2:
                  QMessageBox.warning(self, "Edit Error", "Equipment ID is currently used.")
              else:
                  QMessageBox.critical(self, "Error", "An unexpected error occurred.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while saving the equipment: {str(e)}")
            self.close()  # Close the dialog in case of an error
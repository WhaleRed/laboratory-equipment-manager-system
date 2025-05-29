import sys
from src.modules import delete, edit, add, fetchData
from datetime import datetime    #Need ni siya for delete
from PyQt6.QtCore import Qt
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication
from src.uifolder.EquipmentManager_CSM import Ui_MainWindow
from src.uifolder.connectors import Connector
from src.uifolder.confirmation import Confirmation
from PyQt6 import QtWidgets, QtCore, QtGui
from functools import partial

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setupTableBehavior()
        
        self.connector = Connector(self)
        self.logic = Confirmation(self)
        
        self.pageNum = "1" #initial'
        self.total_pages = 1 # initial
        self.per_page = 10
        self.borrower_id = ""

        # For Scrollbar
        self.Item_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.Item_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        
        #for users page
        self.UpageNum = 1
        self.UtotalPages = 1
        self.spacer = "        "
        
        self.populateEquipmentTable()
        self.populateReturnTable()
        self.populateBorrowTable()
        self.populateReplaceTable()
        self.populateBorrowerTable()
        self.populateProfTable()
        
        self.update_button_state()
        
        self.Admin_User_Page.setCurrentIndex(0) # Set the initial page to the first tab
        self.User_Interactive_Page.setCurrentIndex(0) # Set the initial page to the first tab
        
        # Transaction connections
        self.searchbox_transaction.returnPressed.connect(self.populateCurrentTable) # change pa ni
        
        self.Date_box_borrow.currentIndexChanged.connect(lambda _: self.populateBorrowTable())
        self.Date_box_return.currentIndexChanged.connect(lambda _: self.populateReturnTable())
        self.Date_box_replace.currentIndexChanged.connect(lambda _: self.populateReplaceTable())
        
        self.arrow_right_borrow.clicked.connect(self.go_to_next_page)
        self.arrow_right_return.clicked.connect(self.go_to_next_page)
        self.arrow_right_replace.clicked.connect(self.go_to_next_page)
        
        self.arrow_left_borrow.clicked.connect(self.go_to_prev_page)
        self.arrow_left_return.clicked.connect(self.go_to_prev_page)
        self.arrow_left_replace.clicked.connect(self.go_to_prev_page)
        
        self.page_box_borow.returnPressed.connect(self.go_to_page)
        self.page_box_return.returnPressed.connect(self.go_to_page)
        self.Page_box_replace.returnPressed.connect(self.go_to_page)
        
        # Inventory connections
        self.searchbox_inventory.returnPressed.connect(self.populateEquipmentTable)
        self.category_box_inventory.currentIndexChanged.connect(self.populateEquipmentTable)
        self.sort_box_inventory.currentIndexChanged.connect(self.populateEquipmentTable)

        self.arrow_right.clicked.connect(self.go_to_next_page)
        self.arrow_left.clicked.connect(self.go_to_prev_page)
        self.page_box_inventory.returnPressed.connect(self.go_to_page)
        
        # Users connections
        self.searchbox_borrowers.returnPressed.connect(self.populateCurrentTable)
        
        self.Filter_box_Prof.currentIndexChanged.connect(self.populateProfTable)
        self.Filter_box_Students.currentIndexChanged.connect(self.populateBorrowerTable)
        
        self.arrow_right_Prof.clicked.connect(self.go_to_next_page)
        self.arrow_right_Students.clicked.connect(self.go_to_next_page)
        
        self.arrow_left_Prof.clicked.connect(self.go_to_prev_page)
        self.arrow_left_Students.clicked.connect(self.go_to_prev_page)
        
        self.page_box_Prof.returnPressed.connect(self.go_to_page)
        self.page_box_Students.returnPressed.connect(self.go_to_page)
        
        # ui updates
        self.Admin_Page.currentChanged.connect(self.onIndexChanged)
        self.Dashboard_Frame.currentChanged.connect(self.onIndexChanged)
        self.Dashboard_Frame_Borrowers.currentChanged.connect(self.onIndexChanged)
        
        #Add item connections
        self.next_button_uinfo.clicked.connect(self.setItemTableValues)
        self.borrow_button_user.clicked.connect(self.setModeBorrow)
        self.return_button_user.clicked.connect(self.setModeReturn)
        self.replace_button_user.clicked.connect(self.setModeReplace)
        self.addItemState = 2
        self.search_box.returnPressed.connect(self.setItemTableValues)
        self.category_box_additem.currentIndexChanged.connect(self.setItemTableValues)
        self.increment.clicked.connect(self.Ugo_to_next_page)
        self.decrement.clicked.connect(self.Ugo_to_prev_page)
        

        self.additem_button.clicked.connect(self.openAddItem)  # Add item button connection

        # Add professor connection
        self.addProfessor_button.clicked.connect(self.openProfessor)
        self.addborrower_button.clicked.connect(self.openBorrower)
        
        self.next_button_uinfo.clicked.connect(self.get_borrower_id)
        self.submit_confirmation.clicked.connect(self.get_item_id)

#-----Helper-----#

    def onIndexChanged(self):
      
      self.pageNum = "1"
      current_SWPage = self.Admin_Page.currentIndex()
      
      buttons = self.sidebar_buttons.findChildren(QtWidgets.QPushButton)
      desired_btn_index = {
          'borrow_button_sidebar': 0,
          'inventory_button_sidebar': 1,
          'user_button_sidebar': 2
      }
      
      for btn in buttons:
        btn_index = desired_btn_index.get(btn.objectName())
        if btn_index == current_SWPage:
            btn.setStyleSheet("""
                color: white;
                border-top-left-radius: 18px;
                border-bottom-left-radius: 18px;
                padding-top: 10px;
                padding-bottom: 10px;
                background-color: #7a0000;  /* Dark red */
            """)
        else:
            btn.setStyleSheet("""
                color: white;
                border-top-left-radius: 18px;
                border-bottom-left-radius: 18px;
                padding-top: 10px;
                padding-bottom: 10px;
                background-color: #A70000;  /* Default red */
            """)
    
      
      match current_SWPage:
          case 0:
              current_tab_index = self.Dashboard_Frame.currentIndex()
              
              match current_tab_index:
                  case 0:  # borrow table
                      self.populateBorrowTable()
                  case 1:  # return table
                      self.populateReturnTable()
                  case 2:  # replace table
                      self.populateReplaceTable()
                  case _:
                      print("Unknown table index")
          case 1:
              self.populateEquipmentTable()
          case 2:
              current_tab_index = self.Dashboard_Frame_Borrowers.currentIndex()
              match current_tab_index:
                case 0:
                  self.populateProfTable()
                case 1:
                  self.populateBorrowerTable()
          case _:
              print(f"Unknown admin page index: {current_SWPage}")
              
      self.update_button_state()

    def populateCurrentTable(self):
      
        currentSWpage = self.Admin_Page.currentIndex()
        
        match currentSWpage:
          case 0:
            current_tab_index = self.Dashboard_Frame.currentIndex()
            match current_tab_index:
              case 0:  
                  self.populateBorrowTable()
              case 1:  
                  self.populateReturnTable()
              case 2:  
                  self.populateReplaceTable()
              case _:
                  print("Unknown table index")
          case 2:
            current_tab_index = self.Dashboard_Frame_Borrowers.currentIndex()
            match current_tab_index:
              case 0:
                self.populateProfTable()
              case 1:
                self.populateBorrowerTable()
            
    def createOptionsButtonED(self, id):
        btn = QtWidgets.QPushButton("    ⋮ ")
        btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        
        btn.setStyleSheet("text-align: center;")
        btn.setStyleSheet("""
                          font-weight: bold;
                          font-size: 12pt;
                          padding: 0;
                          """)
        btn.setFixedSize(50, 50)

        menu = QtWidgets.QMenu(btn)
        edit_action = QtGui.QAction("Edit", self)
        delete_action = QtGui.QAction("Delete", self)
        menu.addAction(edit_action)
        menu.addAction(delete_action)
        
        menu.setStyleSheet("""
                        QMenu {
                            background-color: #f0f0f0;     
                            border: 1px solid #b22222;    
                            padding: 0px;                  
                        }
                        QMenu::item:selected {            
                            background-color: #b22222;      
                            color: white;
                        }
                        """)

        edit_action.triggered.connect(partial(self.editRow, id))
        delete_action.triggered.connect(partial(self.deleteRow, id))

        btn.setMenu(menu)

        return btn
      
    def createOptionsButtonD(self, id):
        btn = QtWidgets.QPushButton("    ⋮ ")
        btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        
        btn.setStyleSheet("""
                          font-weight: bold;
                          font-size: 12pt;
                          padding: 0;
                          """)
        btn.setFixedSize(50, 50)

        menu = QtWidgets.QMenu(btn)
        delete_action = QtGui.QAction("Delete", self)
        menu.addAction(delete_action)
        
        menu.setStyleSheet("""
                        QMenu {
                            background-color: #f0f0f0;     
                            border: 1px solid #b22222;    
                            padding: 0px;                  
                        }
                        QMenu::item:selected {            
                            background-color: #b22222;      
                            color: white;
                        }
                        """)

        delete_action.triggered.connect(partial(self.deleteRow, id))

        btn.setMenu(menu)

        return btn
      
    def createQuantitySpinBox(self, max_quantity):
        spinbox = QtWidgets.QSpinBox()
        spinbox.setMinimum(0)
        spinbox.setMaximum(max_quantity)
        spinbox.setValue(0)  # default selected quantity
        return spinbox

    def setModeBorrow(self):
        self.addItemState = 2
        self.setItemTableValues()
    
    def setModeReturn(self):
        self.addItemState = 0
        self.setItemTableValues()
        
    def setModeReplace(self):
        self.addItemState = 1
        self.setItemTableValues()
      
    def get_borrower_id(self):
        self.borrower_id = self.input_idno_uinfo.text().strip()
      
    def get_item_id(self):
      try:
        item_names, quantities = self.logic.User_Table_Inputs()
        
        for name, qty in zip(item_names, quantities):
            clean_name = (name.strip(),)
            item_id_tup = fetchData.fetch_itemID_from_name(clean_name)
            item_id = item_id_tup[0]
            print(f"id: {item_id}")
            print(f"qty: {qty}")
            self.add_transaction_to_db(item_id, qty)
      except Exception as e:
        print(f"error grtting item id: {e}")
            
    def add_transaction_to_db(self, id, quantity):
      try:
        print("Addiing transaction...")
        mode = self.addItemState
        
        if mode == 0:
            add.addReturnedEquipment(id, self.borrower_id, "Returned", quantity) #needs to change to accomodate multiple item state
            edit.updateEquipmentQuantity(id, quantity, mode)
        elif mode == 1:
            print("adding")
            add.addReplacedEquipment(id, self.borrower_id, quantity)
            edit.updateEquipmentQuantity(id, quantity, mode) # change to update damaged in returned table
        elif mode == 2:
            add.addBorrowedEquipment(id, self.borrower_id, 'In use', quantity)
            edit.updateEquipmentQuantity(id, quantity, mode)
        
      except Exception as e:
        print(f"Error in add_transaction_to_db: {e}")
            
#-----Populates admin tables-----#

    def populateEquipmentTable(self):
        try:

            sortState = self.sort_box_inventory.currentIndex() or 0
            catState = self.category_box_inventory.currentIndex() or 0
            
            searchKeyword = self.searchbox_inventory.text().strip()
            
            data = []
            page = int(self.pageNum)
            
            self.inventory_table.clearContents()
            
            if sortState is None:
                sortState = 0
            
            if searchKeyword:
                data, count = fetchData.searchEquipmentMatch(page, sortState, catState, searchKeyword)
            else:
                data, count = fetchData.searchEquipmentMatch(page, sortState, catState)
            
            self.page_box_inventory.setText(f"{self.pageNum}")
            
            self.total_pages = (count // self.per_page) + (1 if count % self.per_page != 0 else 0)
            
            self.ofTotal_Pages_inventory.setText(f"of {self.total_pages}")

            self.inventory_table.setRowCount(len(data))
            for row, item in enumerate(data):
                self.inventory_table.setItem(row, 0, QtWidgets.QTableWidgetItem(f"{self.spacer}{item[0]}"))
                self.inventory_table.setItem(row, 1, QtWidgets.QTableWidgetItem(f"{self.spacer}{item[1]}"))
                self.inventory_table.setItem(row, 2, QtWidgets.QTableWidgetItem(f"{self.spacer}{item[2]}"))
                self.inventory_table.setItem(row, 3, QtWidgets.QTableWidgetItem(f"{self.spacer}{item[3]}"))
                
                btn = self.createOptionsButtonED(item[0])
                self.inventory_table.setCellWidget(row, 4, btn)
                
        except Exception as e:
            print(f"Error in populateEquipmentTable: {e}")

    def populateBorrowTable(self):
        try:
            sortState = self.Filter_box_borrow.currentIndex() or 0
            dateState = self.Date_box_borrow.currentIndex() or 0
            
            searchKeyword = self.searchbox_transaction.text().strip()
            
            data = []
            page = int(self.pageNum)
            
            self.borrow_table.clearContents()
            
            if searchKeyword:
                data, count = fetchData.searchBorrowedEquipmentMatch(page, sortState, dateState, searchKeyword)
            else:
                data, count = fetchData.searchBorrowedEquipmentMatch(page, sortState, dateState)

            self.page_box_borow.setText(f"{self.pageNum}")
                
            self.total_pages = (count // self.per_page) + (1 if count % self.per_page != 0 else 0)
            self.ofTotal_Pages_borrow.setText(f"of {self.total_pages}")

            self.borrow_table.setRowCount(len(data))
            for row, item in enumerate(data):
                self.borrow_table.setItem(row, 0, QtWidgets.QTableWidgetItem(f"{self.spacer}{item[0]}"))
                self.borrow_table.setItem(row, 1, QtWidgets.QTableWidgetItem(f"{self.spacer}{item[1]}"))
                self.borrow_table.setItem(row, 2, QtWidgets.QTableWidgetItem(f"{self.spacer}{item[2]}"))
                self.borrow_table.setItem(row, 3, QtWidgets.QTableWidgetItem(f"{self.spacer}{item[4]}"))
                self.borrow_table.setItem(row, 4, QtWidgets.QTableWidgetItem(f"{self.spacer}{item[3]}"))
                
                key = (item[0], item[1], item[2])
                btn = self.createOptionsButtonD(key)
                self.borrow_table.setCellWidget(row, 5, btn)
                
        except Exception as e:
            print(f"Error in populateBorrowTable: {e}")

    def populateReturnTable(self):
        try:
            
            sortState = self.Filter_box_return.currentIndex() or 0
            dateState = self.Date_box_return.currentIndex() or 0
            
            searchKeyword = self.searchbox_transaction.text().strip()
            
            data = []
            page = int(self.pageNum)
            
            self.return_table.clearContents()
            
            if sortState is None:
                sortState = 0

            if searchKeyword:
                data, count = fetchData.searchReturnedEquipmentMatch(page, sortState, dateState, searchKeyword)
            else:
                data, count = fetchData.searchReturnedEquipmentMatch(page, sortState, dateState)
            
            self.page_box_return.setText(f"{self.pageNum}")
            
            self.total_pages = (count // self.per_page) + (1 if count % self.per_page != 0 else 0)
            self.ofTotal_Pages_return.setText(f"of {self.total_pages}")

            self.return_table.setRowCount(len(data))
            for row, item in enumerate(data):
                self.return_table.setItem(row, 0, QtWidgets.QTableWidgetItem(f"{self.spacer}{item[0]}"))
                self.return_table.setItem(row, 1, QtWidgets.QTableWidgetItem(f"{self.spacer}{item[1]}"))
                self.return_table.setItem(row, 2, QtWidgets.QTableWidgetItem(f"{self.spacer}{item[2]}"))
                self.return_table.setItem(row, 3, QtWidgets.QTableWidgetItem(f"{self.spacer}{item[4]}"))
                self.return_table.setItem(row, 4, QtWidgets.QTableWidgetItem(f"{self.spacer}{item[3]}"))
                
                key = (item[0], item[1], item[2])
                btn = self.createOptionsButtonD(key)
                self.return_table.setCellWidget(row, 5, btn)
                
        except Exception as e:
            print(f"Error in populateReturnTable: {e}")
                    
    def populateReplaceTable(self):
        try:
            sortState = self.Filter_box_replace.currentIndex() or 0
            dateState = self.Date_box_replace.currentIndex() or 0
            
            searchKeyword = self.searchbox_transaction.text().strip()
            
            data = []
            page = int(self.pageNum)
            
            self.replace_table.clearContents()

            if searchKeyword:
                data, count = fetchData.searchReplacedEquipmentMatch(page, sortState, dateState, searchKeyword)
            else:
                data, count = fetchData.searchReplacedEquipmentMatch(page, sortState, dateState)
            
            self.Page_box_replace.setText(f"{self.pageNum}")
                
            self.total_pages = (count // self.per_page) + (1 if count % self.per_page != 0 else 0)
            self.ofTotal_Pages_replace.setText(f"of {self.total_pages}")
        
            self.replace_table.setRowCount(len(data))
            for row, item in enumerate(data):
                self.replace_table.setItem(row, 0, QtWidgets.QTableWidgetItem(f"{self.spacer}{item[0]}"))
                self.replace_table.setItem(row, 1, QtWidgets.QTableWidgetItem(f"{self.spacer}{item[1]}"))
                self.replace_table.setItem(row, 2, QtWidgets.QTableWidgetItem(f"{self.spacer}{item[2]}"))
                self.replace_table.setItem(row, 3, QtWidgets.QTableWidgetItem(f"{self.spacer}{item[3]}"))
                
                key = (item[0], item[1], item[2])
                btn = self.createOptionsButtonD(key)
                self.replace_table.setCellWidget(row, 4, btn)
            
        except Exception as e:
            print(f"Error in populateReplaceTable: {e}")
            
    def populateBorrowerTable(self):
      try:
          sortState = self.Filter_box_Students.currentIndex() or 0
          
          searchKeyword = self.searchbox_borrowers.text().strip()
          
          data = []
          page = int(self.pageNum)
          
          self.Students_table.clearContents()

          if searchKeyword:
              data, count = fetchData.searchBorrowerMatch(page, sortState, searchKeyword)
          else:
              data, count = fetchData.searchBorrowerMatch(page, sortState)
          
          self.page_box_Students.setText(f"{self.pageNum}")
              
          self.total_pages = (count // self.per_page) + (1 if count % self.per_page != 0 else 0)
          self.ofTotal_Pages_Students.setText(f"of {self.total_pages}")
          
          self.Students_table.setRowCount(len(data))
          for row, item in enumerate(data):
              self.Students_table.setItem(row, 0, QtWidgets.QTableWidgetItem(f"{self.spacer}{item[0]}"))
              self.Students_table.setItem(row, 1, QtWidgets.QTableWidgetItem(f"{self.spacer}{item[2]}"))
              self.Students_table.setItem(row, 2, QtWidgets.QTableWidgetItem(f"{self.spacer}{item[3]}"))
              self.Students_table.setItem(row, 3, QtWidgets.QTableWidgetItem(f"{self.spacer}{item[4]}"))
              self.Students_table.setItem(row, 4, QtWidgets.QTableWidgetItem(f"{self.spacer}        {item[5]}"))
              self.Students_table.setItem(row, 5, QtWidgets.QTableWidgetItem(f"{self.spacer}{item[1]}"))
              
              btn = self.createOptionsButtonED(item[0])
              self.Students_table.setCellWidget(row, 6, btn)
              
      except Exception as e:
            print(f"Error in populateBorrowerTable: {e}")
            
    def populateProfTable(self):
      try:
          sortState = self.Filter_box_Prof.currentIndex() or 0
          
          searchKeyword = self.searchbox_borrowers.text().strip()
          
          data = []
          page = int(self.pageNum)
          
          self.Professors_table.clearContents()

          if searchKeyword:
              data, count = fetchData.searchProfessorMatch(page, sortState, searchKeyword)
          else:
              data, count = fetchData.searchProfessorMatch(page, sortState)
          
          self.page_box_Prof.setText(f"{self.pageNum}")
              
          self.total_pages = (count // self.per_page) + (1 if count % self.per_page != 0 else 0)
          self.ofTotal_Pages_Prof.setText(f"of {self.total_pages}")
          
      
          self.Professors_table.setRowCount(len(data))
          for row, item in enumerate(data):
              self.Professors_table.setItem(row, 0, QtWidgets.QTableWidgetItem(f"{self.spacer}{item[0]}"))
              self.Professors_table.setItem(row, 1, QtWidgets.QTableWidgetItem(f"{self.spacer}{item[1]}"))
              self.Professors_table.setItem(row, 2, QtWidgets.QTableWidgetItem(f"{self.spacer}{item[2]}"))
              
              btn = self.createOptionsButtonED(item[0])
              self.Professors_table.setCellWidget(row, 3, btn)
              
              btn = self.createOptionsButtonED(item[0])
              self.Professors_table.setCellWidget(row, 3, btn)
              
      except Exception as e:
            print(f"Error in populateBorrowerTable: {e}")
      
#-----Edit and Delete functions-----#

    def editRow(self, id):
        res = None
        current_SWPage = self.Admin_Page.currentIndex()

        match current_SWPage:
            case 0:
                field = "transaction"
                current_tab_index = self.Dashboard_Frame.currentIndex()
                match current_tab_index:
                    case 0:
                        res = delete.delBorrowedEquipment(id)
                        self.populateBorrowTable()
                    case 1:
                        res = delete.delReturnedEquipment(id)
                        self.populateReturnTable()
                    case 2:
                        res = delete.delReplacedEquipment(id)
                        self.populateReplaceTable()
            case 1:
                field = "equipment"
                res = delete.delEquipment(id)
                self.populateEquipmentTable()
            case 2:
                current_tab_index = self.Dashboard_Frame_Borrowers.currentIndex()
                match current_tab_index:
                    case 0:   #Edit for prof table
                        field = "professor"
                        curDataProf = fetchData.fetchProfessor(id)
                        self.editOpenProfessor(curDataProf)
                    case 1:   #Edit for borrower table
                        field = "borrower"
                        curDataBorrower = fetchData.fetchBorrower(id)
                        self.editOpenBorrower(curDataBorrower)
        if res is not None:
            if res == 1:              
                QtWidgets.QMessageBox.warning(
                                self,
                                "Edit Failed",
                                f"This {field} cannot be edited because it is referenced in another table."
                            )
            else:
                QtWidgets.QMessageBox.information(
                                self,
                                "Edit Succesful",
                                f"This {field} has been edited."
                            )
        
    def deleteRow(self, id):
        res = None
        current_SWPage = self.Admin_Page.currentIndex()

        match current_SWPage:
            case 0:
                field = "transaction"
                current_tab_index = self.Dashboard_Frame.currentIndex()
                match current_tab_index:
                    case 0:
                        confirm = QtWidgets.QMessageBox.question(
                                self,
                                "Confirm Deletion",
                                f"Are you sure about deleting this {field}?",
                                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
                                QtWidgets.QMessageBox.StandardButton.No
                            )  
                        if confirm == QtWidgets.QMessageBox.StandardButton.Yes:
                            res = delete.delBorrowedEquipment(id)
                            self.populateBorrowTable()
                    case 1:
                        confirm = QtWidgets.QMessageBox.question(
                                self,
                                "Confirm Deletion",
                                f"Are you sure about deleting this {field}?",
                                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
                                QtWidgets.QMessageBox.StandardButton.No
                            )  
                        if confirm == QtWidgets.QMessageBox.StandardButton.Yes:
                            res = delete.delReturnedEquipment(id)
                            self.populateReturnTable()
                    case 2:
                        confirm = QtWidgets.QMessageBox.question(
                                self,
                                "Confirm Deletion",
                                f"Are you sure about deleting this {field}?",
                                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
                                QtWidgets.QMessageBox.StandardButton.No
                            )  
                        if confirm == QtWidgets.QMessageBox.StandardButton.Yes:
                            res = delete.delReplacedEquipment(id)
                            self.populateReplaceTable()
            case 1:
                field = "equipment"
                res = delete.delEquipment(id)
                self.populateEquipmentTable()
            case 2:
                current_tab_index = self.Dashboard_Frame_Borrowers.currentIndex()
                match current_tab_index:
                    case 0:   #Delete for prof table
                        field = "professor"
                        confirm = QtWidgets.QMessageBox.question(
                                self,
                                "Confirm Deletion",
                                f"Are you sure about deleting this {field}?",
                                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
                                QtWidgets.QMessageBox.StandardButton.No
                            )  
                        if confirm == QtWidgets.QMessageBox.StandardButton.Yes:
                            res = delete.delProfessor(id)
                            self.populateProfTable()
                    case 1:   #Delete for borrower table
                        field = "student"
                        confirm = QtWidgets.QMessageBox.question(
                                self,
                                "Confirm Deletion",
                                f"Are you sure about deleting this {field}?",
                                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
                                QtWidgets.QMessageBox.StandardButton.No
                            )  
                        if confirm == QtWidgets.QMessageBox.StandardButton.Yes:
                            res = delete.delBorrower(id)
                            self.populateBorrowerTable()
        if res is not None:
            if res == 1:              
                QtWidgets.QMessageBox.warning(
                                self,
                                "Delete Failed",
                                f"This {field} cannot be deleted because it is referenced in another table."
                            )
            else:
                QtWidgets.QMessageBox.information(
                                self,
                                "Delete Succesful",
                                f"This {field} has been deleted."
                            )
        
#-----Page navigation-----# 
    
    def go_to_next_page(self):
        try:
            current_SWPage = self.Admin_Page.currentIndex()
            
            current_page = int(self.pageNum)
            current_page += 1
            self.pageNum = str(current_page)
            
            print(f"page num: {current_page}")
            
            match current_SWPage:
                case 0:
                    current_tab_index = self.Dashboard_Frame.currentIndex()
                    match current_tab_index:
                        case 0:  # borrow table
                            self.populateBorrowTable()
                        case 1:  # return table
                            self.populateReturnTable()
                        case 2:  # replace table
                            self.populateReplaceTable()
                        case _:
                            print("Unknown table index")
                case 1:
                    self.populateEquipmentTable()
                case 2:
                    current_tab_index = self.Dashboard_Frame_Borrowers.currentIndex()
                    match current_tab_index:
                      case 0:
                        self.populateProfTable()
                      case 1:
                        self.populateBorrowerTable()
                case _:
                    print(f"Unknown admin page index: {current_SWPage}")
                            
            self.update_button_state()
        except Exception as e:
            print(f"Error in go_to_next_page: {e}")

    def go_to_prev_page(self):
        try:
            current_SWPage = self.Admin_Page.currentIndex()
            
            current_page = int(self.pageNum)
            current_page -= 1
            self.pageNum = str(current_page)

            match current_SWPage:
                case 0:
                    current_tab_index = self.Dashboard_Frame.currentIndex()
                    match current_tab_index:
                        case 0:  # borrow table
                            self.populateBorrowTable()
                        case 1:  # return table
                            self.populateReturnTable()
                        case 2:  # replace table
                            self.populateReplaceTable()
                        case _:
                            print("Unknown table index")
                case 1: 
                    self.populateEquipmentTable()
                case 2:
                    current_tab_index = self.Dashboard_Frame_Borrowers.currentIndex()
                    match current_tab_index:
                      case 0:
                        self.populateProfTable()
                      case 1:
                        self.populateBorrowerTable()
                case _:
                    print("Unknown admin page index")
                
            self.update_button_state()
        except Exception as e:
            print(f"Error in go_to_prev_page: {e}")
    
    def go_to_page(self):
        try:
            current_SWPage = self.Admin_Page.currentIndex()
            
            match current_SWPage:
                case 0:
                    current_tab_index = self.Dashboard_Frame.currentIndex()
                    match current_tab_index:
                        case 0:  # borrow table
                            page_input = self.page_box_borow.text().strip() 
                        case 1:  # return table
                            page_input = self.page_box_return.text().strip()  
                        case 2:  # replace table
                            page_input = self.Page_box_replace.text().strip()  
                        case _:
                            print("Unknown table index")
                            return
                case 1:
                    page_input = self.page_box_inventory.text().strip()
                case 2: 
                    current_tab_index = self.Dashboard_Frame_Borrowers.currentIndex()
                    match current_tab_index:
                        case 0:
                          page_input = self.page_box_Prof.text().strip() 
                        case 1:
                          page_input = self.page_box_Students.text().strip() 
                case _:
                    print("Unknown admin page index")
                    return

            if page_input.isdigit():
                page = int(page_input)
                if 1 <= page <= self.total_pages:
                    self.pageNum = str(page)
                    
                    match current_SWPage:
                        case 0:
                            current_tab_index = self.Dashboard_Frame.currentIndex()
                            match current_tab_index:
                                case 0:  # borrow table
                                    self.populateBorrowTable()
                                case 1:  # return table
                                    self.populateReturnTable()
                                case 2:  # replace table
                                    self.populateReplaceTable()
                                case _:
                                    print("Unknown table index")
                        case 1: 
                            self.populateEquipmentTable()
                        case 2:
                            current_tab_index = self.Dashboard_Frame_Borrowers.currentIndex()
                            match current_tab_index:
                              case 0:
                                self.populateProfTable()
                              case 1:
                                self.populateBorrowerTable()
                              case _:
                                  print("Unknown table page index")
                      
                    self.update_button_state()
                else:
                    print(f"Invalid page number: {page_input}")
                    self.clear_page_input(current_tab_index)
            else:
                print("Invalid input. Please enter a valid page number.")
                self.clear_page_input(current_tab_index)

        except Exception as e:
            print(f"Error in go_to_page: {e}")
            # Clear the QLineEdit in case of error
            self.clear_page_input(current_tab_index)

    def clear_page_input(self, tab_index):
        current_SWPage = self.Admin_Page.currentIndex()
        
        match current_SWPage:
            case 0:
                match tab_index:
                    case 0:
                        self.page_box_borow.clear()
                    case 1:
                        self.page_box_return.clear()
                    case 2:
                        self.Page_box_replace.clear()
                    case _:
                        print("Unknown tab index. Could not clear page input.")
            case 1:
                self.page_box_inventory.clear()
            case 2:
              match tab_index:
                    case 0:
                      self.page_box_Prof()
                    case 1:
                      self.page_box_Students()
            case _:
                print("Unknown admin page index")

    def update_button_state(self):
        try:
            current_SWPage = self.Admin_Page.currentIndex() 
            current_page = int(self.pageNum) 
            total_pages = self.total_pages
            
            match current_SWPage:
                case 0:
                    current_tab_index = self.Dashboard_Frame.currentIndex()
                    match current_tab_index:
                        case 0:  # borrow table    
                            self.arrow_left_borrow.setEnabled(current_page > 1)
                            self.arrow_right_borrow.setEnabled(current_page < total_pages)
                        case 1:  # return table
                            self.arrow_left_return.setEnabled(current_page > 1)
                            self.arrow_right_return.setEnabled(current_page < total_pages)
                        case 2:  # replace table
                            self.arrow_left_replace.setEnabled(current_page > 1)
                            self.arrow_right_replace.setEnabled(current_page < total_pages)
                        case _:
                            print("Unknown table index")
                            return
                case 1:
                    self.arrow_left.setEnabled(current_page > 1)
                    self.arrow_right.setEnabled(current_page < total_pages)
                case 2:
                  current_tab_index = self.Dashboard_Frame_Borrowers.currentIndex()
                  match current_tab_index:
                    case 0:
                      self.arrow_left_Prof.setEnabled(current_page > 1)
                      self.arrow_right_Prof.setEnabled(current_page < total_pages)
                    case 1:
                      self.arrow_left_Students.setEnabled(current_page > 1)
                      self.arrow_right_Students.setEnabled(current_page < total_pages)
                case _:
                    print("Unknown admin page index")  
        except Exception as e:
            print(f"Error in update_button_state: {e}")

    def Ugo_to_next_page(self):
      current_page = self.UpageNum
      current_page += 1
      self.UpageNum = current_page
      print(f"page: {self.UpageNum}")
      
      self.setItemTableValues()
      print("n done populating")
      
    def Ugo_to_prev_page(self):
      current_page = self.UpageNum
      current_page -= 1
      self.UpageNum = current_page
      
      print(f"page: {self.UpageNum}")
      
      self.setItemTableValues()
      print("n done populating")

    def Uupdate_pageNumber(self):
      self.Page.setText(f"{self.UpageNum} of {self.UtotalPages}")  # page _ of _
      self.decrement.setEnabled(self.UpageNum > 1)
      self.increment.setEnabled(self.UpageNum < self.UtotalPages)

#-----Add item-----#
    def setItemTableValues(self):
        try:
            self.Uupdate_pageNumber()

            page = self.UpageNum
            category = self.category_box_additem.currentIndex()
            searchKeyword = self.search_box.text().strip()

            self.Item_table.clearContents()

            if self.addItemState == 0:
                data, count = fetchData.fetchItemsInUse(self.input_idno_uinfo.text(), page, category, searchKeyword)
                self.UtotalPages = (count // self.per_page) + (1 if count % self.per_page != 0 else 0)
                self.Uupdate_pageNumber()

            elif self.addItemState == 1:
                data, count = fetchData.fetchDamagedItems(self.input_idno_uinfo.text(), page, category, searchKeyword)
                self.UtotalPages = (count // self.per_page) + (1 if count % self.per_page != 0 else 0)
                self.Uupdate_pageNumber()

            elif self.addItemState == 2:
                # Use updated version without pagination
                data = fetchData.fetchAllAvailableItems(category, searchKeyword)

                # No count, no pagination
                self.UtotalPages = 1
                self.UpageNum = 1
                # Skip self.Uupdate_pageNumber()

            self.Item_table.setRowCount(len(data))
            for row, item in enumerate(data):
                self.Item_table.setItem(row, 0, QtWidgets.QTableWidgetItem(f"{self.spacer}{item[0]}"))
                self.Item_table.setItem(row, 1, QtWidgets.QTableWidgetItem(f"{self.spacer}{item[1]}"))

                available_qty = int(item[1])
                spinbox = self.createQuantitySpinBox(available_qty)
                self.Item_table.setCellWidget(row, 2, spinbox)

        except Exception as e:
            print(f"Failed to populate: {e}")


    #-----Add Professor-----#
    def openProfessor(self):
        from src.uifolder.Professor_dialog import ProfessorDialog
        dialog = ProfessorDialog(self)

        if dialog.exec():
            self.populateProfTable()  # Refresh the professor table after adding a new professor

    #-----Add Item-----#
    def openAddItem(self):
        from src.uifolder.add_dialog import AddDialog
        dialog = AddDialog(self)
        
        if dialog.exec():
            self.populateEquipmentTable()  # Refresh the equipment table after adding a new item

    #-----Add Borrower-----#
    def openBorrower(self):
        from src.uifolder.Student_dialog import Students_Dialog
        dialog = Students_Dialog(self)

        if dialog.exec():
            self.populateBorrowerTable()

    #-----Edit Borrower-----#
    def editOpenBorrower(self, data):
        from src.uifolder.editStudent_dialog import EditStudent_Dialog
        dialog = EditStudent_Dialog(self, data)

        if dialog.exec():
            self.populateBorrowerTable()

    #-----Edit Professor-----#
    def editOpenProfessor(self, data):
        from src.uifolder.editProfessor_dialog import editProfessorDialog
        dialog = editProfessorDialog(self, data)

        if dialog.exec():
            self.populateProfTable()

if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec())
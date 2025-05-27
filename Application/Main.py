import sys
from src.modules import delete, edit, add, fetchData
from datetime import datetime    #Need ni siya for delete
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
        #self.setupTableBehavior()
        
        self.connector = Connector(self)
        self.logic = Confirmation(self)
        
        self.pageNum = "1" #initial'
        self.total_pages = 1 # initial
        self.per_page = 10
        
        self.populateEquipmentTable()
        self.populateReturnTable()
        self.populateBorrowTable()
        self.populateReplaceTable()
        
        # Transaction connections
        self.searchbox_transaction.returnPressed.connect(self.getCurrentTransactionTable) # change pa ni
        
        self.Date_box_borrow.currentIndexChanged.connect(lambda _: self.populateBorrowTable())
        self.Date_box_return.currentIndexChanged.connect(lambda _: self.populateReturnTable())
        self.Date_box_replace.currentIndexChanged.connect(lambda _: self.populateReplaceTable())
        
        self.searchbox_inventory.returnPressed.connect(self.populateEquipmentTable)
        
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

        #Add item connections
        self.borrow_button_user.clicked.connect(self.addBorrowItemCombobox)
#-----Helper-----#

    def getCurrentTransactionTable(self):
        
        current_index = self.Dashboard_Frame.currentIndex()
        
        return current_index

    def getCurrentTransactionTableSearch(self):
        
        current_index = self.Dashboard_Frame.currentIndex()
        
        if current_index == 0:
            self.populateBorrowTable()
        elif current_index == 1:
            self.populateReturnTable()
        elif current_index == 2:
            self.populateReplaceTable()
            
    def createOptionsButton(self, id):
        btn = QtWidgets.QPushButton(" ⋮ ")
        btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        
        btn.setStyleSheet("text-align: center;")
        #btn.setFixedSize(30, 30)

        menu = QtWidgets.QMenu(btn)
        edit_action = QtGui.QAction("Edit", self)
        delete_action = QtGui.QAction("Delete", self)
        menu.addAction(edit_action)
        menu.addAction(delete_action)

        edit_action.triggered.connect(partial(self.editRow, id))
        delete_action.triggered.connect(partial(self.deleteRow, id))

        btn.setMenu(menu)

        return btn

        
#-----Populates tables-----#

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
                self.inventory_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(item[0])))
                self.inventory_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(item[1])))
                self.inventory_table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(item[2])))
                self.inventory_table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(item[3])))
                
                btn = self.createOptionsButton(item[0])
                self.borrow_table.setCellWidget(row, 4, btn)
                
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
                self.borrow_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(item[0])))
                self.borrow_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(item[1])))
                self.borrow_table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(item[2])))
                self.borrow_table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(item[4])))
                self.borrow_table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(item[3])))
                
                btn = self.createOptionsButton(item[0])
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
                self.return_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(item[0])))
                self.return_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(item[1])))
                self.return_table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(item[2])))
                self.return_table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(item[3])))
                self.return_table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(item[4])))
                
                btn = self.createOptionsButton(item[0])
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
                self.replace_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(item[0])))
                self.replace_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(item[1])))
                self.replace_table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(item[2])))
                self.replace_table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(item[3])))
                
                btn = self.createOptionsButton(item[0])
                self.replace_table.setCellWidget(row, 4, btn)
            
        except Exception as e:
            print(f"Error in populateReplaceTable: {e}")
            
            
#-----Edit and Delete functions-----#

    def editRow(row):
        return
        
    def deleteRow(row):
        return
    
#-----Page navigation for transaction tables-----# 
    
    def go_to_next_page(self):
        try:
            current_SWPage = self.Admin_Page.currentIndex()
            
            current_page = int(self.pageNum)
            current_page += 1
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
                #case 2: for users
                case _:
                    print("Unknown admin page index")
                            
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
                #case 2: users page
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
                #case 2: for users
                case _:
                    print("Unknown admin page index")
                    return

            if page_input.isdigit():
                page = int(page_input)
                if 1 <= page <= self.total_pages:
                    self.pageNum = str(page)
                    
                    match current_SWPage:
                        case 0:
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
                        #case 2: users page
                        case _:
                            print("Unknown admin page index")
                        
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
            #case 2:
            case _:
                print("Unknown admin page index")

    
    def update_button_state(self):
        try:
            current_SWPage = self.Admin_Page.currentIndex()
            
            match current_SWPage:
                case 0:
                    current_tab_index = self.Dashboard_Frame.currentIndex() 

                    match current_tab_index:
                        case 0:  # borrow table
                            current_page = int(self.pageNum) 
                            total_pages = self.total_pages
                            
                            self.arrow_left_borrow.setEnabled(current_page > 1)
                            self.arrow_right_borrow.setEnabled(current_page < total_pages)
                        case 1:  # return table
                            current_page = int(self.pageNum)
                            total_pages = self.total_pages
                            
                            self.arrow_left_return.setEnabled(current_page > 1)
                            self.arrow_right_return.setEnabled(current_page < total_pages)
                        case 2:  # replace table
                            current_page = int(self.pageNum) 
                            total_pages = self.total_pages
                            
                            self.arrow_left_replace.setEnabled(current_page > 1)
                            self.arrow_right_replace.setEnabled(current_page < total_pages)
                        case _:
                            print("Unknown table index")
                            return
                case 1:
                    current_page = int(self.pageNum) 
                    total_pages = self.total_pages
                    
                    self.arrow_left.setEnabled(current_page > 1)
                    self.arrow_right.setEnabled(current_page < total_pages)
                #case 2:
                case _:
                    print("Unknown admin page index")  

            print(f"Button states updated")
        except Exception as e:
            print(f"Error in update_button_state: {e}")

#-----Combobox choices-----#
    def addBorrowItemCombobox(self):
        data = fetchData.fetchCategory()
        for row in data:
            self.category_box_additem.addItem(str(row))
    
if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec())
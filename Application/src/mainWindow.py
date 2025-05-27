from PyQt6 import QtWidgets, QtCore, QtGui
from functools import partial
from src.modules import fetchData
from src.uifolder.EquipmentManager_CSM import Ui_MainWindow
from src.uifolder.connectors import Connector
from src.uifolder.confirmation import Confirmation
from src.uifolder.connectors import Connector

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        #self.setupTableBehavior()
        
        self.connector = Connector(self)
        self.logic = Confirmation(self)
        
        self.pageNum = "1" #initial
        
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
        self.arrow_right_replace.clicked.connect(self.go_to_next_page)
        self.arrow_right_return.clicked.connect(self.go_to_next_page)
        
        self.arrow_left_borrow.clicked.connect(self.go_to_prev_page)

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
    
#-----Page navigation-----# 
    
    def go_to_next_page(self):
        try:
            current_tab_index = self.Dashboard_Frame.currentIndex()
            current_page = int(self.pageNum)

            if current_page < 10:  # placeholder sa
                current_page += 1
                self.pageNum = str(current_page)
                print(f"Going to next page: {self.pageNum}")

                match current_tab_index:
                    case 0:  # borrow Table
                        self.populateBorrowTable()
                    case 1:  # return Table
                        self.populateReturnTable()
                    case 2:  # replace Table
                        self.populateReplaceTable()
                    case _:
                        print("Unknown table index!")
        except Exception as e:
            print(f"Error in go_to_next_page: {e}")

            
    def go_to_prev_page(self):
        return
    
    def go_to_page(self):
        return
    
    def update_button_state(self):
        return
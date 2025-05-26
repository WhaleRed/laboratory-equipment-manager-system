from PyQt6 import QtWidgets, QtCore, QtGui
from functools import partial
from .modules import fetchData
from .uifolder.EquipmentManager_CSM import Ui_MainWindow
from .connectors import Connector
from datetime import datetime

DATE_OPTIONS = {
    0: 1,    # Last 1 hour
    1: 3,    # Last 3 hours
    2: 1,    # Last 1 day
    3: 7,    # Last 7 days
    4: 30,   # Last 30 days
    5: 90,   # Last 90 days
    6: 180,  # Last 180 days
}

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setupTableBehavior()
        
        self.connector = Connector(self)
        
        self.pageNum = "1" #initial
        
        self.populateReturnTable()
        self.populateBorrowTable()
        self.populateReplaceTable()
        
        self.Date_box_borrow.currentIndexChanged.connect(self.on_borrow_date_filter_changed)
        #self.Date_box_return.currentIndexChanged.connect(self.on_return_date_filter_changed)
        #self.Date_box_replace.currentIndexChanged.connect(self.on_replace_date_filter_changed)
        
        self.arrow_right_borrow.clicked.connect(self.go_to_next_page)

#-----Date Filter-----#
        
    def on_borrow_date_filter_changed(self, index, sortState=None):
        
        dateState = index - 1
        page = int(self.pageNum)
        day_hour = DATE_OPTIONS.get(dateState)
        
        if day_hour is None:
            print(f"Warning: No date option found for dateState {dateState}")
            return
        
        if sortState is None:
            sortState = 0
        
        match sortState:
            case 0:  # sort by Date
                match dateState:
                    case 0 | 1:  # hour-based
                        data = fetchData.getRecentBorrowedEquipmentByDate(day_hour, page)
                    case 2 | 3 | 4 | 5 | 6:  # day-based
                        data = fetchData.getBorrowedEquipmentByDateSince(day_hour, page)
                    case _:
                        print(f"Warning: Invalid dateState {dateState} for sortState {sortState}")
                        return None
            case 1:  # sort by BorrowerID
                match dateState:
                    case 0 | 1:  # hour-based
                        data = fetchData.getRecentBorrowedEquipmentByBorrowerId(day_hour, page)
                    case 2 | 3 | 4 | 5 | 6:  # day-based
                        data = fetchData.getBorrowedEquipmentByBorrowerIdSince(day_hour, page)
                    case _:
                        print(f"Warning: Invalid dateState {dateState} for sortState {sortState}")
                        return None
            case 2:  # sort by EquipmentID
                match dateState:
                    case 0 | 1:  # hour-based
                        data = fetchData.getRecentBorrowedEquipmentByEquipId(day_hour, page)
                    case 2 | 3 | 4 | 5 | 6:  # day-based
                        data = fetchData.getBorrowedEquipmentByEquipIdSince(day_hour, page)
                    case _:
                        print(f"Warning: Invalid dateState {dateState} for sortState {sortState}")
                        return None
            case _:
                print(f"Warning: Unsupported sortState: {sortState}")
                return None

        print(f"New data: {data}")
        
        self.populateBorrowTable(newData=data)
        
#-----Populates tables-----#

    def populateEquipmentTable(self,  sortState=None, searchKeyword=None, newData=None):
        
        self.inventory_table.clearContents()
        
        if sortState is None:
            sortState = 0
        
        if newData is not None:
            data = newData
        else:
            page = int(self.pageNum)
            if searchKeyword is not None:
                data = fetchData.searchEquipment(searchKeyword, page)
            else:
                match sortState:
                    case 0:
                        data = fetchData.sortEquipmentID(page) # default
                    case 1:
                        data = fetchData.sortEquipmentCateg(page) # sort by category
                    case 2:
                        data = fetchData.sortEquipmentName(page) # sort by equipment name
                    case 3:
                        data = fetchData.sortEquipmentQty(page) # sort by quantity

        self.inventory_table.setRowCount(len(data))
        for row, item in enumerate(data):
            self.inventory_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(item[0])))
            self.inventory_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(item[1])))
            self.inventory_table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(item[2])))
            self.inventory_table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(item[3])))
            self.inventory_table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(item[4])))

    def populateBorrowTable(self,  sortState=None, searchKeyword=None, newData=None):
        
        #sortState = self.Filter_box_borrow.currentIndex()
        #dateState = self.Date_box_borrow.currentIndex() - 1
        #searchKeyword = self.searchbox_transaction.text().strip()
        
        data = []
        page = int(self.pageNum)
        
        self.borrow_table.clearContents()
        
        self.borrow_table.setHorizontalHeaderLabels([
            "ID", "Col1", "Col2", "Status", "Quantity", "Options"
        ])

        if sortState is None:
            sortState = 0
        
        print(f"Populating borrow table, pageNum = {self.pageNum}, sortState={sortState}, searchKeyword={searchKeyword}")
            
        if newData is not None:
            data = newData
        else:
            try:
                page = int(self.pageNum)  # convert pageNum string to int here
            except ValueError:
                print("Conversion failed, defaulting page number to 1")
                page = 1  # default to 1 if conversion fails
                
            if searchKeyword is not None:
                data = fetchData.searchBorrowedEquipment(searchKeyword, page)
            else:
                match sortState:
                    case 0:
                        data = fetchData.sortDateBorrowedEquipment(page) # default 
                    case 1:
                        data = fetchData.sortEIDBorrowedEquipment(page) # sort by equipment ID
                    case 2:
                        data = fetchData.sortBIDBorrowedEquipment(page) # sort by borrower ID
                    #case 3:
                    #   data = fetchData.sortStatusBorrowedEquipment(page)) # sort by status
                    
        print(f"Fetched data for page {page}: {data}")
        if not data:
            print("Warning: No data fetched for this page.")

        for row in data:
            print(f"Date and time: {row[2]}")

        self.borrow_table.setRowCount(len(data))
        for row, item in enumerate(data):
            self.borrow_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(item[0])))
            self.borrow_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(item[1])))
            self.borrow_table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(item[2])))
            self.borrow_table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(item[4])))
            self.borrow_table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(item[3])))
            
            btn = self.createOptionsButton(item[0])
            self.borrow_table.setCellWidget(row, 5, btn)

    def populateReturnTable(self,  sortState=None, searchKeyword=None, newData=None):
        
        self.return_table.clearContents()
        
        if sortState is None:
            sortState = 0

        if newData is not None:
            data = newData
        else:
            page = int(self.pageNum)
            if searchKeyword is not None:
                data = fetchData.searchReturnedEquipment(searchKeyword, page)
            else:
                match sortState:
                    case 0:
                        data = fetchData.sortDateReturnedEquipment(page) # default 
                    case 1:
                        data = fetchData.sortEIDReturnedEquipment(page) # sort by equipment ID
                    case 2:
                        data = fetchData.sortBIDReturnedEquipment(page) # sort by borrower ID
                    case 3:
                        data = fetchData.sortStatusReturnedEquipment(page) # sort by status

        self.return_table.setRowCount(len(data))
        for row, item in enumerate(data):
            self.return_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(item[0])))
            self.return_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(item[1])))
            self.return_table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(item[2])))
            self.return_table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(item[3])))
            self.return_table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(item[4])))
            
    def populateReplaceTable(self,  sortState=None, searchKeyword=None, newData=None):
        
        self.replace_table.clearContents()
        
        if sortState is None:
            sortState = 0
        
        if newData is not None:
            data = newData
        else:
            page = int(self.pageNum)
            if searchKeyword is not None:
                data = fetchData.searchReturnedEquipment(searchKeyword, page)
            else:
                match sortState:
                    case 0:
                        data = fetchData.sortDateReplacedEquipment(page) # default 
                    case 1:
                        data = fetchData.sortEIDReplacedEquipment(page) # sort by equipment ID
                    case 2:
                        data = fetchData.sortBIDReplacedEquipment(page) # sort by borrower ID

        self.replace_table.setRowCount(len(data))
        for row, item in enumerate(data):
            self.replace_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(item[0])))
            self.replace_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(item[1])))
            self.replace_table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(item[2])))
            self.replace_table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(item[3])))
            
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
            
#-----Edit and Delete functions-----#

    def editRow(row):
        return
        
    def deleteRow(row):
        return
    
#-----Page navigation-----# 
    
    def go_to_next_page(self):
        try:
            current_page = int(self.pageNum)
            if current_page < 10:#self.total_pages:
                current_page += 1
                self.pageNum = str(current_page)
                print(f"Going to next page: {self.pageNum}")
                self.populateBorrowTable()  # no arguments
        except Exception as e:
            print(f"Error in go_to_next_page: {e}")
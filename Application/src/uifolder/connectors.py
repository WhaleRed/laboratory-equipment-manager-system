from .EquipmentManager_CSM import Ui_MainWindow
from .confirmation import Confirmation
from .Student_dialog import Students_Dialog
from .add_dialog import AddDialog
class Connector:
    def __init__(self, ui: Ui_MainWindow):
        self.ui = ui
        self.confirmation = Confirmation(self.ui)
        self.connect_admin_buttons()
        self.connect_user_interactive_buttons()


    
    # Connector for Buttons
    def connect_admin_buttons(self):
        
        # Admin User Buttons
        self.ui.admin_icon_sidebar.clicked.connect(self.go_to_admin_user_page)
        self.ui.admin_icon.clicked.connect(self.go_to_admin_user)
        
        
        
        # Inventory Buttons
        self.ui.inventory_button_sidebar.clicked.connect(self.Inventory_Page)

        # Transaction Buttons
        self.ui.borrow_button_sidebar.clicked.connect(self.Transaction_Page)

        # User Button
        self.ui.user_button_sidebar.clicked.connect(self.go_to_AdminBorrower_Page)

        
       
       
    def connect_user_interactive_buttons(self):
        # Back Buttons
        self.ui.back_button_additem.clicked.connect(self.go_back_from_user_interactive)
        self.ui.back_button_uinfo.clicked.connect(self.go_back_from_user_interactive)
        self.ui.back_confirmation.clicked.connect(self.go_back_from_user_interactive)
        
        # Next Buttons
        self.ui.next_button_additem.clicked.connect(self.go_next_from_user_interactive)
        self.ui.next_button_uinfo.clicked.connect(self.go_next_from_user_interactive)
        
        # Borrow Replace and Return Button
        self.ui.borrow_button_user.clicked.connect(self.go_to_borrow)
        self.ui.return_button_user.clicked.connect(self.go_to_borrow)
        self.ui.replace_button_user.clicked.connect(self.go_to_borrow)
        
        # Submit Button
        self.ui.submit_confirmation.clicked.connect(self.go_to_user_interactive_page)

   

    def go_to_user_interactive_page(self):
        self.ui.User_Interactive_Page.setCurrentIndex(0)

    # Admin User
    def go_to_admin_user_page(self):
        index = self.ui.Admin_User_Page.indexOf(self.ui.page)
        if index != -1:
            self.ui.Admin_User_Page.setCurrentIndex(index)
    
    # User Interactive Page to Admin User Page 
    def go_to_admin_user(self):
        # Goes to page 2 (index 1) of the parent stacked widget
        self.ui.Admin_User_Page.setCurrentIndex(1)
    
    # Inventory Page Function
    def Inventory_Page(self):
        # Navigate to Admin_Page container in Admin_User_Page
        self.ui.Admin_User_Page.setCurrentIndex(1)
        # Then set Admin_Page to Inventory
        self.ui.Admin_Page.setCurrentIndex(1)

    # Transaction Page Function
    def Transaction_Page(self):
        self.ui.Admin_User_Page.setCurrentIndex(1)
        self.ui.Admin_Page.setCurrentIndex(0)

    # Admin Borrower Page Function
    def go_to_AdminBorrower_Page(self):
        self.ui.Admin_User_Page.setCurrentIndex(1)
        self.ui.Admin_Page.setCurrentIndex(2)

    
    # Back Function
    def go_back_from_user_interactive(self):
        current_index = self.ui.User_Interactive_Page.currentIndex()
        if current_index > 0:
            self.ui.User_Interactive_Page.setCurrentIndex(current_index - 1)
    
    # Next Funtion
    def go_next_from_user_interactive(self):
        current_index = self.ui.User_Interactive_Page.currentIndex()
          # User Information Page Validator 
        if current_index == self.ui.User_Interactive_Page.indexOf(self.ui.User_Information_PAGE):
            if not self.confirmation.user_input_fields():
                return
        if current_index < self.ui.User_Interactive_Page.count() - 1:
            self.ui.User_Interactive_Page.setCurrentIndex(current_index + 1)

    # Borrow Function
    def go_to_borrow(self):
        current_index = self.ui.User_Interactive_Page.currentIndex()
        if current_index < self.ui.User_Interactive_Page.count() - 1:
            self.ui.User_Interactive_Page.setCurrentIndex(current_index + 1)

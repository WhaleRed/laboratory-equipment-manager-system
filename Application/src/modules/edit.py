import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

db = mysql.connector.connect(
  host= os.getenv("DATABASE_HOST"),
  user = os.getenv("DATABASE_USER"),
  password= os.getenv("DATABASE_PASSWORD"),
  database= os.getenv("DATABASE_NAME")
)

#Borrower Array values must have
# NewID, NewProfID, NewFname, NewLname, NewProgram, NewBlock, CurrentID
def editBorrower(borrower):
  mycursor = db.cursor()
  mycursor.execute("UPDATE borrower SET BorrowerID = %s, ProfessorID = %s, FirstName = %s, LastName = %s, Program = %s, Block = %s WHERE BorrowerID = %s", borrower)
  db.commit()
  mycursor.close()

#Prof Array values must have
#NewProfID, NewFname, NewLname, CurrentProfID
def editProfessor(professor):
  mycursor = db.cursor()
  mycursor.execute("UPDATE professor SET  ProfessorID = %s, FirstName = %s, LastName = %s WHERE ProfessorID =%s", professor)
  db.commit()
  mycursor.close()

#Equipment Array values must have
#NewEquipmentID, NewName, NewQuantity, NewCategory, CurrentEquipmentID
def editEquipment(equipment):
  mycursor = db.cursor()
  mycursor.execute("UPDATE equipment SET EquipmentID = %s, Name = %s, Quantity = %s, Category = %s WHERE EquipmentID = %s", equipment)
  db.commit()
  mycursor.close()

#Equipment Array values must have
#NewEquipmentID, NewBorrowerID, NewBorrow_date, CurrentEquipmentID, CurrentBorrowerID, CurrentBurror_date
def editBorrowedEquipment(equipment):
  mycursor = db.cursor()
  mycursor.execute("UPDATE borrowed_equipment SET EquipmentID = %s, BorrowerID = %s, Borrow_date = %s WHERE (EquipmentID = %s AND BorrowerID = %s AND Borrow_date = %s)", equipment)
  db.commit()
  mycursor.close()

#Equipment Array values must have
#NewEquipmentID, NewBorrowerID, NewReplacement_date, CurrentEquipmentID, CurrentBorrowerID, CurrentReplaced_date
def editReplacedEquipment(equipment):
  mycursor = db.cursor()
  mycursor.execute("UPDATE replaced_equipment SET EquipmentID = %s, BorrowerID = %s, Replacement_date = %s WHERE (EquipmentID = %s AND BorrowerID = %s AND Replacement_date = %s)", equipment)
  db.commit()
  mycursor.close()

#Equipment Array values must have
#NewEquipmentID, NewBorrowerID, NewReturn_date, NewStatus, CurrentEquipmentID, CurrentBorrowerID, CurrentReturn_date
def editReturnedEquipment(equipment):
  mycursor = db.cursor()
  mycursor.execute("UPDATE returned_equipment SET EquipmentID = %s, BorrowerID = %s, Return_date = %s, Status = %s WHERE (EquipmentID = %s AND BorrowerID = %s AND Return_date = %s)", equipment)
  db.commit()
  mycursor.close()
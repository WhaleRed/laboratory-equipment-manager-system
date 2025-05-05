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

#Pass idnum
def delBorrower(idnum):        

  mycursor = db.cursor()

  mycursor.execute("DELETE FROM borrower WHERE BorrowerID = %s", (idnum,))
  db.commit()
  mycursor.close()

#Pass idnum
def delProfessor(idnum):        

  mycursor = db.cursor()

  mycursor.execute("DELETE FROM professor WHERE ProfessorID = %s", (idnum,))
  db.commit()
  mycursor.close()

#Pass idnum
def delEquipment(idnum):        

  mycursor = db.cursor()

  mycursor.execute("DELETE FROM equipment WHERE EquipmentID = %s", (idnum,))
  db.commit()
  mycursor.close()

#Pass multiple values since compounded PK
def delBorrowedEquipment(equipmentID, borrowerID, borrowDate):
  mycursor = db.cursor()

  mycursor.execute("DELETE FROM borrowed_equipment WHERE (EquipmentID = %s AND BorrowerID = %s AND Borrow_date = %s)", (equipmentID, borrowerID, borrowDate))
  db.commit()
  mycursor.close()

#Pass multiple values since compounded PK
def delReplacedEquipment(equipmentID, borrowerID, replacementDate):
  mycursor = db.cursor()

  mycursor.execute("DELETE FROM replaced_equipment WHERE (EquipmentID = %s AND BorrowerID = %s AND Replacement_date = %s)", (equipmentID, borrowerID, replacementDate))
  db.commit()
  mycursor.close()

#Pass multiple values since compounded PK
def delReturnedEquipment(equipmentID, borrowerID, returnedDate):
  mycursor = db.cursor()

  mycursor.execute("DELETE FROM returned_equipment WHERE (EquipmentID = %s AND BorrowerID = %s AND Return_date = %s)", (equipmentID, borrowerID, returnedDate))
  db.commit()
  mycursor.close()
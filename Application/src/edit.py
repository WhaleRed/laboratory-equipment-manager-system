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
# NewID, NewProfID, Fname, Lname, Program, Block, CurrentID
def editBorrower(borrower):
  mycursor = db.cursor()
  mycursor.execute("UPDATE borrower SET BorrowerID = %s, ProfessorID = %s, FirstName = %s, LastName = %s, Program = %s, Block = %s WHERE BorrowerID = %s", borrower)
  db.commit()
  mycursor.close()

#Prof Array values must have
#NewProfID, Fname, Lname, CurrentProfID
def editProfessor(professor):
  mycursor = db.cursor()
  mycursor.execute("UPDATE professor SET  ProfessorID = %s, FirstName = %s, LastName = %s WHERE ProfessorID =%s", professor)
  db.commit()
  mycursor.close()

#Equipment Array values must have
#NewEquipmentID, Name, Quantity, Category, CurrentEquipmentID
def editEquipment(equipment):
  mycursor = db.cursor()
  mycursor.execute("UPDATE equipment SET EquipmentID = %s, Name = %s, Quantity = %s, Category = %s WHERE EquipmentID = %s", equipment)
  db.commit()
  mycursor.close()
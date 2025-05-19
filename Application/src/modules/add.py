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

#Must pass a dictionary


def addBorrower(borrower):
  mycursor = db.cursor()
  try:
    mycursor.execute(
            "INSERT INTO Borrower (BorrowerID, ProfessorID, FirstName, LastName, Program, Block) "
            "VALUES (%(BorrowerID)s, %(ProfessorID)s, %(FirstName)s, %(LastName)s, %(Program)s, %(Block)s)",
            borrower
        )
    db.commit()
    return 0
  except mysql.connector.IntegrityError as e:
    if e.errno == 1062:
      return 1
  finally:
    mycursor.close()

def addProfessor(professor):
  mycursor = db.cursor()
  try:
    mycursor.execute(
            "INSERT INTO Professor (ProfessorID, FirstName, LastName) "
            "VALUES (%(ProfessorID)s, %(FirstName)s, %(LastName)s)",
            professor
        )
    db.commit()
    return 0
  except mysql.connector.IntegrityError as e:
    if e.errno == 1062:
      return 1
  finally:
    mycursor.close()

def addEquipment(equipment):
  mycursor = db.cursor()
  try:
    mycursor.execute(
            "INSERT INTO Equipment (EquipmentID, Name, Quantity, Category"
            "VALUES (%(EquipmentID)s, %(Name)s, %(Quantity)s, %(Category)s)",
            equipment
        )
    db.commit()
    return 0
  except mysql.connector.IntegrityError as e:
    if e.errno == 1062:
      return 1
  finally:
    mycursor.close()

def addBorrowedEquipment(equipment):
  mycursor = db.cursor()
  try:
    mycursor.execute(
            "INSERT INTO Borrowed_equipment (EquipmentID, BorrowerID, Borrow_date) "
            "VALUES (%(EquipmentID)s, %(BorrowerID)s, %(Borrow_date)s)", equipment
            )
    db.commit()
    return 0
  except mysql.connector.IntegrityError as e:
    if e.errno == 1062:
      return 1
  finally:
    mycursor.close()

def addReplacedEquipment(equipment):
  mycursor = db.cursor()
  try:
    mycursor.execute(
            "INSERT INTO Replaced_equipment (EquipmentID, BorrowerID, Replacement_date ) "
            "VALUES (%(EquipmentID)s, %(BorrowerID)s, %(Replacement_date )s)", equipment
            )
    return 0
  except mysql.connector.IntegrityError as e:
    if e.errno == 1062:
      return 1
  finally:
    mycursor.close()

def addReturnedEquipment(equipment):
  mycursor = db.cursor()
  try:
    mycursor.execute(
            "INSERT INTO Replaced_equipment (EquipmentID, BorrowerID, Return_date , Status) "
            "VALUES (%(EquipmentID)s, %(BorrowerID)s, %(Return_date )s, %(Status)s)", equipment
            )
    db.commit()
    return 0
  except mysql.connector.IntegrityError as e:
    if e.errno == 1062:
      return 1
  finally:
    mycursor.close()
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
            "INSERT INTO Borrower (BorrowerID, ProfessorID, FirstName, LastName, Program, YearLevel) "
            "VALUES (%(borrowerId)s, %(profId)s, %(fname)s, %(lname)s, %(program)s, %(yearlevel)s)",
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
            "INSERT INTO Professor (ProfessorId, FirstName, LastName) "
            "VALUES (%(profId)s, %(fname)s, %(lname)s)",
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
            "INSERT INTO Equipment (EquipmentId, Equipment_name, Available, Category)"
            "VALUES (%(EquipmentID)s, %(Equipment_name)s, %(Available)s, %(Category)s)",
            equipment
        )
    db.commit()
    return 0
  except mysql.connector.IntegrityError as e:
    if e.errno == 1062:
      return 1
  finally:
    mycursor.close()

def addBorrowedEquipment(equipmentID, borrowerID, state, qty):
  mycursor = db.cursor()
  try:
    print("borrowing")
    mycursor.execute(
            "INSERT INTO Borrowed_equipment (EquipmentID, BorrowerID, Borrow_date, State, Quantity) "
            "VALUES (%s, %s, NOW(), %s, %s)", (equipmentID, borrowerID, state, qty)
            )
    db.commit()
    return 0
  except mysql.connector.IntegrityError as e:
    if e.errno == 1062:
      return 1
  finally:
    mycursor.close()

def addReplacedEquipment(equipmentID, borrowerID, quantity):
  mycursor = db.cursor()
  try:
    print("replacing")
    print(f"Params: {equipmentID, borrowerID, quantity}")
    mycursor.execute(
            "INSERT INTO Replaced_equipment (EquipmentID, BorrowerID, Replacement_date, Quantity) "
            "VALUES (%s, %s, NOW(), %s)", (equipmentID, borrowerID, quantity)
            )
    db.commit()
    return 0
  except mysql.connector.IntegrityError as e:
    if e.errno == 1062:
      return 1
  finally:
    mycursor.close()

def addReturnedEquipment(equipmentID, borrowerId, state, quantity):
  mycursor = db.cursor()
  try:
    mycursor.execute(
            "INSERT INTO Returned_equipment (EquipmentID, BorrowerID ,Return_date , Status, Quantity) "
            "VALUES (%s, %s, NOW(), %s, %s)", (equipmentID, borrowerId, state, quantity)
            )
    db.commit()
    return 0
  except mysql.connector.IntegrityError as e:
    if e.errno == 1062:
      return 1
  finally:
    mycursor.close()
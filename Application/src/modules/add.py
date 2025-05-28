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
            "VALUES (%(borrowerId)s, %(profId)s, %(fname)s, %(lname)s, %(program)s, %(block)s)",
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

def addBorrowedEquipment(equipment):
  mycursor = db.cursor()
  try:
    mycursor.execute(
            "INSERT INTO Borrowed_equipment (EquipmentID, BorrowerID, Borrow_date) "
            "VALUES (%(equipId)s, %(borrowerId)s, NOW())", equipment
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
            "INSERT INTO Replaced_equipment (EquipmentID, BorrowerID, Replacement_date) "
            "VALUES (%(equipId)s, %(borrowerId)s, NOW())", equipment
            )
    db.commit()
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
            "INSERT INTO Returned_equipment (EquipmentID, BorrowerID ,Return_date , Status) "
            "VALUES (%(equipId)s, %(borrowerId)s, NOW(), %(status)s)", equipment
            )
    db.commit()
    return 0
  except mysql.connector.IntegrityError as e:
    if e.errno == 1062:
      return 1
  finally:
    mycursor.close()
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
            "INSERT INTO Equipment (EquipmentId, Name, Quantity, Category"
            "VALUES (%(equipId)s, %(name)s, %(quantity)s, %(category)s)",
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
            "INSERT INTO Borrowed_equipment (EquipmentID, BorrowerID, Borro) "
            "VALUES (%(equipId)s, %(borrowerId)s, GETDATE())", equipment
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
            "INSERT INTO Replaced_equipment (EquipmentID, BorrowerID) "
            "VALUES (%(equipId)s, %(borrowerId)s, GETDATE())", equipment
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
            "INSERT INTO Replaced_equipment (EquipmentID, BorrowerID , Status) "
            "VALUES (%(equipId)s, %(borrowerId)s, GETDATE(), %(status)s)", equipment
            )
    db.commit()
    return 0
  except mysql.connector.IntegrityError as e:
    if e.errno == 1062:
      return 1
  finally:
    mycursor.close()
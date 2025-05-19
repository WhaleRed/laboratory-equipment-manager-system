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

#-----FYI-----#
#return 0: no error
#return 1: can't delete cus still being used

#Pass idnum
def delBorrower(idnum):        

  mycursor = db.cursor()
  try:
    mycursor.execute("DELETE FROM borrower WHERE BorrowerID = %s", (idnum,))
    db.commit()
    return 0
  except mysql.connector.IntegrityError as e:
    if e.errno == 1451:
      return 1
  finally:
    mycursor.close()

#Pass idnum
def delProfessor(idnum):        

  mycursor = db.cursor()
  try:
    mycursor.execute("DELETE FROM professor WHERE ProfessorID = %s", (idnum,))
    db.commit()
    return 0
  except mysql.connector.IntegrityError as e:
    if e.errno == 1451:
      return 1
  finally:
    mycursor.close()

#Pass idnum
def delEquipment(idnum):        

  mycursor = db.cursor()
  try:
    mycursor.execute("DELETE FROM equipment WHERE EquipmentID = %s", (idnum,))
    db.commit()
    return 0
  except mysql.connector.IntegrityError as e:
    if e.errno == 1451:
      return 1
  finally:
    mycursor.close()

#Pass multiple values since compounded PK
def delBorrowedEquipment(conditions):
  mycursor = db.cursor()
  try:
    mycursor.execute(
            "DELETE FROM borrowed_equipment "
            "WHERE EquipmentID = %(EquipmentID)s "
            "AND BorrowerID = %(BorrowerID)s "
            "AND Borrow_date = %(Borrow_date)s",
            conditions
        )
    db.commit()
    return 0
  except mysql.connector.IntegrityError as e:
    if e.errno == 1451:
      return 1
  finally:
    mycursor.close()

#Pass multiple values since compounded PK
def delReplacedEquipment(conditions):
  mycursor = db.cursor()
  try:
    mycursor.execute(
            "DELETE FROM borrowed_equipment "
            "WHERE EquipmentID = %(EquipmentID)s "
            "AND BorrowerID = %(BorrowerID)s "
            "AND Replacement_date  = %(Replacement_date )s",
            conditions
        )
    db.commit()
    return 0
  except mysql.connector.IntegrityError as e:
    if e.errno == 1451:
      return 1
  finally:
    mycursor.close()

#Pass multiple values since compounded PK
def delReturnedEquipment(conditions):
  mycursor = db.cursor()
  try:
    mycursor.execute(
            "DELETE FROM borrowed_equipment "
            "WHERE EquipmentID = %(EquipmentID)s "
            "AND BorrowerID = %(BorrowerID)s "
            "AND Return_date = %(Return_date)s",
            conditions
        )
    db.commit()
    return 0
  except mysql.connector.IntegrityError as e:
    if e.errno == 1451:
      return 1
  finally:
    mycursor.close()
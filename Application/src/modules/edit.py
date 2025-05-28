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

#----FYI----#
#return 0: no error
#return 1: error because duplicate / PK already exist
#return 2: error because cannot be edited because existing data uses the current data being edited

#Must pass dictionary

#Required keys:
# - new_borrowerId, new_professorId, new_fname, new_lname, 
# - new_program, new_block, and current_borrowerId
def editBorrower(borrower):
  mycursor = db.cursor()
  try:
    mycursor.execute("""
            UPDATE borrower SET 
                BorrowerID = %(new_borrowerId)s,
                ProfessorID = %(new_profId)s,
                FirstName = %(new_fname)s,
                LastName = %(new_lname)s,
                Program = %(new_program)s,
                YearLevel = %(new_yearlvl)s
            WHERE BorrowerID = %(current_borrowerId)s
            """, borrower)
    db.commit()
    return 0
  except mysql.connector.IntegrityError as e:
    if e.errno == 1062:
      return 1
    elif e.errno == 1451:
      return 2
  finally:
    mycursor.close()

#Required keys:
# - new_profId, new_fname, new_lname, current_profId
def editProfessor(professor):
  mycursor = db.cursor()
  try:
    mycursor.execute("""
            UPDATE professor SET  
              ProfessorID = %(new_profId)s,
              FirstName = %(new_fname)s,
              LastName = %(new_lname)s
            WHERE ProfessorID = %(current_profId)s
            """, professor)
    db.commit()
    return 0
  except mysql.connector.IntegrityError as e:
    if e.errno == 1062:
      return 1
    elif e.errno == 1451:
      return 2
  finally:
    mycursor.close()

#Required keys:
# - new_equipId, new_name, new_quantity, new_category, current_equipId
def editEquipment(equipment):
  mycursor = db.cursor()
  try:
    mycursor.execute("""
            UPDATE equipment SET
                EquipmentID = %(new_equipId)s,
                Equipment_name = %(new_name)s,
                Available = %(new_quantity)s,
                Category = %(new_category)s
            WHERE EquipmentID = %(current_equipId)s
            """, equipment)
    db.commit()
    return 0
  except mysql.connector.IntegrityError as e:
    if e.errno == 1062:
      return 1
    elif e.errno == 1451:
      return 2
  finally:
    mycursor.close()
    
def updateEquipmentQuantity(id, newQuantity, mode):
  mycursor = db.cursor()
  
  if mode == 0 or mode == 1:
        query = """
            UPDATE equipment
            SET available = available + %s
            WHERE equipmentID = %s
        """
  elif mode == 2:
      query = """
          UPDATE equipment
          SET available = available - %s
          WHERE equipmentID = %s
      """
  else:
      print("Invalid mode")
      return

  mycursor.execute(query, (newQuantity, id))
  db.commit()

#Required keys:
# - new_equipId, new_borrowerId, new_borrowDate,
# - current_equipId, current_borrowerId, current_borrowDate
def editBorrowedEquipment(equipment):
  mycursor = db.cursor()
  try:
    mycursor.execute("""
            UPDATE borrowed_equipment SET
                EquipmentID = %(new_equipId)s,
                BorrowerID = %(new_borrowerId)s,
                Borrow_date = %(new_borrowDate)s
            WHERE EquipmentID = %(current_equipId)s
              AND BorrowerID = %(current_borrowerId)s
              AND Borrow_date = %(current_borrowDate)s
            """, equipment)
    db.commit()
    return 0
  except mysql.connector.IntegrityError as e:
    if e.errno == 1062:
      return 1
    elif e.errno == 1451:
      return 2
  finally:
    mycursor.close()

#Required keys:
# - new_equipId, new_borrowerId, new_replaceDate,
# - current_equipId, current_borrowerId, current_replaceDate
def editReplacedEquipment(equipment):
  mycursor = db.cursor()
  try:
    mycursor.execute("""
            UPDATE replaced_equipment SET
                EquipmentID = %(new_equipId)s,
                BorrowerID = %(new_borrowerId)s,
                Replacement_date = %(new_replaceDate)s
            WHERE EquipmentID = %(current_equipId)s
              AND BorrowerID = %(current_borrowerId)s
              AND Replacement_date = %(current_replaceDate)s
            """, equipment)
    db.commit()
    return 0
  except mysql.connector.IntegrityError as e:
    if e.errno == 1062:
      return 1
    elif e.errno == 1451:
      return 2
  finally:
    mycursor.close()

#Required keys:
# - new_equipId, new_borrowerId, new_returnDate, new_status,
# - current_equipId, current_borrowerId, current_returnDate
def editReturnedEquipment(equipment):
  mycursor = db.cursor()
  try:
    mycursor.execute("""
            UPDATE returned_equipment SET
                EquipmentID = %(new_equipId)s,
                BorrowerID = %(new_borrowerId)s,
                Return_date = %(new_returnDate)s,
                Status = %(new_status)s
            WHERE EquipmentID = %(current_equipId)s
              AND BorrowerID = %(current_borrowerId)s
              AND Return_date = %(current_returnDate)s
            """, equipment)
    db.commit()
    return 0
  except mysql.connector.IntegrityError as e:
    if e.errno == 1062:
      return 1
    elif e.errno == 1451:
      return 2
  finally:
    mycursor.close()
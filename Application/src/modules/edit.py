import os
from datetime import timedelta
from dotenv import load_dotenv
import mysql.connector
from src.modules import add

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
    
def updateEquipmentQuantityState(eid, bid, newQuantity, mode, pid):
  mycursor = db.cursor()
  try:
    if mode in (0, 3):  # Returned or Damaged
        print("Processing returned or damaged")
        remaining = newQuantity

        mycursor.execute("""
            SELECT quantity, borrow_date, professorID
            FROM borrowed_equipment
            WHERE equipmentID = %s AND borrowerID = %s AND state = 'In use'
            ORDER BY borrow_date ASC
        """, (eid, bid))
        rows = mycursor.fetchall()
        print("Done selecting")

        for qty, borrow_date, pid in rows:
            print(f"Row quantity: {qty}, Remaining to process: {remaining}")

            if remaining <= 0:
                break

            to_subtract = min(remaining, qty)
            if to_subtract <= 0:
                print("Skipping update — nothing to subtract")
                continue

            remaining -= to_subtract

            if to_subtract == qty:
              if mode == 0:
                  mycursor.execute("""
                      UPDATE borrowed_equipment
                      SET state = 'Returned'
                      WHERE equipmentID = %s AND borrowerID = %s AND borrow_date = %s
                  """, (eid, bid, borrow_date))
              else:  # mode == 3 (Damaged)
                  mycursor.execute("""
                      DELETE FROM borrowed_equipment
                      WHERE equipmentID = %s AND borrowerID = %s AND borrow_date = %s
                  """, (eid, bid, borrow_date))
            else:
                mycursor.execute("""
                    UPDATE borrowed_equipment
                    SET quantity = quantity - %s
                    WHERE equipmentID = %s AND borrowerID = %s AND borrow_date = %s
                """, (to_subtract, eid, bid, borrow_date))

                if mode == 0:
                    new_borrow_date = get_unique_borrow_date(mycursor, eid, bid, pid, borrow_date)
                    mycursor.execute("""
                        INSERT INTO borrowed_equipment (equipmentID, borrowerID, professorID, quantity, state, borrow_date)
                        VALUES (%s, %s, %s, %s, 'Returned', %s)
                    """, (eid, bid, pid, to_subtract, new_borrow_date))
                else:
                    pass

            # Call your addReturnedEquipment for damaged entries
            if mode == 3 and to_subtract > 0:
                add.addReturnedEquipment(eid, bid, pid, 'Damaged', to_subtract)

            print(f"Remaining after update: {remaining}")

        if mode == 0 and newQuantity > 0:
            print("Updating equipment stock")
            mycursor.execute("""
                UPDATE equipment
                SET available = available + %s
                WHERE equipmentID = %s
            """, (newQuantity, eid))


            
    elif mode == 1:  # replace previously damaged items
      remaining = newQuantity

      # You now assume the damaged items are still in borrowed_equipment with state 'In use'
      mycursor.execute("""
          SELECT quantity, borrow_date, professorID
          FROM borrowed_equipment
          WHERE equipmentID = %s AND borrowerID = %s AND state = 'In use'
          ORDER BY borrow_date ASC
      """, (eid, bid))

      rows = mycursor.fetchall()

      for qty, borrow_date, pid in rows:
          if remaining <= 0:
              break

          to_subtract = min(remaining, qty)
          if to_subtract <= 0:
              continue

          remaining -= to_subtract

          if qty - to_subtract == 0:
              # Entire row is being replaced
              mycursor.execute("""
                  UPDATE borrowed_equipment
                  SET state = 'Replaced'
                  WHERE equipmentID = %s AND borrowerID = %s AND borrow_date = %s
              """, (eid, bid, borrow_date))
          else:
              # Partial replace — split row
              mycursor.execute("""
                  UPDATE borrowed_equipment
                  SET quantity = quantity - %s
                  WHERE equipmentID = %s AND borrowerID = %s AND borrow_date = %s
              """, (to_subtract, eid, bid, borrow_date))

              new_borrow_date = get_unique_borrow_date(mycursor, eid, bid, pid, borrow_date)

              mycursor.execute("""
                  INSERT INTO borrowed_equipment (equipmentID, borrowerID, professorID, quantity, state, borrow_date)
                  VALUES (%s, %s, %s, %s, 'Replaced', %s)
              """, (eid, bid, pid, to_subtract, new_borrow_date))

      # Update availability to reflect new replacements added to stock
      if newQuantity > 0:
          print("Updating equipment stock after replacement")
          mycursor.execute("""
              UPDATE equipment
              SET available = available + %s
              WHERE equipmentID = %s
          """, (newQuantity, eid))
                      
    elif mode == 2: # borrow
        query = """
            UPDATE equipment
            SET available = available - %s
            WHERE equipmentID = %s
        """
        mycursor.execute(query, (newQuantity, eid))
    else:
        print("Invalid mode")
        return
    
    db.commit()
  except Exception as e:
      print(f"Error updating quantity: {e}")
  finally:
      mycursor.close()

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
    
def get_unique_borrow_date(mycursor, eid, bid, pid, base_date):
    new_date = base_date + timedelta(seconds=1)
    while True:
        mycursor.execute("""
            SELECT 1 FROM borrowed_equipment
            WHERE equipmentID = %s AND borrowerID = %s AND professorID = %s AND borrow_date = %s
        """, (eid, bid, pid, new_date))
        if not mycursor.fetchone():
            return new_date
        new_date += timedelta(seconds=1)
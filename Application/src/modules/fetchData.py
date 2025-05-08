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

#-----For search with pagination-----#

def searchBorrower(searched, page):
  mycursor = db.cursor()
  
  pattern = f"%{searched}%"
  arr = []
  search = []
  for i in range(6):
    search.append(pattern)
  offset = (page-1) * 10
  search.append(offset)

  mycursor.execute("SELECT * FROM borrower WHERE BorrowerID LIKE %s OR ProfessorID LIKE %s OR FirstName LIKE %s OR LastName LIKE %s OR Program LIKE %s OR Block LIKE %s ORDER BY BorrowerID ASC LIMIT 10 OFFSET %s", search)

  for row in mycursor:
    arr.append(row)
  
  mycursor.close()

  return arr

def searchProfessor(searched, page):
  mycursor = db.cursor()

  pattern = f"%{searched}%"
  arr = []
  search = []
  for i in range(3):
    search.append(pattern)
  offset = (page-1) * 10
  search.append(offset)

  mycursor.execute("SELECT * FROM professor WHERE ProfessorID LIKE %s OR FirstName LIKE %s OR LastName LIKE %s ORDER BY ProfessorID ASC LIMIT 10 OFFSET %s", search)

  for row in mycursor:
    arr.append(row)

  mycursor.close()

  return arr

def searchEquipment(searched, page):
  mycursor = db.cursor()

  pattern = f"%{searched}%"
  arr = []
  search = []
  for i in range(4):
    search.append(pattern)
  offset = (page-1) * 10
  search.append(offset)

  mycursor.execute("SELECT * FROM equipment WHERE EquipmentID LIKE %s OR Name LIKE %s OR Quantity LIKE %s OR Category LIKE %s ORDER BY EquipmentID ASC LIMIT 10 OFFSET %s", search)

  for row in mycursor:
    arr.append(row)

  mycursor.close()

  return arr

def searchBorrowedEquipment(searched, page):
  mycursor = db.cursor()

  pattern = f"%{searched}%"
  arr = []
  search = []
  for i in range(3):
    search.append(pattern)
  offset = (page-1) * 10
  search.append(offset)

  mycursor.execute("SELECT * FROM borrowed_equipment WHERE EquipmentID LIKE %s OR BorrowerID LIKE %s OR Borrow_date LIKE %s ORDER BY Borrow_date DESC LIMIT 10 OFFSET %s", search)

  for row in mycursor:
    arr.append(row)

  mycursor.close()

  return arr

def searchReplacedEquipment(searched, page):
  mycursor = db.cursor()

  pattern = f"%{searched}%"
  arr = []
  search = []
  for i in range(3):
    search.append(pattern)
  offset = (page-1) * 10
  search.append(offset)

  mycursor.execute("SELECT * FROM replaced_equipment WHERE EquipmentID LIKE %s OR BorrowerID LIKE %s OR Replacement_date LIKE %s ORDER BY Replacement_date DESC LIMIT 10 OFFSET %s", search)

  for row in mycursor:
    arr.append(row)

  mycursor.close()

  return arr

def searchReturnedEquipment(searched, page):
  mycursor = db.cursor()

  pattern = f"%{searched}%"
  arr = []
  search = []
  for i in range(4):
    search.append(pattern)
  offset = (page-1) * 10
  search.append(offset)

  mycursor.execute("SELECT * FROM returned_equipment WHERE EquipmentID LIKE %s OR BorrowerID LIKE %s OR Return_date LIKE %s OR Status LIKE %s ORDER BY Return_date DESC LIMIT 10 OFFSET %s", search)

  for row in mycursor:
    arr.append(row)

  mycursor.close()

  return arr

#-----Sort for borrowed_equipment table-----#
def sortEIDBorrowedEquipment(page):
  mycursor = db.cursor()
  
  offset = (page-1) * 10
  arr = []

  mycursor.execute("SELECT * FROM borrowed_equipment ORDER BY EquipmentID ASC LIMIT 10 OFFSET %s", (offset,))

  for row in mycursor:
    arr.append(row)
  
  mycursor.close()

  return arr

def sortBIDBorrowedEquipment(page):
  mycursor = db.cursor()
  
  offset = (page-1) * 10
  arr = []

  mycursor.execute("SELECT * FROM borrowed_equipment ORDER BY BorrowerID ASC LIMIT 10 OFFSET %s", (offset,))

  for row in mycursor:
    arr.append(row)
  
  mycursor.close()

  return arr

def sortDateBorrowedEquipment(page):
  mycursor = db.cursor()
  
  offset = (page-1) * 10
  arr = []

  mycursor.execute("SELECT * FROM borrowed_equipment ORDER BY Borrow_date DESC LIMIT 10 OFFSET %s", (offset,))

  for row in mycursor:
    arr.append(row)
  
  mycursor.close()

  return arr

#-----Sort for replaced_equipment table-----#
def sortEIDReplacedEquipment(page):
  mycursor = db.cursor()

  offset = (page-1) * 10
  arr = []

  mycursor.execute("SELECT * FROM replaced_equipment ORDER BY EquipmentID ASC LIMIT 10 OFFSET %s", (offset,))

  for row in mycursor:
    arr.append(row)
  
  mycursor.close()

  return arr

def sortBIDReplacedEquipment(page):
  mycursor = db.cursor()

  offset = (page-1) * 10
  arr = []

  mycursor.execute("SELECT * FROM replaced_equipment ORDER BY BorrowerID ASC LIMIT 10 OFFSET %s", (offset,))

  for row in mycursor:
    arr.append(row)
  
  mycursor.close()

  return arr

def sortDateReplacedEquipment(page):
  mycursor = db.cursor()

  offset = (page-1) * 10
  arr = []

  mycursor.execute("SELECT * FROM replaced_equipment ORDER BY Replacement_date DESC LIMIT 10 OFFSET %s", (offset,))

  for row in mycursor:
    arr.append(row)
  
  mycursor.close()

  return arr

#-----Sort for returned_equipment table-----#
def sortEIDReturnedEquipment(page):
  mycursor = db.cursor()

  offset = (page-1) * 10
  arr = []

  mycursor.execute("SELECT * FROM returned_equipment ORDER BY EquipmentID ASC LIMIT 10 OFFSET %s", (offset,))

  for row in mycursor:
    arr.append(row)
  
  mycursor.close()

  return arr

def sortBIDReturnedEquipment(page):
  mycursor = db.cursor()

  offset = (page-1) * 10
  arr = []

  mycursor.execute("SELECT * FROM returned_equipment ORDER BY BorrowerID ASC LIMIT 10 OFFSET %s", (offset,))

  for row in mycursor:
    arr.append(row)
  
  mycursor.close()

  return arr

def sortDateReturnedEquipment(page):
  mycursor = db.cursor()

  offset = (page-1) * 10
  arr = []

  mycursor.execute("SELECT * FROM returned_equipment ORDER BY Return_date DESC LIMIT 10 OFFSET %s", (offset,))

  for row in mycursor:
    arr.append(row)
  
  mycursor.close()

  return arr

def sortStatusReturnedEquipment(page):
  mycursor = db.cursor()

  offset = (page-1) * 10
  arr = []

  mycursor.execute("SELECT * FROM returned_equipment ORDER BY Status ASC LIMIT 10 OFFSET %s", (offset,))

  for row in mycursor:
    arr.append(row)
  
  mycursor.close()

  return arr

#-----Sort for professor table-----#

def sortProfID(page):
  mycursor = db.cursor()

  offset = (page-1) * 10
  arr = []

  mycursor.execute("SELECT * FROM professor ORDER BY ProfessorID ASC LIMIT 10 OFFSET %s", (offset,))

  for row in mycursor:
    arr.append(row)
  
  mycursor.close()

  return arr

def sortProfFName(page):
  mycursor = db.cursor()

  offset = (page-1) * 10
  arr = []

  mycursor.execute("SELECT * FROM professor ORDER BY FirstName ASC LIMIT 10 OFFSET %s", (offset,))

  for row in mycursor:
    arr.append(row)
  
  mycursor.close()

  return arr

def sortProfLName(page):
  mycursor = db.cursor()

  offset = (page-1) * 10
  arr = []

  mycursor.execute("SELECT * FROM professor ORDER BY LastName ASC LIMIT 10 OFFSET %s", (offset,))

  for row in mycursor:
    arr.append(row)
  
  mycursor.close()

  return arr

#-----Sort for equipment table-----#

def sortEquipmentID(page):
  mycursor = db.cursor()

  offset = (page-1) * 10
  arr = []

  mycursor.execute("SELECT * FROM equipment ORDER BY EquipmentID ASC LIMIT 10 OFFSET %s", (offset,))

  for row in mycursor:
    arr.append(row)

  mycursor.close()

  return arr

def sortEquipmentName(page):
  mycursor = db.cursor()

  offset = (page-1) * 10
  arr = []

  mycursor.execute("SELECT * FROM equipment ORDER BY Name ASC LIMIT 10 OFFSET %s", (offset,))

  for row in mycursor:
    arr.append(row)

  return arr

def sortEquipmentQty(page):
  mycursor = db.cursor()

  offset = (page-1) * 10
  arr = []

  mycursor.execute("SELECT * FROM equipment ORDER BY Quantity DESC LIMIT 10 OFFSET %s", (offset,))

  for row in mycursor:
    arr.append(row)

  return arr

def sortEquipmentCateg(page):
  mycursor = db.cursor()

  offset = (page-1) * 10
  arr = []

  mycursor.execute("SELECT * FROM equipment ORDER BY Category ASC LIMIT 10 OFFSET %s", (offset,))

  for row in mycursor:
    arr.append(row)

  return arr
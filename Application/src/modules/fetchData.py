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

  mycursor.execute("SELECT * FROM borrower WHERE BorrowerID LIKE %s OR ProfessorID LIKE %s OR FirstName LIKE %s OR LastName LIKE %s OR Program LIKE %s OR YearLevel LIKE %s ORDER BY BorrowerID ASC LIMIT 10 OFFSET %s", search)

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
  for i in range(3):
    search.append(pattern)
  offset = (page-1) * 10
  search.append(offset)
  if searched.isdigit() and len(searched) <= 2:
    mycursor.execute("SELECT * FROM equipment WHERE Available LIKE %s ORDER BY EquipmentID ASC LIMIT 10 OFFSET %s", (searched, offset,))
  else:
    mycursor.execute("SELECT * FROM equipment WHERE EquipmentID LIKE %s OR Name LIKE %s OR Category LIKE %s ORDER BY EquipmentID ASC LIMIT 10 OFFSET %s", search)

  for row in mycursor:
    arr.append(row)

  mycursor.close()

  return arr

def searchBorrowedEquipment(searched, page):
  mycursor = db.cursor()

  pattern = f"%{searched}%"
  arr = []
  search = []
  for i in range(2):
    search.append(pattern)
  offset = (page-1) * 10
  search.append(offset)

  if searched.isdigit() and len(searched) <= 3:
    mycursor.execute("SELECT * FROM borrowed_equipment WHERE EquipmentID LIKE %s ORDER BY Borrow_date DESC LIMIT 10 OFFSET %s", (pattern, offset,))
  else:
    mycursor.execute("SELECT * FROM borrowed_equipment WHERE BorrowerID LIKE %s OR Borrow_date LIKE %s ORDER BY Borrow_date DESC LIMIT 10 OFFSET %s", search)

  for row in mycursor:
    arr.append(row)

  mycursor.close()

  return arr

def searchReplacedEquipment(searched, page):
  mycursor = db.cursor()

  pattern = f"%{searched}%"
  arr = []
  search = []
  for i in range(2):
    search.append(pattern)
  offset = (page-1) * 10
  search.append(offset)

  if searched.isdigit() and len(searched) <= 3:
    mycursor.execute("SELECT * FROM replaced_equipment WHERE EquipmentID LIKE %s ORDER BY Replacement_date DESC LIMIT 10 OFFSET %s", (pattern, offset,))
  else:
    mycursor.execute("SELECT * FROM replaced_equipment WHERE BorrowerID LIKE %s OR Replacement_date LIKE %s ORDER BY Replacement_date DESC LIMIT 10 OFFSET %s", search)

  for row in mycursor:
    arr.append(row)

  mycursor.close()

  return arr

def searchReturnedEquipment(searched, page):
  mycursor = db.cursor()

  pattern = f"%{searched}%"
  arr = []
  search = []
  for i in range(3):
    search.append(pattern)
  offset = (page-1) * 10
  search.append(offset)

  if searched.isdigit() and len(searched) <= 3:
    mycursor.execute("SELECT * FROM returned_equipment WHERE EquipmentID LIKE %s  ORDER BY Return_date DESC LIMIT 10 OFFSET %s", (pattern, offset,))
  else:
    mycursor.execute("SELECT * FROM returned_equipment WHERE BorrowerID LIKE %s OR Return_date LIKE %s OR State LIKE %s ORDER BY Return_date DESC LIMIT 10 OFFSET %s", search)

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

def sortStateReturnedEquipment(page):
  mycursor = db.cursor()

  offset = (page-1) * 10
  arr = []

  mycursor.execute("SELECT * FROM returned_equipment ORDER BY State ASC LIMIT 10 OFFSET %s", (offset,))

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

  mycursor.execute("SELECT * FROM equipment ORDER BY Equipment_name ASC LIMIT 10 OFFSET %s", (offset,))

  for row in mycursor:
    arr.append(row)

  mycursor.close()

  return arr

def sortEquipmentQty(page):
  mycursor = db.cursor()

  offset = (page-1) * 10
  arr = []

  mycursor.execute("SELECT * FROM equipment ORDER BY Available DESC LIMIT 10 OFFSET %s", (offset,))

  for row in mycursor:
    arr.append(row)
  
  mycursor.close()

  return arr

def sortEquipmentCateg(page):
  mycursor = db.cursor()

  offset = (page-1) * 10
  arr = []

  mycursor.execute("SELECT * FROM equipment ORDER BY Category ASC LIMIT 10 OFFSET %s", (offset,))

  for row in mycursor:
    arr.append(row)

  mycursor.close()

  return arr

#-----Sort for borrower table-----#

def sortBorrowerID(page):
  mycursor = db.cursor()

  offset = (page-1) * 10
  arr = []

  mycursor.execute("SELECT * FROM borrower ORDER BY BorrowerID ASC LIMIT 10 OFFSET %s", (offset,))

  for row in mycursor:
    arr.append(row)

  mycursor.close()

  return arr

def sortBorrowerProfID(page):
  mycursor = db.cursor()

  offset = (page-1) * 10
  arr = []

  mycursor.execute("SELECT * FROM borrower ORDER BY ProfessorID ASC LIMIT 10 OFFSET %s", (offset,))

  for row in mycursor:
    arr.append(row)

  mycursor.close()

  return arr

def sortBorrowerFName(page):
  mycursor = db.cursor()

  offset = (page-1) * 10
  arr = []

  mycursor.execute("SELECT * FROM borrower ORDER BY FirstName ASC LIMIT 10 OFFSET %s", (offset,))

  for row in mycursor:
    arr.append(row)

  mycursor.close()

  return arr

def sortBorrowerLName(page):
  mycursor = db.cursor()

  offset = (page-1) * 10
  arr = []

  mycursor.execute("SELECT * FROM borrower ORDER BY LastName ASC LIMIT 10 OFFSET %s", (offset,))

  for row in mycursor:
    arr.append(row)

  mycursor.close()

  return arr

def sortBorrowerProg(page):
  mycursor = db.cursor()

  offset = (page-1) * 10
  arr = []

  mycursor.execute("SELECT * FROM borrower ORDER BY Program ASC LIMIT 10 OFFSET %s", (offset,))

  for row in mycursor:
    arr.append(row)

  mycursor.close()

  return arr

def sortBorrowerYearLevel(page):
  mycursor = db.cursor()

  offset = (page-1) * 10
  arr = []

  mycursor.execute("SELECT * FROM borrower ORDER BY YearLevel ASC LIMIT 10 OFFSET %s", (offset,))

  for row in mycursor:
    arr.append(row)

  mycursor.close()

  return arr


#-----All functions above are for viewing records for "All Time"-----#

#-----All functions below are for viewing records by "date range"-----#


#-----get records for the last n days for borrowed equipment-----#

#Get transactions for the last n days and sorted by EquipmentID
def getBorrowedEquipmentByEquipIdSince(days, page):
  mycursor = db.cursor()

  offset = (page-1) * 10

  mycursor.execute("SELECT * FROM borrowed_equipment WHERE Borrow_date >= DATE_SUB(CURRENT_DATE, INTERVAL %s DAY) ORDER BY EquipmentID ASC LIMIT 10 OFFSET %s", (days, offset,))

  arr = mycursor.fetchall()

  mycursor.close()

  return arr

#Get transaction for the last n days and sorted by BorrowerID
def getBorrowedEquipmentByBorrowerIdSince(days, page):
  mycursor = db.cursor()

  offset = (page-1) * 10

  mycursor.execute("SELECT * FROM borrowed_equipment WHERE Borrow_date >= DATE_SUB(CURRENT_DATE, INTERVAL %s DAY) ORDER BY BorrowerID ASC LIMIT 10 OFFSET %s", (days, offset,))

  arr = mycursor.fetchall()

  mycursor.close()

  return arr

#Get transaction for the last n days sorted by DATE DESC
#Default
def getBorrowedEquipmentByDateSince(days, page):
  mycursor = db.cursor()

  offset = (page-1) * 10

  mycursor.execute("SELECT * FROM borrowed_equipment WHERE Borrow_date >= DATE_SUB(CURRENT_DATE, INTERVAL %s DAY) ORDER BY Borrow_date DESC LIMIT 10 OFFSET %s", (days, offset,))

  arr = mycursor.fetchall()

  mycursor.close()

  return arr

#-----get records for the last n days for replaced equipment-----#

#Get transation for the last n days sorted by EquipmentID
def getReplacedEquipmentByEquipIdSince(days, page):
  mycursor = db.cursor()

  offset = (page-1) * 10

  mycursor.execute("SELECT * FROM replaced_equipment WHERE Replacement_date >= DATE_SUB(CURRENT_DATE, INTERVAL %s DAY) ORDER BY EquipmentID ASC LIMIT 10 OFFSET %s", (days, offset,))

  arr = mycursor.fetchall()

  mycursor.close()

  return arr

#Get transation for the last n days sorted by BorrowerID
def getReplacedEquipmentByBorrowerIdSince(days, page):
  mycursor = db.cursor()

  offset = (page-1) * 10

  mycursor.execute("SELECT * FROM replaced_equipment WHERE Replacement_date >= DATE_SUB(CURRENT_DATE, INTERVAL %s DAY) ORDER BY BorrowerID ASC LIMIT 10 OFFSET %s", (days, offset,))

  arr = mycursor.fetchall()

  mycursor.close()

  return arr

#Get transation for the last n days sorted by DATE DESC
#Default
def getReplacedEquipmentByDateSince(days, page):
  mycursor = db.cursor()

  offset = (page-1) * 10

  mycursor.execute("SELECT * FROM replaced_equipment WHERE Replacement_date >= DATE_SUB(CURRENT_DATE, INTERVAL %s DAY) ORDER BY Replacement_date DESC LIMIT 10 OFFSET %s", (days, offset,))

  arr = mycursor.fetchall()

  mycursor.close()

  return arr

#-----get records for the last n days for replaced equipment-----#

#Get transation for the last n days sorted by EquipmentID
def getReturnedEquipmentByEquipIdSince(days, page):
  mycursor = db.cursor()

  offset = (page-1) * 10

  mycursor.execute("SELECT * FROM returned_equipment WHERE Return_date >= DATE_SUB(CURRENT_DATE, INTERVAL %s DAY) ORDER BY EquipmentID ASC LIMIT 10 OFFSET %s", (days, offset,))

  arr = mycursor.fetchall()

  mycursor.close()

  return arr

#Get transation for the last n days sorted by BorrowerID
def getReturnedEquipmentByBorrowerIdSince(days, page):
  mycursor = db.cursor()

  offset = (page-1) * 10

  mycursor.execute("SELECT * FROM returned_equipment WHERE Return_date >= DATE_SUB(CURRENT_DATE, INTERVAL %s DAY) ORDER BY BorrowerID ASC LIMIT 10 OFFSET %s", (days, offset,))

  arr = mycursor.fetchall()

  mycursor.close()

  return arr

#Get transation for the last n days sorted by DATE DESC
#Default
def getReturnedEquipmentByDateSince(days, page):
  mycursor = db.cursor()

  offset = (page-1) * 10

  mycursor.execute("SELECT * FROM returned_equipment WHERE Return_date >= DATE_SUB(CURRENT_DATE, INTERVAL %s DAY) ORDER BY Return_date DESC LIMIT 10 OFFSET %s", (days, offset,))

  arr = mycursor.fetchall()

  mycursor.close()

  return arr

#Get transation for the last n days sorted by State
def getReturnedEquipmentByStateSince(days, page):
  mycursor = db.cursor()

  offset = (page-1) * 10

  mycursor.execute("SELECT * FROM returned_equipment WHERE Return_date >= DATE_SUB(CURRENT_DATE, INTERVAL %s DAY) ORDER BY State ASC LIMIT 10 OFFSET %s", (days, offset,))

  arr = mycursor.fetchall()

  mycursor.close()

  return arr


#-----All functions below are for viewing records by "hour range"-----#

#-----get records for the last n hour(s) for borrowed equipment-----#

#get transaction for the last n hour(s) sorted by EquipmentID
def getRecentBorrowedEquipmentByEquipId(hour, page):
  mycursor = db.cursor()

  offset = (page-1) * 10

  mycursor.execute("SELECT * FROM borrowed_equipment WHERE Borrow_date >= DATE_SUB(NOW(), INTERVAL %s HOUR) ORDER BY EquipmentID ASC LIMIT 10 OFFSET %s", (hour, offset,))

  arr = mycursor.fetchall()

  mycursor.close()

  return arr

#get transaction for the last n hour(s) sorted by BorrowerID
def getRecentBorrowedEquipmentByBorrowerId(hour, page):
  mycursor = db.cursor()

  offset = (page-1) * 10

  mycursor.execute("SELECT * FROM borrowed_equipment WHERE Borrow_date >= DATE_SUB(NOW(), INTERVAL %s HOUR) ORDER BY BorrowerID ASC LIMIT 10 OFFSET %s", (hour, offset,))

  arr = mycursor.fetchall()

  mycursor.close()

  return arr

#get transaction for the last n hour(s) sorted by HOUR DESC
#Default
def getRecentBorrowedEquipmentByDate(hour, page):
  mycursor = db.cursor()

  offset = (page-1) * 10

  mycursor.execute("SELECT * FROM borrowed_equipment WHERE Borrow_date >= DATE_SUB(NOW(), INTERVAL %s HOUR) ORDER BY Borrow_date DESC LIMIT 10 OFFSET %s", (hour, offset,))

  arr = mycursor.fetchall()

  mycursor.close()

  return arr

#-----get records for the last n hour(s) for replaced equipment-----#

#get transaction for the last n hour(s) sorted by EquipmentID
def getRecentReplacedEquipmentByEquipId(hour, page):
  mycursor = db.cursor()

  offset = (page-1) * 10

  mycursor.execute("SELECT * FROM replaced_equipment WHERE Replacement_date >= DATE_SUB(NOW(), INTERVAL %s HOUR) ORDER BY EquipmentID ASC LIMIT 10 OFFSET %s", (hour, offset,))

  arr = mycursor.fetchall()

  mycursor.close()

  return arr

#get transaction for the last n hour(s) sorted by BorrowerID
def getRecentReplacedEquipmentByBorrowerId(hour, page):
  mycursor = db.cursor()

  offset = (page-1) * 10

  mycursor.execute("SELECT * FROM replaced_equipment WHERE Replacement_date >= DATE_SUB(NOW(), INTERVAL %s HOUR) ORDER BY BorrowerID ASC LIMIT 10 OFFSET %s", (hour, offset,))

  arr = mycursor.fetchall()

  mycursor.close()

  return arr

#get transaction for the last n hour(s) sorted by DATE DESC
def getRecentReplacedEquipmentByDate(hour, page):
  mycursor = db.cursor()

  offset = (page-1) * 10

  mycursor.execute("SELECT * FROM replaced_equipment WHERE Replacement_date >= DATE_SUB(NOW(), INTERVAL %s HOUR) ORDER BY Replacement_date DESC LIMIT 10 OFFSET %s", (hour, offset,))

  arr = mycursor.fetchall()

  mycursor.close()

  return arr

#-----get records for the last n hour(s) for returned equipment-----#

#get transaction for the last n hour(s) sorted by EquipmentID
def getRecentReturnedEquipmentByEquipId(hour, page):
  mycursor = db.cursor()

  offset = (page-1) * 10

  mycursor.execute("SELECT * FROM returned_equipment WHERE Return_date >= DATE_SUB(NOW(), INTERVAL %s HOUR) ORDER BY EquipmentID ASC LIMIT 10 OFFSET %s", (hour, offset,))

  arr = mycursor.fetchall()

  mycursor.close()

  return arr

#get transaction for the last n hour(s) sorted by BorroweID
def getRecentReturnedEquipmentByBorrowerId(hour, page):
  mycursor = db.cursor()

  offset = (page-1) * 10

  mycursor.execute("SELECT * FROM returned_equipment WHERE Return_date >= DATE_SUB(NOW(), INTERVAL %s HOUR) ORDER BY BorrowerID ASC LIMIT 10 OFFSET %s", (hour, offset,))

  arr = mycursor.fetchall()

  mycursor.close()

  return arr

#get transaction for the last n hour(s) sorted by DATE DESC
def getRecentReturnedEquipmentByDate(hour, page):
  mycursor = db.cursor()

  offset = (page-1) * 10

  mycursor.execute("SELECT * FROM returned_equipment WHERE Return_date >= DATE_SUB(NOW(), INTERVAL %s HOUR) ORDER BY Return_date DESC LIMIT 10 OFFSET %s", (hour, offset,))

  arr = mycursor.fetchall()

  mycursor.close()

  return arr

#get transaction for the last n hour(s) sorted by State DESC
def getRecentReturnedEquipmentByState(hour, page):
  mycursor = db.cursor()

  offset = (page-1) * 10

  mycursor.execute("SELECT * FROM returned_equipment WHERE Return_date >= DATE_SUB(NOW(), INTERVAL %s HOUR) ORDER BY State ASC LIMIT 10 OFFSET %s", (hour, offset,))

  arr = mycursor.fetchall()

  mycursor.close()

  return arr


#------Search using match------#
def searchBorrowedEquipmentMatch(searched, page, sortState):
   mycursor = db.cursor()

   offset = (page-1) * 10

   mycursor.execute("SELECT * FROM borrowed_equipment WHERE MATCH(EquipmentID, BorrowerID, State) AGAINST(%s IN BOOLEAN MODE) ORDER BY %s ASC LIMIT 10 OFFSET %s", (searched, sortState, offset,))

   arr = mycursor.fetchall()

   mycursor.close()
   return arr
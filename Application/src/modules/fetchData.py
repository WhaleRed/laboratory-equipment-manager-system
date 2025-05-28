import os, re
from dotenv import load_dotenv
from utils import mappings
import mysql.connector

load_dotenv()

PAGE_SIZE = 10

def is_valid_equipment_id(s):
    return bool(re.match(r'^[A-Z]+(-[A-Z0-9]+)*$', s))
  
def is_valid_id(search_term):
    cleaned = ''.join(c for c in search_term if c.isdigit())
    return cleaned.isdigit()

def test():
  mycursor = db.cursor()
  
  mycursor.execute("SELECT EquipmentID FROM Equipment ORDER BY EquipmentID")
  
  arr = []
  for row in mycursor:
    arr.append(row)
  
  mycursor.close()

  return arr
  
  mycursor.close()

db = mysql.connector.connect(
  host= os.getenv("DATABASE_HOST"),
  user = os.getenv("DATABASE_USER"),
  password= os.getenv("DATABASE_PASSWORD"),
  database= os.getenv("DATABASE_NAME")

)

#-----For adding items to database-----#
def fetchEquipmentIds():
  mycursor = db.cursor()
  
  mycursor.execute("SELECT EquipmentID FROM Equipment ORDER BY EquipmentID")
  results = mycursor.fetchall()
  
  mycursor.close()
  
  return [row[0] for row in results]

def fetchEquipmentName():
  mycursor = db.cursor()
  
  mycursor.execute("SELECT Equipment_name FROM Equipment ORDER BY EquipmentID")
  results = mycursor.fetchall()
  
  mycursor.close()
  
  return [row[0] for row in results]

def fetchCategory():
  mycursor = db.cursor()
  
  mycursor.execute("SELECT Category FROM Equipment ORDER BY Category")
  results = mycursor.fetchall()
  
  mycursor.close()
  
  return [row[0] for row in results]

#-----For getting items in use-----#
def fetchItemsInUse(borrowerID, page, categoryidx=None, searched=None):
  mycursor = db.cursor()
  searchFilter = ""
  catFilter = ""
  
  offset = (page - 1) * PAGE_SIZE
  
  catFilter = ""
  params = [borrowerID]
  if categoryidx != 0:
      category = mappings.CATEGORY_MAP.get(categoryidx)
      if category:
          catFilter = "AND e.Category = %s"
          params.append(category)
                   
  if searched:
      searchFilter = "AND Equipment_name LIKE %s "
      params.insert(0, searched)
  
  count_query = f"""
        SELECT COUNT(*)
        FROM borrowed_equipment b
        INNER JOIN equipment e ON b.equipmentID = e.equipmentID
        WHERE b.borrowerID = %s {searchFilter} {catFilter}
    """
    
  mycursor.execute(count_query, params)
  count = mycursor.fetchone()[0]
    
  query = f"""
        SELECT e.Equipment_name, b.Quantity
        FROM equipment e
        INNER JOIN borrowed_equipment b ON e.equipmentID = b.equipmentID
        WHERE b.borrowerID = %s {searchFilter} {catFilter}
        LIMIT %s OFFSET %s
    """
  params += [PAGE_SIZE, offset]
  mycursor.execute(query, params)
  results = mycursor.fetchall()
  
  mycursor.close()
  
  return results, count

#-----For getting damaged items-----#
def fetchDamagedItems(borrowerID, page, categoryidx=None, searched=None):
    mycursor = db.cursor()
    searchFilter= ""
    catFilter = ""

    offset = (page - 1) * PAGE_SIZE
    
    catFilter = ""
    params = [borrowerID]
    if categoryidx != 0:
        category = mappings.CATEGORY_MAP.get(categoryidx)
        if category:
            catFilter = "AND e.Category = %s"
            params.append(category)
            
    if searched:
        searchFilter = "AND Equipment_name LIKE %s "
        params.insert(0, searched)

    count_query = f"""
        SELECT COUNT(*)
        FROM returned_equipment b
        INNER JOIN equipment e ON b.equipmentID = e.equipmentID
        WHERE b.BorrowerID = %s AND b.State = 'Damaged' {searchFilter} {catFilter}
    """
    
    mycursor.execute(count_query, params)
    count = mycursor.fetchone()[0]

    query = f"""
        SELECT e.Equipment_name, b.Quantity
        FROM equipment e
        INNER JOIN returned_equipment b ON e.equipmentID = b.equipmentID
        WHERE b.BorrowerID = %s AND b.State = 'Damaged' {searchFilter} {catFilter}
        LIMIT %s OFFSET %s
    """
    
    params += [PAGE_SIZE, offset]
    mycursor.execute(query, params)
    results = mycursor.fetchall()

    mycursor.close()

    return results, count

#-----For getting available items-----#

def fetchAvailableItems(page, categoryidx=None, searched=None):
    mycursor = db.cursor()
    
    offset = (page - 1) * PAGE_SIZE

    
    catFilter = ""
    searchFilter = ""
    params = []

    if categoryidx != 0:
        category = mappings.CATEGORY_MAP.get(categoryidx)
        if category:
            catFilter = "AND Category = %s"
            params.append(category)

    if searched:
        searchFilter = "AND Equipment_name LIKE %s "
        params.insert(0, searched)

    count_query = f"""
        SELECT COUNT(*)
        FROM equipment
        WHERE Available > 0 {searchFilter} {catFilter}
    """
    mycursor.execute(count_query, params)
    count = mycursor.fetchone()[0]

    query = f"""
        SELECT Equipment_name, Available
        FROM equipment
        WHERE Available > 0 {searchFilter} {catFilter}
        LIMIT %s OFFSET %s
    """
    params += [PAGE_SIZE, offset]
    mycursor.execute(query, params)
    results = mycursor.fetchall()
    
    mycursor.close()
    
    return results, count


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
def searchBorrowedEquipmentMatch(page, sortStateidx, dateState, searched=None):
  db.commit()
  mycursor = db.cursor()

  offset = (page-1) * 10
  params = []

  sortState = mappings.SORT_FIELDS_BORROWED.get(sortStateidx)
  if not sortState:
      return 1      #Attempt to inject
  
  dateFilter = ""
  if dateState != 0:
    if dateState not in mappings.DATE_OPTIONS:
        return 1  # Invalid dateState
    unit, value = mappings.DATE_OPTIONS[dateState]
    dateFilter = f"AND Borrow_date >= DATE_SUB(NOW(), INTERVAL {value} {unit})"
    
  if not searched:
        count_query = (
            f"SELECT COUNT(*) FROM borrowed_equipment "
            f"WHERE 1=1 {dateFilter}"
        )
  else:
    if is_valid_equipment_id(searched) or is_valid_id(searched):
      count_query = (
          f"SELECT COUNT(*) FROM borrowed_equipment "
          f"WHERE (EquipmentID = %s OR BorrowerID = %s) {dateFilter}"
      )
      params = [searched, searched]
    else:
      count_query = (
          f"SELECT COUNT(*) FROM borrowed_equipment "
          f"WHERE MATCH(EquipmentID, BorrowerID, State) "
          f"AGAINST (%s IN BOOLEAN MODE) "
          f"{dateFilter}"
      )
      params = [searched]
  
  mycursor.execute(count_query, tuple(params))
  total_count = mycursor.fetchone()[0] 
    
  if not searched: 
      query = (
          f"SELECT * FROM borrowed_equipment "
          f"WHERE 1=1 {dateFilter} "
          f"ORDER BY {sortState} ASC LIMIT 10 OFFSET %s"
      )
      mycursor.execute(query, (offset,))
  else:
    if is_valid_equipment_id(searched) or is_valid_id(searched):
      query = (
          f"SELECT * FROM borrowed_equipment "
          f"WHERE (EquipmentID = %s OR BorrowerID = %s) {dateFilter}"
          f"ORDER BY {sortState} ASC LIMIT 10 OFFSET %s"
      )
      params = [searched, searched, offset]
    else:
      query = (
          f"SELECT * FROM borrowed_equipment "
          f"WHERE MATCH(EquipmentID, BorrowerID, State) "
          f"AGAINST (%s IN BOOLEAN MODE) "
          f"{dateFilter} "
          f"ORDER BY {sortState} ASC LIMIT 10 OFFSET %s"
      )
      params = [searched, offset]
    mycursor.execute(query, tuple(params))

  arr = mycursor.fetchall()

  mycursor.close()
  return arr, total_count


def searchReturnedEquipmentMatch(page, sortStateidx, dateState, searched=None):
  db.commit()
  mycursor = db.cursor()

  offset = (page-1) * 10
  params = []

  sortState = mappings.SORT_FIELDS_RETURNED.get(sortStateidx)
  if not sortState:
      return 1      # Attempt to inject
  
  dateFilter = ""
  if dateState != 0:
    if dateState not in mappings.DATE_OPTIONS:
        return 1  # Attempt to inject
    unit, value = mappings.DATE_OPTIONS[dateState]
    dateFilter = f"AND Return_date >= DATE_SUB(NOW(), INTERVAL {value} {unit})"
    
  if not searched:
        count_query = (
            f"SELECT COUNT(*) FROM returned_equipment "
            f"WHERE 1=1 {dateFilter}"
        )
  else:
    if is_valid_equipment_id(searched) or is_valid_id(searched):
      count_query = (
          f"SELECT COUNT(*) FROM returned_equipment "
          f"WHERE (EquipmentID = %s OR BorrowerID = %s) {dateFilter}"
      )
      params = [searched, searched]
    else:
      count_query = (
          f"SELECT COUNT(*) FROM returned_equipment "
          f"WHERE MATCH(EquipmentID, BorrowerID, State) "
          f"AGAINST (%s IN BOOLEAN MODE) "
          f"{dateFilter}"
      )
      params = [searched]
  
  mycursor.execute(count_query, tuple(params))
  total_count = mycursor.fetchone()[0] 
  
  if not searched:  # if empty or None
        if sortState == "Return_date":
            query = (
                f"SELECT * FROM returned_equipment "
                f"WHERE 1=1 {dateFilter} "
                f"ORDER BY Return_date DESC LIMIT 10 OFFSET %s"
            )
            mycursor.execute(query, (offset,))
        else:
            query = (
                f"SELECT * FROM returned_equipment "
                f"WHERE 1=1 {dateFilter} "
                f"ORDER BY {sortState} ASC LIMIT 10 OFFSET %s"
            )
            mycursor.execute(query, (offset,))
  else:
    if is_valid_equipment_id(searched) or is_valid_id(searched):
      query = (
          f"SELECT * FROM returned_equipment "
          f"WHERE (EquipmentID = %s OR BorrowerID = %s) {dateFilter}"
          f"ORDER BY {sortState} ASC LIMIT 10 OFFSET %s"
      )
      params = [searched, searched, offset]
    else:
      query = (
          f"SELECT * FROM returned_equipment "
          f"WHERE MATCH(EquipmentID, BorrowerID, State) "
          f"AGAINST (%s IN BOOLEAN MODE) "
          f"{dateFilter} "
          f"ORDER BY {sortState} ASC LIMIT 10 OFFSET %s"
      )
      params = [searched, offset]
    mycursor.execute(query, tuple(params))
  
  arr = mycursor.fetchall()

  mycursor.close()
  
  return arr, total_count


def searchReplacedEquipmentMatch(page, sortStateidx, dateState, searched=None):
  db.commit()
  mycursor = db.cursor()

  offset = (page-1) * 10
  params = []

  sortState = mappings.SORT_FIELDS_REPLACED.get(sortStateidx)
  if not sortState:
      return 1      #Attempt to inject
  
  dateFilter = ""
  if dateState != 0:
    if dateState not in mappings.DATE_OPTIONS:
        return 1  # Invalid dateState
    unit, value = mappings.DATE_OPTIONS[dateState]
    dateFilter = f"AND Replacement_date >= DATE_SUB(NOW(), INTERVAL {value} {unit})"
    
  if not searched:
        count_query = (
            f"SELECT COUNT(*) FROM replaced_equipment "
            f"WHERE 1=1 {dateFilter}"
        )
  else:
    if is_valid_equipment_id(searched) or is_valid_id(searched):
      count_query = (
          f"SELECT COUNT(*) FROM replaced_equipment "
          f"WHERE (EquipmentID = %s OR BorrowerID = %s) {dateFilter}"
      )
      params = [searched, searched]
    else:
      count_query = (
          f"SELECT COUNT(*) FROM replaced_equipment "
          f"WHERE MATCH(EquipmentID, BorrowerID) "
          f"AGAINST (%s IN BOOLEAN MODE) "
          f"{dateFilter}"
      )
      params = [searched]
  
  mycursor.execute(count_query, tuple(params))
  total_count = mycursor.fetchone()[0] 
  
  if not searched:  # if empty or None
        if sortState == "Replacement_date":
            query = (
                f"SELECT * FROM replaced_equipment "
                f"WHERE 1=1 {dateFilter} "
                f"ORDER BY replacement_date DESC LIMIT 10 OFFSET %s"
            )
            mycursor.execute(query, (offset,))
        else:
            query = (
                f"SELECT * FROM replaced_equipment "
                f"WHERE 1=1 {dateFilter} "
                f"ORDER BY {sortState} ASC LIMIT 10 OFFSET %s"
            )
            mycursor.execute(query, (offset,))
  else:
    if is_valid_equipment_id(searched) or is_valid_id(searched):
      query = (
          f"SELECT * FROM replaced_equipment "
          f"WHERE (EquipmentID = %s OR BorrowerID = %s) {dateFilter}"
          f"ORDER BY {sortState} ASC LIMIT 10 OFFSET %s"
      )
      params = [searched, searched, offset]
    else:
      query = (
          f"SELECT * FROM replaced_equipment "
          f"WHERE MATCH(EquipmentID, BorrowerID) "
          f"AGAINST (%s IN BOOLEAN MODE) "
          f"{dateFilter} "
          f"ORDER BY {sortState} ASC LIMIT 10 OFFSET %s"
      )
      params = [searched, offset]
    mycursor.execute(query, tuple(params))
  
  arr = mycursor.fetchall()

  mycursor.close()
  return arr, total_count


def searchBorrowerMatch(page, sortStateidx, searched=None):
    db.commit()
    
    # Create cursor with try-finally to ensure cleanup
    mycursor = db.cursor()
    
    try:
        # Clear any existing unread results first
        try:
            while mycursor.nextset():
                pass
        except:
            pass  # No more results to clear
            
        offset = (page-1) * 10
        params = []

        sortState = mappings.SORT_FIELDS_BORROWER.get(sortStateidx)
        if not sortState:
            return 1      #Attempt to inject
        
        # Execute count query
        if not searched:
            count_query = "SELECT COUNT(*) FROM borrower WHERE 1=1"
            mycursor.execute(count_query)
        else:
            if is_valid_id(searched):
                count_query = "SELECT COUNT(*) FROM borrower WHERE BorrowerID = %s"
                params = [searched]
            else:
                count_query = (
                    "SELECT COUNT(*) FROM borrower "
                    "WHERE MATCH(ProfessorID, BorrowerID, FirstName, LastName, Program, YearLevel) "
                    "AGAINST (%s IN BOOLEAN MODE)"
                )
                params = [searched]
            mycursor.execute(count_query, tuple(params))

        total_count = mycursor.fetchone()[0]
        
        # Consume any remaining results from count query
        try:
            mycursor.fetchall()  # This ensures no unread results remain
        except:
            pass
            
        # Close the cursor and create a new one for main query
        mycursor.close()
        mycursor = db.cursor()
        
        # Execute main query
        if not searched:
            query = (
                f"SELECT * FROM borrower "
                f"ORDER BY {sortState} ASC LIMIT 10 OFFSET %s"
            )
            mycursor.execute(query, (offset,))
        else:
            if is_valid_id(searched):
                query = (
                    f"SELECT * FROM borrower "
                    f"WHERE BorrowerID = %s "
                    f"ORDER BY {sortState} ASC LIMIT 10 OFFSET %s"
                )
                params = [searched, offset]
            else:
                query = (
                    f"SELECT * FROM borrower "
                    f"WHERE MATCH(ProfessorID, BorrowerID, FirstName, LastName, Program, YearLevel) "
                    f"AGAINST (%s IN BOOLEAN MODE) "
                    f"ORDER BY {sortState} ASC LIMIT 10 OFFSET %s"
                )
                params = [searched, offset]
            mycursor.execute(query, tuple(params))

        arr = mycursor.fetchall()
        
        return arr, total_count
        
    except Exception as e:
        print(f"Database error in searchBorrowerMatch: {e}")
        import traceback
        traceback.print_exc()
        return 1
        
    finally:
        # Always close the cursor, even if there's an exception
        try:
            mycursor.close()
        except:
            pass


def searchEquipmentMatch(page, sortStateidx, categoryidx, searched=None):
  db.commit()
  mycursor = db.cursor()

  offset = (page-1) * 10
  params = []

  sortState = mappings.SORT_FIELDS_EQUIPMENT.get(sortStateidx)
  if not sortState:
      return 1      #Attempt to inject
    
  category = mappings.CATEGORY_MAP.get(categoryidx)

  catFilter = ""
  
  if category is not None:
        catFilter = "AND Category = %s "
        params.append(category)
        
  if not searched:
        count_query = (
            f"SELECT COUNT(*) FROM equipment "
            f"WHERE 1=1 {catFilter}"
        )
        mycursor.execute(count_query, params)
  else:
    if is_valid_equipment_id(searched):
      count_query = (
          f"SELECT COUNT(*) FROM equipment "
          f"WHERE EquipmentID = %s"
          f"{catFilter}"
      )
      params = [searched]
    else:
      count_query = (
          f"SELECT COUNT(*) FROM equipment "
          f"WHERE MATCH(EquipmentID, Equipment_name, Category) AGAINST (%s IN BOOLEAN MODE) "
          f"{catFilter}"
      )
      params = [searched]
    mycursor.execute(count_query, params)
  total_count = mycursor.fetchone()[0]
  
  if not searched:
        query = (
            f"SELECT * FROM equipment "
            f"WHERE 1=1 {catFilter}"
            f"ORDER BY {sortState} ASC LIMIT 10 OFFSET %s"
        )
        params.append(offset)
        mycursor.execute(query, params)
  else:
    if is_valid_equipment_id(searched) or is_valid_id(searched):
      query = (
          f"SELECT * FROM equipment "
          f"WHERE EquipmentID = %s "
          f"{catFilter}"
          f"ORDER BY {sortState} ASC LIMIT 10 OFFSET %s"
      )
      params = [searched, offset]
    else:
      query = (
          f"SELECT * FROM equipment "
          f"WHERE MATCH(EquipmentID, Equipment_name, Category) AGAINST (%s IN BOOLEAN MODE) "
          f"{catFilter}"
          f"ORDER BY {sortState} ASC LIMIT 10 OFFSET %s"
      )
      params = [searched, offset]
    mycursor.execute(query, tuple(params))

  arr = mycursor.fetchall()

  mycursor.close()
  return arr, total_count


def searchProfessorMatch(page, sortStateidx, searched=None):
  db.commit()
  mycursor = db.cursor()

  offset = (page-1) * 10

  sortState = mappings.SORT_FIELDS_PROFESSOR.get(sortStateidx)
  if not sortState:
      return 1      #Attempt to inject
  
  if not searched:
        count_query = (
            f"SELECT COUNT(*) FROM professor "
            f"WHERE 1=1"
        )
        mycursor.execute(count_query)
  else: 
    if is_valid_id(searched):
      count_query = (
          f"SELECT COUNT(*) FROM professor "
          f"WHERE ProfessorID = %s"
      )
      params = [searched]
    else:
      count_query = (
          f"SELECT COUNT(*) FROM professor "
          f"WHERE MATCH(ProfessorID, FirstName, LastName) AGAINST (%s IN BOOLEAN MODE)"
      )
      params = [searched]
    mycursor.execute(count_query, params)
  total_count = mycursor.fetchone()[0]
  
  if not searched:
        query = (
            f"SELECT * FROM professor "
            f"ORDER BY {sortState} ASC LIMIT 10 OFFSET %s"
        )
        mycursor.execute(query, (offset,))
  else:
    if is_valid_id(searched):
      query = (
          f"SELECT * FROM professor "
          f"WHERE ProfessorID = %s"
          f"ORDER BY {sortState} ASC LIMIT 10 OFFSET %s"
      )
      params = [searched, offset]
    else:
      query = (
          f"SELECT * FROM professor "
          f"WHERE MATCH(ProfessorID, FirstName, LastName) "
          f"AGAINST (%s IN BOOLEAN MODE) "
          f"ORDER BY {sortState} ASC LIMIT 10 OFFSET %s"
      )
      params = [searched, offset]
    mycursor.execute(query, tuple(params))

  arr = mycursor.fetchall()

  mycursor.close()
  return arr, total_count


def fetchProfID():
  mycursor = db.cursor()
  
  mycursor.execute("SELECT ProfessorID FROM Professor ORDER BY ProfessorID")
  results = mycursor.fetchall()
  
  mycursor.close()
  
  return [row[0] for row in results]

def fetchBorrower(idnum):
  mycursor = db.cursor()
  
  mycursor.execute("SELECT * FROM borrower WHERE BorrowerID = %s",(idnum,))
  results = mycursor.fetchall()
  
  mycursor.close()
  return results

def fetchProfessor(idnum):
  mycursor = db.cursor()
  
  mycursor.execute("SELECT * FROM professor WHERE ProfessorID = %s",(idnum,))
  results = mycursor.fetchall()
  
  mycursor.close()
  return results

def fetch_EquipmentName(equipment_name):
   mycursor = db.cursor()

   mycursor.execute("SELECT * FROM equipment WHERE Equipment_name = %s", (equipment_name,))
   results = mycursor.fetchall()

   mycursor.close()
   return results

def fetchEquipmentData(idnum):
  mycursor = db.cursor()
  
  mycursor.execute("SELECT * FROM equipment WHERE EquipmentID = %s",(idnum,))
  results = mycursor.fetchall()
  
  mycursor.close()
  return results  
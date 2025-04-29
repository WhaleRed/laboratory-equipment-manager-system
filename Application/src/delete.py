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

def delBorrower(idnum):        

  mycursor = db.cursor()

  mycursor.execute("DELETE FROM borrower WHERE BorrowerID = %s", (idnum,))
  db.commit()
  mycursor.close()

def delProfessor(idnum):        

  mycursor = db.cursor()

  mycursor.execute("DELETE FROM professor WHERE ProfessorID = %s", (idnum,))
  db.commit()
  mycursor.close()

def delEquipment(idnum):        

  mycursor = db.cursor()

  mycursor.execute("DELETE FROM equipment WHERE EquipmentID = %s", (idnum,))
  db.commit()
  mycursor.close()
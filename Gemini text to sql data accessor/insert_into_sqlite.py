import sqlite3

connection = sqlite3.connect("STUDENT.db") #Connect to SQlite database
cursor = connection.cursor() #Create a cursor object to create table and insert record

#Create table
table_info = """
Create table IF NOT EXISTS STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25), SECTION VARCHAR(25));
"""
cursor.execute(table_info)

#Insert records
cursor.execute('''INSERT INTO STUDENT values('Krish', 'AI', 'A')''')
cursor.execute('''Insert Into STUDENT values('Raj', 'SDE', 'B')''')
cursor.execute('''Insert Into STUDENT values('Jaya', 'AI', 'A')''')
cursor.execute('''Insert Into STUDENT values('Mohan', 'OS', 'B')''')
cursor.execute('''Insert Into STUDENT values('Hari', 'DS', 'C')''')
cursor.execute('''Insert Into STUDENT values('Pavan', 'OS', 'A')''')

#Dislay the records in table STUDENT
print("Records : ")
data = cursor.execute('''Select * FROM STUDENT''')
for row in data:
    print(row)
    
connection.commit()
connection.close()
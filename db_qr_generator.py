import sqlite3
import qrcode
import os

### Initializing values for DB creation
db_name="mydatabase.db"
table_name='inventory'
qr_folder = "QR_Codes" 

name="Olive"
barcode="OL-finnishbrand-005"
rackdetails="H67-R9-C1" 
quantity=9


class db_Qr():  
    def __init__(self, db_name, table_name, name, barcode, rackdetails, quantity, qr_folder):
        self.table_name=table_name
        self.db_name=db_name
        self.name=name
        self.barcode=barcode
        self.rackdetails=rackdetails
        self.quantity=quantity
        self.qr_folder=qr_folder
    
    ### This function add values to database ::
    def db_table(self):
        print(self.db_name)
        db = sqlite3.connect(self.db_name)
        cur = db.cursor()
        # id is the primary key for the table: 
        # you can change if necessary.
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            barcode TEXT,
            rackdetails TEXT,
            quantity TEXT
            )
            """.format(table_name=self.table_name))

        cur.execute("INSERT INTO Inventory ( name, barcode, rackdetails, quantity ) VALUES ( ?, ?, ? ,?)", (self.name, self.barcode,self.rackdetails, self.quantity))
        #cur.execute("INSERT INTO Inventory (id, name, barcode, rackdetails, quantity ) VALUES (?, ?, ?, ? ,?)", (2, "cola", "CL-finishbrand-005", "H59-R9-C5", 4))
        #cur.execute("INSERT INTO Inventory (id, name, barcode, rackdetails, quantity ) VALUES (?, ?, ?, ? ,?)", (3, "cup", "Cp-finishbrand-009", "H14-R8-C6", 4))
        db.commit()
        db.close()
    
    ## This is to generate QR codes for existing DB    
    def generate_QR(self):
        # Connect to the SQLite database (replace 'your_database.db' with your actual database file)
        conn = sqlite3.connect(self.db_name)

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # Execute a SELECT query to fetch all rows from your table
        cursor.execute('SELECT rackdetails FROM inventory')

        # Fetch all the rows as a list of tuples
        rows = cursor.fetchall()

        count=1
        # Iterate through the rows and print the values ('title' is one of the columns)
        for row in rows:
            data= row[0]  # index of the title column
            qr = qrcode.QRCode(version = 1,
                        box_size = 10,
                        border = 5)
        
            # Adding data to the instance 'qr'
            qr.add_data(data)
        
            qr.make(fit = True)
            img = qr.make_image(fill_color = 'black',
                            back_color = 'white')

            qr_code_path = os.path.join(self.qr_folder, f'QR{count}.png')
            img.save(qr_code_path)
            count +=1
            
    def main(self):
        self.db_table()
        self.generate_QR()
        

if __name__ == '__main__':
   m = db_Qr(db_name, table_name,  name, barcode, rackdetails, quantity, qr_folder )
   m.main()
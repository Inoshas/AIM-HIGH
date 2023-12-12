#from datetime import datetime
#import time

import sqlite3
import qrcode
import cv2
import os

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
            img = qr.make_image(fill_color = 'red',
                            back_color = 'white')

            qr_code_path = os.path.join(self.qr_folder, f'QR{count}.png')
            img.save(qr_code_path)
            count +=1



##############################################################################

class process_QR():
    
    def __init__(self, pair, color,dist):
        self.pair=pair
        self.color=color
        self.dist=dist

    ### Stop motors when detect red :::
    def stop_motors(self):
        print(self.color.get_color())
        if self.color.get_color()=='red':
            self.pair.stop()
        
    ## This function is to turn right:
    ## We dont need to write this again, we can call the previous class      
    def turn_move(self):
        pass 
    
    ## This function need to replace with camera reading and decoding QR code::
    def read_QR(self):
        # Name of the QR Code Image file
        filename = "QR2.png"
        # read the QRCODE image
        image = cv2.imread(filename)
        # initialize the cv2 QRCode detector
        detector = cv2.QRCodeDetector()
        # detect and decode
        data, vertices_array, binary_qrcode = detector.detectAndDecode(image)
        # if there is a QR code
        # print the data
        if vertices_array is not None:
            print("QRCode data:")
            print(data)
        else:
            print("There was some error") 

    
    # This function is to match the QR code output with existing one::
    def match_QR():
        pass
        
    #This function is to notify the shop about mismatches   
    def notify():
        pass
        
    ##Rather calling all functions in main, we can define one function to call above functions
    # like phase 1: then we need only one line to procedd phase 1 
    def QR_final_process():
        #1.stop motors when detect red
        #2. read QR code 
        #3. get the picture of the product
        #4. comparison
        #5. notify 
        pass
    


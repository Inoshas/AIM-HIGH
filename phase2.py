
import cv2
<<<<<<< HEAD
from picamera2 import Picamera2
import sqlite3
=======
import os
from picamera2 import Picamera2

>>>>>>> 76ba6222bbcc5ac2d43aa95cdd643d7ed4795bf7

data=None
##############################################################################

class process_QR():
<<<<<<< HEAD
    
    def __init__(self, pair, color,dist,picam,db_name):
=======
    '''
    def __init__(self, pair, color,dist):
>>>>>>> 76ba6222bbcc5ac2d43aa95cdd643d7ed4795bf7
        self.pair=pair
        self.color=color
        self.dist=dist
        self.picam=picam
        self.db_name=db_name

<<<<<<< HEAD

    ### Stop motors when detect red and start reading QR code:::
    def pass_QR(self):
        self.pair.stop()
        self.read_QR()
        
=======
    ### Stop motors when detect red :::
    def stop_motors(self):
        print(self.color.get_color())
        if self.color.get_color()=='red':
            self.pair.stop()
    '''
      
    ## This function is to turn right:
    ## We dont need to write this again, we can call the previous class 
    ### or we can also fix camera to side..     
    def turn_move(self):
        pass 
>>>>>>> 76ba6222bbcc5ac2d43aa95cdd643d7ed4795bf7
    
    ## This function will read the QR code and exit the 'if loop'
    # if it has detect  the QR code::
    def read_QR(self):
<<<<<<< HEAD
        global data
        # start the picam
        self.picam.start()
        # define QR detector
        detector = cv2.QRCodeDetector()
        while True:
            # Note that picam always capture pictures as arrays
            frame=self.picam.capture_array()
            _=self.picam.capture_array()
            #_, frame = picam.read()
            data, bbox, _ = detector.detectAndDecode(frame)
            # make the box around QR code
            if(bbox is not None):
                bb_pts = bbox.astype(int).reshape(-1, 2)
                num_bb_pts = len(bb_pts)
                for i in range(num_bb_pts):
                    cv2.line(frame,
                            tuple(bb_pts[i]),
                            tuple(bb_pts[(i+1) % num_bb_pts]),
                            color=(255, 0, 255), thickness=2)
                    # Here read the frame data:
                    cv2.putText(frame, data,
                            (bb_pts[0][0], bb_pts[0][1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 255, 0), 2)
                # If you read the QR code: disable camera and move forward
                if data:
                    print("data found: ", data)
                    self.picam.stop()
                    self.match_QR()
                    self.pair.run_for_rotations(1,-15,15)
                    return
        # Destroy all windows::            
        cv2.destroyAllWindows()


    # This function is to match the QR code output with existing one::
    # And for now we are updating the quantity of the relevant QRcode product:::
    def match_QR(self):
        global data
        con = sqlite3.connect(self.db_name)

        # Create a cursor object to execute SQL queries
        cursor = con.cursor()
        # Update DB inventory quantity column
        query_update = "UPDATE inventory SET quantity = quantity + 1 WHERE rackdetails = ?"
        cursor.execute(query_update, (data,))

        # Commit the changes
        con.commit()

        # Execute a SELECT query to fetch the updated quantity
        query_select = "SELECT quantity FROM inventory WHERE rackdetails = ?"
        cursor.execute(query_select, (data,))
        updated_quantity = cursor.fetchone()[0]
        
        # Execute a SELECT query to fetch the updated quantity
        query_select = "SELECT name FROM inventory WHERE rackdetails = ?"
        cursor.execute(query_select, (data,))
        name_col = cursor.fetchone()[0]

        # Close the cursor and connection
        cursor.close()
        con.close()

        # Print the updated quantity
        print(f"Quantity updated. {name_col} and its new quantity: {updated_quantity} ")
        print("***************")
    
        # Iterate through the rows and print the values ('title' is one of the columns)
        
    #These functions are for expansions:::
    def object_detect():
        pass
    def notify(self):
=======
        picam = Picamera2()
        picam.preview_configuration.main.size=(640,480)
        picam.preview_configuration.main.format="RGB888"
        picam.preview_configuration.align()
        picam.configure("preview")
        picam.start()
        detector = cv2.QRCodeDetector()
        while True:
            frame=picam.capture_array()
            _=picam.capture_array()
            #_, frame = picam.read()
            data, bbox, _ = detector.detectAndDecode(frame)
            if(bbox is not None):
                bb_pts = bbox.astype(int).reshape(-1, 2)
                num_bb_pts = len(bb_pts)
                for i in range(num_bb_pts):
                    cv2.line(frame,
                            tuple(bb_pts[i]),
                            tuple(bb_pts[(i+1) % num_bb_pts]),
                            color=(255, 0, 255), thickness=2)
                    cv2.putText(frame, data,
                            (bb_pts[0][0], bb_pts[0][1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 255, 0), 2)
                if data:
                    print("data found: ", data)
            cv2.imshow("picam",frame)
            if cv2.waitKey(1)==ord('q'):
                break
        cv2.destroyAllWindows()
        
   
        '''
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
        '''

    # This function is to match the QR code output with existing one::
    def match_QR(self):
        pass
        
        
    #This function is to notify the shop about mismatches   
    def notify(self):
        pass
        
    ##Rather calling all functions in main, we can define one function to call above functions
    # like phase 1: then we need only one line to procedd phase 1 
    def QR_final_process(self):
        #1.stop motors when detect red
        #2. read QR code 
        #3. get the picture of the product
        #4. comparison
        #5. notify 
>>>>>>> 76ba6222bbcc5ac2d43aa95cdd643d7ed4795bf7
        pass
    
        
 
    


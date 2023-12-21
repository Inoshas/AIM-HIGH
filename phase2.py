
import cv2
from picamera2 import Picamera2
import sqlite3
import os
import time
import sys
sys.path.append("/yolov5")
from yolov5 import detect


data=None

   
##############################################################################

                    
class process_QR():
    
    def __init__(self, pair, color,dist,picam,db_name):
        self.pair=pair
        self.color=color
        self.dist=dist
        self.picam=picam
        self.db_name=db_name


    ### Stop motors when detect red and start reading QR code:::
    def pass_QR(self):
        self.pair.stop()
        self.read_QR()
        
    
    ## This function will read the QR code and exit the 'if loop'
    # if it has detect  the QR code::
    def read_QR(self):
        global data
        image_folder = os.path.join("yolov5", "data", "images")
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)
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
                    image_path = os.path.join(image_folder, "QR_detect.jpg")
                    cv2.imwrite(image_path, frame)
                    time.sleep(3)
                    self.picam.stop()
                    detect.yolo5_run()
                    #self.match_QR()
                    self.pair.run_for_rotations(1,-15,15)
                    print('leaving loop')
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
        pass
    
        
 
    


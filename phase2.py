
import cv2
import os
from picamera2 import Picamera2


##############################################################################

class process_QR():
    '''
    def __init__(self, pair, color,dist):
        self.pair=pair
        self.color=color
        self.dist=dist

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
    
    ## This function need to replace with camera reading and decoding QR code::
    def read_QR(self):
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
        pass
    


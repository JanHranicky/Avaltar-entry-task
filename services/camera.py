import cv2
from processing.frame_transformer import FrameTransformer
from processing.people_detection import PeopleDetection
import time

class Camera(object):
    test_video_path = './static/test2.mp4'
    
    def __init__(self):
        self.cap = cv2.VideoCapture(self.test_video_path)
        
        self.transformer = FrameTransformer()
        self.transformer.add_transformation(PeopleDetection())

    def get_frame(self):
        ret, frame = self.cap.read()
        
        # If the video ends, restart it
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read() #read another frame

        frame = self.transformer.transform(frame) #apply all transformations for the frame
        
        fourcc = cv2.VideoWriter_fourcc(*'theo')
        _, img_encoded = cv2.imencode('.jpg', frame)
        
        return img_encoded.tobytes()
    
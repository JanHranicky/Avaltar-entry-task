import cv2
from processing.frame_transformer import FrameTransformer
from processing.people_detection import PeopleDetection

class Camera(object):
    test_video_path = './static/test2.mp4'
    
    def __init__(self):
        self.cap = cv2.VideoCapture(self.test_video_path)
        
        self.transformer = FrameTransformer()
        self.transformer.add_transformation(PeopleDetection())

    def get_resolution(self):
        return (int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)))

    def get_frame(self, encode_jpg=False):
        ret, frame = self.cap.read()
        
        # If the video ends, restart it
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read() #read another frame

        frame = self.transformer.transform(frame) #apply all transformations for the frame
        
        if encode_jpg:
            _, img_encoded = cv2.imencode('.jpg', frame)
            frame = img_encoded.tobytes()
            
        return frame
    
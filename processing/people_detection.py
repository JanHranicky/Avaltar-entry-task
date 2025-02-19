from processing.frame_transformation_interface import FrameTransformation
import cv2
from ultralytics import YOLO
import random
from flask import current_app

class PeopleDetection(FrameTransformation):
    def __init__(self):
        super().__init__()
        self.model = current_app.config['YOLOV8']
        
    def apply(self, frame):
        predicted_bbs = self._get_bb_prediction(frame)
        return self._plot_bbs(frame, predicted_bbs)
    
    def _get_bb_prediction(self, frame):
        PERSON_CLASS_KEY = 0
        detection_class_list = [PERSON_CLASS_KEY]
        
        result = self.model(frame)
        
        bb_list = []    
        for r in result:
            for box, cls, conf in zip(r.boxes.xyxyn, r.boxes.cls, r.boxes.conf):
                if int(cls) in detection_class_list:
                    bb = {
                        'class': int(cls.item()),
                        'confidence': float(conf.item()),
                        'xyxyn': box.tolist(),
                    }
                    bb_list.append(bb)
            
        return bb_list

    def _plot_bbs(self, frame, bbs):
        COLOR_GREEN = (0, 255, 0)
        h, w, _ = frame.shape 
        for bb in bbs:
            x_min, y_min, x_max, y_max = bb['xyxyn'][:4] 
            x_min, y_min = int(x_min * w), int(y_min * h)
            x_max, y_max = int(x_max * w), int(y_max * h)

            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

            label = f"{self.model.names[bb['class']]}, conf:{round(bb['confidence'],2)}"
            cv2.putText(frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_GREEN, 2)
        return frame    
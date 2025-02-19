import cv2
from ultralytics import YOLO
import random 

def stream_video(model, video_path):
    # Open video file
    cap = cv2.VideoCapture(video_path)

    while True:
        ret, frame = cap.read()
        
        # If the video ends, restart it
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        predicted_bbs = get_bb_prediction(model, frame)
        frame = plot_bbs(model, frame, predicted_bbs)
        
        cv2.imshow("Video Stream", frame)

        # Press 'q' to quit
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def get_bb_prediction(model, frame):
    PERSON_CLASS_KEY = 0
    detection_class_list = [PERSON_CLASS_KEY]
    
    result = model(frame)
    
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

def plot_bbs(model, frame, bbs):
    COLOR_GREEN = (0, 255, 0)
    h, w, _ = frame.shape 
    for bb in bbs:
        x_min, y_min, x_max, y_max = bb['xyxyn'][:4] 
        x_min, y_min = int(x_min * w), int(y_min * h)
        x_max, y_max = int(x_max * w), int(y_max * h)

        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

        label = f"{model.names[bb['class']]}, conf:{round(bb['confidence'],2)}"
        cv2.putText(frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_GREEN, 2)
    return frame

if __name__ == '__main__':
    TEST_VIDEO_PATH = '../video1.mp4'
    model = YOLO('yolov8n.pt')
    
    stream_video(model, TEST_VIDEO_PATH)
    
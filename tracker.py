
import time
from YoloDetector import YoloDetector
import cv2
from centroidtracker import CentroidTracker
from shapely.geometry import Polygon
import numpy as np

file_path = r"model/classes.txt"
classes = []
color_name = {}
dir_r_check_3, dir_l_check_3 = 0, 0
flag, skip, id_check_list, object_id, count, old_x1_value, direction, direction_diction = False, 0, [], 0, 0, [], {}, {}
result = cv2.VideoWriter('./TSF.avi', cv2.VideoWriter_fourcc(*'MJPG'), 3, (960, 540))
tracker = CentroidTracker(maxDisappeared=30, maxDistance=50)
tracker_line_coordinates = [550, 330, 1250,330]
f = open(file_path, "r")
for x in f:
    classes.append(x.strip())
detector = YoloDetector("model/yolov3-tiny-obj.cfg", "model/yolov3-tiny-obj_last.weights", classes)
cap = cv2.VideoCapture("Video/6-2-SF-CoreShop_Error.mp4")
ret, frame = cap.read()
ft = 10
print("Classes are", classes)


def intersect(box1, box2):
    global flag, skip
    thresh = 2
    x1, y1, x2, y2 = box1
    a1, b1, a2, b2 = box2
    p1 = Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])
    p2 = Polygon([(a1, b1), (a2, b1), (a2, b2), (a1, b2)])
    if p1.intersects(p2):
        flag = True
    else:
        if skip >= thresh:
            skip = 0
            flag = False
        skip += 1
    return flag


def find_centroid(tracker_coordinates):
    x1, y1, x2, y2 = tracker_coordinates
    x_center = int((x1 + x2) / 2)
    y_center = int((y1 + y2) / 2)
    return x_center, y_center


'''def find_direction(tracker_coordinates, obj_id):
    global old_x1_value, dir_r_check_3, dir_l_check_3, direction
    x1, y1, x2, y2 = tracker_coordinates
    old_x1_value.append(x1)
    if len(old_x1_value) > 2:
        if x1 > old_x1_value[-2]:
            dir_r_check_3 += 1
            if dir_r_check_3 > 3:
                if obj_id not in direction.keys():
                    direction[obj_id] = "Bottum to Top"
                    print("{}'s direction is Bottum to Top".format(obj_id))
        else:
            dir_r_check_3 = 0
        if x1 < old_x1_value[-2]:
            dir_l_check_3 += 1
            if dir_l_check_3 > 3:
                if obj_id not in direction.keys():
                    direction[obj_id] = "Top to Bottum"
                    print("{}'s direction is Top to Bottum".format(obj_id))
        else:
            dir_l_check_3 = 0
    return direction'''


def tracker_call(detection_results, img):
    global count, object_id, id_check_list, flag, direction_diction 
    cv2.line(img, (tracker_line_coordinates[0], tracker_line_coordinates[1]),
             (tracker_line_coordinates[2], tracker_line_coordinates[3]), (0, 0, 255), thickness=2)
    proper_coordinates_list = [item for t in detection_results[classes[1]] for item in t]
    if len(detection_results[classes[0]]) > 0:

        print("core:", detection_results[classes[0]], "pin:", detection_results[classes[1]])
        a=len(detection_results[classes[0]])
        b=len(detection_results[classes[1]])
        print("core:",a)
        print("pin:",b)
        tracker_out1 = tracker.update(detection_results[classes[0]])
        tracker_out2 = tracker.update(detection_results[classes[1]])
        c=len(tracker_out1)
        print("Tracker Count:",c)
        tracker_out = {**tracker_out1, **tracker_out2}
 
                
        print("////", tracker_out1)
        
        for (tracker_id, coord) in tracker_out1.items():
            
            object_id = tracker_id
            x_c, y_c = find_centroid(coord)
            cv2.circle(img, (x_c, y_c), 7, (255, 255, 0), -1)
            #direction_diction = find_direction(coord, object_id)
        flag = intersect(coord, tracker_line_coordinates)
        
        if flag and count < 1:
            int
            id_check_list.append(object_id)
            count += 1
        if flag and object_id != id_check_list[-1]:
            id_check_list.append(object_id)
                        
        if  (len(tracker_out) != 6):
           
                cv2.putText(img, "Status : {}".format('core violation'), (1000, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0),thickness=3)
    img = draw_on_frame(img, detection_results)
    
    
    cv2.putText(frame, ("Count = {}".format(len(detection_results[classes[0]]))), (800, 60), fontFace=cv2.FONT_HERSHEY_COMPLEX,
                fontScale=1, color=(0, 255, 255), thickness=2)
        

            
    '''diction_key = list(direction_diction.keys())
    if len(direction_diction) > 0:
        cv2.putText(frame, "Direction = {}".format(direction_diction[diction_key[-1]]), (800, 110),
                    fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, color=(0, 255, 255), thickness=2)'''
    return img


def draw_on_frame(img, detection_result):
    for cls, objs in detection_result.items():
        if classes[0] == cls:
            for x1, y1, x2, y2 in objs:
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(img, cls, (x1, y1 - 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), thickness=2)
        elif classes[1] == cls:
            for x1, y1, x2, y2 in objs:
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, cls, (x1, y1 - 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), thickness=2)
        '''elif classes[2] == cls:
            for x1, y1, x2, y2 in objs:
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(img, cls, (x1, y1 - 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), thickness=2)
        elif classes[3] == cls:
            for x1, y1, x2, y2 in objs:
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 0), 2)
                cv2.putText(img, cls, (x1, y1 - 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), thickness=2)
        elif classes[4] == cls:
            for x1, y1, x2, y2 in objs:
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
                cv2.putText(img, cls, (x1, y1 - 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), thickness=2)'''
    return img


while cap.isOpened():
    start_time = time.time()
    ret, frame = cap.read()
    ret, frame = cap.read()
    ret, frame = cap.read()
    results = detector.detect(frame, conf=0.2)
    frame = tracker_call(results, frame)
    frame = cv2.resize(frame, None, fx=0.50, fy=0.50)
   # print(frame.shape)
    cv2.putText(frame, "FPS: %.2f" % (1/(time.time()-start_time)), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0, 0, 0), thickness=2)
    #print(frame.shape)
    cv2.imshow("frame", frame)
    result.write(frame)
    key = cv2.waitKey(ft) & 0xFF
    if key == ord('q'):
        break
cap.release()
result.release()
cv2.destroyAllWindows()
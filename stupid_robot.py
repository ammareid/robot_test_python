import time
from datetime import datetime
from rplidar import RPLidar


############ Main Code ############

right_object_detected = False
left_object_detected = False

OBSTACLE_THRESHOLD = 500
Right_angle_threshhold = 45
Left_angle_threshhold = 315

lidar = RPLidar('COM3',baudrate=115200)

info = lidar.get_info()
print(info)

health = lidar.get_health()
print(health)

for scanNo, scan in enumerate(lidar.iter_scans()):
    # right meaning 0 < angle < 45
    # left meaning 315 < angle < 360
    right_object_detected = False
    left_object_detected = False


    
    for lineNo, line in enumerate(scan):
        angle = line[1]
        distance = line[2]
        
        if ( (0 < angle) and (angle < Right_angle_threshhold)) and (distance<OBSTACLE_THRESHOLD):
            right_object_detected = True
#             print("Right Detected. Angle:",angle, "Distance: ", distance)
        elif ((Left_angle_threshhold < angle) and (angle < 360)) and (distance<OBSTACLE_THRESHOLD):
            left_object_detected = True
            
    print("Right: ", right_object_detected, ", Left:", left_object_detected)
    
    
    
    if right_object_detected and left_object_detected:
        #go_left(2)
        print("Full left")
        time.sleep(2)
    elif right_object_detected :
#         go_left(1.5)
        print("Go left")
        time.sleep(1.5)
    elif left_object_detected:
#         go_right(1.5) 
        print("Go right")
        time.sleep(1.5)
    else :
#         go_forward()
        print("Forward")
     
        
    #if scanNo >= 100:
      #  break

# scan = lidar.iter_scans()

lidar.stop()
lidar.stop_motor()
lidar.disconnect()

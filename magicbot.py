import RPi.GPIO as GPIO
import time
from datetime import datetime
from rplidar import RPLidar
ignore_scan = True

# Set GPIO mode and pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
IN1 = 17
IN2 = 18
IN3 = 27
IN4 = 22
ENA = 23  # Enable pin for motor A
ENB = 24  # Enable pin for motor B

# Set PWM frequency and duty cycle
PWM_FREQ = 1000  # PWM frequency in Hz
DUTY_CYCLE = 50  # Initial duty cycle (0-100)

# Setup GPIO pins as output
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)

# Create PWM objects for motor control
pwm_a = GPIO.PWM(ENA, PWM_FREQ)
pwm_b = GPIO.PWM(ENB, PWM_FREQ)

# Start PWM with initial duty cycle
pwm_a.start(DUTY_CYCLE)
pwm_b.start(DUTY_CYCLE)

# Function to go forward
def go_forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

# Function to go right
def go_right(angle):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    time.sleep(angle)  # Adjust the sleep duration based on gyro readings
    ignore_scan=True
    

# Function to go left
def go_left(angle):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    time.sleep(angle)  # Adjust the sleep duration based on gyro readings
    ignore_scan=True

# Function to change motor speed
def change_speed(duty_cycle):
    pwm_a.ChangeDutyCycle(duty_cycle)
    pwm_b.ChangeDutyCycle(duty_cycle)

############ Main Code ############

right_object_detected = False
left_object_detected = False

OBSTACLE_THRESHOLD = 500
Right_angle_threshhold = 45
Left_angle_threshhold = 315

lidar = RPLidar('/dev/ttyUSB0')

info = lidar.get_info()
print(info)

health = lidar.get_health()
print(health)
while(True):
    try:
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
                elif ((Left_angle_threshhold < angle) and (angle < 360)) and (distance<OBSTACLE_THRESHOLD):
                    left_object_detected = True
                    
            print("Right: ", right_object_detected, ", Left:", left_object_detected)

            if(ignore_scan==True)
                #go_forward()
                ignore_scan=False
            elif right_object_detected and left_object_detected:
                print("Full left")
                go_left(2)
            elif right_object_detected :
                print("Go left")
                go_left(1.5)
            elif left_object_detected:
                print("Go right")
                go_right(1.5) 
            else:
                print("Forward")
                go_forward()
                
    except Exception:
        lidar.stop()
        lidar.disconnect()
        lidar = RPLidar('/dev/ttyUSB0')
        ignore_scan = True

lidar.stop()
lidar.stop_motor()
lidar.disconnect()

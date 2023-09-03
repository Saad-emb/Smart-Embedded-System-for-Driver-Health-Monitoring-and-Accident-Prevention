import cv2
import dlib
import RPi.GPIO as GPIO
import time
from scipy.spatial import distance
import can
import struct
import serial

# Initialization of serial port
port2=serial.Serial(port='/dev/serial0',baudrate=9600, timeout=1, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)

# Initialization of the CAN bus
can_interface = 'socketcan'  # Use 'socketcan' for SocketCAN interfaces
bus = can.interface.Bus(channel='can0', bustype=can_interface)

# Set the pin number for the buzzer
buzzer_pin = 4

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)
# Create a PWM object
pwm = GPIO.PWM(buzzer_pin, 1000)  # Set frequency to 1000 Hz

def play_alarm():
    while True:
        pwm.start(50)  # Start PWM with 50% duty cycle

def calculate_EAR(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear_aspect_ratio = (A+B)/(2.0*C)
    return ear_aspect_ratio

cap = cv2.VideoCapture(0)
hog_face_detector = dlib.get_frontal_face_detector()
dlib_facelandmark = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

while True:
    _, frame = cap.read()

    message = bus.recv()  # Wait for receiving a CAN message
    if message.arbitration_id == 0x7FF:  # Check if the message ID matches the expected value
        # Decode the received data
        bpm, spo2 = struct.unpack('ff', message.data)

        # Print the decoded values
        print("BPM: {}, SpO2: {}%".format(bpm, spo2))
        #send serial
        bpm_str = str(int(bpm))
        spo2_str = str(int(spo2))
        data_str = bpm_str + ',' + spo2_str + ',' +'\n'
        port2.write(data_str.encode())  
     


    pwm.start(0)
    signal=0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = hog_face_detector(gray)
    for face in faces:
        face_landmarks = dlib_facelandmark(gray, face)
        leftEye = []
        rightEye = []

        for n in range(36,42):
            x = face_landmarks.part(n).x
            y = face_landmarks.part(n).y
            leftEye.append((x,y))
            next_point = n+1
            if n == 41:
                next_point = 36
            x2 = face_landmarks.part(next_point).x
            y2 = face_landmarks.part(next_point).y
            cv2.line(frame,(x,y),(x2,y2),(0,255,0),1)

        for n in range(42,48):
            x = face_landmarks.part(n).x
            y = face_landmarks.part(n).y
            rightEye.append((x,y))
            next_point = n+1
            if n == 47:
                next_point = 42
            x2 = face_landmarks.part(next_point).x
            y2 = face_landmarks.part(next_point).y
            cv2.line(frame,(x,y),(x2,y2),(0,255,0),1)

        left_ear = calculate_EAR(leftEye)
        right_ear = calculate_EAR(rightEye)

        EAR = (left_ear+right_ear)/2
        EAR = round(EAR,2)
        
        if EAR < 0.26:
            cv2.putText(frame,"DROWSY",(20,100), cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,255),4)
            cv2.putText(frame,"Are you Sleepy?",(20,400), cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),4)
            print("Drowsy")
            # Turn on the buzzer alarm
            pwm.start(50)  # Start PWM with 50% duty cycle
            time.sleep(0.2)  # Play the tone for 0.2 seconds
            pwm.start(0)   # Stop the PWM signal
            time.sleep(0.2)  # Pause for 0.2 seconds
            signal=1
        
        print(EAR)
        #bpm_str = str(int(bpm))
        #spo2_str = str(int(spo2))
        #data_str = bpm_str + ',' + spo2_str + ',' +'\n'
        #port2.write(data_str.encode())       

    cv2.imshow("Are you Sleepy", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
bus.shutdown()

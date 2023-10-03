# Smart-Embedded-System-for-Driver-Health-Monitoring-and-Accident-Prevention# 
## Introduction
Road accidents are a major public health problem that can be caused by a variety of
factors, including driver fatigue and health issues. As part of this project, we will
develop an innovative on-board system that combines automotive and medicine to
monitor the health status of drivers in real time and prevent accidents. The system
uses a combination of heart rate, oxygen sensors, cameras and AI algorithm to
detect signs of driver fatigue and health issues. In the event of a heart attack or any
other serious health condition detected, the system will activate emergency
measures to ensure the safety of the driver and other road users.

As part of my end-of-year project, i developed an intelligent on-board system for
real-time monitoring of drivers' health status and prevention of health-related
accidents. This report presents my approach to designing and implementing this
innovative system.

## Overall Project Architecture:

<p align="center">

  ![1](https://github.com/Saad-emb/Smart-Embedded-System-for-Driver-Health-Monitoring-and-Accident-Prevention/assets/123195068/553ab703-22a7-4e8d-9429-cc4ce133859c)

</p>
The system uses a MAX30102 sensor to measure the driver's heart rate and oxygen
saturation. The data captured by the sensor is then transmitted to the ESP32
microcontroller via the I2C communication protocol. The ESP32 microcontroller is
responsible for acquiring and transmitting data to the MCP2515, using the SPI
protocol. The MCP2515, as a CAN controller, facilitates the transmission of data to
the Raspberry Pi 4 via the CAN bus.
The Raspberry Pi 4 runs specially designed Python code to analyze the received
data. Using advanced algorithms, the system detects signs of driver fatigue by
analyzing changes in heart rate and oxygen saturation. When fatigue is detected,
appropriate alarms are triggered to prevent potential accidents.
In summary, our project aims to develop an intelligent on-board system for
monitoring the health status of drivers and preventing accidents related to health
problems. By using appropriate sensors, microcontrollers and communication
protocols, we have created a powerful and promising system. This report details
our approach and the results obtained, paving the way for new advances in the field
of automotive safety.
The implementation of The project is  done in 6 steps:
## 1st step: Acquisition of biometric data with sensor MAX30102 and sending of the can frame with the can bus from the microcontroller to raspberry

In the first step of my implementation, I used the MAX30102 sensor for acquiring biometric data, which included heart rate (BPM) and blood oxygen level (SpO2). The sensor was communicated with using the I2C bus of the ESP32 microcontroller. Once the I2C bus was initialized, the MAX30102 sensor was configured with the necessary parameters.

Subsequently, I established a loop to consistently update and retrieve data from the sensor. Within this loop, I extracted BPM and SpO2 values upon detecting a heartbeat. These values were then transmitted via the CAN frame with the address 0x7FF. Additionally, the data was displayed on the console terminal, providing real-time monitoring of the rhythm values.

![2](https://github.com/Saad-emb/Smart-Embedded-System-for-Driver-Health-Monitoring-and-Accident-Prevention/assets/123195068/bb045eee-04d2-40cb-9e49-4a9ed38f00fd)


## 2nd step: Receiving abd decoding of the can frame in the raspberry card
This step allowed to retrieve the CAN frames sent by the ESP32 microcontroller and
decoding of the CAN frame.
using the "python-can" Python library and the "struct.unpack()" function to
unpack the received data.
we assume that the data is encoded as two floating point values, representing
BPM and SpO2. Using the `'ff'` format string, `"struct.unpack()"` unpacks the data
appropriately.
Finally,the decoded values (BPM and SpO2) is displayed in the terminal using the
"print()" function.
This step allows us to decode the data received from the CAN frame and display the
corresponding values (BPM and SpO2) on the Raspberry Pi.

![3](https://github.com/Saad-emb/Smart-Embedded-System-for-Driver-Health-Monitoring-and-Accident-Prevention/assets/123195068/f417bc6f-c7d3-4e29-a5ca-32068f84e845)


## 3rd step: Main program (fatigue detection and data acquisition via the mcp2515 with can bus)
In this part of the code, i perform eye fatigue detection and data acquisition through
the MCU (Raspberry pi) using the CAN bus. Here is a detailed description:
1. Serial port and CAN bus initialization:
In this first part of the code, it initialize the serial port port2̀ by specifying the
necessary communication parameters, such as the port used, the baud rate, the
timeout, etc. Next, we create a  bus object to communicate over the CAN bus. This
will allow us to receive data from sensors or other devices connected to the CAN
bus.
2. GPIO Setup:
This part of the code is about configuring the GPIO (General Purpose Input/Output) on
the Raspberry Pi. We use the RPi.GPIO library to set the GPIO mode and configure the
buzzer pin as an output. Additionally, we are creating a PWM (Pulse Width Modulation)
object that will allow us to control the buzzer by adjusting the frequency and duty cycle
of the signal.
20
3. Alarm playback function:
This `play_alarm` function is responsible for playing the buzzer alarm. It is called
when fatigue detection is activated. The function starts the PWM signal with a duty
cycle of 50%, which activates the buzzer. This loop runs indefinitely until the
function stop is triggered.
4. EAR calculation function:
The code also includes a function called `calculate_EAR` which is used to calculate
the eye aspect ratio (EAR). This function takes the coordinates of the eye keypoints
detected by the dlib model. Using these coordinates, it calculates the Euclidean
distance between the necessary points and uses this distance to determine the
aspect ratio of the eye. Aspect ratio is a measure used in the detection of eye strain.
5. Data acquisition and fatigue detection:
This part is responsible for acquiring data from the camera and detecting fatigue
using dlib's face detection model. The code starts by capturing an image from the
camera. Then it waits to receive a message on the CAN bus. When a message is
received, the data is extracted and displayed in the terminal. The data is then sent
via the serial port.
In parallel, the code uses dlib's face detection model to detect faces in the captured
image. Once a face is detected, eye key points are extracted from the detected face.
The distances between these key points are used to calculate the eye aspect ratio
(EAR) for each eye. If the value of the EAR is lower than a specified threshold, the
code considers that the person is tired and activates the buzzer alarm.
Execution of these steps is done in a continuous loop, allowing real-time data
acquisition and continuous fatigue detection.

## 4th step: Simulation in case of emergency

In this  step, i  set up a simulation using CARLA and we perform actions
based on the biometric data received via UART. 

- The `getbpm_spo2()` function  reads data from the serial port.Then
convert the received values into BPM (beats per minute) and SpO2 (oxygen
saturation) and display them on the screen.

- The function `send_email()`, is used to send an emergency email with vehicle position coordinates when an emergency
situation is detected. This function uses the SMTP protocol and requires
authentication information to send the e-mail.
Next, we configure the serial communication by defining the port and the communication
parameters. 
- The `emergency_check()` function checks if the BPM and SpO2 values are below
the emergency thresholds. If so, it triggers an emergency action, which consists of stopping
the vehicle and sending an email with the position coordinates.
- In the main function `main()`, it connect to the CARLA simulator and configure the
necessary parameters. We choose the blueprints of the vehicles (in this example a
Tesla Model 3), we place them on the map of the simulation.
In the main loop, we get the position of the vehicle and we move the spectator
camera to follow it. We receive the biometric data from the serial port and check if
an emergency situation is detected by calling the `emergency_check()` function.

![5](https://github.com/Saad-emb/Smart-Embedded-System-for-Driver-Health-Monitoring-and-Accident-Prevention/assets/123195068/c9c7f28f-e372-4ece-ab53-79a8f16a7147)


If an emergency is detected, the car stops and the gybe signals are triggered.

![6](https://github.com/Saad-emb/Smart-Embedded-System-for-Driver-Health-Monitoring-and-Accident-Prevention/assets/123195068/aff46395-8afc-4f49-8bb4-3f25b4946825)


and display an emergency message and  sends an email using the
and then we display an emergency message and we send an email using the
send_email() function.send_email() function.

![7](https://github.com/Saad-emb/Smart-Embedded-System-for-Driver-Health-Monitoring-and-Accident-Prevention/assets/123195068/6e69ea68-2828-4557-8d74-171f06e9a7fa)

## Conclusion 

Overall, this project demonstrates the potential of integrating biometric data and
the ADAS simulation environment for safer driving and rapid response to
emergency situations. It highlights the growing importance of the convergence
between automotive, health and technology domains to improve driver safety and
well-being


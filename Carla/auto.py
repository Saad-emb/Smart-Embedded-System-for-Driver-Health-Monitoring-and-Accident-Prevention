import glob
import os
import sys
import serial
import time
from random import *
try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

import math
import random

import glob
import os
import sys
import carla
import random
import pygame
try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def getbpm_spo2():
    bpm=0
    spo2=0
    signal=0
    line = port.readline().decode('utf-8', errors='ignore').strip()
    if line:
        try:
            # Split the received data into BPM and SpO2 values
            bpm, spo2 = map(float, line.split(','))

            # Display the received data
            print("Received BPM: {}, SpO2: {}%".format(bpm, spo2))
            # Do whatever you want with the data on the PC side
        except ValueError:
            # Handle the case when the received data cannot be converted to float
            data_list = line.split(',')
            bpm = int(data_list[0])  

           
            spo2 = int(data_list[1]) 
           
            #signal = float(data_list[2])
            print("Received BPM: {}, SpO2: {}%".format(bpm, spo2))
            
    return int(bpm),int(spo2)

def send_email(x,y,z):
    sender_email="emergencyprojetpfa@gmail.com"
    rec_email="kouzmanesaad@gmail.com"
    password="grizoodybqmyizjz"
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = rec_email
    message["Subject"] = "Emergency Alert! Vehicle Position: x={}, y={}, z={}".format(x, y, z)
    body = """
    Dear Recipient,

    This email is to notify you about a driver emergency. Immediate action may be required.

    Vehicle Position: 
    x = {}
    y = {}
    z = {}

    Please take appropriate measures to ensure the safety and well-being of the driver.

    Kind regards,
    Emergency System
    """.format(x, y, z)
    message.attach(MIMEText(body, "plain"))
    server = smtplib.SMTP('smtp.gmail.com',587)
    
    try: 
        server.starttls()
        server.login (sender_email, password)
        print ("Login success")
        server.sendmail (sender_email, rec_email, message.as_string()) 
        print ("Email has been sent to ", rec_email)
    except Exception as e:
        print("An error occurred while sending the email:", str(e))



port = serial.Serial(port='COM3', baudrate=9600, timeout=1)  # Replace 'COM1' with the actual port

def emergency_check(bpm, spo2, ear):
    return bpm < 50 or spo2 < 80 
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

class HUD(object):
    def __init__(self, width, height):
        self.dim = (width, height)
        self.font = pygame.font.Font(None, 20)  # Set the font for the HUD text
        self.bpm = 0
        self.spo2 = 0

    def update_values(self, bpm, spo2):
        self.bpm = bpm
        self.spo2 = spo2

    def render(self, display):
        # Clear the display
        display.fill((0, 0, 0))

        # Render the BPM value on the display surface
        bpm_surface = self.font.render('BPM: {}'.format(self.bpm), True, (255, 255, 255))
        display.blit(bpm_surface, (8, 8))

        # Render the SpO2 value on the display surface
        spo2_surface = self.font.render('SpO2: {}'.format(self.spo2), True, (255, 255, 255))
        display.blit(spo2_surface, (8, 28))

        # Update the display
        pygame.display.flip()




def main():
    # Connect to the CARLA simulator
    client = carla.Client('localhost', 2000)
    client.set_timeout(5.0)
    hud = HUD(800, 600)
    

    try:
        # Load the CARLA world and get the blueprint library
        world = client.get_world()
        blueprint_library = world.get_blueprint_library()

        # Choose a vehicle blueprint for the Camaro
        camaro_bp = blueprint_library.find('vehicle.tesla.model3')

        # Choose a vehicle blueprint for the lead vehicle
        lead_vehicle_bp = blueprint_library.find('vehicle.audi.tt')

        # Set the Camaro's autopilot attribute to True
        camaro_bp.set_attribute('role_name', 'autopilot')

        # Choose a spawn point for the Camaro
        camaro_spawn_point = random.choice(world.get_map().get_spawn_points())


        try:
            # Spawn the Camaro in the CARLA world
            camaro = world.spawn_actor(camaro_bp, camaro_spawn_point)
            print("Camaro spawned.")

            # Set the Camaro to autopilot
            camaro.set_autopilot(True)
            print("Camaro set to autopilot.")

            # Choose a spawn point for the lead vehicle
            lead_vehicle_spawn_point = random.choice(world.get_map().get_spawn_points())

            # Spawn the lead vehicle in the CARLA world
            lead_vehicle = world.spawn_actor(lead_vehicle_bp, lead_vehicle_spawn_point)
            print("Lead vehicle spawned.")
            # Create a display surface
            display = pygame.display.set_mode((200, 100))
            emergency=0
            sent=False

            while True:
                if emergency !=10: 
                # Get the Camaro's transform (position and rotation)
                     camaro_transform = camaro.get_transform()
                     #time.sleep(1)

                     # Get the Camaro's location
                     camaro_location = camaro_transform.location

                     # Set the spectator camera to follow the Camaro
                     camera_location = carla.Location(x=-10, y=-1, z=5)  # Adjust the camera position here
                     camera_rotation = carla.Rotation(pitch=-15,yaw=0)  # Adjust the camera rotation here
                     spectator_transform = carla.Transform(camaro_location + camera_location, camera_rotation)
                     world.get_spectator().set_transform(spectator_transform)
                     #get data fron serial port 
                

                # Update the BPM and SpO2 values
                bpm,spo2 = getbpm_spo2()
               

                if bpm < 40 or spo2 < 70 : 
                    if emergency==10: 
                         camaro.set_light_state(carla.VehicleLightState(carla.VehicleLightState.RightBlinker | carla.VehicleLightState.Brake |carla.VehicleLightState.LeftBlinker ))  
                         camaro.set_autopilot(False) 
                         camaro.apply_control(carla.VehicleControl(throttle=0.0, brake=1.0)) 
                         print("Emergency! trigerred")
                         vehicle_location = camaro.get_location()
                         x = vehicle_location.x
                         y = vehicle_location.y
                         z = vehicle_location.z
                         print("Vehicle Position: x={}, y={}, z={}".format(x, y, z))
                         subject = "Emergency Alert!"
                         if sent==False:
                            send_email(x,y,z)
                            sent=True
                         else:
                             print("Message Already sent")

                    else:     
                        print("Emergency! warning", emergency)
                        emergency=emergency+1
                        #camaro.set_light_state(carla.VehicleLightState(carla.VehicleLightState.RightBlinker | carla.VehicleLightState.Brake |carla.VehicleLightState.LeftBlinker ))
                else:
                        emergency=0
                        # Resume normal autopilot
                        camaro.set_autopilot(True)

                        

                # Update the HUD with the BPM and SpO2 values
                hud.update_values(bpm, spo2)

                # Render the HUD                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
                hud.render(display)

              
                

        finally:
            # Destroy the vehicles and stop the CARLA client
            if camaro is not None:
                camaro.destroy()
            if lead_vehicle is not None:
                lead_vehicle.destroy()
            client.stop()

    except KeyboardInterrupt:
        # Stop the CARLA client when Ctrl+C is pressed
        client.stop()


if __name__ == '__main__':
    main()

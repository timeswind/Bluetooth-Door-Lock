import bluetooth
import time
from picamera import PiCamera
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import smtplib
import RPi.GPIO as GPIO

#length of time taken to scan for bluetooth devices
search_time = 5
#Bluetooth address of owner
my_blue_address = '70:8A:09:08:F6:3A'
#Bluetooth addresses to ignor so duplicated emails wont be sent
ignor_address =['60:A3:7D:D5:E9:C1']
	
#Set unlock rotation
unlock = [  [1,0,0,1],
            [0,0,0,1],
            [0,0,1,1],
            [0,0,1,0],
            [0,1,1,0],
            [0,1,0,0],
            [1,1,0,0],
	    [0,0,0,1]]

#Set lock rotation
lock = [	[0,0,0,1],
	[1,1,0,0],
	[0,1,0,0],
	[0,1,1,0],
	[0,0,1,0],
	[0,0,1,1],
	[0,0,0,1],
	[1,0,0,1]]

#Email details
from_email = 'raspicam314@gmail.com'
from_password = 'password3.14'
to_email = 'raspicam314@gmail.com'

#Method to check if a discovered address is in the ignor_address list
def listContains(ignor_address, addr):
    check = False
    
    for i in range(0, len(ignor_address)):
        if ignor_address[i] == addr:
            check = True
            break
        
    return check
#---------------------------------------------------------------------------------------------------------------
	
#Method used to activate the door lock
def doorLock(rotation):
    GPIO.setmode(GPIO.BCM)
    #Setup the GPIO pins
    control_pin = [26, 13, 6, 5]

    for pin in control_pin:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)
	
    #Rotation length
    for i in range(500):    
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(control_pin[pin], rotation[halfstep][pin])
                #Rotation speed
                time.sleep(0.001)
	
    #Clear GPIO
    GPIO.cleanup()
#---------------------------------------------------------------------------------------------------------------

#Method to control how long the door is unlocked
def stopwatch(seconds):
	start = time.time()
	time.clock()
	elapsed = 0
	while elapsed < seconds:
		elapsed = time.time()-start
		time.sleep(1)
#---------------------------------------------------------------------------------------------------------------

#Method used to take picture and send it via email when unknown device is discoved
def sendEmail(from_email, from_password, to_email):
	camera = PiCamera()
	timeCaptured = '/home/pi/Desktop/Camera/Pic' + datetime.datetime.now().strftime('%Y-%m-%d%H:%M:%S') + '.png'
	camera.rotation = 180
	camera.capture(timeCaptured)
	
	print("Image Captured")
	
	#Message to be sent
	msg = MIMEMultipart()
	msg['From'] = from_email
	msg['To'] = to_email
	msg['Subject'] = 'Unknown Device Detected'
	body = 'There has been an unknown bluetooth device detected in the vicinity.'
	msg.attach(MIMEText(body, 'plain'))
	
	#Attach the image to the message
	attachment = open(timeCaptured,'rb')
	image = MIMEImage(attachment.read())
	msg.attach(image)
	
	#Connect to server and send the email
	server = smtplib.SMTP("smtp.gmail.com",587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(from_email, from_password)
	server.sendmail(from_email, to_email, msg.as_string())
	server.quit()
	print("Email sent")
#-------------------------------------------------------------------------------------------------------------

while True:
	print('Searching for devices.....')

	#Search for all discoverable bluetooth devices
	all_devices = bluetooth.discover_devices(duration = search_time, flush_cache = True, lookup_names= True)

	#Check if any devices were found
	if len(all_devices) > 0:
		#loop through all_devices and check the addresses
		for addr, name in all_devices:
			#print out the name and address of each device
			print('Name: ' + name + ' - Address: ' + addr)
        
			#if the detected address is the same aas my_blue_address
			if addr == my_blue_address:
				doorLock(unlock)
				print('Door Unlocked')
				stopwatch(5)
				GPIO.setmode(GPIO.BCM)
				doorLock(lock)
				print('Door Locked')
            
			elif listContains(ignor_address, addr) == False:
				#Take picture and send email to owner
				sendEmail(from_email, from_password, to_email)
				#Add address to ignor list to avoid sending duplicated emails
				ignor_address.append(addr)
            
	else:
		print('No devices found, ensure your bluetooth is discoverable')
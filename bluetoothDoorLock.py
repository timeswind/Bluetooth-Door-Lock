import bluetooth
import time
from picamera import PiCamera
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import smtplib
import RPi.GPIO as GPIO

# length of time taken to scan for bluetooth devices
search_time = 5
# Bluetooth address of owner
my_blue_address = '8C:86:1E:B1:65:F1'
# Bluetooth addresses to ignor so duplicated emails wont be sent
ignor_address = ['60:A3:7D:D5:E9:C1']


# Email details
from_email = 'raspicam314@gmail.com'
from_password = 'password3.14'
to_email = 'raspicam314@gmail.com'

# Method to check if a discovered address is in the ignor_address list


def listContains(ignor_address, addr):
    check = False

    for i in range(0, len(ignor_address)):
        if ignor_address[i] == addr:
            check = True
            break

    return check
# ---------------------------------------------------------------------------------------------------------------

# Method used to activate the door lock


def doorLock(status):

    Relay_Ch1 = 26

    GPIO.output(Relay_Ch1, status)

    # Clear GPIO
    # GPIO.cleanup()
# ---------------------------------------------------------------------------------------------------------------

# Method to control how long the door is unlocked


def stopwatch(seconds):
    start = time.time()
    time.clock()
    elapsed = 0
    while elapsed < seconds:
        elapsed = time.time() - start
        time.sleep(1)
# ---------------------------------------------------------------------------------------------------------------

# Method used to take picture and send it via email when unknown device is
# discoved


def sendEmail(from_email, from_password, to_email):
    camera = PiCamera()
    timeCaptured = '/home/pi/Desktop/Camera/Pic' + \
        datetime.datetime.now().strftime('%Y-%m-%d%H:%M:%S') + '.png'
    camera.rotation = 180
    camera.capture(timeCaptured)

    print("Image Captured")

    # Message to be sent
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = 'Unknown Device Detected'
    body = 'There has been an unknown bluetooth device detected in the vicinity.'
    msg.attach(MIMEText(body, 'plain'))

    # Attach the image to the message
    attachment = open(timeCaptured, 'rb')
    image = MIMEImage(attachment.read())
    msg.attach(image)

    # Connect to server and send the email
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(from_email, from_password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()
    print("Email sent")
# -------------------------------------------------------------------------------------------------------------


while True:
    print('Searching for devices.....')
    Relay_Ch1 = 26
    Relay_Ch2 = 20
    Relay_Ch3 = 21

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(Relay_Ch1, GPIO.OUT)
    GPIO.setup(Relay_Ch2, GPIO.OUT)
    GPIO.setup(Relay_Ch3, GPIO.OUT)
  # Search for all discoverable bluetooth devices
    all_devices = bluetooth.discover_devices(
        duration=search_time, flush_cache=True, lookup_names=True)

   # Check if any devices were found
    if len(all_devices) > 0:
        # loop through all_devices and check the addresses
        for addr, name in all_devices:
            # print out the name and address of each device
            print('Name: ' + name + ' - Address: ' + addr)

            # if the detected address is the same aas my_blue_address
            if addr == my_blue_address:
                doorLock(GPIO.LOW)
                print('Door Unlocked')
                stopwatch(5)
                doorLock(GPIO.HIGH)
                print('Door Locked')

            elif listContains(ignor_address, addr) == False:
                # Take picture and send email to owner
                # sendEmail(from_email, from_password, to_email)
                # Add address to ignor list to avoid sending duplicated
                # emails
                ignor_address.append(addr)

    else:
        print('No devices found, ensure your bluetooth is discoverable')

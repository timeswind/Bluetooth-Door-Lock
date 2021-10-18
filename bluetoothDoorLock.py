import bluetooth
import select
import time
import RPi.GPIO as GPIO

# Relay Channels
Relay_Ch1 = 26
Relay_Ch2 = 20
Relay_Ch3 = 21

# length of time taken to scan for bluetooth devices
search_time = 5
# Bluetooth address of owner
my_blue_address = '8C:86:1E:B1:65:F1'
# Bluetooth addresses to ignor so duplicated emails wont be sent
ignor_address = ['60:A3:7D:D5:E9:C1']

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
    GPIO.output(Relay_Ch1, status)

    # Clear GPIO
    # GPIO.cleanup()
# ---------------------------------------------------------------------------------------------------------------

# Method to control how long the door is unlocked


def stopwatch(seconds):
    start = time.time()
    time.time.perf_counter()
    elapsed = 0
    while elapsed < seconds:
        elapsed = time.time() - start
        time.sleep(1)
# ---------------------------------------------------------------------------------------------------------------

# Method used to take picture and send it via email when unknown device is
# discoved

class MyDiscoverer(bluetooth.DeviceDiscoverer):

    def pre_inquiry(self):
        self.done = False

    def device_discovered(self, address, device_class, rssi, name):
        print("%s - %s" % (address, name))

        # get some information out of the device class and display it.
        # voodoo magic specified at:
        #
        # https://www.bluetooth.org/foundry/assignnumb/document/baseband
        major_classes = ("Miscellaneous",
                         "Computer",
                         "Phone",
                         "LAN/Network Access point",
                         "Audio/Video",
                         "Peripheral",
                         "Imaging")
        major_class = (device_class >> 8) & 0xf
        if major_class < 7:
            print("  %s" % major_classes[major_class])
        else:
            print("  Uncategorized")

        print("  services:")
        service_classes = ((16, "positioning"),
                           (17, "networking"),
                           (18, "rendering"),
                           (19, "capturing"),
                           (20, "object transfer"),
                           (21, "audio"),
                           (22, "telephony"),
                           (23, "information"))

        for bitpos, classname in service_classes:
            if device_class & (1 << (bitpos-1)):
                print("    %s" % classname)
        print("  RSSI: " + str(rssi))

    def inquiry_complete(self):
        self.done = True


while True:
    d = MyDiscoverer()
    d.find_devices(lookup_names=True)

    readfiles = [d, ]

    while True:
        rfds = select.select(readfiles, [], [])[0]

        if d in rfds:
            d.process_event()

        if d.done:
            break
        
#     print('Searching for devices.....')

#     GPIO.setwarnings(False)
#     GPIO.setmode(GPIO.BCM)

#     GPIO.setup(Relay_Ch1, GPIO.OUT)
#     GPIO.setup(Relay_Ch2, GPIO.OUT)
#     GPIO.setup(Relay_Ch3, GPIO.OUT)

#     # default open switches

#     GPIO.output(Relay_Ch1, GPIO.HIGH)
#     GPIO.output(Relay_Ch2, GPIO.HIGH)
#     GPIO.output(Relay_Ch3, GPIO.HIGH)

#   # Search for all discoverable bluetooth devices
#     all_devices = bluetooth.discover_devices(
#         duration=search_time, flush_cache=True, lookup_names=True)

#    # Check if any devices were found
#     if len(all_devices) > 0:
#         # loop through all_devices and check the addresses
#         for addr, name in all_devices:
#             # print out the name and address of each device
#             print('Name: ' + name + ' - Address: ' + addr)

#             # if the detected address is the same aas my_blue_address
#             if addr == my_blue_address:
#                 doorLock(GPIO.LOW)
#                 print('Door Unlocked')
#                 stopwatch(5)
#                 doorLock(GPIO.HIGH)
#                 print('Door Locked')

#             elif listContains(ignor_address, addr) == False:
#                 # Take picture and send email to owner
#                 # sendEmail(from_email, from_password, to_email)
#                 # Add address to ignor list to avoid sending duplicated
#                 # emails
#                 ignor_address.append(addr)

#     else:
#         print('No devices found, ensure your bluetooth is discoverable')


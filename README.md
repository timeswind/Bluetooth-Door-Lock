# Bluetooth-Door-Lock

# Introduction

The following documentation will be discussing everything that went into the development of our Bluetooth Door Lock project.  We will be looking at the technologies we used to create our project, like Bluetooth, a stepper motor, a camera and Wi-Fi.  We will also talk about how the project software was put together.  We will then be looking at all the features that the project provides.  This documentation will help you understand how the project works.

# Overview

When deciding on an idea for our project we knew we wanted to create something that would bring an element of convenience to peoples lives; we also wanted the project to have a practical use in the real world.  In the end we all agreed upon creating an automated door lock.  This would make it easier for a person to access their home if, for some reason they could not use their hands.

Once we had the basis of our project we then had to figure out how we would go about creating it so that it worked effectively and reliably.  We chose to use Bluetooth as the way of distinguishing between users as all devices have a unique Bluetooth address.  This was a way of giving the project a security component.  When the owner is detected a stepper motor is activated which will rotate, unlocking the door, after a set amount of time the door will automatically lock again adding another element of security to the project.

When an unknown Bluetooth address is detected the camera will take a picture; to ensure the picture that was taken has a unique name and therefor can be located easily, it is given the date and time as its name.  The picture will be attached to an email which is then sent automatically to the email address of the owner of the home.  This unknown Bluetooth address is then temporarily saved so that duplicate emails won’t be sent to the owner.  These processes will repeat continuously until the project is turned off.

# Bluetooth

Bluetooth technology is a standardised protocol that allows for the communication of wireless devices over a short-range waveform.  It was invented in 1994 by Ericsson.  Wireless technologies require both a hardware and software component.  The hardware is required to be able to send the necessary signal through low energy radio waves.

The software will determine what is sent over the Bluetooth signal and how this signal will be interpreted.  For a device to use Bluetooth it needs a computer chip that has a Bluetooth radio.  The software must be universally accepted by all devices to allow for communication.  Examples of technologies that have embraced Bluetooth are printers, speakers, laptops, keyboards and headsets. 

Bluetooth is similar to Wi-Fi; however, it can work between any two enabled devices and does not require any additional network equipment such as routers.  Bluetooth works over a maximum distance of 164 feet, which is more than enough for many home, car and consumer applications.

All Bluetooth devices are managed using a star topology.  These Bluetooth networks are commonly known as piconets.  The networks use a master/slave model to control when and where devices can send data.  A single master device can be connected to up to seven different slave devices.  Any slave device can only be connected to a single master.

 
Master/slave diagram https://learn.sparkfun.com/tutorials/bluetooth-basics

The master manages communication throughout the piconet.  It can send data to any of its slaves and request data from them as well.  Slaves are unable to communicate with other slaves; they are only allowed to transmit to and receive from their master.

Bluetooth technology determine device connection based on inquiry and inquiry scan.  The first device will send an inquiry when it is looking for devices in the area.  A second device will scan for inquiries and would respond to the one sent by the first device.  As a result, the second device will appear as an active on the first device.  If the second device is selected a connection will be made.

# Python Code

In order to use the built-in Bluetooth of the Raspberry Pi we had to download and install the PyBluez module from the pypi project page.  PyBluez provides helpful functions that programmers can take advantage of in order to use the Raspberry Pi Bluetooth.

When creating the Python code, we first need to import the PyBluez module.  Next, we must create a variable to hold the Bluetooth address of the owner that will enable to door to unlock (my_blue_address).  We then have a list called ignore_address that holds the addresses we wish to ignore. 

We need to access the Bluetooth module so that we can get all the discoverable devices in the area; to do this we create a variable that will call the function we need.

all_devices = bluetooth.discover_devices(duration = 5, flush_cache =   True, lookup_names = True)

The duration variable is how much time we wish to look for discoverable devices before making any checks on the addresses.  

Once the duration time has passed we loop through the all_devices list; we then compare the discovered address in the first position of the list to see if it is the same as my_blue_address.  If the addresses match we can activate the motor to unlock the door.

If the address doesn’t match we check if the address has already been discovered and added to the ignore_address.
 
Snippet from bluetoothDoorLock.py

If the discovered address is already in the ignore_address list then we do nothing.  
If it is an unknown address a photo will be taken and sent via email to the owner.  The address will then be temporarily stored in ignore_address using ignore_address.append(address); this is to ensure duplicate emails aren’t sent.

These processes will be carried out for every index in the all devices list.  Once this loop is finished we will cycle back to the top of the while True infinite loop and repeat.  As the all_devices list is within this loop it will clear the addresses it had previously stored and continue to find new ones.  This will ensure that all addresses in the list will be unique and prevent redundant data.

# Features

I created this project so that people are able to safely unlock doors without needing a physical key.  The process works by storing all discoverable Bluetooth devices in the vicinity are read and stored for each cycle threw the code; all these addresses will then be processed to determine what operation will be performed.  

If a discovered Bluetooth address matches the owners address the stepper motor will rotate, unlocking the door.  After an allotted amount of time the motor will rotate in the opposite directing to ensure the door locks behind the owner.  Due to all Bluetooth devices having a unique address it ensures that only the owners device is able to unlock the door.

When an unknown address is discovered the ignore_address list will be checked to see if it had previously been found.  If the address isn’t in the list then a photo will be taken using the camera and attached to an email.  The email will then be sent to the owner, notifying him that there is an unknown Bluetooth device near the lock.

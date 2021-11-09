#!/usr/bin/env python3

import argparse
import sys

import usb.core
import usb.backend.libusb1

parser = argparse.ArgumentParser(description="jump_ch552_bl")
parser.add_argument('-v','--vid', help="VID", required=True)
parser.add_argument('-p','--pid', help="PID", required=True)

args = parser.parse_args()

idVendor  = int(args.vid, 0)
idProduct = int(args.pid, 0)

device = usb.core.find(idVendor=idVendor, idProduct=idProduct)


if device is None:
    raise ValueError('CH552 device not found. Please ensure it is connected.')
    sys.exit(1)

iProduct = usb.util.get_string(device, device.iProduct)

if iProduct != "Sipeed-Debug":
    print(f"Error: wrong device. Search for Sipeed-Debug iProduct found {iProduct}")
    sys.exit(1)

# detach kernel before claim
try:
    if device.is_kernel_driver_active(0):
        device.detach_kernel_driver(0)
except Exception as e:
    print("Error: fails to detach kernel")
    print(e)
    sys.exit(1)

# Claim interface 0
try:
    usb.util.claim_interface(device, 0)
except Exception as e:
    print("Error: fails to claim interface")
    print(e)
    sys.exit(1)

FTDI_DEVICE_OUT_REQTYPE = 0x40
SIO_WRITE_EEPROM_REQUEST = 0x91

# send 0x91: write eeprom -> ch552_jtag don't care message but jump to bl mode
try:
    device.ctrl_transfer(FTDI_DEVICE_OUT_REQTYPE,
        SIO_WRITE_EEPROM_REQUEST, 0, 0, None, 5000)
except usb.core.USBError as e: # device immediately reboot
    pass

print("Done")

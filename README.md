# jump_ch552_to_bl
Script to switch ch55x_jtag  firmare to bl mode

[Sipeed tangNano1K](https://tangnano.sipeed.com/en/) has a JTAG/serial interface
based on a ch552 MPU.
The [firmware](https://github.com/diodep/ch55x_jtag) mimic the **FTDI FT2232C**
device and may be updated (as mentioned [here](https://qiita.com/ciniml/items/05ac7fd2515ceed3f88d))
by, first, switching the microcontroler in *BL* mode.

This feature is done by sending *bRequest* `0x91` (*write eeprom*) with
*requestType* `0x40` using USB control transfer.

Official way is to use **ft_prog**. This script do the same and allows to
prepare firmware update.

## Requirement

**pyusb**

## How to use

```bash
usage: jump_to_ch552_bl.py [-h] -v VID -p PID

jump_to_ch552_bl

optional arguments:
  -h, --help         show this help message and exit
  -v VID, --vid VID  VID
  -p PID, --pid PID  PID
```

Once device in **BL mode** (check using lsusb) follow
[these instructions](https://qiita.com/ciniml/items/05ac7fd2515ceed3f88d)

before:

```bash
$ lsusb -v -d 4348:55e0
Bus 002 Device 092: ID 0403:6010 Future Technology Devices International, Ltd FT2232C/D/H Dual UART/FIFO IC
Device Descriptor:
  bLength                18
  bDescriptorType         1
  bcdUSB               2.00
  bDeviceClass            0
  bDeviceSubClass         0
  bDeviceProtocol         0
  bMaxPacketSize0         8
  idVendor           0x0403 Future Technology Devices International, Ltd
  idProduct          0x6010 FT2232C/D/H Dual UART/FIFO IC
  bcdDevice            5.00
  iManufacturer           1 Kongou Hikari
  iProduct                2 Sipeed-Debug
  iSerial                 3 8552F9D5BC
  bNumConfigurations      1
```

after:

```bash
$ lsusb -v -d 4348:55e0
Bus 002 Device 093: ID 4348:55e0 WinChipHead 
Device Descriptor:
  bLength                18
  bDescriptorType         1
  bcdUSB               1.10
  bDeviceClass          255 Vendor Specific Class
  bDeviceSubClass       128 
  bDeviceProtocol        85 
  bMaxPacketSize0         8
  idVendor           0x4348 WinChipHead
  idProduct          0x55e0 
  bcdDevice            1.00
  iManufacturer           0 
  iProduct                0 
  iSerial                 0 
  bNumConfigurations      1

```

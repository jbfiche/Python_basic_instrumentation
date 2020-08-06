# Instructions to get 3D printer going in Linux


## Install bCNC

Go to website and follow instructions.
Briefly, do:

1. Install Tkinker doing ```apt-get install python-tk```
2. Install bCNC: ```python2 -m pip install --upgrade bCNC```
2. find what port the printer is connected to by running
```dmesg | grep tty```
If you can still not detect who you should be looking at, then disconnect
and connect again and you should see it appearing in the list by reruing the dmesg command
2. Run bCNC using ```python2 -m bCNC &```.
2. Now,you should be able to connect by selecting the tty serial port.


## Communicating with the serial port

By default it seems only root or nobody is in the group that controls the IO of the serial port. This has to be solved by adding yourself to the list in the corresponding group.

Edit /etc/group. Look for 'tty' and add your name to the end of the list. For instance:

```tty:x:5:marcnol```

It seems that also the group 'dialout' needs to be joined. Just do it in case it is true, but you can also test and adapt this helpline.

I also read you need to logout and login again for changes to take place. To verify if they did, run ```groups```

## identify and try a connection to the serial port

To identify the serial we will disconnect and reconnect the device from the USB port. Then running

```desmg | grep tty```

you should get something like

```
[    0.256098] printk: console [tty0] enabled
[    2.018855] 00:03: ttyS0 at I/O 0x3f8 (irq = 4, base_baud = 115200) is a 16550A
[    2.041043] 0000:00:16.3: ttyS4 at I/O 0x70a0 (irq = 17, base_baud = 115200) is a 16550A
[   16.574219] usb 3-8: ch341-uart converter now attached to ttyUSB0
```

Now, we know the tty device we are looking for is /dev/ttyUSB0. Let's now send a serial command to see if it answers back:

```stty -F /dev/ttyUSB0```

and the answer should be:

```
speed 9600 baud; line = 0;
-brkint -imaxbel
```

Then run minicom as follows:
```
minicom -D /dev/ttyUSB0
```

You should be able to connect and then get the message:

```
Grbl v0.Xx ['$' for help]
```

And this is where I get stuck. The website https://github.com/grbl/grbl/wiki/Using-Grbl tells me that this is good news, as far as connection goes. The machine also does some noises as recognizing the connection. But then one should be able to run '$' and get an answer but I did not manage to get this working so far...

__more soon!__

You can also run a GUI terminal such as gtkterm, but I could not get very far with this.

## Install and run cncjs

First install npm package manager using ```apt install npm```

Then download and install cncjs:

```
git clone https://github.com/cncjs/cncjs.git
cd cncjs
git checkout master
npm install
npm run prepare
./bin/cncjs
```

Make sure you run the server as superuser otherwise you may have problems connecting to the serial port.

Once you do run you will see something like this:

![CNCjsInterface.png](http://)

Set the port to /dev/ttyUSB0, then select 115200 to baud rate.

You should be able to open a connection and get a reply from the grbl controller. I get:

```
Grbl 1.1f ['$' for help]
client> $$
$0=10 (Step pulse time, microseconds)
$1=25 (Step idle delay, milliseconds)
$2=0 (Step pulse invert, mask)
$3=5 (Step direction invert, mask)
$4=0 (Invert step enable pin, boolean)
$5=0 (Invert limit pins, boolean)
$6=0 (Invert probe pin, boolean)
$10=1 (Status report options, mask)
$11=0.010 (Junction deviation, millimeters)
$12=0.002 (Arc tolerance, millimeters)
$13=0 (Report in inches, boolean)
$20=0 (Soft limits enable, boolean)
$21=0 (Hard limits enable, boolean)
$22=0 (Homing cycle enable, boolean)
$23=0 (Homing direction invert, mask)
$24=25.000 (Homing locate feed rate, mm/min)
$25=500.000 (Homing search seek rate, mm/min)
$26=250 (Homing switch debounce delay, milliseconds)
$27=1.000 (Homing switch pull-off distance, millimeters)
$30=1000 (Maximum spindle speed, RPM)
$31=0 (Minimum spindle speed, RPM)
$32=0 (Laser-mode enable, boolean)
$100=1600.000 (X-axis travel resolution, step/mm)
$101=1600.000 (Y-axis travel resolution, step/mm)
$102=1600.000 (Z-axis travel resolution, step/mm)
$110=1000.000 (X-axis maximum rate, mm/min)
$111=1000.000 (Y-axis maximum rate, mm/min)
$112=800.000 (Z-axis maximum rate, mm/min)
$120=30.000 (X-axis acceleration, mm/sec^2)
$121=30.000 (Y-axis acceleration, mm/sec^2)
$122=30.000 (Z-axis acceleration, mm/sec^2)
$130=200.000 (X-axis maximum travel, millimeters)
$131=200.000 (Y-axis maximum travel, millimeters)
$132=200.000 (Z-axis maximum travel, millimeters)
ok
```

If you just get the first line, try disconnecting the module to move the stage manually from the main board. It interferes with the connections from your linux box.

You should be able to send G-code. I used something very simple, for example a circle:

```
G17 G20 G90 G94 G54
G0 Z0.25
X-0.5 Y0.
Z0.1
G01 Z0. F5.
G02 X0. Y0.5 I0.5 J0. F2.5
X0.5 Y0. I0. J-0.5
X0. Y-0.5 I-0.5 J0.
X-0.5 Y0. I0. J0.5
G01 Z0.1 F5.
G00 X0. Y0. Z0.25
```

And the mill should be making a circle!

# Controlling the mill from Python3

Now that you can connect and mill from linux, let's get the funny part working. Install python3, and the serial module using ```pip install pyserial```.

Then open an editor like Atom and copy paste the following code:

``` python=

#!/usr/bin/env python
"""\
Simple g-code streaming script for grbl
"""

import serial
import time

# Open grbl serial port
s = serial.Serial('/dev/ttyUSB0',115200)

# Open g-code file
f = open('circle.nc','r');

# Wake up grbl
s.write(b"\r\n\r\n")
time.sleep(2)   # Wait for grbl to initialize
s.flushInput()  # Flush startup text in serial input

# Stream g-code to grbl
for line in f:
    string2Send=line.strip()+"\r\n" #"".join([l,'\r'])
    print("Sending :{}".format(string2Send))
    s.write(string2Send.encode()) # Send g-code block to grbl
    grbl_out = s.readline() # Wait for grbl response with carriage return
    print(" : " + grbl_out.decode().strip())

# Close file and serial port
f.close()
```

The file 'circle.nc' contains the G-code I used earlier in CNCjs.

You should see the mill now running the code! Remeber to run the code as root to be able to open the port. I will find a work around this later. I tried adding dialout and tty to my username but so far this did not do the trick.

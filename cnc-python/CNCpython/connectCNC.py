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
    #l = line.strip() # Strip all EOL characters for streaming
    string2Send=line.strip()+"\r\n" #"".join([l,'\r'])
    print("Sending :{}".format(string2Send))
    #s.write(str.encode("G17 G20 G90 G94 G54")) # Send g-code block to grbl
    s.write(string2Send.encode()) # Send g-code block to grbl
    grbl_out = s.readline() # Wait for grbl response with carriage return
    print(" : " + grbl_out.decode().strip())

# Wait here until grbl is finished to close serial port and file.
#raw_input("  Press <Enter> to exit and disable grbl.")

# Close file and serial port

f.close()

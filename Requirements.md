##List of requirements/packages for each program

**Driver.py** : pyserial,time

**Wells.py** : pyserial,time

**Valve.py** : pyserial,time

**DriverMS2000.py**: pyserial,time

**andorEmccd.py** : ctypes, time, numpy, threading, collections, contextlib.
The drivers from ANDOR corresponding to your system (either atmcd32d.dll or atmcd64d.dll). Need to make sure they are localized at the path indicated in the program.

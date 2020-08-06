from uldaq import (get_daq_device_inventory, DaqDevice, InterfaceType,
                   DigitalDirection, DigitalPortIoType)


daq_device = None;
interface_type = InterfaceType.USB

devices = get_daq_device_inventory(interface_type)
number_of_devices = len(devices)
if number_of_devices == 0:
    raise Exception('Error: No DAQ devices found')

print('Found', number_of_devices, 'DAQ device(s):')

daq_device = DaqDevice(devices[0])
descriptor = daq_device.get_descriptor()
print('\nConnecting to', descriptor.dev_string, '- please wait...')
daq_device.connect()

if daq_device:
    if daq_device.is_connected():
        daq_device.disconnect()
    daq_device.release()
    

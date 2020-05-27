from uldaq import (get_daq_device_inventory, DaqDevice, InterfaceType,
	AOutFlag,
	DigitalDirection,DigitalPortIoType)
from First_Project.Model.DAQ.base import DAQBase

class Daq(DAQBase):

	# Define the __init__ construction method
	# ---------------------------------------

	def __init__(self, DAQ_id):
		# print('Init of class Daq')
		super().__init__(DAQ_id)
		self.DAQ_id = DAQ_id
		self.interface_type = InterfaceType.USB

	# Define a method returning the id of the selected DAQ
	# ----------------------------------------------------

	def idn(self):
		print('The device unique id is {}'.format(self.DAQ_id))

	# Define the initialization method
	# --------------------------------
	
	def initialize(self):

    	# Check there is a DAQ connected to the computer
		# ----------------------------------------------

		devices = get_daq_device_inventory(self.interface_type)
		number_of_devices = len(devices)
		if number_of_devices == 0:
			raise Exception('Error: No DAQ devices found')

		# Look for the device with the proper ID
		# --------------------------------------

		for device in devices:
			id = device.unique_id
			if id == self.DAQ_id:

				daq_device = DaqDevice(device)
				daq_device.connect()
				self.daq_device = daq_device
				print('\nThe device with ID={} was found and connected'.format(self.DAQ_id))

			else:
				self.daq_device = None
				print("\nThe device with ID={} was not found".format(self.DAQ_id))

	
	# Define a method to set the voltage of an output channel
	# -------------------------------------------------------

	def set_ao_voltage(self,ao_channel,voltage):

		if self.daq_device.is_connected():
			ao_device = self.daq_device.get_ao_device()

			if ao_device is None:
				raise Exception('Error: The DAQ device does not support analog output')

			# SHOULD BE A CONFIG PARAMETER OF THE DAQ

			ao_info = ao_device.get_info()
			output_range = ao_info.get_ranges()[0] # The range is -10/10V
			Nports = ao_info.get_num_chans()

			# SHOULD CHECK THE VOLTAGE IS WITHIN THE RANGE

			if ao_channel<=Nports:
				ao_device.a_out(ao_channel, output_range, AOutFlag.DEFAULT, float(voltage))
			else:
				print('The ao channel does not exist')
		else:
			print('The DAQ is not connected')


	# Define a method to set the digital output state
	# -----------------------------------------------

	def set_do_value(self,do_channel,value):

		if self.daq_device.is_connected():
			dio_device = self.daq_device.get_dio_device()

			if dio_device is None:
				raise Exception('Error: The DAQ device does not support digital output')

			dio_info = dio_device.get_info()
			Nports = dio_info.get_num_ports()
			port_types = dio_info.get_port_types()

			print(Nports)
			print(port_types)

			if do_channel<=Nports:
				port_to_write = port_types[do_channel]
				port_info = dio_info.get_port_info(port_to_write)
			else:
				print('The do channel does not exist')


			# Configure the port for output.
			if (port_info.port_io_type == DigitalPortIoType.IO or port_info.port_io_type == DigitalPortIoType.BITIO):
				dio_device.d_config_port(port_to_write, DigitalDirection.OUTPUT)

			print('    Function demonstrated: dio_device.d_out()')
			print('    Port: ', port_types[do_channel].name)



			if value == 1:
				dio_device.d_out(port_to_write,int(255))
			elif value == 0:
				dio_device.d_out(port_to_write,int(0))
			else:
				print('The set value is not valid (should be either 0 or 1)')


	# Define the release method for disconnecting the DAQ
	# ---------------------------------------------------

	def disconnect(self):

		if self.daq_device.is_connected():
			self.daq_device.disconnect()

		self.daq_device.release()
		print('\nConnection closed')

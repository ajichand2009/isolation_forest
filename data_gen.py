#!/usr/bin/python3

# Generate network packets.

import numpy as np



# TODO: Create hashmap of attributes to indices. This will help in conversion of
#       objects to Numpy arrays for further processing.

# TODO: Generate random connections with random packets.

class Packet:
	def __init__(self,
				 src_ip_addr="192.168.1.1",
				 dst_ip_addr="192.168.1.2",
				 src_port="1",
				 dst_port="2",
				 packet_type="body", # start/stop/body/ack
				 header_bytes="1",
				 payload_bytes="1",
				 application_protocol="https"): # ftp, http, https
		self.src_ip_addr = src_ip_addr
		self.dst_ip_addr = dst_ip_addr
		self.src_port = src_port
		self.dst_port = dst_port
		self.packet_type = packet_type
		self.header_bytes = header_bytes
		self.payload_bytes = payload_bytes
		self.application_protocol = application_protocol
	
	def print_attributes(self):
		print("Source IP Address : ",self.src_ip_addr)
		print("Destination IP Address :",self.dst_ip_addr)
		print("Source Port :",self.src_port)
		print("Destination Port :",self.dst_port)
		print("Packet Type :",self.packet_type)
		print("Total number of Header bytes :",self.header_bytes)
		print("Total number of Payload bytes :",self.payload_bytes)
		print("Application Protocol :",self.application_protocol)

class Connection:
	def __init__(self,
				 start_time=0,
				 end_time=1,
				 device=0,
				 port=1,
				 server=2,
				 num_packets=1,
				 total_header_bytes=1,
				 total_payload_bytes=1):
	
		self.start_time = start_time
		self.end_time = end_time
		self.device =device
		self.port = port
		self.server = server
		self.num_packets = num_packets
		self.total_header_bytes = total_header_bytes
		self.total_payload_bytes = total_payload_bytes

	def print_attributes(self):
		print("Start Time :",self.start_time)
		print("End Time :",self.end_time)
		print("Device :",self.device)
		print("Port :",self.port)
		print("Server :",self.server)
		print("Number of Packets :",self.num_packets)
		print("Total number of bytes of Header :",self.total_header_bytes)
		print("Total number of bytes of Payload:",self.total_payload_bytes)


#!/usr/bin/python3

# Generate network packets.

import numpy as np


np.random.seed(1)

#========================================================================

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
		#self.numpy_array = np.asarray([src_ip_addr,dst_ip_addr,src_port,dst_port,packet_type,header_bytes,payload_bytes,application_protocol])
	
	def print_attributes(self):
		print("Source IP Address : ",self.src_ip_addr)
		print("Destination IP Address :",self.dst_ip_addr)
		print("Source Port :",self.src_port)
		print("Destination Port :",self.dst_port)
		print("Packet Type :",self.packet_type)
		print("Total number of Header bytes :",self.header_bytes)
		print("Total number of Payload bytes :",self.payload_bytes)
		print("Application Protocol :",self.application_protocol)
		#print("Numpy array :",self.numpy_array)

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
		#self.numpy_array = np.array([start_time,end_time,device,port,server,num_packets,total_header_bytes,total_payload_bytes])

	def print_attributes(self):
		print("Start Time :",self.start_time)
		print("End Time :",self.end_time)
		print("Device :",self.device)
		print("Port :",self.port)
		print("Server :",self.server)
		print("Number of Packets :",self.num_packets)
		print("Total number of bytes of Header :",self.total_header_bytes)
		print("Total number of bytes of Payload:",self.total_payload_bytes)
		#print("Numpy Array:",self.numpy_array)

#========================================================================

packet_type_array = ["start","stop","body","ack"]
application_protocol_array = ["ftp","http","https"]
ip_addr_array = []

ip_addr_prefix = "192.168.1."

for i in range(100):
	x = ip_addr_prefix+str(i)
	ip_addr_array.append(x)

def gen_random_packet():
	packet_type = np.random.choice(packet_type_array)
	application_protocol = np.random.choice(application_protocol_array)
	src_ip_addr = np.random.choice(ip_addr_array)
	dst_ip_addr = np.random.choice(ip_addr_array)
	src_port = np.random.randint(1,10)
	dst_port = np.random.randint(1,10)
	header_bytes = np.random.randint(1,5)
	payload_bytes = np.random.randint(1,10)
	if src_ip_addr != dst_ip_addr and src_port != dst_port:
		print("Creating packet...")
		p = Packet(src_ip_addr,dst_ip_addr,src_port,dst_port,packet_type,header_bytes,payload_bytes,application_protocol)
		return p

def gen_random_connection():
	start_time = np.random.randint(1,100)
	end_time = start_time + np.random.randint(1,5)
	device = np.random.randint(1,10)
	port = np.random.randint(1,10)
	server = np.random.randint(1,10)
	num_packets = np.random.randint(1,10)
	header_bytes = np.random.randint(1,5)
	payload_bytes = np.random.randint(1,10)
	c = Connection(start_time,end_time,device,port,server,num_packets,header_bytes,payload_bytes)
	return c

for i in range(10):
	p = gen_random_packet()
	p.print_attributes()
	print("\nEND OF PACKET\n")

for i in range(10):
	c = gen_random_connection()
	c.print_attributes()
	print("\nEND OF CONNECTION\n")

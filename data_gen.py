#!/usr/bin/python3

# Generate network packets.

import numpy as np


np.random.seed(1)

# Port numbers range from 0 - 65535 ( 16 bits used to encode all combinations ).
# System Ports ( 0 - 1023 )
# User Ports ( 1024 - 49151 )
# Private/Dynamic Ports ( 49152 - 65535)

#========================================================================
# CLASSES
#========================================================================

class Packet:
	def __init__(self,
				 src_ip_addr="192.168.1.1",
				 dst_ip_addr="192.168.1.2",
				 src_port= 1,
				 dst_port= 2,
				 packet_type= "body", # start(syn)/stop(fin)/body/ack
				 header_bytes= 1,
				 payload_bytes= 1,
				 network_protocol = "tcp" # tcp, udp
				 application_protocol= "https"): # ftp, http, https
		self.src_ip_addr = src_ip_addr
		self.dst_ip_addr = dst_ip_addr
		self.src_port = src_port
		self.dst_port = dst_port
		self.packet_type = packet_type
		self.header_bytes = header_bytes
		self.payload_bytes = payload_bytes
		self.network_protocol = network_protocol
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
		print("Network Protocol :",self.network_protocol)
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
				 src_ip_addr = "192.168.1.1",
				 src_port = 1,
				 dst_ip_addr = "192.168.1.2",
				 dst_port = 2,
				 total_header_bytes=1,
				 total_payload_bytes=1):
	
		self.start_time = start_time
		self.end_time = end_time
		self.device =device
		self.port = port
		self.server = server
		self.num_packets = num_packets
		
		self.src_ip_addr = src_ip_addr
		self.src_port = src_port
		self.dst_ip_addr = dst_ip_addr
		self.dst_port = dst_port

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

		print("Source IP address :",self.src_ip_addr)
		print("Source Port :",self.src_port)
		print("Destination IP address :",self.dst_ip_addr)
		print("Destination Port :",self.dst_port)

		print("Total number of bytes of Header :",self.total_header_bytes)
		print("Total number of bytes of Payload:",self.total_payload_bytes)
		#print("Numpy Array:",self.numpy_array)

class Node:
	def __init__(self,server=0,ip_addr="192.168.1.1",port=1,transaction_state="IDLE"):
		self.server = server # 0 :- Device ; 1 :- Server
		self.ip_addr = ip_addr
		self.port = port
		self.received_packet = None
		self.packet_to_send = None
		self.sent_packet_array = []
		self.received_packet_array = []
		self.transaction_state = transaction_state # IDLE,SYN_ACK_WAIT,FIN_ACK_WAIT,FIN_ACK_WAIT_2,DATA_TRANSFER
	
	def set_packet(self,ip_addr,port):
		self.packet_to_send = gen_random_packet()
		self.packet_to_send.src_ip_addr = self.ip_addr
		self.packet_to_send.src_port = self.port
		self.packet_to_send.dst_ip_addr = ip_addr
		self.packet_to_send.dst_port = port
		self.sent_packet_array.append(packet_to_send)
	
	def initiate_transaction(self):
		self.packet_to_send.packet_type = "syn"
		self.transaction_state = "SYN_ACK_WAIT_1"

	def end_transaction(self):
		self.packet_to_send.packet_type = "fin"
		self.transaction_state = "FIN_ACK_WAIT_1"

	def response_transaction(self):
		if self.received_packet.packet_type == "syn" and self.transaction_state == "IDLE":
			self.set_packet(received_packet.ip_addr,received_packet.port)
			self.packet_to_send.packet_type = "syn_ack"
			self.transaction_state = "SYN_ACK_WAIT_2"
		elif self.received_packet.packet_type == "syn_ack" and self.transaction_state == "SYN_ACK_WAIT":
			self.set_packet(received_packet.ip_addr,received_packet.port)
			self.packet_to_send.packet_type = "ack"
			self.transaction_state = "DATA_TRANSFER"
		elif self.received_packet.packet_type == "fin" and self.transaction_state == "DATA_TRANSFER":
			self.set_packet(received_packet.ip_addr,received_packet.port)
			self.packet_to_send.packet_type = "ack"
			self.transaction_state = "FIN_ACK_WAIT_2"
		elif self.transaction_state == "FIN_ACK_WAIT_2":
			self.set_packet(received_packet.ip_addr,received_packet.port)
			self.packet_to_send.packet_type = "fin"
			self.transaction_state = "FIN_ACK_WAIT_3"
		elif self.received_packet.packet_type == "fin" and self.transaction_state == "FIN_ACK_WAIT_1":	
			self.set_packet(received_packet.ip_addr,received_packet.port)
			self.packet_to_send.packet_type = "ack"
			self.transaction_state = "IDLE"
		elif self.received_packet.packet_type == "ack" and self.transaction_state == "SYN_ACK_WAIT_2":
			self.transaction_state = "DATA_TRANSFER"
		elif self.received_packet.packet_type == "ack" and self.transaction_state == "FIN_ACK_WAIT_2":
			self.transaction_state = "IDLE"

	def get_packet(self,packet):
		if packet is not None and packet.dst_ip_addr == self.ip_addr and packet.dst_port == self.port:
			self.received_packet = packet
			self.received_packet_array.append(packet)

	def send_syn_packet(self,ip_addr,port):
		self.packet_to_send = gen_random_packet()
		self.packet_to_send.packet_type = "syn"
		self.packet_to_send.src_ip_addr = self.ip_addr
		self.packet_to_send.src_port = self.port
		self.packet_to_send.dst_ip_addr = ip_addr
		self.packet_to_send.dst_port = port
		self.transaction_state = "SYN_ACK_WAIT_1"
	
	def send_syn_ack_packet(self):
		if self.received_packet is not None and self.received_packet.packet_type == "syn":
			self.packet_to_send = self.received_packet
			self.packet_to_send.packet_type = "syn_ack"

	
	def send_fin_packet(self):
		self.packet_to_send = gen_random_packet()
		self.packet_to_send.packet_type = "fin"
	
	def send_ack_packet(self):
		self.packet_to_send = self.received_packet
		self.packet_to_send.packet_type = "ack"
		if self.transaction_state == "SYN_ACK":
			self.transaction_state = "DATA_TRANSFER"
				

#========================================================================
# END CLASSES
#========================================================================

#========================================================================
# FUNCTIONS
#========================================================================

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

#========================================================================
# END FUNCTIONS
#========================================================================


packet_type_array = ["syn","fin","body","ack","syn_ack"]
application_protocol_array = ["ftp","http","https"]
ip_addr_array = []

ip_addr_prefix = "192.168.1."

# Generate array of IP addresses.

for i in range(100):
	x = ip_addr_prefix+str(i)
	ip_addr_array.append(x)

n1 = Node()
n1.ip_addr = "192.168.1.1"
n1.server = 1
n1.port = 1

n2 = Node()
n2.ip_addr = "192.168.1.2"
n2.server = 0
n2.port = 2

for i in range(10):
	p = gen_random_packet()
	p.print_attributes()
	print("\nEND OF PACKET\n")


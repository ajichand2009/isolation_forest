#!/usr/bin/python3

# Generate network packets.

import numpy as np
from collections import deque


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
				 network_protocol = "tcp", # tcp, udp
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
				 src_ip_addr = "192.168.1.1",
				 src_port = 1,
				 dst_ip_addr = "192.168.1.2",
				 dst_port = 2,
				 cur_state = "IDLE",
				 nxt_state = "IDLE"):

		self.name = src_ip_addr+' '+str(src_port)+' '+dst_ip_addr+' '+str(dst_port)
		self.invert_name = dst_ip_addr+' '+str(dst_port)+' '+src_ip_addr+' '+str(src_port)
		
		self.src_ip_addr = src_ip_addr
		self.src_port = src_port
		self.dst_ip_addr = dst_ip_addr
		self.dst_port = dst_port

		self.cur_state = cur_state
		self.nxt_state = nxt_state

		self.packet = None
		self.packet_array = []

	def print_attributes(self):

		print("Source IP address :",self.src_ip_addr)
		print("Source Port :",self.src_port)
		print("Destination IP address :",self.dst_ip_addr)
		print("Destination Port :",self.dst_port)

		print("Current State :",self.cur_state)
		print("Next State :",self.nxt_state)

	def next_state(self):
		if(self.packet.packet_type=="syn" and self.cur_state=="SRC_SYN"):
			self.nxt_state = "DST_SYN_ACK"
		elif(self.packet.packet_type=="syn_ack" and self.cur_state=="DST_SYN_ACK"):
			self.nxt_state = "SRC_SYN_ACK"
		elif(self.packet.packet_type=="ack" and self.cur_state=="SRC_SYN_ACK"):
			self.nxt_state = "READY"
		elif(self.packet.packet_type=="fin" and self.cur_state=="SRC_FIN"):
			self.nxt_state = "DST_FIN_ACK"
		elif(self.packet.packet_type=="ack" and self.cur_state=="DST_FIN_ACK"):
			self.nxt_state = "DST_FIN"
		elif(self.packet.packet_type=="fin" and self.cur_state=="DST_FIN"):
			self.nxt_state = "SRC_FIN_ACK"
		elif(self.packet.packet_type=="ack" and self.cur_state=="DST_FIN"):
			self.nxt_state = "IDLE"

	def nxt_state_set(self,packet=None):
		conn_name = generate_connection_name(self.src_ip_addr,self.src_port,self.dst_ip_addr,self.dst_port)
		if packet is None and conn_name in receive_map and receive_map[conn_name]:
			packet = receive_map[conn_name].pop()
		if(self.cur_state=="IDLE"):
			if(packet.packet_type=="syn"):
				self.nxt_state = "SYN_WAIT"
		elif(self.cur_state=="SYN_GEN"):
			self.nxt_state = "SYN_ACK_WAIT"
		elif(self.cur_state=="SYN_WAIT"):
			self.nxt_state = "ACK_WAIT_SYN"
		elif(self.cur_state=="SYN_ACK_WAIT"):
			if(packet.packet_type=="syn_ack"):
				self.nxt_state = "SEND_READY"
		elif(self.cur_state=="ACK_WAIT_SYN"):
			if(packet.packet_type=="ack"):
				self.nxt_state = "RECEIVE_READY"
		elif(self.cur_state=="FIN_GEN"):
			self.nxt_state = "ACK_WAIT_FIN_1"
		elif(self.cur_state=="FIN_WAIT"):
			self.nxt_state = "FIN_GEN_2"
		elif(self.cur_state=="FIN_GEN_2"):
			self.nxt_state = "ACK_WAIT_FIN_2"
		elif(self.cur_state=="ACK_WAIT_FIN_1"):
			if(packet.packet_type=="ack"):
				self.nxt_state = "FIN_WAIT_2"
		elif(self.cur_state=="FIN_WAIT_2"):
			self.nxt_state = "IDLE"
		elif(self.cur_state=="ACK_WAIT_FIN_2"):
			if(packet.packet_type=="ack"):
				self.nxt_state = "IDLE"
		elif(self.cur_state=="SEND_READY"):
			if(packet.packet_type=="fin"):
				self.nxt_state = "FIN_WAIT"
		elif(self.cur_state=="RECEIVE_READY"):
			if(packet.packet_type=="fin"):
				self.nxt_state = "FIN_WAIT"
	
	def cur_state_action(self):
		conn_name = generate_connection_name(self.src_ip_addr,self.src_port,self.dst_ip_addr,self.dst_port)
		p = Packet(self.src_ip_addr,self.src_port,self.dst_ip_addr,self.dst_port)
		if(self.cur_state=="SYN_GEN"): # Switch to SYN_ACK_WAIT state.
			p.packet_type = "syn"
			if conn_name in send_map:
				send_map[conn_name].append(p)
			#self.nxt_state = "SYN_ACK_WAIT"
		elif(self.cur_state=="SYN_WAIT"): # Send SYN_ACK packet and switch to ACK_WAIT_SYN state.
			p.packet_type = "syn_ack"
			if conn_name in send_map:
				send_map[conn_name].append(p)
			#self.nxt_state = "ACK_WAIT_SYN"
		elif(self.cur_state=="SYN_ACK_WAIT"): # Send ACK packet and switch to SEND_READY state.
			p.packet_type = "ack"
			if conn_name in send_map:
				send_map[conn_name].append(p)
			#self.nxt_state = "SEND_READY"
		#elif(self.cur_state=="ACK_WAIT_SYN"): # Switch to RECEIVE_READY state.
			#self.nxt_state = "RECEIVE_READY"
		elif(self.cur_state=="FIN_GEN"): # Switch to ACK_WAIT_FIN_1 state
			p.packet_type = "fin"
			if conn_name in send_map:
				send_map[conn_name].append(p)
			#self.nxt_state = "ACK_WAIT_FIN_1"
		elif(self.cur_state=="FIN_WAIT"): # Send ACK. Switch to FIN_GEN_2 state.
			p.packet_type = "ack"
			if conn_name in send_map:
				send_map[conn_name].append(p)
			#self.nxt_state = "FIN_GEN_2"
		elif(self.cur_state=="FIN_GEN_2"): # Send FIN. Switch to ACK_WAIT_FIN_2 state.
			p.packet_type = "fin"
			if conn_name in send_map:
				send_map[conn_name].append(p)
			#self.nxt_state = "ACK_WAIT_FIN_2"
		#elif(self.cur_state=="ACK_WAIT_FIN_1"): # Switch to FIN_WAIT_2 state.
			#self.nxt_state = "FIN_WAIT_2"
		elif(self.cur_state=="FIN_WAIT_2"): # Send ACK. Switch to IDLE state.
			p.packet_type = "ack"
			send_map[conn_name].append(p)
			#self.nxt_state = "IDLE"
		#elif(self.cur_state=="ACK_WAIT_FIN_2"): # Switch to IDLE state.
			#self.nxt_state = "IDLE"
		elif(self.cur_state=="SEND_READY"): # Send data packet.
			p.packet_type = "data"
			if conn_name in send_map:
				send_map[conn_name].append(p)


class Node:
	def __init__(self,node_type="device",ip_addr="192.168.1.1",n_ports=100,max_conn_per_port=10):
		self.node_type = node_type
		self.ip_addr = ip_addr
		self.n_ports = n_ports
		self.act_conn = {} # TO BE DEPRECATED (?) ; currently maps ports to connection names
		for i in range(n_ports):
			self.act_conn[i] = {}
		self.max_conn_per_port = max_conn_per_port
		self.conn_map = {} # Map connection names to connection instances.

	def perform_conn_actions(self):
		for i in self.conn_map.keys():
			self.conn_map[i].nxt_state_set()
			self.conn_map[i].cur_state_action()

	def perform_state_update(self): # Update current state of each connection in the node.
		for i in self.conn_map.keys():
			self.conn_map[i].cur_state = self.conn_map[i].nxt_state

	def update_queue(self): # Transfer packets from send queue to receive queue.
		for i in self.conn_map.keys():
			if(send_map[i]):
				receive_map[i].append(send_map[i].pop())

	def add_connection(self,port1,ip2,port2): # TO BE DEPRECATED (?)
		conn_name = generate_connection_name(self.ip_addr,port1,ip2,port2)
		conn = Connection(self.ip_addr,port1,ip2,port2)
		self.conn_map[conn_name] = conn
										
	def send_syn_packet(self,src_port,dst_ip_addr,dst_port):
		p = Packet()
		p.src_ip_addr = self.ip_addr
		p.src_port = src_port
		p.dst_ip_addr = dst_ip_addr
		p.dst_port = dst_port
		p.packet_type = "syn"
		return p

	def send_syn_ack_packet(self,src_port,dst_ip_addr,dst_port):
		p = Packet()
		p.src_ip_addr = self.ip_addr
		p.src_port = src_port
		p.dst_ip_addr = dst_ip_addr
		p.dst_port = dst_port
		p.packet_type = "syn_ack"
		return p

    
	def send_ack_packet(self,src_port,dst_ip_addr,dst_port):
		p = Packet()
		p.src_ip_addr = self.ip_addr
		p.src_port = src_port
		p.dst_ip_addr = dst_ip_addr
		p.dst_port = dst_port
		p.packet_type = "ack"
		return p

	def send_fin_packet(self,src_port,dst_ip_addr,dst_port):
		p = Packet()
		p.src_ip_addr = self.ip_addr
		p.src_port = src_port
		p.dst_ip_addr = dst_ip_addr
		p.dst_port = dst_port
		p.packet_type = "fin"
		return p

	def send_data_packet(self,src_port,dst_ip_addr,dst_port):
		p = Packet()
		p.src_ip_addr = self.ip_addr
		p.src_port = src_port
		p.dst_ip_addr = dst_ip_addr
		p.dst_port = dst_port
		p.packet_type = "data"
		return p

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
	node_type = np.random.randint(1,10)
	num_packets = np.random.randint(1,10)
	header_bytes = np.random.randint(1,5)
	payload_bytes = np.random.randint(1,10)
	c = Connection(start_time,end_time,device,port,node_type,num_packets,header_bytes,payload_bytes)
	return c

def generate_random_connection(n1,n2):
	src_ip_addr = n1.ip_addr
	src_port = np.random.randint(n1.n_ports)
	dst_ip_addr = n2.ip_addr
	dst_port = np.random.randint(n2.n_ports)
	c1 = Connection(src_ip_addr,src_port,dst_ip_addr,dst_port)
	c2 = Connection(src_ip_addr,src_port,dst_ip_addr,dst_port)
	n1.act_conn[src_port][c1.name] = c1
	n2.act_conn[dst_port][c1.name] = c1

def generate_connection_name(src_ip_addr,src_port,dst_ip_addr,dst_port):
	name = src_ip_addr+' '+str(src_port)+' '+dst_ip_addr+' '+str(dst_port)
	return name

def generate_invert_connection_name(src_ip_addr,src_port,dst_ip_addr,dst_port):
	invert_name = dst_ip_addr+' '+str(dst_port)+' '+src_ip_addr+' '+str(src_port)
	return invert_name

def generate_connection_info(name):
	[src_ip_addr,src_port,dst_ip_addr,dst_port] = ' '.split(name)
	return [src_ip_addr,src_port,dst_ip_addr,dst_port]


def start_connection(ip1,port1,ip2,port2):
	node1 = node_map[ip1]
	node2 = node_map[ip2]
	node1.add_connection(port1,ip2,port2)
	node2.add_connection(port2,ip1,port1)
	p = node1.send_syn_packet(port1,ip2,port2)
	conn_name = generate_connection_name(ip1,port1,ip2,port2)
	conn = Connection(ip1,port1,ip2,port2)
	node1.conn_map[conn_name] = Connection(ip1,port1,ip2,port2,"SYN_GEN","IDLE")
	node2.conn_map[conn_name] = Connection(ip1,port1,ip2,port2,"IDLE","IDLE")

def end_connection(ip1,port1,ip2,port2):
	node1 = node_map[ip1]
	node2 = node_map[ip2]
	conn_name = generate_connection_name(ip1,port1,ip2,port2)
	if conn_name in node1.conn_map:
		node1.conn_map[conn_name].cur_state = "FIN_GEN"
	if conn_name in node2.conn_map:
		node2.conn_map[conn_name].cur_state = "IDLE"

#========================================================================
# END FUNCTIONS
#========================================================================

#========================================================================
# MAIN
#========================================================================

packet_type_array = ["syn","fin","body","ack","syn_ack"]
application_protocol_array = ["ftp","http","https"]
ip_addr_array = []

ip_addr_prefix = "192.168.1."

# Generate array of IP addresses.

for i in range(100):
	x = ip_addr_prefix+str(i)
	ip_addr_array.append(x)

# Global variables

node_map = {}
connection_map = {}

for i in range(100):
	n = Node()
	n.ip_addr = ip_addr_array[i]
	node_map[n.ip_addr] = n

# Map connection names to queue of packets.
send_map = {}
receive_map = {}

start_connection("192.168.1.1",1,"192.168.1.2",2)

timeunit = 0

for i in range(5):
	for i in node_map.keys():
		node_map[i].perform_conn_actions()
	timeunit += 1
	for i in node_map.keys():
		node_map[i].perform_state_update()
		node_map[i].update_queue()


#========================================================================
# END MAIN
#========================================================================

# LOGIC
# Send queue and receive queue contain 'Packet' objects.
# In a time-unit, every 'Node' object performs its 'init_proc'
# based on the current state of each of its connections.
# Then, every 'Node' object performs its 'resp_proc' based on the
# current state of each of its connections.
# After this, increment time unit and update states of all connections on
# all 'Node' objects.
# Packet transfer is done via Send and Receive Queues. Transfer packet
# from send queue to receive queue upon incrementing time unit ( along with state update ).
# Every Node sends packet to send queue, and receives packet from receive queue.
# A packet is 'received' only if IP address of destination, matches that of the node.
# 'resp_proc' relies on this packet reception.

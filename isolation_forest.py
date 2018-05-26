#!/usr/bin/python

import numpy as np

########################################################################
# CLASSES
########################################################################
class Node:
	def __init__(self,data):
		self.left = None
		self.right = None
		self.data = data
	
	def insert(self,data):
		if data < self.data:
			if self.left is None:
				self.left = Node(data)
			else:
				self.left.insert(data)
		elif data > self.data:
			if self.right is None:
				self.right = Node(data)
			else:
				self.right.insert(data)
		else:
			self.data = data

	def lookup(self,data,parent=None):
		if data < self.data:
			if self.left is None:
				return None,None
			return self.left.lookup(data,self)
		elif data > self.data:
			if self.right is None:
				return None,None
			return self.right.lookup(data,self)
		else:
			return self,parent
	
	def path_length(self,data,length=0):
		if data < self.data:
			if self.left is None:
				return length
			return self.left.path_length(data,length+1)
		elif data > self.data:
			if self.right is None:
				return length
			return self.right.path_length(data,length+1)
		else:
			return length

	def children_count(self):
		count = 0
		if self.left:
			count += 1
		if self.right:
			count += 1
		return count

	def delete(self,data):
		node,parent = self.lookup(data)
		if node is not None:
			children_count = node.children_count()
		if children_count == 0:
			if parent:
				if parent.left is node:
					parent.left = None
				else:
					parent.right = None
				del node
			else:
				self.data = None
		elif children_count == 1:
			if node.left:
				n = node.left
			else:
				n = node.right
			if parent:
				if parent.left is node:
					parent.left = n
				else:
					parent.right = n
				del node
			else:
				self.left = n.left
				self.right = n.right
				self.data = n.data
		else:
			parent = node
			successor = node.right
			while successor.left:
				parent = successor
				successor = successor.left
			node.data = successor.data
			if parent.left == successor:
				parent.left = successor.right
			else:
				parent.right = successor.right

	def print_tree(self):
		if self.left:
			self.left.print_tree()
		print self.data
		if self.right:
			self.right.print_tree()

	def compare_trees(self,node):
		if node is None:
			return False
		if self.data != node.data:
			return False
		res = True
		if self.left is None:
			if node.left:
				return False

class Tree:
	def __init__(self,data,max_depth,pivot_attr,pivot_val):
		self.root_node = Node(data)
		self.node_count = 1
		self.depth = 0
		self.max_depth = max_depth
		# 'pivot_attr' is an index to a Numpy 1-D array.
		self.pivot_attr = pivot_attr
		# 'pivot_val' is the value of 'data[pivot_attr]' of the root node.
		# This is the value around which the tree is built.
		self.pivot_val = pivot_val

	def add_node(self,data):
		self.root_node.insert(data)
	
	def lookup_node(self,data):
		self.root_node.lookup(data)
	
	def delete_node(self,data):
		self.root_node.delete(data)

	def path_length(self,data):
		self.root_node.path_length(data)

class Forest:
	def __init__(self,data,num_trees):
		self.tree_list = []
		self.tree_list.append(Tree(data,8))
		self.num_trees = num_trees

########################################################################
# FUNCTIONS
########################################################################
def harmonic(x):
	y = np.log2(x)+0.5772156649
	# The number is Euler's constant.
	return y

def average_path_length(x):
	y = 2*harmonic(x-1) - (2*(x-1)/x)
	return y	

def anomaly_score(x,tree,n):
	s = 2**(-tree.path_length(x)/average_path_length(n))
	return s

########################################################################
# MAIN
########################################################################

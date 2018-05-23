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

########################################################################
# FUNCTIONS
########################################################################


########################################################################
# MAIN
########################################################################

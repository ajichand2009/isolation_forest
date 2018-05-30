#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt

########################################################################
# CLASSES
########################################################################
class Node:
	def __init__(self,data,pivot_attr,pivot_val=None,depth=0):
		self.left = None
		self.right = None
		self.data = data
		self.pivot_attr = pivot_attr
		self.pivot_val = pivot_val
		self.depth = depth

	def build_tree(self,height_limit=8):
		a = self.data[self.pivot_attr,:]
		a_min = np.min(a)
		a_max = np.max(a)
		#while self.data.shape[1] > 1 or self.depth < height_limit:
		if self.data.shape[1] > 1 and self.depth < height_limit and a_min < a_max:
			self.pivot_val = np.random.randint(a_min,a_max)
			left,right = partition(self.data,self.pivot_attr,self.pivot_val)
			self.left = Node(left,self.pivot_attr,self.pivot_val,self.depth+1)
			self.right = Node(right,self.pivot_attr,self.pivot_val,self.depth+1)
			self.left.build_tree()
			self.right.build_tree()
	
	def print_tree(self):
		print(self.data)
		if self.left:
			self.left.print_tree()
		if self.right:
			self.right.print_tree()
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

# Function to partition a matrix 'X' based on a pivot attribute
# (row index of the matrix) and a pivot value
def partition(X,pivot_attr,pivot_val=None):
	a = X[pivot_attr,:]
	if pivot_val is None:
		a_min = np.min(a)
		a_max = np.max(a)
		pivot_val = np.random.randint(a_min,a_max)
	b = np.where(a<pivot_val)
	c = np.where(a>=pivot_val)
#	d = np.where(a==pivot_val)
	Y = X[:,b[0]]
	Z = X[:,c[0]]
	print(pivot_val)
#	W = X[:,d[0]]
	return Y,Z

########################################################################
# MAIN
########################################################################
np.random.seed(1)
X = np.random.randint(100,size=(2,4))+1

X_train = X[:,0:7]
X_test = X[:,7:10]

t = Node(X,0)
t.build_tree()
t.print_tree()

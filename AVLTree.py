#id1:
#name1:
#username1:
#id2:
#name2:
#username2:


"""A class represnting a node in an AVL tree"""

class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 
	
	@type key: int
	@param key: key of your node
	@type value: string
	@param value: data of your node
	"""
	def __init__(self, key=None, value=None):  #added default values to key and value
		self.key = key
		self.value = value
		if key is not None:
			self.left: AVLNode = AVLNode()
			self.right: AVLNode = AVLNode()
			self.left.parent = self
			self.right.parent = self
			self.height = 0
		else:
			self.left = None
			self.right = None
			self.height = -1
		self.parent = None


	# פונקציה נחמדה שתאפשר להשוות נודים באמצעות אופרטור
	def __eq__(self, other):
		return isinstance(other, AVLNode) and self.key == other.key


	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		return self.key is not None


	# this function finds the next sequential node O(logn)
	def successor(self):
		curr_node = self

		# next sequential node is on the right below
		if self.right.is_real_node():
			curr_node = self.right
			while curr_node.left.is_real_node():
				curr_node = curr_node.left

		# next sequential node is on the right but above
		else:
			prev_node = curr_node
			curr_node = curr_node.parent
			while curr_node.key != None:
				if curr_node.left == prev_node:
					return curr_node
				prev_node = curr_node
				curr_node = curr_node.parent
		return curr_node

"""
A class implementing an AVL tree.
"""

class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.
	"""
	def __init__(self):
		self.root = AVLNode(None, None)
		self.max = None
		self.size = 0


	# custom functions
	# עדיף להעביר לNodeAVL ככה שלא תצטרך להעביר node כInput
	def _update_height(self, node):
		node.height = 1 + max(node.left.height, node.right.height)

	def _balance_factor(self, node):
		return node.left.height - node.right.height

	def _rotate_left(self, x):
		y = x.right
		x.right = y.left
		if y.left.is_real_node():
			y.left.parent = x

		y.parent = x.parent
		if x.parent is None:
			self.root = y
		elif x == x.parent.left:
			x.parent.left = y
		else:
			x.parent.right = y

		y.left = x
		x.parent = y

		self._update_height(x)
		self._update_height(y)

	def _rotate_right(self, x):
		y = x.left
		x.left = y.right
		if y.right.is_real_node():
			y.right.parent = x

		y.parent = x.parent
		if x.parent is None:
			self.root = y
		elif x == x.parent.right:
			x.parent.right = y
		else:
			x.parent.left = y

		y.right = x
		x.parent = y

		self._update_height(x)
		self._update_height(y)

	def _rebalance(self, node): # got modified to always go up to the root - critical in case of deletions (cost is still logn)
		promotes = 0

		while node is not None:
			old_height = node.height
			self._update_height(node)

			if node.height > old_height:
				promotes += 1

			bf = self._balance_factor(node)

			# Left heavy
			if bf == 2:
				if self._balance_factor(node.left) < 0:
					self._rotate_left(node.left)
				self._rotate_right(node)

			# Right heavy
			if bf == -2:
				if self._balance_factor(node.right) > 0:
					self._rotate_right(node.right)
				self._rotate_left(node)

			node = node.parent

		return promotes



	"""searches for a node in the dictionary corresponding to the key (starting at the root)
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def search(self, key):
		node = self.root
		edges = 0
		while node.is_real_node():
			if key == node.key:
				return node, edges + 1
			elif key < node.key:
				node = node.left
			else:
				node = node.right
			edges += 1
		return None, -1


	"""searches for a node in the dictionary corresponding to the key, starting at the max
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def finger_search(self, key):
		node = self.max
		edges = 0

		if node is None or not node.is_real_node():
			return None, -1
		if key > node.key:
			return None, -1
		if key == node.key:
			return node, 1
		
		while node.parent is not None and node.parent.is_real_node():
			if key > node.parent.key:
				break
			node = node.parent
			edges += 1
			if key == node.key:
				return node, edges + 1
			
		while node.is_real_node():
			if key == node.key:
				return node, edges + 1
			elif key < node.key:
				node = node.left
			else:
				node = node.right
			edges += 1

		return None, -1



	"""inserts a new node into the dictionary with corresponding key and value (starting at the root)

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""

	def insert(self, key, val):
		if not self.root.is_real_node():
			self.root = AVLNode(key, val)
			self.max = self.root
			return self.root, 0, 0

		node = self.root
		parent = None
		edges = 0

		while node.is_real_node():
			parent = node
			edges += 1
			if key < node.key:
				node = node.left
			else:
				node = node.right

		new_node = AVLNode(key, val)
		new_node.parent = parent

		if key < parent.key:
			parent.left = new_node
		else:
			parent.right = new_node

		# update max
		if self.max is None or key > self.max.key:
			self.max = new_node

		promotes = self._rebalance(parent)
		self.size += 1

		return new_node, edges, promotes



	"""inserts a new node into the dictionary with corresponding key and value, starting at the max

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""
	def finger_insert(self, key, val):
		if self.max is None or not self.max.is_real_node():
			self.root = AVLNode(key, val)
			self.max = self.root
			return self.root, 0, 0

		node = self.max
		edges = 0

		# climb up
		while node.parent is not None and key < node.parent.key:
			node = node.parent
			edges += 1

		# descend
		current = node
		while current.is_real_node():
			parent = current
			edges += 1
			if key < current.key:
				current = current.left
			else:
				current = current.right

		new_node = AVLNode(key, val)
		new_node.parent = parent

		if key < parent.key:
			parent.left = new_node
		else:
			parent.right = new_node

		# update max
		if key > self.max.key:
			self.max = new_node

		promotes = self._rebalance(parent)

		return new_node, edges, promotes



	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	"""
	def delete(self, node: AVLNode):
		if node is None or not node.is_real_node():
			return
		
		# update max if needed (if we are about to delete max)
		if self.max == node:
			if node.left.is_real_node():
				self.max = node.left
				while self.max.right.is_real_node():
					self.max = self.max.right
			else:
				self.max = node.parent

		# case 1: node has two real children
		if node.left.is_real_node() and node.right.is_real_node():
			succ = node.successor()
			node.key = succ.key
			node.value = succ.value
			node = succ  # now delete successor instead

		# case 2 and 3: node has one real child or none
		child = node.left if node.left.is_real_node() else node.right
		parent = node.parent

		if parent is None:
			self.root = child
			if child.is_real_node():
				child.parent = None
		else:
			if parent.left == node:
				parent.left = child
			else:
				parent.right = child
			if child.is_real_node():
				child.parent = parent

		self._rebalance(parent)
		self.size -= 1

	
	"""joins self with item and another AVLTree

	@type tree2: AVLTree 
	@param tree2: a dictionary to be joined with self
	@type key: int 
	@param key: the key separting self and tree2
	@type val: string
	@param val: the value corresponding to key
	@pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
	or the opposite way
	"""
	def join(self, tree2, key, val):
		# self is empty tree
		if not self.root.is_real_node():
			tree2.insert(key, val)
			self.root = tree2.root
			self.max = tree2.max
			return

		# tree2 is empty tree
		if not tree2.root.is_real_node():
			self.insert(key, val)
			return
		
		# define left_tree < key < right_tree
		if key > self.root.key:
			left_tree = self.root
			right_tree = tree2.root
		else: 
			left_tree = tree2.root
			right_tree = self.root

		# self and tree2 have the same height
		if left_tree.root.height == right_tree.root.height:
			new_root = AVLNode(key, val)
			new_root.left = left_tree.root
			new_root.right = right_tree.root
			left_tree.root.parent = new_root
			right_tree.root.parent = new_root

			self.root = new_root
			self._update_height(new_root)
			self._rebalance(new_root)
		
		#     \
		#      L
		#	    \
		#	     k
		#	    / \
		#	  L.r  R
		elif left_tree.root.height > right_tree.root.height:
			node = left_tree.root
			while node.right.height > right_tree.root.height:
				node = node.right

			new_node = AVLNode(key, val)
			new_node.left = node.right
			new_node.right = right_tree.root

			if new_node.left.is_real_node():
				new_node.left.parent = new_node
			right_tree.root.parent = new_node

			node.right = new_node
			new_node.parent = node

			self.root = left_tree.root
			self._rebalance(node)

		#            /
		#           R
		#		   /
		#		  k
		#		 / \
		#		L  R.l
		else:
			node = right_tree.root
			while node.left.height > left_tree.root.height:
				node = node.left

			new_node = AVLNode(key, val)
			new_node.right = node.left
			new_node.left = left_tree.root

			if new_node.right.is_real_node():
				new_node.right.parent = new_node
			left_tree.root.parent = new_node

			node.left = new_node
			new_node.parent = node

			self.root = right_tree.root
			self._rebalance(node)

		self.max = right_tree.max
		self.size = self.size + 1 + tree2.size
		return


	"""splits the dictionary at a given node

	@type node: AVLNode
	@pre: node is in self
	@param node: the node in the dictionary to be used for the split
	@rtype: (AVLTree, AVLTree)
	@returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
	dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
	dictionary larger than node.key.
	"""
	def split(self, node):
		left_tree = AVLTree()
		right_tree = AVLTree()

		if node.left.is_real_node():
			left_tree.root = node.left
			left_tree.root.parent = None

		if node.right.is_real_node():
			right_tree.root = node.right
			right_tree.root.parent = None

		# Walk upward and rebuild
		curr = node
		parent = curr.parent

		while parent is not None:
			# curr is a left child
			if curr == parent.left:
				temp = AVLTree()
				if parent.right.is_real_node():
					temp.root = parent.right
					temp.root.parent = None

				temp.join(right_tree, parent.key, parent.value)
				right_tree = temp

			# curr is a right child
			else:
				temp = AVLTree()
				if parent.left.is_real_node():
					temp.root = parent.left
					temp.root.parent = None

				left_tree.join(temp, parent.key, parent.value)

			curr = parent
			parent = parent.parent

		# Update max
		if left_tree.root.is_real_node():
			left_tree.max = left_tree.root
			while left_tree.max.right.is_real_node():
				left_tree.max = left_tree.max.right

		if right_tree.root.is_real_node():
			right_tree.max = right_tree.root
			while right_tree.max.right.is_real_node():
				right_tree.max = right_tree.max.right

		return left_tree, right_tree

	
	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self):
		# go to the left node on the tree
		curr_node = self.root
		while curr_node.left.is_real_node():
			curr_node = curr_node.left

		array = []
		while curr_node != None:
			array.append((curr_node.key, curr_node.value))
			curr_node = curr_node.successor()
		return array


	"""returns the node with the maximal key in the dictionary

	@rtype: AVLNode
	@returns: the maximal node, None if the dictionary is empty
	"""
	def max_node(self):
		return self.max

	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""
	def size(self):
		return self.size


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		return self.root

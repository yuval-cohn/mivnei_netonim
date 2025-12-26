'''
    In order to run the tester:
    1.  Make sure your AVLTree.py file and this file
        are both in the same directory.
    2.  Run: python3 student_tester.py  
    3.  Your grade will be printed at the end.
        Only failed tests will be printed.
'''

import unittest
import numpy as np
from AVLTree import AVLTree, AVLNode

# pylint: disable=C0115,C0116

class BasicStudentTester(unittest.TestCase):

    def setUp(self):
        self.tree = AVLTree()

    def test_insert_small(self):
        self.tree.insert(10, "10")
        self.tree.insert(5, "5")
        self.tree.insert(15, "15")

        self.assertEqual(self.tree.size(), 3)
        self.assertIsNotNone(self.tree.search(10)[0])
        self.assertIsNotNone(self.tree.search(5)[0])
        self.assertIsNotNone(self.tree.search(15)[0])

    def test_delete_small(self):
        for i in range(5):
            self.tree.insert(i, str(i))

        self.assertEqual(self.tree.size(), 5)

        self.tree.delete(self.tree.search(0)[0])
        self.tree.delete(self.tree.search(3)[0])

        self.assertEqual(self.tree.size(), 3)

    def test_insert_delete_mix(self):
        nums = [7, 3, 9, 1, 5]
        for x in nums:
            self.tree.insert(x, str(x))

        self.assertEqual(self.tree.size(), 5)

        self.tree.delete(self.tree.search(5)[0])
        self.assertEqual(self.tree.size(), 4)

        self.tree.insert(20, "20")
        self.assertEqual(self.tree.size(), 5)

    # ------------------------------------
    # NEW TEST: max_node() correctness
    # ------------------------------------
    def test_max_node(self):
        # Empty dictionary
        self.assertIsNone(self.tree.max_node())

        # Insert values
        vals = [10, 4, 22, 8, 30, 1, 15]
        for x in vals:
            self.tree.insert(x, str(x))

        # Max should be 30
        self.assertIsNotNone(self.tree.max_node())
        self.assertEqual(self.tree.max_node().key, 30)

        # Delete the max node
        self.tree.delete(self.tree.search(30)[0])

        # Max should now be 22
        self.assertEqual(self.tree.max_node().key, 22)

class SearchTest(unittest.TestCase):
    def setUp(self):
        self.tree = AVLTree()
        keys = [50, 30, 70, 20, 40, 60, 80]
        for key in keys:
            self.tree.insert(key, str(key))

    def test_search_empty(self):
        tree = AVLTree()
        node, edges = tree.search(1)
        self.assertIsNone(node)
        self.assertEqual(1, edges)

    def test_search_existing(self):
        # self.tree.print_tree()
        node, edges = self.tree.search(60)
        self.assertIsNotNone(node)
        self.assertEqual(node.key, 60)
        self.assertEqual(3, edges)

    def test_search_non_existing(self):
        # self.tree.print_tree()
        node, edges = self.tree.search(90)
        self.assertIsNone(node)
        self.assertEqual(4, edges)

    def test_search_non_existing2(self):
        tree = AVLTree()
        keys = [4, 2, 6, 1, 3, 5, 7]
        for key in keys:
            tree.insert(key, str(key))
        # tree.print_tree()
        node, edges = tree.search(8)
        self.assertIsNone(node)
        self.assertEqual(4, edges)

    def test_search_num_edges(self):
        tree2 = AVLTree()
        num_nodes = int(1e3)
        for i in range(num_nodes):
            tree2.insert(i, str(i))
        print("Inserted " + str(num_nodes) + " nodes")
        self.assertEqual(tree2.size(), num_nodes)
        tree_height = tree2.get_root().height
        max_height = 0
        for i in range(num_nodes):
            node, edges = tree2.search(i)
            self.assertIsNotNone(node)
            self.assertEqual(node.key, i)
            max_height = max(max_height, edges)
        print("Max height found in searches: " + str(max_height))
        self.assertLessEqual(max_height, tree_height+1)

class FingerSearchTest(unittest.TestCase):
    def setUp(self):
        self.tree = AVLTree()
        keys = [10, 25, 5, 15, 3, 7, 12, 30]
        for key in keys:
            self.tree.insert(key, str(key))

    def test_empty_tree(self):
        empty_tree = AVLTree()
        node, edges = empty_tree.finger_search(10)
        self.assertIsNone(node)
        self.assertEqual(1, edges)

    def test_existing(self):
        # self.tree.print_tree()
        key = 30
        node, edges = self.tree.finger_search(key)
        self.assertIsNotNone(node)
        self.assertEqual(node.key, key)
        self.assertEqual(1, edges)

    def test_existing_far(self):
        # self.tree.print_tree()
        node, edges = self.tree.finger_search(5)
        self.assertIsNotNone(node)
        self.assertEqual(5, node.key)
        self.assertEqual(5, edges)

    def test_non_existing(self):
        # self.tree.print_tree()
        node, edges = self.tree.finger_search(40)
        self.assertIsNone(node)
        self.assertEqual(2, edges)

    def test_non_existing_far(self):
        # self.tree.print_tree()
        node, edges = self.tree.finger_search(1)
        self.assertIsNone(node)
        self.assertEqual(7, edges)

class InsertTest(unittest.TestCase):
    def setUp(self):
        self.tree = AVLTree()

    def test_insert_search(self):
        keys = [20, 10, 30, 5, 15, 25, 35]
        lengths = [0, 1, 1, 2, 2, 2, 2]
        heights = [0, 1, 0, 2, 0, 1, 0]
        for i, key in enumerate(keys):
            node, length, height = self.tree.insert(key, str(key))
            self.assertEqual(key, node.key)
            self.assertEqual(lengths[i], length)
            self.assertEqual(heights[i], height)
        # self.tree.print_tree()
        self.assertEqual(self.tree.size(), len(keys))
        for i, key in enumerate(keys):
            node, length = self.tree.search(key)
            self.assertIsNotNone(node)
            self.assertEqual(key, node.key)
            self.assertEqual(lengths[i] + 1, length)

    def test_insert_large(self):
        num_nodes = int(1e4)
        max_height = 0
        for i in range(num_nodes):
            res = self.tree.insert(i, str(i))
            max_height = max(max_height, res[1])
        print("Inserted " + str(num_nodes) + " nodes")
        self.assertEqual(self.tree.size(), num_nodes)
        height_limit = np.log2(num_nodes) + 1
        self.assertLessEqual(max_height, height_limit, "Tree height exceeds limit")

        for i in range(num_nodes):
            node, length = self.tree.search(i)
            self.assertIsNotNone(node)
            self.assertGreaterEqual(length, 0)

        print("Tested " + str(num_nodes) + " nodes")

    def test_insert_unbalanced_case1(self):
        keys = [6, 7, 8]
        for key in keys:
            self.tree.insert(key, str(key))
        # self.tree.print_tree()
        self.assertEqual(1, self.tree.get_root().height, "Tree height error")
        self.assertEqual(8, self.tree.max_node().key, "Max node error")

    def test_insert_unbalanced_case2(self):
        keys = [6, 8, 7]
        for key in keys:
            self.tree.insert(key, str(key))
        # self.tree.print_tree()
        self.assertEqual(1, self.tree.get_root().height, "Tree height error")
        self.assertEqual(8, self.tree.max_node().key, "Max node error")

    def test_insert_unbalanced_case3(self):
        keys = [8, 6, 7]
        for key in keys:
            self.tree.insert(key, str(key))
        # self.tree.print_tree()
        self.assertEqual(1, self.tree.get_root().height, "Tree height error")
        self.assertEqual(8, self.tree.max_node().key, "Max node error")

    def test_insert_unbalanced_case4(self):
        keys = [8, 7, 6]
        for key in keys:
            self.tree.insert(key, str(key))
        # self.tree.print_tree()
        self.assertEqual(1, self.tree.get_root().height, "Tree height error")
        self.assertEqual(8, self.tree.max_node().key, "Max node error")

    def test_insert_unbalanced(self):
        keys = [12, 8, 15, 6, 10, 14, 24, 11, 13, 20, 29, 19]
        for key in keys:
            self.tree.insert(key, str(key))
        self.assertEqual(4, self.tree.get_root().height, "Tree height error")
        self.tree.insert(18, str(18))
        # self.tree.print_tree()
        self.assertEqual(4, self.tree.get_root().height, "Tree height error")
        self.assertEqual(29, self.tree.max_node().key, "Max node error")

class FingerInsertTest(unittest.TestCase):
    def setUp(self):
        self.tree = AVLTree()
        self.keys = [50, 30, 70, 20, 40, 60, 80]
        for key in self.keys:
            self.tree.insert(key, str(key))
        self.assertEqual(self.tree.size(), len(self.keys))

    def test_finger_insert_empty_tree(self):
        tree = AVLTree()
        key = 5
        node, edges, height = tree.finger_insert(key, str(key))
        self.assertEqual(key, node.key)
        # tree.print_tree()
        self.assertEqual(0, edges)
        self.assertEqual(0, height)

    def test_finger_insert_close(self):
        key = 85
        node, edges, height = self.tree.finger_insert(key, str(key))
        self.assertEqual(key, node.key)
        self.assertEqual(1, edges)
        self.assertEqual(3, height)

    def test_finger_insert_far(self):
        key = 5
        node, edges, height = self.tree.finger_insert(key, str(key))
        self.assertEqual(key, node.key)
        # self.tree.print_tree()
        self.assertEqual(5, edges)
        self.assertEqual(3, height)

class DeleteTest(unittest.TestCase):
    def setUp(self):
        self.tree = AVLTree()

    def test_delete_empty_tree(self):
        virtual_node = AVLNode(None, None)
        node = AVLNode(10, "10")
        node.left = virtual_node
        node.right = virtual_node
        node.parent = virtual_node
        self.tree.delete(node)  # Should not raise an error

    def test_delete_node_not_in_tree(self):
        virtual_node = AVLNode(None, None)
        node = AVLNode(10, "10")
        node.left = virtual_node
        node.right = virtual_node
        node.parent = virtual_node
        self.tree.insert(20, "20")
        self.tree.delete(node)  # Should not raise an error

    def test_delete_case1(self):
        """ node is a leaf """
        keys = [20, 10, 30, 5, 15, 25]
        size_orig = len(keys)
        for key in keys:
            self.tree.insert(key, str(key))
        node = self.tree.search(25)[0]
        self.tree.delete(node)
        node = self.tree.search(25)[0]
        self.assertIsNone(node)
        # self.tree.print_tree()
        self.assertEqual(size_orig - 1, self.tree.size())

    def test_delete_case2(self):
        """ Node has 1 child """
        keys = [20, 10, 30, 5, 15, 25]
        size_orig = len(keys)
        for key in keys:
            self.tree.insert(key, str(key))
        node = self.tree.search(30)[0]
        self.tree.delete(node)
        node = self.tree.search(30)[0]
        self.assertIsNone(node)
        # self.tree.print_tree()
        length = self.tree.search(25)[1]
        self.assertEqual(2, length)
        self.assertEqual(size_orig - 1, self.tree.size())

    def test_delete_case3(self):
        """ node has two children """
        keys = [20, 10, 30, 5, 15, 25]
        size_orig = len(keys)
        for key in keys:
            self.tree.insert(key, str(key))
        # self.tree.print_tree()
        node = self.tree.search(10)[0]
        # Get successor before deletion
        successor = self.tree.search(15)[0]
        self.assertEqual(15, successor.key)
        self.tree.delete(node)
        node = self.tree.search(10)[0]
        self.assertIsNone(node)
        # self.tree.print_tree()
        self.assertEqual(size_orig - 1, self.tree.size())
        self.assertEqual(successor.key, 15, "Successor key error")

        # Replaced with successor
        node, length = self.tree.search(15)
        self.assertEqual(successor, node, "Node replacement error")
        self.assertEqual(2, length)

    def test_delete_case3b(self):
        """ node has two children """
        keys = [20, 10, 30, 5, 15, 25, 12]
        size_orig = len(keys)
        for key in keys:
            self.tree.insert(key, str(key))
        # self.tree.print_tree()
        node = self.tree.search(10)[0]
        # Get successor before deletion
        successor = self.tree.search(12)[0]
        self.assertEqual(12, successor.key)
        self.tree.delete(node)
        node = self.tree.search(10)[0]
        self.assertIsNone(node)
        # self.tree.print_tree()
        self.assertEqual(size_orig - 1, self.tree.size())
        self.assertEqual(successor.key, 12, "Successor key error")

        # Replaced with successor
        node, length = self.tree.search(12)
        self.assertEqual(successor, node, "Node replacement error")
        self.assertEqual(2, length)

    def test_delete_case4(self):
        """ node is the root and a leaf """
        key = 20
        self.tree.insert(key, str(key))
        node = self.tree.get_root()
        self.tree.delete(node)
        node = self.tree.get_root()
        self.assertIsNone(node)
        self.assertEqual(0, self.tree.size())

    def test_delete_case5(self):
        """ node is the root and has one child """
        keys = [20, 10]
        size_orig = len(keys)
        for key in keys:
            self.tree.insert(key, str(key))
        node = self.tree.search(20)[0]
        self.tree.delete(node)
        node = self.tree.search(20)[0]
        self.assertIsNone(node)
        # self.tree.print_tree()
        length = self.tree.search(10)[1]
        self.assertEqual(1, length)
        self.assertEqual(size_orig - 1, self.tree.size())

    def test_delete_case6(self):
        """ node is the root and has two children """
        keys = [20, 10, 30]
        size_orig = len(keys)
        for key in keys:
            self.tree.insert(key, str(key))
        # self.tree.print_tree()
        node = self.tree.search(20)[0]
        self.tree.delete(node)
        node = self.tree.search(20)[0]
        self.assertIsNone(node)
        # self.tree.print_tree()
        self.assertEqual(size_orig - 1, self.tree.size())

        # Replaced with successor
        length = self.tree.search(30)[1]
        self.assertEqual(1, length)
        length = self.tree.search(10)[1]
        self.assertEqual(2, length)

class DeleteUnbalancedTest(unittest.TestCase):
    def setUp(self):
        self.tree = AVLTree()

    def test_case1a(self):
        # Left rotation, BF of right child is 1
        keys = [6, 5, 7, 8]
        for key in keys:
            self.tree.insert(key, str(key))
        # self.tree.print_tree()
        node = self.tree.search(5)[0]
        self.tree.delete(node)
        # self.tree.print_tree()
        self.assertEqual(1, self.tree.get_root().height)
        self.assertEqual(8, self.tree.max_node().key, "Max node error")

    def test_case1b(self):
        # Left rotation, BF of right child is 0
        keys = [6, 5, 8, 7, 9]
        for key in keys:
            self.tree.insert(key, str(key))
        # self.tree.print_tree()
        node = self.tree.search(5)[0]
        self.tree.delete(node)
        # self.tree.print_tree()
        self.assertEqual(2, self.tree.get_root().height)
        self.assertEqual(9, self.tree.max_node().key, "Max node error")

    def test_case2(self):
        # Right then left rotation, BF of right child is 1
        keys = [6, 5, 8, 7]
        for key in keys:
            self.tree.insert(key, str(key))
        # self.tree.print_tree()
        node = self.tree.search(5)[0]
        self.tree.delete(node)
        # self.tree.print_tree()
        self.assertEqual(1, self.tree.get_root().height)
        self.assertEqual(8, self.tree.max_node().key, "Max node error")

    def test_case3(self):
        # Left then right rotation, BF of left child is -1
        keys = [8, 6, 9, 7]
        for key in keys:
            self.tree.insert(key, str(key))
        # self.tree.print_tree()
        node = self.tree.search(9)[0]
        self.tree.delete(node)
        # self.tree.print_tree()
        self.assertEqual(1, self.tree.get_root().height)
        self.assertEqual(8, self.tree.max_node().key, "Max node error")

    def test_case4a(self):
        # Right rotation, BF of left child is 1
        keys = [8, 7, 9, 6]
        for key in keys:
            self.tree.insert(key, str(key))
        # self.tree.print_tree()
        node = self.tree.search(9)[0]
        self.tree.delete(node)
        # self.tree.print_tree()
        self.assertEqual(1, self.tree.get_root().height)
        self.assertEqual(8, self.tree.max_node().key, "Max node error")

    def test_case4b(self):
        # Right rotation, BF of left child is 0
        keys = [9, 7, 10, 6, 8]
        for key in keys:
            self.tree.insert(key, str(key))
        # self.tree.print_tree()
        node = self.tree.search(10)[0]
        self.tree.delete(node)
        # self.tree.print_tree()
        self.assertEqual(2, self.tree.get_root().height)
        self.assertEqual(9, self.tree.max_node().key, "Max node error")

    def test_large(self):
        # Right rotation, BF of left child is 0
        keys = [15, 8, 22, 4, 11, 20, 24, 2, 9, 12, 18, 13]
        for key in keys:
            self.tree.insert(key, str(key))
        # self.tree.print_tree()
        node = self.tree.search(24)[0]
        self.tree.delete(node)
        # self.tree.print_tree()
        root = self.tree.get_root()
        self.assertEqual(11, root.key)
        self.assertEqual(3, self.tree.get_root().height)
        self.assertEqual(22, self.tree.max_node().key, "Max node error")

class JoinTest(unittest.TestCase):
    def setUp(self):
        self.tree1 = AVLTree()
        self.tree2 = AVLTree()

    def join_test_func(self, keys1: list[int], keys2: list[int], median_key: int):
        for key in keys1:
            self.tree1.insert(key, str(key))
        for key in keys2:
            self.tree2.insert(key, str(key))
        # self.tree1.print_tree()
        # self.tree2.print_tree()
        median_value = str(median_key)
        self.tree1.join(self.tree2, median_key, median_value)
        # self.tree1.print_tree()
        self.assertEqual(self.tree1.size(), len(keys1) + len(keys2) + 1)
        for key in keys1 + keys2 + [median_key]:
            node, _ = self.tree1.search(key)
            self.assertIsNotNone(node, f"Key {key} not found after join")
            self.assertEqual(key, node.key)
        expected_size = len(keys1) + len(keys2) + 1
        self.assertEqual(expected_size, self.tree1.size())

    def test_join(self):
        keys1 = list(range(10, 20))
        keys2 = list(range(1, 8))
        median_key = 9
        self.join_test_func(keys1, keys2, median_key)
        tree_height = self.tree1.get_root().height
        diff = self.tree1.get_root().height - tree_height
        self.assertLessEqual(diff, 1, "Tree height increased by more than 1 after join")
        self.assertGreaterEqual(diff, 0, "Tree height decreased after join")

    def test_join2(self):
        keys1 = [5, 6, 7]
        keys2 = [1, 2, 3]
        median_key = 4
        self.join_test_func(keys1, keys2, median_key)
        res = self.tree1.avl_to_array()
        keys = [k for k, v in res]
        expected_keys = [1, 2, 3, 4, 5, 6, 7]
        self.assertEqual(expected_keys, keys, "Keys order incorrect after join")

    def test_join3(self):
        keys1 = [1, 2, 3]
        keys2 = [5, 6, 7]
        median_key = 4
        self.join_test_func(keys1, keys2, median_key)
        res = self.tree1.avl_to_array()
        keys = [k for k, v in res]
        expected_keys = [1, 2, 3, 4, 5, 6, 7]
        self.assertEqual(expected_keys, keys, "Keys order incorrect after join")

    def test_join_empty_tree1(self):
        keys1 = []
        keys2 = [10, 20]
        median_key = 30
        self.join_test_func(keys1, keys2, median_key)
        tree_height = self.tree1.get_root().height
        self.assertEqual(1, tree_height, "Tree height incorrect after joining with empty tree")

    def test_join_empty_tree2(self):
        keys1 = [10, 20]
        keys2 = []
        median_key = 9
        self.join_test_func(keys1, keys2, median_key)
        tree_height = self.tree1.get_root().height
        self.assertEqual(1, tree_height, "Tree height incorrect after joining with empty tree")

class SplitTest(unittest.TestCase):
    def setUp(self):
        self.tree = AVLTree()
        keys = [20, 10, 30, 5, 15, 25, 35]
        for key in keys:
            self.tree.insert(key, str(key))

    def test_split1(self):
        split_key = 20
        # self.tree.print_tree()
        node, _ = self.tree.search(split_key)
        left_tree, right_tree = self.tree.split(node)
        # left_tree.print_tree()
        # right_tree.print_tree()
        left_keys = [10, 5, 15]
        right_keys = [30, 25, 35]
        for key in left_keys:
            node, _ = left_tree.search(key)
            self.assertIsNotNone(node)
            self.assertEqual(key, node.key)
        for key in right_keys:
            node, _ = right_tree.search(key)
            self.assertIsNotNone(node)
            self.assertEqual(key, node.key)

    def test_split2(self):
        split_key = 10
        # self.tree.print_tree()
        split_node = self.tree.search(split_key)[0]
        t1, t2 = self.tree.split(split_node)
        # t1.print_tree()
        # t2.print_tree()
        t1_arr = t1.avl_to_array()
        t_max = 0
        for key, _ in t1_arr:
            t_max = max(t_max, key)
        self.assertLess(t_max, split_key)
        t2_arr = t2.avl_to_array()
        t_max = 0
        for key, _ in t2_arr:
            t_max = max(t_max, key)
        self.assertGreater(t_max, split_key)

    def test_split3(self):
        split_key = 30
        # self.tree.print_tree()
        split_node = self.tree.search(split_key)[0]
        t1, t2 = self.tree.split(split_node)
        # t1.print_tree()
        # t2.print_tree()
        t1_arr = t1.avl_to_array()
        t_max = 0
        for key, _ in t1_arr:
            t_max = max(t_max, key)
        self.assertLess(t_max, split_key)
        t2_arr = t2.avl_to_array()
        t_max = 0
        for key, _ in t2_arr:
            t_max = max(t_max, key)
        self.assertGreater(t_max, split_key)

    def test_split_none(self):
        # self.tree.print_tree()
        t1, t2 = self.tree.split(None)
        # t1.print_tree()
        # t2.print_tree()
        self.assertIsNone(t1.get_root())
        self.assertIsNone(t2.get_root())

    def test_split_not_node(self):
        # self.tree.print_tree()
        t1, t2 = self.tree.split(20)  # Not a node
        # t1.print_tree()
        # t2.print_tree()
        self.assertIsNone(t1.get_root())
        self.assertIsNone(t2.get_root())

class AVLToArrayTest(unittest.TestCase):
    def setUp(self):
        self.tree = AVLTree()
        keys = [20, 10, 30, 5, 15, 25, 35]
        for key in keys:
            self.tree.insert(key, str(key))

    def test_avl_to_array(self):
        arr = self.tree.avl_to_array()
        keys = [k for k, v in arr]
        expected_keys = [5, 10, 15, 20, 25, 30, 35]
        self.assertEqual(expected_keys, keys)

    def test_large(self):
        tree = AVLTree()
        num_nodes = int(1e4)
        for i in range(num_nodes):
            tree.insert(i, str(i))
        self.assertEqual(tree.size(), num_nodes)
        tree.avl_to_array()  # Just to make sure it works

class MaxNodeTest(unittest.TestCase):
    def setUp(self):
        self.tree = AVLTree()

    def test_max_node_empty(self):
        self.assertIsNone(self.tree.max_node())

    def test_max_node_non_empty(self):
        keys = [20, 10, 30, 5, 15, 25, 35]
        for key in keys:
            self.tree.insert(key, str(key))
        max_node = self.tree.max_node()
        self.assertIsNotNone(max_node)
        self.assertEqual(35, max_node.key)

    def test_max_node_large(self):
        num_nodes = int(1e4)
        for i in range(num_nodes):
            self.tree.insert(i, str(i))
        max_node = self.tree.max_node()
        self.assertIsNotNone(max_node)
        self.assertEqual(num_nodes - 1, max_node.key)

class SizeTest(unittest.TestCase):
    def setUp(self):
        self.tree = AVLTree()

    def test_size_empty(self):
        self.assertEqual(0, self.tree.size())

    def test_size_non_empty(self):
        keys = [20, 10, 30, 5, 15, 25, 35]
        for i, key in enumerate(keys):
            self.tree.insert(key, str(key))
            self.assertEqual(i + 1, self.tree.size())

class GetRootTest(unittest.TestCase):
    def setUp(self):
        self.tree = AVLTree()

    def test_get_root_empty(self):
        self.assertIsNone(self.tree.get_root())

    def test_get_root_non_empty(self):
        keys = [20, 10, 30]
        for key in keys:
            self.tree.insert(key, str(key))
        root = self.tree.get_root()
        self.assertIsNotNone(root)
        self.assertEqual(20, root.key)


if __name__ == "__main__":
    print("Running Student Tester...\n")
    unittest.main()

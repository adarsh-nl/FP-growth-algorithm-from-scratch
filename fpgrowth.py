import numpy as np
import itertools
from collections import Counter

DEBUG = False

def debug(str):
  if DEBUG:
    print(str)

def load_data(data_path):
  """
  Loads transactional data from a file and returns it as a list of lists.

  Args:
  data_path: path to the file containing the transactional data

  Returns:
  A list of lists where each inner list represents a transaction.
  """
  Transactions = []
  
  with open (data_path, 'r') as data:
    for lines in data:
      str_line = list(lines.strip().split(','))
      Transactions.append(str_line)
  return Transactions

# Set the path to the file containing the transactional data
path = "/content/data.txt"
# Load the transactional data from the file
transactions = load_data(path)
# Remove empty items from the transactional data
transactions = [list(filter(lambda x: x != '', transaction)) for transaction in transactions]
# Print the first 100 transactions
print(transactions[:100])

def find_uniItems(transactions):
  """
  Finds the unique items in the transactional data.

  Args:
  transactions: a list of lists where each inner list represents a transaction

  Returns:
  A list of unique items in the transactional data.
  """
  unique_items = []
  for i in transactions:
    for j in i:
      if j not in unique_items:
        unique_items.append(j)
  return unique_items

# Find the unique items in the transactional data
unique_items = find_uniItems(transactions)
# Remove empty items from the unique items list
unique_items.remove('')
# Print the unique items in the transactional data
print("Unique_items in the transactional data are:\n{}".format(unique_items))

def find_frequency(lists):
    """
    Finds the frequency of each item in a list of lists.

    Args:
    lists: a list of lists

    Returns:
    A dictionary where the keys are the items in the input list and the values are their frequency.
    """
    result = {}
    for sub_list in lists:
        sub_list_counter = Counter(sub_list)
        for item, count in sub_list_counter.items():
            if item in result:
                result[item] += count
            else:
                result[item] = count
    return result

# Find the frequency of each item in the transactional data
frequent_item_sets = find_frequency(transactions)
# Print the frequency of each item
print(frequent_item_sets)

# Set the minimum support threshold to 40%
min_support = (40/100)*len(transactions)
# Print the minimum support of the dataset
print("The minimum support of the dataset is: {}".format(min_support))

def remove_infrequent_and_sort(frequent_item_sets, min_support):
  """
  Removes infrequent items and sorts the frequent item sets in decreasing order of frequency.

  Args:
  frequent_item_sets: a dictionary where the keys are the items and the values are their frequency.
  min_support: the minimum support threshold.

  Returns:
  A dictionary where the keys are the frequent item sets and the values are their frequency, sorted in decreasing order of frequency.
  """
  temp_itemset = frequent_item_sets.copy()
  for key,values in frequent_item_sets.items():
    if values < min_support:
      temp_itemset.pop(key)
    elif key == '':
      temp_itemset.pop(key)
    else:
      continue
      
  frequent_item_sets = temp_itemset
  keys = list(frequent_item_sets.keys())
  values = list(frequent_item_sets.values())
  sorted_value_index = np.argsort(values)
  sorted_value_index = np.flip
  sorted_value_index = np.flip(sorted_value_index)
  frequent_item_sets = {keys[i]: values[i] for i in sorted_value_index}
  return frequent_item_sets

frequent_item_sets = remove_infrequent_and_sort(frequent_item_sets, min_support)
print("The frequent item sets that satisfy the support count are: {}".format(frequent_item_sets))

def build_ordered_itemset(transactions, frequent_item_sets):
    """
    Returns a list of transactions where each transaction contains only frequent item sets, in the same order as they appear in the original transactions.

    Parameters:
    transactions (List): List of transactions
    frequent_item_sets (Dict): Dictionary of frequent item sets

    Returns:
    List: List of transactions with frequent item sets in the same order as they appear in the original transactions.
    """
    # Get a list of frequent item sets
    keys = list(frequent_item_sets.keys())
    
    # Create a new list of transactions containing only frequent item sets
    temp_transactions = []
    for transaction in transactions:
        temp_items = []
        for item in transaction:
            if item in keys:
                temp_items.append(item)
        temp_transactions.append(temp_items)
    
    # Rearrange the frequent item sets in each transaction to match the original order
    transactions = []
    for temp_transaction in temp_transactions:
        new_transaction = []
        for key in keys:
            if key in temp_transaction:
                new_transaction.append(key)
        transactions.append(new_transaction)
    
    return transactions


class Node:
    """
    A node in the FP tree.
    """
    def __init__(self, item, count, parent):
        """
        Creates a new node in the FP tree.

        Parameters:
        item (Any): The item associated with the node.
        count (int): The count of the item.
        parent (Node): The parent node.
        """
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {}
        self.next_node = None
        self.link = None

    def add_child(self, child):
        """
        Adds a child node to the current node.

        Parameters:
        child (Node): The child node to be added.
        """
        if child.item not in self.children:
            self.children[child.item] = child

    def increment_count(self, count):
        """
        Increments the count of the node.

        Parameters:
        count (int): The count to be added to the node's count.
        """
        self.count += count

    def get_nodes_with_item(self, item):
        """
        Returns a list of nodes with the given item.

        Parameters:
        item (Any): The item to search for.

        Returns:
        List: A list of nodes with the given item.
        """
        nodes = []
        if self.item == item:
            nodes.append(self)
        for child in self.children.values():
            nodes.extend(child.get_nodes_with_item(item))
        return nodes


class FPTree:
    """
    A class that represents an FP-Tree (Frequent Pattern Tree).

    Attributes:
    - root: a Node object that represents the root of the tree
    - header_table: a dictionary that stores the first occurrence of each item in the tree
    """
    def __init__(self):
        """
        Initializes an empty FP-Tree with a root node and an empty header table.
        """
        self.root = Node("*", 0, None)
        self.header_table = {}

    def add_transaction(self, transaction):
        """
        Adds a transaction to the FP-Tree.

        Parameters:
        - transaction: a list of items in the transaction

        Returns:
        - None
        """
        current_node = self.root
        for item in transaction:
            child_node = current_node.children.get(item)
            if child_node is None:
                child_node = Node(item, 0, current_node)
                current_node.children[item] = child_node
                if item in self.header_table:
                    last_node = self.header_table[item]
                    while last_node.link is not None:
                        last_node = last_node.link
                    last_node.link = child_node
                else:
                    self.header_table[item] = child_node
            child_node.increment_count(1)
            current_node = child_node

    def get_frequent_items(self, min_support):
        """
        Returns a dictionary that contains frequent items in the tree and their support counts.

        Parameters:
        - min_support: an integer that represents the minimum support count for an item to be considered frequent

        Returns:
        - a dictionary that maps frequent items to their support counts
        """
        frequent_items = {}
        for item in self.header_table:
            support = 0
            node = self.header_table[item]
            while node is not None:
                support += node.count
                node = node.link
            if support >= min_support:
                frequent_items[item] = support
        return frequent_items
    
    def get_nodes_with_item(self, item):
        """
        Returns a list of nodes in the tree that contain a specific item.

        Parameters:
        - item: a string that represents the item to search for

        Returns:
        - a list of Node objects that contain the item
        """
        return self.header_table.get(item, [])

def find_pattern_base(fptree, node, item):
    """
    Returns a pattern base for a given item in the FP-Tree.

    Parameters:
    - fptree: an FPTree object
    - node: a Node object in the FP-Tree
    - item: a string that represents the item to search for

    Returns:
    - a dictionary that maps a frozen set of prefix items to their support count
    """
    pattern_base = {}
    while node is not None:
        prefix_path = []
        temp_node = node
        while temp_node.parent is not None:
            if temp_node.name != "null" and temp_node.name != item:
                prefix_path.append(temp_node.name)
            temp_node = temp_node.parent
        if len(prefix_path) > 0:
            pattern_base[frozenset(prefix_path)] = node.count
        if node.link is None:
            break
        node = node.link
    return pattern_base

def create_subtree(fptree, min_support):
    """
    Given an FPTree and a minimum support threshold, creates a conditional FPTree.

    Args:
        fptree (FPTree): The FPTree to use as the basis for the conditional FPTree.
        min_support (int): The minimum support threshold to use for the conditional FPTree.

    Returns:
        FPTree: The conditional FPTree.
    """

    # Get the list of items in the FPTree's header table
    items = list(fptree.header_table.keys())

    # Prune the FPTree's header table to remove items that don't meet the minimum support threshold
    for item in items:
        # Calculate the support of the current item
        support = 0
        node = fptree.header_table[item]
        while node is not None:
            support += node.count
            node = node.link

        # If the support is less than the minimum support, remove the item from the header table
        if support < min_support:
            del fptree.header_table[item]
        # Otherwise, update the item's support in the header table to be the total support for that item
        else:
            fptree.header_table[item] = support

    # Convert the linked list of nodes for each item in the header table to a list
    for item in fptree.header_table:
        nodes = []
        node = fptree.header_table[item]
        while node is not None:
            nodes.append(node)
            node = node.link
        fptree.header_table[item] = nodes

    # Create the conditional FPTree by adding transactions for each item in the header table
    conditional_tree = FPTree()
    for item in items:
        # Find the pattern base for the current item
        pattern_base = find_pattern_base(fptree.root, item)

        # Add the transactions for the current item to the conditional FPTree
        for transaction, count in pattern_base.items():
            transaction_list = list(transaction)
            for i in range(count):
                conditional_tree.add_transaction(transaction_list)

    # Get the frequent items in the conditional FPTree
    frequent_items = conditional_tree.get_frequent_items(min_support)

    # Update the header table of the conditional FPTree with the frequent items
    for item in frequent_items:
        conditional_tree.header_table[item] = frequent_items[item]

    # Return the conditional FPTree
    return conditional_tree

 def generate_frequent_patterns(fptree, min_support, prefix=[]):
    """
    Generates all frequent itemsets from an FP-tree recursively.

    Args:
        fptree (FPTree): The FP-tree to mine frequent itemsets from.
        min_support (int): The minimum support count threshold.
        prefix (list, optional): A prefix path of items leading to the current node.
            Defaults to an empty list.

    Yields:
        tuple: A tuple (itemset, support) representing a frequent itemset and its support count.
            The itemset is a frozenset of items and the support count is an integer.

    """
    # sort items in descending order of support count
    items = [v[0] for v in sorted(fptree.items(), key=lambda kv: kv[1]['support'])]
    for item in items:
        # create a new prefix path with the current item
        new_prefix = prefix.copy()
        new_prefix.append(item)
        # yield the itemset and its support count
        support = fptree[item]["support"]
        yield (frozenset(new_prefix), support)
        # recursively generate frequent itemsets for the conditional FP-tree
        conditional_pattern_base = find_pattern_base(fptree[item]["node_link"], item)
        conditional_tree = create_subtree(conditional_pattern_base, min_support)
        if len(conditional_tree) > 0:
            for pattern in generate_frequent_patterns(conditional_tree, min_support, new_prefix):
                yield pattern
                
class FP_Growth:
    """
    A class for mining frequent itemsets using the FP-Growth algorithm.
    """

    def __init__(self, transactions, min_support):
        """
        Initialize the FP-Growth object.

        Args:
        transactions (list): A list of transactions, where each transaction is a list of items.
        min_support (int): The minimum support threshold.

        Returns:
        None
        """
        self.transactions = transactions
        self.min_support = min_support

    def build_fptree(self):
        """
        Builds the FPTree for the given transactions.

        Args:
        None

        Returns:
        None
        """
        self.fptree = FPTree()
        for transaction in self.transactions:
            self.fptree.add_transaction(transaction)

    def generate_frequent_itemsets(self, node, suffix):
        """
        Generates frequent itemsets for the given node in the FPTree.

        Args:
        node (FPTreeNode): The node to generate frequent itemsets for.
        suffix (set): The suffix to add to the frequent itemsets.

        Returns:
        list: A list of frequent itemsets and their corresponding support.
        """
        frequent_itemsets = []
        support = node.count
        for item, child_node in node.children.items():
            itemset = suffix.copy()
            itemset.add(item)
            frequent_itemsets.append((itemset, support))
            frequent_itemsets.extend(self.generate_frequent_itemsets(child_node, itemset))
        return frequent_itemsets

    def mine_frequent_itemsets(self):
        """
        Mines frequent itemsets using the FP-Growth algorithm.

        Args:
        None

        Returns:
        list: A list of frequent itemsets and their corresponding support.
        """
        self.build_fptree()
        frequent_itemsets = []
        for item, count in self.fptree.get_frequent_items(self.min_support).items():
            frequent_itemsets.append((frozenset([item]), count))
        for itemset in itertools.chain.from_iterable(
                self.generate_frequent_itemsets(self.fptree.header_table[item], set()) for item in self.fptree.header_table):
            frequent_itemsets.append(itemset)
        return frequent_itemsets

fp = FP_Growth(transactions, min_support)
frequent_itemsets = fp.mine_frequent_itemsets()
#print(frequent_itemsets)
for i in range(len(frequent_itemsets)):
  print("{}\n".format(frequent_itemsets[i]))

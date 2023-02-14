# FP-growth-algorithm-from-scratch


The code is an implementation of the FP-Growth algorithm for frequent itemset mining in transactional datasets.

It starts by loading transactional data from a file and then finds the unique items present in the dataset. Then, it calculates the frequency of each item in the dataset and removes infrequent items based on a minimum support threshold. It also sorts the remaining frequent items in decreasing order of their frequency.

Next, it constructs an ordered itemset from the frequent items and the original transactions. Then, it constructs an FP-Tree from the ordered itemset and finds all frequent itemsets in the dataset.

The code also has several helper functions to add transactions to the FP-Tree, find frequent items and their support, and create a subtree of the FP-Tree for a given item. Overall, the code performs the steps of the FP-Growth algorithm to efficiently mine frequent itemsets in transactional datasets.

# Sample output:

({'Butter', 'Bread', 'Sugar', 'Cheese'}, 37)
({'Butter', 'Panner', 'Cheese', 'Bread', 'Sugar'}, 19)
({'Butter', 'Panner', 'Cheese', 'Bread', 'Sugar', 'Tea Powder'}, 11)
({'Butter', 'Panner', 'Cheese', 'Bread', 'Sugar', 'Lassi'}, 11)
({'Butter', 'Panner', 'Cheese', 'Bread', 'Sugar', 'Lassi', 'Tea Powder'}, 4)
({'Butter', 'Tea Powder', 'Cheese', 'Bread', 'Sugar'}, 19)

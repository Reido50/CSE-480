'''
Write a function, named check_funtional_dependency, that takes two arguments, 
a table (represented as a list of dictionaries, where each dictionary’s key is 
a column and its value is the datum) and a functional dependency (a class already 
implemented in the starter code). Your function should return True if the 
functional dependency is true for the table, False otherwise.
'''

import itertools

class FunctionalDependency:
    def __init__(self, left_attributes_set, right_attributes_set):
        self.left_attributes_set = left_attributes_set
        self.right_attributes_set = right_attributes_set

    def __str__(self):
        return f"FunctionalDependency({self.left_attributes_set}, {self.right_attributes_set})"
    __repr__ = __str__
    
def check_funtional_dependency(list_of_dict_rows, functional_dependency):
    checker_dict = {}
    for row in list_of_dict_rows:
    	left = []
    	right = []
    	for attrib, value in row.items():
    		if attrib in functional_dependency.left_attributes_set:
    			left.append(value)
    		if attrib in functional_dependency.right_attributes_set:
    			right.append(value)
    	left = tuple(left)
    	right = tuple(right)
    	if checker_dict.get(left) == None:
    		checker_dict[left] = right
    	else:
    		if checker_dict[left] != right:
    			return False
    return True

list_of_dict_rows = [
        {"name": "Josh", "age": 29, "pet": "RaceTrack", "allergies": "Wheat"},
        {"name": "Cam", "age": 26, "pet": "CrashDown", "allergies": "None"},
        {"name": "Zizhen", "age": 24, "pet": "Bugs Bunny", "allergies": "Calculus"},
        {"name": "Dennis", "age": 40, "pet": "Dany", "allergies": "Wheat"},
        {"name": "Jie", "age": 24, "pet": "Ghost", "allergies": "None"},
    ]
# This table has 4 columns: name, age, pet, and allergies
left_side_set = {"age", "allergies"}
right_side_set = {"name", "age"}
functional_dependency = FunctionalDependency(left_side_set, right_side_set)
print(check_funtional_dependency(list_of_dict_rows, functional_dependency))


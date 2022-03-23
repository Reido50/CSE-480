'''
Write a function, named “is_key” that takes three arguments: a set of all the attributes in a 
relation, a list of functional dependences (see previous question), and a proposed attribute 
set which may be a key for the relation. Your function should return True only if the proposed
attribute set is a key for the relation (not just a super key).
'''

import itertools

class FunctionalDependency:
    def __init__(self, left_attributes_set, right_attributes_set):
        self.left_attributes_set = left_attributes_set
        self.right_attributes_set = right_attributes_set

    def __str__(self):
        return f"FunctionalDependency({self.left_attributes_set}, {self.right_attributes_set})"
    __repr__ = __str__

def populate_closure(list_of_fds, attribute_set):
    closure = attribute_set

    # Populate closure until it doesn't change
    next_closure = closure
    while True:
        for fd in list_of_fds:
            if fd.left_attributes_set in next_closure:
                next_closure.append(fd.right_attributes_set)
        if next_closure == closure:
            break
        closure = next_closure

    return closure

def is_key(all_attributes, list_of_fds, attribute_set):
    closure = populate_closure(list_of_fds, attribute_set)
    # Is it not a superkey?
    if closure != all_attributes:
        return False
    # Is it not the key?
    for L in range(0, len(attribute_set) + 1):
        for perm in itertools.permutations(attribute_set, L):
            perm_closure = populate_closure(list_of_fds, perm)
            if perm_closure == all_attributes:
                return False
    # It must be the key
    return True

all_attributes = {"username", "first_name", "last_name", "id"}
list_of_fds = [
    FunctionalDependency({"username"}, {"first_name", "last_name"}),
    FunctionalDependency({"last_name"}, {"id"}),
]
attribute_set = {"username"}
print(is_key(all_attributes, list_of_fds, attribute_set))

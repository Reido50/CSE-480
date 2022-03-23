import sqlite3
import unittest
from pprint import pprint
import sys
import os
sys.path.append("/home/codio/workspace/student_code/")
from is_key import FunctionalDependency,is_key

class TestIsKey(unittest.TestCase):
  def test_visible_1(self):
    # Last Multiple Choice Question

    all_attributes = {"username", "first_name", "last_name", "id"}
    list_of_fds = [
        FunctionalDependency({"username"}, {"first_name", "last_name"}),
        FunctionalDependency({"last_name"}, {"id"}),
    ]
    attribute_set = {"username"}

    print(f"All attributes: {all_attributes}")
    print("FDs:")
    pprint(list_of_fds)
    print(f"Attribute Set: {attribute_set}")

    result = is_key(all_attributes, list_of_fds, attribute_set)
    print(f"Result: {result}")
    assert result

  def test_visible_2(self):
    # Not Even A Super Key
    all_attributes = {"username", "first_name", "last_name", "id"}
    list_of_fds = [
        FunctionalDependency({"username"}, {"first_name", "last_name"}),
        FunctionalDependency({"last_name"}, {"id"}),
    ]
    attribute_set = {"first_name", "last_name"}

    print(f"All attributes: {all_attributes}")
    print("FDs:")
    pprint(list_of_fds)
    print(f"Attribute Set: {attribute_set}")

    result = is_key(all_attributes, list_of_fds, attribute_set)
    print(f"Result: {result}")
    assert not result
    
  def test_visible_3(self):
    # A Super Key, but not a key
    all_attributes = {"username", "first_name", "last_name", "id"}
    list_of_fds = [
        FunctionalDependency({"username"}, {"first_name", "last_name"}),
        FunctionalDependency({"last_name"}, {"id"}),
    ]
    attribute_set = {"username", "last_name"}

    print(f"All attributes: {all_attributes}")
    print("FDs:")
    pprint(list_of_fds)
    print(f"Attribute Set: {attribute_set}")

    result = is_key(all_attributes, list_of_fds, attribute_set)
    print(f"Result: {result}")
    assert not result

  def test_visible_4(self):
    # Not all attributes must be in FDs
    pass

  def test_visible_5(self):
    # Make sure to check against All Attributes
    all_attributes = {"username", "first_name", "last_name", "id", "zipcode", "city", "age"}
    list_of_fds = [
        FunctionalDependency({"username"}, {"first_name", "last_name"}),
        FunctionalDependency({"last_name"}, {"id"}),
        FunctionalDependency({"zipcode"}, {"city"}),
    ]
    attribute_set = {"username", "zipcode", "age", "city"}

    print(f"All attributes: {all_attributes}")
    print("FDs:")
    pprint(list_of_fds)
    print(f"Attribute Set: {attribute_set}")

    result = is_key(all_attributes, list_of_fds, attribute_set)
    print(f"Result: {result}")
    assert not result

  def test_visible_6(self):
    # Late Addition
    all_attributes = {"A", "B", "C", "D", "E", "F", "G"}
    list_of_fds = [
        FunctionalDependency({"A", "B"}, {"C"}),
        FunctionalDependency({"A", "C"}, {"B"}),
        FunctionalDependency({"C", "B"}, {"A"}),
    ]
    attribute_set = {"A"}
    print(f"All attributes: {all_attributes}")
    print("FDs:")
    pprint(list_of_fds)
    print(f"Attribute Set: {attribute_set}")

    result = is_key(all_attributes, list_of_fds, attribute_set)
    print(f"Result: {result}")
    assert not result

  def test_visible_7(self):
    # Another
    all_attributes = {"username", "first_name", "last_name", "id", "zipcode", "city", "age", "rating"}
    list_of_fds = [
        FunctionalDependency({"username"}, {"first_name", "last_name"}),
        FunctionalDependency({"last_name", "first_name"}, {"id"}),
        FunctionalDependency({"rating"}, {"city"}),
        FunctionalDependency({"zipcode"}, {"city"}),
    ]
    attribute_set = {"username", "zipcode", "age", "zipcode", "rating"}

    print(f"All attributes: {all_attributes}")
    print("FDs:")
    pprint(list_of_fds)
    print(f"Attribute Set: {attribute_set}")

    result = is_key(all_attributes, list_of_fds, attribute_set)
    print(f"Result: {result}")
    assert result

    attribute_set = {"username", "zipcode", "age", "zipcode", "rating", "city"}

    print(f"All attributes: {all_attributes}")
    print("FDs:")
    pprint(list_of_fds)
    print(f"Attribute Set: {attribute_set}")

    result = is_key(all_attributes, list_of_fds, attribute_set)
    print(f"Result: {result}")
    assert not result

    attribute_set = {"username", "zipcode", "age", "zipcode"}

    print(f"All attributes: {all_attributes}")
    print("FDs:")
    pprint(list_of_fds)
    print(f"Attribute Set: {attribute_set}")

    result = is_key(all_attributes, list_of_fds, attribute_set)
    print(f"Result: {result}")
    assert not result

  def test_hidden_1(self):
    all_attributes = {"username", "first_name", "last_name", "id", "zipcode", "city", "age", "rating"}
    list_of_fds = [
        FunctionalDependency({"username"}, {"first_name", "last_name"}),
        FunctionalDependency({"last_name"}, {"id"}),
        FunctionalDependency({"rating"}, {"city"}),
        FunctionalDependency({"zipcode"}, {"city"}),
    ]
    attribute_set = {"username", "zipcode", "age", "zipcode", "rating"}

    print(f"All attributes: {all_attributes}")
    print("FDs:")
    pprint(list_of_fds)
    print(f"Attribute Set: {attribute_set}")

    result = is_key(all_attributes, list_of_fds, attribute_set)
    print(f"Result: {result}")
    assert result

    attribute_set = {"username", "zipcode", "age", "zipcode", "rating", "city"}

    print(f"All attributes: {all_attributes}")
    print("FDs:")
    pprint(list_of_fds)
    print(f"Attribute Set: {attribute_set}")

    result = is_key(all_attributes, list_of_fds, attribute_set)
    print(f"Result: {result}")
    assert not result

    attribute_set = {"username", "zipcode", "age", "zipcode"}

    print(f"All attributes: {all_attributes}")
    print("FDs:")
    pprint(list_of_fds)
    print(f"Attribute Set: {attribute_set}")

    result = is_key(all_attributes, list_of_fds, attribute_set)
    print(f"Result: {result}")
    assert not result

if __name__ == '__main__':
    unittest.main()
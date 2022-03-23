import sqlite3
import unittest
from pprint import pprint
import sys
import os
sys.path.append("/home/codio/workspace/student_code/")
from functional_dependency import check_funtional_dependency, FunctionalDependency

class TestFunctionalDependency(unittest.TestCase):
  def test_visible_1(self):
    # First Test Case (Okay)
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
    # age allergies ---> name age
    # it holds because no rows matching on the left attributes disagree on the right

    print("Table:")
    pprint(list_of_dict_rows)
    print(f"FD: {functional_dependency}")

    result = check_funtional_dependency(list_of_dict_rows, functional_dependency)
    print(f"Result: {result}")

    assert result

  def test_visible_2(self):
    # Doesn't Hold
    list_of_dict_rows = [
        {"name": "Josh", "age": 29, "pet": "RaceTrack", "allergies": "Wheat"},
        {"name": "Cam", "age": 26, "pet": "CrashDown", "allergies": "None"},
        {"name": "Zizhen", "age": 24, "pet": "Bugs Bunny", "allergies": "Calculus"},
        {"name": "Dennis", "age": 40, "pet": "Dany", "allergies": "Wheat"},
        {"name": "Jie", "age": 24, "pet": "Ghost", "allergies": "None"},
    ]

    left_side_set = {"allergies"}
    right_side_set = {"name", "age"}
    functional_dependency = FunctionalDependency(left_side_set, right_side_set)

    print("Table:")
    pprint(list_of_dict_rows)
    print(f"FD: {functional_dependency}")

    result = check_funtional_dependency(list_of_dict_rows, functional_dependency)
    print(f"Result: {result}")
    # FD doesn't hold because Josh and Dennis both have a wheat allergy, but differ in name (and age too)
    assert not result

  def test_visible_3(self):
    # Other Columns
    list_of_dict_rows = [
        {"name": "Josh", "age": 29, "pet": "RaceTrack", "allergies": "Wheat", "zipcode": 98105},
        {"name": "Cam", "age": 26, "pet": "CrashDown", "allergies": "None", "zipcode": 48824},
        {"name": "Zizhen", "age": 24, "pet": "Bugs Bunny", "allergies": "Calculus", "zipcode": 48823},
        {"name": "Dennis", "age": 40, "pet": "Dany", "allergies": "Wheat", "zipcode": 48823},
        {"name": "Jie", "age": 24, "pet": "Ghost", "allergies": "None", "zipcode": 48823},
    ]

    left_side_set = {"zipcode", "allergies"}
    right_side_set = {"name", "age"}
    functional_dependency = FunctionalDependency(left_side_set, right_side_set)

    print("Table:")
    pprint(list_of_dict_rows)
    print(f"FD: {functional_dependency}")

    result = check_funtional_dependency(list_of_dict_rows, functional_dependency)
    print(f"Result: {result}")

    assert result

    left_side_set = {"zipcode"}
    right_side_set = {"zipcode"}
    functional_dependency = FunctionalDependency(left_side_set, right_side_set)

    print("Table:")
    pprint(list_of_dict_rows)
    print(f"FD: {functional_dependency}")

    result = check_funtional_dependency(list_of_dict_rows, functional_dependency)
    print(f"Result: {result}")

    assert result

  def test_visible_4(self):
    # Another Test Case
    list_of_dict_rows = [
        {"name":"Elaine", "age":86, "health":"Fair", "city": "LA"},
        {"name":"Albert", "age":83, "health":"Poor", "city": "LA"},
        {"name":"Josh", "age":30, "health":"Moderate", "city": "East Lansing"},
        {"name":"Rick", "age":30, "health":"Moderate", "city": "Seattle"},
        {"name":"Emily", "age":26, "health":"Excellent", "city": "East Lansing"},
        {"name":"Alex", "age":30, "health":"Excellent", "city": "Brighton"},
        {"name":"Alexa", "age":31, "health":"Excellent", "city": "Brighton"},
        {"name":"Jose", "age":35, "health":"Excellent", "city": "Brighton"},
    ]

    left_side_set = {"city", "age", "health"}
    right_side_set = {"name"}
    functional_dependency = FunctionalDependency(left_side_set, right_side_set)

    print("Table:")
    pprint(list_of_dict_rows)
    print(f"FD: {functional_dependency}")

    result = check_funtional_dependency(list_of_dict_rows, functional_dependency)
    print(f"Result: {result}")

    assert result

    left_side_set = {"city", "age", "health"}
    right_side_set = {"city"}
    functional_dependency = FunctionalDependency(left_side_set, right_side_set)

    print("Table:")
    pprint(list_of_dict_rows)
    print(f"FD: {functional_dependency}")

    result = check_funtional_dependency(list_of_dict_rows, functional_dependency)
    print(f"Result: {result}")

    assert result


    left_side_set = {"name"}
    right_side_set = {"age", "health", "city"}
    functional_dependency = FunctionalDependency(left_side_set, right_side_set)

    print("Table:")
    pprint(list_of_dict_rows)
    print(f"FD: {functional_dependency}")

    result = check_funtional_dependency(list_of_dict_rows, functional_dependency)
    print(f"Result: {result}")

    assert result


    left_side_set = {"age", "health"}
    right_side_set = {"city"}
    functional_dependency = FunctionalDependency(left_side_set, right_side_set)

    print("Table:")
    pprint(list_of_dict_rows)
    print(f"FD: {functional_dependency}")

    result = check_funtional_dependency(list_of_dict_rows, functional_dependency)
    print(f"Result: {result}")

    assert not result

  def test_hidden_1(self):
    # Hidden
    list_of_dict_rows = [
        {"name":"Elaine", "age":86, "health":"Fair", "city": "LA"},
        {"name":"Albert", "age":83, "health":"Poor", "city": "LA"},
        {"name":"Josh", "age":30, "health":"Moderate", "city": "East Lansing"},
        {"name":"Rick", "age":30, "health":"Moderate", "city": "Seattle"},
        {"name":"Emily", "age":26, "health":"Excellent", "city": "East Lansing"},
        {"name":"Alex", "age":30, "health":"Excellent", "city": "Brighton"},
        {"name":"Alexa", "age":31, "health":"Excellent", "city": "Brighton"},
    ]

    left_side_set = {"city", "age", "health"}
    right_side_set = {"name"}
    functional_dependency = FunctionalDependency(left_side_set, right_side_set)

    print("Table:")
    pprint(list_of_dict_rows)
    print(f"FD: {functional_dependency}")

    result = check_funtional_dependency(list_of_dict_rows, functional_dependency)
    print(f"Result: {result}")

    assert result

    left_side_set = {"city", "age", "health"}
    right_side_set = {"city"}
    functional_dependency = FunctionalDependency(left_side_set, right_side_set)

    print("Table:")
    pprint(list_of_dict_rows)
    print(f"FD: {functional_dependency}")

    result = check_funtional_dependency(list_of_dict_rows, functional_dependency)
    print(f"Result: {result}")

    assert result


    left_side_set = {"name"}
    right_side_set = {"age", "health", "city"}
    functional_dependency = FunctionalDependency(left_side_set, right_side_set)

    print("Table:")
    pprint(list_of_dict_rows)
    print(f"FD: {functional_dependency}")

    result = check_funtional_dependency(list_of_dict_rows, functional_dependency)
    print(f"Result: {result}")

    assert result


    left_side_set = {"age", "health"}
    right_side_set = {"city"}
    functional_dependency = FunctionalDependency(left_side_set, right_side_set)

    print("Table:")
    pprint(list_of_dict_rows)
    print(f"FD: {functional_dependency}")

    result = check_funtional_dependency(list_of_dict_rows, functional_dependency)
    print(f"Result: {result}")

    assert not result

if __name__ == '__main__':
    unittest.main()
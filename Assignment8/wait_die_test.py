import unittest
from pprint import pprint
import sys
import os
sys.path.append("/home/codio/workspace/student_code/")

from wait_die_scheduler import wait_die_scheduler, Action

class TestWaitDieScheduler(unittest.TestCase):
  def test_visible_1(self):
    actions = [
      Action(object_="A", transaction="pear", type_="WRITE"),
      Action(object_="NA", transaction="pear", type_="COMMIT"),
      ]

    expected = [Action('A', 'pear', 'LOCK'),
    Action('A', 'pear', 'WRITE'),
    Action('NA', 'pear', 'COMMIT'),
    Action('A', 'pear', 'UNLOCK')]

    print("Actions = ")
    pprint(actions)

    print("Expected = ")
    pprint(expected)

    result = wait_die_scheduler(actions)
    print("Result = ")
    pprint(result)

    assert result == expected

    """

    Doing one action for each transaction:

    Adding Action('A', 'pear', 'WRITE') to its transaction

    Doing one action for each transaction:
    Trying to do pear
      Doing LOCK Action('A', 'pear', 'LOCK')
      Doing WRITE Action('A', 'pear', 'WRITE')

    Adding Action('NA', 'pear', 'COMMIT') to its transaction

    Doing one action for each transaction:
    Trying to do pear
      Doing COMMIT Action('NA', 'pear', 'COMMIT')
      Doing UNLOCK Action('A', 'pear', 'UNLOCK')

    Doing one action for each transaction:
    Trying to do pear
    """
  
  def test_visible_2(self):
    actions = [
      Action(object_="A", transaction="pear", type_="WRITE"),
      Action(object_="B", transaction="apple", type_="WRITE"),
      Action(object_="B", transaction="pear", type_="WRITE"),
      Action(object_="A", transaction="apple", type_="WRITE"),
      Action(object_="NA", transaction="apple", type_="COMMIT"),
      Action(object_="NA", transaction="pear", type_="COMMIT"),
      ]

    expected = [Action('A', 'pear', 'LOCK'),
    Action('A', 'pear', 'WRITE'),
    Action('B', 'apple', 'LOCK'),
    Action('B', 'apple', 'WRITE'),
    Action('NA', 'pear', 'WAIT'),
    Action('NA', 'apple', 'ROLLBACK'),
    Action('B', 'apple', 'UNLOCK'),
    Action('B', 'pear', 'LOCK'),
    Action('B', 'pear', 'WRITE'),
    Action('NA', 'apple', 'ROLLBACK'),
    Action('NA', 'apple', 'ROLLBACK'),
    Action('NA', 'pear', 'COMMIT'),
    Action('A', 'pear', 'UNLOCK'),
    Action('B', 'pear', 'UNLOCK'),
    Action('B', 'apple', 'LOCK'),
    Action('B', 'apple', 'WRITE'),
    Action('A', 'apple', 'LOCK'),
    Action('A', 'apple', 'WRITE'),
    Action('NA', 'apple', 'COMMIT'),
    Action('A', 'apple', 'UNLOCK'),
    Action('B', 'apple', 'UNLOCK')]

    print("Actions = ")
    pprint(actions)

    print("Expected = ")
    pprint(expected)

    result = wait_die_scheduler(actions)
    print("Result = ")
    pprint(result)

    assert expected == result

    """
    Doing one action for each transaction:

    Adding Action('A', 'pear', 'WRITE') to its transaction

    Doing one action for each transaction:
    Trying to do pear
      Doing LOCK Action('A', 'pear', 'LOCK')
      Doing WRITE Action('A', 'pear', 'WRITE')

    Adding Action('B', 'apple', 'WRITE') to its transaction

    Doing one action for each transaction:
    Trying to do apple
      Doing LOCK Action('B', 'apple', 'LOCK')
      Doing WRITE Action('B', 'apple', 'WRITE')
    Trying to do pear

    Adding Action('B', 'pear', 'WRITE') to its transaction

    Doing one action for each transaction:
    Trying to do apple
    Trying to do pear
      Doing WAIT (Transaction([Action('A', 'pear', 'WRITE'), Action('B', 'pear', 'WRITE')], 0, 1) is older)

    Adding Action('A', 'apple', 'WRITE') to its transaction

    Doing one action for each transaction:
    Trying to do apple
      Doing ROLLBACK (Transaction([Action('B', 'apple', 'WRITE'), Action('A', 'apple', 'WRITE')], 1, 1) is younger)
      Doing UNLOCK Action('B', 'apple', 'UNLOCK')
    Trying to do pear
      Doing LOCK Action('B', 'pear', 'LOCK')
      Doing WRITE Action('B', 'pear', 'WRITE')

    Adding Action('NA', 'apple', 'COMMIT') to its transaction

    Doing one action for each transaction:
    Trying to do apple
      Doing ROLLBACK (Transaction([Action('B', 'apple', 'WRITE'), Action('A', 'apple', 'WRITE'), Action('NA', 'apple', 'COMMIT')], 1, 0) is younger)
    Trying to do pear

    Adding Action('NA', 'pear', 'COMMIT') to its transaction

    Doing one action for each transaction:
    Trying to do apple
      Doing ROLLBACK (Transaction([Action('B', 'apple', 'WRITE'), Action('A', 'apple', 'WRITE'), Action('NA', 'apple', 'COMMIT')], 1, 0) is younger)
    Trying to do pear
      Doing COMMIT Action('NA', 'pear', 'COMMIT')
      Doing UNLOCK Action('A', 'pear', 'UNLOCK')
      Doing UNLOCK Action('B', 'pear', 'UNLOCK')

    Doing one action for each transaction:
    Trying to do apple
      Doing LOCK Action('B', 'apple', 'LOCK')
      Doing WRITE Action('B', 'apple', 'WRITE')
    Trying to do pear

    Doing one action for each transaction:
    Trying to do apple
      Doing LOCK Action('A', 'apple', 'LOCK')
      Doing WRITE Action('A', 'apple', 'WRITE')
    Trying to do pear

    Doing one action for each transaction:
    Trying to do apple
      Doing COMMIT Action('NA', 'apple', 'COMMIT')
      Doing UNLOCK Action('A', 'apple', 'UNLOCK')
      Doing UNLOCK Action('B', 'apple', 'UNLOCK')
    Trying to do pear

    Doing one action for each transaction:
    Trying to do apple
    Trying to do pear
    """

  def test_visible_3(self):
    # Three Transactions
    actions = [
      Action(object_="A", transaction="pear", type_="WRITE"),
      Action(object_="B", transaction="apple", type_="WRITE"),
      Action(object_="C", transaction="carrot", type_="WRITE"),
      Action(object_="B", transaction="pear", type_="WRITE"),
      Action(object_="A", transaction="apple", type_="WRITE"),
      Action(object_="NA", transaction="apple", type_="COMMIT"),
      Action(object_="B", transaction="carrot", type_="WRITE"),
      Action(object_="NA", transaction="pear", type_="COMMIT"),
      Action(object_="NA", transaction="carrot", type_="COMMIT"),
      ]

    expected = [Action('A', 'pear', 'LOCK'),
    Action('A', 'pear', 'WRITE'),
    Action('B', 'apple', 'LOCK'),
    Action('B', 'apple', 'WRITE'),
    Action('C', 'carrot', 'LOCK'),
    Action('C', 'carrot', 'WRITE'),
    Action('NA', 'pear', 'WAIT'),
    Action('NA', 'apple', 'ROLLBACK'),
    Action('B', 'apple', 'UNLOCK'),
    Action('B', 'pear', 'LOCK'),
    Action('B', 'pear', 'WRITE'),
    Action('NA', 'apple', 'ROLLBACK'),
    Action('NA', 'apple', 'ROLLBACK'),
    Action('NA', 'carrot', 'ROLLBACK'),
    Action('C', 'carrot', 'UNLOCK'),
    Action('NA', 'apple', 'ROLLBACK'),
    Action('C', 'carrot', 'LOCK'),
    Action('C', 'carrot', 'WRITE'),
    Action('NA', 'pear', 'COMMIT'),
    Action('A', 'pear', 'UNLOCK'),
    Action('B', 'pear', 'UNLOCK'),
    Action('B', 'apple', 'LOCK'),
    Action('B', 'apple', 'WRITE'),
    Action('NA', 'carrot', 'ROLLBACK'),
    Action('C', 'carrot', 'UNLOCK'),
    Action('A', 'apple', 'LOCK'),
    Action('A', 'apple', 'WRITE'),
    Action('C', 'carrot', 'LOCK'),
    Action('C', 'carrot', 'WRITE'),
    Action('NA', 'apple', 'COMMIT'),
    Action('A', 'apple', 'UNLOCK'),
    Action('B', 'apple', 'UNLOCK'),
    Action('B', 'carrot', 'LOCK'),
    Action('B', 'carrot', 'WRITE'),
    Action('NA', 'carrot', 'COMMIT'),
    Action('B', 'carrot', 'UNLOCK'),
    Action('C', 'carrot', 'UNLOCK')]

    print("Actions = ")
    pprint(actions)

    print("Expected = ")
    pprint(expected)

    result = wait_die_scheduler(actions)
    print("Result = ")
    pprint(result)


    assert expected == result

    """
    Doing one action for each transaction:

    Adding Action('A', 'pear', 'WRITE') to its transaction

    Doing one action for each transaction:
    Trying to do pear
      Doing LOCK Action('A', 'pear', 'LOCK')
      Doing WRITE Action('A', 'pear', 'WRITE')

    Adding Action('B', 'apple', 'WRITE') to its transaction

    Doing one action for each transaction:
    Trying to do apple
      Doing LOCK Action('B', 'apple', 'LOCK')
      Doing WRITE Action('B', 'apple', 'WRITE')
    Trying to do pear

    Adding Action('C', 'carrot', 'WRITE') to its transaction

    Doing one action for each transaction:
    Trying to do apple
    Trying to do carrot
      Doing LOCK Action('C', 'carrot', 'LOCK')
      Doing WRITE Action('C', 'carrot', 'WRITE')
    Trying to do pear

    Adding Action('B', 'pear', 'WRITE') to its transaction

    Doing one action for each transaction:
    Trying to do apple
    Trying to do carrot
    Trying to do pear
      Doing WAIT (Transaction([Action('A', 'pear', 'WRITE'), Action('B', 'pear', 'WRITE')], 0, 1) is older)

    Adding Action('A', 'apple', 'WRITE') to its transaction

    Doing one action for each transaction:
    Trying to do apple
      Doing ROLLBACK (Transaction([Action('B', 'apple', 'WRITE'), Action('A', 'apple', 'WRITE')], 1, 1) is younger)
      Doing UNLOCK Action('B', 'apple', 'UNLOCK')
    Trying to do carrot
    Trying to do pear
      Doing LOCK Action('B', 'pear', 'LOCK')
      Doing WRITE Action('B', 'pear', 'WRITE')

    Adding Action('NA', 'apple', 'COMMIT') to its transaction

    Doing one action for each transaction:
    Trying to do apple
      Doing ROLLBACK (Transaction([Action('B', 'apple', 'WRITE'), Action('A', 'apple', 'WRITE'), Action('NA', 'apple', 'COMMIT')], 1, 0) is younger)
    Trying to do carrot
    Trying to do pear

    Adding Action('B', 'carrot', 'WRITE') to its transaction

    Doing one action for each transaction:
    Trying to do apple
      Doing ROLLBACK (Transaction([Action('B', 'apple', 'WRITE'), Action('A', 'apple', 'WRITE'), Action('NA', 'apple', 'COMMIT')], 1, 0) is younger)
    Trying to do carrot
      Doing ROLLBACK (Transaction([Action('C', 'carrot', 'WRITE'), Action('B', 'carrot', 'WRITE')], 2, 1) is younger)
      Doing UNLOCK Action('C', 'carrot', 'UNLOCK')
    Trying to do pear

    Adding Action('NA', 'pear', 'COMMIT') to its transaction

    Doing one action for each transaction:
    Trying to do apple
      Doing ROLLBACK (Transaction([Action('B', 'apple', 'WRITE'), Action('A', 'apple', 'WRITE'), Action('NA', 'apple', 'COMMIT')], 1, 0) is younger)
    Trying to do carrot
      Doing LOCK Action('C', 'carrot', 'LOCK')
      Doing WRITE Action('C', 'carrot', 'WRITE')
    Trying to do pear
      Doing COMMIT Action('NA', 'pear', 'COMMIT')
      Doing UNLOCK Action('A', 'pear', 'UNLOCK')
      Doing UNLOCK Action('B', 'pear', 'UNLOCK')

    Adding Action('NA', 'carrot', 'COMMIT') to its transaction

    Doing one action for each transaction:
    Trying to do apple
      Doing LOCK Action('B', 'apple', 'LOCK')
      Doing WRITE Action('B', 'apple', 'WRITE')
    Trying to do carrot
      Doing ROLLBACK (Transaction([Action('C', 'carrot', 'WRITE'), Action('B', 'carrot', 'WRITE'), Action('NA', 'carrot', 'COMMIT')], 2, 1) is younger)
      Doing UNLOCK Action('C', 'carrot', 'UNLOCK')
    Trying to do pear

    Doing one action for each transaction:
    Trying to do apple
      Doing LOCK Action('A', 'apple', 'LOCK')
      Doing WRITE Action('A', 'apple', 'WRITE')
    Trying to do carrot
      Doing LOCK Action('C', 'carrot', 'LOCK')
      Doing WRITE Action('C', 'carrot', 'WRITE')
    Trying to do pear

    Doing one action for each transaction:
    Trying to do apple
      Doing COMMIT Action('NA', 'apple', 'COMMIT')
      Doing UNLOCK Action('A', 'apple', 'UNLOCK')
      Doing UNLOCK Action('B', 'apple', 'UNLOCK')
    Trying to do carrot
      Doing LOCK Action('B', 'carrot', 'LOCK')
      Doing WRITE Action('B', 'carrot', 'WRITE')
    Trying to do pear

    Doing one action for each transaction:
    Trying to do apple
    Trying to do carrot
      Doing COMMIT Action('NA', 'carrot', 'COMMIT')
      Doing UNLOCK Action('B', 'carrot', 'UNLOCK')
      Doing UNLOCK Action('C', 'carrot', 'UNLOCK')
    Trying to do pear

    Doing one action for each transaction:
    Trying to do apple
    Trying to do carrot
    Trying to do pear
    """

  def test_visible_4(self):
    # Multiple writes

    actions = [
      Action(object_="A", transaction="pear", type_="WRITE"),
      Action(object_="B", transaction="pear", type_="WRITE"),
      Action(object_="B", transaction="pear", type_="WRITE"),
      Action(object_="NA", transaction="pear", type_="COMMIT"),
      
      ]

    expected = [Action('A', 'pear', 'LOCK'),
    Action('A', 'pear', 'WRITE'),
    Action('B', 'pear', 'LOCK'),
    Action('B', 'pear', 'WRITE'),
    Action('B', 'pear', 'WRITE'),
    Action('NA', 'pear', 'COMMIT'),
    Action('A', 'pear', 'UNLOCK'),
    Action('B', 'pear', 'UNLOCK')]

    print("Actions = ")
    pprint(actions)

    print("Expected = ")
    pprint(expected)

    result = wait_die_scheduler(actions)
    print("Result = ")
    pprint(result)


    assert expected == result

    """

    Doing one action for each transaction:

    Adding Action('A', 'pear', 'WRITE') to its transaction

    Doing one action for each transaction:
    Trying to do pear
      Doing LOCK Action('A', 'pear', 'LOCK')
      Doing WRITE Action('A', 'pear', 'WRITE')

    Adding Action('B', 'pear', 'WRITE') to its transaction

    Doing one action for each transaction:
    Trying to do pear
      Doing LOCK Action('B', 'pear', 'LOCK')
      Doing WRITE Action('B', 'pear', 'WRITE')

    Adding Action('B', 'pear', 'WRITE') to its transaction

    Doing one action for each transaction:
    Trying to do pear
      Doing WRITE Action('B', 'pear', 'WRITE')

    Adding Action('NA', 'pear', 'COMMIT') to its transaction

    Doing one action for each transaction:
    Trying to do pear
      Doing COMMIT Action('NA', 'pear', 'COMMIT')
      Doing UNLOCK Action('A', 'pear', 'UNLOCK')
      Doing UNLOCK Action('B', 'pear', 'UNLOCK')
    """

  def test_visible_5(self):
    # Another Example

    actions = [
      Action(object_="A", transaction="pear", type_="WRITE"),
      Action(object_="B", transaction="apple", type_="WRITE"),
      Action(object_="C", transaction="carrot", type_="WRITE"),
      Action(object_="B", transaction="apple", type_="WRITE"),
      Action(object_="C", transaction="apple", type_="WRITE"),
      Action(object_="A", transaction="apple", type_="WRITE"),
      Action(object_="NA", transaction="apple", type_="COMMIT"),
      Action(object_="B", transaction="carrot", type_="WRITE"),
      Action(object_="NA", transaction="pear", type_="COMMIT"),
      Action(object_="NA", transaction="carrot", type_="COMMIT"),
      ]

    expected = [Action('A', 'pear', 'LOCK'),
    Action('A', 'pear', 'WRITE'),
    Action('B', 'apple', 'LOCK'),
    Action('B', 'apple', 'WRITE'),
    Action('C', 'carrot', 'LOCK'),
    Action('C', 'carrot', 'WRITE'),
    Action('B', 'apple', 'WRITE'),
    Action('NA', 'apple', 'WAIT'),
    Action('NA', 'apple', 'WAIT'),
    Action('NA', 'apple', 'WAIT'),
    Action('NA', 'apple', 'WAIT'),
    Action('NA', 'carrot', 'ROLLBACK'),
    Action('C', 'carrot', 'UNLOCK'),
    Action('C', 'apple', 'LOCK'),
    Action('C', 'apple', 'WRITE'),
    Action('NA', 'carrot', 'ROLLBACK'),
    Action('NA', 'pear', 'COMMIT'),
    Action('A', 'pear', 'UNLOCK'),
    Action('A', 'apple', 'LOCK'),
    Action('A', 'apple', 'WRITE'),
    Action('NA', 'carrot', 'ROLLBACK'),
    Action('NA', 'apple', 'COMMIT'),
    Action('A', 'apple', 'UNLOCK'),
    Action('B', 'apple', 'UNLOCK'),
    Action('C', 'apple', 'UNLOCK'),
    Action('C', 'carrot', 'LOCK'),
    Action('C', 'carrot', 'WRITE'),
    Action('B', 'carrot', 'LOCK'),
    Action('B', 'carrot', 'WRITE'),
    Action('NA', 'carrot', 'COMMIT'),
    Action('B', 'carrot', 'UNLOCK'),
    Action('C', 'carrot', 'UNLOCK')]

    print("Actions = ")
    pprint(actions)

    print("Expected = ")
    pprint(expected)

    result = wait_die_scheduler(actions)
    print("Result = ")
    pprint(result)


    assert expected == result

    """
    Doing one action for each transaction:

    Adding Action('A', 'pear', 'WRITE') to its transaction

    Doing one action for each transaction:
    Trying to do pear
      Doing LOCK Action('A', 'pear', 'LOCK')
      Doing WRITE Action('A', 'pear', 'WRITE')

    Adding Action('B', 'apple', 'WRITE') to its transaction

    Doing one action for each transaction:
    Trying to do apple
      Doing LOCK Action('B', 'apple', 'LOCK')
      Doing WRITE Action('B', 'apple', 'WRITE')
    Trying to do pear

    Adding Action('C', 'carrot', 'WRITE') to its transaction

    Doing one action for each transaction:
    Trying to do apple
    Trying to do carrot
      Doing LOCK Action('C', 'carrot', 'LOCK')
      Doing WRITE Action('C', 'carrot', 'WRITE')
    Trying to do pear

    Adding Action('B', 'apple', 'WRITE') to its transaction

    Doing one action for each transaction:
    Trying to do apple
      Doing WRITE Action('B', 'apple', 'WRITE')
    Trying to do carrot
    Trying to do pear

    Adding Action('C', 'apple', 'WRITE') to its transaction

    Doing one action for each transaction:
    Trying to do apple
      Doing WAIT (Transaction([Action('B', 'apple', 'WRITE'), Action('B', 'apple', 'WRITE'), Action('C', 'apple', 'WRITE')], 1, 2) is older)
    Trying to do carrot
    Trying to do pear

    Adding Action('A', 'apple', 'WRITE') to its transaction

    Doing one action for each transaction:
    Trying to do apple
      Doing WAIT (Transaction([Action('B', 'apple', 'WRITE'), Action('B', 'apple', 'WRITE'), Action('C', 'apple', 'WRITE'), Action('A', 'apple', 'WRITE')], 1, 2) is older)
    Trying to do carrot
    Trying to do pear

    Adding Action('NA', 'apple', 'COMMIT') to its transaction

    Doing one action for each transaction:
    Trying to do apple
      Doing WAIT (Transaction([Action('B', 'apple', 'WRITE'), Action('B', 'apple', 'WRITE'), Action('C', 'apple', 'WRITE'), Action('A', 'apple', 'WRITE'), Action('NA', 'apple', 'COMMIT')], 1, 2) is older)
    Trying to do carrot
    Trying to do pear

    Adding Action('B', 'carrot', 'WRITE') to its transaction

    Doing one action for each transaction:
    Trying to do apple
      Doing WAIT (Transaction([Action('B', 'apple', 'WRITE'), Action('B', 'apple', 'WRITE'), Action('C', 'apple', 'WRITE'), Action('A', 'apple', 'WRITE'), Action('NA', 'apple', 'COMMIT')], 1, 2) is older)
    Trying to do carrot
      Doing ROLLBACK (Transaction([Action('C', 'carrot', 'WRITE'), Action('B', 'carrot', 'WRITE')], 2, 1) is younger)
      Doing UNLOCK Action('C', 'carrot', 'UNLOCK')
    Trying to do pear

    Adding Action('NA', 'pear', 'COMMIT') to its transaction

    Doing one action for each transaction:
    Trying to do apple
      Doing LOCK Action('C', 'apple', 'LOCK')
      Doing WRITE Action('C', 'apple', 'WRITE')
    Trying to do carrot
      Doing ROLLBACK (Transaction([Action('C', 'carrot', 'WRITE'), Action('B', 'carrot', 'WRITE')], 2, 0) is younger)
    Trying to do pear
      Doing COMMIT Action('NA', 'pear', 'COMMIT')
      Doing UNLOCK Action('A', 'pear', 'UNLOCK')

    Adding Action('NA', 'carrot', 'COMMIT') to its transaction

    Doing one action for each transaction:
    Trying to do apple
      Doing LOCK Action('A', 'apple', 'LOCK')
      Doing WRITE Action('A', 'apple', 'WRITE')
    Trying to do carrot
      Doing ROLLBACK (Transaction([Action('C', 'carrot', 'WRITE'), Action('B', 'carrot', 'WRITE'), Action('NA', 'carrot', 'COMMIT')], 2, 0) is younger)
    Trying to do pear

    Doing one action for each transaction:
    Trying to do apple
      Doing COMMIT Action('NA', 'apple', 'COMMIT')
      Doing UNLOCK Action('A', 'apple', 'UNLOCK')
      Doing UNLOCK Action('B', 'apple', 'UNLOCK')
      Doing UNLOCK Action('C', 'apple', 'UNLOCK')
    Trying to do carrot
      Doing LOCK Action('C', 'carrot', 'LOCK')
      Doing WRITE Action('C', 'carrot', 'WRITE')
    Trying to do pear

    Doing one action for each transaction:
    Trying to do apple
    Trying to do carrot
      Doing LOCK Action('B', 'carrot', 'LOCK')
      Doing WRITE Action('B', 'carrot', 'WRITE')
    Trying to do pear

    Doing one action for each transaction:
    Trying to do apple
    Trying to do carrot
      Doing COMMIT Action('NA', 'carrot', 'COMMIT')
      Doing UNLOCK Action('B', 'carrot', 'UNLOCK')
      Doing UNLOCK Action('C', 'carrot', 'UNLOCK')
    Trying to do pear

    Doing one action for each transaction:
    Trying to do apple
    Trying to do carrot
    Trying to do pear
    """

  def test_visible_6(self):
    # Another Visible One

    actions = [
      Action(object_="A", transaction="carrot", type_="WRITE"),
      Action(object_="A", transaction="pear", type_="WRITE"),
      Action(object_="B", transaction="apple", type_="WRITE"),
      Action(object_="C", transaction="carrot", type_="WRITE"),
      Action(object_="B", transaction="apple", type_="WRITE"),
      Action(object_="D", transaction="fig", type_="WRITE"),
      Action(object_="NA", transaction="fig", type_="COMMIT"),
      Action(object_="C", transaction="apple", type_="WRITE"),
      Action(object_="A", transaction="apple", type_="WRITE"),
      Action(object_="NA", transaction="apple", type_="COMMIT"),
      Action(object_="B", transaction="carrot", type_="WRITE"),
      Action(object_="NA", transaction="pear", type_="COMMIT"),
      Action(object_="NA", transaction="carrot", type_="COMMIT"),
      ]
      
    expected = [Action('A', 'carrot', 'LOCK'),
    Action('A', 'carrot', 'WRITE'),
    Action('NA', 'pear', 'ROLLBACK'),
    Action('B', 'apple', 'LOCK'),
    Action('B', 'apple', 'WRITE'),
    Action('NA', 'pear', 'ROLLBACK'),
    Action('C', 'carrot', 'LOCK'),
    Action('C', 'carrot', 'WRITE'),
    Action('NA', 'pear', 'ROLLBACK'),
    Action('B', 'apple', 'WRITE'),
    Action('NA', 'pear', 'ROLLBACK'),
    Action('D', 'fig', 'LOCK'),
    Action('D', 'fig', 'WRITE'),
    Action('NA', 'pear', 'ROLLBACK'),
    Action('NA', 'fig', 'COMMIT'),
    Action('D', 'fig', 'UNLOCK'),
    Action('NA', 'pear', 'ROLLBACK'),
    Action('NA', 'apple', 'ROLLBACK'),
    Action('B', 'apple', 'UNLOCK'),
    Action('NA', 'pear', 'ROLLBACK'),
    Action('B', 'apple', 'LOCK'),
    Action('B', 'apple', 'WRITE'),
    Action('NA', 'pear', 'ROLLBACK'),
    Action('B', 'apple', 'WRITE'),
    Action('NA', 'pear', 'ROLLBACK'),
    Action('NA', 'apple', 'ROLLBACK'),
    Action('B', 'apple', 'UNLOCK'),
    Action('B', 'carrot', 'LOCK'),
    Action('B', 'carrot', 'WRITE'),
    Action('NA', 'pear', 'ROLLBACK'),
    Action('NA', 'apple', 'ROLLBACK'),
    Action('NA', 'pear', 'ROLLBACK'),
    Action('NA', 'apple', 'ROLLBACK'),
    Action('NA', 'carrot', 'COMMIT'),
    Action('A', 'carrot', 'UNLOCK'),
    Action('B', 'carrot', 'UNLOCK'),
    Action('C', 'carrot', 'UNLOCK'),
    Action('A', 'pear', 'LOCK'),
    Action('A', 'pear', 'WRITE'),
    Action('B', 'apple', 'LOCK'),
    Action('B', 'apple', 'WRITE'),
    Action('NA', 'pear', 'COMMIT'),
    Action('A', 'pear', 'UNLOCK'),
    Action('B', 'apple', 'WRITE'),
    Action('C', 'apple', 'LOCK'),
    Action('C', 'apple', 'WRITE'),
    Action('A', 'apple', 'LOCK'),
    Action('A', 'apple', 'WRITE'),
    Action('NA', 'apple', 'COMMIT'),
    Action('A', 'apple', 'UNLOCK'),
    Action('B', 'apple', 'UNLOCK'),
    Action('C', 'apple', 'UNLOCK')]

    print("Actions = ")
    pprint(actions)

    print("Expected = ")
    pprint(expected)

    result = wait_die_scheduler(actions)
    print("Result = ")
    pprint(result)

    assert expected == result

if __name__ == '__main__':
    unittest.main()  
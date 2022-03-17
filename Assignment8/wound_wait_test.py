import unittest
from pprint import pprint
import sys
import os
sys.path.append("/home/codio/workspace/student_code/")

from wound_wait_scheduler import wound_wait_scheduler, Action

class TestWoundWaitScheduler(unittest.TestCase):
  def test_visible_1(self):
    # Two Transactions

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
    Action('NA', 'apple', 'ROLLBACK'),
    Action('B', 'apple', 'UNLOCK'),
    Action('B', 'pear', 'LOCK'),
    Action('B', 'pear', 'WRITE'),
    Action('NA', 'apple', 'WAIT'),
    Action('NA', 'apple', 'WAIT'),
    Action('NA', 'apple', 'WAIT'),
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

    result = wound_wait_scheduler(actions)
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
      Doing (wounding of apple) ROLLBACK (Transaction([Action('A', 'pear', 'WRITE'), Action('B', 'pear', 'WRITE')], 0, 1) is older)
      Doing UNLOCK Action('B', 'apple', 'UNLOCK')
      Doing LOCK Action('B', 'pear', 'LOCK')
      Doing WRITE Action('B', 'pear', 'WRITE')

    Adding Action('A', 'apple', 'WRITE') to its transaction

    Doing one action for each transaction:
    Trying to do apple
      Doing WAIT (Transaction([Action('B', 'apple', 'WRITE'), Action('A', 'apple', 'WRITE')], 1, 0) is younger)
    Trying to do pear

    Adding Action('NA', 'apple', 'COMMIT') to its transaction

    Doing one action for each transaction:
    Trying to do apple
      Doing WAIT (Transaction([Action('B', 'apple', 'WRITE'), Action('A', 'apple', 'WRITE'), Action('NA', 'apple', 'COMMIT')], 1, 0) is younger)
    Trying to do pear

    Adding Action('NA', 'pear', 'COMMIT') to its transaction

    Doing one action for each transaction:
    Trying to do apple
      Doing WAIT (Transaction([Action('B', 'apple', 'WRITE'), Action('A', 'apple', 'WRITE'), Action('NA', 'apple', 'COMMIT')], 1, 0) is younger)
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
  
  def test_visible_2(self):
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
    Action('NA', 'carrot', 'ROLLBACK'),
    Action('C', 'carrot', 'UNLOCK'),
    Action('C', 'apple', 'LOCK'),
    Action('C', 'apple', 'WRITE'),
    Action('NA', 'carrot', 'WAIT'),
    Action('NA', 'apple', 'WAIT'),
    Action('NA', 'carrot', 'WAIT'),
    Action('NA', 'apple', 'WAIT'),
    Action('NA', 'carrot', 'WAIT'),
    Action('NA', 'apple', 'WAIT'),
    Action('NA', 'carrot', 'WAIT'),
    Action('NA', 'apple', 'WAIT'),
    Action('NA', 'carrot', 'WAIT'),
    Action('NA', 'pear', 'COMMIT'),
    Action('A', 'pear', 'UNLOCK'),
    Action('A', 'apple', 'LOCK'),
    Action('A', 'apple', 'WRITE'),
    Action('NA', 'carrot', 'WAIT'),
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

    result = wound_wait_scheduler(actions)
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
      Doing (wounding of carrot) ROLLBACK (Transaction([Action('B', 'apple', 'WRITE'), Action('B', 'apple', 'WRITE'), Action('C', 'apple', 'WRITE')], 1, 2) is older)
      Doing UNLOCK Action('C', 'carrot', 'UNLOCK')
      Doing LOCK Action('C', 'apple', 'LOCK')
      Doing WRITE Action('C', 'apple', 'WRITE')
    Trying to do carrot
      Doing WAIT (Transaction([Action('C', 'carrot', 'WRITE')], 2, 0) is younger)
    Trying to do pear

    Adding Action('A', 'apple', 'WRITE') to its transaction

    Doing one action for each transaction:
    Trying to do apple
      Doing WAIT (Transaction([Action('B', 'apple', 'WRITE'), Action('B', 'apple', 'WRITE'), Action('C', 'apple', 'WRITE'), Action('A', 'apple', 'WRITE')], 1, 3) is younger)
    Trying to do carrot
      Doing WAIT (Transaction([Action('C', 'carrot', 'WRITE')], 2, 0) is younger)
    Trying to do pear

    Adding Action('NA', 'apple', 'COMMIT') to its transaction

    Doing one action for each transaction:
    Trying to do apple
      Doing WAIT (Transaction([Action('B', 'apple', 'WRITE'), Action('B', 'apple', 'WRITE'), Action('C', 'apple', 'WRITE'), Action('A', 'apple', 'WRITE'), Action('NA', 'apple', 'COMMIT')], 1, 3) is younger)
    Trying to do carrot
      Doing WAIT (Transaction([Action('C', 'carrot', 'WRITE')], 2, 0) is younger)
    Trying to do pear

    Adding Action('B', 'carrot', 'WRITE') to its transaction

    Doing one action for each transaction:
    Trying to do apple
      Doing WAIT (Transaction([Action('B', 'apple', 'WRITE'), Action('B', 'apple', 'WRITE'), Action('C', 'apple', 'WRITE'), Action('A', 'apple', 'WRITE'), Action('NA', 'apple', 'COMMIT')], 1, 3) is younger)
    Trying to do carrot
      Doing WAIT (Transaction([Action('C', 'carrot', 'WRITE'), Action('B', 'carrot', 'WRITE')], 2, 0) is younger)
    Trying to do pear

    Adding Action('NA', 'pear', 'COMMIT') to its transaction

    Doing one action for each transaction:
    Trying to do apple
      Doing WAIT (Transaction([Action('B', 'apple', 'WRITE'), Action('B', 'apple', 'WRITE'), Action('C', 'apple', 'WRITE'), Action('A', 'apple', 'WRITE'), Action('NA', 'apple', 'COMMIT')], 1, 3) is younger)
    Trying to do carrot
      Doing WAIT (Transaction([Action('C', 'carrot', 'WRITE'), Action('B', 'carrot', 'WRITE')], 2, 0) is younger)
    Trying to do pear
      Doing COMMIT Action('NA', 'pear', 'COMMIT')
      Doing UNLOCK Action('A', 'pear', 'UNLOCK')

    Adding Action('NA', 'carrot', 'COMMIT') to its transaction

    Doing one action for each transaction:
    Trying to do apple
      Doing LOCK Action('A', 'apple', 'LOCK')
      Doing WRITE Action('A', 'apple', 'WRITE')
    Trying to do carrot
      Doing WAIT (Transaction([Action('C', 'carrot', 'WRITE'), Action('B', 'carrot', 'WRITE'), Action('NA', 'carrot', 'COMMIT')], 2, 0) is younger)
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

  def test_visible_3(self):
    # More Help

    actions = [
      Action(object_="A", transaction="pear", type_="WRITE"),
      Action(object_="B", transaction="apple", type_="WRITE"),
      Action(object_="C", transaction="carrot", type_="WRITE"),
      Action(object_="B", transaction="apple", type_="WRITE"),
      Action(object_="C", transaction="apple", type_="WRITE"),
      Action(object_="A", transaction="apple", type_="WRITE"),
      Action(object_="NA", transaction="apple", type_="COMMIT"),
      Action(object_="B", transaction="carrot", type_="WRITE"),
      Action(object_="NA", transaction="carrot", type_="COMMIT"),
      Action(object_="NA", transaction="pear", type_="COMMIT"),
      ]

    expected = [Action('A', 'pear', 'LOCK'),
    Action('A', 'pear', 'WRITE'),
    Action('B', 'apple', 'LOCK'),
    Action('B', 'apple', 'WRITE'),
    Action('C', 'carrot', 'LOCK'),
    Action('C', 'carrot', 'WRITE'),
    Action('B', 'apple', 'WRITE'),
    Action('NA', 'carrot', 'ROLLBACK'),
    Action('C', 'carrot', 'UNLOCK'),
    Action('C', 'apple', 'LOCK'),
    Action('C', 'apple', 'WRITE'),
    Action('NA', 'carrot', 'WAIT'),
    Action('NA', 'apple', 'WAIT'),
    Action('NA', 'carrot', 'WAIT'),
    Action('NA', 'apple', 'WAIT'),
    Action('NA', 'carrot', 'WAIT'),
    Action('NA', 'apple', 'WAIT'),
    Action('NA', 'carrot', 'WAIT'),
    Action('NA', 'apple', 'WAIT'),
    Action('NA', 'carrot', 'WAIT'),
    Action('NA', 'apple', 'WAIT'),
    Action('NA', 'carrot', 'WAIT'),
    Action('NA', 'pear', 'COMMIT'),
    Action('A', 'pear', 'UNLOCK'),
    Action('A', 'apple', 'LOCK'),
    Action('A', 'apple', 'WRITE'),
    Action('NA', 'carrot', 'WAIT'),
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

    result = wound_wait_scheduler(actions)
    print("Result = ")
    pprint(result)
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
      Doing (wounding of carrot) ROLLBACK (Transaction([Action('B', 'apple', 'WRITE'), Action('B', 'apple', 'WRITE'), Action('C', 'apple', 'WRITE')], 1, 2) is older)
      Doing UNLOCK Action('C', 'carrot', 'UNLOCK')
      Doing LOCK Action('C', 'apple', 'LOCK')
      Doing WRITE Action('C', 'apple', 'WRITE')
    Trying to do carrot
      Doing WAIT (Transaction([Action('C', 'carrot', 'WRITE')], 2, 0) is younger)
    Trying to do pear

    Adding Action('A', 'apple', 'WRITE') to its transaction

    Doing one action for each transaction:
    Trying to do apple
      Doing WAIT (Transaction([Action('B', 'apple', 'WRITE'), Action('B', 'apple', 'WRITE'), Action('C', 'apple', 'WRITE'), Action('A', 'apple', 'WRITE')], 1, 3) is younger)
    Trying to do carrot
      Doing WAIT (Transaction([Action('C', 'carrot', 'WRITE')], 2, 0) is younger)
    Trying to do pear

    Adding Action('NA', 'apple', 'COMMIT') to its transaction

    Doing one action for each transaction:
    Trying to do apple
      Doing WAIT (Transaction([Action('B', 'apple', 'WRITE'), Action('B', 'apple', 'WRITE'), Action('C', 'apple', 'WRITE'), Action('A', 'apple', 'WRITE'), Action('NA', 'apple', 'COMMIT')], 1, 3) is younger)
    Trying to do carrot
      Doing WAIT (Transaction([Action('C', 'carrot', 'WRITE')], 2, 0) is younger)
    Trying to do pear

    Adding Action('B', 'carrot', 'WRITE') to its transaction

    Doing one action for each transaction:
    Trying to do apple
      Doing WAIT (Transaction([Action('B', 'apple', 'WRITE'), Action('B', 'apple', 'WRITE'), Action('C', 'apple', 'WRITE'), Action('A', 'apple', 'WRITE'), Action('NA', 'apple', 'COMMIT')], 1, 3) is younger)
    Trying to do carrot
      Doing WAIT (Transaction([Action('C', 'carrot', 'WRITE'), Action('B', 'carrot', 'WRITE')], 2, 0) is younger)
    Trying to do pear

    Adding Action('NA', 'carrot', 'COMMIT') to its transaction

    Doing one action for each transaction:
    Trying to do apple
      Doing WAIT (Transaction([Action('B', 'apple', 'WRITE'), Action('B', 'apple', 'WRITE'), Action('C', 'apple', 'WRITE'), Action('A', 'apple', 'WRITE'), Action('NA', 'apple', 'COMMIT')], 1, 3) is younger)
    Trying to do carrot
      Doing WAIT (Transaction([Action('C', 'carrot', 'WRITE'), Action('B', 'carrot', 'WRITE'), Action('NA', 'carrot', 'COMMIT')], 2, 0) is younger)
    Trying to do pear

    Adding Action('NA', 'pear', 'COMMIT') to its transaction

    Doing one action for each transaction:
    Trying to do apple
      Doing WAIT (Transaction([Action('B', 'apple', 'WRITE'), Action('B', 'apple', 'WRITE'), Action('C', 'apple', 'WRITE'), Action('A', 'apple', 'WRITE'), Action('NA', 'apple', 'COMMIT')], 1, 3) is younger)
    Trying to do carrot
      Doing WAIT (Transaction([Action('C', 'carrot', 'WRITE'), Action('B', 'carrot', 'WRITE'), Action('NA', 'carrot', 'COMMIT')], 2, 0) is younger)
    Trying to do pear
      Doing COMMIT Action('NA', 'pear', 'COMMIT')
      Doing UNLOCK Action('A', 'pear', 'UNLOCK')

    Doing one action for each transaction:
    Trying to do apple
      Doing LOCK Action('A', 'apple', 'LOCK')
      Doing WRITE Action('A', 'apple', 'WRITE')
    Trying to do carrot
      Doing WAIT (Transaction([Action('C', 'carrot', 'WRITE'), Action('B', 'carrot', 'WRITE'), Action('NA', 'carrot', 'COMMIT')], 2, 0) is younger)
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

    assert expected == result


  def test_visible_4(self):
    # Another Visible

    actions = [
      Action(object_="A", transaction="pear", type_="WRITE"),
      Action(object_="B", transaction="apple", type_="WRITE"),
      Action(object_="C", transaction="carrot", type_="WRITE"),
      Action(object_="B", transaction="apple", type_="WRITE"),
      Action(object_="C", transaction="apple", type_="WRITE"),
      Action(object_="A", transaction="apple", type_="WRITE"),
      Action(object_="NA", transaction="apple", type_="COMMIT"),
      Action(object_="B", transaction="carrot", type_="WRITE"),
      Action(object_="B", transaction="pear", type_="WRITE"),
      Action(object_="NA", transaction="pear", type_="COMMIT"),
      Action(object_="NA", transaction="carrot", type_="COMMIT"),
      Action(object_="Q", transaction="lemon", type_="WRITE"),
      Action(object_="NA", transaction="lemon", type_="COMMIT"),
      ]
      
    expected = [Action('A', 'pear', 'LOCK'),
    Action('A', 'pear', 'WRITE'),
    Action('B', 'apple', 'LOCK'),
    Action('B', 'apple', 'WRITE'),
    Action('C', 'carrot', 'LOCK'),
    Action('C', 'carrot', 'WRITE'),
    Action('B', 'apple', 'WRITE'),
    Action('NA', 'carrot', 'ROLLBACK'),
    Action('C', 'carrot', 'UNLOCK'),
    Action('C', 'apple', 'LOCK'),
    Action('C', 'apple', 'WRITE'),
    Action('NA', 'carrot', 'WAIT'),
    Action('NA', 'apple', 'WAIT'),
    Action('NA', 'carrot', 'WAIT'),
    Action('NA', 'apple', 'WAIT'),
    Action('NA', 'carrot', 'WAIT'),
    Action('NA', 'apple', 'WAIT'),
    Action('NA', 'carrot', 'WAIT'),
    Action('NA', 'apple', 'WAIT'),
    Action('NA', 'carrot', 'WAIT'),
    Action('NA', 'apple', 'ROLLBACK'),
    Action('B', 'apple', 'UNLOCK'),
    Action('C', 'apple', 'UNLOCK'),
    Action('B', 'pear', 'LOCK'),
    Action('B', 'pear', 'WRITE'),
    Action('NA', 'apple', 'WAIT'),
    Action('C', 'carrot', 'LOCK'),
    Action('C', 'carrot', 'WRITE'),
    Action('NA', 'pear', 'COMMIT'),
    Action('A', 'pear', 'UNLOCK'),
    Action('B', 'pear', 'UNLOCK'),
    Action('B', 'apple', 'LOCK'),
    Action('B', 'apple', 'WRITE'),
    Action('NA', 'carrot', 'WAIT'),
    Action('B', 'apple', 'WRITE'),
    Action('NA', 'carrot', 'WAIT'),
    Action('Q', 'lemon', 'LOCK'),
    Action('Q', 'lemon', 'WRITE'),
    Action('NA', 'carrot', 'ROLLBACK'),
    Action('C', 'carrot', 'UNLOCK'),
    Action('C', 'apple', 'LOCK'),
    Action('C', 'apple', 'WRITE'),
    Action('NA', 'carrot', 'WAIT'),
    Action('NA', 'lemon', 'COMMIT'),
    Action('Q', 'lemon', 'UNLOCK'),
    Action('A', 'apple', 'LOCK'),
    Action('A', 'apple', 'WRITE'),
    Action('NA', 'carrot', 'WAIT'),
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

    result = wound_wait_scheduler(actions)
    print("Result = ")
    pprint(result)


    assert expected == result
    

if __name__ == '__main__':
    unittest.main()  
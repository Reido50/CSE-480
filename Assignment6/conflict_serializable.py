from sqlalchemy import false


class Action:
  """
  This is the Action class. It is already in the test cases, so please don't
  put it in your solution.
  """
  def __init__(self, object_, transaction, is_write):
    self.object_ = object_
    self.transaction = transaction
    self.is_write = is_write

  def __str__(self):
    return f"Action({self.object_}, {self.transaction}, {self.is_write})"

def detect_conflict(action_a, action_b):
    if action_a.transaction == action_b.transaction:
        return True
    elif action_a.object_ != action_b.object_:
        return False
    elif action_a.is_write or action_b.is_write:
        return True 
    return False

def determine_precedence(list_of_actions):
    precdence = []
    for i in range(len(list_of_actions)):
        for j in range(i + 1, len(list_of_actions)):
            first = list_of_actions[i]
            second = list_of_actions[j]
            if detect_conflict(first, second) and first.transaction != second.transaction:
                precdence.append((first.transaction, second.transaction))
    return sorted(set(precdence))

def is_conflict_serializable(schedule):
    precedence = determine_precedence(schedule)
    for first in precedence:
        for second in precedence:
            if first == second:
                continue
            if first[0] == second[1] and first[1] == second[0]:
                return False
    return True

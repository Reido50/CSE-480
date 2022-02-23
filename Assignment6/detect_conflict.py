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
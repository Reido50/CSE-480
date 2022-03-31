class Action:
  """
  This is the Action class. It is already in the test cases, so please don't
  put it in your solution.
  """
  def __init__(self, object_, transaction, type_):
    self.object_ = object_
    self.transaction = transaction
    assert type_ in ("READ", "WRITE", "LOCK", "UNLOCK")
    self.type_ = type_
  def __str__(self):
    return f"Action({self.object_}, {self.transaction}, {self.type_})"
  __repr__ = __str__

class NotSerial(Exception): pass

def check_if_serial(actions):
  done_trans = []
  current_trans = None
  for action in actions:
    if current_trans is None:
      current_trans = action.transaction
    elif current_trans != action.transaction:
      if action.transaction in done_trans:
        raise NotSerial("Not Serial!");
      else:
        done_trans.append(current_trans)
        current_trans = action.transaction

actions = [
    Action(object_="A", transaction="T2", type_="LOCK"),
    Action(object_="B", transaction="T3", type_="LOCK"),
    Action(object_="A", transaction="T2", type_="UNLOCK"),
    ]
check_if_serial(actions)
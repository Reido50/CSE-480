class LegalityOfScheduleViolation(Exception): pass
class TwoPhasedLockingViolation(Exception): pass
class ConsistencyOfTransactionViolation(Exception): pass

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


# Do not modify code above this line

def validate_locking_schedule(actions):
    active = {}
    for action in actions:
        if action.type == "READ" or action.type == "WRITE":
            # Check if read/write is valid
            if active.get(action.transaction) == None:
                raise ConsistencyOfTransactionViolation("Cannot write/read in a transaction with no locks.")
            else:
                read = False
                for obj_locked in action[action.transaction]:
                    if obj_locked == action.object:
                        read = True
                        break
        elif action.type == "LOCK":
            # Add lock to active
            if active.get(action.transaction) == None:
                active[action.transaction] = [action.object]
            else:
                active[action.transaction].append(action.object)
        else:
            # Remove lock from active if exists
            if active.get(action.transaction) == None:
                raise ConsistencyOfTransactionViolation("Cannot unlock in a transaction with no locks.")
            else:
                unlocked = False
                for obj_locked in active[action.transaction]:
                    if obj_locked == action.object:
                        active[action.transaction].remove(obj_locked)
                        unlocked = True
                        break
                if not unlocked:
                    raise ConsistencyOfTransactionViolation("Cannot unlock an object that is not locked.")                    
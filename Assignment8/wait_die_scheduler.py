from pprint import pprint

class Action:
  """
  This is the Action class.
  """
  def __init__(self, object_, transaction, type_):
    self.object_ = object_
    self.transaction = transaction
    assert type_ in ("WRITE", "COMMIT", "ROLLBACK", "LOCK", "UNLOCK", "WAIT")
    self.type_ = type_
  def __str__(self):
    return f"Action('{self.object_}', '{self.transaction}', '{self.type_}')"
  __repr__ = __str__
  def __eq__(self, other):
    return ((self.object_ == other.object_) and 
      (self.transaction == other.transaction) and 
      (self.type_ == other.type_))



# Do not modify any code above this line


def wait_die_scheduler(actions):
    # Initialize the empty schedule
    schedule = []
    transactions = {}
    current_index_in_transaction = {}
    locks = {}
    timestamp = {}
    time = 0
    actionInd = 0

    while True:
        # Doing one action for each transaction
        for key in sorted(transactions.keys()):
            i = current_index_in_transaction[key]
            if i >= len(transactions[key]): continue
            attempt = transactions[key][i]

            # Process Action
            if attempt.type_ == "WRITE":
                if locks.get(attempt.object_) is not None:
                    # If the item is locked
                    if locks[attempt.object_] == attempt.transaction:
                        schedule.append(attempt)
                    elif timestamp[attempt.transaction] < timestamp[locks[attempt.object_]]:
                        # Wait
                        schedule.append(Action("NA", attempt.transaction, "WAIT"))
                        continue
                    else:
                        # Die
                        schedule.append(Action("NA", attempt.transaction, "ROLLBACK"))
                        for item in locks.items():
                            if item[1] == attempt.transaction:
                                locks[item[0]] = None
                                schedule.append(Action(item[0], item[1], "UNLOCK"))
                        current_index_in_transaction[key] = 0
                        continue
                else:
                    # If the item is not locked
                    schedule.append(Action(attempt.object_, attempt.transaction, "LOCK"))
                    locks[attempt.object_] = attempt.transaction
                    schedule.append(attempt)
            elif attempt.type_ == "COMMIT":
                schedule.append(attempt)
                for item in locks.items():
                    if item[1] == attempt.transaction:
                        locks[item[0]] = None
                        schedule.append(Action(item[0], item[1], "UNLOCK"))
                locks[attempt.object_] = None
            current_index_in_transaction[key] += 1

        # Adding Action to its transaction
        if actionInd < len(actions):
            action = actions[actionInd]
            if transactions.get(action.transaction) is None:
                transactions[action.transaction] = [action]
                current_index_in_transaction[action.transaction] = 0
                timestamp[action.transaction] = time
                time += 1
            else:
                transactions[action.transaction].append(action)
            actionInd += 1

        # Check if it's time to stop
        done = True
        for key in transactions:
            i = current_index_in_transaction[key]
            if i < len(transactions[key]): done = False
        if actionInd < len(actions):
            done = False
        if done:
            break

    # Return the schedule
    return schedule

actions = [
      Action(object_="A", transaction="pear", type_="WRITE"),
      Action(object_="B", transaction="pear", type_="WRITE"),
      Action(object_="B", transaction="pear", type_="WRITE"),
      Action(object_="NA", transaction="pear", type_="COMMIT"),
      ]
pprint(wait_die_scheduler(actions))
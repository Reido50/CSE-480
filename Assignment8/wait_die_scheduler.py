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

    # Store actions of the transactions and setup indexing
    transactions = {}
    current_index_in_transaction = {}
    for action in actions:
        if (transactions.get(action.transaction) is None):
            transactions[action.transaction] = [action]
            current_index_in_transaction[action.transaction] = 0
        else:
            transactions[action.transaction].append(action)
    
    # Iterate through transactions, picking one action out of each at a time
    done = False
    locks = {}
    while not done:
        done = True
        for key in transactions:
            i = current_index_in_transaction[key]
            if i >= len(transactions[key]): continue
            action = transactions[key][i]

            # Process Action
            print(action)
            if action.type_ == "WRITE":
                if locks.get(action.object_) is not None:
                    if action.transaction < locks[action.object_]:
                        schedule.append(Action(action.object_, action.transaction, "WAIT"))
                    else:
                        schedule.append(Action(action.object_, action.transaction, "ROLLBACK"))
                        current_index_in_transaction[key] = 0
                        continue
                else:
                    schedule.append(Action(action.object_, action.transaction, "LOCK"))
                    locks[action.object_] = action.transaction
                schedule.append(action)
            elif action.type_ == "COMMIT":
                schedule.append(action)
                schedule.append(Action(action.object_, action.transaction, "UNLOCK"))

            current_index_in_transaction[key] += 1
            if current_index_in_transaction[key] != len(transactions[key]):
                done = False

    # Return the schedule
    return schedule

actions = [
      Action(object_="A", transaction="pear", type_="WRITE"),
      Action(object_="NA", transaction="pear", type_="COMMIT"),
      ]
print(wait_die_scheduler(actions))
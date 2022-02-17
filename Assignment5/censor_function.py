# Note not all or your solution should be in the function definition 

def censor(x):
  new_string = x
  censor_list = ["UMich", "Maize", "Blue", "Wolverines"]
  for word in censor_list:
    new_string = new_string.replace(word, "*" * len(word))
  return new_string
    

def add_censor_function(conn):
  conn.create_function("censor", 1, censor)

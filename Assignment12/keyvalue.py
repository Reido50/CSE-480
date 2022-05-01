# START OF SERVER.PY
import copy
class Server:
    def __init__(self):
        self.store = {}

    def insert(self, key, value):
        self.store[key] = value

    def read(self, key):
        return self.store.get(key)

    def replace_store(self, new_store):
        self.store = copy.deepcopy(new_store)

# START OF CLIENT.PY
servers = []
master_store = {}
class Client:
    def __init__(self, server_instance):
        if server_instance not in servers:
            servers.append(server_instance)
        self.server = server_instance

    def put(self, key, value):
        self.server.insert(key, value)
        master_store[key] = value

    def get(self, key):
        return self.server.read(key)

    def sync_servers(self):
        for s in servers:
            s.replace_store(master_store)


# START OF THE EXAMPLE CODE
# Constructing a server and two clients linked to it
s1 = Server()
c1 = Client(s1)
c2 = Client(s1)

# Storing the key "hello" with the value "world"
c1.put("hello", "world")

# Note, both clients should agree on the changes to the server 
assert c1.get("hello") == "world"
assert c2.get("hello") == "world"

# A new (empty) server and client
s2 = Server()
c3 = Client(s2)

# This other server should not have access to the original server's data
assert c3.get("hello") is None

# Syncs all the servers together
c2.sync_servers()

# Now the second server knows about "hello" -> "world"
assert c3.get("hello") == "world"

# However, the servers are still independant
c3.put("josh", "nahum")
assert c2.get("josh") is None
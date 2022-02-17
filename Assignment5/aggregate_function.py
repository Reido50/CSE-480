class LineCensor:
    def __init__(self):
        self.lineCount = 0
    def step(self, value):
        censor_list = ["UMich", "Maize", "Blue", "Wolverines"]
        for word in censor_list:
            if value.find(word) != -1:
                self.lineCount += 1
                return
    def finalize(self):
        return self.lineCount

def add_aggregate_function(conn):
    conn.create_aggregate("lines_censored", 1, LineCensor)

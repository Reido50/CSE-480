class Table:
    def __init__(self):
        self.contents = []
        pass

    def insert_into(self, row):
        self.contents.append(row)
        pass
    
    def select(self, columns_to_display, columns_to_order_by):
        selected = []
        for row in self.contents:
            selected_row = []
            for label in columns_to_display:
                selected_row.append(row[label])
            selected.append(selected_row)
        
        pass

table_1 = Table()

table_1.insert_into(row = {"name": "Josh", "grade": 3.0, "age": 31, "eye": "brown"})
table_1.insert_into(row = {"name": "Emily", "grade": 3.5, "age": 29, "eye": "hazel"})
table_1.insert_into(row = {"name": "Josh", "grade": 3.0, "age": 30, "eye": "green"})
table_1.insert_into(row = {"name": "Josh", "grade": 2.0, "age": 20, "eye": "red"})

result = table_1.select(
    columns_to_display = ["grade", "age", "name"], 
    columns_to_order_by = ["name", "age"])

expected = [[3.5, 29, 'Emily'], [2.0, 20, 'Josh'], [3.0, 30, 'Josh'], [3.0, 31, 'Josh']]

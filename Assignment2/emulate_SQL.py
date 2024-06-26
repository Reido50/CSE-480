class Table:
    def __init__(self):
        self.contents = []
        pass

    def insert_into(self, row):
        self.contents.append(row)
        pass
    
    def select(self, columns_to_display, columns_to_order_by):
        # Sort contents
        for i in range(len(columns_to_order_by) - 1, -1, -1):
            self.contents = sorted(self.contents, key = lambda l: l[columns_to_order_by[i]])

        # Select contents
        selected = []
        for row in self.contents:
            selected_row = []
            for select_label in columns_to_display:
                selected_row.append(row[select_label])
            selected.append(selected_row)
        return selected
        pass

    def left_outer_join(self, other_table, self_on_column, other_on_column):
        joined = Table()

        for self_val in self.select([self_on_column], []):
            for other_val in other_table.select([other_on_column], []):
                if self_val == other_val:
                    joined.insert_into()
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

print(result)

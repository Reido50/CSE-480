import csv

def get_balances(csv_string):
    csv_lines = csv_string.split('\n')
    csv_list = csv.reader(csv_lines, delimiter=',')
    user_transaction = {}
    column_order = {"User" : 0, "Amount" : 0, "Transaction" : 0, "Notes" : 0}
    first_row = True
    for row in csv_list:
        if first_row:
            index = 0
            for label in row:
                column_order[label] = index
                index += 1
            first_row = False
        else:
            transaction = (int)(row[column_order["Amount"]])
            if row[column_order["Transaction"]] == "Withdraw":
                transaction = -transaction
            if user_transaction.get(row[column_order["User"]]) is None:
                user_transaction[row[column_order["User"]]] = 0
            user_transaction[row[column_order["User"]]] += transaction
    return user_transaction

test_str = "User,Amount,Transaction,Notes\nReid,5,Deposit,bleh\nReid,3,Withdraw,bleh"
print(get_balances(test_str))

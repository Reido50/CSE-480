def collate_josh(left, right):
    if left.find("josh") != -1 and right.find("josh")  == -1:
        return -1
    if left.find("josh") == -1 and right.find("josh")  != -1:
        return 1
    if left == right:
        return 0
    if left < right:
        return -1
    else:
        return 1


def add_collation(conn):
    conn.create_collation("JOSH_FIRST", collate_josh)

print(collate_josh("a josh", "a josh"))
print(collate_josh("zach josh", "abc"))
print(collate_josh("abc", "bhja"))

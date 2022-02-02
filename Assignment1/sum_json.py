import json

def sum_all_numbers_in_list(l):
    sum = 0
    for item in l:
        if type(item) is dict:
            sum += sum_all_numbers_in_list(item.values())
        elif type(item) is list or type(item) is tuple:
            sum += sum_all_numbers_in_list(item)
        elif type(item) is int or type(item) is float:
            sum += item
    return sum

def sum_all_JSON_numbers(json_string):
    json_dict = json.loads(json_string)
    return sum_all_numbers_in_list(json_dict.values())

input_string = '{"name":"josh", "age":31, "instructor":true, "degree dates": [2005, 2006, 2013], "pets":["CrashDown", "Ghost", "RaceTrack", "Dany"], "car":{"model":"Ford Fusion", "milage":170000, "snacks":["sunflower seeds", "beef jerkey", "candy"]}}'
print(sum_all_JSON_numbers(input_string))
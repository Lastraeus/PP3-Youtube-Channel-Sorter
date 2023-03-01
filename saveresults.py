import os
import json


def leading_zeros_filenum(num):
    """Takes a int and returns a string with 5 leading zeros.
    For use as as a file number"""
    result = f'{num:05d}'
    return result


def save_data_to_json(data):
    isExist = os.path.exists("/outputs/json")
    if not isExist:
        os.makedirs("/outputs/json")
    filenum = 1
    filenum_string = leading_zeros_filenum(filenum)
    filepath = (f'outputs/json/output{filenum_string}.json')
    while os.path.exists(filepath):
        filenum = filenum + 1
        filenum_string = leading_zeros_filenum(filenum)
        filepath = (f'outputs/json/output{filenum_string}.json')
    jsonString = json.dumps(data)
    jsonFile = open(filepath, "w")
    jsonFile.write(jsonString)
    jsonFile.close()
    return filepath


def string_to_txt_file(string):
    isExist = os.path.exists("outputs/txt")
    if not isExist:
        os.makedirs("outputs/txt")
    filenum = 1
    filenum_string = leading_zeros_filenum(filenum)
    filepath = (f'outputs/txt/output{filenum_string}.txt')
    while os.path.exists(filepath):
        filenum = filenum + 1
        filenum_string = leading_zeros_filenum(filenum)
        filepath = (f'outputs/txt/output{filenum_string}.txt')
    with open(filepath, 'w') as f:
        f.write(string)
    return filepath


# test_string1 = """Hello, world!
# This is a test.
# thank you!"""
# test_string2 = """Another Test"""
# test_string3 = """A Third Test"""

# string_to_txt_file(test_string1)
# string_to_txt_file(test_string2)
# string_to_txt_file(test_string3)
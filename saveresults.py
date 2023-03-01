from os.path import exists
import json


def leading_zeros_filenum(num):
    """Takes a int and returns a string with 5 leading zeros.
    For use as as a file number"""
    result = f'{num:05d}'
    return result


def save_data_to_json(data):
    filenum = 1
    filenum_string = leading_zeros_filenum(filenum)
    filepath = (f'test/json/test_output{filenum_string}.json')
    while exists(filepath):
        filenum = filenum + 1
        filenum_string = leading_zeros_filenum(filenum)
        filepath = (f'test/json/test_output{filenum_string}.json')
    jsonString = json.dumps(data)
    jsonFile = open(filepath, "w")
    jsonFile.write(jsonString)
    jsonFile.close()


def string_to_txt_file(string):
    filenum = 1
    filenum_string = leading_zeros_filenum(filenum)
    filepath = (f'test/txt/test_output{filenum_string}.txt')
    while exists(filepath):
        filenum = filenum + 1
        filenum_string = leading_zeros_filenum(filenum)
        filepath = (f'test/txt/test_output{filenum_string}.txt')
    with open(filepath, 'w') as f:
        f.write(string)


# test_string1 = """Hello, world!
# This is a test.
# thank you!"""
# test_string2 = """Another Test"""
# test_string3 = """A Third Test"""

# string_to_txt_file(test_string1)
# string_to_txt_file(test_string2)
# string_to_txt_file(test_string3)
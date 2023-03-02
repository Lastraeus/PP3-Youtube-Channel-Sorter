import os
import json
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials


def leading_zeros_filenum(num):
    """Takes a int and returns a string with 5 leading zeros.
    For use as a file number"""
    result = f'{num:05d}'
    return result


def save_data_to_json(data):
    """takes a json compatitble object and saves it as a json to the
    outputs/json folder returns the filepath to it."""
    isExist = os.path.exists("/outputs")
    if not isExist:
        os.makedirs("/outputs")
    filenum = 1
    filenum_string = leading_zeros_filenum(filenum)
    filepath = (f'outputs/output{filenum_string}.json')
    while os.path.exists(filepath):
        filenum = filenum + 1
        filenum_string = leading_zeros_filenum(filenum)
        filepath = (f'outputs/output{filenum_string}.json')
    jsonString = json.dumps(data)
    jsonFile = open(filepath, "w")
    jsonFile.write(jsonString)
    jsonFile.close()
    return filepath


def string_to_txt_file(string):
    """takes string and saves it as a txt file to the outputs/txt folder
    returns the filepath to it."""
    isExist = os.path.exists("outputs/")
    if not isExist:
        os.makedirs("outputs")
    filenum = 1
    filenum_string = leading_zeros_filenum(filenum)
    filepath = (f'outputs/output{filenum_string}.txt')
    while os.path.exists(filepath):
        filenum = filenum + 1
        filenum_string = leading_zeros_filenum(filenum)
        filepath = (f'outputs/output{filenum_string}.txt')
    with open(filepath, 'w') as f:
        f.write(string)
    return filepath


def upload_file_to_gdrive(file_path, folder_name):
    """Take the filepath of the new file and target folder of the gdrive,
    creates a instance pydrive2 instance then uploads it to drive.
    Sets permissions for the file to sharable and provides the link"""
    scope = ["https://www.googleapis.com/auth/drive"]
    gauth = GoogleAuth()
    gauth.auth_method = 'service'
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'drive_creds.json',
        scope
        )
    drive = GoogleDrive(gauth)

    if folder_name == "txt":
        folder_id = '1OzCotUCYfZEhczTSBD-WnwA_TJbyPiNZ'  # txt folder

    file1 = drive.CreateFile(
        {'parents': [{"id": folder_id}]})
    file1.SetContentFile(file_path)
    file1.Upload()
    file1.InsertPermission({
        'type': 'anyone',
        'value': 'anyone',
        'role': 'reader'})
    print('Your result is saved at the link below.')
    print('Select it with mouse and right click --> copy \n')
    print(file1['alternateLink'])

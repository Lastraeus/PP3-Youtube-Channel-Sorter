from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials


def upload_file_to_gdrive(content, filename):
    """Creates a instance pydrive2 file, with the inputted details
    then uploads it to drive. Sets permissions for the file to
    sharable and provides the link"""
    scope = ["https://www.googleapis.com/auth/drive"]
    gauth = GoogleAuth()
    gauth.auth_method = 'service'
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'drive_creds.json',
        scope
        )
    drive = GoogleDrive(gauth)

    folder_id = '1Of9A2YgSDtcuh6yt8Vc3uTFE9LKtbZH_'  # /sorter/all folder

    mimetype = "text/plain"

    file1 = drive.CreateFile(
        {
            'parents': [{"id": folder_id}],
            'title': filename,
            'mimeType': mimetype,
        }
        )
    file1.SetContentString(content)
    file1.Upload()
    file1.InsertPermission({
        'type': 'anyone',
        'value': 'anyone',
        'role': 'reader'})
    print('Your result is saved at the link below.')
    print('Select it with mouse and right click --> copy \n')
    print(file1['alternateLink'])

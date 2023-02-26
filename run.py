"""
Query template from 
https://medium.com/mcd-unison/youtube-data-api-v3-in
-python-tutorial-with-examples-e829a25d2ebd#5999
"""
import googleapiclient.discovery
import pytube  # specifically pip install git+https://github.com/felipeucelli/pytube.git for modern channelurl parsing
import json

test_channel1 = "https://www.youtube.com/@kaptainkristian"
test_channel2 = "https://www.youtube.com/@billwurtz"
test_channel3 = "https://www.youtube.com/@billwurtzwrongname"

f = open("creds.json")
api_key_data = json.load(f)



try:
    channel = pytube.Channel(test_channel1)
    channel_id = channel.channel_id
    print(channel_id)
except:
    print("That is not a valid youtube URL")


# API information
api_service_name = "youtube"
api_version = "v3"
# API key
DEVELOPER_KEY = api_key_data["key1"]
print(DEVELOPER_KEY)

# print("Welcome to the YouTube Channel Sorter")
# inputted_url = input("Please input a channel URL \n")
# print(f'The chosen url is {inputted_url}')

# API client
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)
# # 'request' variable is the only thing you must change
# # depending on the resource and method you need to use
# # in your query
# request = None #add request here when channel ID in hand



# # Query execution
# response = request.execute()
# # Print the results
# print(response)
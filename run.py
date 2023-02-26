import googleapiclient.discovery
import pytube  # specifically pip install git+https://github.com/felipeucelli/pytube.git for modern channelurl parsing
import json, datetime

from dateutil.relativedelta import relativedelta
from dateutil import parser

test_channel1 = "https://www.youtube.com/@kaptainkristian"
test_channel2 = "https://www.youtube.com/user/billwurtz"
test_channel4 = "https://www.youtube.com/user/billwurtz"
test_channel4 = "https://www.youtube.com/@billwurtzwrongname" # Invalid case
test_channel5 = "https://www.youtube.com/@scottmanley/videos"

api_service_name = "youtube"
api_version = "v3"
f = open("creds.json")
api_key_data = json.load(f)
DEVELOPER_KEY = api_key_data["key1"]
channel_all_vid_playlist_id = False


print("Welcome to the YouTube Channel Sorter")
inputted_url = input("Please input a channel URL \n")

try:
    channel = pytube.Channel(inputted_url)
    channel_id = channel.channel_id
    print("Channel Found")
    channel_all_vid_playlist_id = channel_id[:1] + "U" + channel_id[1 + 1:]  #https://stackoverflow.com/questions/41752946/replacing-a-character-from-a-certain-index
except:
    print("That is not a valid YouTube Channel URL")

def assess_oldest_date(in_date, timeframe):
    now = datetime.datetime.now()
    check_date = parser.parse(in_date).date()
    delta = relativedelta(check_date, now)
    print(delta)




if channel_all_vid_playlist_id:
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)

    # 'request' variable is the only thing you must change
    # depending on the resource and method you need to use
    # in your query
    request = youtube.playlistItems().list(        
        part="snippet,contentDetails",
        maxResults=50,
        playlistId=channel_all_vid_playlist_id
    )

    # Query execution
    print("Preparing to compile channel video data")
    response = request.execute()
    print("Channel Data Compiled")
    returned_videos = response["items"]
    last_video_on_page = returned_videos[-1]
    oldest_publishedDate_on_page = last_video_on_page["snippet"]["publishedAt"]

    print(f'Oldest Video on this results page was posted {oldest_publishedDate_on_page}')
    print(assess_oldest_date(oldest_publishedDate_on_page, 0))
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
TEST_TARGET_DATE = datetime.datetime(2022, 2, 27)

def print_initial_screen():
    print("Welcome to the YouTube Channel Sorter")

def user_prompt():
    inputted_url = input("Please input a valid channel URL \n")

    try:
        channel = pytube.Channel(inputted_url)
        channel_id = channel.channel_id
        print("Channel Found")
        channel_all_vid_playlist_id = channel_id[:1] + "U" + channel_id[1 + 1:]
        return channel_all_vid_playlist_id

    except:
        print("That is not a valid YouTube Channel URL")
        user_prompt()

def assess_oldest_date(in_date, timeframe):
    now = datetime.datetime.now()
    check_date = parser.parse(in_date).date()
    delta = relativedelta(check_date, now)
    print(delta)

def parse_api_response(response):
    returned_videos = response["items"]
    last_video_on_page = returned_videos[-1]
    oldest_publishedAt_on_page = last_video_on_page["snippet"]["publishedAt"]
    return oldest_publishedAt_on_page

def query_api(playlist_id):
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)

    # 'request' variable is the only thing you must change
    # depending on the resource and method you need to use
    # in your query
    request = youtube.playlistItems().list(        
        part="snippet,contentDetails",
        maxResults=50,
        playlistId=playlist_id
    )

    # Query execution
    print("Preparing to return channel video data")
    r = request.execute()
    return r
    print("Channel Data returned successfully")
    

def result_output(passed_result):
    print(f'Oldest Video in in last 50 uploaded to channel was posted {passed_result}')
    print(assess_oldest_date(passed_result, 0))

def main():
    print_initial_screen()
    query = user_prompt()
    print(query)
    if query:
        print("channelID secrured")
        r = query_api(query)
        result = parse_api_response(r)
        result_output(result)

if __name__ == "__main__":
    main()
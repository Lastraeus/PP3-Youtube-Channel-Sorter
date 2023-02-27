import json 
import datetime
import googleapiclient.discovery
import pytube  # specifically pip install git+https://github.com/felipeucelli/pytube.git for modern channelurl parsing
from googleapiclient.errors import HttpError
from dateutil.relativedelta import relativedelta
from dateutil import parser
from dateutil import tz
from operator import itemgetter
from ascii import logo1

# INITIAL VARIABLES -------------------------------------------------------------------------------
api_service_name = "youtube"
api_version = "v3"
f = open("creds.json")
api_key_data = json.load(f)
DEVELOPER_KEY = api_key_data["key1"]
SAMPLE_RETURN_DATE = parser.parse("2022-09-19T18:08:46Z") #used to get correct timezone for comparison
ACCEPTED_TIMEFRAMES = ["y", "s", "m", "w"]
live_now = datetime.datetime.now  #run as live_now()
api_response_meta = {}
full_vid_list = []
last_page_token = ""
need_next_page = False
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)
vid_ids = []
vids_to_show = []
eighty_hashes = "--------------------------------------------------------------------------------"

# Welcome and Prompt Fucntion Section -------------------------------------------------------------
def print_initial_screen():
    print(logo1)
    print("Welcome to the YouTube Channel Sorter")
    print("Created by Cian Lane\n")
    print("See https://github.com/Lastraeus/PP3-Youtube-Channel-Sorter \nfor README and full credits\n\n")


def channel_prompt():
    inputted_url = input("Please input a valid channel URL \n")

    try:
        channel = pytube.Channel(inputted_url)
        channel_id = channel.channel_id
        print("Channel Found")
        channel_all_vid_playlist_id = channel_id[:1] + "U" + channel_id[1 + 1:]
        return channel_all_vid_playlist_id
    except:
        print("That is not a valid YouTube Channel URL")
        channel_prompt()


def timeframe_prompt():
    print(
"""
Choose timeframe for most views; \n
Last (Y)ear, Last (S)ix Months, Last (M)onth, Last (W)eek
"""
    )
    selected_timeframe = input("Enter a letter:\n")
    selected_timeframe = selected_timeframe.lower()
    if selected_timeframe in ACCEPTED_TIMEFRAMES:
        tf = calculate_past_timeframes(selected_timeframe)
        print("Loading Selected Results")
        print("This can take a minute if the channel has many videos")
        return tf

    print(f'{selected_timeframe} is not in {ACCEPTED_TIMEFRAMES}')
    print("please enter one of the bracketed letters to select")


def calculate_past_timeframes(input_letter):
    if input_letter == "y":
        one_year_ago = live_now() - relativedelta(years=+1)
        return one_year_ago

    elif input_letter == "s":
        six_months_ago = live_now() - relativedelta(months=+6)
        return six_months_ago

    elif input_letter == "m":
        one_month_ago = live_now() - relativedelta(months=+1)
        return one_month_ago

    elif input_letter == "w":
        one_week_ago = live_now() - relativedelta(weeks=+1)
        return one_week_ago

    else:
        print("Unknown Timeframe passed")


# Response Parsing Section ------------------------------------------------------------------------
def get_total_vids(response):
    total_channel_videos = response["pageInfo"]["totalResults"]
    return total_channel_videos


def get_next_page_token(response):
    next_token = response["nextPageToken"]
    return next_token


def get_oldest_date_in_response(response):
    returned_videos = response["items"]
    last_video_on_page = returned_videos[-1]
    oldest_datetime = parser.parse(last_video_on_page["snippet"]["publishedAt"])
    return oldest_datetime


def add_response_vids_to_list(response):
    returned_videos = response["items"]

    for i in returned_videos:
        full_vid_list.append(i)

    save_data_to_json(full_vid_list, "test_vid_list")


def date_format_to_google_dates(target_date, SAMPLE_RETURN_DATE):
    target_date_tz = target_date.astimezone(SAMPLE_RETURN_DATE.tzinfo)
    return target_date_tz


def is_next_page_needed(last_video_date, target_date):
    if last_video_date > target_date:
        return True
    else:
        return False


def sort_and_trim_vid_list(list_of_dicts):
    newlist = sorted(list_dicts, key=itemgetter('name'), reverse=True)


def grab_ids_in_date(target_date):
    for item in full_vid_list:
        item_datetime = parser.parse(item["snippet"]["publishedAt"])
        if item_datetime > target_date:
            vid_ids.append(item['contentDetails']['videoId'])


# Output Results After Searching/Parsing Section --------------------------------------------------------------
def output_results(results, response, last_date):
    total_channel_vids = get_total_vids(response)
    vids_to_show.sort(key=lambda vid: vid['views'], reverse=True)
    print(eighty_hashes)  # default width of template terminal
    print(f'Channel has {total_channel_vids} total visible videos\n')
    print(f'Channel has {len(vids_to_show)} videos in selected timeframe\n')
    print(f'Oldest Video in Selected Timeframe uploaded to channel was posted:')
    print(last_date)
    print(eighty_hashes)
    for video in vids_to_show[:10]:
        print(video["title"])
        print(f'Views: {video["views"]}, Published: {video["published"]}')
        print(video['url'], "\n")


def handle_error_reason(error_reason):
    if error_reason == "playlistNotFound":
        print("Unfortunately this channel/playlist doesn't seem to have any videos")
        print("Please try again or choose another")
        print("This time... maybe try one with videos that need sorting\n")
    
    if "quota" in error_reason.lower():
        if (DEVELOPER_KEY == api_key_data["key1"]):
            DEVELOPER_KEY = api_key_data["key2"]
        else:
            print("Issue with API Quota Limit. Maybe Try Again Tomorrow.")


# Utility Function Section ------------------------------------------------------------------------
def save_data_to_json(data, filename):
    jsonString = json.dumps(full_vid_list)
    jsonFile = open(f'{filename}.json', "w")
    jsonFile.write(jsonString)
    jsonFile.close()


def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


# Query API Functions Section ---------------------------------------------------------------------
def query_api(playlist_id):
    request = youtube.playlistItems().list(        
        part="snippet,contentDetails",
        maxResults=50,
        playlistId=playlist_id
    )
    

    # If the error is a rate limit or connection error,
    # wait and try again.
    # if err.resp.status in [403, 500, 503]:
    #     time.sleep(5)
    # else: raise
    try:
        r = request.execute()
        return r
    except HttpError as err:
        if err.resp.get('content-type', '').startswith('application/json'):
            reason = json.loads(err.content).get('error').get('errors')[0].get('reason')
            handle_error_reason(reason)
            return None


def query_api_next_page(playlist_id, token):
    request = youtube.playlistItems().list(        
        part="snippet,contentDetails",
        maxResults=50,
        playlistId=playlist_id,
        pageToken=token
    )
    r = request.execute()
    return r


def query_vids(vid_ids):
    nextPageToken = None
    if len(vid_ids) <= 50:
        while True:
            vid_request = youtube.videos().list(
                part="snippet,statistics",
                id=','.join(vid_ids),
                maxResults=50
            )

            vid_response = vid_request.execute()

            for item in vid_response['items']:
                vid_views = item['statistics']['viewCount']
                published = item["snippet"]["publishedAt"]
                vid_id = item['id']
                title = item["snippet"]["title"]
                yt_link = f'https://youtu.be/{vid_id}'

                vids_to_show.append(
                    {
                        'views': int(vid_views),
                        'title': title,
                        'url': yt_link,
                        "published": published
                    }
                )

            nextPageToken = vid_response.get('nextPageToken')

            if not nextPageToken:
                break
    else:
        list_of_ids_lists = list(divide_chunks(vid_ids, 50))
        split_vid_list_query(list_of_ids_lists)


def split_vid_list_query(list_of_ids_lists):
    for id_list in list_of_ids_lists:
        nextPageToken = None
        while True:
            vid_request = youtube.videos().list(
                part="snippet,statistics",
                id=','.join(id_list),
                maxResults=50
            )

            vid_response = vid_request.execute()

            for item in vid_response['items']:
                vid_views = item['statistics']['viewCount']
                vid_id = item['id']
                title = item["snippet"]["title"]
                published = item["snippet"]["publishedAt"]
                yt_link = f'https://youtu.be/{vid_id}'

                vids_to_show.append(
                    {
                        'views': int(vid_views),
                        'title': title,
                        'url': yt_link,
                        "published": published
                    }
                )

            nextPageToken = vid_response.get('nextPageToken')

            if not nextPageToken:
                break


# Main() Section ----------------------------------------------------------------------------------
def main():
    print_initial_screen()
    r = None
    while r == None:
        channel_playlist_id = channel_prompt()
        saved_playlist_id = channel_playlist_id
        target_date = None
        while target_date == None:
            target_date = timeframe_prompt()
        target_date = date_format_to_google_dates(target_date, SAMPLE_RETURN_DATE)
        r = query_api(channel_playlist_id)
    # save_data_to_json(r, "latest_response_test")
    original_response = r #Save for general channel/playlist metadata parsing
    oldest_response_datetime = get_oldest_date_in_response(r)
    add_response_vids_to_list(r)
    while is_next_page_needed(oldest_response_datetime, target_date):
        if r["nextPageToken"]:
            token = r["nextPageToken"]
            r = query_api_next_page(saved_playlist_id, token)
            oldest_response_datetime = get_oldest_date_in_response(r)
            add_response_vids_to_list(r)
            # save_data_to_json(r, "latest_response_test")
        else:
            break
    grab_ids_in_date(target_date)
    query_vids(vid_ids)
    output_results(vids_to_show, original_response, oldest_response_datetime)

if __name__ == "__main__":
    main()

# Channels on hand to test app with ---------------------------------------------------------------
# test_channel1 = "https://www.youtube.com/@kaptainkristian"
# test_channel2 = "https://www.youtube.com/@quill18"
# test_channel4 = "https://www.youtube.com/user/billwurtz"
# test_channel4 = "https://www.youtube.com/@billwurtzwrongname" # Invalid case
# test_channel5 = "https://www.youtube.com/@scottmanley/videos"

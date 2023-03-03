"""
Runs and organizes the main operations of the YouTube Channel Sorter App.
Handles welcome screen, initial user prompts,
parsing user prompts into appropriate querys
and the youtube api querys themselves.
Passes the results to output_system.py for
final outputting."""
import json
import datetime

import pytube  # specifically https://github.com/felipeucelli/pytube.git
import pyinputplus as pyip
import googleapiclient.discovery
from googleapiclient.errors import HttpError
from dateutil.relativedelta import relativedelta
from dateutil import parser

from ascii import LOGO
import output_system as out

# YouTube API query componenet variables--------------------------------------
# https://medium.com/mcd-unison
# /youtube-data-api-v3-in-python-tutorial-with-examples-e829a25d2ebd#5999
# for initial query template
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
f = open("yt_creds.json", encoding="utf-8")
API_KEY_DATA = json.load(f)
DEVELOPER_KEY = API_KEY_DATA["key1"]
youtube = googleapiclient.discovery.build(
    API_SERVICE_NAME,
    API_VERSION,
    developerKey=DEVELOPER_KEY
    )


# Welcome and Prompt Fucntion Section ----------------------------------------


def print_initial_screen():
    """Prints The Logo and Initial details of app"""
    print(LOGO)
    print("Welcome to the YouTube Channel Sorter")
    print("Created by Cian Lane\n")
    print("See https://github.com/Lastraeus/PP3-Youtube-Channel-Sorter")
    print("for README and full credits\n")
    print("The Default search sort will be:")
    print(out.DEFAULT_STRING)
    print('There will be a option to re-sort, re-print')
    print('and save the full results at the end\n')
    print("Hint: Right-Click and copy/paste the link from youtube itself\n")


def channel_prompt():
    """Asks for a channel url to sort, then uses pytube
    to validate any possible valid YouTube URL
    Returns the playlist ID of the channel if found with pytube.
    if the search failed it lets the user know to try again"""
    inputted_url = input("Please input a valid channel URL:\n")

    try:
        channel = pytube.Channel(inputted_url)
        channel_id = channel.channel_id
        print("Channel Found")
        channel_all_vid_playlist_id = channel_id[:1] + "U" + channel_id[1 + 1:]
        # channel "all videos" playlist id is same as channel id but
        # with the second char changed to "U" instead of "C"
        return channel_all_vid_playlist_id
    except Exception:
        print("That is not a valid YouTube Channel URL")


def timeframe_prompt():
    """Asks the user to select a valid timeframe.
    Keeps asking until one is received
    returns that timeframe"""
    print("""
Choose timeframe for most views; \n
Last (Y)ear, Last (S)ix Months, Last (M)onth, Last (W)eek
""")
    selected_timeframe = input("Enter a letter:\n")
    selected_timeframe = selected_timeframe.lower()
    if selected_timeframe in out.ACCEPTED_TIMEFRAMES:
        timeframe = calculate_past_timeframes(selected_timeframe)
        print(out.LINE_STRING)
        print("Loading Selected Results")
        print("This can take a minute if the channel has many videos")
        return timeframe

    print(f'{selected_timeframe} is not in {out.ACCEPTED_TIMEFRAMES}')
    print("please enter one of the bracketed letters to select")


def calculate_past_timeframes(input_letter):
    """Accepts the selected timeframe letter and converts that to a
    datetime unit"""
    live_now = datetime.datetime.now  # run as live_now()
    if input_letter == "y":
        # https://stackoverflow.com/questions/546321
        # /how-do-i-calculate-the-date-six
        # -months-from-the-current-date-using-the-datetime
        one_year_ago = live_now() - relativedelta(years=+1)
        print('You selected: "Last Year"')
        return one_year_ago

    elif input_letter == "s":
        six_months_ago = live_now() - relativedelta(months=+6)
        print('You selected: "Last Six Months"')
        return six_months_ago

    elif input_letter == "m":
        one_month_ago = live_now() - relativedelta(months=+1)
        print('You selected: "Last Month"')
        return one_month_ago

    elif input_letter == "w":
        one_week_ago = live_now() - relativedelta(weeks=+1)
        print('You selected: "Last Week"')
        return one_week_ago

    else:
        print("Unknown Timeframe passed")


# YouTube Query API Functions Section ----------------------------------------
# https://github.com/CoreyMSchafer/code_snippets
# /blob/master/Python/YouTube-API/03-Most-Popular-Video-Playlist/start.py
# was heavily refferenced here for my api query functions needs
def query_playlistitems_api(playlist_id, token=None):
    """takes a playlist ID from prompt and returns the json response"""
    play_list_request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=50,
        playlistId=playlist_id,
        pageToken=token
    )
    # https://stackoverflow.com/questions/
    # 23945784/how-to-manage-google-api-errors-in-python
    try:
        resp = play_list_request.execute()
        print("API call was a sucess")
        return resp
    except HttpError as err:
        if err.resp.get('content-type', '').startswith('application/json'):
            reason = json.loads(err.content).get('error').get('errors')[0].get(
                'reason'
                )
            print(reason)
            return None


def query_vids(id_list, target_list):
    """takes a list of video ids and then returns details about them.
    All items are appended to vids_in_target_time dict"""
    next_page_token = None
    if len(id_list) <= 50:
        while True:
            vid_request = youtube.videos().list(
                part="snippet,statistics",
                id=','.join(id_list),
                maxResults=50
            )

            vid_response = vid_request.execute()

            for item in vid_response['items']:
                vid_views = item['statistics']['viewCount']
                try:
                    vid_likes = item['statistics']['likeCount']
                except KeyError:
                    vid_likes = ""
                try:
                    vid_comments = item['statistics']['commentCount']
                except KeyError:
                    vid_comments = ""
                date = item["snippet"]["publishedAt"]
                channel = item["snippet"]["channelTitle"]
                vid_id = item['id']
                title = item["snippet"]["title"]
                yt_link = f'https://youtu.be/{vid_id}'

                target_list.append(
                    {
                        'title': title,
                        'likes': vid_likes,
                        'comments': vid_comments,
                        'views': int(vid_views),
                        'url': yt_link,
                        "date": date,
                        'channel': channel
                    }
                )

            next_page_token = vid_response.get('nextPageToken')

            if not next_page_token:
                break

    else:
        list_of_vid_id_lists = list(divide_chunks(id_list, 50))
        split_vid_list_query(list_of_vid_id_lists)


def split_vid_list_query(list_of_vid_id_lists):
    """Feeds a block of 50 video ids to api to query,
    due to max of 50 ids submitted per query
    all of which end up appended to vids_in_target_time dictionary"""
    for id_list in list_of_vid_id_lists:
        query_vids(id_list)


# Response Parsing Section ---------------------------------------------------


def get_oldest_date_in_response(response):
    """searches the api response json for the oldest video
    published date in the list of items.
    can check the last item in any batch response list,
    as well as the last video in the trimmed results within timeframe"""
    # https://www.geeksforgeeks.org/type-isinstance-python/
    if isinstance(response, list):
        last_video_on_page = response[-1]
        oldest_datetime = parser.parse(last_video_on_page["date"])
        return oldest_datetime
    else:
        returned_videos = response["items"]
        last_video_on_page = returned_videos[-1]
        oldest_datetime = parser.parse(
            last_video_on_page["snippet"]["publishedAt"]
            )
        return oldest_datetime


def add_playlist_items_to_list(response):
    """After a playlist query is searched, add the found video json items
    to the full_playlist_items_list"""
    returned_videos = response["items"]
    items_list = []
    
    for item in returned_videos:
        items_list.append(item)
    
    return items_list


def date_format_to_google_dates(target_date, sample_date):
    """converts a standard datetime object to the timezone format
    that google api results return in"""
    # https://appdividend.com/2023/01/
    # 07/typeerror-cant-compare-offset-naive-and-offset-aware-datetimes/
    target_date_tz = target_date.astimezone(sample_date.tzinfo)
    return target_date_tz


def grab_ids_in_date(target_date, items_list):
    """strips the ids from the playlist items in full_playlist_items_list
    only grabs the ones in target_date range
    adds them to the vid_id_list for a 'video list query'
    to get significantly more details on each"""
    out_list = []
    for item in items_list:
        item_datetime = parser.parse(item["snippet"]["publishedAt"])
        if item_datetime > target_date:
            out_list.append(item['contentDetails']['videoId'])
    
    return out_list


# Utility Function Section --------------------------------------------------


# https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
def divide_chunks(list_to_divide, max_chunk_size):
    """Divides a list of items into a list of smaller lists of size max
    used to divide id_lists that are too long for googles multi_video list
    api query"""
    for i in range(0, len(list_to_divide), max_chunk_size):
        yield list_to_divide[i:i + max_chunk_size]


def handle_error_reason(error_reason):
    """handles api error cases;
    playlistNotFound for a channel with no videos
    and any error mentioning quota incase a limit is reached"""
    if error_reason == "playlistNotFound":
        print("""Unfortunately this channel/playlist
            doesn't seem to have any videos
            """)
        print("Please try again or choose another")
        print("This time... maybe try one with videos that need sorting\n")

    if "quota" in error_reason.lower():
        print("Issue with API Quota Limit. Try Again Tomorrow when it resets.")


def ask_restart():
    """asks the user if they would like to search again, if not
    it then ends the program"""
    print('Would you like to run another search? y/n?')
    print()
    yesno = pyip.inputYesNo(default="no")
    if yesno == "no":
        print("Goodbye!")
        exit()


# Main() Section -------------------------------------------------------------
def main_search():
    """The Main search loop. Takes the user from inputting valid url,
    through timeframe selection, and then makes query calls to youtube api
    returns metadata after query_vids() has added all neccessary items to
    vids_in_target_time"""
    resp = None
    while resp is None:

        channel_playlist_id = None
        while channel_playlist_id is None:
            channel_playlist_id = channel_prompt()

        saved_playlist_id = channel_playlist_id

        target_date = None
        while target_date is None:
            target_date = timeframe_prompt()

        SAMPLE_RETURN_DATE = parser.parse("2022-09-19T18:08:46Z")
        # used to get correct timezone for comparison
        # (Taken from test qurey result)

        target_date = date_format_to_google_dates(
            target_date,
            SAMPLE_RETURN_DATE)

        resp = query_playlistitems_api(channel_playlist_id)

    original_resp = resp  # Save for general channel/playlist metadata

    oldest_response_datetime = get_oldest_date_in_response(resp)

    full_playlist_items_list = []
    
    full_playlist_items_list = add_playlist_items_to_list(
        resp)
    while oldest_response_datetime > target_date:
        if resp["nextPageToken"]:
            token = resp["nextPageToken"]
            resp = query_playlistitems_api(saved_playlist_id, token)
            oldest_response_datetime = get_oldest_date_in_response(resp)
            full_playlist_items_list = add_playlist_items_to_list(
                resp)

        else:
            break

    timeframe_vid_ids = grab_ids_in_date(
        target_date,
        full_playlist_items_list)

    viditems_in_target_time = []
    query_vids(timeframe_vid_ids, viditems_in_target_time)

    lastvideo_date_in_timeframe = get_oldest_date_in_response(
        viditems_in_target_time
        )

    return viditems_in_target_time, original_resp, lastvideo_date_in_timeframe


def main():
    """Holds main loop(for multiple searches), Runs welcome screen, runs
    main_search then moves to output. Loops output while user is still
    sorting the results. moves to asking the user for another search from
    the start, exits if they are done."""
    try:
        while True:
            print_initial_screen()
            org_resp = None
            last_video_date = None
            vids_in_target_time, org_resp, last_video_date = main_search()
            out.output_loop(vids_in_target_time, org_resp, last_video_date)
            ask_restart()

    except KeyboardInterrupt:
        print("Unfortuneatly Ctrl-C is the shortcut to exit this template.")
        print("Please run again.")


if __name__ == "__main__":
    main()

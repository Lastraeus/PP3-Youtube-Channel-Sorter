import math
import json
import datetime
from os import remove

import pytube  # specifically https://github.com/felipeucelli/pytube.git
import pyinputplus as pyip
import googleapiclient.discovery
from googleapiclient.errors import HttpError
from dateutil.relativedelta import relativedelta
from dateutil import parser

import saveresults
from ascii import logo1

# INITIAL VARIABLES ----------------------------------------------------------
api_service_name = "youtube"
api_version = "v3"
f = open("yt_creds.json")
api_key_data = json.load(f)
DEVELOPER_KEY = api_key_data["key1"]
SAMPLE_RETURN_DATE = parser.parse("2022-09-19T18:08:46Z")
# used to get correct timezone for comparison

ACCEPTED_TIMEFRAMES = ["y", "s", "m", "w"]
live_now = datetime.datetime.now  # run as live_now()
api_response_meta = {}
full_vid_list = []
youtube = googleapiclient.discovery.build(
    api_service_name,
    api_version,
    developerKey=DEVELOPER_KEY
    )
vid_id_list = []
vids_in_target_time = []
LINE_STRING = "-" * 80  # Max width of template terminal is 80 chars
DEFAULT_SORT_ORDER = 'views'
DEFAULT_NUM_OF_RESULTS = 3

# Welcome and Prompt Fucntion Section ----------------------------------------


def print_initial_screen():
    """Prints The Logo and Initial details of app"""
    print(logo1)
    print("Welcome to the YouTube Channel Sorter")
    print("Created by Cian Lane\n")
    print("See https://github.com/Lastraeus/PP3-Youtube-Channel-Sorter")
    print("for README and full credits\n\n")

    print("Hint: Right Click and copy/paste is all that works here :(\n\n")


def channel_prompt():
    """Asks for a channel url to sort, then uses pytube
    to validate any possible valid YouTube URL
    Returns the channel ID if found with pytube
    if the search failed it lets the user know to try again"""
    inputted_url = input("Please input a valid channel URL \n")

    try:
        channel = pytube.Channel(inputted_url)
        channel_id = channel.channel_id
        print("Channel Found")
        channel_all_vid_playlist_id = channel_id[:1] + "U" + channel_id[1 + 1:]
        return channel_all_vid_playlist_id
    except Exception():
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
    if selected_timeframe in ACCEPTED_TIMEFRAMES:
        timeframe = calculate_past_timeframes(selected_timeframe)
        print(LINE_STRING)
        print("Loading Selected Results")
        print("This can take a minute if the channel has many videos")
        return timeframe

    print(f'{selected_timeframe} is not in {ACCEPTED_TIMEFRAMES}')
    print("please enter one of the bracketed letters to select")


def calculate_past_timeframes(input_letter):
    """Accepts the selected timeframe letter and converts that to a
    datetime unit"""
    if input_letter == "y":
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


# Response Parsing Section ---------------------------------------------------


def get_total_channel_vids(response):
    """searches the api response json for the total video count on the channel"""
    total_channel_videos = response["pageInfo"]["totalResults"]
    return total_channel_videos


def get_oldest_date_in_response(response):
    """searches the api response json for the odlest video published date in the list of items.
    can check the last item in any batch response list, 
    as well as the last video in the trimmed results within timeframe"""

    if type(response) is list:
        last_video_on_page = response[-1]
        oldest_datetime = parser.parse(last_video_on_page["published"])
        return oldest_datetime
    else:
        returned_videos = response["items"]
        last_video_on_page = returned_videos[-1]
        oldest_datetime = parser.parse(
            last_video_on_page["snippet"]["publishedAt"]
            )
        return oldest_datetime


def add_response_vids_to_list(response):
    """After a playlist query is searched, add the found video json items
    to the full_vid_list"""
    returned_videos = response["items"]
    for i in returned_videos:
        full_vid_list.append(i)


def date_format_to_google_dates(target_date, sample_date):
    """converts a standard datetime object to the timezone format
    that google api results return in"""
    target_date_tz = target_date.astimezone(sample_date.tzinfo)
    return target_date_tz


def grab_ids_in_date(target_date):
    """strips the ids from the playlist items in full_vid_list
    only grabs the ones in target_date range
    adds them to the vid_id_list for a 'video list query'
    to get significantly more details on each"""
    for item in full_vid_list:
        item_datetime = parser.parse(item["snippet"]["publishedAt"])
        if item_datetime > target_date:
            vid_id_list.append(item['contentDetails']['videoId'])


def get_credits_used(total_videos):
    """takes a int of total videos returned from query
    returns the amount of api quota credits it took to get"""
    x = total_videos
    quota_credits_used = math.ceil((x / 50)) * 2
    return quota_credits_used


# Output Results After Searching/Parsing Section -----------------------------
def output_results(results, response, last_date):
    """combines and formats the gathered data and then outputs it for the user.
    offers them a choice of saving the full result as a google drive link"""
    total_channel_vids = get_total_channel_vids(response)
    total_vids_in_timeframe = len(vids_in_target_time)
    quota_used = get_credits_used(total_vids_in_timeframe)

    vids_in_target_time.sort(
        key=lambda vid: vid[DEFAULT_SORT_ORDER],
        reverse=True)

    output_header_string = make_header_string(
        total_channel_vids,
        total_vids_in_timeframe,
        last_date,
        quota_used)

    terminal_output_results_string = make_terminal_results_string(
        output_header_string,
        DEFAULT_SORT_ORDER,
        DEFAULT_NUM_OF_RESULTS
        )

    print(terminal_output_results_string)
    print(LINE_STRING)
    print('Would you like to save the full list of results to a text file?')
    print('Enter y/n')
    yesno = pyip.inputYesNo(default="no")
    if yesno == "yes":
        full_output_string = make_full_results_string(output_header_string)
        newfile = saveresults.string_to_txt_file(full_output_string)
        try:
            saveresults.upload_file_to_gdrive(newfile, "txt")
            remove(newfile)
        except Exception as e:
            print(e)


def make_header_string(
        total_channel_vids,
        total_vids_in_timeframe,
        last_date,
        quota_used):
    """Combines meta info for the search and makes a header string to
    go at the top of the result output. Returns the string"""

    output_header_list = []
    output_header_list.append(LINE_STRING)
    output_header_list.append(
        f'Channel has {total_channel_vids} total visible videos\n'
        )
    output_header_list.append(
        f'Channel has {total_vids_in_timeframe} videos in selected timeframe\n'
        )
    output_header_list.append(
        'Oldest Video in Selected Timeframe uploaded to channel was posted:'
        )
    output_header_list.append(f'{last_date}')
    output_header_list.append(f'Total API Quota Credits used: {quota_used}')
    output_header_list.append(LINE_STRING)
    output_header_string = "\n".join(output_header_list)
    return output_header_string


def make_terminal_results_string(
    output_header_string,
    order=DEFAULT_SORT_ORDER,
    total_output_results=DEFAULT_NUM_OF_RESULTS,
):
    """Takes the defaults and strings needed to format results for the terminal and then
    combines them and returns it"""

    terminal_output_part_list = []

    settings = (
        f'Top {total_output_results} Results\nSorted by: {order}'
        )
    output_results_list = []
    for video in vids_in_target_time[:total_output_results]:
        output_results_list.append(video["title"])
        output_results_list.append(
            f'Views: {video["views"]}, Published: {video["published"]}'
            )
        output_results_list.append(f'{video["url"]}\n')
    terminal_output_results_string = "\n".join(output_results_list)

    terminal_output_part_list.append(output_header_string)
    terminal_output_part_list.append(settings)
    terminal_output_part_list.append(LINE_STRING)
    terminal_output_part_list.append(terminal_output_results_string)
    terminal_output_string = "\n".join(terminal_output_part_list)

    return terminal_output_string


def make_full_results_string(output_header_string):
    """Takes the defaults and strings needed to format results for the full list of results and then
    combines them and returns it"""
    output_results_list = []

    for video in vids_in_target_time:
        output_results_list.append(video["title"])
        output_results_list.append(
            f'Views: {video["views"]}, Published: {video["published"]}'
            )
        output_results_list.append(f'{video["url"]}\n')
    full_output_results_string = "\n".join(output_results_list)

    full_output_part_list = []
    full_output_part_list.append(output_header_string)
    full_output_part_list.append(full_output_results_string)
    full_output_string = "\n".join(full_output_part_list)

    return full_output_string


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
    print('Would you like to run another search? y/n')
    yesno = pyip.inputYesNo(default="no")
    if yesno == "no":
        print("Goodbye!")
        exit()


# Utility Function Section --------------------------------------------------
def divide_chunks(list_to_divide, max):
    """Divides a list of items into a list of smaller lists of size max
    used to divide id_lists that are too long for googles multi_video list
    api query"""
    for i in range(0, len(list_to_divide), max):
        yield list_to_divide[i:i + max]


# YouTube Query API Functions Section ----------------------------------------
def query_playlistitems_api(playlist_id, token=None):
    play_list_request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=50,
        playlistId=playlist_id,
        pageToken=token
    )

    # https://stackoverflow.com/questions/23945784/how-to
    # -manage-google-api-errors-in-python
    # If the error is a rate limit or connection error,
    # wait and try again.
    # if err.resp.status in [403, 500, 503]:
    #     time.sleep(5)
    # else: raise
    try:
        r = play_list_request.execute()
        return r
    except HttpError as err:
        if err.resp.get('content-type', '').startswith('application/json'):
            reason = json.loads(err.content).get('error').get('errors')[0].get(
                'reason'
                )
            handle_error_reason(reason)
            return None


def query_vids(id_list):
    nextPageToken = None
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
                published = item["snippet"]["publishedAt"]
                vid_id = item['id']
                title = item["snippet"]["title"]
                yt_link = f'https://youtu.be/{vid_id}'

                vids_in_target_time.append(
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
        list_of_vid_id_lists = list(divide_chunks(id_list, 50))
        split_vid_list_query(list_of_vid_id_lists)


def split_vid_list_query(list_of_vid_id_lists):
    """Feeds a block of 50 video ids to api to query,
    due to max of 50 ids submitted per query"""
    for vid_id_list in list_of_vid_id_lists:
        query_vids(vid_id_list)


# Main() Section -------------------------------------------------------------
def main():
    while True:
        print_initial_screen()
        r = None
        while r is None:
            channel_playlist_id = channel_prompt()
            saved_playlist_id = channel_playlist_id
            target_date = None
            while target_date is None:
                target_date = timeframe_prompt()
            target_date = date_format_to_google_dates(
                target_date,
                SAMPLE_RETURN_DATE)
            r = query_playlistitems_api(channel_playlist_id)
        original_response = r  # Save for general channel/playlist metadata
        oldest_response_datetime = get_oldest_date_in_response(r)
        add_response_vids_to_list(r)
        while oldest_response_datetime > target_date:
            if r["nextPageToken"]:
                token = r["nextPageToken"]
                r = query_playlistitems_api(saved_playlist_id, token)
                oldest_response_datetime = get_oldest_date_in_response(r)
                add_response_vids_to_list(r)
            else:
                break
        grab_ids_in_date(target_date)
        query_vids(vid_id_list)
        last_video_date_in_timeframe = get_oldest_date_in_response(
            vids_in_target_time
            )
        output_results(
            vids_in_target_time,
            original_response,
            last_video_date_in_timeframe
            )
        ask_restart()


if __name__ == "__main__":
    main()

"""Module for Youtube-Channel-Sorter to handle YouTube API Calls
within a certain timeframe when main_search is called,
used for returning data on channel videos
 in a certain timeframe"""
import json

import googleapiclient.discovery
from googleapiclient.errors import HttpError
from dateutil import parser

import channel_id_getter

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

# Main Search Logic Section---------------------------------------------------


def main_search():
    """The main search loop. Takes the user from inputting valid url,
    through timeframe selection, and then makes query calls to youtube api
    returns metadata after query_vids() has added all neccessary items to
    vids_in_target_time"""
    resp = None
    while resp is None:
        playlist_id = channel_id_getter.get_valid_channel_id()
        target_date = channel_id_getter.get_target_date()

        resp = query_playlistitems_api(playlist_id)

    original_response = resp  # Save for general channel/playlist metadata

    oldest_response_datetime = get_oldest_date_in_response(resp)

    full_playlist_items_list = []

    full_playlist_items_list = add_playlist_items_to_list(
        resp)
    while oldest_response_datetime > target_date:
        if resp["nextPageToken"]:
            token = resp["nextPageToken"]
            resp = query_playlistitems_api(playlist_id, token)
            oldest_response_datetime = get_oldest_date_in_response(resp)
            full_playlist_items_list = add_playlist_items_to_list(
                resp)

        else:
            break

    timeframe_vid_ids = grab_ids_in_date(
        target_date,
        full_playlist_items_list)

    vid_items_in_target_time = []
    query_vids(timeframe_vid_ids, vid_items_in_target_time)

    last_video_date_in_timeframe = get_oldest_date_in_response(
        vid_items_in_target_time
        )

    return [
        vid_items_in_target_time,
        original_response,
        last_video_date_in_timeframe]

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
        split_vid_list_query(list_of_vid_id_lists, target_list)


def split_vid_list_query(list_of_vid_id_lists, target_list):
    """Feeds a block of 50 video ids to api to query,
    due to max of 50 ids submitted per query
    all of which end up appended to vids_in_target_time dictionary"""
    for id_list in list_of_vid_id_lists:
        query_vids(id_list, target_list)


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

"""Module that handles all systems used to turn the targeted query list of
api results into the desired output"""

import math
import datetime

import pyinputplus as pyip

import save_results as save

live_now = datetime.datetime.now  # run as live_now()
LINE_STRING = "-" * 80  # Max width of template terminal is 80 chars

# Search option DEFAULTS and variables ---------------------------------------
ACCEPTED_SORTS = ["views", "title", "likes", "comments", "date"]
ACCEPTED_NUM_OF_RESULTS = ["1", "3", "5", "10"]
ACCEPTED_TIMEFRAMES = ["y", "s", "m", "w"]
ACCEPTED_ORDERS = ["desc", "asc"]

DEFAULT_STRING = 'Sort by Views and show top 3 results\n'
DEFAULT_SORT = "views"
DEFAULT_NUM_TO_OUTPUT = 3
DEFAULT_ORDER = "desc"

DEFAULT_SETTINGS = [
    DEFAULT_SORT,
    DEFAULT_NUM_TO_OUTPUT,
    DEFAULT_ORDER]


def output_loop(vids_in_target_time, org_resp, last_video_date):
    """Runs a default search first, for ease of use,
    then prompts the user if they want to sort the current results in
    timeframe differently, updates the sort settings and keeps going
    until user is done resorting and saving the results they want from
    that particular channel & timeframe"""
    settings = DEFAULT_SETTINGS
    keep_sorting = True
    while keep_sorting:
        output_results(
            vids_in_target_time,
            org_resp,
            last_video_date,
            settings
            )
        settings, keep_sorting = new_settings_prompt()


def new_settings_prompt():
    """gets the users consent to continue resorting results returned from query
    indicates to output_loop the users desire to keep resorting"""
    print('Would you like to sort these results differently?')
    yes_no = pyip.inputYesNo(prompt="Enter y/n \n", default="no")
    if yes_no == "yes":
        settings = select_new_sort_settings()
        keep_sorting = True
        return settings, keep_sorting
    else:
        settings = DEFAULT_SETTINGS
        keep_sorting = False
        return settings, keep_sorting


def select_new_sort_settings():
    """Querys the user on what sort of sorting they want to do
    validation with pyinputplus
    generates a new list of settings which it returns"""
    sort = pyip.inputMenu(
        ACCEPTED_SORTS,
        prompt="What way do you want to sort the results?\n",
        default="views",
        numbered=True)
    print(f'You chose: {sort}\n')

    num = pyip.inputMenu(
        ACCEPTED_NUM_OF_RESULTS,
        prompt="How many results do you want to display in this terminal?\n",
        default=5,
        lettered=True)
    print(f'You chose: {num}\n')

    num = int(num)

    order = pyip.inputMenu(
        ACCEPTED_ORDERS,
        prompt="How do you want to order them, Decending Or Ascending?\n",
        default="desc",
        numbered=True)
    print(f'You chose: {order}\n')

    new_settings = [sort, num, order]
    return new_settings


def output_results(
        vids_in_target_time,
        response,
        last_date,
        settings_list):
    """combines and formats the gathered data and then outputs it for the user.
    offers them a choice of saving the full result as a google drive link"""
    channel_title = vids_in_target_time[0]["channel"]
    total_channel_vids = response["pageInfo"]["totalResults"]
    total_vids_in_timeframe = len(vids_in_target_time)
    quota_used = get_credits_used(total_vids_in_timeframe)

    sort_by = settings_list[0]
    target_num_of_results = settings_list[1]
    order = settings_list[2]

    if order == "desc":
        vids_in_target_time.sort(
            key=lambda vid: vid[sort_by],
            reverse=True)
    else:
        vids_in_target_time.sort(
            key=lambda vid: vid[sort_by],
            reverse=False)

    output_header_string = make_header_string(
        total_channel_vids,
        total_vids_in_timeframe,
        last_date,
        quota_used,
        channel_title)

    terminal_output_results_string = make_terminal_results_string(
        output_header_string,
        sort_by,
        target_num_of_results,
        vids_in_target_time
        )

    print(terminal_output_results_string)
    print(LINE_STRING)
    print('Would you like to save the FULL list of the results to a txt file?')
    print('Enter y/n')
    yesno = pyip.inputYesNo(default="no")
    if yesno == "yes":
        full_output_string = make_full_results_string(
            vids_in_target_time,
            output_header_string
            )
        new_now = live_now().strftime("%Y-%m-%d-%H-%M-%S")
        filename = f'{new_now}-{channel_title}-{sort_by}'
        save.upload_txt_file_to_gdrive(full_output_string, filename)


# Output Components Functions ------------------------------------------------


def make_header_string(
        total_channel_vids,
        total_vids_in_timeframe,
        last_date,
        quota_used,
        channel_title):
    """Combines meta info for the search and makes a header string to
    go at the top of the result output. Returns the string"""

    output_header_list = []
    output_header_list.append(LINE_STRING)
    output_header_list.append(f'Channel Title: {channel_title}')
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
    sort_by,
    total_output_results,
    vids_in_target_time
):
    """Takes the defaults and strings needed to format results
    for the terminal and then combines them and returns it"""

    terminal_output_part_list = []

    settings = (
        f'Top {total_output_results} Results\nSorted by: {sort_by}'
        )
    output_results_list = []
    for video in vids_in_target_time[:total_output_results]:
        output_results_list.append(video["title"])
        output_results_list.append(
            f'Views: {video["views"]}, Published: {video["date"]}'
            )
        output_results_list.append(
            f'Likes: {video["likes"]}, Comments: {video["comments"]}'
            )
        output_results_list.append(f'{video["url"]}\n')
    terminal_output_results_string = "\n".join(output_results_list)

    terminal_output_part_list.append(output_header_string)
    terminal_output_part_list.append(settings)
    terminal_output_part_list.append(LINE_STRING)
    terminal_output_part_list.append(terminal_output_results_string)
    terminal_output_string = "\n".join(terminal_output_part_list)

    return terminal_output_string


def make_full_results_string(vids_in_target_time, output_header_string):
    """Takes the defaults and strings needed to format results for the full
    list of results and then combines them and returns it"""
    output_results_list = []

    for video in vids_in_target_time:
        output_results_list.append(video["title"])
        output_results_list.append(
            f'Views: {video["views"]}, Published: {video["date"]}'
            )
        output_results_list.append(f'{video["url"]}\n')
    full_output_results_string = "\n".join(output_results_list)

    full_output_part_list = []
    full_output_part_list.append(output_header_string)
    full_output_part_list.append(full_output_results_string)
    full_output_string = "\n".join(full_output_part_list)

    return full_output_string


def get_credits_used(total_videos):
    """takes a int of total videos returned from query
    returns the amount of api quota credits it took to get.
    Current implementation is for every query that results in
    up to 50 videos (max batch size), two quota points are used."""

    quota_credits_used = math.ceil((total_videos / 50)) * 2
    return quota_credits_used

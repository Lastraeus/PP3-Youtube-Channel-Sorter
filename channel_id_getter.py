"""Module handles initial screen and user prompts
functions here take the inputted url, validates it works with pytube
then takes the users choice of timeframe.
funcs in this module return the correct date from the
selected timeframe to then pass out of the module"""
import datetime

import pytube  # specifically https://github.com/felipeucelli/pytube.git
from dateutil.relativedelta import relativedelta
from dateutil import parser

import output_system as out


SAMPLE_RETURN_DATE = parser.parse("2022-09-19T18:08:46Z")
# used to get correct timezone for comparison
# (Taken from test qurey result)


def get_valid_channel_id():
    """Runs a loop testing user inputs against pytube for
    valid channel urls, returns a valid id for a channel's
    playlist of all their videos"""
    channel_playlist_id = None
    while channel_playlist_id is None:
        channel_playlist_id = channel_prompt()

    return channel_playlist_id


def get_target_date():
    """Keeps prompting the user until a valid selection of a timeframe
    returns a date conversion of that timeframe"""
    target_date = None
    while target_date is None:
        target_date = timeframe_prompt()

    target_date = date_format_to_google_dates(
        target_date,
        SAMPLE_RETURN_DATE)
    return target_date


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

    # TODO dive into pytube2 code to see if we can deal with all possible
    # exceptions that their channel.channel_id can throw
    except Exception:
        print("That is not a valid YouTube Channel URL")


def timeframe_prompt():
    """Asks the user to select a valid timeframe.
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


def date_format_to_google_dates(target_date, sample_date):
    """converts a standard datetime object to the timezone format
    that google api results return in"""
    # https://appdividend.com/2023/01/
    # 07/typeerror-cant-compare-offset-naive-and-offset-aware-datetimes/
    target_date_tz = target_date.astimezone(sample_date.tzinfo)
    return target_date_tz

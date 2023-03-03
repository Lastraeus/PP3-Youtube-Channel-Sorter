"""
Runs and organizes the main operations of the YouTube Channel Sorter App.
Handles welcome screen, initial user prompts,
Passes the results to output_system.py for
final outputting."""

from ascii import LOGO
import query_youtube as yt
import output_system as out

# Begin and End Functions Section --------------------------------------------


def restart_instructions():
    """tells the user if they would like to search again,
    to hit the run button again."""
    print('If you want to run another search,')
    print("just hit the run button up top!\n")
    print("Goodbye!")
    exit()


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

# main() func section --------------------------------------------------------


def main():
    """Holds main program loop. Runs welcome screen,
    then calls yt.main_search then moves to output,
    then instructs the user how to run another search then
    exits.
    Also includes a CTRL C handle message,
    since people really really want to use that for copy pasting"""
    try:
        while True:
            print_initial_screen()

            vid_items_in_target_time = None
            original_response = None
            last_video_date_in_timeframe = None

            response_data_objects = []
            response_data_objects = yt.main_search()

            vid_items_in_target_time = response_data_objects[0]
            original_response = response_data_objects[1]
            last_video_date_in_timeframe = response_data_objects[2]

            out.output_loop(
                vid_items_in_target_time,
                original_response,
                last_video_date_in_timeframe)

            restart_instructions()

    except KeyboardInterrupt:
        print("Unfortuneatly Ctrl-C is the shortcut to exit this template.")
        print("Please run again.")


if __name__ == "__main__":
    main()

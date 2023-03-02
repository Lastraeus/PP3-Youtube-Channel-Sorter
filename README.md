# Cian's Code Institute Final Grade Calculator - PP2:

## [Link to live website](https://youtube-channel-sorter.herokuapp.com/)

## __Purpose of the Project__
To create a terminal based app using Python that prompts the user to input a YouTube channel url and then receive back an output of the videos on that channel, sorted by most popular on a certain timeframe, such as a year.

Youtube does not by default allow you to see a channel's top videos within a certain timeframe. You can only sort by;

    "Most recent" 
    
  which requires you to comb through the list yourself for videos with views more than average for that period

and

    "Most Popular" 
  which will sort every video on their channel back to it's inception, by views. The problem being that videos from way back often by default have many more views than more recent ones.

The purpose of this project, is to be able to query this application and have it (however slowly) automate this process of searching for you.

## __Research__
__Understanding the Target Problem__

Initially I investigated the official google API qutoas for searching with a given api key were quite strict.
https://developers.google.com/youtube/v3/determine_quota_cost
You are only allowed 100 "searches" a day which was possibly too strict for this projects needs during development. I then found https://stackoverflow.com/questions/18953499/youtube-api-to-fetch-all-videos-on-a-channel

and

https://stackoverflow.com/questions/74348727/youtube-data-api-get-channel-by-handle

which led me to piece together a plan of using the official api using the "lists" query, instead, of which you get 10,000 querys per api key, instead of 100. Possibly with a slower pytube version as a backup.

I also investigated using this branch of pytube
https://github.com/felipeucelli/pytube
which had been updated to handle the newwer @youtube handles.
So basic testing of this showed that it was working but quite slow to parse all videos in a channel (it doesn't use a official api query), but it's channel url parsing into channel ID functionality was undeniable.

Also looked at were

yt-dlp
https://github.com/yt-dlp/yt-dlp

and 

https://github.com/alexmercerind/youtube-search-python which was deprecated for over 8 months

__Audience Needs/Stories__

'It's really unfortunate that google doesn't let you sort like Reddit does within a channel'

'When a channel has been running for years, I wish I could sort by the best of their more "modern" videos.'

'You can sometimes do it by searching the channel name in youtubes own search and using their filters, but often times it gets contaminated with other channels results and playlists instead of videos, or often the search is just plain missing lots of the videos' see https://www.youtube.com/results?search_query=%40bbcnews&sp=CAMSAggF compared to looking at https://www.youtube.com/@BBC/videos

__Search For Similar Apps__
see above for now - TBD
## __Planning__
I  planned a version of the app hosted on heroku using the Code Institute template for the terminal.

The terminal app when run would offer a help page, that could be accessed with "h" and then prompt the user.

This would wait for the user to enter a channel name, and optionally, a timeframe in weeks, months or years. and then return the top 5 or so results sorting by most popular(views) in that timeframe

### __Color Scheme__
Color Scheme tbd after initial testing.





## __Features__
TBD

### __Technology Used__
TBD

### __Possible Future Features to Implement__
Ideas for future possible features include;

TBD


## __Testing__
### __General Testing Process__
TBD
### __Hardware__
TBD
### __Software__
TBD

### __Validator Testing__
TBD


### __Bugs Encountered__
 __1.__ 

TBD


### __Unfixed Bugs__
NA

## __Deployment__

## __Credits__
Query template from https://medium.com/mcd-unison/youtube-data-api-v3-in-python-tutorial-with-examples-e829a25d2ebd#5999

datetime #1 https://java2blog.com/check-if-date-is-greater-than-today-python/

datetime #2 https://stackoverflow.com/questions/63513596/python-get-same-day-last-year

datetime #3 https://stackoverflow.com/questions/546321/how-do-i-calculate-the-date-six-months-from-the-current-date-using-the-datetime

datetime #4 https://appdividend.com/2023/01/07/typeerror-cant-compare-offset-naive-and-offset-aware-datetimes/

replacing the C in Channel ID with U so that it becomes the all channel videos playlist
https://stackoverflow.com/questions/41752946/replacing-a-character-from-a-certain-index

main func reference https://realpython.com/python-main-function/

switch statement for timeframe choice https://www.freecodecamp.org/news/python-switch-statement-switch-case-example/

itemgetter https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-a-value-of-the-dictionarygit 

get views https://github.com/CoreyMSchafer/code_snippets/blob/master/Python/YouTube-API/03-Most-Popular-Video-Playlist/start.py

handle api errors https://stackoverflow.com/questions/23945784/how-to-manage-google-api-errors-in-python


divide list into chunks (for video querys using vidID lists more than 50 items long) https://www.geeksforgeeks.org/break-list-chunks-size-n-python/

playlist not found and other error handling https://stackoverflow.com/questions/23945784/how-to-manage-google-api-errors-in-python

textfile https://www.pythontutorial.net/python-basics/python-create-text-file/

make output as one string for writing to file or printing
https://flexiple.com/python/python-append-to-string/

check type is list not json https://www.geeksforgeeks.org/python-type-function/

leading zeros for output https://www.delftstack.com/howto/python/python-leading-zeros/

pydrive2 for permission sharing https://docs.iterative.ai/PyDrive2/filemanagement/#insert-permissions

use service account https://github.com/iterative/PyDrive2/issues/21

pyinputplus https://pypi.org/project/PyInputPlus/

upload to drive from existing file https://harshmaur.com/how-to-use-pydrive2-to-upload-a-file-to-google-drive-folder

refference for basic pydrive2 use https://stackoverflow.com/questions/46562255/python-upload-my-own-files-into-my-drive-using-pydrive-library

RE linter warning about missing dynamically created attribute on google service api call https://stackoverflow.com/questions/35990313/avoid-pylint-warning-e1101-instance-of-has-no-member-for-class-with-dyn/54156144#54156144

### __Content__
__Text Content__


__Code__


__Colors__
__Misc syntax reference etc:__

### __Media__

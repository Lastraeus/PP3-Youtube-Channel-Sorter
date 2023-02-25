# Cian's Code Institute Final Grade Calculator - PP2:

## [Link to live website - TODO]()

## __Purpose of the Project__
To create a terminal based app using Python that prompts the user to input a YouTube channel url and then receive back an output of the videos on that channel, sorted by most popular on a certain timeframe, such as a year.

Youtube does not by default allow you to see a channel's top videos within a certain timeframe. You can only sort by;

    "Most recent" which requires you to comb through the list yourself for videos with views more than average for that period

and

    "Most Popular" which will sort every video on their channel back to it's inception, by views. The problem being that videos might be unfairly biased with higher views.

The purpose of this project, is to be able to query this application and have it (however slowly) automate this process of searching for you.

## __Research__
__Understanding the Target Problem__

Initially I investigated the official google API qutoas for searching with a given api key were quite strict.
https://developers.google.com/youtube/v3/determine_quota_cost
You are only allowed 100 searches a day which was possibly too strict for this projects needs during development. I then found https://stackoverflow.com/questions/18953499/youtube-api-to-fetch-all-videos-on-a-channel

and

https://stackoverflow.com/questions/74348727/youtube-data-api-get-channel-by-handle

which led me to piece together a plan of using the official api. Possibly with a slower pytube version as a backup.

I also investigated using this branch of pytube
https://github.com/felipeucelli/pytube
which had been updated to handle the newwer @youtube handles.
So basic testing of this showed that it was working but quite slow.

Also looked at were

yt-dlp
https://github.com/yt-dlp/yt-dlp

and 

https://github.com/alexmercerind/youtube-search-python which was deprecated for over 8 months

![Official Calculation Weights and rules](docs/readme-images/target-rules-from-official-assessment-guide.png)

__Audience Needs/Stories__

"It's really unfortunate that google doesn't let you sort like Reddit does within a channel"

__Search For Similar Apps__
see above for now - TBD
## __Planning__
I  planned a version of the app hosted on heroku using the Code Institute template for the terminal.

The terminal app when run would offer a help page, that could be accessed with "h" and then prompt the user.

This would wait for the user to enter a channel name, and optionally, a timeframe in weeks, months or years. and then return the top 5 or so results sorting by most popular(views) in that timeframe

### __Color Scheme__
Color Scheme tbd after initial testing.

  ![Coolor Website palette](docs/readme-images/coolors-color-palette.png)



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
### __Content__
__Text Content__


__Code__


__Colors__
__Misc syntax reference etc:__

### __Media__

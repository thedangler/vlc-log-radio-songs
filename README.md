# VLC No UI Spotify sync
Adds songs that are being played from an internet radio station to spotify playlist.
- Internet radio station must change the metadata for the artist and song for it to work.

#helloworld hexchat show current playing song in vlc.



# vlc-log-radio-songs - Windows Only
Log all the songs playing to excel and and them to Spotify playlist

# Why?
Began as a test to see how to use xlwings. I came up with a fun problem to solve and it snowballed from there

# Setup VLC
Open vlc and goto Tools -> Preferences

Show Setting - Choose All

In interfaces click on Main interface - Check Web make sure http is written out in the box

Expand Main interfaces choose Lua.

Lua HTTP - put in a password and source directory. Mine is C:\Program Files (x86)\VideoLAN\VLC\lua\http

Check off Directory index

Save

It should work and you can test it by going to: http://localhost:8080/requests/status.xml

Fire up a internet radio and start logging songs

Comment out xlwings code if you dont want to use excel to log music.

## Note: the station I listen to sends out a string of artist - song name , your station maybe different and the parser may need to change.

Don't forget to update the config.py file with your informaiton.

#### TODO
* Clean up code - if else indents
* Search for duplicates in the DB - Done in VLC No UI
* Log songs to excel and DB at the end after attempting to add to spotify
* Move filters to DB pre load from config.
* Remove xlwings and make csv file instead
* Test on other platforms

# vlc-log-radio-songs
Using vlc http server i'm logging all the songs that play on the internet radio station I listen to

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

## Note: the station I listen to sends out a string of artist - song name , your staytion maybe different and the parser may need to change.
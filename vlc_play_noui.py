import vlc
import config
import time
import requests
import sys
#wtf same as console ???
print('Python %s' % (sys.executable))

current_song = ''

def callback(event,player):
    global current_song
    m = player.get_media()

    if current_song != m.get_meta(vlc.Meta.NowPlaying):
        current_song = m.get_meta(vlc.Meta.NowPlaying)
        print("\rSong changed:  %s" % current_song,end='')

instance = vlc.Instance()
player_l = instance.media_list_player_new()
media = instance.media_list_new([r'C:\Users\mhebel3\Downloads\listen.pls'])
player_l.set_media_list(media)
player_l.play() # starts vlc in the background and plays the music
time.sleep(2)
p = player_l.get_media_player() # get the media player
m = p.get_media()

print(m.get_meta(vlc.Meta.NowPlaying))
current_song = m.get_meta(vlc.Meta.NowPlaying)
event_m = m.event_manager()
event_m_p = p.event_manager()

#event_m_p.event_attach(vlc.EventType.MediaPlayerTitleChanged,callback,p)
#event_m.event_attach(vlc.EventType.MediaMetaChanged,callback)
#event_m.event_attach(vlc.EventType.MediaParsedChanged,callback_m,m)
event_m_p.event_attach(vlc.EventType.MediaPlayerTimeChanged,callback,p) # stupid, don't want to use this one but its the only call back triggered
#event_m.event_attach(vlc.EventType.MediaStateChanged,callback)

input()






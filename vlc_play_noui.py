import vlc
import config
import time
import requests
import sys
print('Python %s' % (sys.executable))
import spotipy
import spotipy.util as util
import sqlite3

current_song = None


def filter(artist):
    filter_artist = ['Split Infinity Radio', 'The Voice of Crom House Band', 'Wasabi Speaks']
    if artist in filter_artist:
        return True
    else:
        return False

def is_duplicate(song,artist):
    try:
        conn = sqlite3.connect('music.db')
        c = conn.cursor()
        c.execute("select count(*) from music where artist = ? and song = ? and spotify = 0", (artist,song))
        (has_song,) = c.fetchone()
        return has_song == 1
        conn.close()
    except:
        print(' | Not Added to DB')
        return False

def callback(event,player):
    global current_song
    m = player.get_media()
    if current_song != m.get_meta(vlc.Meta.NowPlaying):
        current_song = m.get_meta(vlc.Meta.NowPlaying)
        if current_song is None:
            return
        artist, song = current_song.split('-', 1)

        artist = artist.strip()
        song = song.strip()

        if is_duplicate(song, artist) == False and filter(artist) == False:
            spotifyLookup(artist, song)

def spotifyAuth(username):
    scope = 'playlist-modify-private user-library-read playlist-modify-public'
    token = util.prompt_for_user_token(username, scope, config.SPOTIPY_CLIENT_ID,
                                       config.SPOTIPY_CLIENT_SECRET, config.SPOTIPY_REDIRECT_URI)
    return token

def addToPlaylist(track_id):
    token = spotifyAuth(config.SPOTIFY_USER_NAME)
    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        results = sp.user_playlist_add_tracks(config.SPOTIFY_USER_NAME, config.SPOTIFY_PLAYLIST_ID, [track_id])
        if results.get('snapshot_id',False):
            return True
        else:
            return False
    else:
        print(" | Spotify - Can't get token")


def spotifyLookup(artist,song):

    token = spotifyAuth(config.SPOTIFY_USER_NAME)
    if token:
        sp = spotipy.Spotify(auth=token)
        search_str = "artist:%s track:%s" % (artist,song)
        result = sp.search(search_str,limit=1,type='track')
        if len(result['tracks']['items']) > 0:
            if addToPlaylist(result['tracks']['items'][0]['id']):
                try:
                    conn = sqlite3.connect('music.db')
                    c = conn.cursor()
                    c.execute("insert into music values (?,?,?,?,?,?)", (artist, song, 0, 0,'Matt', 1))
                    conn.commit()
                    conn.close()
                except:
                    print(' | Not Added to DB')
                print("\n %s - %s  Added to Spotify Playlist" % (artist,song))
        else:
            print("\n Spotify - Track not found")
    else:
        print("\n Spotify - Can't get token")

instance = vlc.Instance()
player_l = instance.media_list_player_new()
media = instance.media_list_new([r'D:\Users\mhebel3\Downloads\listen.pls'])
player_l.set_media_list(media)
player_l.play() # starts vlc in the background and plays the music
p = player_l.get_media_player()


p = player_l.get_media_player() # get the media player
m = p.get_media()

event_m = m.event_manager()
event_m_p = p.event_manager()

#event_m_p.event_attach(vlc.EventType.MediaPlayerTitleChanged,callback,p)
#event_m.event_attach(vlc.EventType.MediaMetaChanged,callback,p)
#event_m.event_attach(vlc.EventType.MediaParsedChanged,callback_m,m)
event_m_p.event_attach(vlc.EventType.MediaPlayerTimeChanged,callback,p) # stupid, don't want to use this one but its the only call back triggered
#event_m.event_attach(vlc.EventType.MediaStateChanged,callback)

q = 1
mute = False
while q == 1:

    cmd = input("Enter a command: play,pause,quit(q),mute: ")
    if cmd == "q" or cmd == "quit":
        q = 0
    elif cmd == "play":
        p.play()
    elif cmd == "pause":
        p.pause()
    elif cmd == "mute":
        mute = not mute
        if mute:
            p.audio_set_volume(0)
        else:
            p.audio_set_volume(60)

    else:
        pass

exit(1)






# Made by Matt H
# TODO clean up code - if else indents
# TODO Search for duplicates in the DB
# TODO Log songs to excel and DB at the end after attempting to add to spotify
# TODO move filters to DB pre load from config.

from __future__ import print_function
import requests
from xml.etree import ElementTree
from html.parser import HTMLParser
import html
import xlwings as xw
import time
import sqlite3
import datetime
import spotipy
import spotipy.util as util
import config
import pywinauto



print('Getting songs:')

#put in the database
filter_artist = ['Split Infinity Radio','The Voice of Crom House Band','Wasabi Speaks']

def getInfo():

    s = requests.Session()
    s.auth = ('', 'test')
    r = s.get('http://localhost:8080/requests/status.xml', verify=False)

    parser = HTMLParser()

    root = ElementTree.fromstring(r.text)
    now_playing = root.find("./information/category[@name='meta']/info[@name='now_playing']").text
    now_playing = html.unescape(now_playing).strip()
    msg = ''
    try:
        artist,song = now_playing.split('-',1)
        artist = artist.strip()
        song = song.strip()
        msg = logSong(artist, song)
    except:
        msg = 'Wrong name format for song %s' % now_playing
    finally:
        print('\r'+msg,end='')
    if 'Added' in msg:
        spotifyLookup(artist,song)
        return True
    else:
        return False

def filter(artist):
    global filter_artist
    if artist in filter_artist:
        return True
    else:
        return False

def logSong(artist,song,own=False,downloaded=False,added_by = 'Matt'):
    b = xw.Book('C:\\Users\\mhebel3\\Documents\\Music\\music.xls')
    sheet = b.sheets['Sheet1']

    if checkDuplicates(sheet,artist,song):
        return '%s - %s | Duplicate' % (artist,song)
    if filter(artist):
        return '%s filtered out' % artist

    nextrow = sheet.range('A1').current_region.last_cell.row
    sheet.range('A1:E1').offset(nextrow).value = [artist,song,own,downloaded,added_by]

    try:
        conn = sqlite3.connect('music.db')
        c = conn.cursor()
        c.execute("insert into music values (?,?,?,?,?,?)", (artist,song,0,0,added_by,0))
        conn.commit()
        conn.close()
    except:
        print(' | Not Added to DB')

    return '%s - %s | Added' % (artist,song)

def checkDuplicates(sheet,artist,song):
    last_row = sheet.range('A1').current_region.last_cell.row
    last_cell = 'A2:E%s' % (last_row)
    song_list = sheet.range(last_cell).value
    for item in song_list:
        if(item[0] == artist and item[1] == song):
            return True
    return False

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
        #"spotify:user:thedangler:playlist:1U8C7xJVJ6nlP5OXxnVPAA"


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
                    c.execute("update music set spotify = 1 where artist = ? and song = ?", (artist, song))
                    conn.commit()
                    conn.close()
                except:
                    print(' | Could not update DB')
                print(" | %s - %s  Added to Spotify Playlist" % (artist,song))
        else:
            print(" | Spotify - Track not found")
    else:
        print(" | Spotify - Can't get token")

# does the authentication
# TODO do error checking in here
def spotifyAuth(username):
    scope = 'playlist-modify-private user-library-read'
    token = util.prompt_for_user_token(username, scope, config.SPOTIPY_CLIENT_ID,
                                       config.SPOTIPY_CLIENT_SECRET, config.SPOTIPY_REDIRECT_URI)
    return token

while True:
    getInfo()
    time.sleep(60)
    if datetime.datetime.now().time().hour == config.HOUR_TO_STOP:
        try:
            # close vlc player automatically and then exit the program.
            p = pywinauto.application.Application()
            w_handle = pywinauto.findwindows.find_windows(title_re=r'.* VLC media player')[0]
            window = p.window_(handle=w_handle)
            window.Close()
        except:
            pass
        exit()




from __future__ import print_function
import requests
from xml.etree import ElementTree
from html.parser import HTMLParser
import xlwings as xw
import time
import sqlite3
import datetime
import sys
import spotipy
import spotipy.util as util
import config



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
    now_playing = parser.unescape(now_playing)
    msg = ''
    try:
        artist,song = now_playing.split('-',1)
        artist = artist.strip()
        song = song.strip()
        msg = logSong(artist, song)

    except:
        msg = 'Wrong name format'
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

    conn = sqlite3.connect('music.db')
    c = conn.cursor()
    c.execute("insert into music values (?,?,?,?,?)", (artist,song,0,0,added_by))
    conn.commit()
    conn.close()

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
    scope = 'playlist-modify-public'
    token = util.prompt_for_user_token('thedangler', scope)
    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        results = sp.user_playlist_add_tracks('thedangler', '1U8C7xJVJ6nlP5OXxnVPAA', [track_id])
        print(results)
    else:
        print("Can't get token")
        #"spotify:user:thedangler:playlist:1U8C7xJVJ6nlP5OXxnVPAA"


def spotifyLookup(artist,song):
    scope = 'user-library-read'
    username = 'thedangler'
    token = util.prompt_for_user_token(username,scope,config.SPOTIPY_CLIENT_ID,config.SPOTIPY_CLIENT_SECRET,config.SPOTIPY_REDIRECT_URI)
    if token:
        sp = spotipy.Spotify(auth=token)
        search_str = "artist:%s track:$s" % (artist,song)
        result = sp.search(search_str,limit=1,type='track')
        if len(result['tracks']['items']) > 0:
            addToPlaylist(result['tracks']['items'][0]['id'])
    else:
        print("Can't get token")

while True:
    getInfo()
    time.sleep(60)
    if datetime.datetime.now().time().hour == 18:
        exit()




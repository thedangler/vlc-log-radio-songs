from __future__ import print_function
import requests
from xml.etree import ElementTree
from HTMLParser import HTMLParser
import xlwings as xw
import time
import sqlite3

print('Getting songs:')

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
        artist,song = now_playing.split('-')
        artist = artist.strip()
        song = song.strip()
        msg = logSong(artist, song)

    except:
        msg = 'Wrong name format'
    finally:
        print('\r'+msg,end='')

def filter(artist):
    if artist in ['Split Infinity Radio']:
        return True
    else:
        return False

def logSong(artist,song,own=False,downloaded=False,added_by = 'Matt'):
    b = xw.Book('C:\\Users\\mhebel3\\Documents\\music.xls')
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

while True:
    getInfo()
    time.sleep(60)

from __future__ import print_function
import requests
import hexchat
import time
from html.parser import HTMLParser
from xml.etree import ElementTree


__module_name__ = "VLC Now Playing"
__module_version__ = "1.0"
__module_description__ = "Shows the curent playing song in an open VLC session. Other VLC settings need to be setup for this to work"

current_song = ""

print("Prints out the current playing song in VLC every 90 seconds")

def getVLCSong():
    s = requests.Session()
    s.auth = ('', 'password')
    r = s.get('http://localhost:8080/requests/status.xml', verify=False)
    if r.status_code == 200:
        parser = HTMLParser()
        root = ElementTree.fromstring(r.text)
        now_playing = root.find("./information/category[@name='meta']/info[@name='now_playing']").text

        return now_playing

    return False


def showsong_cb(userdata):
    global current_song
    song = getVLCSong()
    if current_song != song:
        #hexchat.command('me is listening to ' + song)
        print('Currently playing ' + song)
        current_song = song

    return 1

myhook = hexchat.hook_timer(90000, showsong_cb)

#!/usr/bin/env python
import appscript
import subprocess
import os
import sqlite3 as lite
import sys
import time

CONST_FF_PROFILE_PATH = "/Users/Oli/Library/Application Support/Firefox/Profiles/lls08fma.default-1425635353616/places.sqlite"
CONST_URL = "youtube.com"
CONST_APPLESCRIPT = """osascript -e 'tell application "System Events" to tell process "YouTube to MP3" to click menu item "Paste url" of menu 1 of menu bar item "File" of menu bar 1'"""

#Returns list of URLs sorted by window
def chrome_get_data():
	return appscript.app('Google Chrome').windows.tabs.URL.get()

#Returns the first URL to match CONST_URL
def chrome_get_link():
	for window in combURL[::-1]:
		for url in window:
			if url.find(CONST_URL) != -1:
				return url


#Returns a list of browsing history tuples (date, url) sorteds old to new
def ff_get_data(path): #Returns the browsing history as a two dimensional array
	con = lite.connect(path)
	cur = con.cursor()
	cur.execute("SELECT datetime(moz_historyvisits.visit_date/1000000,'unixepoch'), moz_places.url FROM moz_places, moz_historyvisits WHERE moz_places.id = moz_historyvisits.place_id")
	data = cur.fetchall()
	return data

#Returns the most recent URL that matches CONST_URL
def ff_get_link(data):
	for (date,url) in reversed(data):
		if(url.find(CONST_URL) != -1):
			return url

data = ff_get_data(CONST_FF_PROFILE_PATH)
url = ff_get_link(data)
#Write url to clipboard
copy = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE) 
copy.stdin.write(url)

#Use AppleScript to paste url into YouTube to MP3
os.system("""osascript -e 'tell application "System Events" to tell process "YouTube to MP3" to click menu item "Paste url" of menu 1 of menu bar item "File" of menu bar 1'""")
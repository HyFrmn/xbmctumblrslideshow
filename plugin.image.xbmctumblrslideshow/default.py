#!/usr/bin/env python
import sys
import urllib2
import json
import ConfigParser
import xbmcgui
import xbmcaddon
import os
__settings__ = xbmcaddon.Addon(id='script.image.lastfm.slideshow')
__language__ = __settings__.getLocalizedString
lib = os.path.join(__settings__.getAddonInfo('path'), 'Resources', 'lib')
sys.path.append(lib)

print sys.path
from xbmcapi import XBMCSourcePlugin

config = ConfigParser.ConfigParser()
config.read(os.path.join(__settings__.getAddonInfo('path'),'config.txt'))

#Use old API key if one is not found
try:
	API_KEY = config.get('API','key')
except (ConfigParser.NoSectionError ,ConfigParser.NoOptionError) as e:
	API_KEY = 'x1XhpKkt9qCtqyXdDEGHp5TCDQ1TOWm2VTLiWUm0FHpdkHI5Rj'
	pass

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)


plugin = XBMCSourcePlugin()

def catagories():	
#Use settings from menu if nothing is found in the config file
	try:	
		cats = config.get('blogs','blog_name').split(',')
	except (ConfigParser.NoSectionError ,ConfigParser.NoOptionError) as e:
		cats = [c.strip() for c in plugin.getSetting('tumblrs').split()]
		pass

	for cat in cats:
		thumbnail = 'http://api.tumblr.com/v2/blog/%s.tumblr.com/avatar/256' % cat
		listitem = xbmcgui.ListItem(cat, iconImage=thumbnail)
		ok = plugin.addDirectoryItem(url='%s/%s' % (plugin.root, cat), listitem=listitem, isFolder=True)
	plugin.endOfDirectory()

urls = []
def listimages(tumblr):
	print tumblr
	start = int(plugin.query.get('start',0))
	url = 'http://api.tumblr.com/v2/blog/%s.tumblr.com/posts/photo?api_key=%s&offset=%d' % (tumblr, API_KEY, start)
	print 'URL:', url
	fd = urllib2.urlopen(url)
	dom = json.load(fd)
	fd.close()

	posts = dom['response']['posts']
	if len(posts) >= 20:
		thumbnail = 'http://api.tumblr.com/v2/blog/%s.tumblr.com/avatar/256' % tumblr
		listitem = xbmcgui.ListItem('Next Page (%d - %d)' % (start + 20, start + 40), iconImage=thumbnail)
		url = plugin.root + plugin.path + '?start=' + str(start + 20)
		plugin.addDirectoryItem(url=url, listitem=listitem,isFolder=True)
	post_index = start
	for post in posts:
		index = 1
		children = [photo['alt_sizes'][0] for photo in post['photos']]
		for tag in children:
			if len(children) > 1:
				label = 'Post %d - %d' % (post_index, index)
			else:
				label = 'Post %d' % (post_index)
			listitem = xbmcgui.ListItem(label)
			url = tag['url']
			if (url in urls):
				continue
			print 'URL:', url
			plugin.addDirectoryItem(url=url, listitem=listitem)
			index += 1
		post_index += 1
	plugin.endOfDirectory()

if plugin.path:
	tumblr = plugin.path.split('/')[0]
	listimages(tumblr)
else:
	catagories()
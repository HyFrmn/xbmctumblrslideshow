#!/usr/bin/env python
import re
import urllib2
from xml.dom.minidom import parse

import xbmc
import xbmcgui
import xbmcplugin

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

TUMBLR_THUMB = 'https://si0.twimg.com/profile_images/2020829304/t.png'

class XBMCPlugin(object):
	def __init__(self):
		self.root = re.match(r'plugin:\/\/[A-Za-z0-9_.-]+\/', sys.argv[0]).group(0)
		self.path = sys.argv[0].replace(self.root,'').split('?')[0]
		self.query = {}
		if '?' in sys.argv[2]:
			query = sys.argv[2][1:].split('&')
			for q in query:
				k, v = q.split('=')
				self.query[k] = v
		self.id = int(sys.argv[1])

	def getSetting(self, setting):
		return xbmcplugin.getSetting(self.id, setting)

	def endOfDirectory(self):
		xbmcplugin.endOfDirectory(self.id)

	def addDirectoryItem(self, url, listitem=None, isFolder=False):
		return xbmcplugin.addDirectoryItem(handle=self.id, url=url, listitem=listitem, isFolder=isFolder)


plugin = XBMCPlugin()

print 'sys.argv:', sys.argv
paths = sys.argv[0].replace('plugin://plugin.image.xbmctumbl/','').split('/')

def catagories():
	cats = [c.strip() for c in plugin.getSetting('tumblrs').split()]
	for cat in cats:
		listitem = xbmcgui.ListItem(cat, iconImage="DefaultFolder.png")
		ok = plugin.addDirectoryItem(url='plugin://plugin.image.xbmctumbl/%s' % cat, listitem=listitem, isFolder=True)
	plugin.endOfDirectory()

urls = []
def listimages(tumblr):
	print tumblr
	start = int(plugin.query.get('start',0))
	url = 'http://%s.tumblr.com/api/read?start=%d' % (tumblr, start)
	print 'URL:', url
	fd = urllib2.urlopen(url)
	dom = parse(fd)
	fd.close()

	post_tags = dom.getElementsByTagName('post')
	photo_tags = dom
	if len(post_tags) >= 20:
		listitem = xbmcgui.ListItem('Next Page...')
		url = plugin.root + plugin.path + '?start=' + str(start + 20)
		plugin.addDirectoryItem(url=url, listitem=listitem,isFolder=True)
	post = start
	for post_tag in post_tags:
		post_name = post_tag.getAttribute('slug')
		index = 1
		children = [tag for tag in post_tag.getElementsByTagName('photo-url') if tag.getAttribute('max-width') == '1280']
		for tag in children:
			if len(children) > 1:
				label = 'Post %d - %d' % (post, index)
			else:
				label = 'Post %d' % (post)
			listitem = xbmcgui.ListItem(label)
			url = getText(tag.childNodes)
			if (url in urls):
				continue
			print 'URL:', url
			plugin.addDirectoryItem(url=url, listitem=listitem)
			index += 1
		post += 1
	plugin.endOfDirectory()

if plugin.path:
	tumblr = paths[0]
	listimages(tumblr)
else:
	catagories()
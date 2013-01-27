#!/usr/bin/env python
import xbmc
import xbmcgui
import xbmcplugin

import urllib2

from xml.dom.minidom import parse

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

TUMBLR_THUMB = 'https://si0.twimg.com/profile_images/2020829304/t.png'

class XBMCAPI(object):
	def __init__(self, id):
		self.id = int(id)

	def getSetting(self, setting):
		return xbmcplugin.getSetting(self.id, setting)

	def endOfDirectory(self):
		xbmcplugin.endOfDirectory(self.id)

	def addDirectoryItem(self, url, listitem=None, isFolder=False):
		return xbmcplugin.addDirectoryItem(handle=self.id, url=url, listitem=listitem, isFolder=isFolder)


xbmcapi = XBMCAPI(sys.argv[1])

print sys.argv
paths = sys.argv[0].replace('plugin://plugin.image.xbmctumbl/','').split('/')

def catagories():
	cats = [c.strip() for c in xbmcapi.getSetting('tumblrs').split()]
	print 'CATS:', xbmcapi.getSetting('tumblrs')
	for cat in cats:
		listitem = xbmcgui.ListItem(cat, iconImage="DefaultFolder.png")
		ok = xbmcapi.addDirectoryItem(url='plugin://plugin.image.xbmctumbl/%s' % cat, listitem=listitem, isFolder=True)
	xbmcapi.endOfDirectory()

def listimages(tumblr):
	print tumblr
	url = 'http://%s.tumblr.com/api/read' % tumblr
	print url
	fd = urllib2.urlopen(url)
	dom = parse(fd)
	fd.close()

	photo_tags = dom.getElementsByTagName('photo-url')
	index = 0
	for tag in photo_tags:
		if tag.getAttribute('max-width') != '1280':
			continue
		listitem = xbmcgui.ListItem('Image %d' % index)
		url = getText(tag.childNodes)
		print 'URL:', url
		xbmcapi.addDirectoryItem(url=url, listitem=listitem)
		index += 1
	xbmcapi.endOfDirectory()

if paths[0]:
	print 'PATHS:', paths
	tumblr = paths[0]
	listimages(tumblr)
else:
	catagories()
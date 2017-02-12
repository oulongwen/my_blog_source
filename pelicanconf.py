#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Longwen Ou'
SITENAME = "Longwen's Blog"
SITEURL = 'http://localhost:8000'

SITELOGO = '/images/profile.jpg'
BROWSER_COLOR = '2196F3'

PATH = 'content'

TIMEZONE = 'America/New_York'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
THEME = '/Users/oulongwen/WebDev/projects/my-theme/Flex'

MAIN_MENU = True

# Blogroll
#LINKS = (('Pelican', 'http://getpelican.com/'),
#         ('Python.org', 'http://python.org/'),
#         ('Jinja2', 'http://jinja.pocoo.org/'),
#         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('github', 'https://github.com/oulongwen'),
          ('stack-overflow', 'http://stackoverflow.com/users/7187106/longwen-ou'),)


# Menu items
MENUITEMS = (('Archives', '/archives.html'),
             ('Categories', '/categories.html'),
			 ('Tags', '/tags.html'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

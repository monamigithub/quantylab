#!/usr/bin/env python
# -*- coding: utf-8 -*- #
import os
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
now = datetime.datetime.now()

AUTHOR = '김문권'
SITEURL = 'https://quantylab.github.io'
SITENAME = 'QuantyLab'
SITETITLE = SITENAME
SITESUBTITLE = '퀀트투자 연구소'
SITEDESCRIPTION = ''
SITELOGO = None
FAVICON = '/images/favicon.ico'
BROWSER_COLOR = '#333333'
PYGMENTS_STYLE = 'vs'

ROBOTS = 'index, follow'

THEME = os.path.join(BASE_DIR, 'pelican-themes/Flex')
PATH = 'content'
TIMEZONE = 'Asia/Seoul'

I18N_TEMPLATES_LANG = 'ko'
DEFAULT_LANG = 'ko'


DATE_FORMATS = {
    'ko': '%Y-%m-%d',
}

FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

USE_FOLDER_AS_CATEGORY = True
MAIN_MENU = True
HOME_HIDE_TAGS = True

#LINKS = (('Portfolio', 'http://alexandrevicenzi.com'),)

SOCIAL = (('github', 'https://github.com/quantylab'),
          ('linkedin', 'https://www.linkedin.com/in/moonkwonkim'))

MENUITEMS = (('Archives', '/archives.html'),
             ('Categories', '/categories.html'),
             ('Tags', '/tags.html'),)

CC_LICENSE = {
    'name': 'Creative Commons Attribution-NonCommercial-ShareAlike',
    'version': '4.0',
    'slug': 'by-nc-sa'
}

COPYRIGHT_YEAR = now.year

DEFAULT_PAGINATION = 10

PLUGIN_PATHS = ['./pelican-plugins']
PLUGINS = ['sitemap', 'post_stats', 'i18n_subsites']

JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.6,
        'indexes': 0.6,
        'pages': 0.5,
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly',
    }
}

DISQUS_SITENAME = "moonkwonkim"
#ADD_THIS_ID = 'ra-55adbb025d4f7e55'

#STATUSCAKE = {
#    'trackid': 'SL0UAgrsYP',
#    'days': 7,
#    'rumid': 6852,
#    'design': 6,
#}

STATIC_PATHS = ['img', 'data', 'extra']

EXTRA_PATH_METADATA = {
    'extra/custom.css': {'path': 'static/custom.css'},
    'extra/googlefaf75a5303a8d9f4.html': {'path': 'googlefaf75a5303a8d9f4.html'},
    'extra/naver05a93500b403624c88b17792fedd5191.html': {'path': 'naver05a93500b403624c88b17792fedd5191.html'},
}

IGNORE_FILES = ['.*']

READERS = {'html': None}

CUSTOM_CSS = 'static/custom.css'

DISABLE_URL_HASH = True

USE_LESS = True

GOOGLE_ADSENSE = {
    'ca_id': 'ca-pub-3183919385403812',
    'page_level_ads': True,
    'ads': {
        'aside': '7692470929',
        'main_menu': '1866596466',
        'index_top': '',
        'index_bottom': '5684166949',
        'article_top': '',
        'article_bottom': '7257980762',
    }
}

GOOGLE_ANALYTICS = 'UA-111763758-1'
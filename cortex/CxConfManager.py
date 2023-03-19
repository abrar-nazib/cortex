"""Module for Configuration Management"""

import os
import json

BASEDIR = os.path.dirname(__file__)

THEME_CONF_PATH = os.path.join(BASEDIR, '../conf/themes.json')
with open(THEME_CONF_PATH, 'rb') as f:
    themeConf = json.load(f)


# Creating Themes icon list
icons = themeConf["Dark"]["icons"]

for name in icons:
    """Take icon names from config and assign absolute path to them"""
    icons[name] = os.path.join(BASEDIR, "../icons", icons[name])

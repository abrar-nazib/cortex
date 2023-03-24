"""Module for Configuration Management"""

import os
import json

BASEDIR = os.path.dirname(__file__)

THEME_CONF_PATH = os.path.join(BASEDIR, '../conf/themes.json')
SETTINGS_CONF_PATH = os.path.join(BASEDIR, "../conf/settings.json")
with open(THEME_CONF_PATH, 'r') as tf:
    themeConf = json.load(tf)


# Creating Themes icon list
images = themeConf["Dark"]["images"]
for name in images:
    """Take icon names from config and assign absolute path to them"""
    images[name] = os.path.join(BASEDIR, "../images", images[name])

# Creating Themes icon list
icons = themeConf["Dark"]["icons"]
for name in icons:
    """Take icon names from config and assign absolute path to them"""
    icons[name] = os.path.join(BASEDIR, "../icons", icons[name])
#


def loadSettingsData():
    global settingsConf
    global servoConf
    global cameraConf
    with open(SETTINGS_CONF_PATH, 'r') as sf:
        settingsConf = json.load(sf)
    servoConf = settingsConf["Servo"]
    cameraConf = settingsConf["Camera"]


def saveSettingsData():
    global settingsConf
    global servoConf
    global cameraConf
    settingsConf["Camera"] = cameraConf
    settingsConf["Servo"] = servoConf
    with open(SETTINGS_CONF_PATH, 'w') as sf:
        json.dump(settingsConf, sf, indent=2)


loadSettingsData()

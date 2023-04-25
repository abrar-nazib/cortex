import typing
import os
import json

# setting the configuration paths
BASEDIR = os.path.dirname(__file__)
CONF_PATH = os.path.join(BASEDIR, '../conf/config.json')


class Icons:
    def __init__(self, configDict: typing.Dict[str, typing.Any]):
        self.__dict__.update(configDict)
        for elem in configDict:
            setattr(self, elem, os.path.join(
                BASEDIR, "../icons", os.path.basename(configDict[elem])))

    def __repr__(self) -> str:
        return f"{self.__dict__}"


class Images:
    def __init__(self, configDict: typing.Dict[str, typing.Any]):
        self.__dict__.update(configDict)
        for elem in configDict:
            setattr(self, elem, os.path.join(
                BASEDIR, "../images", os.path.basename(configDict[elem])))

    def __repr__(self) -> str:
        return f"{self.__dict__}"


class Theme:
    def __init__(self, configDict: typing.Dict[str, typing.Any]):
        self.__dict__.update(configDict)
        for elem in configDict:
            if elem == "images":
                setattr(self, elem, Images(configDict[elem]))
            elif elem == "icons":
                setattr(self, elem, Icons(configDict[elem]))
            else:
                setattr(self, elem, configDict[elem])

    def __repr__(self) -> str:
        return f"{self.__dict__}"


class ThemeConfig:
    def __init__(self, configDict: typing.Dict[str, typing.Any]):
        self.__dict__.update(configDict)
        for elem in configDict:
            setattr(self, elem, Theme(configDict[elem]))

    def __repr__(self) -> str:
        return f"{self.__dict__}"


class HardwareConfig:
    def __init__(self, configDict: typing.Dict[str, typing.Any]):
        self.__dict__.update(configDict)
        # for elem in configDict:
        #     setattr(self, elem, configDict[elem])


class CameraConfig:
    def __init__(self, configDict: typing.Dict[str, typing.Any]):
        self.__dict__.update(configDict)
        # for elem in configDict:
        #     setattr(self, elem, configDict[elem])


class Servo:
    def __init__(self, configDict: typing.Dict[str, typing.Any]):
        self.__dict__.update(configDict)
        for elem in configDict:
            setattr(self, elem, configDict[elem])

    def __repr__(self) -> str:
        return f"{self.__dict__}"


class ServoConfig:
    def __init__(self, configDict: typing.Dict[str, typing.Any]):
        self.__dict__.update(configDict)
        for elem in configDict:
            setattr(self, elem, Servo(configDict[elem]))

    def __repr__(self) -> str:
        return f"{self.__dict__}"


class Config:
    def __init__(self):
        configDict = self.loadConfig()
        self.Theme = ThemeConfig(configDict["Theme"])
        self.Servo = ServoConfig(configDict["Servo"])
        self.Camera = CameraConfig(configDict["Camera"])
        self.Hardware = HardwareConfig(configDict["Hardware"])
        # self.saveConfig()

    @classmethod
    def to_dict(cls, obj) -> typing.Dict[str, typing.Any]:
        """Converts an object to a dictionary.

        Args:
            obj (typing.Any): Config object

        Returns:
            typing.Dict[str, typing.Any]: Dictionary Representation of the object
        """
        if isinstance(obj, dict):
            return {k: cls.to_dict(v) for k, v in obj.items()}
        elif hasattr(obj, '__dict__'):
            return cls.to_dict(vars(obj))
        elif isinstance(obj, list):
            return [cls.to_dict(elem) for elem in obj]
        else:
            return obj

    def saveConfig(self, configPath: str = CONF_PATH):
        """Saves the current configuration to a json file."""

        # with open(configPath, 'w') as cf:
        # json.dump(Config.to_dict(self), cf, indent=2)
        print(Config.to_dict(self))

    def loadConfig(self, configPath: str = CONF_PATH):
        with open(configPath, 'r') as cf:
            configDict = json.load(cf)
        return configDict


# list the methods of __dict__
# print(dir(config.__dict__))
conf = Config()
IMAGES = conf.Theme.Dark.images
ICONS = conf.Theme.Dark.icons
COLORS = conf.Theme.Dark
conf.saveConfig()

"""Config parser."""
from os.path import expanduser, expandvars
import configparser
from singleton import singleton

from configparser import ExtendedInterpolation


class ExtendedEnvInterpolation(ExtendedInterpolation):
    def before_get(self, parser, section, option, value, defaults):
        return super(ExtendedEnvInterpolation, self).before_get(parser,
                                                                section,
                                                                option,
                                                                expandvars(expanduser(value)),
                                                                defaults)

    def before_set(self, parser, section, option, value):
        return super(ExtendedEnvInterpolation, self).before_set(parser,
                                                                section,
                                                                option,
                                                                expandvars(expanduser(value)))


@singleton
class ConfigSystem(configparser.ConfigParser):
    pass


def getConfig(section):  # pylint: disable=invalid-name
    """
    Get config helper function.
    Return the config for the given section.
    """
    return ConfigSystem.get_instance().get_section(section) # pylint: disable=no-member
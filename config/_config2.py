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
    Get config section helper function.

    This function allows access to the given `section` of the config in a similar way to the
    python logging system.

    Args:
        section (str): The name of the `section` to retrieve.

    Returns:
         configparser.SectionProxy: A `SectionProxy` object for the requested `section`.

    Raises:
        configparser.NoSectionError: If `section` does not exist in the config.
    """
    instance = ConfigSystem.get_instance()  # pylint: disable=no-member
    if not instance.has_section(section):
        raise configparser.NoSectionError(section)
    return instance[section]

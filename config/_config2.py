"""Config parser."""
from os.path import expanduser, expandvars
import configparser
from singleton import singleton

__all__ = ('ConfigSystem', 'getConfig', 'ExtendedEnvInterpolation')


class ExtendedEnvInterpolation(configparser.ExtendedInterpolation):
    """Extended Interpolator that also expands env variables."""

    # pylint: disable=too-many-arguments
    def before_get(self, parser, section, option, value, defaults):
        """
        Before get.

        Expands out both user ~ and environment variables.
        """
        return super(ExtendedEnvInterpolation, self).before_get(parser,
                                                                section,
                                                                option,
                                                                expandvars(expanduser(value)),
                                                                defaults)

    def before_set(self, parser, section, option, value):
        """
        Before set.

        Expands out both user ~ and environment variables.
        """
        return super(ExtendedEnvInterpolation, self).before_set(parser,
                                                                section,
                                                                option,
                                                                expandvars(expanduser(value)))


@singleton
class ConfigSystem(configparser.ConfigParser):
    """Singleton version of `ConfigParser`."""

    def __init__(self, *args, **kwargs):
        """Initialisation."""
        if len(args) < 10:  # not explicitly set in args
            kwargs.setdefault("interpolation", ExtendedEnvInterpolation())
        super(ConfigSystem, self).__init__(*args, **kwargs)


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

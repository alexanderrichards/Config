"""Configuration System Module."""
import ast
import logging
import ConfigParser
from os.path import abspath, realpath, expanduser, expandvars
from copy import deepcopy
from collections import defaultdict

from singleton import singleton


@singleton
class ConfigSystem(object):
    """Config system singleton."""

    def __init__(self, configs=None):
        """Initialisation."""
        self._config = defaultdict(dict)
        self._logger = logging.getLogger(__name__)
        if configs is not None:
            self.read(configs)

    @property
    def config(self):
        """Get the current state of the configuration."""
        return dict(deepcopy(self._config))

    @property
    def sections(self):
        """Get list of sections."""
        return self._config.keys()

    @property
    def entry_point_map(self):
        """Return the entry point map."""
        return deepcopy(self._config['Core'].get("entry_point_map"))

    @entry_point_map.setter
    def entry_point_map(self, map_):
        """Set the entry point map (one time only)."""
        if self._config['Core'].get("entry_point_map") is not None:
            self._logger.warning("Can not re-set entry_point_map once it's been set.")
        else:
            self._config['Core']['entry_point_map'] = map_

    def get_section(self, section):
        """Return a given section."""
        return deepcopy(self._config[section])

    def read(self, filenames, ignore_errors=False):
        """Set-up the configuration system."""
        config_parser = ConfigParser.SafeConfigParser()
        config_parser.optionxform = str

        if isinstance(filenames, basestring):
            filenames = [filenames]
        filenames = {abspath(realpath(expanduser(expandvars(filename))))
                     for filename in filenames}

        for filename in filenames:
            try:
                with open(filename, 'rb') as config_file:
                    config_parser.readfp(config_file)
                self._logger.debug("Read config file: %s", filename)
            except IOError:
                self._logger.warning("Failed to open config file: %r", filename)
                if not ignore_errors:
                    raise
            except ConfigParser.Error:
                self._logger.warning("Failed to read config file: %r", filename)
                if not ignore_errors:
                    raise

        for section in config_parser.sections():
            self._config[section].update((key, ast.literal_eval(val))
                                         for key, val in config_parser.items(section))


def getConfig(section):  # pylint: disable=invalid-name
    """Return the config for the given section."""
    return ConfigSystem.get_instance().get_section(section)  # pylint: disable=no-member

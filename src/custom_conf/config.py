import logging
from abc import abstractmethod
from argparse import Namespace
from pathlib import Path
from typing import Any

import custom_conf.errors as err
from custom_conf.properties.property import Property
from custom_conf.reader import read_yaml


logger = logging.getLogger(__name__)


class InstanceDescriptorMixin:
    """ Enable descriptors on an instance instead of a class.
    See https://blog.brianbeck.com/post/74086029/instance-descriptors.
    """

    def __getattribute__(self, name: str) -> Any:
        value = object.__getattribute__(self, name)
        if hasattr(value, '__get__'):
            value = value.__get__(self, self.__class__)
        return value

    def __setattr__(self, name: str, value: Any) -> None:
        try:
            obj = object.__getattribute__(self, name)
        except AttributeError:
            pass
        else:
            if hasattr(obj, '__set__'):
                return obj.__set__(self, value)
        return object.__setattr__(self, name, value)


def list_configs(directory: Path) -> list[Path]:
    """ List all config files in the given directory. """
    if not directory.is_dir():
        logger.warning(f"Could not find configuration files in "
                       f"{directory}, because it is not a directory.")
        return []
    return list(directory.glob("*.yaml")) + list(directory.glob("*.yml"))


class BaseConfig(InstanceDescriptorMixin):
    """ Basic config without any properties. """
    def __init__(self, load_default=False, load_all=False) -> None:
        self._initialized = False
        self._create_config_dir()
        self.properties = []
        self._initialize_config_properties()
        # Always load default config first, before loading any custom config
        # or program parameters.
        if load_default:
            self.load_default_config()
        if load_all:
            self.load_configs(self.config_dir)

    @property
    def initialized(self) -> bool:
        try:
            return self._initialized
        except AttributeError:
            return False

    def __setattr__(self, name: str, value: Any) -> None:
        # Disallow adding new (unknown) properties after initialization.
        if self.initialized and isinstance(value, Property):
            try:
                object.__getattribute__(self, name)
            except AttributeError:
                raise err.AddAfterInitError(name=name)
        super().__setattr__(name, value)

    def _register_properties(self) -> None:
        for var in vars(self):
            prop = object.__getattribute__(self, var)
            if not isinstance(prop, Property):
                continue
            if var != prop.name:
                raise err.MismatchedPropertyNameError(prop=prop, name=var)
            prop.register(self)

    def _initialize_config_properties(self) -> None:
        self._register_properties()
        self._initialized = True

    def load_default_config(self) -> None:
        """ Loads the default configuration.

        Should be called before loading any other configuration. """
        if not self.load_config(self.default_config_path):
            logger.error("Errors occurred when reading the given configs. "
                         "Exiting...")
            quit(err.INVALID_CONFIG_EXIT_CODE)

    def load_configs(self, path: Path) -> None:
        """ Tries to load the config file, if path is a file. If path is a
        directory, try to load all config files contained. """

        configs = [path] if path.is_file() else list_configs(path)
        if not configs:
            return

        valid = True
        for path in configs:
            # Do not load the default config again.
            if path == self.default_config_path:
                continue
            valid &= self.load_config(path)
        valid &= self._validate_no_missing_properties()
        if valid:
            return

        logger.error("Errors occurred when reading the given configs. "
                     "Exiting...")
        quit(err.INVALID_CONFIG_EXIT_CODE)

    def load_config(self, path: Path) -> bool:
        """ Load the given config.

        :param path: Path to config file.
        :return: True, if loading was a success, False if any errors occurred.
        """
        if path.exists() and path.is_file():
            data, valid = read_yaml(path)
            valid &= self._validate_no_invalid_properties(data)
            return valid

        logger.error(f"The given configuration file either does not "
                     f"exist or is not a proper file: '{path}'.")
        return False

    def load_args(self, args_ns: Namespace):
        """ Reads the program arguments in args. """
        args = {arg: getattr(args_ns, arg)
                for arg in dir(args_ns) if not arg.startswith("_")}
        for config_path in args.pop("config", []):
            path = Path(config_path).resolve()
            if path.is_dir():
                logger.info(
                    f"The given config path '{path}' leads to a directory. "
                    f"All configs in the directory will be read.")
                self.load_configs(path)
            else:
                self.load_config(path)

        for name, value in args.items():
            if value is None:
                # Nothing to log, cause this just means argument is unset.
                continue
            if name not in self.properties:
                logger.error(f"Tried to set unknown property '{name}'.")
                continue
            setattr(self, name, value)

    def _validate_no_invalid_properties(self, data: dict[str, Any]) -> bool:
        valid = True
        for name, value in data.items():
            # Even if an item is invalid, continue reading to find all errors.
            try:
                if name not in self.properties:
                    raise err.UnknownPropertyError(name=name, value=value)
                setattr(self, name, value)
            except err.PropertyError:
                valid = False
        return valid

    def _validate_no_missing_properties(self) -> bool:
        missing_keys = []
        for key in self.properties:
            try:
                getattr(self, key)
            except err.MissingRequiredPropertyError:
                missing_keys.append(key)

        if missing_keys:
            logger.warning(
                "The following values are required, but are missing in "
                "the configuration: ['{}']. This usually only happens, "
                "if the default configuration was changed, instead of "
                "creating a custom one.".format("', '".join(missing_keys)))
            return False
        return True

    @property
    @abstractmethod
    def config_dir(self) -> Path:
        """ The path to the directory, which holds additional config files. """
        pass

    @property
    @abstractmethod
    def default_config_path(self) -> Path:
        """ Return the path to the default configuration. """
        pass

    @property
    @abstractmethod
    def source_dir(self) -> Path:
        """ Return the path to the source directory. """
        pass

    def _create_config_dir(self) -> None:
        if self.config_dir.exists():
            return
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def __str__(self) -> str:
        string_like = (str, Path)

        def _get_property_string(_name: str, _value: Any) -> str:
            wrapper = "'" if isinstance(_value, string_like) else ""
            return f"\t{_name:{max_name_len}}: {wrapper}{_value}{wrapper}"

        base_string = "\nCurrent configuration: [\n{}\n]"

        property_names = self.properties + ["base_path", "default_config_path"]
        max_name_len = max(len(name) for name in property_names)

        # This can only fail if some properties are missing. However, in
        # that case we have already quit.
        prop_strings = [_get_property_string(name, getattr(self, name))
                        for name in property_names]

        return base_string.format("\n".join(prop_strings))

"""
    This file is part of OGRaySpY
    Author: Marcelo Francis Máduar (maduar@vivaldi.net)


    Provides default settings that can be overridden,
    including language, folders, algorithms and others.

"""

from ograypsy.classes.localize import Localize

class BaseSettings:
    def __init__(self) -> None:
        """ Set locale. """
        self._locale = None

    @property
    def locale(self) -> str:
        return self._locale

    @locale.setter
    def locale(self, lcid: str) -> None:
        self._locale = lcid
        Localize.set_locale(lcid)

    def set_spectra_filepath(self, filepath: str) -> None:
        self._spectra_filepath = filepath

class StaticSingleton(type):
    """ Metaclass to ensure singleton behavior & route everything to
    our BaseSettings instance to emulate static behavior. """
    _instance = BaseSettings()

    def reset(cls) -> None:
        """ Reset all settings to default. """
        StaticSingleton._instance = BaseSettings()
        StaticSingleton._instance.set_swe_filepath()
        Localize.reset()

    def set(cls, values: dict) -> None:
        """ Helper mass-set method. """
        for key, value in values.items():
            setattr(StaticSingleton._instance, key, value)

    def __getattr__(cls, name: str):
        return getattr(StaticSingleton._instance, name)

    def __setattr__(cls, name: str, value) -> None:
        return setattr(StaticSingleton._instance, name, value)


class settings(metaclass=StaticSingleton):
    """ Expose actual class for import. """
    pass
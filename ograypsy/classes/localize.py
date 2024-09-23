"""
    This file is part of OGRaySpY
    Author: Marcelo Francis Máduar (maduar@vivaldi.net)


    Sets up translations and provides our own _() function. This will look for
    a translation file for the full locale and fall back to the parent locale,
    for example pt_BR then pt. If a file is found, then the full locale string
    (e.g. pt_BR) will be passed to locale.setlocale() for localizing datetimes.

"""

import gettext, locale, os

class Localize:
    lcid = None
    translation = None
    localedir = f'{os.path.dirname(__file__)}{os.sep}..{os.sep}locales'

    def set_locale(self, lcid: str) -> None:
        languages = (lcid, lcid[:2])
        translation = gettext.translation(
            'ograyspy',
            localedir=Localize.localedir,
            languages=languages, fallback=True
        )

        if isinstance(translation, gettext.GNUTranslations):
            Localize.lcid = lcid
            Localize.translation = translation
            locale.setlocale(locale.LC_TIME, lcid)
        else:
            self.reset()

    def reset(self) -> None:
        Localize.lcid = None
        Localize.translation = None
        locale.setlocale(locale.LC_TIME, 'en_US')






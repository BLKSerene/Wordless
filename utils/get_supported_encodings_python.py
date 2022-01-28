# ----------------------------------------------------------------------
# Wordless: Utilities - Supported Encodings of Python
# Copyright (C) 2018-2022  Ye Lei (叶磊)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

# Standard encodings: https://docs.python.org/3/library/codecs.html#standard-encodings
# Python specific encodings: https://docs.python.org/3/library/codecs.html#python-specific-encodings

import encodings
import pkgutil

non_encodings = [
    'aliases',
    'charmap',

    'idna',
    'mbcs',
    'oem',
    'palmos',
    'punycode',
    'raw_unicode_escape',
    'undefined',
    'unicode_escape',

    'base64_codec',
    'bz2_codec',
    'hex_codec',
    'quopri_codec',
    'uu_codec',
    'zlib_codec',

    'rot_13'
]

encodings_supported = set(name for imp, name, ispkg in pkgutil.iter_modules(encodings.__path__) if not ispkg)

for encoding in non_encodings:
    encodings_supported.remove(encoding)

for encoding in sorted(encodings_supported):
    print(encoding)

# Aliases
encoding_aliases_merged = {}

encoding_aliases = encodings.aliases.aliases

for alias, encoding in encoding_aliases.items():
    if encoding not in encoding_aliases_merged:
        encoding_aliases_merged[encoding] = [alias]
    else:
        encoding_aliases_merged[encoding].append(alias)

for encoding in non_encodings:
    if encoding in encoding_aliases_merged:
        del encoding_aliases_merged[encoding]

for encoding, aliases in encoding_aliases_merged.items():
    print(f"{encoding}: {', '.join(aliases)}")

#
# Wordless: Utilities - Supported Encodings of Python
#
# Copyright (C) 2018-2019 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

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
	'unicode_internal',

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

print('---------- List of all supported encodings in Python ----------')

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

print('\n---------- List of all aliases of encodings in Python ----------')

for encoding, aliases in encoding_aliases_merged.items():
	print(f"{encoding}: {', '.join(aliases)}")

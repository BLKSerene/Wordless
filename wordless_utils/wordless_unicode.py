#
# Wordless: Utilities for Unicode Characters
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import re

import sacremoses

# Unicode Blocks: https://en.wikipedia.org/wiki/Unicode_block

def is_cjk(char):
	return sacremoses.util.is_cjk(char)

def is_kana(char):
	unicode_kana = [
		# Hiragana:
		#     https://en.wikipedia.org/wiki/Hiragana_(Unicode_block)
		(0x3040, 0x309F),
		# Katakana:
		#     https://en.wikipedia.org/wiki/Katakana_(Unicode_block)
		(0x30A0, 0x30FF),
		# Katakana Phonetic Extensions:
		#     https://en.wikipedia.org/wiki/Katakana_Phonetic_Extensions
		(0x31F0, 0x31FF),
		# Enclosed CJK Letters and Months:
		#     https://en.wikipedia.org/wiki/Enclosed_CJK_Letters_and_Months
		(0x32D0, 0x32FE),
		# CJK Compatibility:
		#     https://en.wikipedia.org/wiki/CJK_Compatibility
		(0x3300, 0x3357),
		# Halfwidth and Fullwidth Forms:
		#     https://en.wikipedia.org/wiki/Halfwidth_and_fullwidth_forms
		(0xFF65, 0xFF9F),
		# Kana Supplement:
		#     https://en.wikipedia.org/wiki/Kana_Supplement
		(0x1B000, 0x1B0FF),
		# Kana Extended-A:
		#     https://en.wikipedia.org/wiki/Kana_Extended-A
		(0x1B100, 0x1B12F)
	]

	return any([unicode_start <= ord(char) <= unicode_end
		        for unicode_start, unicode_end in unicode_kana])

def is_thai(char):
	# Thai:
	#     https://en.wikipedia.org/wiki/Thai_(Unicode_block)
	return 0x0E00 <= ord(char) <= 0x0E7F

def has_thai(token):
	return re.search(r'[\u0E00-\u0E7F]', token)

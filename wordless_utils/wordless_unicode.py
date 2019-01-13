#
# Wordless: Utilities for Unicode Characters
#
# Copyright (C) 2018-2019 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

# Unicode Blocks: https://en.wikipedia.org/wiki/Unicode_block

def is_han(char):
    unicode_han = [
        # CJK Radicals Supplement:
        #     https://en.wikipedia.org/wiki/CJK_Radicals_Supplement
        (0x2E80, 0x2EFF),
        # Kangxi Radicals:
        #     https://en.wikipedia.org/wiki/Kangxi_radical#Unicode
        (0x2F00, 0X2FDF),
        # Ideographic Description Characters
        #     https://en.wikipedia.org/wiki/Ideographic_Description_Characters_(Unicode_block)
        (0x2FF0, 0x2FFF),
        # CJK Symbols and Punctuation:
        #     https://en.wikipedia.org/wiki/CJK_Symbols_and_Punctuation
        (0x3000, 0x302D), (0x3030, 0x3030), (0x3036, 0x303F),
        # Bopomofo
        #     https://en.wikipedia.org/wiki/Bopomofo_(Unicode_block)
        (0x3100, 0x312F),
        # Kanbun:
        #     https://en.wikipedia.org/wiki/Kanbun_(Unicode_block)
        (0x3190, 0x319F),
        # Bopomofo Extended:
        #     https://en.wikipedia.org/wiki/Bopomofo_Extended
        (0x31A0, 0x31BF),
        # CJK Strokes
        #     https://en.wikipedia.org/wiki/CJK_Strokes_(Unicode_block)
        (0x31C0, 0x31EF),
        # Enclosed CJK Letters and Months:
        #     https://en.wikipedia.org/wiki/Enclosed_CJK_Letters_and_Months
        (0x3220, 0x325F), (0x3280, 0x32CF),
        # CJK Compatibility:
        #     https://en.wikipedia.org/wiki/CJK_Compatibility
        (0x3358, 0x33FF),
        # CJK Unified Ideographs Extension A:
        #     https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_Extension_A
        (0x3400, 0x4DBF),
        # Yijing Hexagram Symbols:
        #     https://en.wikipedia.org/wiki/Yijing_Hexagram_Symbols
        (0x4DC0, 0x4DFF),
        # CJK Unified Ideographs:
        #     https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_(Unicode_block)
        (0x4E00, 0x9FFF),
        
        # Yi Syllables:
        #     https://en.wikipedia.org/wiki/Yi_Syllables
        (0xA000, 0xA48F),
        # Yi Radicals:
        #     https://en.wikipedia.org/wiki/Yi_Radicals
        (0xA490, 0xA4CF),
        # Phags-pa:
        #     https://en.wikipedia.org/wiki/Fraser_alphabet
        (0xA840, 0xA87F),
        # CJK Compatibility Ideographs:
        #     https://en.wikipedia.org/wiki/CJK_Compatibility_Ideographs
        (0xF900, 0xFAFF),
        # CJK Compatibility Forms:
        #     https://en.wikipedia.org/wiki/CJK_Compatibility_Forms
        (0xFE30, 0xFE4F),

        # Ideographic Symbols and Punctuation:
        #     https://en.wikipedia.org/wiki/Ideographic_Symbols_and_Punctuation
        (0x16FE0, 0x16FFF),
        # Tangut:
        #     https://en.wikipedia.org/wiki/Tangut_(Unicode_block)
        (0x17000, 0x187FF),
        # Tangut Components:
        #     https://en.wikipedia.org/wiki/Tangut_Components
        (0x18800, 0x18AFF),
        # Nushu:
        #     https://en.wikipedia.org/wiki/Nushu_(Unicode_block)
        (0x1B170, 0x1B2FF),

        # CJK Unified Ideographs Extension B:
        #     https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_Extension_B
        (0x20000, 0x2A6DF),
        # CJK Unified Ideographs Extension C:
        #     https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_Extension_C
        (0x2A700, 0x2B73F),
        # CJK Unified Ideographs Extension D:
        #     https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_Extension_D
        (0x2B740, 0x2B81F),
        # CJK Unified Ideographs Extension E:
        #     https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_Extension_E
        (0x2B820, 0x2CEAF),
        # CJK Unified Ideographs Extension F:
        #     https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_Extension_F
        (0x2CEB0, 0x2EBEF),
        # CJK Compatibility Ideographs Supplement:
        #     https://en.wikipedia.org/wiki/CJK_Compatibility_Ideographs_Supplement
        (0x2F800, 0x2FA1F)
    ]

    return any([unicode_start <= ord(char) <= unicode_end
                for unicode_start, unicode_end in unicode_han])

def is_kana(char):
    unicode_kana = [
        # CJK Symbols and Punctuation:
        #     https://en.wikipedia.org/wiki/CJK_Symbols_and_Punctuation
        (0x3031, 0x3035),
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
        #     https://en.wikipedia.org/wiki/Halfwidth_and_fullwidth_forms#In_Unicode
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

def is_tibetan(char):
    # Tibetan:
    #     https://en.wikipedia.org/wiki/Tibetan_(Unicode_block)
    return 0x0F00 <= ord(char) <= 0x0FFF



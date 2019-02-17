#
# Wordless: Text - Text Utilities
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

def to_sections(tokens, number_sections):
    sections = []

    section_size, remainder = divmod(len(tokens), number_sections)

    for i in range(number_sections):
        if i < remainder:
            section_start = i * section_size + i
        else:
            section_start = i * section_size + remainder

        if i + 1 < remainder:
            section_stop = (i + 1) * section_size + i + 1
        else:
            section_stop = (i + 1) * section_size + remainder

        sections.append(tokens[section_start:section_stop])

    return sections

#
# Wordless: Utility Function for Texts
#
# Copyright (C) 2018-2019 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

def check_context(i, tokens, settings,
                  search_terms_inclusion, search_terms_exclusion):
    if settings['inclusion']['inclusion'] or settings['exclusion']['exclusion']:
        len_tokens = len(tokens)

        # Inclusion
        if settings['inclusion']['inclusion'] and search_terms_inclusion:
            inclusion_matched = False

            for search_term in search_terms_inclusion:
                if inclusion_matched:
                    break

                for j in range(settings['inclusion']['context_window_left'],
                               settings['inclusion']['context_window_right'] + 1):
                    if i + j < 0 or i + j > len_tokens - 1:
                        continue

                    if j != 0:
                        if tuple(tokens[i + j : i + j + len(search_term)]) == tuple(search_term):
                            inclusion_matched = True

                            break
        else:
            inclusion_matched = True

        # Exclusion
        exclusion_matched = True

        if settings['exclusion']['exclusion'] and search_terms_exclusion:
            for search_term in search_terms_exclusion:
                if not exclusion_matched:
                    break

                for j in range(settings['exclusion']['context_window_left'],
                               settings['exclusion']['context_window_right'] + 1):
                    if i + j < 0 or i + j > len_tokens - 1:
                        continue

                    if j != 0:
                        if tuple(tokens[i + j : i + j + len(search_term)]) == tuple(search_term):
                            exclusion_matched = False

                            break

        if inclusion_matched and exclusion_matched:
            return True
        else:
            return False
    else:
        return True

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

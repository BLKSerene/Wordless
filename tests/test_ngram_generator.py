# ----------------------------------------------------------------------
# Tests: Work Area - N-gram Generator
# Copyright (C) 2018-2025  Ye Lei (叶磊)
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import random

from tests import (
    wl_test_file_area,
    wl_test_init
)
from wordless import wl_ngram_generator
from wordless.wl_dialogs import wl_dialogs_misc
from wordless.wl_nlp import wl_texts

main_global = None

def test_ngram_generator():
    main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')

    settings = main.settings_custom['ngram_generator']
    settings_table = main.settings_custom['tables']['ngram_generator']['lang_specific_settings']

    settings['search_settings']['multi_search_mode'] = True
    settings['search_settings']['search_terms'] = wl_test_init.SEARCH_TERMS
    settings['generation_settings']['ngram_size_min'] = 1
    settings['generation_settings']['ngram_size_max'] = 1

    measures_dispersion = list(main.settings_global['measures_dispersion'])
    measures_adjusted_freq = list(main.settings_global['measures_adjusted_freq'])

    for i in range(2 + wl_test_file_area.NUM_FILES_OTHERS):
        match i:
            # Single file
            case 0:
                wl_test_init.select_test_files(main, no_files = (0,))
            # Multiple files
            case 1:
                wl_test_init.select_test_files(main, no_files = (1, 2))
            # Miscellaneous
            case _:
                wl_test_init.select_test_files(main, no_files = (i + 1,))

                match main.settings_custom['file_area']['files_open'][i + 1]['name']:
                    # Tibetan
                    case '[bod] Tibetan tshegs':
                        settings_table['add_missing_ending_tshegs'] = True
                    case '[xct] Tibetan tshegs':
                        settings_table['add_missing_ending_tshegs'] = False
                    # Miscellaneous
                    case '[eng_us] Starting with a punctuation mark' | '[eng_us] Starting with tags':
                        pass
                    case _:
                        continue

        settings['generation_settings']['measure_dispersion'] = random.choice(measures_dispersion)
        settings['generation_settings']['measure_adjusted_freq'] = random.choice(measures_adjusted_freq)

        global main_global
        main_global = main

        print(f"Files: {' | '.join(wl_test_init.get_test_file_names(main))}")
        print(f"Measure of dispersion: {settings['generation_settings']['measure_dispersion']}")
        print(f"Measure of adjusted frequency: {settings['generation_settings']['measure_adjusted_freq']}")

        worker_ngram_generator = wl_ngram_generator.Wl_Worker_Ngram_Generator_Table(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(main),
        )

        worker_ngram_generator.finished.connect(update_gui)
        worker_ngram_generator.run()

def update_gui(err_msg, ngrams_freq_files, ngrams_stats_files):
    print(err_msg)
    assert not err_msg

    assert len(ngrams_freq_files) == len(ngrams_stats_files) >= 1

    files_selected = list(main_global.wl_file_area.get_selected_files())
    num_files_selected = len(files_selected)
    settings = main_global.settings_custom['ngram_generator']['generation_settings']

    measure_dispersion = settings['measure_dispersion']
    measure_adjusted_freq = settings['measure_adjusted_freq']

    for ngram, freq_files in ngrams_freq_files.items():
        stats_files = ngrams_stats_files[ngram]

        # N-gram
        assert ngram

        # Frequency
        match files_selected[0]['name']:
            case '[bod] Tibetan tshegs':
                assert freq_files == [2, 2]
            case '[xct] Tibetan tshegs':
                assert freq_files == [1, 1]

        assert len(freq_files) == num_files_selected + 1
        assert freq_files[-1] == sum(freq_files[:-1])

        # Dispersion & Adjusted Frequency
        assert len(stats_files) == num_files_selected + 1

        for dispersion, adjusted_freq in stats_files:
            if measure_dispersion == 'none':
                assert dispersion is None
            else:
                assert dispersion >= 0

            if measure_adjusted_freq == 'none':
                assert adjusted_freq is None
            else:
                assert adjusted_freq >= 0

        # Number of Files Found
        assert len([freq for freq in freq_files[:-1] if freq]) >= 1

# Check that the results of unigrams and bigrams are the exact concatenation of those of unigrams and those of bigrams
def test_ngram_generator_ngram_size():
    settings = main_global.settings_custom['ngram_generator']

    settings['search_settings']['search_term'] = wl_test_init.SEARCH_TERMS[0]
    settings['generation_settings']['measure_dispersion'] = 'juillands_d'
    settings['generation_settings']['measure_adjusted_freq'] = 'juillands_u'

    wl_test_init.select_test_files(main_global, no_files = (0,))

    for ngram_size_min, ngram_size_max in (
        (1, 1),
        (2, 2),
        (1, 2)
    ):
        settings['generation_settings']['ngram_size_min'] = ngram_size_min
        settings['generation_settings']['ngram_size_max'] = ngram_size_max

        worker_ngram_generator = wl_ngram_generator.Wl_Worker_Ngram_Generator_Table(
            main_global,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(main_global),
        )

        worker_ngram_generator.finished.connect(update_gui_ngram_size(ngram_size_min, ngram_size_max))
        worker_ngram_generator.run()

    # pylint: disable=undefined-variable
    assert ngrams_freq_files_1_2 == ngrams_freq_files_1_1 | ngrams_freq_files_2_2
    assert ngrams_stats_files_1_2 == ngrams_stats_files_1_1 | ngrams_stats_files_2_2

def update_gui_ngram_size(ngram_size_min, ngram_size_max):
    def update_gui(err_msg, ngrams_freq_files, ngrams_stats_files):
        assert not err_msg

        globals()[f'ngrams_freq_files_{ngram_size_min}_{ngram_size_max}'] = ngrams_freq_files
        globals()[f'ngrams_stats_files_{ngram_size_min}_{ngram_size_max}'] = ngrams_stats_files

    return update_gui

def test_get_ngrams_is():
    tokens = wl_texts.to_tokens(('1', '2', '1'))

    assert wl_ngram_generator.get_ngrams_is(
        ngrams = [(tokens[0],), (tokens[1],), (tokens[2],)],
        tokens = tokens
    ) == [((tokens[0],), 0), ((tokens[1],), 1), ((tokens[2],), 2)]

if __name__ == '__main__':
    test_ngram_generator()
    test_ngram_generator_ngram_size()
    test_get_ngrams_is()

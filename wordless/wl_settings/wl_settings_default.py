# ----------------------------------------------------------------------
# Wordless: Settings - Default settings
# Copyright (C) 2018-2023  Ye Lei (叶磊)
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

import networkx
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QDesktopWidget

from wordless.wl_tagsets import (
    wl_tagset_universal,
    wl_tagset_eng_penn_treebank,
    wl_tagset_jpn_unidic,
    wl_tagset_khm_alt,
    wl_tagset_kor_mecab,
    wl_tagset_lao_seqlabeling,
    wl_tagset_lao_yunshan_cup_2020,
    wl_tagset_rus_open_corpora,
    wl_tagset_rus_russian_national_corpus,
    wl_tagset_tha_blackboard,
    wl_tagset_tha_orchid,
    wl_tagset_bod_botok,
    wl_tagset_vie_underthesea
)
from wordless.wl_utils import wl_misc, wl_paths

_tr = QCoreApplication.translate
is_windows, is_macos, is_linux = wl_misc.check_os()

# The following settings need to be loaded before initialization of the main window
DEFAULT_INTERFACE_SCALING = '100%'

# Font family
if is_windows:
    DEFAULT_FONT_FAMILY = 'Arial'
elif is_macos:
    # SF Pro is the system font on macOS >= 10.11 but is not installed by default
    DEFAULT_FONT_FAMILY = 'Helvetica Neue'
elif is_linux:
    linux_distro = wl_misc.get_linux_distro()

    if linux_distro == 'ubuntu':
        DEFAULT_FONT_FAMILY = 'Ubuntu'
    elif linux_distro == 'debian':
        DEFAULT_FONT_FAMILY = 'DejaVu'
    elif linux_distro == 'arch':
        DEFAULT_FONT_FAMILY = 'Noto Sans'

# Font size
if is_windows:
    DEFAULT_FONT_SIZE = 9
elif is_macos:
    DEFAULT_FONT_SIZE = 13
elif is_linux:
    DEFAULT_FONT_SIZE = 11

# Directories for imports and exports
DEFAULT_DIR_WORDLESS = wl_paths.get_path_file('', internal = False)
DEFAULT_DIR_IMPS = wl_paths.get_path_file('imports', internal = False)
DEFAULT_DIR_EXPS = wl_paths.get_path_file('exports', internal = False)

def init_settings_default(main):
    desktop_widget = QDesktopWidget()

    settings_default = {
        '1st_startup': True,
        'file_area_cur': _tr('wl_settings_default', 'Observed Files'),
        'work_area_cur': _tr('wl_settings_default', 'Profiler'),

        'menu': {
            'prefs': {
                'display_lang': 'eng_us',
                'layouts': {
                    'central_widget': [main.height() - 210, 210]
                },
                'show_status_bar': True
            },

            'help': {
                'citing': {
                    'select_citation_sys': _tr('wl_settings_default', 'APA (7th edition)')
                },

                'donating': {
                    'donating_via': 'PayPal'
                }
            }
        },

        'file_area': {
            'files_open': [],
            'files_open_ref': [],
            'files_closed': [],
            'files_closed_ref': [],

            'dialog_open_files': {
                'auto_detect_encodings': True,
                'auto_detect_langs': True,
                'include_files_in_subfolders': True
            }
        },

        'profiler': {
            'tab': _tr('wl_settings_default', 'Counts'),

            'token_settings': {
                'words': True,
                'all_lowercase': True,
                'all_uppercase': True,
                'title_case': True,
                'nums': True,
                'punc_marks': False,

                'treat_as_all_lowercase': False,
                'apply_lemmatization': False,
                'filter_stop_words': False,

                'assign_pos_tags': False,
                'ignore_tags': False,
                'use_tags': False
            },

            'table_settings': {
                'show_pct_data': True,
                'show_cum_data': False,
                'show_breakdown_file': True
            }
        },

        'concordancer': {
            'token_settings': {
                'punc_marks': False,

                'assign_pos_tags': False,
                'ignore_tags': False,
                'use_tags': False
            },

            'search_settings': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'match_case': False,
                'match_whole_words': False,
                'match_inflected_forms': False,
                'use_regex': False,
                'match_without_tags': False,
                'match_tags': False
            },

            'context_settings': {
                'incl': {
                    'incl': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'match_case': False,
                    'match_whole_words': False,
                    'match_inflected_forms': False,
                    'use_regex': False,
                    'match_without_tags': False,
                    'match_tags': False,

                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                },

                'excl': {
                    'excl': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'match_case': False,
                    'match_whole_words': False,
                    'match_inflected_forms': False,
                    'use_regex': False,
                    'match_without_tags': False,
                    'match_tags': False,

                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                }
            },

            'generation_settings': {
                'width_left_char': 50,
                'width_left_token': 10,
                'width_left_sentence_seg': 0,
                'width_left_sentence': 0,
                'width_left_para': 0,
                'width_right_char': 50,
                'width_right_token': 10,
                'width_right_sentence_seg': 0,
                'width_right_sentence': 0,
                'width_right_para': 0,
                'width_unit': _tr('wl_settings_default', 'Token')
            },

            'table_settings': {
                'show_pct_data': True
            },

            'fig_settings': {
                'sort_results_by': _tr('wl_settings_default', 'File')
            },

            'zapping_settings': {
                'zapping': False,
                'replace_keywords_with': 15,
                'placeholder': '_',
                'add_line_nums': True,
                'randomize_outputs': True
            },

            'sort_results': {
                'sorting_rules': [
                    [_tr('wl_settings_default', 'File'), _tr('wl_settings_default', 'Ascending')],
                    [_tr('wl_settings_default', 'Token no.'), _tr('wl_settings_default', 'Ascending')]
                ]
            },

            'search_results': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'match_case': False,
                'match_whole_words': False,
                'match_inflected_forms': False,
                'use_regex': False,
                'match_without_tags': False,
                'match_tags': False
            }
        },

        'concordancer_parallel': {
            'token_settings': {
                'punc_marks': False,

                'assign_pos_tags': False,
                'ignore_tags': False,
                'use_tags': False
            },

            'search_settings': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'match_case': False,
                'match_whole_words': False,
                'match_inflected_forms': False,
                'use_regex': False,
                'match_without_tags': False,
                'match_tags': False
            },

            'context_settings': {
                'incl': {
                    'incl': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'match_case': False,
                    'match_whole_words': False,
                    'match_inflected_forms': False,
                    'use_regex': False,
                    'match_without_tags': False,
                    'match_tags': False,

                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                },

                'excl': {
                    'excl': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'match_case': False,
                    'match_whole_words': False,
                    'match_inflected_forms': False,
                    'use_regex': False,
                    'match_without_tags': False,
                    'match_tags': False,

                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                }
            },

            'table_settings': {
                'show_pct_data': True
            },

            'search_results': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'match_case': False,
                'match_whole_words': False,
                'match_inflected_forms': False,
                'use_regex': False,
                'match_without_tags': False,
                'match_tags': False
            }
        },

        'dependency_parser': {
            'token_settings': {
                'punc_marks': False,

                'assign_pos_tags': False,
                'ignore_tags': False,
                'use_tags': False
            },

            'search_settings': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'match_case': False,
                'match_whole_words': False,
                'match_inflected_forms': False,
                'use_regex': False,
                'match_without_tags': False,
                'match_tags': False
            },

            'context_settings': {
                'incl': {
                    'incl': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'match_case': False,
                    'match_whole_words': False,
                    'match_inflected_forms': False,
                    'use_regex': False,
                    'match_without_tags': False,
                    'match_tags': False,

                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                },

                'excl': {
                    'excl': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'match_case': False,
                    'match_whole_words': False,
                    'match_inflected_forms': False,
                    'use_regex': False,
                    'match_without_tags': False,
                    'match_tags': False,

                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                }
            },

            'table_settings': {
                'show_pct_data': True
            },

            'fig_settings': {
                'show_pos_tags': True,
                'show_fine_grained_pos_tags': False,
                'show_lemmas': False,
                'compact_mode': False,
                'show_in_separate_tab': False
            },

            'search_results': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'match_case': False,
                'match_whole_words': False,
                'match_inflected_forms': False,
                'use_regex': False,
                'match_without_tags': False,
                'match_tags': False
            }
        },

        'wordlist_generator': {
            'token_settings': {
                'words': True,
                'all_lowercase': True,
                'all_uppercase': True,
                'title_case': True,
                'nums': True,
                'punc_marks': False,

                'treat_as_all_lowercase': False,
                'apply_lemmatization': False,
                'filter_stop_words': False,

                'assign_pos_tags': False,
                'ignore_tags': False,
                'use_tags': False
            },

            'generation_settings': {
                'syllabification': True,
                'measure_dispersion': 'juillands_d',
                'measure_adjusted_freq': 'juillands_u'
            },

            'table_settings': {
                'show_pct_data': True,
                'show_cum_data': False,
                'show_breakdown_file': True
            },

            'fig_settings': {
                'graph_type': _tr('wl_settings_default', 'Line chart'),
                'sort_by_file': _tr('wl_settings_default', 'Total'),
                'use_data': _tr('wl_settings_default', 'Frequency'),
                'use_pct': False,
                'use_cumulative': False,

                'rank_min': 1,
                'rank_min_no_limit': True,
                'rank_max': 50,
                'rank_max_no_limit': False,
            },

            'filter_results': {
                'file_to_filter': _tr('wl_settings_default', 'Total'),

                'len_token_min': 1,
                'len_token_min_no_limit': True,
                'len_token_max': 20,
                'len_token_max_no_limit': True,

                'num_syls_min': 1,
                'num_syls_min_no_limit': True,
                'num_syls_max': 20,
                'num_syls_max_no_limit': True,

                'freq_min': 0,
                'freq_min_no_limit': True,
                'freq_max': 1000,
                'freq_max_no_limit': True,

                'dispersion_min': -100,
                'dispersion_min_no_limit': True,
                'dispersion_max': 100,
                'dispersion_max_no_limit': True,

                'adjusted_freq_min': 0,
                'adjusted_freq_min_no_limit': True,
                'adjusted_freq_max': 1000,
                'adjusted_freq_max_no_limit': True,

                'num_files_found_min': 1,
                'num_files_found_min_no_limit': True,
                'num_files_found_max': 100,
                'num_files_found_max_no_limit': True
            },

            'search_results': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'match_case': False,
                'match_whole_words': False,
                'match_inflected_forms': False,
                'use_regex': False,
                'match_without_tags': False,
                'match_tags': False
            }
        },

        'ngram_generator': {
            'token_settings': {
                'words': True,
                'all_lowercase': True,
                'all_uppercase': True,
                'title_case': True,
                'nums': True,
                'punc_marks': False,

                'treat_as_all_lowercase': False,
                'apply_lemmatization': False,
                'filter_stop_words': False,

                'assign_pos_tags': False,
                'ignore_tags': False,
                'use_tags': False
            },

            'search_settings': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'match_case': False,
                'match_whole_words': False,
                'match_inflected_forms': False,
                'use_regex': False,
                'match_without_tags': False,
                'match_tags': False,

                'search_term_position_min': 1,
                'search_term_position_min_no_limit': True,
                'search_term_position_max': 2,
                'search_term_position_max_no_limit': True
            },

            'context_settings': {
                'incl': {
                    'incl': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'match_case': False,
                    'match_whole_words': False,
                    'match_inflected_forms': False,
                    'use_regex': False,
                    'match_without_tags': False,
                    'match_tags': False,

                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                },

                'excl': {
                    'excl': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'match_case': False,
                    'match_whole_words': False,
                    'match_inflected_forms': False,
                    'use_regex': False,
                    'match_without_tags': False,
                    'match_tags': False,

                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                }
            },

            'generation_settings': {
                'ngram_size_sync': False,
                'ngram_size_min': 2,
                'ngram_size_max': 2,
                'allow_skipped_tokens': False,
                'allow_skipped_tokens_num': 1,

                'measure_dispersion': 'juillands_d',
                'measure_adjusted_freq': 'juillands_u'
            },

            'table_settings': {
                'show_pct_data': True,
                'show_cum_data': False,
                'show_breakdown_file': True
            },

            'fig_settings': {
                'graph_type': _tr('wl_settings_default', 'Line chart'),
                'sort_by_file': _tr('wl_settings_default', 'Total'),
                'use_data': _tr('wl_settings_default', 'Frequency'),
                'use_pct': False,
                'use_cumulative': False,

                'rank_min': 1,
                'rank_min_no_limit': True,
                'rank_max': 50,
                'rank_max_no_limit': False,
            },

            'filter_results': {
                'file_to_filter': _tr('wl_settings_default', 'Total'),

                'len_ngram_min': 1,
                'len_ngram_min_no_limit': True,
                'len_ngram_max': 20,
                'len_ngram_max_no_limit': True,

                'freq_min': 0,
                'freq_min_no_limit': True,
                'freq_max': 1000,
                'freq_max_no_limit': True,

                'dispersion_min': -100,
                'dispersion_min_no_limit': True,
                'dispersion_max': 100,
                'dispersion_max_no_limit': True,

                'adjusted_freq_min': 0,
                'adjusted_freq_min_no_limit': True,
                'adjusted_freq_max': 1000,
                'adjusted_freq_max_no_limit': True,

                'num_files_found_min': 1,
                'num_files_found_min_no_limit': True,
                'num_files_found_max': 100,
                'num_files_found_max_no_limit': True
            },

            'search_results': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'match_case': False,
                'match_whole_words': False,
                'match_inflected_forms': False,
                'use_regex': False,
                'match_without_tags': False,
                'match_tags': False
            }
        },

        'collocation_extractor': {
            'token_settings': {
                'words': True,
                'all_lowercase': True,
                'all_uppercase': True,
                'title_case': True,
                'nums': True,
                'punc_marks': False,

                'treat_as_all_lowercase': False,
                'apply_lemmatization': False,
                'filter_stop_words': False,

                'assign_pos_tags': False,
                'ignore_tags': False,
                'use_tags': False
            },

            'search_settings': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'match_case': False,
                'match_whole_words': False,
                'match_inflected_forms': False,
                'use_regex': False,
                'match_without_tags': False,
                'match_tags': False
            },

            'context_settings': {
                'incl': {
                    'incl': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'match_case': False,
                    'match_whole_words': False,
                    'match_inflected_forms': False,
                    'use_regex': False,
                    'match_without_tags': False,
                    'match_tags': False,

                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                },

                'excl': {
                    'excl': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'match_case': False,
                    'match_whole_words': False,
                    'match_inflected_forms': False,
                    'use_regex': False,
                    'match_without_tags': False,
                    'match_tags': False,

                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                }
            },

            'generation_settings': {
                'window_sync': False,
                'window_left': -5,
                'window_right': 5,

                'limit_searching': _tr('wl_settings_default', 'None'),

                'test_statistical_significance': 'pearsons_chi_squared_test',
                'measure_bayes_factor': 'log_likelihood_ratio_test',
                'measure_effect_size': 'pmi'
            },

            'table_settings': {
                'show_pct_data': True,
                'show_cum_data': False,
                'show_breakdown_span_position': True,
                'show_breakdown_file': True
            },

            'fig_settings': {
                'graph_type': _tr('wl_settings_default', 'Line chart'),
                'sort_by_file': _tr('wl_settings_default', 'Total'),
                'use_data': _tr('wl_settings_default', 'p-value'),
                'use_pct': False,
                'use_cumulative': False,

                'rank_min': 1,
                'rank_min_no_limit': True,
                'rank_max': 50,
                'rank_max_no_limit': False
            },

            'filter_results': {
                'file_to_filter': _tr('wl_settings_default', 'Total'),

                'len_collocate_min': 1,
                'len_collocate_min_no_limit': True,
                'len_collocate_max': 20,
                'len_collocate_max_no_limit': True,

                'freq_position': _tr('wl_settings_default', 'Total'),
                'freq_min': 0,
                'freq_min_no_limit': True,
                'freq_max': 1000,
                'freq_max_no_limit': True,

                'test_stat_min': -100,
                'test_stat_min_no_limit': True,
                'test_stat_max': 100,
                'test_stat_max_no_limit': True,

                'p_val_min': 0,
                'p_val_min_no_limit': True,
                'p_val_max': 0.05,
                'p_val_max_no_limit': True,

                'bayes_factor_min': -100,
                'bayes_factor_min_no_limit': True,
                'bayes_factor_max': 100,
                'bayes_factor_max_no_limit': True,

                'effect_size_min': -100,
                'effect_size_min_no_limit': True,
                'effect_size_max': 100,
                'effect_size_max_no_limit': True,

                'num_files_found_min': 1,
                'num_files_found_min_no_limit': True,
                'num_files_found_max': 100,
                'num_files_found_max_no_limit': True
            },

            'search_results': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'match_case': False,
                'match_whole_words': False,
                'match_inflected_forms': False,
                'use_regex': False,
                'match_without_tags': False,
                'match_tags': False
            }
        },

        'colligation_extractor': {
            'token_settings': {
                'words': True,
                'all_lowercase': True,
                'all_uppercase': True,
                'title_case': True,
                'nums': True,
                'punc_marks': False,

                'treat_as_all_lowercase': False,
                'apply_lemmatization': False,
                'filter_stop_words': False,

                'assign_pos_tags': True,
                'ignore_tags': False,
                'use_tags': False
            },

            'search_settings': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'match_case': False,
                'match_whole_words': False,
                'match_inflected_forms': False,
                'use_regex': False,
                'match_without_tags': False,
                'match_tags': False
            },

            'context_settings': {
                'incl': {
                    'incl': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'match_case': False,
                    'match_inflected_forms': False,
                    'match_whole_words': False,
                    'use_regex': False,
                    'match_without_tags': False,
                    'match_tags': False,

                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                },

                'excl': {
                    'excl': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'match_case': False,
                    'match_inflected_forms': False,
                    'match_whole_words': False,
                    'use_regex': False,
                    'match_without_tags': False,
                    'match_tags': False,

                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                }
            },

            'generation_settings': {
                'window_sync': False,
                'window_left': -5,
                'window_right': 5,

                'limit_searching': _tr('wl_settings_default', 'None'),

                'test_statistical_significance': 'pearsons_chi_squared_test',
                'measure_bayes_factor': 'log_likelihood_ratio_test',
                'measure_effect_size': 'pmi'
            },

            'table_settings': {
                'show_pct_data': True,
                'show_cum_data': False,
                'show_breakdown_span_position': True,
                'show_breakdown_file': True
            },

            'fig_settings': {
                'graph_type': _tr('wl_settings_default', 'Line chart'),
                'sort_by_file': _tr('wl_settings_default', 'Total'),
                'use_data': _tr('wl_settings_default', 'p-value'),
                'use_pct': False,
                'use_cumulative': False,

                'rank_min': 1,
                'rank_min_no_limit': True,
                'rank_max': 50,
                'rank_max_no_limit': False
            },

            'filter_results': {
                'file_to_filter': _tr('wl_settings_default', 'Total'),

                'len_collocate_min': 1,
                'len_collocate_min_no_limit': True,
                'len_collocate_max': 20,
                'len_collocate_max_no_limit': True,

                'freq_position': _tr('wl_settings_default', 'Total'),
                'freq_min': 0,
                'freq_min_no_limit': True,
                'freq_max': 1000,
                'freq_max_no_limit': True,

                'test_stat_min': -100,
                'test_stat_min_no_limit': True,
                'test_stat_max': 100,
                'test_stat_max_no_limit': True,

                'p_val_min': 0,
                'p_val_min_no_limit': True,
                'p_val_max': 0.05,
                'p_val_max_no_limit': True,

                'bayes_factor_min': -100,
                'bayes_factor_min_no_limit': True,
                'bayes_factor_max': 100,
                'bayes_factor_max_no_limit': True,

                'effect_size_min': -100,
                'effect_size_min_no_limit': True,
                'effect_size_max': 100,
                'effect_size_max_no_limit': True,

                'num_files_found_min': 1,
                'num_files_found_min_no_limit': True,
                'num_files_found_max': 100,
                'num_files_found_max_no_limit': True
            },

            'search_results': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'match_case': False,
                'match_whole_words': False,
                'match_inflected_forms': False,
                'use_regex': False,
                'match_without_tags': False,
                'match_tags': False
            },
        },

        'keyword_extractor': {
            'token_settings': {
                'words': True,
                'all_lowercase': True,
                'all_uppercase': True,
                'title_case': True,
                'nums': True,
                'punc_marks': False,

                'treat_as_all_lowercase': False,
                'apply_lemmatization': False,
                'filter_stop_words': False,

                'assign_pos_tags': False,
                'ignore_tags': False,
                'use_tags': False
            },

            'generation_settings': {
                'test_statistical_significance': 'pearsons_chi_squared_test',
                'measure_bayes_factor': 'log_likelihood_ratio_test',
                'measure_effect_size': 'or',
            },

            'table_settings': {
                'show_pct_data': True,
                'show_cum_data': False,
                'show_breakdown_file': True
            },

            'fig_settings': {
                'graph_type': _tr('wl_settings_default', 'Line chart'),
                'sort_by_file': _tr('wl_settings_default', 'Total'),
                'use_data': _tr('wl_settings_default', 'p-value'),
                'use_pct': False,
                'use_cumulative': False,

                'rank_min': 1,
                'rank_min_no_limit': True,
                'rank_max': 50,
                'rank_max_no_limit': False
            },

            'filter_results': {
                'file_to_filter': _tr('wl_settings_default', 'Total'),

                'len_keyword_min': 1,
                'len_keyword_min_no_limit': True,
                'len_keyword_max': 20,
                'len_keyword_max_no_limit': True,

                'freq_min': 0,
                'freq_min_no_limit': True,
                'freq_max': 1000,
                'freq_max_no_limit': True,

                'test_stat_min': -100,
                'test_stat_min_no_limit': True,
                'test_stat_max': 100,
                'test_stat_max_no_limit': True,

                'p_val_min': 0,
                'p_val_min_no_limit': True,
                'p_val_max': 0.05,
                'p_val_max_no_limit': True,

                'bayes_factor_min': -100,
                'bayes_factor_min_no_limit': True,
                'bayes_factor_max': 100,
                'bayes_factor_max_no_limit': True,

                'effect_size_min': -100,
                'effect_size_min_no_limit': True,
                'effect_size_max': 100,
                'effect_size_max_no_limit': True,

                'num_files_found_min': 1,
                'num_files_found_min_no_limit': True,
                'num_files_found_max': 100,
                'num_files_found_max_no_limit': True
            },

            'search_results': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'match_case': False,
                'match_whole_words': False,
                'match_inflected_forms': False,
                'use_regex': False,
                'match_without_tags': False,
                'match_tags': False
            }
        },

        'settings': {
            'node_cur': _tr('wl_settings_default', 'General')
        },

        # Settings - General
        'general': {
            'ui_settings': {
                'interface_scaling': DEFAULT_INTERFACE_SCALING,
                'font_family': DEFAULT_FONT_FAMILY,
                'font_size': DEFAULT_FONT_SIZE
            },

            'proxy_settings': {
                'use_proxy': False,
                'address': '',
                'port': '',
                'username': '',
                'password': ''
            },

            'update_settings': {
                'check_updates_on_startup': True
            },

            'misc_settings': {
                'confirm_on_exit': True
            },

            # Settings - General - Import
            'imp': {
                'files': {
                    'default_path': DEFAULT_DIR_WORDLESS
                },

                'search_terms': {
                    'default_path': DEFAULT_DIR_WORDLESS,
                    'default_encoding': 'utf_8',
                    'detect_encodings': True
                },

                'stop_words': {
                    'default_path': DEFAULT_DIR_WORDLESS,
                    'default_encoding': 'utf_8',
                    'detect_encodings': True
                },

                'temp_files': {
                    'default_path': DEFAULT_DIR_IMPS,
                }
            },

            # Settings - General - Export
            'exp': {
                'tables': {
                    'default_path': DEFAULT_DIR_EXPS,
                    'default_type': _tr('wl_settings_default', 'Excel workbooks (*.xlsx)'),
                    'default_encoding': 'utf_8'
                },

                'search_terms': {
                    'default_path': DEFAULT_DIR_EXPS,
                    'default_encoding': 'utf_8'
                },

                'stop_words': {
                    'default_path': DEFAULT_DIR_EXPS,
                    'default_encoding': 'utf_8'
                }
            }
        },

        # Settings - Files
        'files': {
            'default_settings': {
                'encoding': 'utf_8',
                'lang': 'eng_us',
                'tokenized': False,
                'tagged': False
            },

            'auto_detection_settings': {
                'num_lines': 100,
                'num_lines_no_limit': False
            },

            'misc_settings': {
                'read_files_in_chunks': 10
            },

            # Settings - Files - Tags
            'tags': {
                'header_tag_settings': [
                    [_tr('wl_settings_default', 'Non-embedded'), _tr('wl_settings_default', 'Header'), '<teiHeader>', '</teiHeader>']
                ],

                'body_tag_settings': [
                    [_tr('wl_settings_default', 'Embedded'), _tr('wl_settings_default', 'Part of speech'), '_*', 'N/A'],
                    [_tr('wl_settings_default', 'Embedded'), _tr('wl_settings_default', 'Part of speech'), '/*', 'N/A'],
                    [_tr('wl_settings_default', 'Non-embedded'), _tr('wl_settings_default', 'Others'), '<*>', 'N/A']
                ],

                'xml_tag_settings': [
                    [_tr('wl_settings_default', 'Non-embedded'), _tr('wl_settings_default', 'Paragraph'), '<p>', '</p>'],
                    [_tr('wl_settings_default', 'Non-embedded'), _tr('wl_settings_default', 'Sentence'), '<s>', '</s>'],
                    [_tr('wl_settings_default', 'Non-embedded'), _tr('wl_settings_default', 'Word'), '<w>', '</w>'],
                    [_tr('wl_settings_default', 'Non-embedded'), _tr('wl_settings_default', 'Word'), '<c>', '</c>']
                ]
            }
        },

        # Settings - Sentence Tokenization
        'sentence_tokenization': {
            'sentence_tokenizer_settings': {
                'afr': 'stanza_afr',
                'ara': 'stanza_ara',
                'hye': 'stanza_hye',
                'hyw': 'stanza_hyw',
                'eus': 'stanza_eus',
                'bel': 'stanza_bel',
                'bul': 'stanza_bul',
                'mya': 'stanza_mya',
                'bxr': 'stanza_bxr',
                'cat': 'spacy_dependency_parser_cat',
                'lzh': 'stanza_lzh',
                'zho_cn': 'spacy_dependency_parser_zho',
                'zho_tw': 'spacy_dependency_parser_zho',
                'chu': 'stanza_chu',
                'cop': 'stanza_cop',
                'hrv': 'spacy_dependency_parser_hrv',
                'ces': 'stanza_ces',
                'dan': 'spacy_dependency_parser_dan',
                'nld': 'spacy_dependency_parser_nld',
                'eng_gb': 'spacy_dependency_parser_eng',
                'eng_us': 'spacy_dependency_parser_eng',
                'myv': 'stanza_myv',
                'est': 'stanza_est',
                'fao': 'stanza_fao',
                'fin': 'spacy_dependency_parser_fin',
                'fra': 'spacy_dependency_parser_fra',
                'fro': 'stanza_fro',
                'glg': 'stanza_glg',
                'deu_at': 'spacy_dependency_parser_deu',
                'deu_de': 'spacy_dependency_parser_deu',
                'deu_ch': 'spacy_dependency_parser_deu',
                'got': 'stanza_got',
                'grc': 'stanza_grc',
                'ell': 'spacy_dependency_parser_ell',
                'hbo': 'stanza_hbo',
                'heb': 'stanza_heb',
                'hin': 'stanza_hin',
                'hun': 'stanza_hun',
                'isl': 'stanza_isl',
                'ind': 'stanza_ind',
                'gle': 'stanza_gle',
                'ita': 'spacy_dependency_parser_ita',
                'jpn': 'spacy_dependency_parser_jpn',
                'khm': 'khmer_nltk_khm',
                'kaz': 'stanza_kaz',
                'kor': 'spacy_dependency_parser_kor',
                'kmr': 'stanza_kmr',
                'kir': 'stanza_kir',
                'lao': 'laonlp_lao',
                'lat': 'stanza_lat',
                'lav': 'stanza_lav',
                'lij': 'stanza_lij',
                'lit': 'spacy_dependency_parser_lit',
                'mkd': 'spacy_dependency_parser_mkd',
                'mal': 'nltk_punkt_mal',
                'mlt': 'stanza_mlt',
                'glv': 'stanza_glv',
                'mar': 'stanza_mar',
                'pcm': 'stanza_pcm',
                'nob': 'spacy_dependency_parser_nob',
                'nno': 'stanza_nno',
                'fas': 'stanza_fas',
                'pol': 'spacy_dependency_parser_pol',
                'qpm': 'stanza_qpm',
                'por_br': 'spacy_dependency_parser_por',
                'por_pt': 'spacy_dependency_parser_por',
                'ron': 'spacy_dependency_parser_ron',
                'rus': 'spacy_dependency_parser_rus',
                'orv': 'stanza_orv',
                'sme': 'stanza_sme',
                'san': 'stanza_san',
                'gla': 'stanza_gla',
                'srp_latn': 'stanza_srp_latn',
                'snd': 'stanza_snd',
                'slk': 'stanza_slk',
                'slv': 'spacy_dependency_parser_slv',
                'hsb': 'stanza_hsb',
                'spa': 'spacy_dependency_parser_spa',
                'swe': 'spacy_dependency_parser_swe',
                'tam': 'stanza_tam',
                'tel': 'stanza_tel',
                'tha': 'pythainlp_crfcut',
                'bod': 'botok_bod',
                'tur': 'stanza_tur',
                'ukr': 'spacy_dependency_parser_ukr',
                'urd': 'stanza_urd',
                'uig': 'stanza_uig',
                'vie': 'underthesea_vie',
                'cym': 'stanza_cym',
                'wol': 'stanza_wol',

                'other': 'spacy_sentencizer'
            },

            'preview': {
                'preview_lang': 'eng_us',
                'preview_samples': '',
                'preview_results': ''
            }
        },

        # Settings - Word Tokenization
        'word_tokenization': {
            'word_tokenizer_settings': {
                'afr': 'stanza_afr',
                'sqi': 'spacy_sqi',
                'amh': 'spacy_amh',
                'ara': 'stanza_ara',
                'hye': 'stanza_hye',
                'hyw': 'stanza_hyw',
                'asm': 'sacremoses_moses',
                'aze': 'spacy_aze',
                'eus': 'stanza_eus',
                'ben': 'sacremoses_moses',
                'bel': 'stanza_bel',
                'bul': 'stanza_bul',
                'mya': 'stanza_mya',
                'bxr': 'stanza_bxr',
                'cat': 'spacy_cat',
                'lzh': 'stanza_lzh',
                'zho_cn': 'spacy_zho',
                'zho_tw': 'spacy_zho',
                'chu': 'stanza_chu',
                'cop': 'stanza_cop',
                'hrv': 'spacy_hrv',
                'ces': 'stanza_ces',
                'dan': 'spacy_dan',
                'nld': 'spacy_nld',
                'eng_gb': 'spacy_eng',
                'eng_us': 'spacy_eng',
                'myv': 'stanza_myv',
                'est': 'stanza_est',
                'fao': 'stanza_fao',
                'fin': 'spacy_fin',
                'fra': 'spacy_fra',
                'fro': 'stanza_fro',
                'glg': 'stanza_glg',
                'lug': 'spacy_lug',
                'deu_at': 'spacy_deu',
                'deu_de': 'spacy_deu',
                'deu_ch': 'spacy_deu',
                'got': 'stanza_got',
                'grc': 'stanza_grc',
                'ell': 'spacy_ell',
                'guj': 'sacremoses_moses',
                'hbo': 'stanza_hbo',
                'heb': 'stanza_heb',
                'hin': 'stanza_hin',
                'hun': 'stanza_hun',
                'isl': 'stanza_isl',
                'ind': 'stanza_ind',
                'gle': 'stanza_gle',
                'ita': 'spacy_ita',
                'jpn': 'spacy_jpn',
                'kan': 'sacremoses_moses',
                'kaz': 'stanza_kaz',
                'khm': 'khmer_nltk_khm',
                'kor': 'spacy_kor',
                'kmr': 'stanza_kmr',
                'kir': 'stanza_kir',
                'lao': 'laonlp_lao',
                'lat': 'stanza_lat',
                'lav': 'stanza_lav',
                'lij': 'stanza_lij',
                'lit': 'spacy_lit',
                'ltz': 'spacy_ltz',
                'mkd': 'spacy_mkd',
                'msa': 'spacy_msa',
                'mal': 'sacremoses_moses',
                'mlt': 'stanza_mlt',
                'glv': 'stanza_glv',
                'mar': 'stanza_mar',
                'pcm': 'stanza_pcm',
                'mni': 'sacremoses_moses',
                'nep': 'spacy_nep',
                'nob': 'spacy_nob',
                'nno': 'stanza_nno',
                'ori': 'sacremoses_moses',
                'fas': 'stanza_fas',
                'pol': 'spacy_pol',
                'qpm': 'stanza_qpm',
                'por_br': 'spacy_por',
                'por_pt': 'spacy_por',
                'pan_guru': 'sacremoses_moses',
                'ron': 'spacy_ron',
                'rus': 'spacy_rus',
                'orv': 'stanza_orv',
                'sme': 'stanza_sme',
                'san': 'stanza_san',
                'gla': 'stanza_gla',
                'srp_cyrl': 'spacy_srp',
                'srp_latn': 'stanza_srp_latn',
                'snd': 'stanza_snd',
                'sin': 'spacy_sin',
                'slk': 'stanza_slk',
                'slv': 'spacy_slv',
                'dsb': 'spacy_dsb',
                'hsb': 'stanza_hsb',
                'spa': 'spacy_spa',
                'swe': 'spacy_swe',
                'tgl': 'spacy_tgl',
                'tgk': 'nltk_tok_tok',
                'tam': 'stanza_tam',
                'tat': 'spacy_tat',
                'tel': 'stanza_tel',
                'tdt': 'sacremoses_moses',
                'tha': 'pythainlp_max_matching_tcc',
                'bod': 'botok_bod',
                'tir': 'spacy_tir',
                'tsn': 'spacy_tsn',
                'tur': 'stanza_tur',
                'ukr': 'spacy_ukr',
                'urd': 'stanza_urd',
                'uig': 'stanza_uig',
                'vie': 'underthesea_vie',
                'cym': 'stanza_cym',
                'wol': 'stanza_wol',
                'yor': 'spacy_yor',

                'other': 'spacy_eng'
            },

            'preview': {
                'preview_lang': 'eng_us',
                'preview_samples': '',
                'preview_results': ''
            }
        },

        # Settings - Syllable Tokenization
        'syl_tokenization': {
            'syl_tokenizer_settings': {
                'afr': 'pyphen_afr',
                'sqi': 'pyphen_sqi',
                'bel': 'pyphen_bel',
                'bul': 'pyphen_bul',
                'cat': 'pyphen_cat',
                'hrv': 'pyphen_hrv',
                'ces': 'pyphen_ces',
                'dan': 'pyphen_dan',
                'nld': 'pyphen_nld',
                'eng_gb': 'pyphen_eng_gb',
                'eng_us': 'pyphen_eng_us',
                'epo': 'pyphen_epo',
                'est': 'pyphen_est',
                'fra': 'pyphen_fra',
                'glg': 'pyphen_glg',
                'deu_at': 'pyphen_deu_at',
                'deu_de': 'pyphen_deu_de',
                'deu_ch': 'pyphen_deu_ch',
                'ell': 'pyphen_ell',
                'hun': 'pyphen_hun',
                'isl': 'pyphen_isl',
                'ind': 'pyphen_ind',
                'ita': 'pyphen_ita',
                'lit': 'pyphen_lit',
                'lav': 'pyphen_lav',
                'mon': 'pyphen_mon',
                'nob': 'pyphen_nob',
                'nno': 'pyphen_nno',
                'pol': 'pyphen_pol',
                'por_br': 'pyphen_por_br',
                'por_pt': 'pyphen_por_pt',
                'ron': 'pyphen_ron',
                'rus': 'pyphen_rus',
                'srp_cyrl': 'pyphen_srp_cyrl',
                'srp_latn': 'pyphen_srp_latn',
                'slk': 'pyphen_slk',
                'slv': 'pyphen_slv',
                'spa': 'pyphen_spa',
                'swe': 'pyphen_swe',
                'tel': 'pyphen_tel',
                'tha': 'pythainlp_tha',
                'ukr': 'pyphen_ukr',
                'zul': 'pyphen_zul'
            },

            'preview': {
                'preview_lang': 'eng_us',
                'preview_samples': '',
                'preview_results': ''
            }
        },

        # Settings - POS Tagging
        'pos_tagging': {
            'pos_tagger_settings': {
                'pos_taggers': {
                    'afr': 'stanza_afr',
                    'ara': 'stanza_ara',
                    'hye': 'stanza_hye',
                    'hyw': 'stanza_hyw',
                    'eus': 'stanza_eus',
                    'bel': 'stanza_bel',
                    'bul': 'stanza_bul',
                    'bxr': 'stanza_bxr',
                    'cat': 'spacy_cat',
                    'lzh': 'stanza_lzh',
                    'zho_cn': 'spacy_zho',
                    'zho_tw': 'spacy_zho',
                    'chu': 'stanza_chu',
                    'cop': 'stanza_cop',
                    'hrv': 'spacy_hrv',
                    'ces': 'stanza_ces',
                    'dan': 'spacy_dan',
                    'nld': 'spacy_nld',
                    'eng_gb': 'spacy_eng',
                    'eng_us': 'spacy_eng',
                    'myv': 'stanza_myv',
                    'est': 'stanza_est',
                    'fao': 'stanza_fao',
                    'fin': 'spacy_fin',
                    'fra': 'spacy_fra',
                    'fro': 'stanza_fro',
                    'glg': 'stanza_glg',
                    'deu_at': 'spacy_deu',
                    'deu_de': 'spacy_deu',
                    'deu_ch': 'spacy_deu',
                    'got': 'stanza_got',
                    'grc': 'stanza_grc',
                    'ell': 'spacy_ell',
                    'hbo': 'stanza_hbo',
                    'heb': 'stanza_heb',
                    'hin': 'stanza_hin',
                    'hun': 'stanza_hun',
                    'isl': 'stanza_isl',
                    'ind': 'stanza_ind',
                    'gle': 'stanza_gle',
                    'ita': 'spacy_ita',
                    'jpn': 'spacy_jpn',
                    'kaz': 'stanza_kaz',
                    'khm': 'khmer_nltk_khm',
                    'kor': 'spacy_kor',
                    'kmr': 'stanza_kmr',
                    'kir': 'stanza_kir',
                    'lao': 'laonlp_seqlabeling',
                    'lat': 'stanza_lat',
                    'lav': 'stanza_lav',
                    'lij': 'stanza_lij',
                    'lit': 'spacy_lit',
                    'mkd': 'spacy_mkd',
                    'mlt': 'stanza_mlt',
                    'glv': 'stanza_glv',
                    'mar': 'stanza_mar',
                    'pcm': 'stanza_pcm',
                    'nob': 'spacy_nob',
                    'nno': 'stanza_nno',
                    'fas': 'stanza_fas',
                    'pol': 'spacy_pol',
                    'qpm': 'stanza_qpm',
                    'por_br': 'spacy_por',
                    'por_pt': 'spacy_por',
                    'ron': 'spacy_ron',
                    'rus': 'spacy_rus',
                    'orv': 'stanza_orv',
                    'sme': 'stanza_sme',
                    'san': 'stanza_san',
                    'gla': 'stanza_gla',
                    'srp_latn': 'stanza_srp_latn',
                    'slk': 'stanza_slk',
                    'slv': 'spacy_slv',
                    'hsb': 'stanza_hsb',
                    'spa': 'spacy_spa',
                    'swe': 'spacy_swe',
                    'tam': 'stanza_tam',
                    'tel': 'stanza_tel',
                    'tha': 'pythainlp_perceptron_pud',
                    'bod': 'botok_bod',
                    'tur': 'stanza_tur',
                    'ukr': 'spacy_ukr',
                    'urd': 'stanza_urd',
                    'uig': 'stanza_uig',
                    'vie': 'underthesea_vie',
                    'cym': 'stanza_cym',
                    'wol': 'stanza_wol'
                },

                'to_universal_pos_tags': False
            },

            'preview': {
                'preview_lang': 'eng_us',
                'preview_samples': '',
                'preview_results': ''
            },

            # Settings - POS Tagging - Tagsets
            'tagsets': {
                'preview_settings': {
                    'preview_lang': 'eng_us',
                    'preview_pos_tagger': {}
                },

                'mapping_settings': {
                    'eng_gb': {
                        'nltk_perceptron_eng': wl_tagset_eng_penn_treebank.MAPPINGS,
                    },
                    'eng_us': {
                        'nltk_perceptron_eng': wl_tagset_eng_penn_treebank.MAPPINGS,
                    },

                    'jpn': {
                        'sudachipy_jpn': wl_tagset_jpn_unidic.MAPPINGS
                    },

                    'khm': {
                        'khmer_nltk_khm': wl_tagset_khm_alt.MAPPINGS
                    },

                    'kor': {
                        'python_mecab_ko_mecab': wl_tagset_kor_mecab.MAPPINGS
                    },

                    'lao': {
                        'laonlp_seqlabeling': wl_tagset_lao_seqlabeling.MAPPINGS,
                        'laonlp_yunshan_cup_2020': wl_tagset_lao_yunshan_cup_2020.MAPPINGS
                    },

                    'rus': {
                        'nltk_perceptron_rus': wl_tagset_rus_russian_national_corpus.MAPPINGS,
                        'pymorphy3_morphological_analyzer': wl_tagset_rus_open_corpora.MAPPINGS
                    },

                    'tha': {
                        'pythainlp_perceptron_blackboard': wl_tagset_tha_blackboard.MAPPINGS,
                        'pythainlp_perceptron_orchid': wl_tagset_tha_orchid.MAPPINGS,
                        'pythainlp_perceptron_pud': wl_tagset_universal.MAPPINGS
                    },

                    'bod': {
                        'botok_bod': wl_tagset_bod_botok.MAPPINGS
                    },

                    'ukr': {
                        'pymorphy3_morphological_analyzer': wl_tagset_rus_open_corpora.MAPPINGS
                    },

                    'vie': {
                        'underthesea_vie': wl_tagset_vie_underthesea.MAPPINGS
                    }
                }
            }
        },

        # Settings - Lemmatization
        'lemmatization': {
            'lemmatizer_settings': {
                'afr': 'stanza_afr',
                'sqi': 'simplemma_sqi',
                'ara': 'stanza_ara',
                'hye': 'stanza_hye',
                'hyw': 'stanza_hyw',
                'ast': 'simplemma_ast',
                'eus': 'stanza_eus',
                'bel': 'stanza_bel',
                'ben': 'spacy_ben',
                'bul': 'stanza_bul',
                'bxr': 'stanza_bxr',
                'cat': 'spacy_cat',
                'lzh': 'stanza_lzh',
                'zho_cn': 'stanza_zho_cn',
                'zho_tw': 'stanza_zho_tw',
                'chu': 'stanza_chu',
                'cop': 'stanza_cop',
                'hrv': 'spacy_hrv',
                'ces': 'stanza_ces',
                'dan': 'spacy_dan',
                'nld': 'spacy_nld',
                'enm': 'simplemma_enm',
                'eng_gb': 'spacy_eng',
                'eng_us': 'spacy_eng',
                'myv': 'stanza_myv',
                'est': 'stanza_est',
                'fin': 'spacy_fin',
                'fra': 'spacy_fra',
                'fro': 'stanza_fro',
                'glg': 'stanza_glg',
                'kat': 'simplemma_kat',
                'deu_at': 'spacy_deu',
                'deu_de': 'spacy_deu',
                'deu_ch': 'spacy_deu',
                'got': 'stanza_got',
                'grc': 'stanza_grc',
                'ell': 'spacy_ell',
                'hbo': 'stanza_hbo',
                'heb': 'stanza_heb',
                'hin': 'stanza_hin',
                'hun': 'stanza_hun',
                'isl': 'stanza_isl',
                'ind': 'stanza_ind',
                'gle': 'stanza_gle',
                'ita': 'spacy_ita',
                'jpn': 'spacy_jpn',
                'kaz': 'stanza_kaz',
                'kor': 'spacy_kor',
                'kmr': 'stanza_kmr',
                'kir': 'stanza_kir',
                'lat': 'stanza_lat',
                'lav': 'stanza_lav',
                'lij': 'stanza_lij',
                'lit': 'spacy_lit',
                'ltz': 'simplemma_ltz',
                'mkd': 'spacy_mkd',
                'msa': 'simplemma_msa',
                'glv': 'stanza_glv',
                'mar': 'stanza_mar',
                'pcm': 'stanza_pcm',
                'nob': 'spacy_nob',
                'nno': 'stanza_nno',
                'fas': 'stanza_fas',
                'pol': 'spacy_pol',
                'qpm': 'stanza_qpm',
                'por_br': 'spacy_por',
                'por_pt': 'spacy_por',
                'ron': 'spacy_ron',
                'rus': 'spacy_rus',
                'orv': 'stanza_orv',
                'sme': 'stanza_sme',
                'san': 'stanza_san',
                'gla': 'stanza_gla',
                'srp_cyrl': 'spacy_srp',
                'srp_latn': 'stanza_srp_latn',
                'slk': 'stanza_slk',
                'slv': 'spacy_slv',
                'hsb': 'stanza_hsb',
                'spa': 'spacy_spa',
                'swa': 'simplemma_swa',
                'swe': 'spacy_swe',
                'tgl': 'simplemma_tgl',
                'tam': 'stanza_tam',
                'bod': 'botok_bod',
                'tur': 'stanza_tur',
                'ukr': 'spacy_ukr',
                'urd': 'stanza_urd',
                'uig': 'stanza_uig',
                'cym': 'stanza_cym',
                'wol': 'stanza_wol'
            },

            'preview': {
                'preview_lang': 'eng_us',
                'preview_samples': '',
                'preview_results': ''
            }
        },

        # Settings - Stop Word Lists
        'stop_word_lists': {
            'stop_word_list_settings': {
                'ara': 'nltk_ara',
                'aze': 'nltk_aze',
                'eus': 'nltk_eus',
                'ben': 'nltk_ben',
                'cat': 'nltk_cat',
                'zho_cn': 'nltk_zho_cn',
                'zho_tw': 'nltk_zho_tw',
                'dan': 'nltk_dan',
                'nld': 'nltk_nld',
                'eng_gb': 'nltk_eng',
                'eng_us': 'nltk_eng',
                'fin': 'nltk_fin',
                'fra': 'nltk_fra',
                'deu_at': 'nltk_deu',
                'deu_de': 'nltk_deu',
                'deu_ch': 'nltk_deu',
                'ell': 'nltk_ell',
                'heb': 'nltk_heb',
                'hun': 'nltk_hun',
                'ind': 'nltk_ind',
                'ita': 'nltk_ita',
                'kaz': 'nltk_kaz',
                'lao': 'laonlp_lao',
                'nep': 'nltk_nep',
                'nob': 'nltk_nor',
                'nno': 'nltk_nor',
                'por_br': 'nltk_por',
                'por_pt': 'nltk_por',
                'ron': 'nltk_ron',
                'rus': 'nltk_rus',
                'slv': 'nltk_slv',
                'spa': 'nltk_spa',
                'swe': 'nltk_swe',
                'tgk': 'nltk_tgk',
                'tha': 'pythainlp_tha',
                'tur': 'nltk_tur',

                'other': 'custom'
            },

            'custom_lists': {},

            'preview': {
                'preview_lang': 'eng_us'
            }
        },

        # Settings - Dependency Parsing
        'dependency_parsing': {
            'dependency_parser_settings': {
                'afr': 'stanza_afr',
                'ara': 'stanza_ara',
                'hye': 'stanza_hye',
                'hyw': 'stanza_hyw',
                'eus': 'stanza_eus',
                'bel': 'stanza_bel',
                'bul': 'stanza_bul',
                'bxr': 'stanza_bxr',
                'cat': 'spacy_cat',
                'lzh': 'stanza_lzh',
                'zho_cn': 'spacy_zho',
                'zho_tw': 'spacy_zho',
                'chu': 'stanza_chu',
                'cop': 'stanza_cop',
                'hrv': 'spacy_hrv',
                'ces': 'stanza_ces',
                'dan': 'spacy_dan',
                'nld': 'spacy_nld',
                'eng_gb': 'spacy_eng',
                'eng_us': 'spacy_eng',
                'myv': 'stanza_myv',
                'est': 'stanza_est',
                'fao': 'stanza_fao',
                'fin': 'spacy_fin',
                'fra': 'spacy_fra',
                'fro': 'stanza_fro',
                'glg': 'stanza_glg',
                'deu_at': 'spacy_deu',
                'deu_de': 'spacy_deu',
                'deu_ch': 'spacy_deu',
                'got': 'stanza_got',
                'grc': 'stanza_grc',
                'ell': 'spacy_ell',
                'hbo': 'stanza_hbo',
                'heb': 'stanza_heb',
                'hin': 'stanza_hin',
                'hun': 'stanza_hun',
                'isl': 'stanza_isl',
                'ind': 'stanza_ind',
                'gle': 'stanza_gle',
                'ita': 'spacy_ita',
                'jpn': 'spacy_jpn',
                'kaz': 'stanza_kaz',
                'kor': 'spacy_kor',
                'kmr': 'stanza_kmr',
                'kir': 'stanza_kir',
                'lat': 'stanza_lat',
                'lav': 'stanza_lav',
                'lij': 'stanza_lij',
                'lit': 'spacy_lit',
                'mkd': 'spacy_mkd',
                'mlt': 'stanza_mlt',
                'glv': 'stanza_glv',
                'mar': 'stanza_mar',
                'pcm': 'stanza_pcm',
                'nob': 'spacy_nob',
                'nno': 'stanza_nno',
                'fas': 'stanza_fas',
                'pol': 'spacy_pol',
                'qpm': 'stanza_qpm',
                'por_br': 'spacy_por',
                'por_pt': 'spacy_por',
                'ron': 'spacy_ron',
                'rus': 'spacy_rus',
                'orv': 'stanza_orv',
                'sme': 'stanza_sme',
                'san': 'stanza_san',
                'gla': 'stanza_gla',
                'srp_latn': 'stanza_srp_latn',
                'slk': 'stanza_slk',
                'slv': 'spacy_slv',
                'hsb': 'stanza_hsb',
                'spa': 'spacy_spa',
                'swe': 'spacy_swe',
                'tam': 'stanza_tam',
                'tel': 'stanza_tel',
                'tur': 'stanza_tur',
                'ukr': 'spacy_ukr',
                'urd': 'stanza_urd',
                'uig': 'stanza_uig',
                'vie': 'stanza_vie',
                'cym': 'stanza_cym',
                'wol': 'stanza_wol'
            },

            'preview': {
                'preview_lang': 'eng_us',

                'preview_settings': {
                    'show_pos_tags': True,
                    'show_fine_grained_pos_tags': False,
                    'show_lemmas': False,
                    'collapse_punc_marks': True,
                    'compact_mode': False,
                    'show_in_separate_tab': False
                },

                'preview_samples': ''
            }
        },

        # Settings - Sentiment Analysis
        'sentiment_analysis': {
            'sentiment_analyzer_settings': {
                'zho_cn': 'stanza_zho_cn',
                'eng_gb': 'stanza_eng',
                'eng_us': 'stanza_eng',
                'deu_at': 'stanza_deu',
                'deu_de': 'stanza_deu',
                'deu_ch': 'stanza_deu',
                'mar': 'stanza_mar',
                'rus': 'dostoevsky_rus',
                'spa': 'stanza_spa',
                'vie': 'underthesea_vie'
            },

            'preview': {
                'preview_lang': 'eng_us',
                'preview_samples': '',
                'preview_sentiment_score': '0',
            }
        },

        # Settings - Tables
        'tables': {
            'rank_settings': {
                'continue_numbering_after_ties': False
            },

            'precision_settings': {
                'precision_decimals': 3,
                'precision_pcts': 3,
                'precision_p_vals': 5
            },

            # Settings - Tables - Concordancer
            'concordancer': {
                'sorting_settings': {
                    'highlight_colors': {
                        'lvl_1': '#FF0000', # Red
                        'lvl_2': '#C2691D', # Orange
                        'lvl_3': '#CBBE00', # Yellow
                        'lvl_4': '#3F864C', # Green
                        'lvl_5': '#264E8C', # Blue
                        'lvl_6': '#491D76', # Purple
                    }
                }
            },

            # Settings - Tables - Parallel Concordancer
            'parallel_concordancer': {
                'color_settings': {
                    'search_term_color': '#FF0000' # Red
                }
            }
        },

        # Settings - Measures
        'measures': {
            # Settings - Measures - Readability
            'readability': {
                'rd': {
                    'variant': _tr('wl_settings_default', 'Policy one')
                },

                'ari': {
                    'use_navy_variant': False
                },

                'bormuths_gp': {
                    'cloze_criterion_score': 35
                },

                'colemans_readability_formula': {
                    'variant': '2'
                },

                'x_c50': {
                    'variant': _tr('wl_settings_default', 'New')
                },

                'danielson_bryans_readability_formula': {
                    'variant': '1'
                },

                'fog_index': {
                    'variant_eng': _tr('wl_settings_default', 'Original')
                },

                're': {
                    'use_powers_sumner_kearl_variant_for_all_langs': False,
                    'variant_nld': 'Douma',
                    'variant_spa': 'Fernández Huerta'
                },

                're_farr_jenkins_paterson': {
                    'use_powers_sumner_kearl_variant': False
                },

                'lorge_readability_index': {
                    'use_corrected_formula': True
                },

                'nwl': {
                    'variant': '1'
                },

                'nws': {
                    'variant': '1'
                },

                'spache_grade_lvl': {
                    'use_rev_formula': True
                },

                'trankle_bailers_readability_formula': {
                    'variant': '1'
                }
            },

            # Settings - Measures - Lexical Diversity
            'lexical_diversity': {
                'hdd': {
                    'sample_size': 42
                },

                'logttr': {
                    'variant': 'Herdan'
                },

                'msttr': {
                    'num_tokens_in_each_seg': 100
                },

                'mtld': {
                    'factor_size': 0.720
                },

                'mattr': {
                    'window_size': 500
                },

                'repeat_rate': {
                    'use_data': _tr('wl_settings_default', 'Rank-frequency distribution')
                },

                'shannon_entropy': {
                    'use_data': _tr('wl_settings_default', 'Rank-frequency distribution')
                }
            },

            # Settings - Measures - Dispersion
            'dispersion': {
                'general_settings': {
                    'num_sub_sections': 5
                },

                'griess_dp': {
                    'apply_normalization': True
                }
            },

            # Settings - Measures - Adjusted Frequency
            'adjusted_freq': {
                'general_settings': {
                    'num_sub_sections': 5
                }
            },

            # Settings - Measures - Statistical Significance
            'statistical_significance': {
                'fishers_exact_test': {
                    'direction': _tr('wl_settings_default', 'Two-tailed')
                },

                'log_likelihood_ratio_test': {
                    'apply_correction': False
                },

                'mann_whitney_u_test': {
                    'num_sub_sections': 5,
                    'use_data': _tr('wl_settings_default', 'Relative frequency'),
                    'direction': _tr('wl_settings_default', 'Two-tailed'),
                    'apply_correction': True
                },

                'pearsons_chi_squared_test': {
                    'apply_correction': False
                },

                'students_t_test_1_sample': {
                    'direction': _tr('wl_settings_default', 'Two-tailed')
                },

                'students_t_test_2_sample': {
                    'num_sub_sections': 5,
                    'use_data': _tr('wl_settings_default', 'Relative frequency'),
                    'direction': _tr('wl_settings_default', 'Two-tailed')
                },

                'welchs_t_test': {
                    'num_sub_sections': 5,
                    'use_data': _tr('wl_settings_default', 'Relative frequency'),
                    'direction': _tr('wl_settings_default', 'Two-tailed')
                },

                'z_score': {
                    'direction': _tr('wl_settings_default', 'Two-tailed')
                },

                'z_score_berry_rogghe': {
                    'direction': _tr('wl_settings_default', 'Two-tailed')
                }
            },

            # Settings - Measures - Bayes Factor
            'bayes_factor': {
                'log_likelihood_ratio_test': {
                    'apply_correction': False
                },

                'students_t_test_2_sample': {
                    'num_sub_sections': 5,
                    'use_data': _tr('wl_settings_default', 'Relative frequency'),
                    'direction': _tr('wl_settings_default', 'Two-tailed')
                }
            },

            # Settings - Measures - Effect Size
            'effect_size': {
                'kilgarriffs_ratio': {
                    'smoothing_param': 1.00
                }
            }
        },

        # Settings - Figures
        'figs': {
            # Settings - Figures - Line Charts
            'line_charts': {
                'general_settings': {
                    'font': DEFAULT_FONT_FAMILY
                }
            },

            # Settings - Figures - Word Clouds
            'word_clouds': {
                'font_settings': {
                    'font': 'GNU Unifont',
                    'font_path': '',

                    'font_size_min': 4,
                    'font_size_max': desktop_widget.height(),
                    # Auto
                    'relative_scaling': -0.01,

                    'font_color': _tr('wl_settings_default', 'Colormap'),
                    'font_color_monochrome': '#000000',
                    'font_color_colormap': 'viridis'
                },

                'bg_settings': {
                    'bg_color': '#FFFFFF',
                    'bg_color_transparent': False
                },

                'mask_settings': {
                    'mask_settings': False,
                    'mask_path': '',
                    'contour_width': 1,
                    'contour_color': '#000000'
                },

                'advanced_settings': {
                    'prefer_hor': 90,
                    'allow_repeated_words': False
                }
            },

            # Settings - Figures - Network Graphs
            'network_graphs': {
                'node_settings': {
                    'node_shape': 'o',
                    'node_size': 800,
                    'node_color': '#5C88C5',
                    'node_opacity': 1.0
                },

                'node_label_settings': {
                    'label_font': DEFAULT_FONT_FAMILY,
                    'label_font_size': DEFAULT_FONT_SIZE,
                    'label_font_weight': 400,
                    'label_font_color': '#000000',
                    'label_opacity': 1.0
                },

                'edge_settings': {
                    'connection_style': 'arc3',
                    'edge_width_min': .1,
                    'edge_width_max': 3,
                    'edge_style': 'solid',
                    'edge_color': '#000000',
                    'edge_opacity': 1.0,
                    'arrow_style': '-|>',
                    'arrow_size': 10
                },

                'edge_label_settings': {
                    'label_position': .5,
                    'rotate_labels': True,
                    'label_font': DEFAULT_FONT_FAMILY,
                    'label_font_size': DEFAULT_FONT_SIZE,
                    'label_font_weight': 400,
                    'label_font_color': '#000000',
                    'label_opacity': 1.0
                },

                'advanced_settings': {
                    'layout': networkx.spring_layout
                }
            }
        }
    }

    # Tagsets
    settings_default['pos_tagging']['tagsets']['preview_settings']['preview_pos_tagger'] = settings_default['pos_tagging']['pos_tagger_settings']['pos_taggers']

    # Custom stop word lists
    for lang in settings_default['stop_word_lists']['stop_word_list_settings']:
        settings_default['stop_word_lists']['custom_lists'][lang] = []

    return settings_default

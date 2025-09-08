# ----------------------------------------------------------------------
# Wordless: Settings - Default settings
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

import copy
import math

import networkx
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from wordless.wl_nlp import wl_pos_tagging
from wordless.wl_tagsets import (
    wl_tagset_cat_universal,
    wl_tagset_dan_universal,
    wl_tagset_eng_penn_treebank,
    wl_tagset_eng_universal,
    wl_tagset_ell_universal,
    wl_tagset_eus_universal,
    wl_tagset_fra_universal,
    wl_tagset_hun_universal,
    wl_tagset_hye_universal,
    wl_tagset_jpn_unidic,
    wl_tagset_khm_alt,
    wl_tagset_kor_mecab,
    wl_tagset_lao_seqlabeling,
    wl_tagset_lao_yunshan_cup_2020,
    wl_tagset_pcm_universal,
    wl_tagset_nor_universal,
    wl_tagset_por_universal,
    wl_tagset_rus_open_corpora,
    wl_tagset_rus_russian_national_corpus,
    wl_tagset_rus_universal,
    wl_tagset_spa_universal,
    wl_tagset_tha_blackboard,
    wl_tagset_tha_orchid,
    wl_tagset_xct_botok,
    wl_tagset_ukr_universal,
    wl_tagset_vie_underthesea,
    wl_tagset_xcl_universal
)
from wordless.wl_utils import (
    wl_misc,
    wl_paths
)

_tr = QtCore.QCoreApplication.translate
is_windows, is_macos, is_linux = wl_misc.check_os()

# The following settings need to be loaded before initialization of the main window
DEFAULT_INTERFACE_SCALING = '100%'

# Font family
if is_windows:
    DEFAULT_FONT_FAMILY = 'Arial'
elif is_macos:
    # SF Pro is the system font on macOS >= 10.13 but is not installed by default
    DEFAULT_FONT_FAMILY = 'Helvetica Neue'
elif is_linux:
    match wl_misc.get_linux_distro():
        case 'ubuntu':
            DEFAULT_FONT_FAMILY = 'Ubuntu'
        case 'debian':
            DEFAULT_FONT_FAMILY = 'DejaVu'
        case 'arch':
            DEFAULT_FONT_FAMILY = 'Noto Sans'

# Font size
if is_windows:
    DEFAULT_FONT_SIZE = 9
elif is_macos:
    DEFAULT_FONT_SIZE = 13
elif is_linux:
    DEFAULT_FONT_SIZE = 11

# Layouts
DEFAULT_HEIGHT_FILE_AREA = 210
DEFAULT_WIDHT_SETTINGS = 410

# Directories for imports and exports
DEFAULT_DIR_WORDLESS = wl_paths.get_path_file('', internal = False)
DEFAULT_DIR_IMPS = wl_paths.get_path_file('imports', internal = False)
DEFAULT_DIR_EXPS = wl_paths.get_path_file('exports', internal = False)

def init_settings_default(main):
    desktop_widget = QtWidgets.QDesktopWidget()

    settings_default = {
        'tab_file_area': 'corpora_observed',
        'tab_work_area': 'profiler',

        'menu': {
            'prefs': {
                'display_lang': 'eng_us',
                'layouts': {
                    'main_window': [main.height() - DEFAULT_HEIGHT_FILE_AREA, DEFAULT_HEIGHT_FILE_AREA],
                    'profiler': [main.width() - DEFAULT_WIDHT_SETTINGS, DEFAULT_WIDHT_SETTINGS],
                    'concordancer': [main.width() - DEFAULT_WIDHT_SETTINGS, DEFAULT_WIDHT_SETTINGS],
                    'concordancer_parallel': [main.width() - DEFAULT_WIDHT_SETTINGS, DEFAULT_WIDHT_SETTINGS],
                    'dependency_parser': [main.width() - DEFAULT_WIDHT_SETTINGS, DEFAULT_WIDHT_SETTINGS],
                    'wordlist_generator': [main.width() - DEFAULT_WIDHT_SETTINGS, DEFAULT_WIDHT_SETTINGS],
                    'ngram_generator': [main.width() - DEFAULT_WIDHT_SETTINGS, DEFAULT_WIDHT_SETTINGS],
                    'collocation_extractor': [main.width() - DEFAULT_WIDHT_SETTINGS, DEFAULT_WIDHT_SETTINGS],
                    'colligation_extractor': [main.width() - DEFAULT_WIDHT_SETTINGS, DEFAULT_WIDHT_SETTINGS],
                    'keyword_extractor': [main.width() - DEFAULT_WIDHT_SETTINGS, DEFAULT_WIDHT_SETTINGS]
                },
                'show_status_bar': True
            },

            'help': {
                'citing': {
                    'citation_style': _tr('wl_settings_default', 'APA (7th edition)'),
                    'cite_as': _tr('wl_settings_default', 'A journal article')
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

            'dialog_open_corpora': {
                'auto_detect_encodings': True,
                'auto_detect_langs': True,
                'include_files_in_subfolders': True
            }
        },

        'profiler': {
            'tab': 'counts',

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
                'show_breakdown_file': True,
                'show_total': True
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
                'match_tags': False,

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
                }
            },

            'generation_settings': {
                'calc_sentiment_scores': False,

                'context_len_left_char': 50,
                'context_len_left_token': 10,
                'context_len_left_sentence_seg': 0,
                'context_len_left_sentence': 0,
                'context_len_left_para': 0,
                'context_len_right_char': 50,
                'context_len_right_token': 10,
                'context_len_right_sentence_seg': 0,
                'context_len_right_sentence': 0,
                'context_len_right_para': 0,
                'context_len_unit': _tr('wl_settings_default', 'Token')
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

            'results_search': {
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

            'results_sample': {
                'sampling_method': _tr('wl_settings_default', 'None'),
                'sample_size_random': 100,
                'sample_size_systematic_interval': 10,
                'sample_size_systematic_size': 100
            },

            'results_sort': {
                'sorting_rules': [
                    [_tr('wl_settings_default', 'File'), _tr('wl_settings_default', 'Ascending')],
                    [_tr('wl_settings_default', 'Token No.'), _tr('wl_settings_default', 'Ascending')]
                ]
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
                'match_tags': False,

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
                }
            },

            'table_settings': {
                'show_pct_data': True
            },

            'results_search': {
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

            'results_sample': {
                'sampling_method': _tr('wl_settings_default', 'None'),
                'sample_size_random': 100,
                'sample_size_systematic_interval': 10,
                'sample_size_systematic_size': 100
            },
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
                'match_tags': False,
                'match_dependency_relations': False,
                'search_term_position': _tr('wl_settings_default', 'Head/dependent'),

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
                'show_in_separate_tabs': False
            },

            'results_search': {
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

            'results_filter': {
                'file_to_filter': _tr('wl_settings_default', 'Total'),

                'len_head_sync': False,
                'len_head_min': 1,
                'len_head_min_no_limit': True,
                'len_head_max': 20,
                'len_head_max_no_limit': True,

                'len_dependent_sync': False,
                'len_dependent_min': 1,
                'len_dependent_min_no_limit': True,
                'len_dependent_max': 20,
                'len_dependent_max_no_limit': True,

                'dd_sync': False,
                'dd_min': -10,
                'dd_min_no_limit': True,
                'dd_max': 10,
                'dd_max_no_limit': True,

                'add_sync': False,
                'add_min': 0,
                'add_min_no_limit': True,
                'add_max': 10,
                'add_max_no_limit': True,
            },

            'results_sample': {
                'sampling_method': _tr('wl_settings_default', 'None'),
                'sample_size_random': 100,
                'sample_size_systematic_interval': 10,
                'sample_size_systematic_size': 100
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
                'show_syllabified_forms': True,

                'measure_dispersion': 'juillands_d',
                'measure_adjusted_freq': 'juillands_u'
            },

            'table_settings': {
                'show_pct_data': True,
                'show_cum_data': False,
                'show_breakdown_file': True,
                'show_total': True
            },

            'fig_settings': {
                'graph_type': _tr('wl_settings_default', 'Line chart'),
                'sort_by_file': _tr('wl_settings_default', 'Total'),
                'use_data': _tr('wl_settings_default', 'Frequency'),
                'use_pct': False,
                'use_cumulative': False,

                'rank_sync': False,
                'rank_min': 1,
                'rank_min_no_limit': True,
                'rank_max': 50,
                'rank_max_no_limit': False,
            },

            'results_search': {
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

            'results_filter': {
                'file_to_filter': _tr('wl_settings_default', 'Total'),

                'len_token_sync': False,
                'len_token_min': 1,
                'len_token_min_no_limit': True,
                'len_token_max': 20,
                'len_token_max_no_limit': True,

                'num_syls_sync': False,
                'num_syls_min': 1,
                'num_syls_min_no_limit': True,
                'num_syls_max': 20,
                'num_syls_max_no_limit': True,

                'freq_sync': False,
                'freq_min': 0,
                'freq_min_no_limit': True,
                'freq_max': 1000,
                'freq_max_no_limit': True,

                'dispersion_sync': False,
                'dispersion_min': 0,
                'dispersion_min_no_limit': True,
                'dispersion_max': 1,
                'dispersion_max_no_limit': True,

                'adjusted_freq_sync': False,
                'adjusted_freq_min': 0,
                'adjusted_freq_min_no_limit': True,
                'adjusted_freq_max': 1000,
                'adjusted_freq_max_no_limit': True,

                'num_files_found_sync': False,
                'num_files_found_min': 1,
                'num_files_found_min_no_limit': True,
                'num_files_found_max': 100,
                'num_files_found_max_no_limit': True
            },

            'results_sample': {
                'sampling_method': _tr('wl_settings_default', 'None'),
                'sample_size_random': 100,
                'sample_size_systematic_interval': 10,
                'sample_size_systematic_size': 100
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

                'search_term_position_sync': False,
                'search_term_position_min': 1,
                'search_term_position_min_no_limit': True,
                'search_term_position_max': 2,
                'search_term_position_max_no_limit': True,

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
                'show_breakdown_file': True,
                'show_total': True
            },

            'fig_settings': {
                'graph_type': _tr('wl_settings_default', 'Line chart'),
                'sort_by_file': _tr('wl_settings_default', 'Total'),
                'use_data': _tr('wl_settings_default', 'Frequency'),
                'use_pct': False,
                'use_cumulative': False,

                'rank_sync': False,
                'rank_min': 1,
                'rank_min_no_limit': True,
                'rank_max': 50,
                'rank_max_no_limit': False,
            },

            'results_search': {
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

            'results_filter': {
                'file_to_filter': _tr('wl_settings_default', 'Total'),

                'len_ngram_sync': False,
                'len_ngram_min': 1,
                'len_ngram_min_no_limit': True,
                'len_ngram_max': 20,
                'len_ngram_max_no_limit': True,

                'freq_sync': False,
                'freq_min': 0,
                'freq_min_no_limit': True,
                'freq_max': 1000,
                'freq_max_no_limit': True,

                'dispersion_sync': False,
                'dispersion_min': 0,
                'dispersion_min_no_limit': True,
                'dispersion_max': 1,
                'dispersion_max_no_limit': True,

                'adjusted_freq_sync': False,
                'adjusted_freq_min': 0,
                'adjusted_freq_min_no_limit': True,
                'adjusted_freq_max': 1000,
                'adjusted_freq_max_no_limit': True,

                'num_files_found_sync': False,
                'num_files_found_min': 1,
                'num_files_found_min_no_limit': True,
                'num_files_found_max': 100,
                'num_files_found_max_no_limit': True
            },

            'results_sample': {
                'sampling_method': _tr('wl_settings_default', 'None'),
                'sample_size_random': 100,
                'sample_size_systematic_interval': 10,
                'sample_size_systematic_size': 100
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
                'match_tags': False,

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
                'show_breakdown_file': True,
                'show_total': True
            },

            'fig_settings': {
                'graph_type': _tr('wl_settings_default', 'Line chart'),
                'sort_by_file': _tr('wl_settings_default', 'Total'),
                'use_data': _tr('wl_settings_default', 'p-value'),
                'use_pct': False,
                'use_cumulative': False,

                'rank_sync': False,
                'rank_min': 1,
                'rank_min_no_limit': True,
                'rank_max': 50,
                'rank_max_no_limit': False
            },

            'results_search': {
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

            'results_filter': {
                'file_to_filter': _tr('wl_settings_default', 'Total'),

                'len_node_sync': False,
                'len_node_min': 1,
                'len_node_min_no_limit': True,
                'len_node_max': 20,
                'len_node_max_no_limit': True,

                'len_collocate_sync': False,
                'len_collocate_min': 1,
                'len_collocate_min_no_limit': True,
                'len_collocate_max': 20,
                'len_collocate_max_no_limit': True,

                'len_collocation_sync': False,
                'len_collocation_min': 2,
                'len_collocation_min_no_limit': True,
                'len_collocation_max': 40,
                'len_collocation_max_no_limit': True,

                'freq_position': _tr('wl_settings_default', 'Total'),
                'freq_sync': False,
                'freq_min': 0,
                'freq_min_no_limit': True,
                'freq_max': 1000,
                'freq_max_no_limit': True,

                'test_stat_sync': False,
                'test_stat_min': -100,
                'test_stat_min_no_limit': True,
                'test_stat_max': 100,
                'test_stat_max_no_limit': True,

                'p_val_sync': False,
                'p_val_min': 0,
                'p_val_min_no_limit': True,
                'p_val_max': 0.05,
                'p_val_max_no_limit': True,

                'bayes_factor_sync': False,
                'bayes_factor_min': -100,
                'bayes_factor_min_no_limit': True,
                'bayes_factor_max': 100,
                'bayes_factor_max_no_limit': True,

                'effect_size_sync': False,
                'effect_size_min': -100,
                'effect_size_min_no_limit': True,
                'effect_size_max': 100,
                'effect_size_max_no_limit': True,

                'num_files_found_sync': False,
                'num_files_found_min': 1,
                'num_files_found_min_no_limit': True,
                'num_files_found_max': 100,
                'num_files_found_max_no_limit': True
            },

            'results_sample': {
                'sampling_method': _tr('wl_settings_default', 'None'),
                'sample_size_random': 100,
                'sample_size_systematic_interval': 10,
                'sample_size_systematic_size': 100
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
                'show_breakdown_file': True,
                'show_total': True
            },

            'fig_settings': {
                'graph_type': _tr('wl_settings_default', 'Line chart'),
                'sort_by_file': _tr('wl_settings_default', 'Total'),
                'use_data': _tr('wl_settings_default', 'p-value'),
                'use_pct': False,
                'use_cumulative': False,

                'rank_sync': False,
                'rank_min': 1,
                'rank_min_no_limit': True,
                'rank_max': 50,
                'rank_max_no_limit': False
            },

            'results_search': {
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

            'results_filter': {
                'file_to_filter': _tr('wl_settings_default', 'Total'),

                'len_node_sync': False,
                'len_node_min': 1,
                'len_node_min_no_limit': True,
                'len_node_max': 20,
                'len_node_max_no_limit': True,

                'len_collocate_sync': False,
                'len_collocate_min': 1,
                'len_collocate_min_no_limit': True,
                'len_collocate_max': 20,
                'len_collocate_max_no_limit': True,

                'len_colligation_sync': False,
                'len_colligation_min': 2,
                'len_colligation_min_no_limit': True,
                'len_colligation_max': 40,
                'len_colligation_max_no_limit': True,

                'freq_position': _tr('wl_settings_default', 'Total'),
                'freq_sync': False,
                'freq_min': 0,
                'freq_min_no_limit': True,
                'freq_max': 1000,
                'freq_max_no_limit': True,

                'test_stat_sync': False,
                'test_stat_min': -100,
                'test_stat_min_no_limit': True,
                'test_stat_max': 100,
                'test_stat_max_no_limit': True,

                'p_val_sync': False,
                'p_val_min': 0,
                'p_val_min_no_limit': True,
                'p_val_max': 0.05,
                'p_val_max_no_limit': True,

                'bayes_factor_sync': False,
                'bayes_factor_min': -100,
                'bayes_factor_min_no_limit': True,
                'bayes_factor_max': 100,
                'bayes_factor_max_no_limit': True,

                'effect_size_sync': False,
                'effect_size_min': -100,
                'effect_size_min_no_limit': True,
                'effect_size_max': 100,
                'effect_size_max_no_limit': True,

                'num_files_found_sync': False,
                'num_files_found_min': 1,
                'num_files_found_min_no_limit': True,
                'num_files_found_max': 100,
                'num_files_found_max_no_limit': True
            },

            'results_sample': {
                'sampling_method': _tr('wl_settings_default', 'None'),
                'sample_size_random': 100,
                'sample_size_systematic_interval': 10,
                'sample_size_systematic_size': 100
            }
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
                'show_breakdown_file': True,
                'show_total': True
            },

            'fig_settings': {
                'graph_type': _tr('wl_settings_default', 'Line chart'),
                'sort_by_file': _tr('wl_settings_default', 'Total'),
                'use_data': _tr('wl_settings_default', 'p-value'),
                'use_pct': False,
                'use_cumulative': False,

                'rank_sync': False,
                'rank_min': 1,
                'rank_min_no_limit': True,
                'rank_max': 50,
                'rank_max_no_limit': False
            },

            'results_search': {
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

            'results_filter': {
                'file_to_filter': _tr('wl_settings_default', 'Total'),

                'len_keyword_sync': False,
                'len_keyword_min': 1,
                'len_keyword_min_no_limit': True,
                'len_keyword_max': 20,
                'len_keyword_max_no_limit': True,

                'freq_sync': False,
                'freq_min': 0,
                'freq_min_no_limit': True,
                'freq_max': 1000,
                'freq_max_no_limit': True,

                'test_stat_sync': False,
                'test_stat_min': -100,
                'test_stat_min_no_limit': True,
                'test_stat_max': 100,
                'test_stat_max_no_limit': True,

                'p_val_sync': False,
                'p_val_min': 0,
                'p_val_min_no_limit': True,
                'p_val_max': 0.05,
                'p_val_max_no_limit': True,

                'bayes_factor_sync': False,
                'bayes_factor_min': -100,
                'bayes_factor_min_no_limit': True,
                'bayes_factor_max': 100,
                'bayes_factor_max_no_limit': True,

                'effect_size_sync': False,
                'effect_size_min': -100,
                'effect_size_min_no_limit': True,
                'effect_size_max': 100,
                'effect_size_max_no_limit': True,

                'num_files_found_sync': False,
                'num_files_found_min': 1,
                'num_files_found_min_no_limit': True,
                'num_files_found_max': 100,
                'num_files_found_max_no_limit': True
            },

            'results_sample': {
                'sampling_method': _tr('wl_settings_default', 'None'),
                'sample_size_random': 100,
                'sample_size_systematic_interval': 10,
                'sample_size_systematic_size': 100
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
                'always_confirm_on_exit': True
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
                'display_warning_when_opening_nontext_files': True,
                'read_files_in_chunks': 10
            },

            # Settings - Files - Tags
            'tags': {
                'header_tag_settings': [
                    [_tr('wl_settings_default', 'Nonembedded'), _tr('wl_settings_default', 'Header'), '<teiHeader>', '</teiHeader>']
                ],

                'body_tag_settings': [
                    [_tr('wl_settings_default', 'Embedded'), _tr('wl_settings_default', 'Part of speech'), '_*', 'N/A'],
                    [_tr('wl_settings_default', 'Embedded'), _tr('wl_settings_default', 'Part of speech'), '/*', 'N/A'],
                    [_tr('wl_settings_default', 'Nonembedded'), _tr('wl_settings_default', 'Others'), '<*>', 'N/A']
                ],

                'xml_tag_settings': [
                    [_tr('wl_settings_default', 'Nonembedded'), _tr('wl_settings_default', 'Paragraph'), '<p>', '</p>'],
                    [_tr('wl_settings_default', 'Nonembedded'), _tr('wl_settings_default', 'Sentence'), '<s>', '</s>'],
                    [_tr('wl_settings_default', 'Nonembedded'), _tr('wl_settings_default', 'Word'), '<w>', '</w>'],
                    [_tr('wl_settings_default', 'Nonembedded'), _tr('wl_settings_default', 'Word'), '<c>', '</c>']
                ]
            }
        },

        # Settings - Sentence Tokenization
        'sentence_tokenization': {
            'sentence_tokenizer_settings': {
                'afr': 'stanza_afr',
                'sqi': 'stanza_sqi',
                'ara': 'stanza_ara',
                'xcl': 'stanza_xcl',
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
                'ang': 'stanza_ang',
                'eng_gb': 'spacy_dependency_parser_eng',
                'eng_us': 'spacy_dependency_parser_eng',
                'myv': 'stanza_myv',
                'est': 'stanza_est',
                'fao': 'stanza_fao',
                'fin': 'spacy_dependency_parser_fin',
                'fra': 'spacy_dependency_parser_fra',
                'fro': 'stanza_fro',
                'glg': 'stanza_glg',
                'kat': 'stanza_kat',
                'deu_at': 'spacy_dependency_parser_deu',
                'deu_de': 'spacy_dependency_parser_deu',
                'nds': 'stanza_nds',
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
                'kaz': 'stanza_kaz',
                'khm': 'khmer_nltk_khm',
                'kpv': 'stanza_kpv',
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
                'srp_cyrl': 'stanza_srp_latn',
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
                'xct': 'botok_xct',
                'bod': 'modern_botok_bod',
                'tur': 'stanza_tur',
                'ota': 'stanza_ota',
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
                'sqi': 'stanza_sqi',
                'amh': 'spacy_amh',
                'ara': 'stanza_ara',
                'xcl': 'stanza_xcl',
                'hye': 'stanza_hye',
                'hyw': 'stanza_hyw',
                'asm': 'sacremoses_moses',
                'aze': 'spacy_aze',
                'eus': 'stanza_eus',
                'bel': 'stanza_bel',
                'ben': 'sacremoses_moses',
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
                'ang': 'stanza_ang',
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
                'kat': 'stanza_kat',
                'deu_at': 'spacy_deu',
                'deu_de': 'spacy_deu',
                'nds': 'stanza_nds',
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
                'kpv': 'stanza_kpv',
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
                'mni_mtei': 'sacremoses_moses',
                'glv': 'stanza_glv',
                'mar': 'stanza_mar',
                'nep': 'spacy_nep',
                'pcm': 'stanza_pcm',
                'nob': 'spacy_nob',
                'nno': 'stanza_nno',
                'ori': 'sacremoses_moses',
                'pan_guru': 'sacremoses_moses',
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
                'srp_cyrl': 'spacy_srp_cyrl',
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
                'xct': 'botok_xct',
                'bod': 'modern_botok_bod',
                'tir': 'spacy_tir',
                'tsn': 'spacy_tsn',
                'tur': 'stanza_tur',
                'ota': 'stanza_ota',
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
                'asm': 'pyphen_asm',
                'eus': 'pyphen_eus',
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
                'kan': 'pyphen_kan',
                'lav': 'pyphen_lav',
                'lit': 'pyphen_lit',
                'mar': 'pyphen_mar',
                'mon_cyrl': 'pyphen_mon_cyrl',
                'nob': 'pyphen_nob',
                'nno': 'pyphen_nno',
                'ori': 'pyphen_ori',
                'pan_guru': 'pyphen_pan_guru',
                'pol': 'pyphen_pol',
                'por_br': 'pyphen_por_br',
                'por_pt': 'pyphen_por_pt',
                'ron': 'pyphen_ron',
                'rus': 'pyphen_rus',
                'san': 'pyphen_san',
                'srp_cyrl': 'pyphen_srp_cyrl',
                'srp_latn': 'pyphen_srp_latn',
                'slk': 'pyphen_slk',
                'slv': 'pyphen_slv',
                'spa': 'pyphen_spa',
                'swe': 'pyphen_swe',
                'tel': 'pyphen_tel',
                'tha': 'pythainlp_han_solo',
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
                    'sqi': 'stanza_sqi',
                    'ara': 'stanza_ara',
                    'xcl': 'stanza_xcl',
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
                    'ang': 'stanza_ang',
                    'eng_gb': 'spacy_eng',
                    'eng_us': 'spacy_eng',
                    'myv': 'stanza_myv',
                    'est': 'stanza_est',
                    'fao': 'stanza_fao',
                    'fin': 'spacy_fin',
                    'fra': 'spacy_fra',
                    'fro': 'stanza_fro',
                    'glg': 'stanza_glg',
                    'kat': 'stanza_kat',
                    'deu_at': 'spacy_deu',
                    'deu_de': 'spacy_deu',
                    'nds': 'stanza_nds',
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
                    'kpv': 'stanza_kpv',
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
                    'srp_cyrl': 'stanza_srp_latn',
                    'srp_latn': 'stanza_srp_latn',
                    'snd': 'stanza_snd',
                    'slk': 'stanza_slk',
                    'slv': 'spacy_slv',
                    'hsb': 'stanza_hsb',
                    'spa': 'spacy_spa',
                    'swe': 'spacy_swe',
                    'tam': 'stanza_tam',
                    'tel': 'stanza_tel',
                    'tha': 'pythainlp_perceptron_pud',
                    'xct': 'botok_xct',
                    'bod': 'modern_botok_bod',
                    'tur': 'stanza_tur',
                    'ota': 'stanza_ota',
                    'ukr': 'spacy_ukr',
                    'urd': 'stanza_urd',
                    'uig': 'stanza_uig',
                    'vie': 'underthesea_vie',
                    'cym': 'stanza_cym',
                    'wol': 'stanza_wol'
                },

                'separator_between_tokens_pos_tags': '_',
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
                    'sqi': {
                        'stanza_sqi': copy.deepcopy(wl_tagset_eng_universal.tagset_mapping)
                    },

                    'xcl': {
                        'stanza_xcl': wl_tagset_xcl_universal.tagset_mapping
                    },
                    'hye': {
                        'stanza_hye': copy.deepcopy(wl_tagset_hye_universal.tagset_mapping)
                    },
                    'hyw': {
                        'stanza_hyw': copy.deepcopy(wl_tagset_hye_universal.tagset_mapping)
                    },

                    'eus': {
                        'stanza_eus': wl_tagset_eus_universal.tagset_mapping
                    },

                    'bxr': {
                        'stanza_bxr': copy.deepcopy(wl_tagset_eng_universal.tagset_mapping)
                    },

                    'cat': {
                        'spacy_cat': wl_tagset_cat_universal.tagset_mapping
                    },

                    'dan': {
                        'spacy_dan': copy.deepcopy(wl_tagset_dan_universal.tagset_mapping),
                        'stanza_dan': copy.deepcopy(wl_tagset_dan_universal.tagset_mapping)
                    },

                    'eng_gb': {
                        'nltk_perceptron_eng': copy.deepcopy(wl_tagset_eng_penn_treebank.tagset_mapping),
                    },
                    'eng_us': {
                        'nltk_perceptron_eng': copy.deepcopy(wl_tagset_eng_penn_treebank.tagset_mapping),
                    },

                    'ell': {
                        'spacy_ell': copy.deepcopy(wl_tagset_ell_universal.tagset_mapping),
                        'stanza_ell': copy.deepcopy(wl_tagset_ell_universal.tagset_mapping)
                    },

                    'fra': {
                        'spacy_fra': copy.deepcopy(wl_tagset_fra_universal.tagset_mapping),
                        'stanza_fra': copy.deepcopy(wl_tagset_fra_universal.tagset_mapping)
                    },

                    'nds': {
                        'stanza_nds': copy.deepcopy(wl_tagset_eng_universal.tagset_mapping)
                    },

                    'heb': {
                        'stanza_heb': copy.deepcopy(wl_tagset_eng_universal.tagset_mapping)
                    },

                    'hun': {
                        'stanza_hun': wl_tagset_hun_universal.tagset_mapping
                    },

                    'jpn': {
                        'sudachipy_jpn': wl_tagset_jpn_unidic.tagset_mapping
                    },

                    'khm': {
                        'khmer_nltk_khm': wl_tagset_khm_alt.tagset_mapping
                    },

                    'kor': {
                        'python_mecab_ko_mecab': wl_tagset_kor_mecab.tagset_mapping
                    },

                    'lao': {
                        'laonlp_seqlabeling': wl_tagset_lao_seqlabeling.tagset_mapping,
                        'laonlp_yunshan_cup_2020': wl_tagset_lao_yunshan_cup_2020.tagset_mapping
                    },

                    'lij': {
                        'stanza_lij': copy.deepcopy(wl_tagset_eng_universal.tagset_mapping)
                    },

                    'mkd': {
                        'spacy_mkd': copy.deepcopy(wl_tagset_eng_universal.tagset_mapping)
                    },

                    'glv': {
                        'stanza_glv': copy.deepcopy(wl_tagset_eng_universal.tagset_mapping)
                    },

                    'mar': {
                        'stanza_mar': copy.deepcopy(wl_tagset_eng_universal.tagset_mapping)
                    },

                    'pcm': {
                        'stanza_pcm': wl_tagset_pcm_universal.tagset_mapping
                    },

                    'nob': {
                        'spacy_nob': wl_tagset_nor_universal.tagset_mapping
                    },

                    'qpm': {
                        'stanza_qpm': copy.deepcopy(wl_tagset_eng_universal.tagset_mapping)
                    },

                    'por_br': {
                        'spacy_por': copy.deepcopy(wl_tagset_por_universal.tagset_mapping),
                        'stanza_por': copy.deepcopy(wl_tagset_por_universal.tagset_mapping)
                    },
                    'por_pt': {
                        'spacy_por': copy.deepcopy(wl_tagset_por_universal.tagset_mapping),
                        'stanza_por': copy.deepcopy(wl_tagset_por_universal.tagset_mapping)
                    },

                    'rus': {
                        'nltk_perceptron_rus': wl_tagset_rus_russian_national_corpus.tagset_mapping,
                        'pymorphy3_morphological_analyzer': copy.deepcopy(wl_tagset_rus_open_corpora.tagset_mapping),
                        'spacy_rus': copy.deepcopy(wl_tagset_rus_universal.tagset_mapping),
                        'stanza_rus': copy.deepcopy(wl_tagset_rus_universal.tagset_mapping)
                    },

                    'san': {
                        'stanza_san': copy.deepcopy(wl_tagset_eng_universal.tagset_mapping)
                    },

                    'snd': {
                        'stanza_snd': copy.deepcopy(wl_tagset_eng_universal.tagset_mapping)
                    },

                    'hsb': {
                        'stanza_hsb': copy.deepcopy(wl_tagset_eng_universal.tagset_mapping)
                    },

                    'spa': {
                        'spacy_spa': wl_tagset_spa_universal.tagset_mapping
                    },

                    'tel': {
                        'stanza_tel': copy.deepcopy(wl_tagset_eng_universal.tagset_mapping)
                    },

                    'tha': {
                        'pythainlp_perceptron_blackboard': wl_tagset_tha_blackboard.tagset_mapping,
                        'pythainlp_perceptron_orchid': wl_tagset_tha_orchid.tagset_mapping,
                        'pythainlp_perceptron_pud': copy.deepcopy(wl_tagset_eng_universal.tagset_mapping)
                    },

                    'xct': {
                        'botok_xct': copy.deepcopy(wl_tagset_xct_botok.tagset_mapping)
                    },
                    'bod': {
                        'modern_botok_bod': copy.deepcopy(wl_tagset_eng_universal.tagset_mapping)
                    },

                    'ukr': {
                        'pymorphy3_morphological_analyzer': copy.deepcopy(wl_tagset_rus_open_corpora.tagset_mapping),
                        'spacy_ukr': wl_tagset_ukr_universal.tagset_mapping
                    },

                    'vie': {
                        'underthesea_vie': wl_tagset_vie_underthesea.tagset_mapping
                    }
                }
            }
        },

        # Settings - Lemmatization
        'lemmatization': {
            'lemmatizer_settings': {
                'afr': 'stanza_afr',
                'sqi': 'stanza_sqi',
                'ara': 'stanza_ara',
                'xcl': 'stanza_xcl',
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
                'ang': 'stanza_ang',
                'eng_gb': 'spacy_eng',
                'eng_us': 'spacy_eng',
                'myv': 'stanza_myv',
                'est': 'stanza_est',
                'fin': 'spacy_fin',
                'fra': 'spacy_fra',
                'fro': 'stanza_fro',
                'glg': 'stanza_glg',
                'kat': 'stanza_kat',
                'deu_at': 'spacy_deu',
                'deu_de': 'spacy_deu',
                'nds': 'stanza_nds',
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
                'kpv': 'stanza_kpv',
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
                'srp_cyrl': 'spacy_srp_cyrl',
                'srp_latn': 'stanza_srp_latn',
                'slk': 'stanza_slk',
                'slv': 'spacy_slv',
                'hsb': 'stanza_hsb',
                'spa': 'spacy_spa',
                'swa': 'simplemma_swa',
                'swe': 'spacy_swe',
                'tgl': 'simplemma_tgl',
                'tam': 'stanza_tam',
                'xct': 'botok_xct',
                'bod': 'modern_botok_bod',
                'tur': 'stanza_tur',
                'ota': 'stanza_ota',
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
                'stop_word_lists': {
                    'afr': 'spacy_afr',
                    'sqi': 'spacy_sqi',
                    'amh': 'spacy_amh',
                    'ara': 'spacy_ara',
                    'hye': 'spacy_hye',
                    'hyw': 'spacy_hye',
                    'aze': 'spacy_aze',
                    'eus': 'spacy_eus',
                    'ben': 'spacy_ben',
                    'bul': 'spacy_bul',
                    'cat': 'spacy_cat',
                    'zho_cn': 'spacy_zho_cn',
                    'zho_tw': 'spacy_zho_cn',
                    'hrv': 'spacy_hrv',
                    'ces': 'spacy_ces',
                    'dan': 'spacy_dan',
                    'nld': 'spacy_nld',
                    'eng_gb': 'spacy_eng',
                    'eng_us': 'spacy_eng',
                    'est': 'spacy_est',
                    'fin': 'spacy_fin',
                    'fra': 'spacy_fra',
                    'lug': 'spacy_lug',
                    'deu_at': 'spacy_deu',
                    'deu_de': 'spacy_deu',
                    'deu_ch': 'spacy_deu',
                    'grc': 'spacy_grc',
                    'ell': 'spacy_ell',
                    'guj': 'spacy_guj',
                    'heb': 'spacy_heb',
                    'hin': 'spacy_hin',
                    'hun': 'spacy_hun',
                    'isl': 'spacy_isl',
                    'ind': 'spacy_ind',
                    'gle': 'spacy_gle',
                    'ita': 'spacy_ita',
                    'jpn': 'spacy_jpn',
                    'kan': 'spacy_kan',
                    'kaz': 'nltk_kaz',
                    'kor': 'spacy_kor',
                    'kmr': 'spacy_kmr',
                    'kir': 'spacy_kir',
                    'lao': 'laonlp_lao',
                    'lat': 'spacy_lat',
                    'lav': 'spacy_lav',
                    'lij': 'spacy_lij',
                    'lit': 'spacy_lit',
                    'ltz': 'spacy_ltz',
                    'mkd': 'spacy_mkd',
                    'msa': 'spacy_msa',
                    'mal': 'spacy_mal',
                    'mar': 'spacy_mar',
                    'nep': 'spacy_nep',
                    'nob': 'spacy_nob',
                    'fas': 'spacy_fas',
                    'pol': 'spacy_pol',
                    'por_br': 'spacy_por',
                    'por_pt': 'spacy_por',
                    'ron': 'spacy_ron',
                    'rus': 'spacy_rus',
                    'san': 'spacy_san',
                    'gla': 'spacy_gla',
                    'srp_cyrl': 'spacy_srp_cyrl',
                    'srp_latn': 'spacy_srp_cyrl',
                    'sin': 'spacy_sin',
                    'slk': 'spacy_slk',
                    'slv': 'spacy_slv',
                    'dsb': 'spacy_dsb',
                    'hsb': 'spacy_hsb',
                    'spa': 'spacy_spa',
                    'swe': 'spacy_swe',
                    'tgk': 'nltk_tgk',
                    'tgl': 'spacy_tgl',
                    'tam': 'spacy_tam',
                    'tat': 'spacy_tat',
                    'tel': 'spacy_tel',
                    'tha': 'pythainlp_tha',
                    'xct': 'spacy_bod',
                    'bod': 'spacy_bod',
                    'tir': 'spacy_tir',
                    'tsn': 'spacy_tsn',
                    'tur': 'spacy_tur',
                    'ukr': 'spacy_ukr',
                    'urd': 'spacy_urd',
                    'vie': 'spacy_vie',
                    'yor': 'spacy_yor',

                    'other': 'custom'
                },

                'case_sensitive': False,
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
                'sqi': 'stanza_sqi',
                'ara': 'stanza_ara',
                'xcl': 'stanza_xcl',
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
                'ang': 'stanza_ang',
                'eng_gb': 'spacy_eng',
                'eng_us': 'spacy_eng',
                'myv': 'stanza_myv',
                'est': 'stanza_est',
                'fao': 'stanza_fao',
                'fin': 'spacy_fin',
                'fra': 'spacy_fra',
                'fro': 'stanza_fro',
                'glg': 'stanza_glg',
                'kat': 'stanza_kat',
                'deu_at': 'spacy_deu',
                'deu_de': 'spacy_deu',
                'nds': 'stanza_nds',
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
                'kpv': 'stanza_kpv',
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
                'srp_cyrl': 'stanza_srp_latn',
                'srp_latn': 'stanza_srp_latn',
                'snd': 'stanza_snd',
                'slk': 'stanza_slk',
                'slv': 'spacy_slv',
                'hsb': 'stanza_hsb',
                'spa': 'spacy_spa',
                'swe': 'spacy_swe',
                'tam': 'stanza_tam',
                'tel': 'stanza_tel',
                'tha': 'stanza_tha',
                'tur': 'stanza_tur',
                'ota': 'stanza_ota',
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
                    'show_in_separate_tabs': False
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
                'spa': 'stanza_spa',
                'vie': 'underthesea_vie'
            },

            'preview': {
                'preview_lang': 'eng_us',
                'preview_samples': ''
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

            'misc_settings': {
                'show_thousand_separators': True
            },

            # Settings - Tables - Profiler
            'profiler': {
                'lang_specific_settings': {
                    'add_missing_ending_tshegs': False
                }
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
                'highlight_color_settings': {
                    'search_term_color': '#FF0000' # Red
                }
            },

            # Settings - Tables - Dependency Parser
            'dependency_parser': {
                'highlight_color_settings': {
                    'head_color': '#FF0000', # Red
                    'dependent_color': '#3F864C', # Green
                }
            },

            # Settings - Tables - Wordlist Generator
            'wordlist_generator': {
                'lang_specific_settings': {
                    'add_missing_ending_tshegs': True
                }
            },

            # Settings - Tables - N-gram Generator
            'ngram_generator': {
                'lang_specific_settings': {
                    'add_missing_ending_tshegs': True
                }
            },

            # Settings - Tables - Collocation Extractor
            'collocation_extractor': {
                'lang_specific_settings': {
                    'add_missing_ending_tshegs': True
                }
            },

            # Settings - Tables - Colligation Extractor
            'colligation_extractor': {
                'lang_specific_settings': {
                    'add_missing_ending_tshegs': True
                }
            },

            # Settings - Tables - Keyword Extractor
            'keyword_extractor': {
                'lang_specific_settings': {
                    'add_missing_ending_tshegs': True
                }
            }
        },

        # Settings - Measures
        'measures': {
            # Settings - Measures - Readability
            'readability': {
                'rd': {
                    'variant': _tr('wl_settings_default', 'Policy One')
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

                'spache_readability_formula': {
                    'use_rev_formula': True
                },

                'trankle_bailers_readability_formula': {
                    'variant': '1'
                }
            },

            # Settings - Measures - Lexical Density/Diversity
            'lexical_density_diversity': {
                'hdd': {
                    'sample_size': 42
                },

                'logttr': {
                    'variant': 'Herdan'
                },

                'msttr': {
                    'num_tokens_in_each_seg': 1000
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
                    'num_subsections': 5
                },

                'griess_dp': {
                    'apply_normalization': True
                }
            },

            # Settings - Measures - Adjusted Frequency
            'adjusted_freq': {
                'general_settings': {
                    'num_subsections': 5
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
                    'num_subsections': 5,
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
                    'num_subsections': 5,
                    'use_data': _tr('wl_settings_default', 'Relative frequency'),
                    'direction': _tr('wl_settings_default', 'Two-tailed')
                },

                'z_test': {
                    'direction': _tr('wl_settings_default', 'Two-tailed')
                },

                'z_test_berry_rogghe': {
                    'direction': _tr('wl_settings_default', 'Two-tailed')
                }
            },

            # Settings - Measures - Bayes Factor
            'bayes_factor': {
                'log_likelihood_ratio_test': {
                    'apply_correction': False
                },

                'students_t_test_2_sample': {
                    'num_subsections': 5,
                    'use_data': _tr('wl_settings_default', 'Relative frequency'),
                    'direction': _tr('wl_settings_default', 'Two-tailed')
                }
            },

            # Settings - Measures - Effect Size
            'effect_size': {
                'kilgarriffs_ratio': {
                    'smoothing_param': 1.00
                },

                'mi': {
                    'base_log': 2
                },

                'nmi': {
                    'base_log': math.e
                },

                'pmi': {
                    'base_log': 2
                },

                'im3': {
                    'base_log': 2
                },

                'npmi': {
                    'base_log': math.e
                },

                'im2': {
                    'base_log': 2
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
                    'font': 'Droid Sans Mono',
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
                    'node_size': 100,
                    # The color of horizontal headers in tables (#5C88C5) with 80% opacity
                    'node_color': '#7DA0D1',
                    'node_opacity': 1.0,
                    'border_width': 1,
                    'border_color': '#7DA0D1',
                    'same_as_node_color': True
                },

                'node_label_settings': {
                    'font_family': DEFAULT_FONT_FAMILY,
                    'font_size': DEFAULT_FONT_SIZE,
                    'font_weight': 400,
                    'font_color': '#000000',
                    'label_opacity': 1.0,
                    'hor_alignment': 'center',
                    'vert_alignment': 'center'
                },

                'edge_settings': {
                    'connection_style': 'arc3',
                    'edge_width_min': 0.5,
                    'edge_width_max': 3,
                    'edge_style': 'solid',
                    # The color of horizontal headers in tables (#5C88C5) with 50% opacity
                    'edge_color': '#ADC3E2',
                    'edge_opacity': 1.0,
                    'arrow_style': '-|>',
                    'arrow_size': 10
                },

                'edge_label_settings': {
                    'label_position': 0.5,
                    'rotate_labels': True,
                    'font_family': DEFAULT_FONT_FAMILY,
                    'font_size': DEFAULT_FONT_SIZE,
                    'font_weight': 400,
                    'font_color': '#000000',
                    'label_opacity': 1.0,
                    'hor_alignment': 'center',
                    'vert_alignment': 'center'
                },

                'advanced_settings': {
                    'layout': networkx.spring_layout
                }
            }
        }
    }

    # Sentiment Analysis - Preview - Sentiment score
    precision = settings_default['tables']['precision_settings']['precision_decimals']
    settings_default['sentiment_analysis']['preview']['preview_sentiment_score'] = f'{0:.{precision}f}'

    # Tagsets
    for mappings in settings_default['pos_tagging']['tagsets']['mapping_settings'].values():
        for mapping in mappings.values():
            if len(mapping[0]) == 4:
                for i, (_, universal_pos_tag, _, _) in enumerate(mapping):
                    mapping[i].insert(2, wl_pos_tagging.to_content_function(universal_pos_tag))

    settings_default['pos_tagging']['tagsets']['preview_settings']['preview_pos_tagger'] = settings_default['pos_tagging']['pos_tagger_settings']['pos_taggers'].copy()

    # Custom stop word lists
    for lang in main.settings_global['langs'].values():
        lang_code = lang[0]

        if lang_code not in settings_default['stop_word_lists']['stop_word_list_settings']['stop_word_lists']:
            settings_default['stop_word_lists']['stop_word_list_settings']['stop_word_lists'][lang_code] = 'custom'

        settings_default['stop_word_lists']['custom_lists'][lang_code] = []

    return settings_default

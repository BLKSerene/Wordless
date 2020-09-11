#
# Wordless: Settings - Default Settings
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

from wl_tagsets import (
    wl_tagset_universal,
    wl_tagset_eng_penn_treebank,
    wl_tagset_jpn_unidic,
    wl_tagset_rus_open_corpora,
    wl_tagset_rus_russian_national_corpus,
    wl_tagset_tha_orchid,
    wl_tagset_bod_botok,
    wl_tagset_vie_underthesea,
    wl_tagset_zho_jieba
)
from wl_utils import wl_misc

def init_settings_default(main):
    main.settings_default = {
        'work_area_cur': main.tr('Overview'),

        'layouts': {
            'central_widget': [main.height() - 100 - 210, 210]
        },

        'files': {
            'files_open': [],
            'files_closed': [],

            'folder_settings': {
                'subfolders': True
            },

            'auto_detection_settings': {
                'detect_langs': True,
                'detect_text_types': True,
                'detect_encodings': True
            }
        },

        'overview': {
            'token_settings': {
                'words': True,
                'lowercase': True,
                'uppercase': True,
                'title_case': True,
                'nums': True,
                'puncs': False,

                'treat_as_lowercase': True,
                'lemmatize_tokens': False,
                'filter_stop_words': False,

                'ignore_tags': True,
                'ignore_tags_tags': False,
                'ignore_tags_type': main.tr('all'),
                'ignore_tags_type_tags': main.tr('non-POS'),
                'use_tags': False
            },

            'generation_settings': {
                'base_sttr': 1000
            },

            'table_settings': {
                'show_pct': True,
                'show_cumulative': False,
                'show_breakdown': True
            }
        },
    
        'concordancer': {
            'token_settings': {
                'puncs': False,

                'ignore_tags': True,
                'ignore_tags_tags': False,
                'ignore_tags_type': main.tr('all'),
                'ignore_tags_type_tags': main.tr('non-POS'),
                'use_tags': False
            },
            
            'search_settings': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'ignore_case': True,
                'match_inflected_forms': True,
                'match_whole_words': True,
                'use_regex': False,

                'ignore_tags': True,
                'ignore_tags_tags': False,
                'ignore_tags_type': main.tr('all'),
                'ignore_tags_type_tags': main.tr('non-POS'),
                'match_tags': False
            },

            'context_settings': {
                'inclusion': {
                    'inclusion': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'ignore_case': True,
                    'match_inflected_forms': True,
                    'match_whole_words': True,
                    'use_regex': False,

                    'ignore_tags': True,
                    'ignore_tags_tags': False,
                    'ignore_tags_type': main.tr('all'),
                    'ignore_tags_type_tags': main.tr('non-POS'),
                    'match_tags': False,
                    
                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                },
                
                'exclusion': {
                    'exclusion': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'ignore_case': True,
                    'match_inflected_forms': True,
                    'match_whole_words': True,
                    'use_regex': False,

                    'ignore_tags': True,
                    'ignore_tags_tags': False,
                    'ignore_tags_type': main.tr('all'),
                    'ignore_tags_type_tags': main.tr('non-POS'),
                    'match_tags': False,
                    
                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                }
            },
            
            'generation_settings': {
                'width_left_para': 0,
                'width_left_sentence': 0,
                'width_left_clause': 0,
                'width_left_token': 10,
                'width_left_char': 50,
                'width_right_para': 0,
                'width_right_sentence': 0,
                'width_right_clause': 0,
                'width_right_token': 10,
                'width_right_char': 50,
                'width_unit': main.tr('Token'),

                'sampling_method': main.tr('None'),
                'sample_size_first_n_lines': 100,
                'sample_size_systematic_fixed_interval': 2,
                'sample_size_systematic_fixed_size': 100,
                'sample_size_random': 100
            },

            'table_settings': {
                'show_pct': True
            },

            'fig_settings': {
                'sort_results_by': main.tr('File')
            },

            'sort_results': {
                'sorting_rules': [
                    [main.tr('Node'), main.tr('Ascending')],
                    [main.tr('File'), main.tr('Ascending')],
                    [main.tr('Token No.'), main.tr('Ascending')]
                ],

                'highlight_colors': [
                    # Red
                    '#F00',
                    # Orange
                    '#C2691D',
                    # Yellow
                    '#CBBE00',
                    # Green
                    '#3F864C',
                    # Blue
                    '#264E8C',
                    # Purple
                    '#491D76'
                ]
            },

            'search_results': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'ignore_case': True,
                'match_inflected_forms': True,
                'match_whole_words': True,
                'use_regex': False,

                'ignore_tags': True,
                'ignore_tags_tags': False,
                'ignore_tags_type': main.tr('all'),
                'ignore_tags_type_tags': main.tr('non-POS'),
                'match_tags': False
            }
        },
    
        'wordlist': {
            'token_settings': {
                'words': True,
                'lowercase': True,
                'uppercase': True,
                'title_case': True,
                'nums': True,
                'puncs': False,

                'treat_as_lowercase': True,
                'lemmatize_tokens': False,
                'filter_stop_words': False,

                'ignore_tags': True,
                'ignore_tags_tags': False,
                'ignore_tags_type': main.tr('all'),
                'ignore_tags_type_tags': main.tr('non-POS'),
                'use_tags': False
            },

            'generation_settings': {
                'measure_dispersion': main.tr('Juilland\'s D'),
                'measure_adjusted_freq': main.tr('Juilland\'s U')
            },

            'table_settings': {
                'show_pct': True,
                'show_cumulative': False,
                'show_breakdown': True
            },

            'fig_settings': {
                'graph_type': main.tr('Line Chart'),
                'use_file': main.tr('Total'),
                'use_data': main.tr('Frequency'),
                'use_pct': False,
                'use_cumulative': False,

                'rank_min': 1,
                'rank_min_no_limit': True,
                'rank_max': 50,
                'rank_max_no_limit': False,
            },

            'filter_results': {
                'file_to_filter': main.tr('Total'),

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

                'len_token_min': 1,
                'len_token_min_no_limit': True,
                'len_token_max': 20,
                'len_token_max_no_limit': True,

                'num_files_found_min': 1,
                'num_files_found_min_no_limit': True,
                'num_files_found_max': 100,
                'num_files_found_max_no_limit': True
            },

            'search_results': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'ignore_case': True,
                'match_inflected_forms': True,
                'match_whole_words': True,
                'use_regex': False,

                'ignore_tags': True,
                'ignore_tags_tags': False,
                'ignore_tags_type': main.tr('all'),
                'ignore_tags_type_tags': main.tr('non-POS'),
                'match_tags': False
            }
        },
    
        'ngram': {
            'token_settings': {
                'words': True,
                'lowercase': True,
                'uppercase': True,
                'title_case': True,
                'nums': True,
                'puncs': False,

                'treat_as_lowercase': True,
                'lemmatize_tokens': False,
                'filter_stop_words': False,

                'ignore_tags': True,
                'ignore_tags_tags': False,
                'ignore_tags_type': main.tr('all'),
                'ignore_tags_type_tags': main.tr('non-POS'),
                'use_tags': False
            },

            'search_settings': {
                'search_settings': True,

                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'ignore_case': True,
                'match_inflected_forms': True,
                'match_whole_words': True,
                'use_regex': False,

                'ignore_tags': True,
                'ignore_tags_tags': False,
                'ignore_tags_type': main.tr('all'),
                'ignore_tags_type_tags': main.tr('non-POS'),
                'match_tags': False,

                'search_term_position_min': 1,
                'search_term_position_min_no_limit': True,
                'search_term_position_max': 2,
                'search_term_position_max_no_limit': True,
                'allow_skipped_tokens_within_search_terms': True
            },

            'context_settings': {
                'inclusion': {
                    'inclusion': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'ignore_case': True,
                    'match_inflected_forms': True,
                    'match_whole_words': True,
                    'use_regex': False,

                    'ignore_tags': True,
                    'ignore_tags_tags': False,
                    'ignore_tags_type': main.tr('all'),
                    'ignore_tags_type_tags': main.tr('non-POS'),
                    'match_tags': False,
                    
                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                },
                
                'exclusion': {
                    'exclusion': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'ignore_case': True,
                    'match_inflected_forms': True,
                    'match_whole_words': True,
                    'use_regex': False,

                    'ignore_tags': True,
                    'ignore_tags_tags': False,
                    'ignore_tags_type': main.tr('all'),
                    'ignore_tags_type_tags': main.tr('non-POS'),
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

                'measure_dispersion': main.tr('Juilland\'s D'),
                'measure_adjusted_freq': main.tr('Juilland\'s U')
            },

            'table_settings': {
                'show_pct': True,
                'show_cumulative': False,
                'show_breakdown': True
            },

            'fig_settings': {
                'graph_type': main.tr('Line Chart'),
                'use_file': main.tr('Total'),
                'use_data': main.tr('Frequency'),
                'use_pct': False,
                'use_cumulative': False,

                'rank_min': 1,
                'rank_min_no_limit': True,
                'rank_max': 50,
                'rank_max_no_limit': False,
            },

            'filter_results': {
                'file_to_filter': main.tr('Total'),

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

                'ignore_case': True,
                'match_inflected_forms': True,
                'match_whole_words': True,
                'use_regex': False,

                'ignore_tags': True,
                'ignore_tags_tags': False,
                'ignore_tags_type': main.tr('all'),
                'ignore_tags_type_tags': main.tr('non-POS'),
                'match_tags': False
            }
        },

        'collocation': {
            'token_settings': {
                'words': True,
                'lowercase': True,
                'uppercase': True,
                'title_case': True,
                'nums': True,
                'puncs': False,

                'treat_as_lowercase': True,
                'lemmatize_tokens': False,
                'filter_stop_words': False,

                'ignore_tags': True,
                'ignore_tags_tags': False,
                'ignore_tags_type': main.tr('all'),
                'ignore_tags_type_tags': main.tr('non-POS'),
                'use_tags': False
            },
            
            'search_settings': {
                'search_settings': True,

                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'ignore_case': True,
                'match_inflected_forms': True,
                'match_whole_words': True,
                'use_regex': False,

                'ignore_tags': True,
                'ignore_tags_tags': False,
                'ignore_tags_type': main.tr('all'),
                'ignore_tags_type_tags': main.tr('non-POS'),
                'match_tags': False
            },

            'context_settings': {
                'inclusion': {
                    'inclusion': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'ignore_case': True,
                    'match_inflected_forms': True,
                    'match_whole_words': True,
                    'use_regex': False,

                    'ignore_tags': True,
                    'ignore_tags_tags': False,
                    'ignore_tags_type': main.tr('all'),
                    'ignore_tags_type_tags': main.tr('non-POS'),
                    'match_tags': False,
                    
                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                },
                
                'exclusion': {
                    'exclusion': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'ignore_case': True,
                    'match_inflected_forms': True,
                    'match_whole_words': True,
                    'use_regex': False,

                    'ignore_tags': True,
                    'ignore_tags_tags': False,
                    'ignore_tags_type': main.tr('all'),
                    'ignore_tags_type_tags': main.tr('non-POS'),
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

                'test_significance': main.tr('Pearson\'s Chi-squared Test'),
                'measure_effect_size': main.tr('Pointwise Mutual Information'),
            },

            'table_settings': {
                'show_pct': True,
                'show_cumulative': False,
                'show_breakdown_position': True,
                'show_breakdown_file': True
            },

            'fig_settings': {
                'graph_type': main.tr('Line Chart'),
                'use_file': main.tr('Total'),
                'use_data': main.tr('p-value'),
                'use_pct': False,
                'use_cumulative': False,

                'rank_min': 1,
                'rank_min_no_limit': True,
                'rank_max': 50,
                'rank_max_no_limit': False
            },

            'filter_results': {
                'file_to_filter': main.tr('Total'),

                'len_collocate_min': 1,
                'len_collocate_min_no_limit': True,
                'len_collocate_max': 20,
                'len_collocate_max_no_limit': True,

                'freq_position': main.tr('Total'),
                'freq_min': 0,
                'freq_min_no_limit': True,
                'freq_max': 1000,
                'freq_max_no_limit': True,

                'test_stat_min': -100,
                'test_stat_min_no_limit': True,
                'test_stat_max': 100,
                'test_stat_max_no_limit': True,

                'p_value_min': 0,
                'p_value_min_no_limit': True,
                'p_value_max': 0.05,
                'p_value_max_no_limit': True,

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

                'ignore_case': True,
                'match_inflected_forms': True,
                'match_whole_words': True,
                'use_regex': False,

                'ignore_tags': True,
                'ignore_tags_tags': False,
                'ignore_tags_type': main.tr('all'),
                'ignore_tags_type_tags': main.tr('non-POS'),
                'match_tags': False
            }
        },

        'colligation': {
            'token_settings': {
                'words': True,
                'lowercase': True,
                'uppercase': True,
                'title_case': True,
                'nums': True,
                'puncs': False,

                'treat_as_lowercase': True,
                'lemmatize_tokens': False,
                'filter_stop_words': False,

                'ignore_tags': True,
                'ignore_tags_tags': False,
                'ignore_tags_type': main.tr('all'),
                'ignore_tags_type_tags': main.tr('non-POS'),
                'use_tags': False
            },

            'search_settings': {
                'search_settings': True,

                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'ignore_case': True,
                'match_inflected_forms': True,
                'match_whole_words': True,
                'use_regex': False,

                'ignore_tags': True,
                'ignore_tags_tags': False,
                'ignore_tags_type': main.tr('all'),
                'ignore_tags_type_tags': main.tr('non-POS'),
                'match_tags': False
            },

            'context_settings': {
                'inclusion': {
                    'inclusion': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'ignore_case': True,
                    'match_inflected_forms': False,
                    'match_whole_words': True,
                    'use_regex': False,

                    'ignore_tags': True,
                    'ignore_tags_tags': False,
                    'ignore_tags_type': main.tr('all'),
                    'ignore_tags_type_tags': main.tr('non-POS'),
                    'match_tags': False,
                    
                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                },
                
                'exclusion': {
                    'exclusion': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'ignore_case': True,
                    'match_inflected_forms': False,
                    'match_whole_words': True,
                    'use_regex': False,

                    'ignore_tags': True,
                    'ignore_tags_tags': False,
                    'ignore_tags_type': main.tr('all'),
                    'ignore_tags_type_tags': main.tr('non-POS'),
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

                'test_significance': main.tr('Pearson\'s Chi-squared Test'),
                'measure_effect_size': main.tr('Pointwise Mutual Information')
            },

            'table_settings': {
                'show_pct': True,
                'show_cumulative': False,
                'show_breakdown_position': True,
                'show_breakdown_file': True
            },

            'fig_settings': {
                'graph_type': main.tr('Line Chart'),
                'use_file': main.tr('Total'),
                'use_data': main.tr('p-value'),
                'use_pct': False,
                'use_cumulative': False,

                'rank_min': 1,
                'rank_min_no_limit': True,
                'rank_max': 50,
                'rank_max_no_limit': False
            },

            'filter_results': {
                'file_to_filter': main.tr('Total'),

                'len_collocate_min': 1,
                'len_collocate_min_no_limit': True,
                'len_collocate_max': 20,
                'len_collocate_max_no_limit': True,

                'freq_position': main.tr('Total'),
                'freq_min': 0,
                'freq_min_no_limit': True,
                'freq_max': 1000,
                'freq_max_no_limit': True,

                'test_stat_min': -100,
                'test_stat_min_no_limit': True,
                'test_stat_max': 100,
                'test_stat_max_no_limit': True,

                'p_value_min': 0,
                'p_value_min_no_limit': True,
                'p_value_max': 0.05,
                'p_value_max_no_limit': True,

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

                'ignore_case': True,
                'match_inflected_forms': True,
                'match_whole_words': True,
                'use_regex': False,

                'ignore_tags': True,
                'ignore_tags_tags': False,
                'ignore_tags_type': main.tr('all'),
                'ignore_tags_type_tags': main.tr('non-POS'),
                'match_tags': False
            },
        },

        'keyword': {
            'token_settings': {
                'words': True,
                'lowercase': True,
                'uppercase': True,
                'title_case': True,
                'nums': True,
                'puncs': False,

                'treat_as_lowercase': True,
                'lemmatize_tokens': False,
                'filter_stop_words': False,

                'ignore_tags': True,
                'ignore_tags_type': main.tr('all'),
                'ignore_tags_tags': False,
                'ignore_tags_type_tags': main.tr('non-POS'),
                'use_tags': False
            },

            'generation_settings': {
                'ref_file': '',
                'test_significance': main.tr('Log-likelihood Ratio Test'),
                'measure_effect_size': main.tr('Kilgarriff\'s Ratio'),
                'measure_dispersion': main.tr('Juilland\'s D')
            },
            
            'table_settings': {
                'show_pct': True,
                'show_cumulative': False,
                'show_breakdown': True
            },

            'fig_settings': {
                'graph_type': main.tr('Line Chart'),
                'use_file': main.tr('Total'),
                'use_data': main.tr('p-value'),
                'use_pct': False,
                'use_cumulative': False,

                'rank_min': 1,
                'rank_min_no_limit': True,
                'rank_max': 50,
                'rank_max_no_limit': False
            },

            'filter_results': {
                'file_to_filter': main.tr('Total'),

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

                'p_value_min': 0,
                'p_value_min_no_limit': True,
                'p_value_max': 0.05,
                'p_value_max_no_limit': True,

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

                'ignore_case': True,
                'match_inflected_forms': True,
                'match_whole_words': True,
                'use_regex': False,

                'ignore_tags': True,
                'ignore_tags_tags': False,
                'ignore_tags_type': main.tr('all'),
                'ignore_tags_type_tags': main.tr('non-POS'),
                'match_tags': False
            }
        },

        'menu': {
            'prefs': {
                'show_status_bar': True
            },

            'help': {
                'citing': {
                    'citation_sys': main.tr('APA (7th Edition)')
                },

                'acks': {
                    'browse_category': main.tr('General')
                },

                'donating': {
                    'donating_via': main.tr('PayPal')
                }
            }
        },

        'settings': {
            'tab': 'General'
        },

        'general': {
            'font_settings': {
                'font_family': 'Arial',
                'font_size': 12
            },

            'update_settings': {
                'check_updates_on_startup': True
            },

            'misc': {
                'confirm_on_exit': True
            }
        },

        'import': {
            'files': {
                'default_path': wl_misc.get_normalized_path('.')
            },

            'search_terms': {
                'default_path': wl_misc.get_normalized_path('.'),
                'detect_encodings': True
            },

            'stop_words': {
                'default_path': wl_misc.get_normalized_path('.'),
                'detect_encodings': True
            },

            'temp_files': {
                'default_path': wl_misc.get_normalized_path('Import/'),
                'default_encoding': 'utf_8'
            }
        },

        'export': {
            'tables': {
                'default_path': wl_misc.get_normalized_path('Export/'),
                'default_type': main.tr('Excel Workbook (*.xlsx)'),
                'default_encoding': 'utf_8'
            },

            'search_terms': {
                'default_path': wl_misc.get_normalized_path('Export/'),
                'default_encoding': 'utf_8'
            },

            'stop_words': {
                'default_path': wl_misc.get_normalized_path('Export/'),
                'default_encoding': 'utf_8'
            }
        },

        'auto_detection': {
            'detection_settings': {
                'number_lines': 100,
                'number_lines_no_limit': False
            },

            'default_settings': {
                'default_lang': 'eng',
                'default_text_type': ('untokenized', 'untagged'),
                'default_encoding': 'utf_8'
            }
        },

        'data': {
            'precision_decimal': 2,
            'precision_pct': 2,
            'precision_p_value': 5
        },

        'tags': {
            'tags_pos': [
                ['_', ''],
                ['/', '']
            ],

            'tags_non_pos': [
                ['<', '>'],
                ['[', ']']
            ]
        },

        'sentence_tokenization': {
            'sentence_tokenizers': {
                'afr': main.tr('spaCy - Sentencizer'),
                'sqi': main.tr('spaCy - Sentencizer'),
                'ara': main.tr('spaCy - Sentencizer'),
                'hye': main.tr('spaCy - Sentencizer'),
                'eus': main.tr('spaCy - Sentencizer'),
                'ben': main.tr('spaCy - Sentencizer'),
                'bul': main.tr('spaCy - Sentencizer'),
                'cat': main.tr('spaCy - Sentencizer'),
                'zho_cn': main.tr('Wordless - Chinese Sentence Tokenizer'),
                'zho_tw': main.tr('Wordless - Chinese Sentence Tokenizer'),
                'hrv': main.tr('spaCy - Sentencizer'),
                'ces': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'dan': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'nld': main.tr('spaCy - Sentencizer'),
                'eng': main.tr('syntok - Sentence Segmenter'),
                'est': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'fin': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'fra': main.tr('spaCy - Sentencizer'),
                'deu': main.tr('syntok - Sentence Segmenter'),
                'ell': main.tr('spaCy - Sentencizer'),
                'heb': main.tr('spaCy - Sentencizer'),
                'hin': main.tr('spaCy - Sentencizer'),
                'hun': main.tr('spaCy - Sentencizer'),
                'isl': main.tr('spaCy - Sentencizer'),
                'ind': main.tr('spaCy - Sentencizer'),
                'gle': main.tr('spaCy - Sentencizer'),
                'ita': main.tr('spaCy - Sentencizer'),
                'jpn': main.tr('Wordless - Japanese Sentence Tokenizer'),
                'kan': main.tr('spaCy - Sentencizer'),
                'lav': main.tr('spaCy - Sentencizer'),
                'lit': main.tr('spaCy - Sentencizer'),
                'ltz': main.tr('spaCy - Sentencizer'),
                'nob': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'nno': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'fas': main.tr('spaCy - Sentencizer'),
                'pol': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'por': main.tr('spaCy - Sentencizer'),
                'ron': main.tr('spaCy - Sentencizer'),
                'rus': main.tr('razdel - Russian Sentenizer'),
                'sin': main.tr('spaCy - Sentencizer'),
                'slk': main.tr('spaCy - Sentencizer'),
                'slv': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'spa': main.tr('syntok - Sentence Segmenter'),
                'swe': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'tgl': main.tr('spaCy - Sentencizer'),
                'tam': main.tr('spaCy - Sentencizer'),
                'tat': main.tr('spaCy - Sentencizer'),
                'tel': main.tr('spaCy - Sentencizer'),
                'tha': main.tr('PyThaiNLP - CRFCut'),
                'bod': main.tr('botok - Tibetan Sentence Tokenizer'),
                'tur': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'ukr': main.tr('spaCy - Sentencizer'),
                'urd': main.tr('spaCy - Sentencizer'),
                'vie': main.tr('Underthesea - Vietnamese Sentence Tokenizer'),

                'other': main.tr('NLTK - Punkt Sentence Tokenizer')
            },

            'preview_lang': 'eng',
            'preview_samples': '',
            'preview_results': ''
        },

        'word_tokenization': {
            'word_tokenizers': {
                'afr': main.tr('spaCy - Afrikaans Word Tokenizer'),
                'sqi': main.tr('spaCy - Albanian Word Tokenizer'),
                'ara': main.tr('spaCy - Arabic Word Tokenizer'),
                'hye': main.tr('spaCy - Armenian Word Tokenizer'),
                'eus': main.tr('spaCy - Basque Word Tokenizer'),
                'ben': main.tr('spaCy - Bengali Word Tokenizer'),
                'bul': main.tr('spaCy - Bulgarian Word Tokenizer'),
                'cat': main.tr('spaCy - Catalan Word Tokenizer'),
                'zho_cn': main.tr('jieba - Chinese Word Tokenizer'),
                'zho_tw': main.tr('jieba - Chinese Word Tokenizer'),
                'hrv': main.tr('spaCy - Croatian Word Tokenizer'),
                'ces': main.tr('spaCy - Czech Word Tokenizer'),
                'dan': main.tr('spaCy - Danish Word Tokenizer'),
                'nld': main.tr('spaCy - Dutch Word Tokenizer'),
                'eng': main.tr('spaCy - English Word Tokenizer'),
                'fin': main.tr('spaCy - Finnish Word Tokenizer'),
                'fra': main.tr('spaCy - French Word Tokenizer'),
                'deu': main.tr('spaCy - German Word Tokenizer'),
                'ell': main.tr('spaCy - Greek (Modern) Word Tokenizer'),
                'heb': main.tr('spaCy - Hebrew Word Tokenizer'),
                'hin': main.tr('spaCy - Hindi Word Tokenizer'),
                'hun': main.tr('spaCy - Hungarian Word Tokenizer'),
                'isl': main.tr('spaCy - Icelandic Word Tokenizer'),
                'ind': main.tr('spaCy - Indonesian Word Tokenizer'),
                'gle': main.tr('spaCy - Irish Word Tokenizer'),
                'ita': main.tr('spaCy - Italian Word Tokenizer'),
                'jpn': main.tr('nagisa - Japanese Word Tokenizer'),
                'kan': main.tr('spaCy - Kannada Word Tokenizer'),
                'lav': main.tr('Sacremoses - Moses Tokenizer'),
                'lit': main.tr('spaCy - Lithuanian Word Tokenizer'),
                'ltz': main.tr('spaCy - Luxembourgish Word Tokenizer'),
                'mar': main.tr('spaCy - Marathi Word Tokenizer'),
                'nob': main.tr('spaCy - Norwegian Bokmål Word Tokenizer'),
                'fas': main.tr('spaCy - Persian Word Tokenizer'),
                'pol': main.tr('spaCy - Polish Word Tokenizer'),
                'por': main.tr('spaCy - Portuguese Word Tokenizer'),
                'ron': main.tr('spaCy - Romanian Word Tokenizer'),
                'rus': main.tr('razdel - Russian Word Tokenizer'),
                'srp_cyrl': main.tr('spaCy - Serbian Word Tokenizer'),
                'srp_latn': main.tr('spaCy - Serbian Word Tokenizer'),
                'sin': main.tr('spaCy - Sinhala Word Tokenizer'),
                'slk': main.tr('spaCy - Slovak Word Tokenizer'),
                'slv': main.tr('spaCy - Slovenian Word Tokenizer'),
                'spa': main.tr('spaCy - Spanish Word Tokenizer'),
                'swe': main.tr('spaCy - Swedish Word Tokenizer'),
                'tgl': main.tr('spaCy - Tagalog Word Tokenizer'),
                'tgk': main.tr('NLTK - Tok-tok Tokenizer'),
                'tam': main.tr('spaCy - Tamil Word Tokenizer'),
                'tat': main.tr('spaCy - Tatar Word Tokenizer'),
                'tel': main.tr('spaCy - Telugu Word Tokenizer'),
                'tha': main.tr('PyThaiNLP - Maximum Matching + TCC'),
                'bod': main.tr('botok - Tibetan Word Tokenizer'),
                'tur': main.tr('spaCy - Turkish Word Tokenizer'),
                'ukr': main.tr('spaCy - Ukrainian Word Tokenizer'),
                'urd': main.tr('spaCy - Urdu Word Tokenizer'),
                'vie': main.tr('Underthesea - Vietnamese Word Tokenizer'),

                'other': main.tr('spaCy - English Word Tokenizer')
            },

            'preview_lang': 'eng',
            'preview_samples': '',
            'preview_results': ''
        },

        'word_detokenization': {
            'word_detokenizers': {
                'cat': main.tr('Sacremoses - Moses Detokenizer'),
                'zho_cn': main.tr('Wordless - Chinese Word Detokenizer'),
                'zho_tw': main.tr('Wordless - Chinese Word Detokenizer'),
                'ces': main.tr('Sacremoses - Moses Detokenizer'),
                'nld': main.tr('Sacremoses - Moses Detokenizer'),
                'eng': main.tr('Sacremoses - Moses Detokenizer'),
                'fin': main.tr('Sacremoses - Moses Detokenizer'),
                'fra': main.tr('Sacremoses - Moses Detokenizer'),
                'deu': main.tr('Sacremoses - Moses Detokenizer'),
                'ell': main.tr('Sacremoses - Moses Detokenizer'),
                'hun': main.tr('Sacremoses - Moses Detokenizer'),
                'isl': main.tr('Sacremoses - Moses Detokenizer'),
                'gle': main.tr('Sacremoses - Moses Detokenizer'),
                'ita': main.tr('Sacremoses - Moses Detokenizer'),
                'jpn': main.tr('Wordless - Japanese Word Detokenizer'),
                'lav': main.tr('Sacremoses - Moses Detokenizer'),
                'lit': main.tr('Sacremoses - Moses Detokenizer'),
                'pol': main.tr('Sacremoses - Moses Detokenizer'),
                'por': main.tr('Sacremoses - Moses Detokenizer'),
                'ron': main.tr('Sacremoses - Moses Detokenizer'),
                'rus': main.tr('Sacremoses - Moses Detokenizer'),
                'slk': main.tr('Sacremoses - Moses Detokenizer'),
                'slv': main.tr('Sacremoses - Moses Detokenizer'),
                'spa': main.tr('Sacremoses - Moses Detokenizer'),
                'swe': main.tr('Sacremoses - Moses Detokenizer'),
                'tam': main.tr('Sacremoses - Moses Detokenizer'),
                'tha': main.tr('Wordless - Thai Word Detokenizer'),
                'bod': main.tr('Wordless - Tibetan Word Detokenizer'),

                'other': main.tr('Sacremoses - Moses Detokenizer')
            },

            'preview_lang': 'eng',
            'preview_samples': '',
            'preview_results': ''
        },

        'pos_tagging': {
            'pos_taggers': {
                'zho_cn': main.tr('jieba - Chinese POS Tagger'),
                'zho_tw':  main.tr('jieba - Chinese POS Tagger'),
                'dan': main.tr('spaCy - Danish POS Tagger'),
                'nld': main.tr('spaCy - Dutch POS Tagger'),
                'eng': main.tr('spaCy - English POS Tagger'),
                'fra': main.tr('spaCy - French POS Tagger'),
                'deu': main.tr('spaCy - German POS Tagger'),
                'ell': main.tr('spaCy - Greek (Modern) POS Tagger'),
                'ita': main.tr('spaCy - Italian POS Tagger'),
                'jpn': main.tr('nagisa - Japanese POS Tagger'),
                'lit': main.tr('spaCy - Lithuanian POS Tagger'),
                'nob': main.tr('spaCy - Norwegian Bokmål POS Tagger'),
                'por': main.tr('spaCy - Portuguese POS Tagger'),
                'rus': main.tr('pymorphy2 - Morphological Analyzer'),
                'spa': main.tr('spaCy - Spanish POS Tagger'),
                'tha': main.tr('PyThaiNLP - Perceptron Tagger (ORCHID)'),
                'bod': main.tr('botok - Tibetan POS Tagger'),
                'ukr': main.tr('pymorphy2 - Morphological Analyzer'),
                'vie': main.tr('Underthesea - Vietnamese POS Tagger')
            },

            'to_universal_pos_tags': False,

            'preview_lang': 'eng',
            'preview_samples': '',
            'preview_results': ''
        },

        'tagsets': {
            'preview_lang': 'eng',

            'preview_pos_tagger': {
                'zho_cn': main.tr('jieba - Chinese POS Tagger'),
                'zho_tw': main.tr('jieba - Chinese POS Tagger'),
                'dan': main.tr('spaCy - Danish POS Tagger'),
                'nld': main.tr('spaCy - Dutch POS Tagger'),
                'eng': main.tr('spaCy - English POS Tagger'),
                'fra': main.tr('spaCy - French POS Tagger'),
                'deu': main.tr('spaCy - German POS Tagger'),
                'ell': main.tr('spaCy - Greek (Modern) POS Tagger'),
                'ita': main.tr('spaCy - Italian POS Tagger'),
                'jpn': main.tr('nagisa - Japanese POS Tagger'),
                'lit': main.tr('spaCy - Lithuanian POS Tagger'),
                'nob': main.tr('spaCy - Norwegian Bokmål POS Tagger'),
                'pol': main.tr('spaCy - Polish POS Tagger'),
                'por': main.tr('spaCy - Portuguese POS Tagger'),
                'ron': main.tr('spaCy - Romanian POS Tagger'),
                'rus': main.tr('pymorphy2 - Morphological Analyzer'),
                'spa': main.tr('spaCy - Spanish POS Tagger'),
                'tha': main.tr('PyThaiNLP - Perceptron Tagger (ORCHID)'),
                'bod': main.tr('botok - Tibetan POS Tagger'),
                'ukr': main.tr('pymorphy2 - Morphological Analyzer'),
                'vie': main.tr('Underthesea - Vietnamese POS Tagger')
            },

            'mappings': {
                'zho_cn': {
                    main.tr('jieba - Chinese POS Tagger'): wl_tagset_zho_jieba.MAPPINGS
                },

                'zho_tw': {
                    main.tr('jieba - Chinese POS Tagger'): wl_tagset_zho_jieba.MAPPINGS
                },

                'eng': {
                    main.tr('NLTK - Perceptron POS Tagger'): wl_tagset_eng_penn_treebank.MAPPINGS,
                },

                'jpn': {
                    main.tr('nagisa - Japanese POS Tagger'): wl_tagset_jpn_unidic.MAPPINGS
                },

                'rus': {
                    main.tr('NLTK - Perceptron POS Tagger'): wl_tagset_rus_russian_national_corpus.MAPPINGS,
                    main.tr('pymorphy2 - Morphological Analyzer'): wl_tagset_rus_open_corpora.MAPPINGS
                },

                'tha': {
                    main.tr('PyThaiNLP - Perceptron Tagger (ORCHID)'): wl_tagset_tha_orchid.MAPPINGS,
                    main.tr('PyThaiNLP - Perceptron Tagger (PUD)'): wl_tagset_universal.MAPPINGS
                },

                'bod': {
                    main.tr('botok - Tibetan POS Tagger'): wl_tagset_bod_botok.MAPPINGS
                },

                'ukr': {
                    main.tr('pymorphy2 - Morphological Analyzer'): wl_tagset_rus_open_corpora.MAPPINGS
                },

                'vie': {
                    main.tr('Underthesea - Vietnamese POS Tagger'): wl_tagset_vie_underthesea.MAPPINGS
                }
            }
        },

        'lemmatization': {
            'lemmatizers': {
                'ast': main.tr('Lemmatization Lists - Asturian Lemma List'),
                'bul': main.tr('Lemmatization Lists - Bulgarian Lemma List'),
                'cat': main.tr('Lemmatization Lists - Catalan Lemma List'),
                'ces': main.tr('Lemmatization Lists - Czech Lemma List'),
                'dan': main.tr('spaCy - Danish Lemmatizer'),
                'nld': main.tr('spaCy - Dutch Lemmatizer'),
                'eng': main.tr('spaCy - English Lemmatizer'),
                'est': main.tr('Lemmatization Lists - Estonian Lemma List'),
                'fra': main.tr('spaCy - French Lemmatizer'),
                'glg': main.tr('Lemmatization Lists - Galician Lemma List'),
                'deu': main.tr('spaCy - German Lemmatizer'),
                'grc': main.tr('lemmalist-greek - Greek (Ancient) Lemma List'),
                'ell': main.tr('spaCy - Greek (Modern) Lemmatizer'),
                'hun': main.tr('Lemmatization Lists - Hungarian Lemma List'),
                'gle': main.tr('Lemmatization Lists - Irish Lemma List'),
                'ita': main.tr('spaCy - Italian Lemmatizer'),
                'lit': main.tr('spaCy - Lithuanian Lemmatizer'),
                'glv': main.tr('Lemmatization Lists - Manx Lemma List'),
                'nob': main.tr('spaCy - Norwegian Bokmål Lemmatizer'),
                'fas': main.tr('Lemmatization Lists - Persian Lemma List'),
                'pol': main.tr('spaCy - Polish Lemmatizer'),
                'por': main.tr('spaCy - Portuguese Lemmatizer'),
                'ron': main.tr('spaCy - Romanian Lemmatizer'),
                'rus': main.tr('pymorphy2 - Morphological Analyzer'),
                'gla': main.tr('Lemmatization Lists - Scottish Gaelic Lemma List'),
                'slk': main.tr('Lemmatization Lists - Slovak Lemma List'),
                'slv': main.tr('Lemmatization Lists - Slovenian Lemma List'),
                'spa': main.tr('spaCy - Spanish Lemmatizer'),
                'swe': main.tr('Lemmatization Lists - Swedish Lemma List'),
                'bod': main.tr('botok - Tibetan Lemmatizer'),
                'ukr': main.tr('pymorphy2 - Morphological Analyzer'),
                'cym': main.tr('Lemmatization Lists - Welsh Lemma List')
            },

            'preview_lang': 'eng',
            'preview_samples': '',
            'preview_results': ''

        },

        'stop_words': {
            'stop_words': {
                'afr': main.tr('Stopwords ISO - Afrikaans Stop Words'),
                'sqi': main.tr('spaCy - Albanian Stop Words'),
                'ara': main.tr('Stopwords ISO - Arabic Stop Words'),
                'hye': main.tr('Stopwords ISO - Armenian Stop Words'),
                'aze': main.tr('NLTK - Azerbaijani Stop Words'),
                'eus': main.tr('Stopwords ISO - Basque Stop Words'),
                'bel': main.tr('extra-stopwords - Belarusian Stop Words'),
                'ben': main.tr('Stopwords ISO - Bengali Stop Words'),
                'bre': main.tr('Stopwords ISO - Breton Stop Words'),
                'bul': main.tr('Stopwords ISO - Bulgarian Stop Words'),
                'cat': main.tr('Stopwords ISO - Catalan Stop Words'),
                'zho_cn': main.tr('Stopwords ISO - Chinese (Simplified) Stop Words'),
                'zho_tw': main.tr('Stopwords ISO - Chinese (Traditional) Stop Words'),
                'hrv': main.tr('Stopwords ISO - Croatian Stop Words'),
                'ces': main.tr('Stopwords ISO - Czech Stop Words'),
                'dan': main.tr('Stopwords ISO - Danish Stop Words'),
                'nld': main.tr('Stopwords ISO - Dutch Stop Words'),
                'eng': main.tr('Stopwords ISO - English Stop Words'),
                'epo': main.tr('Stopwords ISO - Esperanto Stop Words'),
                'est': main.tr('Stopwords ISO - Estonian Stop Words'),
                'fin': main.tr('Stopwords ISO - Finnish Stop Words'),
                'fra': main.tr('Stopwords ISO - French Stop Words'),
                'glg': main.tr('Stopwords ISO - Galician Stop Words'),
                'deu': main.tr('Stopwords ISO - German Stop Words'),
                'grc': main.tr('Stopwords ISO - Greek Stop Words'),
                'ell': main.tr('Stopwords ISO - Greek Stop Words'),
                'guj': main.tr('Stopwords ISO - Gujarati Stop Words'),
                'hau': main.tr('Stopwords ISO - Hausa Stop Words'),
                'heb': main.tr('Stopwords ISO - Hebrew Stop Words'),
                'hin': main.tr('Stopwords ISO - Hindi Stop Words'),
                'hun': main.tr('Stopwords ISO - Hungarian Stop Words'),
                'isl': main.tr('spaCy - Icelandic Stop Words'),
                'ind': main.tr('Stopwords ISO - Indonesian Stop Words'),
                'gle': main.tr('Stopwords ISO - Irish Stop Words'),
                'ita': main.tr('Stopwords ISO - Italian Stop Words'),
                'jpn': main.tr('Stopwords ISO - Japanese Stop Words'),
                'kan': main.tr('spaCy - Kannada Stop Words'),
                'kaz': main.tr('NLTK - Kazakh Stop Words'),
                'kor': main.tr('Stopwords ISO - Korean Stop Words'),
                'kur': main.tr('Stopwords ISO - Kurdish Stop Words'),
                'lat': main.tr('Stopwords ISO - Latin Stop Words'),
                'lav': main.tr('Stopwords ISO - Latvian Stop Words'),
                'lit': main.tr('Stopwords ISO - Lithuanian Stop Words'),
                'msa': main.tr('Stopwords ISO - Malay Stop Words'),
                'mar': main.tr('Stopwords ISO - Marathi Stop Words'),
                'mon': main.tr('extra-stopwords - Mongolian Stop Words'),
                'nep': main.tr('NLTK - Nepali Stop Words'),
                'nob': main.tr('Stopwords ISO - Norwegian Stop Words'),
                'nno': main.tr('Stopwords ISO - Norwegian Stop Words'),
                'fas': main.tr('Stopwords ISO - Persian Stop Words'),
                'pol': main.tr('Stopwords ISO - Polish Stop Words'),
                'por': main.tr('Stopwords ISO - Portuguese Stop Words'),
                'ron': main.tr('Stopwords ISO - Romanian Stop Words'),
                'rus': main.tr('Stopwords ISO - Russian Stop Words'),
                'srp_cyrl': main.tr('spaCy - Serbian (Cyrillic) Stop Words'),
                'srp_latn': main.tr('spaCy - Serbian (Latin) Stop Words'),
                'sin': main.tr('spaCy - Sinhala Stop Words'),
                'slk': main.tr('Stopwords ISO - Slovak Stop Words'),
                'slv': main.tr('Stopwords ISO - Slovenian Stop Words'),
                'som': main.tr('Stopwords ISO - Somali Stop Words'),
                'sot': main.tr('Stopwords ISO - Sotho (Southern) Stop Words'),
                'spa': main.tr('Stopwords ISO - Spanish Stop Words'),
                'swa': main.tr('Stopwords ISO - Swahili Stop Words'),
                'swe': main.tr('Stopwords ISO - Swedish Stop Words'),
                'tgl': main.tr('Stopwords ISO - Tagalog Stop Words'),
                'tgk': main.tr('NLTK - Tajik Stop Words'),
                'tam': main.tr('spaCy - Tamil Stop Words'),
                'tat': main.tr('spaCy - Tatar Stop Words'),
                'tel': main.tr('spaCy - Telugu Stop Words'),
                'tha': main.tr('PyThaiNLP - Thai Stop Words'),
                'tur': main.tr('Stopwords ISO - Turkish Stop Words'),
                'ukr': main.tr('Stopwords ISO - Ukrainian Stop Words'),
                'urd': main.tr('Stopwords ISO - Urdu Stop Words'),
                'vie': main.tr('Stopwords ISO - Vietnamese Stop Words'),
                'yor': main.tr('Stopwords ISO - Yoruba Stop Words'),
                'zul': main.tr('Stopwords ISO - Zulu Stop Words')
            },

            'custom_lists': {
                'afr': [],
                'sqi': [],
                'ara': [],
                'hye': [],
                'aze': [],
                'eus': [],
                'bel': [],
                'ben': [],
                'bre': [],
                'bul': [],
                'cat': [],
                'zho_cn': [],
                'zho_tw': [],
                'hrv': [],
                'ces': [],
                'dan': [],
                'nld': [],
                'eng': [],
                'epo': [],
                'est': [],
                'fin': [],
                'fra': [],
                'glg': [],
                'deu': [],
                'grc': [],
                'ell': [],
                'guj': [],
                'hau': [],
                'heb': [],
                'hin': [],
                'hun': [],
                'isl': [],
                'ind': [],
                'gle': [],
                'ita': [],
                'jpn': [],
                'kan': [],
                'kaz': [],
                'kor': [],
                'kur': [],
                'lat': [],
                'lav': [],
                'lit': [],
                'msa': [],
                'mar': [],
                'mon': [],
                'nep': [],
                'nob': [],
                'nno': [],
                'fas': [],
                'pol': [],
                'por': [],
                'ron': [],
                'rus': [],
                'srp_cyrl': [],
                'srp_latn': [],
                'sin': [],
                'slk': [],
                'slv': [],
                'sot': [],
                'som': [],
                'spa': [],
                'swa': [],
                'swe': [],
                'tgl': [],
                'tgk': [],
                'tam': [],
                'tat': [],
                'tel': [],
                'tha': [],
                'tur': [],
                'ukr': [],
                'urd': [],
                'vie': [],
                'yor': [],
                'zul': [],
                'other': []
            },

            'preview_lang': 'eng',
        },

        'measures': {
            'dispersion': {
                'general': {
                    'number_sections': 5
                }
            },

            'adjusted_freq': {
                'general': {
                    'number_sections': 5,
                    'use_same_settings_dispersion': True
                }
            },

            'statistical_significance': {
                'z_score': {
                    'direction': 'Two-tailed'
                },

                'students_t_test_2_sample': {
                    'number_sections': 5,
                    'use_data': main.tr('Relative Frequency'),
                    'variances': main.tr('Equal'),
                },

                'pearsons_chi_squared_test': {
                    'apply_correction': True
                },

                'fishers_exact_test': {
                    'direction': main.tr('Two-tailed')
                },

                'mann_whitney_u_test': {
                    'number_sections': 5,
                    'use_data': main.tr('Relative Frequency'),
                    'direction': main.tr('Two-tailed'),
                    'apply_correction': True
                }
            },

            'effect_size': {
                'kilgarriffs_ratio': {
                    'smoothing_param': 1.00
                }
            }
        },

        'figs': {
            'line_chart': {
                'font': 'Arial'
            },

            'word_cloud': {
                'font': 'Code2000',
                'bg_color': '#FFFFFF'
            },

            'network_graph': {
                'layout': 'Spring',
                'node_font': 'Arial',
                'node_font_size': 10,
                'edge_font': 'Arial',
                'edge_font_size': 8,
                'edge_color': '#5C88C5'
            }
        }
    }

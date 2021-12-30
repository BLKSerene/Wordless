#
# Wordless: Settings - Default Settings
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
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
    wl_tagset_tha_lst20,
    wl_tagset_tha_orchid,
    wl_tagset_bod_botok,
    wl_tagset_vie_underthesea,
    wl_tagset_zho_jieba
)
from wl_utils import wl_misc

def init_settings_default(main):
    main.settings_default = {
        '1st_startup': True,
        'work_area_cur': main.tr('Overview'),

        'layouts': {
            'central_widget': [main.height() - 100 - 210, 210]
        },

        'file_area': {
            'files_open': [],
            'files_closed': [],

            'folder_settings': {
                'subfolders': True
            },

            'auto_detection_settings': {
                'detect_langs': True,
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
            'parallel_mode': False,
            'token_settings': {
                'puncs': False,

                'ignore_tags': True,
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
                    'match_tags': False,
                    
                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                }
            },
            
            'generation_settings': {
                'width_left_para': 0,
                'width_left_sentence': 0,
                'width_left_token': 10,
                'width_left_char': 50,
                'width_right_para': 0,
                'width_right_sentence': 0,
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

            'zapping_settings': {
                'zapping': False,
                'replace_keywords_with': 15,
                'placeholder': '_',
                'add_line_nums': True,
                'discard_position_info': True,
                'randomize_outputs': True
            },

            'sort_results': {
                'sorting_rules': [
                    [main.tr('Node'), 0],
                    [main.tr('File'), 0],
                    [main.tr('Token No.'), 0]
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
                'match_tags': False
            }
        },

        'concordancer_parallel': {
            'parallel_mode': False,
            'token_settings': {
                'puncs': False,

                'ignore_tags': True,
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
                    'match_tags': False,
                    
                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                }
            },
            
            'generation_settings': {
                'src_file': '',
                'tgt_file': '',

                'sampling_method': main.tr('None'),
                'sample_size_first_n_lines': 100,
                'sample_size_systematic_fixed_interval': 2,
                'sample_size_systematic_fixed_size': 100,
                'sample_size_random': 100
            },

            'table_settings': {
                'show_pct': True
            },

            'sort_results': {
                'sorting_rules': [
                    [main.tr('Node'), 0],
                    [main.tr('Segment No.'), 0]
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
                'use_tags': False
            },

            'generation_settings': {
                'measure_dispersion': main.tr("Juilland's D"),
                'measure_adjusted_freq': main.tr("Juilland's U")
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

                'measure_dispersion': main.tr("Juilland's D"),
                'measure_adjusted_freq': main.tr("Juilland's U")
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

                'limit_searching': main.tr('None'),

                'test_significance': main.tr("Pearson's Chi-squared Test"),
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

                'limit_searching': main.tr('None'),

                'test_significance': main.tr("Pearson's Chi-squared Test"),
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
                'use_tags': False
            },

            'generation_settings': {
                'ref_files': [],
                'test_significance': main.tr('Log-likelihood Ratio Test'),
                'measure_effect_size': main.tr("Kilgarriff's Ratio"),
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
                'font_size': 14
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
                'default_encoding': 'utf_8',
                'detect_encodings': True
            },

            'stop_words': {
                'default_path': wl_misc.get_normalized_path('.'),
                'default_encoding': 'utf_8',
                'detect_encodings': True
            },

            'temp_files': {
                'default_path': wl_misc.get_normalized_path('Import/'),
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

        'files': {
            'default_settings': {
                'lang': 'eng_us',
                'tokenized': main.tr('No'),
                'tagged': main.tr('No'),
                'encoding': 'utf_8'
            },

            'auto_detection_settings': {
                'number_lines': 100,
                'number_lines_no_limit': False
            },

            'misc': {
                'read_files_in_chunks': 100
            }
        },

        'tags': {
            'tags_header': [
                ['Non-embedded', 'Header', '<teiHeader>', '</teiHeader>']
            ],

            'tags_body': [
                ['Embedded', 'Part of Speech', '_', ''],
                ['Non-embedded', 'Others', '<*>', '</*>']
            ],

            'tags_xml': [
                ['Non-embedded', 'Paragraph', '<p>', '</p>'],
                ['Non-embedded', 'Sentence', '<s>', '</s>'],
                ['Non-embedded', 'Word', '<w>', '</w>'],
                ['Non-embedded', 'Word', '<c>', '</c>']
            ]
        },

        'data': {
            'continue_numbering_after_ties': False,
            
            'precision_decimal': 2,
            'precision_pct': 2,
            'precision_p_value': 5
        },

        'sentence_tokenization': {
            'sentence_tokenizers': {
                'afr': 'spacy_sentencizer',
                'sqi': 'spacy_sentencizer',
                'amh': 'spacy_sentencizer',
                'ara': 'spacy_sentencizer',
                'hye': 'spacy_sentencizer',
                'aze': 'spacy_sentencizer',
                'eus': 'spacy_sentencizer',
                'ben': 'spacy_sentencizer',
                'bul': 'spacy_sentencizer',
                'cat': 'spacy_sentencizer',
                'zho_cn': 'spacy_sentence_recognizer',
                'zho_tw': 'spacy_sentence_recognizer',
                'hrv': 'spacy_sentencizer',
                'ces': 'nltk_punkt',
                'dan': 'spacy_sentence_recognizer',
                'nld': 'spacy_sentence_recognizer',
                'eng_gb': 'spacy_sentence_recognizer',
                'eng_us': 'spacy_sentence_recognizer',
                'est': 'nltk_punkt',
                'fin': 'nltk_punkt',
                'fra': 'spacy_sentence_recognizer',
                'deu_at': 'spacy_sentence_recognizer',
                'deu_de': 'spacy_sentence_recognizer',
                'deu_ch': 'spacy_sentence_recognizer',
                'grc': 'spacy_sentencizer',
                'ell': 'spacy_sentence_recognizer',
                'guj': 'spacy_sentencizer',
                'heb': 'spacy_sentencizer',
                'hin': 'spacy_sentencizer',
                'hun': 'spacy_sentencizer',
                'isl': 'tokenizer_isl',
                'ind': 'spacy_sentencizer',
                'gle': 'spacy_sentencizer',
                'ita': 'spacy_sentence_recognizer',
                'jpn': 'wordless_jpn',
                'kan': 'spacy_sentencizer',
                'kir': 'spacy_sentencizer',
                'lav': 'spacy_sentencizer',
                'lij': 'spacy_sentence_recognizer',
                'lit': 'spacy_sentencizer',
                'ltz': 'spacy_sentencizer',
                'mkd': 'spacy_sentencizer',
                'mal': 'spacy_sentencizer',
                'mar': 'spacy_sentencizer',
                'nep': 'spacy_sentencizer',
                'nob': 'spacy_sentence_recognizer',
                'nno': 'nltk_punkt',
                'fas': 'spacy_sentencizer',
                'pol': 'spacy_sentence_recognizer',
                'por_br': 'spacy_sentence_recognizer',
                'por_pt': 'spacy_sentence_recognizer',
                'ron': 'spacy_sentence_recognizer',
                'rus': 'spacy_sentence_recognizer',
                'san': 'spacy_sentencizer',
                'srp_cyrl': 'spacy_sentencizer',
                'srp_latn': 'spacy_sentencizer',
                'sin': 'spacy_sentencizer',
                'slk': 'spacy_sentencizer',
                'slv': 'nltk_punkt',
                'spa': 'spacy_sentence_recognizer',
                'swe': 'nltk_punkt',
                'tgl': 'spacy_sentencizer',
                'tam': 'spacy_sentencizer',
                'tat': 'spacy_sentencizer',
                'tel': 'spacy_sentencizer',
                'tha': 'pythainlp_crfcut',
                'bod': 'botok_bod',
                'tir': 'spacy_sentencizer',
                'tsn': 'spacy_sentencizer',
                'tur': 'nltk_punkt',
                'ukr': 'spacy_sentencizer',
                'urd': 'spacy_sentencizer',
                'vie': 'underthesea_vie',
                'yor': 'spacy_sentencizer',

                'other': 'spacy_sentence_recognizer'
            },

            'preview_lang': 'eng_us',
            'preview_samples': '',
            'preview_results': ''
        },

        'word_tokenization': {
            'word_tokenizers': {
                'afr': 'spacy_afr',
                'sqi': 'spacy_sqi',
                'amh': 'spacy_amh',
                'ara': 'spacy_ara',
                'hye': 'spacy_hye',
                'asm': 'sacremoses_moses',
                'aze': 'spacy_aze',
                'eus': 'spacy_eus',
                'ben': 'spacy_ben',
                'bul': 'spacy_bul',
                'cat': 'spacy_cat',
                'zho_cn': 'spacy_zho',
                'zho_tw': 'spacy_zho',
                'hrv': 'spacy_hrv',
                'ces': 'spacy_ces',
                'dan': 'spacy_dan',
                'nld': 'spacy_nld',
                'eng_gb': 'spacy_eng',
                'eng_us': 'spacy_eng',
                'est': 'spacy_est',
                'fin': 'spacy_fin',
                'fra': 'spacy_fra',
                'deu_at': 'spacy_deu',
                'deu_de': 'spacy_deu',
                'deu_ch': 'spacy_deu',
                'grc': 'spacy_grc',
                'ell': 'spacy_ell',
                'guj': 'spacy_guj',
                'heb': 'spacy_heb',
                'hin': 'spacy_hin',
                'hun': 'spacy_hun',
                'isl': 'tokenizer_isl',
                'ind': 'spacy_ind',
                'gle': 'spacy_gle',
                'ita': 'spacy_ita',
                'jpn': 'nagisa_jpn',
                'kan': 'spacy_kan',
                'kir': 'spacy_kir',
                'lav': 'spacy_lav',
                'lij': 'spacy_lij',
                'lit': 'spacy_lit',
                'ltz': 'spacy_ltz',
                'mkd': 'spacy_mkd',
                'mal': 'spacy_mal',
                'mar': 'spacy_mar',
                'mni': 'sacremoses_moses',
                'nep': 'spacy_nep',
                'nob': 'spacy_nob',
                'ori': 'sacremoses_moses',
                'fas': 'spacy_fas',
                'pol': 'spacy_pol',
                'por_br': 'spacy_por',
                'por_pt': 'spacy_por',
                'pan': 'sacremoses_moses',
                'ron': 'spacy_ron',
                'rus': 'razdel_rus',
                'san': 'spacy_san',
                'srp_cyrl': 'spacy_srp',
                'srp_latn': 'spacy_srp',
                'sin': 'spacy_sin',
                'slk': 'spacy_slk',
                'slv': 'spacy_slv',
                'spa': 'spacy_spa',
                'swe': 'spacy_swe',
                'tgl': 'spacy_tgl',
                'tgk': 'nltk_tok_tok',
                'tam': 'spacy_tam',
                'tat': 'spacy_tat',
                'tel': 'spacy_tel',
                'tdt': 'sacremoses_moses',
                'tha': 'pythainlp_max_matching_tcc',
                'bod': 'botok_bod',
                'tir': 'spacy_tir',
                'tsn': 'spacy_tsn',
                'tur': 'spacy_tur',
                'ukr': 'spacy_ukr',
                'urd': 'spacy_urd',
                'vie': 'underthesea_vie',
                'yor': 'spacy_yor',

                'other': 'spacy_eng'
            },

            'preview_lang': 'eng_us',
            'preview_samples': '',
            'preview_results': ''
        },

        'syl_tokenization': {
            'syl_tokenizers': {
                'afr': 'pyphen_afr',
                'sqi': 'pyphen_sqi',
                'bel': 'pyphen_bel',
                'bul': 'pyphen_bul',
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

            'preview_lang': 'eng_us',
            'preview_samples': '',
            'preview_results': ''
        },

        'word_detokenization': {
            'word_detokenizers': {
                'asm': 'sacremoses_moses',
                'ben': 'sacremoses_moses',
                'cat': 'sacremoses_moses',
                'zho_cn': 'wordless_zho',
                'zho_tw': 'wordless_zho',
                'ces': 'sacremoses_moses',
                'nld': 'sacremoses_moses',
                'eng_gb': 'sacremoses_moses',
                'eng_us': 'sacremoses_moses',
                'est': 'sacremoses_moses',
                'fin': 'sacremoses_moses',
                'fra': 'sacremoses_moses',
                'deu_at': 'sacremoses_moses',
                'deu_de': 'sacremoses_moses',
                'deu_ch': 'sacremoses_moses',
                'ell': 'sacremoses_moses',
                'guj': 'sacremoses_moses',
                'hin': 'sacremoses_moses',
                'hun': 'sacremoses_moses',
                'isl': 'sacremoses_moses',
                'gle': 'sacremoses_moses',
                'ita': 'sacremoses_moses',
                'jpn': 'wordless_jpn',
                'kan': 'sacremoses_moses',
                'lav': 'sacremoses_moses',
                'lit': 'sacremoses_moses',
                'mal': 'sacremoses_moses',
                'mar': 'sacremoses_moses',
                'mni': 'sacremoses_moses',
                'ori': 'sacremoses_moses',
                'pol': 'sacremoses_moses',
                'por_br': 'sacremoses_moses',
                'por_pt': 'sacremoses_moses',
                'pan': 'sacremoses_moses',
                'ron': 'sacremoses_moses',
                'rus': 'sacremoses_moses',
                'slk': 'sacremoses_moses',
                'slv': 'sacremoses_moses',
                'spa': 'sacremoses_moses',
                'swe': 'sacremoses_moses',
                'tam': 'sacremoses_moses',
                'tel': 'sacremoses_moses',
                'tdt': 'sacremoses_moses',
                'tha': 'wordless_tha',
                'bod': 'wordless_bod',

                'other': 'sacremoses_moses'
            },

            'preview_lang': 'eng_us',
            'preview_samples': '',
            'preview_results': ''
        },

        'pos_tagging': {
            'pos_taggers': {
                'cat': 'spacy_cat',
                'zho_cn': 'spacy_zho',
                'zho_tw': 'spacy_zho',
                'dan': 'spacy_dan',
                'nld': 'spacy_nld',
                'eng_gb': 'spacy_eng',
                'eng_us': 'spacy_eng',
                'fra': 'spacy_fra',
                'deu_at': 'spacy_deu',
                'deu_de': 'spacy_deu',
                'deu_ch': 'spacy_deu',
                'ell': 'spacy_ell',
                'ita': 'spacy_ita',
                'jpn': 'nagisa_jpn',
                'lit': 'spacy_lit',
                'mkd': 'spacy_mkd',
                'nob': 'spacy_nob',
                'pol': 'spacy_pol',
                'por_br': 'spacy_por',
                'por_pt': 'spacy_por',
                'ron': 'spacy_ron',
                'rus': 'spacy_rus',
                'spa': 'spacy_spa',
                'tha': 'pythainlp_perceptron_pud',
                'bod': 'botok_bod',
                'ukr': 'pymorphy2_morphological_analyzer',
                'vie': 'underthesea_vie'
            },

            'to_universal_pos_tags': False,

            'preview_lang': 'eng_us',
            'preview_samples': '',
            'preview_results': ''
        },

        'tagsets': {
            'preview_lang': 'eng_us',

            'preview_pos_tagger': {
                'cat': 'spacy_cat',
                'zho_cn': 'spacy_zho',
                'zho_tw': 'spacy_zho',
                'dan': 'spacy_dan',
                'nld': 'spacy_nld',
                'eng_gb': 'spacy_eng',
                'eng_us': 'spacy_eng',
                'fra': 'spacy_fra',
                'deu_at': 'spacy_deu',
                'deu_de': 'spacy_deu',
                'deu_ch': 'spacy_deu',
                'ell': 'spacy_ell',
                'ita': 'spacy_ita',
                'jpn': 'nagisa_jpn',
                'lit': 'spacy_lit',
                'mkd': 'spacy_mkd',
                'nob': 'spacy_nob',
                'pol': 'spacy_pol',
                'por_br': 'spacy_por',
                'por_pt': 'spacy_por',
                'ron': 'spacy_ron',
                'rus': 'spacy_rus',
                'spa': 'spacy_spa',
                'tha': 'pythainlp_perceptron_pud',
                'bod': 'botok_bod',
                'ukr': 'pymorphy2_morphological_analyzer',
                'vie': 'underthesea_vie'
            },

            'mappings': {
                'zho_cn': {
                    'jieba_zho': wl_tagset_zho_jieba.MAPPINGS
                },
                'zho_tw': {
                    'jieba_zho': wl_tagset_zho_jieba.MAPPINGS
                },

                'eng_gb': {
                    'nltk_perceptron': wl_tagset_eng_penn_treebank.MAPPINGS,
                },
                'eng_us': {
                    'nltk_perceptron': wl_tagset_eng_penn_treebank.MAPPINGS,
                },

                'jpn': {
                    'nagisa_jpn': wl_tagset_jpn_unidic.MAPPINGS
                },

                'rus': {
                    'nltk_perceptron': wl_tagset_rus_russian_national_corpus.MAPPINGS,
                    'pymorphy2_morphological_analyzer': wl_tagset_rus_open_corpora.MAPPINGS
                },

                'tha': {
                    'pythainlp_perceptron_lst20': wl_tagset_tha_lst20.MAPPINGS,
                    'pythainlp_perceptron_orchid': wl_tagset_tha_orchid.MAPPINGS,
                    'pythainlp_perceptron_pud': wl_tagset_universal.MAPPINGS
                },

                'bod': {
                    'botok_bod': wl_tagset_bod_botok.MAPPINGS
                },

                'ukr': {
                    'pymorphy2_morphological_analyzer': wl_tagset_rus_open_corpora.MAPPINGS
                },

                'vie': {
                    'underthesea_vie': wl_tagset_vie_underthesea.MAPPINGS
                }
            }
        },

        'lemmatization': {
            'lemmatizers': {
                'ast': 'lemmatization_lists_ast',
                'ben': 'spacy_ben',
                'bul': 'lemmatization_lists_bul',
                'cat': 'spacy_cat',
                'hrv': 'spacy_hrv',
                'ces': 'spacy_ces',
                'dan': 'spacy_dan',
                'nld': 'spacy_nld',
                'eng_gb': 'spacy_eng',
                'eng_us': 'spacy_eng',
                'est': 'lemmatization_lists_est',
                'fra': 'spacy_fra',
                'glg': 'lemmatization_lists_glg',
                'deu_at': 'spacy_deu',
                'deu_de': 'spacy_deu',
                'deu_ch': 'spacy_deu',
                'grc': 'lemmalist_greek_grc',
                'ell': 'spacy_ell',
                'hun': 'spacy_hun',
                'ind': 'spacy_ind',
                'gle': 'lemmatization_lists_gle',
                'ita': 'spacy_ita',
                'lit': 'spacy_lit',
                'ltz': 'spacy_ltz',
                'mkd': 'spacy_mkd',
                'glv': 'lemmatization_lists_glv',
                'nob': 'spacy_nob',
                'fas': 'spacy_fas',
                'pol': 'spacy_pol',
                'por_br': 'spacy_por',
                'por_pt': 'spacy_por',
                'ron': 'spacy_ron',
                'rus': 'spacy_rus',
                'gla': 'lemmatization_lists_gla',
                'srp_cyrl': 'spacy_srp_cyrl',
                'slk': 'lemmatization_lists_slk',
                'slv': 'lemmatization_lists_slv',
                'spa': 'spacy_spa',
                'swe': 'spacy_swe',
                'tgl': 'spacy_tgl',
                'bod': 'botok_bod',
                'tur': 'spacy_tur',
                'ukr': 'pymorphy2_morphological_analyzer',
                'urd': 'spacy_urd',
                'cym': 'lemmatization_lists_cym'
            },

            'preview_lang': 'eng_us',
            'preview_samples': '',
            'preview_results': ''

        },

        'stop_word_lists': {
            'stop_word_lists': {
                'afr': 'spacy_afr',
                'akk': 'cltk_akk',
                'sqi': 'spacy_sqi',
                'amh': 'spacy_amh',
                'ara': 'spacy_ara',
                'arb': 'cltk_arb',
                'hye': 'spacy_hye',
                'aze': 'spacy_aze',
                'eus': 'spacy_eus',
                'bel': 'extra_stopwords_bel',
                'ben': 'spacy_ben',
                'bre': 'stopwords_iso_bre',
                'bul': 'spacy_bul',
                'cat': 'spacy_cat',
                'zho_cn': 'spacy_zho_cn',
                'zho_tw': 'spacy_zho_tw',
                'cop': 'cltk_cop',
                'hrv': 'spacy_hrv',
                'ces': 'spacy_ces',
                'dan': 'spacy_dan',
                'nld': 'spacy_nld',
                'enm': 'cltk_enm',
                'ang': 'cltk_ang',
                'eng_gb': 'spacy_eng',
                'eng_us': 'spacy_eng',
                'epo': 'stopwords_iso_epo',
                'est': 'spacy_est',
                'fin': 'spacy_fin',
                'fra': 'spacy_fra',
                'fro': 'cltk_fro',
                'glg': 'stopwords_iso_glg',
                'deu_at': 'spacy_deu',
                'deu_de': 'spacy_deu',
                'gmh': 'cltk_gmh',
                'deu_ch': 'spacy_deu',
                'grc': 'spacy_grc',
                'ell': 'spacy_ell',
                'guj': 'spacy_guj',
                'hau': 'stopwords_iso_hau',
                'heb': 'spacy_heb',
                'hin': 'cltk_hin',
                'hun': 'spacy_hun',
                'isl': 'spacy_isl',
                'ind': 'spacy_ind',
                'gle': 'spacy_gle',
                'ita': 'spacy_ita',
                'jpn': 'spacy_jpn',
                'kan': 'spacy_kan',
                'kaz': 'nltk_kaz',
                'kor': 'spacy_kor',
                'kur': 'stopwords_iso_kur',
                'kir': 'spacy_kir',
                'lat': 'cltk_lat',
                'lav': 'spacy_lav',
                'lij': 'spacy_lij',
                'lit': 'spacy_lit',
                'ltz': 'spacy_ltz',
                'mkd': 'spacy_mkd',
                'msa': 'stopwords_iso_msa',
                'mal': 'spacy_mal',
                'mar': 'spacy_mar',
                'omr': 'cltk_omr',
                'mon': 'extra_stopwords_mon',
                'nep': 'spacy_nep',
                'non': 'cltk_non',
                'nob': 'spacy_nob',
                'nno': 'nltk_nno',
                'fas': 'spacy_fas',
                'pol': 'spacy_pol',
                'por_br': 'spacy_por',
                'por_pt': 'spacy_por',
                'pan': 'cltk_pan',
                'ron': 'spacy_ron',
                'rus': 'spacy_rus',
                'san': 'cltk_san',
                'srp_cyrl': 'spacy_srp_cyrl',
                'srp_latn': 'spacy_srp_latn',
                'sin': 'spacy_sin',
                'slk': 'spacy_slk',
                'slv': 'spacy_slv',
                'som': 'stopwords_iso_som',
                'sot': 'stopwords_iso_sot',
                'spa': 'spacy_spa',
                'swa': 'stopwords_iso_swa',
                'swe': 'spacy_swe',
                'tgl': 'spacy_tgl',
                'tgk': 'nltk_tgk',
                'tam': 'spacy_tam',
                'tat': 'spacy_tat',
                'tel': 'spacy_tel',
                'tha': 'pythainlp_tha',
                'tir': 'spacy_tir',
                'tsn': 'spacy_tsn',
                'tur': 'spacy_tur',
                'ukr': 'spacy_ukr',
                'urd': 'spacy_urd',
                'vie': 'spacy_vie',
                'yor': 'spacy_yor',
                'zul': 'stopwords_iso_zul',

                'other': 'custom'
            },

            'custom_lists': {
                'afr': [],
                'akk': [],
                'sqi': [],
                'amh': [],
                'ara': [],
                'arb': [],
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
                'cop': [],
                'hrv': [],
                'ces': [],
                'dan': [],
                'nld': [],
                'enm': [],
                'ang': [],
                'eng_gb': [],
                'eng_us': [],
                'epo': [],
                'est': [],
                'fin': [],
                'fra': [],
                'fro': [],
                'glg': [],
                'deu_at': [],
                'deu_de': [],
                'gmh': [],
                'deu_ch': [],
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
                'kir': [],
                'lat': [],
                'lav': [],
                'lij': [],
                'lit': [],
                'ltz': [],
                'mkd': [],
                'msa': [],
                'mal': [],
                'mar': [],
                'omr': [],
                'mon': [],
                'nep': [],
                'non': [],
                'nob': [],
                'nno': [],
                'fas': [],
                'pol': [],
                'por_br': [],
                'por_pt': [],
                'pan': [],
                'ron': [],
                'rus': [],
                'san': [],
                'srp_cyrl': [],
                'srp_latn': [],
                'sin': [],
                'slk': [],
                'slv': [],
                'som': [],
                'sot': [],
                'spa': [],
                'swa': [],
                'swe': [],
                'tgl': [],
                'tgk': [],
                'tam': [],
                'tat': [],
                'tel': [],
                'tha': [],
                'tir': [],
                'tsn': [],
                'tur': [],
                'ukr': [],
                'urd': [],
                'vie': [],
                'yor': [],
                'zul': [],
                
                'other': []
            },

            'preview_lang': 'eng_us',
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

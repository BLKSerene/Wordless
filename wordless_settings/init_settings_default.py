#
# Wordless: Initialization of Default Settings
#
# Copyright (C) 2018-2019 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import os

from wordless_tagsets import *

def init_settings_default(main):
    main.settings_default = {
        'current_tab': main.tr('Overview'),

        'file': {
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
                'treat_as_lowercase': True,
                'lemmatize': False,
                'filter_stop_words': False,

                'nums': True,
                'puncs': False
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
                'puncs': False
            },
            
            'search_settings': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'ignore_case': True,
                'match_inflected_forms': True,
                'match_whole_word': True,
                'use_regex': False
            },

            'context_settings': {
                'inclusion': {
                    'inclusion': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'ignore_case': True,
                    'match_inflected_forms': True,
                    'match_whole_word': True,
                    'use_regex': False,
                    
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
                    'match_whole_word': True,
                    'use_regex': False,
                    
                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                }
            },
            
            'generation_settings': {
                'width_left_token': 10,
                'width_left_char': 50,
                'width_right_token': 10,
                'width_right_char': 50,
                'width_unit': main.tr('Token'),

                'number_lines': 100,
                'number_lines_no_limit': True,
                'every_nth_line': 2,
                'every_nth_line_no_limit': True
            },

            'table_settings': {
                'show_pct': True
            },

            'plot_settings': {
                'sort_results_by': main.tr('File')
            },

            'sorting_settings': {
                'sorting_rules': [
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
                'match_whole_word': True,
                'use_regex': False,
            }
        },
    
        'wordlist': {
            'token_settings': {
                'words': True,
                'lowercase': True,
                'uppercase': True,
                'title_case': True,
                'treat_as_lowercase': True,
                'lemmatize': False,
                'filter_stop_words': False,

                'nums': True,
                'puncs': False
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

            'plot_settings': {
                'plot_type': main.tr('Line Chart'),
                'use_file': main.tr('Total'),
                'use_data': main.tr('Frequency'),
                'use_pct': False,
                'use_cumulative': False,

                'rank_min': 1,
                'rank_min_no_limit': True,
                'rank_max': 50,
                'rank_max_no_limit': False,
            },

            'filter_settings': {
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

                'number_files_found_min': 1,
                'number_files_found_min_no_limit': True,
                'number_files_found_max': 100,
                'number_files_found_max_no_limit': True,

                'filter_file': main.tr('Total')
            },

            'search_results': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'ignore_case': True,
                'match_inflected_forms': True,
                'match_whole_word': True,
                'use_regex': False
            }
        },
    
        'ngrams': {
            'token_settings': {
                'words': True,
                'lowercase': True,
                'uppercase': True,
                'title_case': True,
                'treat_as_lowercase': True,
                'lemmatize': False,
                'filter_stop_words': False,

                'nums': True,
                'puncs': False
            },

            'search_settings': {
                'search_settings': True,

                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'ignore_case': True,
                'match_inflected_forms': True,
                'match_whole_word': True,
                'use_regex': False,

                'keyword_position_min': 1,
                'keyword_position_min_no_limit': True,
                'keyword_position_max': 2,
                'keyword_position_max_no_limit': True
            },

            'context_settings': {
                'inclusion': {
                    'inclusion': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'ignore_case': True,
                    'match_inflected_forms': True,
                    'match_whole_word': True,
                    'use_regex': False,
                    
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
                    'match_whole_word': True,
                    'use_regex': False,
                    
                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                }
            },
            
            'generation_settings': {
                'ngram_size_sync': False,
                'ngram_size_min': 2,
                'ngram_size_max': 2,
                'allow_skipped_tokens': 0,

                'measure_dispersion': main.tr('Juilland\'s D'),
                'measure_adjusted_freq': main.tr('Juilland\'s U')
            },

            'table_settings': {
                'show_pct': True,
                'show_cumulative': False,
                'show_breakdown': True
            },

            'plot_settings': {
                'plot_type': main.tr('Line Chart'),
                'use_file': main.tr('Total'),
                'use_data': main.tr('Frequency'),
                'use_pct': False,
                'use_cumulative': False,

                'rank_min': 1,
                'rank_min_no_limit': True,
                'rank_max': 50,
                'rank_max_no_limit': False,
            },

            'filter_settings': {
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

                'len_ngram_min': 1,
                'len_ngram_min_no_limit': True,
                'len_ngram_max': 20,
                'len_ngram_max_no_limit': True,

                'number_files_found_min': 1,
                'number_files_found_min_no_limit': True,
                'number_files_found_max': 100,
                'number_files_found_max_no_limit': True,

                'filter_file': main.tr('Total')
            },

            'search_results': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'ignore_case': True,
                'match_inflected_forms': True,
                'match_whole_word': True,
                'use_regex': False
            }
        },

        'collocation': {
            'token_settings': {
                'words': True,
                'lowercase': True,
                'uppercase': True,
                'title_case': True,
                'treat_as_lowercase': True,
                'lemmatize': False,
                'filter_stop_words': False,

                'nums': True,
                'puncs': False
            },
            
            'search_settings': {
                'search_settings': True,

                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'ignore_case': True,
                'match_inflected_forms': True,
                'match_whole_word': True,
                'use_regex': False
            },

            'context_settings': {
                'inclusion': {
                    'inclusion': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'ignore_case': True,
                    'match_inflected_forms': True,
                    'match_whole_word': True,
                    'use_regex': False,
                    
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
                    'match_whole_word': True,
                    'use_regex': False,
                    
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

            'plot_settings': {
                'plot_type': main.tr('Line Chart'),
                'use_file': main.tr('Total'),
                'use_data': main.tr('p-value'),
                'use_pct': False,
                'use_cumulative': False,

                'rank_min': 1,
                'rank_min_no_limit': True,
                'rank_max': 50,
                'rank_max_no_limit': False
            },

            'filter_settings': {
                'freq_filter_data': main.tr('Frequency'),
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

                'len_collocate_min': 1,
                'len_collocate_min_no_limit': True,
                'len_collocate_max': 20,
                'len_collocate_max_no_limit': True,

                'number_files_found_min': 1,
                'number_files_found_min_no_limit': True,
                'number_files_found_max': 100,
                'number_files_found_max_no_limit': True,

                'filter_file': main.tr('Total')
            },

            'search_results': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'ignore_case': True,
                'match_inflected_forms': True,
                'match_whole_word': True,
                'use_regex': False
            }
        },

        'colligation': {
            'token_settings': {
                'words': True,
                'lowercase': True,
                'uppercase': True,
                'title_case': True,
                'treat_as_lowercase': True,
                'lemmatize': False,
                'filter_stop_words': False,

                'nums': True,
                'puncs': False
            },

            'search_settings': {
                'search_settings': True,

                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'ignore_case': True,
                'match_inflected_forms': True,
                'match_whole_word': True,
                'use_regex': False
            },

            'context_settings': {
                'inclusion': {
                    'inclusion': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'ignore_case': True,
                    'match_inflected_forms': False,
                    'match_whole_word': True,
                    'use_regex': False,
                    
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
                    'match_whole_word': True,
                    'use_regex': False,
                    
                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                }
            },
            
            'generation_settings': {
                'node_type': main.tr('Token'),
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

            'plot_settings': {
                'plot_type': main.tr('Line Chart'),
                'use_file': main.tr('Total'),
                'use_data': main.tr('p-value'),
                'use_pct': False,
                'use_cumulative': False,

                'rank_min': 1,
                'rank_min_no_limit': True,
                'rank_max': 50,
                'rank_max_no_limit': False
            },

            'filter_settings': {
                'freq_filter_data': main.tr('Frequency'),
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

                'len_collocate_min': 1,
                'len_collocate_min_no_limit': True,
                'len_collocate_max': 20,
                'len_collocate_max_no_limit': True,

                'number_files_found_min': 1,
                'number_files_found_min_no_limit': True,
                'number_files_found_max': 100,
                'number_files_found_max_no_limit': True,

                'filter_file': main.tr('Total')
            },

            'search_results': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'ignore_case': True,
                'match_inflected_forms': True,
                'match_whole_word': True,
                'use_regex': False
            },
        },

        'keywords': {
            'token_settings': {
                'words': True,
                'lowercase': True,
                'uppercase': True,
                'title_case': True,
                'treat_as_lowercase': True,
                'lemmatize': False,
                'filter_stop_words': False,

                'nums': True,
                'puncs': False
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

            'plot_settings': {
                'plot_type': main.tr('Line Chart'),
                'use_file': main.tr('Total'),
                'use_data': main.tr('p-value'),
                'use_pct': False,
                'use_cumulative': False,

                'rank_min': 1,
                'rank_min_no_limit': True,
                'rank_max': 50,
                'rank_max_no_limit': False
            },

            'filter_settings': {
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

                'dispersion_min': -100,
                'dispersion_min_no_limit': True,
                'dispersion_max': 100,
                'dispersion_max_no_limit': True,

                'len_keyword_min': 1,
                'len_keyword_min_no_limit': True,
                'len_keyword_max': 20,
                'len_keyword_max_no_limit': True,

                'number_files_found_min': 1,
                'number_files_found_min_no_limit': True,
                'number_files_found_max': 100,
                'number_files_found_max_no_limit': True,

                'filter_file': main.tr('Total')
            },

            'search_results': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'ignore_case': True,
                'match_inflected_forms': True,
                'match_whole_word': True,
                'use_regex': False
            }
        },

        'general': {
            'font_monospace': 'Consolas',
            'style_highlight': 'border: 1px solid Red;'
        },

        'import': {
            'files': {
                'default_path': os.path.normpath(os.path.realpath('.'))
            },

            'search_terms': {
                'default_path': os.path.normpath(os.path.realpath('.')),
                'detect_encodings': True
            },

            'temp_files': {
                'default_path': os.path.normpath(os.path.realpath('Import/')),
                'default_encoding': 'utf_8'
            }
        },

        'export': {
            'tables': {
                'default_path': os.path.normpath(os.path.realpath('Export/')),
                'default_type': main.tr('Excel Workbook (*.xlsx)'),
                'default_encoding': 'utf_8'
            },

            'search_terms': {
                'default_path': os.path.normpath(os.path.realpath('Export/')),
                'default_encoding': 'utf_8'
            }
        },

        'data': {
            'precision_decimal': 2,
            'precision_pct': 2,
            'precision_p_value': 5
        },

        'lang_detection': {
            'detection_settings': {
                'detection_engine': 'langid.py',
                'number_lines': 100,
                'number_lines_no_limit': False
            },

            'default_settings': {
                'default_lang': 'eng'
            }
        },

        'encoding_detection': {
            'default_settings': {
                'default_encoding': 'utf_8'
            }
        },

        'sentence_tokenization': {
            'sentence_tokenizers': {
                'zho_cn': main.tr('Wordless - Chinese Sentence Tokenizer'),
                'zho_tw': main.tr('Wordless - Chinese Sentence Tokenizer'),
                'ces': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'dan': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'nld': main.tr('spaCy - Dutch Sentence Tokenizer'),
                'eng': main.tr('spaCy - English Sentence Tokenizer'),
                'est': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'fin': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'fra': main.tr('spaCy - French Sentence Tokenizer'),
                'deu': main.tr('spaCy - German Sentence Tokenizer'),
                'ell': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'ita': main.tr('spaCy - Italian Sentence Tokenizer'),
                'jpn': main.tr('Wordless - Japanese Sentence Tokenizer'),
                'nob': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'nno': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'pol': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'por': main.tr('spaCy - Portuguese Sentence Tokenizer'),
                'slv': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'spa': main.tr('spaCy - Spanish Sentence Tokenizer'),
                'swe': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'tha': main.tr('PyThaiNLP - Thai Sentence Tokenizer'),
                'tur': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'vie': main.tr('Underthesea - Vietnamese Sentence Tokenizer'),

                'other': main.tr('NLTK - Punkt Sentence Tokenizer')
            },

            'preview_lang': 'eng',
            'preview_samples': '',
            'preview_results': ''
        },

        'word_tokenization': {
            'word_tokenizers': {
                'ara': main.tr('spaCy - Arabic Word Tokenizer'),
                'ben': main.tr('spaCy - Bengali Word Tokenizer'),
                'cat': main.tr('SacreMoses - Moses Tokenizer'),
                'zho_cn': main.tr('jieba - Chinese Word Tokenizer'),
                'zho_tw': main.tr('jieba - Chinese Word Tokenizer'),
                'hrv': main.tr('spaCy - Croatian Word Tokenizer'),
                'ces': main.tr('NLTK - Tok-tok Tokenizer'),
                'dan': main.tr('spaCy - Danish Word Tokenizer'),
                'nld': main.tr('spaCy - Dutch Word Tokenizer'),
                'eng': main.tr('spaCy - English Word Tokenizer'),
                'fin': main.tr('SacreMoses - Moses Tokenizer'),
                'fra': main.tr('spaCy - French Word Tokenizer'),
                'deu': main.tr('spaCy - German Word Tokenizer'),
                'ell': main.tr('SacreMoses - Moses Tokenizer'),
                'heb': main.tr('spaCy - Hebrew Word Tokenizer'),
                'hin': main.tr('spaCy - Hindi Word Tokenizer'),
                'hun': main.tr('SacreMoses - Moses Tokenizer'),
                'isl': main.tr('SacreMoses - Moses Tokenizer'),
                'ind': main.tr('spaCy - Indonesian Word Tokenizer'),
                'gle': main.tr('spaCy - Irish Word Tokenizer'),
                'ita': main.tr('spaCy - Italian Word Tokenizer'),
                'jpn': main.tr('nagisa - Japanese Word Tokenizer'),
                'lav': main.tr('SacreMoses - Moses Tokenizer'),
                'nob': main.tr('spaCy - Norwegian Bokmål Word Tokenizer'),
                'fas': main.tr('NLTK - Tok-tok Tokenizer'),
                'pol': main.tr('SacreMoses - Moses Tokenizer'),
                'por': main.tr('spaCy - Portuguese Word Tokenizer'),
                'ron': main.tr('SacreMoses - Moses Tokenizer'),
                'rus': main.tr('NLTK - Tok-tok Tokenizer'),
                'sin': main.tr('spaCy - Sinhala Word Tokenizer'),
                'slk': main.tr('SacreMoses - Moses Tokenizer'),
                'slv': main.tr('SacreMoses - Moses Tokenizer'),
                'spa': main.tr('spaCy - Spanish Word Tokenizer'),
                'swe': main.tr('SacreMoses - Moses Tokenizer'),
                'tgk': main.tr('NLTK - Tok-tok Tokenizer'),
                'tam': main.tr('SacreMoses - Moses Tokenizer'),
                'tat': main.tr('spaCy - Tatar Word Tokenizer'),
                'tel': main.tr('spaCy - Telugu Word Tokenizer'),
                'tha': main.tr('PyThaiNLP - Maximum Matching Algorithm + TCC'),
                'bod': main.tr('pybo - Tibetan Word Tokenizer'),
                'tur': main.tr('spaCy - Turkish Word Tokenizer'),
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
                'cat': main.tr('SacreMoses - Moses Detokenizer'),
                'zho_cn': main.tr('Wordless - Chinese Word Detokenizer'),
                'zho_tw': main.tr('Wordless - Chinese Word Detokenizer'),
                'ces': main.tr('SacreMoses - Moses Detokenizer'),
                'nld': main.tr('SacreMoses - Moses Detokenizer'),
                'eng': main.tr('NLTK - Penn Treebank Detokenizer'),
                'fin': main.tr('SacreMoses - Moses Detokenizer'),
                'fra': main.tr('SacreMoses - Moses Detokenizer'),
                'deu': main.tr('SacreMoses - Moses Detokenizer'),
                'ell': main.tr('SacreMoses - Moses Detokenizer'),
                'hun': main.tr('SacreMoses - Moses Detokenizer'),
                'isl': main.tr('SacreMoses - Moses Detokenizer'),
                'jpn': main.tr('Wordless - Japanese Word Detokenizer'),
                'lav': main.tr('SacreMoses - Moses Detokenizer'),
                'pol': main.tr('SacreMoses - Moses Detokenizer'),
                'por': main.tr('SacreMoses - Moses Detokenizer'),
                'ron': main.tr('SacreMoses - Moses Detokenizer'),
                'rus': main.tr('SacreMoses - Moses Detokenizer'),
                'slk': main.tr('SacreMoses - Moses Detokenizer'),
                'slv': main.tr('SacreMoses - Moses Detokenizer'),
                'spa': main.tr('SacreMoses - Moses Detokenizer'),
                'swe': main.tr('SacreMoses - Moses Detokenizer'),
                'tam': main.tr('SacreMoses - Moses Detokenizer'),
                'tha': main.tr('Wordless - Thai Word Detokenizer'),

                'other': main.tr('NLTK - Penn Treebank Detokenizer')
            },

            'preview_lang': 'eng',
            'preview_samples': '',
            'preview_results': ''
        },

        'pos_tagging': {
            'pos_taggers': {
                'zho_cn': main.tr('jieba - Chinese POS Tagger'),
                'zho_tw':  main.tr('jieba - Chinese POS Tagger'),
                'nld': main.tr('spaCy - Dutch POS Tagger'),
                'eng': main.tr('spaCy - English POS Tagger'),
                'fra': main.tr('spaCy - French POS Tagger'),
                'deu': main.tr('spaCy - German POS Tagger'),
                'ita': main.tr('spaCy - Italian POS Tagger'),
                'jpn': main.tr('nagisa - Japanese POS Tagger'),
                'por': main.tr('spaCy - Portuguese POS Tagger'),
                'rus': main.tr('pymorphy2 - Morphological Analyzer'),
                'spa': main.tr('spaCy - Spanish POS Tagger'),
                'tha': main.tr('PyThaiNLP - Perceptron Tagger - ORCHID Corpus'),
                'bod': main.tr('pybo - Tibetan POS Tagger'),
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
            'preview_pos_tagger': main.tr('NLTK - Perceptron POS Tagger'),

            'mappings': {
                'zho_cn': {
                    main.tr('jieba - Chinese POS Tagger'): zho_jieba.mappings
                },

                'zho_tw': {
                    main.tr('jieba - Chinese POS Tagger'): zho_jieba.mappings
                },

                'nld': {
                    main.tr('spaCy - Dutch POS Tagger'): nld_spacy.mappings
                },
                
                'eng': {
                    main.tr('NLTK - Perceptron POS Tagger'): eng_penn_treebank.mappings,
                    main.tr('spaCy - English POS Tagger'): eng_penn_treebank_onto_notes_5.mappings
                },

                'fra': {
                    main.tr('spaCy - French POS Tagger'): fra_spacy.mappings
                },

                'deu': {
                    main.tr('spaCy - German POS Tagger'): deu_tiger_treebank.mappings
                },

                'ita': {
                    main.tr('spaCy - Italian POS Tagger'): ita_spacy.mappings
                },

                'jpn': {
                    main.tr('nagisa - Japanese POS Tagger'): jpn_unidic.mappings
                },

                'por': {
                    main.tr('spaCy - Portuguese POS Tagger'): por_spacy.mappings
                },

                'rus': {
                    main.tr('NLTK - Perceptron POS Tagger'): rus_russian_national_corpus.mappings,
                    main.tr('pymorphy2 - Morphological Analyzer'): rus_open_corpora.mappings
                },

                'spa': {
                    main.tr('spaCy - Spanish POS Tagger'): spa_spacy.mappings
                },

                'tha': {
                    main.tr('PyThaiNLP - Perceptron POS Tagger - ORCHID Corpus'): tha_orchid.mappings,
                    main.tr('PyThaiNLP - Perceptron POS Tagger - PUD Corpus'): all_universal.mappings
                },

                'bod': {
                    main.tr('pybo - Tibetan POS Tagger'): bod_pybo.mappings
                },

                'ukr': {
                    main.tr('pymorphy2 - Morphological Analyzer'): rus_open_corpora.mappings
                },

                'vie': {
                    main.tr('Underthesea - Vietnamese POS Tagger'): vie_underthesea.mappings
                }
            }
        },

        'lemmatization': {
            'lemmatizers': {
                'ast': main.tr('Lemmatization Lists'),
                'bul': main.tr('Lemmatization Lists'),
                'cat': main.tr('Lemmatization Lists'),
                'ces': main.tr('Lemmatization Lists'),
                'nld': main.tr('spaCy - Dutch Lemmatizer'),
                'eng': main.tr('spaCy - English Lemmatizer'),
                'est': main.tr('Lemmatization Lists'),
                'fra': main.tr('spaCy - French Lemmatizer'),
                'gla': main.tr('Lemmatization Lists'),
                'glg': main.tr('Lemmatization Lists'),
                'deu': main.tr('spaCy - German Lemmatizer'),
                'hun': main.tr('Lemmatization Lists'),
                'gle': main.tr('Lemmatization Lists'),
                'ita': main.tr('spaCy - Italian Lemmatizer'),
                'glv': main.tr('Lemmatization Lists'),
                'fas': main.tr('Lemmatization Lists'),
                'por': main.tr('spaCy - Portuguese Lemmatizer'),
                'ron': main.tr('Lemmatization Lists'),
                'rus': main.tr('pymorphy2 - Morphological Analyzer'),
                'slk': main.tr('Lemmatization Lists'),
                'slv': main.tr('Lemmatization Lists'),
                'spa': main.tr('spaCy - Spanish Lemmatizer'),
                'swe': main.tr('Lemmatization Lists'),
                'bod': main.tr('pybo - Tibetan Lemmatizer'),
                'ukr': main.tr('pymorphy2 - Morphological Analyzer'),
                'cym': main.tr('Lemmatization Lists')
            },

            'preview_lang': 'eng',
            'preview_samples': '',
            'preview_results': ''

        },

        'stop_words': {
            'stop_words': {
                'afr': 'Stopwords ISO',
                'ara': 'Stopwords ISO',
                'hye': 'Stopwords ISO',
                'aze': 'NLTK',
                'eus': 'Stopwords ISO',
                'ben': 'Stopwords ISO',
                'bre': 'Stopwords ISO',
                'bul': 'Stopwords ISO',
                'cat': 'Stopwords ISO',
                'zho_cn': 'Stopwords ISO',
                'zho_tw': 'Stopwords ISO',
                'hrv': 'Stopwords ISO',
                'ces': 'Stopwords ISO',
                'dan': 'Stopwords ISO',
                'nld': 'Stopwords ISO',
                'eng': 'Stopwords ISO',
                'epo': 'Stopwords ISO',
                'est': 'Stopwords ISO',
                'fin': 'Stopwords ISO',
                'fra': 'Stopwords ISO',
                'glg': 'Stopwords ISO',
                'deu': 'Stopwords ISO',
                'ell': 'Stopwords ISO',
                'hau': 'Stopwords ISO',
                'heb': 'Stopwords ISO',
                'hin': 'Stopwords ISO',
                'hun': 'Stopwords ISO',
                'ind': 'Stopwords ISO',
                'gle': 'Stopwords ISO',
                'ita': 'Stopwords ISO',
                'jpn': 'Stopwords ISO',
                'kaz': 'NLTK',
                'kor': 'Stopwords ISO',
                'kur': 'Stopwords ISO',
                'lat': 'Stopwords ISO',
                'lav': 'Stopwords ISO',
                'mar': 'Stopwords ISO',
                'msa': 'Stopwords ISO',
                'nep': 'NLTK',
                'nob': 'Stopwords ISO',
                'nno': 'Stopwords ISO',
                'fas': 'Stopwords ISO',
                'pol': 'Stopwords ISO',
                'por': 'Stopwords ISO',
                'ron': 'Stopwords ISO',
                'rus': 'Stopwords ISO',
                'sin': 'spaCy',
                'slk': 'Stopwords ISO',
                'slv': 'Stopwords ISO',
                'sot': 'Stopwords ISO',
                'som': 'Stopwords ISO',
                'spa': 'Stopwords ISO',
                'swa': 'Stopwords ISO',
                'swe': 'Stopwords ISO',
                'tgl': 'Stopwords ISO',
                'tat': 'spaCy',
                'tel': 'spaCy',
                'tha': 'PyThaiNLP',
                'tur': 'Stopwords ISO',
                'ukr': 'Stopwords ISO',
                'urd': 'Stopwords ISO',
                'vie': 'Stopwords ISO',
                'yor': 'Stopwords ISO',
                'zul': 'Stopwords ISO'
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

                'students_t_test_two_sample': {
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
                    'smoothing_parameter': 1.00
                }
            }
        }
    }

#
# Wordless: Initialization of Default Settings
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import os

def init_settings_default(main):
    main.settings_default = {
        'current_tab': main.tr('Overview'),

        'file': {
            'files_open': [],
            'files_closed': [],

            'subfolders': True,

            'detect_langs': True,
            'detect_encodings': True
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
                'inclusion': True,

                'inclusion_multi_search_mode': False,
                'inclusion_search_term': '',
                'inclusion_search_terms': [],

                'inclusion_ignore_case': True,
                'inclusion_match_inflected_forms': True,
                'inclusion_match_whole_word': True,
                'inclusion_use_regex': False,
                
                'inclusion_context_window_sync': False,
                'inclusion_context_window_left': -5,
                'inclusion_context_window_right': 5,

                'exclusion': True,

                'exclusion_multi_search_mode': False,
                'exclusion_search_term': '',
                'exclusion_search_terms': [],

                'exclusion_ignore_case': True,
                'exclusion_match_inflected_forms': True,
                'exclusion_match_whole_word': True,
                'exclusion_use_regex': False,
                
                'exclusion_context_window_sync': False,
                'exclusion_context_window_left': -5,
                'exclusion_context_window_right': 5
            },
            
            'generation_settings': {
                'width_left_token': 10,
                'width_left_char': 50,
                'width_right_token': 10,
                'width_right_char': 50,
                'width_unit': main.tr('Token'),
                
                'number_lines_no_limit': True,
                'number_lines': 25
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
                'inclusion': True,

                'inclusion_multi_search_mode': False,
                'inclusion_search_term': '',
                'inclusion_search_terms': [],

                'inclusion_ignore_case': True,
                'inclusion_match_inflected_forms': True,
                'inclusion_match_whole_word': True,
                'inclusion_use_regex': False,
                
                'inclusion_context_window_sync': False,
                'inclusion_context_window_left': -5,
                'inclusion_context_window_right': 5,

                'exclusion': True,

                'exclusion_multi_search_mode': False,
                'exclusion_search_term': '',
                'exclusion_search_terms': [],

                'exclusion_ignore_case': True,
                'exclusion_match_inflected_forms': True,
                'exclusion_match_whole_word': True,
                'exclusion_use_regex': False,
                
                'exclusion_context_window_sync': False,
                'exclusion_context_window_left': -5,
                'exclusion_context_window_right': 5
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
                'inclusion': True,

                'inclusion_multi_search_mode': False,
                'inclusion_search_term': '',
                'inclusion_search_terms': [],

                'inclusion_ignore_case': True,
                'inclusion_match_inflected_forms': True,
                'inclusion_match_whole_word': True,
                'inclusion_use_regex': False,
                
                'inclusion_context_window_sync': False,
                'inclusion_context_window_left': -5,
                'inclusion_context_window_right': 5,

                'exclusion': True,

                'exclusion_multi_search_mode': False,
                'exclusion_search_term': '',
                'exclusion_search_terms': [],

                'exclusion_ignore_case': True,
                'exclusion_match_inflected_forms': True,
                'exclusion_match_whole_word': True,
                'exclusion_use_regex': False,
                
                'exclusion_context_window_sync': False,
                'exclusion_context_window_left': -5,
                'exclusion_context_window_right': 5
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
                'freq_filter_data': main.tr('Total'),
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
            'search_results': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'ignore_case': True,
                'match_inflected_forms': True,
                'match_whole_word': True,
                'use_regex': False
            },

            'treat_as_lowercase': True,
            'lemmatize': False,

            'puncs': False,
            
            'search_settings': True,

            'multi_search_mode': False,
            'search_term': '',
            'search_terms': [],

            'ignore_case': True,
            'match_inflected_forms': True,
            'match_whole_word': True,
            'use_regex': False,

            'keyword_type': main.tr('Token'),
            'window_sync': False,
            'window_left': -5,
            'window_right': 5,
            'assoc_measure': main.tr('Pearson\'s Chi-squared Test'),

            'show_pct': True,
            'show_cumulative': False,
            'show_breakdown_position': True,
            'show_breakdown_file': True,

            'plot_type': main.tr('Line Chart'),
            'use_data_file': main.tr('Total'),
            'use_data_col': main.tr('Score (Right)'),
            'use_pct': False,
            'use_cumulative': False,

            'rank_no_limit': False,
            'rank_min': 1,
            'rank_max': 50,

            'filter_file': main.tr('Total'),

            'freq_left_no_limit': True,
            'freq_left_min': 0,
            'freq_left_max': 1000,
            'freq_right_no_limit': True,
            'freq_right_min': 0,
            'freq_right_max': 1000,

            'score_left_no_limit': True,
            'score_left_min': 0,
            'score_left_max': 100,
            'score_right_no_limit': True,
            'score_right_min': 0,
            'score_right_max': 100,

            'files_no_limit': True,
            'files_min': 1,
            'files_max': 100
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
            'file_default_path': os.path.realpath('.'),
            'file_default_lang': 'eng',
            'file_default_encoding': main.tr('All Languages (UTF-8 Without BOM)'),

            'precision_decimal': 2,
            'precision_pct': 2,
            'precision_p_value': 5,

            'font_monospace': 'Consolas',

            'style_highlight': 'border: 1px solid Red;'
        },

        'import': {
            'search_terms_default_path': os.path.realpath('.'),
            'search_terms_default_encoding': main.tr('All Languages (UTF-8 Without BOM)'),
        },

        'export': {
            'tables_default_path': os.path.realpath('./export/'),
            'tables_default_type': main.tr('Excel Workbook (*.xlsx)'),
            'tables_default_encoding': main.tr('All Languages (UTF-8 Without BOM)'),

            'search_terms_default_path': os.path.realpath('./export/'),
            'search_terms_default_encoding': main.tr('All Languages (UTF-8 Without BOM)'),
        },

        'sentence_tokenization': {
            'sentence_tokenizers': {
                'zho_CN': main.tr('Wordless - Chinese Sentence Tokenizer'),
                'zho_TW': main.tr('Wordless - Chinese Sentence Tokenizer'),
                'ces': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'dan': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'nld': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'eng': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'est': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'fin': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'fra': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'deu': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'ell': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'ita': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'nor': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'pol': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'por': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'slv': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'spa': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'swe': main.tr('NLTK - Punkt Sentence Tokenizer'),
                'tur': main.tr('NLTK - Punkt Sentence Tokenizer'),

                'other': main.tr('NLTK - Punkt Sentence Tokenizer'),
            },

            'preview_lang': 'eng',
            'preview_samples': ''
        },

        'word_tokenization': {
            'word_tokenizers': {
                'zho_CN': main.tr('jieba - With HMM'),
                'zho_TW': main.tr('jieba - With HMM'),
                'ces': main.tr('NLTK - Treebank Tokenizer'),
                'dan': main.tr('NLTK - Treebank Tokenizer'),
                'nld': main.tr('NLTK - Treebank Tokenizer'),
                'eng': main.tr('NLTK - Treebank Tokenizer'),
                'est': main.tr('NLTK - Treebank Tokenizer'),
                'fin': main.tr('NLTK - Treebank Tokenizer'),
                'fra': main.tr('NLTK - Treebank Tokenizer'),
                'deu': main.tr('NLTK - Treebank Tokenizer'),
                'ell': main.tr('NLTK - Treebank Tokenizer'),
                'ita': main.tr('NLTK - Treebank Tokenizer'),
                'nor': main.tr('NLTK - Treebank Tokenizer'),
                'pol': main.tr('NLTK - Treebank Tokenizer'),
                'por': main.tr('NLTK - Treebank Tokenizer'),
                'slv': main.tr('NLTK - Treebank Tokenizer'),
                'spa': main.tr('NLTK - Treebank Tokenizer'),
                'swe': main.tr('NLTK - Treebank Tokenizer'),
                'tur': main.tr('NLTK - Treebank Tokenizer'),

                'other': main.tr('NLTK - Treebank Tokenizer')
            },

            'preview_lang': 'eng',
            'preview_samples': ''
        },

        'word_detokenization': {
            'word_detokenizers': {
                'zho_CN': main.tr('Wordless - Chinese Word Detokenizer'),
                'zho_TW': main.tr('Wordless - Chinese Word Detokenizer'),
                'eng': main.tr('NLTK - Moses Detokenizer'),

                'other': main.tr('NLTK - Moses Detokenizer')
            },

            'preview_lang': 'eng',
            'preview_samples': ''
        },

        'pos_tagging': {
            'pos_taggers': {
                'zho_CN': main.tr('jieba'),
                'zho_TW':  main.tr('jieba'),
                'eng': main.tr('NLTK - Perceptron POS Tagger'),
                'rus': main.tr('NLTK - Perceptron POS Tagger')
            },

            'tagsets': {
                'zho_CN': 'jieba',
                'zho_TW': 'jieba',
                'eng': 'Penn Treebank',
                'rus': 'Russian National Corpus'
            },

            'preview_lang': 'eng',
            'preview_samples': ''
        },

        'lemmatization': {
            'lemmatizers': {
                'ast': 'Lemmatization Lists',
                'bul': 'Lemmatization Lists',
                'cat': 'Lemmatization Lists',
                'ces': 'Lemmatization Lists',
                'eng': 'NLTK',
                'est': 'Lemmatization Lists',
                'fra': 'Lemmatization Lists',
                'gla': 'Lemmatization Lists',
                'glg': 'Lemmatization Lists',
                'deu': 'Lemmatization Lists',
                'hun': 'Lemmatization Lists',
                'gle': 'Lemmatization Lists',
                'ita': 'Lemmatization Lists',
                'glv': 'Lemmatization Lists',
                'fas': 'Lemmatization Lists',
                'por': 'Lemmatization Lists',
                'ron': 'Lemmatization Lists',
                'slk': 'Lemmatization Lists',
                'slv': 'Lemmatization Lists',
                'spa': 'Lemmatization Lists',
                'swe': 'Lemmatization Lists',
                'ukr': 'Lemmatization Lists',
                'cym': 'Lemmatization Lists'
            },

            'preview_lang': 'eng',
            'preview_samples': '',

        },

        'stop_words': {
            'stop_words': {
                'afr': 'Stopwords ISO',
                'ara': 'NLTK',
                'hye': 'Stopwords ISO',
                'aze': 'NLTK',
                'eus': 'Stopwords ISO',
                'ben': 'Stopwords ISO',
                'bre': 'Stopwords ISO',
                'bul': 'Stopwords ISO',
                'cat': 'Stopwords ISO',
                'zho_CN': 'HanLP',
                'zho_TW': 'HanLP',
                'hrv': 'Stopwords ISO',
                'ces': 'Stopwords ISO',
                'dan': 'NLTK',
                'nld': 'NLTK',
                'eng': 'NLTK',
                'epo': 'Stopwords ISO',
                'est': 'Stopwords ISO',
                'fin': 'NLTK',
                'fra': 'NLTK',
                'glg': 'Stopwords ISO',
                'deu': 'NLTK',
                'ell': 'NLTK',
                'hau': 'Stopwords ISO',
                'heb': 'Stopwords ISO',
                'hin': 'Stopwords ISO',
                'hun': 'NLTK',
                'ind': 'NLTK',
                'gle': 'Stopwords ISO',
                'ita': 'NLTK',
                'jpn': 'Stopwords ISO',
                'kaz': 'NLTK',
                'kor': 'Stopwords ISO',
                'kur': 'Stopwords ISO',
                'lat': 'Stopwords ISO',
                'lav': 'Stopwords ISO',
                'mar': 'Stopwords ISO',
                'msa': 'Stopwords ISO',
                'nep': 'NLTK',
                'nor': 'NLTK',
                'fas': 'Stopwords ISO',
                'pol': 'Stopwords ISO',
                'por': 'NLTK',
                'ron': 'NLTK',
                'rus': 'NLTK',
                'slk': 'Stopwords ISO',
                'slv': 'Stopwords ISO',
                'sot': 'Stopwords ISO',
                'som': 'Stopwords ISO',
                'spa': 'NLTK',
                'swa': 'Stopwords ISO',
                'swe': 'NLTK',
                'tgl': 'Stopwords ISO',
                'tha': 'Stopwords ISO',
                'tur': 'NLTK',
                'ukr': 'Stopwords ISO',
                'urd': 'Stopwords ISO',
                'vie': 'Stopwords ISO',
                'yor': 'Stopwords ISO',
                'zul': 'Stopwords ISO',
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

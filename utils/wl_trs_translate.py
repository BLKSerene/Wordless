# ----------------------------------------------------------------------
# Utilities: Translations - Translate
# Copyright (C) 2018-2022  Ye Lei (叶磊)
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

import re

import bs4

import wl_trs_utils

# eng_us: [zho_cn]
TRS_LANGS = {
    'Afrikaans': ['南非语'],
    'Albanian': ['阿尔巴尼亚语'],
    'Amharic': ['阿姆哈拉语'],
    'Arabic': ['阿拉伯语'],
    'Armenian': ['亚美尼亚语'],
    'Assamese': ['阿萨姆语'],
    'Asturian': ['阿斯图里亚斯语'],
    'Azerbaijani': ['阿塞拜疆语'],
    'Basque': ['巴斯克语'],
    'Belarusian': ['白俄罗斯语'],
    'Bengali': ['孟加拉语'],
    'Breton': ['布列塔尼语'],
    'Bulgarian': ['保加利亚语'],
    'Catalan': ['加泰罗尼亚语'],
    'Chinese (Simplified)': ['汉语（简体）'],
    'Chinese (Traditional)': ['汉语（繁体）'],
    'Croatian': ['克罗地亚语'],
    'Czech': ['捷克语'],
    'Danish': ['丹麦语'],
    'Dutch': ['荷兰语'],
    'English (United Kingdom)': ['英语（英国）'],
    'English (United States)': ['英语（美国）'],
    'Esperanto': ['世界语'],
    'Estonian': ['爱沙尼亚语'],
    'Finnish': ['芬兰语'],
    'French': ['法语'],
    'Galician': ['加里西亚语'],
    'German (Austria)': ['德语（奥地利）'],
    'German (Germany)': ['德语（德国）'],
    'German (Switzerland)': ['德语（瑞士）'],
    'Greek (Ancient)': ['希腊语（古）'],
    'Greek (Modern)': ['希腊语（现代）'],
    'Gujarati': ['古吉拉特语'],
    'Hausa': ['豪萨语'],
    'Hebrew': ['希伯来语'],
    'Hindi': ['印地语'],
    'Hungarian': ['匈牙利语'],
    'Icelandic': ['冰岛语'],
    'Indonesian': ['印度尼西亚语'],
    'Irish': ['爱尔兰语'],
    'Italian': ['意大利语'],
    'Japanese': ['日语'],
    'Kannada': ['卡纳达语'],
    'Kazakh': ['哈萨克语'],
    'Korean': ['韩语'],
    'Kurdish': ['库尔德语'],
    'Kyrgyz': ['吉尔吉斯语'],
    # 'Latin' contained in 'Serbian (Latin)'
    'Serbian (Latin)': ['塞尔维亚语（拉丁）'],
    'Latin': ['拉丁语'],
    'Latvian': ['拉脱维亚语'],
    'Ligurian': ['利古里亚语'],
    'Lithuanian': ['立陶宛语'],
    'Luxembourgish': ['卢森堡语'],
    'Macedonian': ['马其顿语'],
    # 'Malay' contained in 'Malayalam'
    'Malayalam': ['马拉雅拉姆语'],
    'Malay': ['马来语'],
    'Manx': ['马恩语'],
    'Marathi': ['马拉地语'],
    'Meitei': ['曼尼普尔语'],
    'Mongolian': ['蒙古语'],
    'Nepali': ['尼泊尔语'],
    'Norwegian Bokmål': ['书面挪威语'],
    'Norwegian Nynorsk': ['新挪威语'],
    'Oriya': ['奥里亚语'],
    'Persian': ['波斯语'],
    'Polish': ['波兰语'],
    'Portuguese (Brazil)': ['葡萄牙语（巴西）'],
    'Portuguese (Portugal)': ['葡萄牙语（葡萄牙）'],
    'Punjabi': ['旁遮普语'],
    'Romanian': ['罗马尼亚语'],
    'Russian': ['俄语'],
    'Sanskrit': ['梵语'],
    'Scottish Gaelic': ['苏格兰盖尔语'],
    'Serbian (Cyrillic)': ['塞尔维亚语（西里尔）'],
    'Sinhala': ['僧伽罗语'],
    'Slovak': ['斯洛伐克语'],
    'Slovenian': ['斯洛文尼亚语'],
    'Somali': ['索马里语'],
    'Sorbian (Lower)': ['索布语（下）'],
    'Sorbian (Upper)': ['索布语（上）'],
    'Sotho (Southern)': ['塞索托语'],
    'Spanish': ['西班牙语'],
    'Swahili': ['斯瓦西里语'],
    'Swedish': ['瑞典语'],
    'Tagalog': ['他加禄语'],
    'Tajik': ['塔吉克语'],
    'Tamil': ['泰米尔语'],
    'Tatar': ['鞑靼语'],
    'Telugu': ['泰卢固语'],
    'Tetun Dili': ['帝力德顿语'],
    'Thai': ['泰语'],
    'Tibetan': ['藏语'],
    'Tigrinya': ['提格雷尼亚语'],
    'Tswana': ['茨瓦纳语'],
    'Turkish': ['土耳其语'],
    'Ukrainian': ['乌克兰语'],
    'Urdu': ['乌尔都语'],
    'Vietnamese': ['越南语'],
    'Welsh': ['威尔士语'],
    'Yoruba': ['约鲁巴语'],
    'Zulu': ['祖鲁语'],

    'Other Languages': ['其他语种'],

    # Encodings
    'All Languages': ['所有语种'],
    'Baltic Languages': ['波罗的海诸语'],
    'Celtic Languages': ['凯尔特语'],
    'Chinese': ['汉语'],
    'Cyrillic': ['西里尔'],
    'English': ['英语'],
    # 'European' contained in 'European (Central)', 'European (Northern), etc.
    'European (Central)': ['欧洲（中部）'],
    'European (Northern)': ['欧洲（北部）'],
    'European (Southern)': ['欧洲（南部）'],
    'European (South-Eastern)': ['欧洲（东南部）'],
    'European (Western)': ['欧洲（西部）'],
    'European': ['欧洲'],
    'German': ['德语'],
    'Greek': ['希腊语'],
    'Nordic Languages': ['北欧诸语'],
    'Portuguese': ['葡萄牙语'],

    # NLP utils
    'Norwegian': ['挪威语'],
    'Serbian': ['塞尔维亚语'],
}
TRS_ENCODINGS = {
    # 'with/without BOM' & contained in 'BE/LE with/without BOM'
    'BE with BOM': [' 大端带签名'],
    'BE without BOM': [' 大端无签名'],
    'LE with BOM': [' 小端带签名'],
    'LE without BOM': [' 小端无签名'],
    'with BOM': ['带签名'],
    'without BOM': ['无签名'],
}
TRS_FILE_TYPES = {
    'CSV File (*.csv)': ['CSV 文件 (*.csv)'],
    'Excel Workbook (*.xlsx)': ['Excel 工作簿 (*.xlsx)'],
    'HTML Page (*.htm; *.html)': ['HTML 页面 (*.htm; *.html)'],
    'PDF File (*.pdf)': ['PDF 文件 (*.pdf)'],
    'Text File (*.txt)': ['文本文件 (*.txt)'],
    'Translation Memory File (*.tmx)': ['翻译记忆库文件 (*.tmx)'],
    'Word Document (*.docx)': ['Word 文档 (*.docx)'],
    'XML File (*.xml)': ['XML 文件 (*.xml)'],
    'All Files (*.*)': ['所有文件 (*.*)']
}
TRS_NLP_UTILS = {
    # Settings
    'Sentence Tokenizer Settings': ['分句器设置'],
    'Sentence Tokenizers': ['分句器'],
    'Word Tokenizer Settings': ['分词器设置'],
    'Word Tokenizers': ['分词器'],
    'Syllable Tokenizer Settings': ['分音节器设置'],
    'Syllable Tokenizers': ['分音节器'],
    'Part-of-speech Tagger Settings': ['词性标注器设置'],
    'Part-of-speech Taggers': ['词性标注器'],
    'Lemmatizer Settings': ['词形还原器设置'],
    'Lemmatizers': ['词形还原器'],
    'Stop Word List Settings': ['停用词表设置'],
    'Stop Word Lists': ['停用词表'],

    'Sentence Tokenizer': ['分句器'],
    'Sentence Recognizer': ['句子识别器'],
    'Sentencizer': ['分句器'],

    # 'Tokenizer' contained in 'Word Tokenizer', 'Syllable Tokenizer', and others
    'Legality Syllable Tokenizer': ['合法性分音节器'],
    'Sonority Sequencing Syllable Tokenizer': ['响度顺序分音节器'],
    'Syllable Tokenizer': ['分音节器'],

    # 'Word Tokenizer' contained in 'Word Tokenizer (Split Mode'
    'Word Tokenizer (Split Mode': ['分词器（切分模式'],
    'Word Tokenizer': ['分词器'],
    'Penn Treebank Tokenizer': ['宾州树库分词器'],
    'Twitter Tokenizer': ['推特分词器'],
    'Regular-Expression Tokenizer': ['正则表达式分词器'],
    'Character Tokenizer': ['分字器'],
    'Kanji Tokenizer': ['分字器'],
    'Tokenizer': ['分词器'],
    'Longest Matching': ['最长匹配'],
    'Maximum Matching': ['最大匹配'],

    # 'Part-of-speech Tagger' contained in 'Perceptron Part-of-speech Tagger'
    'Perceptron Part-of-speech Tagger': ['感知机词性标注器'],
    'Part-of-speech Tagger': ['词性标注器'],
    'Morphological Analyzer': ['形态分析器'],

    'Lemmatizer': ['词形还原器'],
    'Lemma List': ['词根表'],
    'Custom List': ['自定义列表'],

    'Stop Word List': ['停用词表']
}
TRS_MISC = {
    # Lists
    'Add': ['添加'],
    'Insert': ['插入'],
    'Remove': ['移除'],
    'Clear': ['清空'],
    'Import': ['导入'],
    'Export': ['导出'],

    # Dialogs
    'Yes': ['是'],
    'No': ['否'],
    'OK': ['确认'],
    'Apply': ['应用'],
    'Save': ['保存'],
    'Open': ['打开'],
    'Cancel': ['取消'],
    'Close': ['关闭'],

    # Statistics
    'None': ['无'],
    'L': ['左'],
    'R': ['右'],
    'Sync': ['同步'],
    'From': ['从'],
    'To': ['至'],
    'No Limit': ['无限制'],
    'Two-tailed': ['双尾'],
    'Left-tailed': ['左尾'],
    'Right-tailed': ['右尾'],

    # File Area
    'Name': ['名称'],
    'Path': ['路径'],
    'Encoding': ['编码'],
    'Language': ['语种'],

    # Work Area
    'Total': ['合计'],

    'Generate Table': ['生成表格'],
    'Generate Figure': ['生成图表'],
    'Clear Table': ['清空表格'],

    'Token Settings': ['形符设置'],
    'Search Settings': ['搜索设置'],
    'Context Settings': ['上下文设置'],
    'Generation Settings': ['生成设置'],
    'Table Settings': ['表格设置'],
    'Figure Settings': ['图表设置'],

    # Misc
    '''
                <hr>
                <div style="text-align: center;">
                    Copyright (C) 2018-2022&nbsp;&nbsp;Ye Lei (<span style="font-family: simsun">叶磊</span>)<br>
                    Licensed Under GNU GPLv3<br>
                    All Other Rights Reserved
                </div>
            ''': [
        '''
                <hr>
                <div style="text-align: center;">
                    版权所有（C）2018-2022&nbsp;&nbsp;<span style="font-family: simsun">叶磊</span><br>
                    遵循 GNU GPLv3 协议<br>
                    保留其他所有权利
                </div>
            '''
    ],

    # Language-specific files
    'ACKNOWLEDGMENTS.md': ['ACKNOWLEDGMENTS_zho_cn.md']
}

with open('../trs/zho_cn.ts', 'r', encoding = 'utf_8') as f:
    soup = bs4.BeautifulSoup(f.read(), features = 'lxml')

for element_context in soup.select('context'):
    for element_message in element_context.select('message'):
        tr_hit = False

        element_src = element_message.select_one('source')
        element_tr = element_message.select_one('translation')

        # Do not re-translate obsolete translations
        if (
            'type' not in element_tr.attrs
            or ('type' in element_tr.attrs and element_tr['type'] != 'obsolete')
        ):
            tr = element_src.text

            # Languages
            for lang, trs in TRS_LANGS.items():
                if lang in tr:
                    tr = tr.replace(lang, trs[0])
                    # Excludes cases such as Mac OS Romanian in encodings
                    tr = tr.replace(f'(Mac OS {trs[0]})', f'(Mac OS {lang})')
                    # Excludes cases such as PyThaiNLP in third-party NLP libraries
                    tr = tr.replace('Py泰语NLP', 'PyThaiNLP')

                    tr_hit = True

                    break

            # Encodings
            for encoding, trs in TRS_ENCODINGS.items():
                if encoding in tr:
                    tr = tr.replace(encoding, trs[0])

                    tr_hit = True

                    break

            # File types
            for file_type, trs in TRS_FILE_TYPES.items():
                if tr == file_type:
                    tr = trs[0]

                    tr_hit = True

                    break

            # NLP utils
            for util, trs in TRS_NLP_UTILS.items():
                if util in tr:
                    tr = tr.replace(util, trs[0])

                    tr_hit = True

                    break

            # Misc
            for item, trs in TRS_MISC.items():
                if tr == item:
                    tr = trs[0]

                    tr_hit = True

                    break

            if tr_hit:
                # Do not replace parentheses in file type filters
                if element_src.text not in TRS_FILE_TYPES:
                    # Parentheses
                    tr = re.sub(r'\s*\(', r'（', tr)
                    tr = re.sub(r'\)\s*', r'）', tr)
                    # Remove whitespace between Chinese characters
                    tr = re.sub(r'(?<=[\u4E00-\u9FFF（）])\s+(?=[\u4E00-\u9FFF（）])', '', tr)

                element_message.select_one('translation').string = tr
                element_message.select_one('translation').attrs = {}

                print(f'Auto-translated "{element_src.text}" into "{tr}".')

with open('../trs/zho_cn.ts', 'w', encoding = 'utf_8') as f:
    f.write(str(soup))

# Release
wl_trs_utils.del_obsolete_trans('../trs/zho_cn.ts')
wl_trs_utils.release_trs()

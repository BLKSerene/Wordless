# ----------------------------------------------------------------------
# Utilities: Translations - Translate
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

import re

import bs4

from utils import wl_trs_utils

# eng_us: [zho_cn]
TRS_LANGS = {
    ' (Cyrillic script)': [' (西里尔文)'],
    ' (Gurmukhi script)': [' (古木基文)'],
    ' (Latin script)': [' (拉丁文)'],
    ' (Meitei script)': [' (曼尼普尔文)'],

    'Afrikaans': ['南非语'],
    'Albanian': ['阿尔巴尼亚语'],
    'Amharic': ['阿姆哈拉语'],
    'Arabic': ['阿拉伯语'],
    'Armenian (Classical)': ['亚美尼亚语（古）'],
    'Armenian (Eastern)': ['亚美尼亚语（东）'],
    'Armenian (Western)': ['亚美尼亚语（西）'],
    'Assamese': ['阿萨姆语'],
    'Asturian': ['阿斯图里亚斯语'],
    'Azerbaijani': ['阿塞拜疆语'],
    'Basque': ['巴斯克语'],
    'Belarusian': ['白俄罗斯语'],
    'Bengali': ['孟加拉语'],
    'Bulgarian': ['保加利亚语'],
    'Burmese': ['缅甸语'],
    'Buryat (Russia)': ['布里亚特语（俄罗斯）'],
    'Catalan': ['加泰罗尼亚语'],
    'Chinese (Classical)': ['汉语（文言）'],
    'Chinese (Simplified)': ['汉语（简体）'],
    'Chinese (Traditional)': ['汉语（繁体）'],
    'Church Slavonic (Old)': ['教会斯拉夫语（古）'],
    'Coptic': ['科普特语'],

    # In names of some language utils (eg. simplemma)
    'Serbo-Croatian': ['塞尔维亚-克罗地亚语'],
    'Croatian': ['克罗地亚语'],

    'Czech': ['捷克语'],
    'Danish': ['丹麦语'],
    'Dutch': ['荷兰语'],
    'English (Middle)': ['英语（中古）'],
    'English (Old)': ['英语（古）'],
    'English (United Kingdom)': ['英语（英国）'],
    'English (United States)': ['英语（美国）'],
    'Erzya': ['埃尔齐亚语'],
    'Esperanto': ['世界语'],
    'Estonian': ['爱沙尼亚语'],
    'Faroese': ['法罗语'],
    'Filipino': ['菲律宾语'],
    'Finnish': ['芬兰语'],

    'French (Old)': ['法语（古）'],
    'French': ['法语'],

    'Galician': ['加里西亚语'],
    'Georgian': ['格鲁吉亚语'],
    'German (Austria)': ['德语（奥地利）'],
    'German (Germany)': ['德语（德国）'],
    'German (Switzerland)': ['德语（瑞士）'],
    'Gothic': ['哥特语'],
    'Greek (Ancient)': ['希腊语（古）'],
    'Greek (Modern)': ['希腊语（现代）'],
    'Gujarati': ['古吉拉特语'],
    'Hebrew (Ancient)': ['希伯来语（古）'],
    'Hebrew (Modern)': ['希伯来语（现代）'],
    'Hindi': ['印地语'],
    'Hungarian': ['匈牙利语'],
    'Icelandic': ['冰岛语'],
    'Indonesian': ['印度尼西亚语'],
    'Irish': ['爱尔兰语'],
    'Italian': ['意大利语'],
    'Japanese': ['日语'],
    'Kannada': ['卡纳达语'],
    'Kazakh': ['哈萨克语'],
    'Khmer': ['柬埔寨语'],
    'Korean': ['韩语'],
    'Kurdish (Kurmanji)': ['库尔德语（库尔曼吉语）'],
    'Kyrgyz': ['吉尔吉斯语'],
    'Lao': ['老挝语'],
    'Latin': ['拉丁语'],
    'Latvian': ['拉脱维亚语'],
    'Ligurian': ['利古里亚语'],
    'Lithuanian': ['立陶宛语'],
    'Luganda': ['卢干达语'],
    'Luxembourgish': ['卢森堡语'],
    'Macedonian': ['马其顿语'],
    'Malayalam': ['马拉雅拉姆语'],
    'Malay': ['马来语'],
    'Maltese': ['马耳他语'],
    'Manx': ['马恩语'],
    'Marathi': ['马拉地语'],
    'Meitei': ['曼尼普尔语'],
    'Mongolian': ['蒙古语'],
    'Nepali': ['尼泊尔语'],
    'Nigerian Pidgin': ['尼日利亚皮钦语'],
    'Norwegian (Bokmål)': ['挪威语（书面）'],
    'Norwegian (Nynorsk)': ['挪威语（新）'],
    'Odia': ['奥里亚语'],
    'Persian': ['波斯语'],
    'Polish': ['波兰语'],
    'Pomak': ['波马克语'],
    'Portuguese (Brazil)': ['葡萄牙语（巴西）'],
    'Portuguese (Portugal)': ['葡萄牙语（葡萄牙）'],
    'Punjabi': ['旁遮普语'],
    'Romanian': ['罗马尼亚语'],

    'Russian (Old)': ['俄语（古）'],
    'Russian': ['俄语'],

    'Sámi (Northern)': ['萨米语（北）'],
    'Sanskrit': ['梵语'],
    'Scottish Gaelic': ['苏格兰盖尔语'],
    'Serbian': ['塞尔维亚语'],
    'Sindhi': ['信德语'],
    'Sinhala': ['僧伽罗语'],
    'Slovak': ['斯洛伐克语'],
    'Slovene': ['斯洛文尼亚语'],
    'Sorbian (Lower)': ['索布语（下）'],
    'Sorbian (Upper)': ['索布语（上）'],
    'Spanish': ['西班牙语'],
    'Swahili': ['斯瓦西里语'],
    'Swedish': ['瑞典语'],
    'Tagalog': ['他加禄语'],
    'Tajik': ['塔吉克语'],
    'Tamil': ['泰米尔语'],
    'Tatar': ['鞑靼语'],
    'Telugu': ['泰卢固语'],
    'Tetun (Dili)': ['德顿语（帝力）'],
    'Thai': ['泰语'],
    'Tibetan': ['藏语'],
    'Tigrinya': ['提格雷尼亚语'],
    'Tswana': ['茨瓦纳语'],
    'Turkish': ['土耳其语'],
    'Ukrainian': ['乌克兰语'],
    'Urdu': ['乌尔都语'],
    'Uyghur': ['维吾尔语'],
    'Vietnamese': ['越南语'],
    'Welsh': ['威尔士语'],
    'Wolof': ['沃洛夫语'],
    'Yoruba': ['约鲁巴语'],
    'Zulu': ['祖鲁语'],

    'Other languages': ['其他语种'],

    # Encodings
    'All languages': ['所有语种'],
    'Baltic languages': ['波罗的海诸语'],
    'Celtic languages': ['凯尔特语'],
    'Chinese': ['汉语'],
    'Cyrillic': ['西里尔'],
    'English': ['英语'],

    'European (Central)': ['欧洲（中部）'],
    'European (Northern)': ['欧洲（北部）'],
    'European (Southern)': ['欧洲（南部）'],
    'European (Southeastern)': ['欧洲（东南部）'],
    'European (Western)': ['欧洲（西部）'],
    'European': ['欧洲'],

    'German': ['德语'],
    'Greek': ['希腊语'],
    'Hebrew': ['希伯来语'],
    'Nordic languages': ['北欧诸语'],
    'Portuguese': ['葡萄牙语'],

    # NLP utils
    'Armenian': ['亚美尼亚语'],
}
TRS_ENCODINGS = {
    # "with/without BOM" contained in "BE/LE with/without BOM"
    'BE with BOM': [' 大端带签名'],
    'BE without BOM': [' 大端无签名'],
    'LE with BOM': [' 小端带签名'],
    'LE without BOM': [' 小端无签名'],
    'with BOM': ['带签名'],
    'without BOM': ['无签名'],
}
TRS_FILE_TYPES = {
    'CSV files (*.csv)': ['CSV 文件 (*.csv)'],
    'Excel workbooks (*.xlsx)': ['Excel 工作簿 (*.xlsx)'],
    'HTML pages (*.htm; *.html)': ['HTML 页面 (*.htm; *.html)'],
    'PDF files (*.pdf)': ['PDF 文件 (*.pdf)'],
    'Text files (*.txt)': ['文本文件 (*.txt)'],
    'Translation memory files (*.tmx)': ['翻译记忆库文件 (*.tmx)'],
    'Word documents (*.docx)': ['Word 文档 (*.docx)'],
    'XML files (*.xml)': ['XML 文件 (*.xml)'],
    'All files (*.*)': ['所有文件 (*.*)']
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
    'Dependency Parser Settings': ['依存分析器设置'],
    'Dependency Parsers': ['依存分析器'],
    'Sentiment Analyzer Settings': ['情感分析器设置'],
    'Sentiment Analyzer': ['情感分析器'],

    'sentence tokenizer': ['分句器'],
    'sentence recognizer': ['句子识别器'],
    'sentencizer': ['分句器'],

    'Legality syllable tokenizer': ['合法性分音节器'],
    'Sonority sequencing syllable tokenizer': ['响度顺序分音节器'],
    'syllable tokenizer': ['分音节器'],
    'Syllable dictionary': ['音节词典'],

    'word tokenizer (split mode A)': ['分词器（切分模式 A）'],
    'word tokenizer (split mode B)': ['分词器（切分模式 B）'],
    'word tokenizer (split mode C)': ['分词器（切分模式 C）'],
    'word tokenizer': ['分词器'],
    'Penn Treebank tokenizer': ['宾州树库分词器'],
    'Twitter tokenizer': ['推特分词器'],
    'Regular-expression tokenizer': ['正则表达式分词器'],
    'character tokenizer': ['分字器'],
    'kanji tokenizer': ['分字器'],
    'tokenizer': ['分词器'],

    'Perceptron part-of-speech tagger': ['感知机词性标注器'],
    'perceptron part-of-speech tagger': ['感知机词性标注器'],
    'part-of-speech tagger': ['词性标注器'],
    'Morphological analyzer': ['形态分析器'],
    'Yunshan Cup 2020': ['2020 云山杯'],

    'lemmatizer': ['词形还原器'],

    'Custom stop word list': ['自定义停用词表'],
    'stop word list': ['停用词表'],

    'dependency parser': ['依存分析器'],
    'sentiment analyzer': ['情感分析器']
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
    'to': ['至'],
    'No limit': ['无限制'],
    'Two-tailed': ['双尾'],
    'Left-tailed': ['左尾'],
    'Right-tailed': ['右尾'],
    'Minimum': ['最小'],
    'Maximum': ['最大'],

    # File Area
    'Name': ['名称'],
    'Path': ['路径'],
    'Encoding': ['编码'],
    'Language': ['语种'],

    # Work Area
    'Total': ['合计'],

    'Generate table': ['生成表格'],
    'Generate figure': ['生成图表'],
    'Clear table': ['清空表格'],

    'Token Settings': ['形符设置'],
    'Search Settings': ['搜索设置'],
    'Context Settings': ['上下文设置'],
    'Generation Settings': ['生成设置'],
    'Table Settings': ['表格设置'],
    'Figure Settings': ['图表设置'],

    # Language-specific files
    'ACKS.md': ['doc/trs/zho_cn/ACKS.md']
}

if __name__ == '__main__':
    with open('trs/zho_cn.ts', 'r', encoding = 'utf_8') as f:
        soup = bs4.BeautifulSoup(f.read(), features = 'lxml')

    for element_context in soup.select('context'):
        for element_message in element_context.select('message'):
            tr_hit = False
            unfinished = False

            element_src = element_message.select_one('source')
            element_tr = element_message.select_one('translation')

            # Do not re-translate obsolete translations
            if (
                'type' not in element_tr.attrs
                or ('type' in element_tr.attrs and element_tr['type'] != 'obsolete')
            ):
                tr = element_src.text
                tr_raw = tr

                # Languages
                for lang, trs in TRS_LANGS.items():
                    # Language names
                    if tr == lang:
                        tr = trs[0]
                    elif f'{lang} (' in tr:
                        tr = tr.replace(f'{lang} (', f'{trs[0]} (', 1)
                    # Script names
                    elif 'script)' in lang and lang in tr:
                        tr = tr.replace(lang, trs[0])
                    # Encoding names
                    elif tr.startswith(f'{lang}/'):
                        tr = tr.replace(f'{lang}/', f'{trs[0]}/', 1)
                    # Language utility names
                    elif f' - {lang} ' in tr:
                        tr = tr.replace(f' - {lang} ', f' - {trs[0]} ', 1)

                # Encodings
                for encoding, trs in TRS_ENCODINGS.items():
                    if encoding in tr:
                        tr = tr.replace(encoding, trs[0])

                        break

                # File types
                for file_type, trs in TRS_FILE_TYPES.items():
                    if tr == file_type:
                        tr = trs[0]

                        break

                # NLP utils
                for util, trs in TRS_NLP_UTILS.items():
                    # Only replace language utility names after language names or at the end of text
                    if f' - {util}' in tr or tr.endswith(util):
                        if f' - {util}' in tr:
                            tr = tr.replace(f' - {util}', f' - {trs[0]}', 1)
                        elif tr.endswith(util):
                            tr = tr.replace(util, trs[0], 1)

                        break

                # Misc
                for item, trs in TRS_MISC.items():
                    if tr == item:
                        tr = trs[0]

                        break

                # Exceptions
                if any((text in tr for text in [])):
                    # Flag translation as unfinished to be reviewed manually
                    unfinished = True

                if tr_raw != tr:
                    # Do not replace parentheses in file type filters
                    if element_src.text not in TRS_FILE_TYPES:
                        # Parentheses
                        tr = re.sub(r'\s*\(', r'（', tr)
                        tr = re.sub(r'\)\s*', r'）', tr)
                        # Remove whitespace between Chinese characters
                        tr = re.sub(r'(?<=[\u4E00-\u9FFF（）])\s+(?=[\u4E00-\u9FFF（）])', '', tr)

                    element_tr.string = tr

                    if unfinished:
                        element_tr.attrs = {'type': 'unfinished'}
                    else:
                        element_tr.attrs = {}

                    print(f'Auto-translated "{element_src.text}" into "{tr}".')

    with open('trs/zho_cn.ts', 'w', encoding = 'utf_8') as f:
        f.write(str(soup))

    # Release
    wl_trs_utils.del_obsolete_trans('trs/zho_cn.ts')
    wl_trs_utils.release_trs()

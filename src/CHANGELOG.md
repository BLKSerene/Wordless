<!--
# Wordless: Changelog
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
-->

<div align="center"><h1>📄 Changelog</h1></div>

## [2.2.0](https://github.com/BLKSerene/Wordless/releases/tag/2.2.0) - ??/??/2022
### 🎉 New Features
- File Area: Add support for .tmx files
- Settings: Add Settings - General - Proxy Settings
- Utils: Add Lemmatization Lists's Russian lemma list
- Utils: Add spaCy's Greek (Ancient) and Irish lemmatizers
- Utils: Add spaCy's Japanese word tokenizer, POS tagger, and lemmatizer
- Utils: Add SudachiPy's Japanese word tokenizer, POS tagger, and lemmatizer
- Utils: Add Underthesea's Vietnamese sentiment analyzer
- Work Area: Add Overview - Paragraph/Sentence/Token/Type/Syllable Length (Variance / Minimum / 25th Percentile / Median / 75th Percentile / Maximum / Range / Modes)

### ✨ Improvements
- File Area: Remove temporary files when closing files
- File Area: Show original file paths instead of modified ones
- Work Area: Update Work Area - Figure Settings - Sort by File

### ❌ Removals
- File Area: Remove Open File(s) / Open Folder / Reload Selected / Reload All / Close Selected / Close All
- Menu: Remove Preferences - Settings - Word Detokenization
- Settings: Remove Settings - Word Detokenization
- Utils: Remove lemmalist-greek's Greek (Ancient) lemma list
- Utils: Remove syntok's sentence segmenter and word tokenizer

### ⏫ Dependency Changes
- Dependencies: Add SudachiPy
- Dependencies: Remove lemmalist-greek
- Dependencies: Remove syntok
- Dependencies: Upgrade Charset Normalizer to 2.0.11
- Dependencies: Upgrade NLTK to 3.6.7
- Dependencies: Upgrade Pyphen to 0.12.0
- Dependencies: Upgrade PyQt to 5.15.6
- Dependencies: Upgrade Requests to 2.27.1
- Dependencies: Upgrade spaCy to 3.2.1
- Dependencies: Upgrade TextBlob to 0.17.1
- Dependencies: Upgrade Underthesea to 1.3.4

## [2.1.0](https://github.com/BLKSerene/Wordless/releases/tag/2.1.0) - 10/14/2021
### 🎉 New Features
- Settings: Add Settings - Files - Miscellaneous - Read files in chunks of lines
- Settings: Add Settings - Files - Tags - Header Tag Settings / Body Tag Settings / XML Tag Settings - Insert/Clear
- Settings: Add Settings - Stop Word Lists - Preview - Insert
- Settings: Add Settings - Syllable Tokenization
- Utils: Add Pyphen's syllable tokenizers
- Utils: Add PyThaiNLP's Thai syllable tokenizer
- Utils: Add spaCy's Azerbaijani word tokenizer and stop word list
- Utils: Add spaCy's Greek (Ancient) word tokenizer and stop word list
- Utils: Add ssg's Thai syllable tokenizer
- Work Area: Add Overview - Automated Readability Index / Coleman-Liau Index / Dale-Chall Readability Score / Devereaux Readability Index / Flesch Reading Ease / Flesch Reading Ease (Simplified) / Flesch-Kincaid Grade Level / FORCAST Grade Level / Gunning Fog Index / SMOG Grade / Spache Grade Level / Write Score / Count of Syllables / Token Length in Syllable / Type Length in Syllable / Syllable Length in Character
- Work Area: Add Work Area - Search Settings - Multi-search Mode - Insert

### ✨ Improvements
- Work Area: Update Keyword - Generation Settings - Reference Files

### 📌 Bugfixes
- File Area: Fix Auto-detection Settings
- Settings: Fix Settings - POS Tagging - Tagsets - Mapping Settings - Reset All
- Settings: Fix Settings - Stop Word Lists - Stop Word Lists Settings - Custom List

### ❌ Removals
- File Area: Remove support for .tmx files

### ⏫ Dependency Changes
- Dependencies: Add Pyphen
- Dependencies: Add ssg
- Dependencies: Upgrade Beautiful Soup to 4.10.0
- Dependencies: Upgrade botok to 0.8.8
- Dependencies: Upgrade Charset Normalizer to 2.0.7
- Dependencies: Upgrade Matplotlib to 3.4.3
- Dependencies: Upgrade NetworkX to 2.6.3
- Dependencies: Upgrade NLTK to 3.6.5
- Dependencies: Upgrade NumPy to 1.21.2
- Dependencies: Upgrade openpyxl to 3.0.9
- Dependencies: Upgrade PyInstaller to 4.5.1
- Dependencies: Upgrade PyThaiNLP to 2.3.2
- Dependencies: Upgrade Sacremoses to 0.0.46
- Dependencies: Upgrade SciPy to 1.7.1
- Dependencies: Upgrade spaCy to 3.1.3
- Dependencies: Upgrade Tokenizer to 3.3.2

## [2.0.0](https://github.com/BLKSerene/Wordless/releases/tag/2.0.0) - 07/21/2021

### 🎉 New Features
- Settings: Add Settings - Files - Default Settings - Tokenized/Tagged
- Utils: Add CLTK's Akkadian, Arabic (Standard), Coptic, English (Middle), English (Old), French (Old), German (Middle High), Greek (Ancient), Hindi, Latin, Marathi (Old), Norse (Old), Punjabi, and Sanskrit stop word lists
- Utils: Add PyThaiNLP's NERCut
- Utils: Add PyThaiNLP's perceptron tagger (LST20)
- Utils: Add spaCy's Amharic, Kyrgyz, Macedonian, Sanskrit, Tigrinya, and Tswana word tokenizers
- Utils: Add spaCy's Amharic, Korean, Kyrgyz, Macedonian, Sanskrit, Tigrinya, and Tswana stop word lists
- Utils: Add spaCy's Bengali, Croatian, Czech, Hungarian, Indonesian, Luxembourgish, Persian, Serbian (Cyrillic), Swedish, Tagalog, Turkish, and Urdu lemmatizers
- Utils: Add spaCy's Catalan POS tagger and lemmatizer
- Utils: Add spaCy's Chinese word tokenizer and POS tagger
- Utils: Add spaCy's Macedonian POS tagger and lemmatizer
- Utils: Add spaCy's Russian POS tagger and lemmatizer
- Utils: Add spaCy's sentence recognizer
- Work Area: Add Collocation/Colligation - Generation Settings - Limit Searching
- Work Area: Add Concordancer (Parallel Mode)

### ✨ Improvements
- File Area: Cache loaded files
- Utils: Update encoding detection
- Utils: Update NLTK's word tokenizers
- Utils: Update spaCy's sentencizer, word tokenizers, POS taggers, and lemmatizers

### 📌 Bugfixes
- Utils: Fix Sacremoses's Moses tokenizer and Moses detokenizer
- Work Area: Fix Concordancer - Sort Results - Order

### ❌ Removals
- Utils: Remove AttaCut's Thai word tokenizer

### ⏫ Dependency Changes
- Dependencies: Add Charset Normalizer
- Dependencies: Add CLTK
- Dependencies: Remove AttaCut
- Dependencies: Remove cChardet
- Dependencies: Remove chardet
- Dependencies: Upgrade botok to 0.8.7
- Dependencies: Upgrade langdetect to 1.0.9
- Dependencies: Upgrade Matplotlib to 3.4.2
- Dependencies: Upgrade NetworkX to 2.6.1
- Dependencies: Upgrade NLTK to 3.6.2
- Dependencies: Upgrade NumPy to 1.21.1
- Dependencies: Upgrade openpyxl to 3.0.7
- Dependencies: Upgrade PyInstaller to 4.4
- Dependencies: Upgrade PyQt to 5.15.4
- Dependencies: Upgrade PyThaiNLP to 2.3.1
- Dependencies: Upgrade Python 3.8.10
- Dependencies: Upgrade python-docx to 0.8.11
- Dependencies: Upgrade Requests to 2.26.0
- Dependencies: Upgrade Sacremoses to 0.0.45
- Dependencies: Upgrade SciPy to 1.7.0
- Dependencies: Upgrade spaCy to 3.1.0
- Dependencies: Upgrade Tokenizer to 3.1.2


## [1.5.0](https://github.com/BLKSerene/Wordless/releases/tag/1.5.0) - 01/15/2021

### 🎉 New Features
- Utils: Add AttaCut's Thai word tokenizer
- Utils: Add pkuseg's Chinese word tokenizer
- Utils: Add TextBlob's English sentiment analyzer
- Utils: Add Tokenizer's Icelandic sentence tokenizer and word tokenizer
- Work Area: Add Collocation/Colligation - Generation Settings - Test of Statistical Significance - Berry-Rogghe’s z-score
- Work Area: Add Concordancer - Sentiment
- Work Area: Add Overview - Count of n-length Sentences

### ✨ Improvements
- File Area: Only load files that can be successfully decoded
- Work Area: Overview/Concordancer - Rename “Clause” to “Sentence Segment”

### 📌 Bugfixes
- Settings: Fix Settings - Word Tokenization - Preview - Select language - Vietnamese
- Utils: Fix NLTK's Penn Treebank Detokenizer
- Work Area: Fix Concordancer - Generate Figure

### ❌ Removals
- File Area: Remove support for .lrc files
- File Area: Remove support for .xls files
- Work Area: Remove Concordancer - Sentence Segment No.
- Work Area: Remove Overview - Count of Sentence Segments / Paragraph Length in Sentence Segment / Sentence Segment Length in Token

### ⏫ Dependency Changes
- Dependencies: Add AttaCut
- Dependencies: Add pkuseg
- Dependencies: Add TextBlob
- Dependencies: Add Tokenizer
- Dependencies: Remove xlrd
- Dependencies: Upgrade chardet to 4.0.0
- Dependencies: Upgrade NumPy to 1.19.5
- Dependencies: Upgrade PyThaiNLP to 2.2.6
- Dependencies: Upgrade Python to 3.8.7
- Dependencies: Upgrade Requests to 2.25.1
- Dependencies: Upgrade SciPy to 1.6.0
- Dependencies: Upgrade spaCy to 2.3.5


## [1.4.0](https://github.com/BLKSerene/Wordless/releases/tag/1.4.0) - 12/11/2020

### 🎉 New Features
- Settings: Add Settings - File - Tags - Header Tag Settings
- Settings: Add Settings - Data - Continue numbering after ties
- Utils: Add botok's Tibetan sentence tokenizer
- Utils: Add NLTK's NLTK tokenizer
- Utils: Add PyThaiNLP's maximum matching + TCC (safe mode)
- Utils: Add spaCy's Armenian, Basque, Estonian, Gujarati, Latvian, Ligurian, Malayalam, Nepali, and Yoruba word tokenizers
- Utils: Add spaCy's Armenian, Basque, Gujarati, Ligurian, Luxembourgish, Malayalam, Nepali, Slovak, Slovenian, and Yoruba stop word lists
- Utils: Add spaCy's Danish POS tagger and lemmatizer
- Utils: Add spaCy's Polish POS tagger and lemmatizer
- Utils: Add spaCy's Romanian POS tagger and lemmatizer
- Utils: Add Stopwords ISO's Gujarati and Lithuanian stop word lists
- Work Area: Add Concordancer - Zapping Settings

### ✨ Improvements
- File Area: Update File Table - Tokenized/Tagged
- File Area: Update support for XML files
- Menu: Disable editing of POS tag mappings for spaCy's POS taggers
- Settings: Update Settings - Files - Tags
- Utils: Update botok's Tibetan word tokenizer, POS tagger, and lemmatizer
- Utils: Update Chinese (Traditional) stop word lists
- Utils: Update NLTK's word tokenizers
- Utils: Update POS tag mappings for spaCy's POS taggers
- Utils: Update PyThaiNLP's CRFCut
- Utils: Update PyThaiNLP's POS taggers
- Utils: Update PyThaiNLP's Thai word tokenizers
- Utils: Update Sacremoses's Moses tokenizer
- Utils: Update Stopwords ISO's Greek and Norwegian stop word lists

### 📌 Bugfixes
- Settings: Fix Settings - POS Tagging
- Work Area: Fix batch processing of a large number of files

### ❌ Removals
- Utils: Remove grk-stoplist's Greek (Ancient) stop word list

### ⏫ Dependency Changes
- Dependencies: Add opencc-python
- Dependencies: Remove grk-stoplist
- Dependencies: Upgrade Beautiful Soup to 4.9.3
- Dependencies: Upgrade botok to 0.8.1
- Dependencies: Upgrade cChardet to 2.1.7
- Dependencies: Upgrade jieba to 0.42.1
- Dependencies: Upgrade langdetect to 1.0.8
- Dependencies: Upgrade Matplotlib to 3.3.3
- Dependencies: Upgrade nagisa to 0.2.7
- Dependencies: Upgrade NetworkX to 2.5
- Dependencies: Upgrade NLTK to 3.5
- Dependencies: Upgrade NumPy to 1.19.3
- Dependencies: Upgrade openpyxl to 3.0.5
- Dependencies: Upgrade PyInstaller to 4.1
- Dependencies: Upgrade pymorphy2 to 0.9.1
- Dependencies: Upgrade PyQt to 5.15.2
- Dependencies: Upgrade PyThaiNLP to 2.2.5
- Dependencies: Upgrade Python to 3.8.6
- Dependencies: Upgrade razdel to 0.5.0
- Dependencies: Upgrade Requests to 2.25.0
- Dependencies: Upgrade Sacremoses to 0.0.43
- Dependencies: Upgrade SciPy to 1.5.4
- Dependencies: Upgrade spaCy to 2.3.4
- Dependencies: Upgrade Stopwords ISO to 1.0.0
- Dependencies: Upgrade syntok to 1.3.1
- Dependencies: Upgrade Underthesea to 1.2.2
- Dependencies: Upgrade WordCloud to 1.8.1


## [1.3.0](https://github.com/BLKSerene/Wordless/releases/tag/1.3.0) - 11/30/2019

### 🎉 New Features
- Utils: Add razdel's Russian sentenizer and word tokenizer
- Utils: Add spaCy's Lithuanian word tokenizer, POS tagger, and lemmatizer
- Utils: Add spaCy's Luxembourgish word tokenizer
- Utils: Add spaCy's Norwegian Bokmål word tokenizer, POS tagger, and lemmatizer
- Utils: Add syntok's sentence segmenter and word tokenizer
- Utils: Add Wordless's sentence and sentence segment splitters
- Work Area: Add Concordancer - Generation Settings - Sampling Method
- Work Area: Add Concordancer - Generation Settings - Width Unit - Paragraph
- Work Area: Add Overview - Paragraph Length in Clause

### ✨ Improvements
- Utils: Force consistent results for language detection
- Utils: Update Sacremoses's Moses tokenizer and detokenizer
- Utils: Update Wordless's sentence segment tokenizer
- Utils: Update spaCy's sentencizer, word tokenizers, POS taggers, and lemmatizers
- Work Area: Display numbers and percentages in different columns
- Work Area: Do not add borders to exported Excel workbooks due to performance issues
- Work Area: Remove illegal characters when exporting tables to Excel workbooks

### 📌 Bugfixes
- File Area / Utils: Fix encoding detection
- Settings: Fix Settings - POS Tagging - Tagsets - Preview Settings - POS Tagger
- Utils: Fix lemmatization of empty tokens
- Work Area: Fix file checking
- Work Area: Fix Overview - Paragraph/Sentence Length

### ❌ Removals
- Utils: Remove Sacremoses's Penn Treebank tokenizer

### ⏫ Dependency Changes
- Dependencies: Add razdel
- Dependencies: Add syntok
- Dependencies: Upgrade Beautiful Soup to 4.8.1
- Dependencies: Upgrade botok (originally named pybo) to 0.6.18
- Dependencies: Upgrade cChardet to 2.1.5
- Dependencies: Upgrade Matplotlib to 3.1.2
- Dependencies: Upgrade NetworkX to 2.4
- Dependencies: Upgrade NumPy to 1.17.4
- Dependencies: Upgrade openpyxl to 3.0.2
- Dependencies: Upgrade PyQt to 5.13.2
- Dependencies: Upgrade Sacremoses to 0.0.35
- Dependencies: Upgrade SciPy to 1.3.3
- Dependencies: Upgrade spaCy to 2.2.3
- Dependencies: Upgrade underthesea to 1.1.17
- Dependencies: Upgrade WordCloud to 1.6.0


## [1.2.0](https://github.com/BLKSerene/Wordless/releases/tag/1.2.0) - 08/27/2019

### 🎉 New Features
- File Area: Add support for .xml files
- Settings: Add Settings - Figures - Line Chart / Word Cloud / Network Graph
- Utils: Add extra-stopwords's stop word lists
- Utils: Add NLTK's Punkt Sentence Tokenizer for Russian
- Utils: Add NLTK's Slovenian and Tajik stop word lists
- Utils: Add spaCy's Marathi word tokenizer and stop word list
- Utils: Add spaCy's Serbian word tokenizer and stop word list
- Work Area: Add Collocation/Colligation - Figure Settings - Graph Type - Network Graph
- Work Area: Add Concordancer - Clause No.
- Work Area: Add Concordancer - Generation Settings - Width Unit - Sentence/Clause
- Work Area: Add Overview - Count of Clauses / Clause Length / Paragraph/Sentence/Token Length (Standard Deviation)

### ✨ Improvements
- Main Window: Check file permissions when exporting tables
- Utils: Update POS tag mappings for pybo's Tibetan POS tagger
- Utils: Update pybo's Tibetan tokenizers, POS tagger, and lemmatizer
- Utils: Update PyThaiNLP's Thai stop word list
- Utils: Update Sacremoses's tokenizers and detokenizer

### 📌 Bugfixes
- Settings: Fix Settings - Stop Words - Preview - Count of Stop Words
- Utils: Fix NLTK's word tokenizers
- Work Area: Fix Collocation and Colligation
- Work Area: Fix Concordancer - Export Selected/All
- Work Area: Fix Concordancer - Sort Results
- Work Area: Fix Work Area - Search Settings / Search in Results

### ⏫ Dependency Changes
- Dependencies: Add extra-stopwords
- Dependencies: Add NetworkX
- Dependencies: Upgrade Beautiful Soup to 4.8.0
- Dependencies: Upgrade Matplotlib to 3.1.1
- Dependencies: Upgrade nagisa to 0.2.4
- Dependencies: Upgrade NLTK to 3.4.5
- Dependencies: Upgrade NumPy to 1.17.0
- Dependencies: Upgrade openpyxl to 2.6.3
- Dependencies: Upgrade pybo to 0.6.7
- Dependencies: Upgrade PyInstaller to 4.0.dev0+46286a1f4
- Dependencies: Upgrade PyQt to 5.13.0
- Dependencies: Upgrade PyThaiNLP to 2.0.7
- Dependencies: Upgrade Python to 3.7.4
- Dependencies: Upgrade Requests to 2.22.0
- Dependencies: Upgrade Sacremoses to 0.0.33
- Dependencies: Upgrade SciPy to 1.3.1
- Dependencies: Upgrade spaCy to 2.1.8
- Dependencies: Upgrade Underthesea to 1.1.16


## [1.1.0](https://github.com/BLKSerene/Wordless/releases/tag/1.1.0) - 03/31/2019

### 🎉 New Features
- Settings: Add Settings - General - Font Settings

### ✨ Improvements
- Main Window: Disable mouse wheel for combo boxes and spin boxes when they are not focused
- Utils: Update spaCy's sentencizer
- Utils: Update POS tag mappings for spaCy's English POS tagger

### 📌 Bugfixes
- File Area: Fix Open Folder
- Settings: Fix Settings - Sentence Tokenization / Word Tokenization / Word Detokenization / POS Tagging / Lemmatization - Preview
- Startup: Fix checking for updates on startup
- Utils: Fix spaCy's sentence tokenizers and word tokenizers
- Utils: Fix Wordless's Chinese and Japanese character tokenizers
- Work Area: Fix Concordancer - Search in Results
- Work Area: Fix Work Area - Search Settings - Context Settings

### ⏫ Dependency Changes
- Dependencies: Upgrade PyQt to 5.12.1
- Dependencies: Upgrade Sacremoses to 0.0.13
- Dependencies: Upgrade spaCy to 2.1.3


## [1.0.0](https://github.com/BLKSerene/Wordless/releases/tag/1.0.0) - 03/20/2019

### 🎉 New Features
- Release Wordless 1.0.0

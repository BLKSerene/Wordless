<!--
# Wordless: Changelog
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
-->

<div align="center"><h1>📄 Changelog</h1></div>

## [3.1.0](https://github.com/BLKSerene/Wordless/releases/tag/3.1.0) - ??/??/2023
### 🎉 New Features
- Settings: Add global settings - encodings - Thai (TIS-620)
- Settings: Add Settings - Figures - Network Graphs - Edge Label Settings - Label position / Rotate labels to lie parallel to edges / Label font weight / Label font color / Label opacity
- Settings: Add Settings - Figures - Network Graphs - Edge Settings - Connection style / Edge width / Edge style / Edge opacity / Arrow style / Arrow size
- Settings: Add Settings - Figures - Network Graphs - Node Label Settings - Label font weight / Label font color / Label opacity
- Settings: Add Settings - Figures - Network Graphs - Node Settings
- Settings: Add Settings - Figures - Word Clouds - Background Settings - Background color - Transparent
- Settings: Add Settings - Figures - Word Clouds - Font Settings - Font size / Relative scaling / Font color
- Settings: Add Settings - Figures - Word Clouds - Mask Settings / Advanced Settings
- Settings: Add Settings - Measures - Dispersion - Gries's DP
- Utils: Add Pyphen's Thai syllable tokenizer
- Work Area: Add Wordlist/N-gram Generator - Generation Settings - Measures of Dispersion / Measure of Adjusted Frequency - Average Logarithmic Distance / Average Reduced Frequency / Average Waiting Time

### ✨ Improvements
- File Area: Disallow empty file names
- File Area: Remove underscores in tokenized Vietnamese files
- Utils: Speed up n-gram/skip-gram generation

### 📌 Bugfixes
- Settings: Fix global settings - encodings
- Settings: Fix Settings - General - User Interface Settings - Interface scaling
- Settings: Fix Settings - Part-of-speech Tagging - Tagsets
- Work Area: Fix Work Area - Filter results

### ❌ Removals
- Settings: Remove Settings - Figures - Word Clouds - Font - GNU FreeFont
- Work Area: Remove Wordlist/N-gram Generator - Generation Settings - Measure of Dispersion - Gries's DPnorm

### ⏫ Dependency Changes
- Dependencies: Upgrade Lingua to 1.3.2
- Dependencies: Upgrade NetworkX to 3.0
- Dependencies: Upgrade NLTK to 3.8.1
- Dependencies: Upgrade NumPy to 1.24.1
- Dependencies: Upgrade pypdf (originally named PyPDF2) to 3.3.0
- Dependencies: Upgrade Pyphen to 0.13.2
- Dependencies: Upgrade PyQt to 5.15.8
- Dependencies: Upgrade Requests to 2.28.2
- Dependencies: Upgrade simplemma to 0.9.1
- Dependencies: Upgrade Underthesea to 6.0.3

## [3.0.0](https://github.com/BLKSerene/Wordless/releases/tag/3.0.0) - 11/21/2022
### 🎉 New Features
- Settings: Add Settings - Dependency Parsing
- Settings: Add Settings - Measures - Readability
- Utils: Add NLTK's Basque, Bengali, Catalan, Chinese (Simplified), Chinese (Traditional), and Hebrew stop word lists
- Utils: Add NLTK's Malayalam Punkt sentence tokenizer
- Utils: Add PyThaiNLP's Thai word detokenizer
- Utils: Add simplemma's lemmatizers
- Utils: Add spaCy's Ganda and Latin word tokenizers
- Utils: Add stopword's stop word lists
- Work Area: Add Dependency Parser
- Work Area: Add Profiler - Automated Arabic Readability Index / Fernández Huerta's Readability Score / Fórmula de comprensibilidad de Gutiérrez de Polini / Fórmula de Crawford / Gulpease Index / Legibilidad µ / Lix / McAlpine EFLAW Readability Score / OSMAN / Rix / Szigriszt's Perspicuity Index / Wiener Sachtextformel

### ✨ Improvements
- Utils: Update NLTK's English and Russian perceptron part-of-speech taggers
- Utils: Update spaCy's sentence tokenizers, word tokenizers, part-of-speech taggers, and lemmatizers
- Work Area: Update N-gram Generator / Collocation Extractor / Colligation Extractor - Search Settings
- Work Area: Update Profiler - Gunning Fog Index / Lensear Write
- Work Area: Update Search Settings / Search in Results

### ❌ Removals
- Menu: Remove Help - Contributing
- Utils: Remove extra-stopwords's stop word lists
- Utils: Remove Lemmatization Lists's lemma lists
- Utils: Remove spaCy's stop word lists
- Utils: Remove Stopwords ISO's stop word lists
- Utils: Remove Wordless's Chinese and Japanese sentence tokenizers
- Utils: Remove Wordless's Thai word detokenizer

### ⏫ Dependency Changes
- Dependencies: Add simplemma and stopword
- Dependencies: Remove extra-stopwords, Lemmatization Lists, and Stopwords ISO
- Dependencies: Upgrade Charset Normalizer to 3.0.1
- Dependencies: Upgrade Lingua to 1.1.3
- Dependencies: Upgrade Matplotlib to 3.6.2
- Dependencies: Upgrade NetworkX to 2.8.8
- Dependencies: Upgrade NumPy to 1.23.5
- Dependencies: Upgrade PyInstaller to 5.6.2
- Dependencies: Upgrade PyPDF2 to 2.11.2
- Dependencies: Upgrade Pyphen to 0.13.1
- Dependencies: Upgrade PyThaiNLP to 3.1.1
- Dependencies: Upgrade SciPy to 1.9.3
- Dependencies: Upgrade spaCy to 3.4.3
- Dependencies: Upgrade spacy-pkuseg to 0.0.32
- Dependencies: Upgrade Underthesea to 1.3.5

## [2.3.0](https://github.com/BLKSerene/Wordless/releases/tag/2.3.0) - 09/25/2022
### 🎉 New Features
- File Area: Add Observed Files / Reference Files
- File Area: Add support for .pdf files
- Settings: Add Settings - Figures - Word Clouds - Font Path
- Settings: Add Settings - General - User Interface Settings - Interface Scaling
- Settings: Add Settings - Measures - Bayes Factor
- Settings: Add Settings - Measures - Statistical Significance - Log-likelihood Ratio Test / Welch's t-test / z-score (Berry-Rogghe)
- Settings: Add Settings - Measures - Statistical Significance - Student's t-test (1-sample) / Student's t-test (2-sample) / Welch's t-test - Direction
- Settings: Add Settings - Tables - Profiler
- Utils: Add NLTK's legality syllable tokenizer and sonority sequencing syllable tokenizer
- Utils: Add NLTK's regular-expression tokenizer
- Utils: Add Pyphen's Catalan syllable tokenizer
- Utils: Add PyThaiNLP's ThaiSumCut
- Utils: Add spaCy's Croatian and Swedish part-of-speech taggers
- Utils: Add spaCy's Finnish part-of-speech tagger and lemmatizer
- Utils: Add spaCy's Sorbian (Lower) word tokenizer and stop word list
- Utils: Add spaCy's Sorbian (Upper) word tokenizer and stop word list
- Utils: Add spaCy's Ukrainian part-of-speech tagger and lemmatizer
- Work Area: Add Collocation/Colligation Extractor - Generation Settings - Limit Searching - Within Sentence Segments
- Work Area: Add Collocation/Colligation/Keyword Extractor - Generation Settings - Measure of Bayes Factor
- Work Area: Add Collocation/Colligation/Keyword Extractor - Generation Settings - Test of Statistical Significance / Measure of Effect Size - None
- Work Area: Add Concordancer - Generation Settings - Width Unit - Sentence Segment
- Work Area: Add Concordancer - Sentence Segment No.
- Work Area: Add Profiler - Count of Sentence Segments / Paragraph Length in Sentence Segments / Sentence Segment Length in Tokens / Count of n-length Sentence Segments
- Work Area: Add Profiler - Paragraph/Sentence/Token/Type/Syllable Length (Interquartile Range)
- Work Area: Add Wordlist/N-gram Generator - Generation Settings - Measure of Dispersion / Adjusted Frequency - None
- Work Area: Add Work Area - Search Settings - Context Settings - Save

### ✨ Improvements
- Settings: Allow resizing of Settings dialog box
- Settings: Update Settings - Files - Tags - Header Tag Settings
- Utils: Update language detection
- Work Area: Allow one-to-many parallel concordancing in Parallel Concordancer
- Work Area: Update Profiler - Type-token Ratio (Standardized)

### 📌 Bugfixes
- File Area: Fix support for .tmx files
- Work Area: Fix Collocation/Colligation Extractor - Generation Settings - Limit Searching
- Work Area: Fix Concordancer / Parallel Concordancer - Exported Selected/All after sorting
- Work Area: Fix Profiler - Table Settings - Show Cumulative after clicking horizontal headers
- Work Area: Fix Profiler - Token Settings - Use tags only

### ❌ Removals
- Settings: Remove Settings - Measures - Adjusted Frequency - Use same settings in "Settings → Measures → Dispersion"
- Utils: Remove CLTK's stop word lists
- Utils: Remove nagisa's Japanese word tokenizer and part-of-speech tagger
- Utils: Remove PyThaiNLP's maximum matching + TCC (safe mode)
- Utils: Remove ssg's Thai syllable tokenizer
- Utils: Remove Tokenizer's Icelandic sentence tokenizer and word tokenizer
- Work Area: Remove Concordancer - Zapping Settings - Discard position information
- Work Area: Remove Concordancer / Parallel Concordancer - Generation Settings - Sampling Method
- Work Area: Remove Keyword Extractor - Generation Settings - Reference Files
- Work Area: Remove N-gram Generator - Search Settings - Allow skipped tokens within search terms
- Work Area: Remove Parallel Concordancer - Sort Results / Generation Settings
- Work Area: Remove Profiler - Generation Settings
- Work Area: Remove Wordlist Generator / N-gram Generator / Collocation Extractor / Colligation Extractor / Keyword Extractor - Generation Settings - Advanced Settings

### ⏫ Dependency Changes
- Dependencies: Add Lingua, PyPDF2, and spacy-pkuseg
- Dependencies: Remove CLTK, langdetect, langid.py, nagisa, pkuseg, ssg, and Tokenizer
- Dependencies: Upgrade Beautiful Soup to 4.11.1
- Dependencies: Upgrade Botok to 0.8.10
- Dependencies: Upgrade Charset Normalizer to 2.1.1
- Dependencies: Upgrade Matplotlib to 3.6.0
- Dependencies: Upgrade NetworkX to 2.8.6
- Dependencies: Upgrade NumPy to 1.23.3
- Dependencies: Upgrade openpyxl to 3.0.10
- Dependencies: Upgrade PyInstaller to 5.4.1
- Dependencies: Upgrade Pyphen to 0.13.0
- Dependencies: Upgrade PyQt to 5.15.7
- Dependencies: Upgrade PyThaiNLP to 3.1.0
- Dependencies: Upgrade Requests to 2.28.1
- Dependencies: Upgrade Sacremoses to 0.0.53
- Dependencies: Upgrade SciPy to 1.9.1
- Dependencies: Upgrade spaCy to 3.4.1
- Dependencies: Upgrade SudachiPy to 0.6.6
- Dependencies: Upgrade WordCloud to 1.8.2.2

## [2.2.0](https://github.com/BLKSerene/Wordless/releases/tag/2.2.0) - 03/12/2022
### 🎉 New Features
- File Area: Add support for .tmx files
- Menu: Add Preferences - Display Language
- Misc: Add Chinese (Simplified) and Chinese (Traditional) translations
- Settings: Add Settings - General - Proxy Settings
- Utils: Add Lemmatization Lists's Russian lemma list
- Utils: Add spaCy's Greek (Ancient) and Irish lemmatizers
- Utils: Add spaCy's Japanese word tokenizer, part-of-speech tagger, and lemmatizer
- Utils: Add SudachiPy's Japanese word tokenizer, part-of-speech tagger, and lemmatizer
- Utils: Add Underthesea's Vietnamese sentiment analyzer
- Work Area: Add Profiler - Paragraph/Sentence/Token/Type/Syllable Length (Variance / Minimum / 25th Percentile / Median / 75th Percentile / Maximum / Range / Modes)

### ✨ Improvements
- File Area: Remove temporary files when closing files
- File Area: Show original file paths instead of modified ones
- Utils: Update CLTK's Norse (Old) stop word list
- Work Area: Update Work Area - Figure Settings - Sort by File

### ❌ Removals
- File Area: Remove Open File(s) / Open Folder / Reload Selected / Reload All / Close Selected / Close All
- Menu: Remove File - Reload Selected/All
- Menu: Remove Preferences - Settings - Word Detokenization
- Settings: Remove Settings - Word Detokenization
- Utils: Remove lemmalist-greek's Greek (Ancient) lemma list
- Utils: Remove razdel's Russian sentenizer and word tokenizer
- Utils: Remove syntok's sentence segmenter and word tokenizer

### ⏫ Dependency Changes
- Dependencies: Add SudachiPy
- Dependencies: Remove lemmalist-greek, razdel, and syntok
- Dependencies: Upgrade Charset Normalizer to 2.0.12
- Dependencies: Upgrade Matplotlib to 3.5.1
- Dependencies: Upgrade NetworkX to 2.7.1
- Dependencies: Upgrade NLTK to 3.7
- Dependencies: Upgrade NumPy to 1.22.3
- Dependencies: Upgrade PyInstaller to 4.10
- Dependencies: Upgrade Pyphen to 0.12.0
- Dependencies: Upgrade PyQt to 5.15.6
- Dependencies: Upgrade PyThaiNLP to 3.0.5
- Dependencies: Upgrade Requests to 2.27.1
- Dependencies: Upgrade Sacremoses to 0.0.47
- Dependencies: Upgrade SciPy to 1.8.0
- Dependencies: Upgrade spaCy to 3.2.3
- Dependencies: Upgrade TextBlob to 0.17.1
- Dependencies: Upgrade Tokenizer to 3.4.0
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
- Dependencies: Add Pyphen and ssg
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
- Utils: Add spaCy's Catalan part-of-speech tagger and lemmatizer
- Utils: Add spaCy's Chinese word tokenizer and part-of-speech tagger
- Utils: Add spaCy's Macedonian part-of-speech tagger and lemmatizer
- Utils: Add spaCy's Russian part-of-speech tagger and lemmatizer
- Utils: Add spaCy's sentence recognizer
- Work Area: Add Collocation/Colligation - Generation Settings - Limit Searching
- Work Area: Add Concordancer (Parallel Mode)

### ✨ Improvements
- File Area: Cache loaded files
- Utils: Update encoding detection
- Utils: Update NLTK's word tokenizers
- Utils: Update spaCy's sentencizer, word tokenizers, part-of-speech taggers, and lemmatizers

### 📌 Bugfixes
- Utils: Fix Sacremoses's Moses tokenizer and Moses detokenizer
- Work Area: Fix Concordancer - Sort Results - Order

### ❌ Removals
- Utils: Remove AttaCut's Thai word tokenizer

### ⏫ Dependency Changes
- Dependencies: Add Charset Normalizer and CLTK
- Dependencies: Remove AttaCut, cChardet, and chardet
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
- Utils: Fix NLTK's Penn Treebank detokenizer
- Work Area: Fix Concordancer - Generate Figure

### ❌ Removals
- File Area: Remove support for .lrc and .xls files
- Work Area: Remove Concordancer - Sentence Segment No.
- Work Area: Remove Overview - Count of Sentence Segments / Paragraph Length in Sentence Segment / Sentence Segment Length in Token

### ⏫ Dependency Changes
- Dependencies: Add AttaCut, pkuseg, TextBlob, and Tokenizer
- Dependencies: Remove xlrd
- Dependencies: Upgrade chardet to 4.0.0
- Dependencies: Upgrade NumPy to 1.19.5
- Dependencies: Upgrade PyThaiNLP to 2.2.6
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
- Utils: Add spaCy's Danish part-of-speech tagger and lemmatizer
- Utils: Add spaCy's Polish part-of-speech tagger and lemmatizer
- Utils: Add spaCy's Romanian part-of-speech tagger and lemmatizer
- Utils: Add Stopwords ISO's Gujarati and Lithuanian stop word lists
- Work Area: Add Concordancer - Zapping Settings

### ✨ Improvements
- File Area: Update Tokenized/Tagged
- File Area: Update support for XML files
- Menu: Disable editing of part-of-speech tag mappings for spaCy's part-of-speech taggers
- Settings: Update Settings - Files - Tags
- Utils: Update botok's Tibetan word tokenizer, part-of-speech tagger, and lemmatizer
- Utils: Update Chinese (Traditional) stop word lists
- Utils: Update NLTK's word tokenizers
- Utils: Update part-of-speech tag mappings for spaCy's part-of-speech taggers
- Utils: Update PyThaiNLP's CRFCut
- Utils: Update PyThaiNLP's part-of-speech taggers
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
- Utils: Add spaCy's Lithuanian word tokenizer, part-of-speech tagger, and lemmatizer
- Utils: Add spaCy's Luxembourgish word tokenizer
- Utils: Add spaCy's Norwegian Bokmål word tokenizer, part-of-speech tagger, and lemmatizer
- Utils: Add syntok's sentence segmenter and word tokenizer
- Utils: Add Wordless's sentence and sentence segment splitters
- Work Area: Add Concordancer - Generation Settings - Sampling Method
- Work Area: Add Concordancer - Generation Settings - Width Unit - Paragraph
- Work Area: Add Overview - Paragraph Length in Clause

### ✨ Improvements
- Utils: Force consistent results for language detection
- Utils: Update Sacremoses's Moses tokenizer and detokenizer
- Utils: Update Wordless's sentence segment tokenizer
- Utils: Update spaCy's sentencizer, word tokenizers, part-of-speech taggers, and lemmatizers
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
- Dependencies: Add razdel and syntok
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
- Utils: Add NLTK's Russian Punkt sentence tokenizer
- Utils: Add NLTK's Slovenian and Tajik stop word lists
- Utils: Add spaCy's Marathi word tokenizer and stop word list
- Utils: Add spaCy's Serbian word tokenizer and stop word list
- Work Area: Add Collocation/Colligation - Figure Settings - Graph Type - Network Graph
- Work Area: Add Concordancer - Clause No.
- Work Area: Add Concordancer - Generation Settings - Width Unit - Sentence/Clause
- Work Area: Add Overview - Count of Clauses / Clause Length / Paragraph/Sentence/Token Length (Standard Deviation)

### ✨ Improvements
- Main Window: Check file permissions when exporting tables
- Utils: Update part-of-speech tag mappings for pybo's Tibetan part-of-speech tagger
- Utils: Update pybo's Tibetan tokenizers, part-of-speech tagger, and lemmatizer
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
- Dependencies: Add extra-stopwords and NetworkX
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
- Utils: Update part-of-speech tag mappings for spaCy's English part-of-speech tagger

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

<!--
# Wordless: Changelog
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
-->

<div align="center"><h1>📄 Changelog</h1></div>

## [v1.4.0](https://github.com/BLKSerene/Wordless/releases/tag/v1.4.0) - ??/??/2020

### 🎉 New Features
- Utils: Add botok's Tibetan sentence tokenizer
- Utils: Add NLTK's NLTK tokenizer
- Utils: Add PyThaiNLP's maximum matching + TCC (safe mode)
- Utils: Add spaCy's Armenian, Basque, Estonian, Gujarati, Latvian, Ligurian, and Malayalam word tokenizers
- Utils: Add spaCy's Armenian, Basque, Gujarati, Ligurian, Luxembourgish, Malayalam, Slovak, and Slovenian stop word lists
- Utils: Add spaCy's Danish POS tagger and lemmatizer
- Utils: Add spaCy's Polish POS tagger and lemmatizer
- Utils: Add spaCy's Romanian POS tagger and lemmatizer
- Utils: Add Stopwords ISO's Gujarati and Lithuanian stop word lists

### ✨ Improvements
- Menu: Disable editing of POS tag mappings for spaCy's POS taggers
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
- Overview: Fix batch processing of a large number of files

### ❌ Removals
- Utils: Remove grk-stoplist's Greek (Ancient) stop word list

### ⏫ Dependency Changes
- Dependencies: Add OpenCC
- Dependencies: Remove grk-stoplist
- Dependencies: Upgrade Beautiful Soup to 4.9.1
- Dependencies: Upgrade botok to 0.8.1
- Dependencies: Upgrade jieba to 0.42.1
- Dependencies: Upgrade lxml to 4.5.2
- Dependencies: Upgrade Matplotlib to 3.3.1
- Dependencies: Upgrade nagisa to 0.2.7
- Dependencies: Upgrade NetworkX to 2.5
- Dependencies: Upgrade NLTK to 3.5
- Dependencies: Upgrade NumPy to 1.19.1
- Dependencies: Upgrade openpyxl to 3.0.5
- Dependencies: Upgrade PyQt to 5.15.0
- Dependencies: Upgrade pytest to 6.0.1
- Dependencies: Upgrade PyThaiNLP to 2.2.0
- Dependencies: Upgrade Python to 3.7.7
- Dependencies: Upgrade razdel to 0.5.0
- Dependencies: Upgrade requests to 2.24.0
- Dependencies: Upgrade Sacremoses to 0.0.43
- Dependencies: Upgrade SciPy to 1.5.2
- Dependencies: Upgrade spaCy to 2.3.2
- Dependencies: Upgrade Stopwords ISO to 1.0.0
- Dependencies: Upgrade syntok to 1.3.1
- Dependencies: Upgrade WordCloud to 1.8.0

## [v1.3.0](https://github.com/BLKSerene/Wordless/releases/tag/v1.3.0) - 11/30/2019

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
- File Area: Update hint messages
- Main Window: Update error messages
- Utils: Force consistent results for language detection
- Utils: Update Sacremoses's Moses tokenizer and detokenizer
- Utils: Update Wordless's sentence segment tokenizer
- Utils: Update spaCy's sentencizer, word tokenizers, POS taggers, and lemmatizers
- Work Area: Display numbers and percentages in different columns
- Work Area: Do not add borders to exported Excel workbooks due to performance issues
- Work Area: Remove illegal characters when exporting tables to Excel workbooks
- Work Area: Show hint messages when exporting tables
- Work Area: Show hint messages when sorting results

### 📌 Bugfixes
- File Area / Utils: Fix encoding detection
- Menu: Fix Preferences - Settings - POS Tagging - Tagsets - Preview Settings - POS Tagger
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
- Dependencies: Upgrade lxml to 4.4.2
- Dependencies: Upgrade Matplotlib to 3.1.2
- Dependencies: Upgrade NetworkX to 2.4
- Dependencies: Upgrade NumPy to 1.17.4
- Dependencies: Upgrade openpyxl to 3.0.2
- Dependencies: Upgrade PyQt to 5.13.2
- Dependencies: Upgrade pytest to 5.3.1
- Dependencies: Upgrade Sacremoses to 0.0.35
- Dependencies: Upgrade SciPy to 1.3.3
- Dependencies: Upgrade spaCy to 2.2.3
- Dependencies: Upgrade syntok to 1.2.2
- Dependencies: Upgrade underthesea to 1.1.17
- Dependencies: Upgrade WordCloud to 1.6.0

## [v1.2.0](https://github.com/BLKSerene/Wordless/releases/tag/v1.2.0) - 08/27/2019

### 🎉 New Features
- File Area: Add support for .xml files
- Menu: Add Preferences - Settings - Figures - Line Chart / Word Cloud / Network Graph
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
- Menu: Fix Preferences - Settings - Stop Words - Preview - Count of Stop Words
- Utils: Fix NLTK's word tokenizers
- Work Area: Fix Collocation and Colligation
- Work Area: Fix Concordancer - Export Selected/All
- Work Area: Fix Concordancer - Sort Results
- Work Area: Fix Work Area - Search Settings / Search in Results

### ⏫ Dependency Changes
- Dependencies: Add extra-stopwords
- Dependencies: Add NetworkX
- Dependencies: Upgrade Beautiful Soup to 4.8.0
- Dependencies: Upgrade lxml to 4.4.1
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
- Dependencies: Upgrade requests to 2.22.0
- Dependencies: Upgrade Sacremoses to 0.0.33
- Dependencies: Upgrade SciPy to 1.3.1
- Dependencies: Upgrade spaCy to 2.1.8
- Dependencies: Upgrade Underthesea to 1.1.16

## [v1.1.0](https://github.com/BLKSerene/Wordless/releases/tag/v1.1.0) - 03/31/2019

### 🎉 New Features
- Menu: Add Preferences - Settings - General - Font Settings

### ✨ Improvements
- Main Window: Disable mouse wheel for combo boxes and spin boxes when they are not focused
- Main Window: Update hint messages
- Utils: Update spaCy's sentencizer
- Utils: Update POS tag mappings for spaCy's English POS tagger

### 📌 Bugfixes
- File Area: Fix Open Folder
- Menu: Fix Preferences - Settings - Sentence Tokenization / Word Tokenization / Word Detokenization / POS Tagging / Lemmatization - Preview
- Startup: Fix checking for updates at startup
- Utils: Fix spaCy's sentence tokenizers and word tokenizers
- Utils: Fix Wordless's Chinese and Japanese character tokenizers
- Work Area: Fix Concordancer - Search in Results
- Work Area: Fix Work Area - error messages
- Work Area: Fix Work Area - Search Settings - Context Settings

### ⏫ Dependency Changes
- Dependencies: Upgrade lxml to 4.3.3
- Dependencies: Upgrade PyQt to 5.12.1
- Dependencies: Upgrade Sacremoses to 0.0.13
- Dependencies: Upgrade spaCy to 2.1.3

## [v1.0.0](https://github.com/BLKSerene/Wordless/releases/tag/v1.0.0) - 03/20/2019

### 🎉 New Features
- First release

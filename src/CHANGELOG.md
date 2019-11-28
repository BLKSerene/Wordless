<!--
# Wordless: Changelog
#
# Copyright (C) 2018-2019  Ye Lei (叶磊))
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
-->

<div align="center"><h1>📄 Changelog</h1></div>

## [v1.3.0](https://github.com/BLKSerene/Wordless/releases/tag/v1.3.0) - ??/??/2019

### 🎉 New Features
- Add razdel's Russian sentenizer and word tokenizer
- Add spaCy's Lithuanian and Norwegian Bokmål word tokenizer, POS tagger, and lemmatizer
- Add spaCy's Luxembourgish word tokenizer
- Add syntok's sentence segmenter and word tokenizer
- Work Area: Add Concordancer - Generation Settings - Width Unit - Paragraph
- Work Area: Add Concordancer - Generation Settings - Sampling Method
- Work Area: Add Overview - Paragraph Length in Clause

### ✨ Improvements
- Display numbers and percentages in different columns
- Do not add borders to exported Excel workbooks due to performance issues
- Force consistent results for language detection
- Remove illegal characters when exporting tables to Excel workbooks
- Update Sacremoses's Moses tokenizer and detokenizer
- Work Area: Show hint messages when exporting tables
- Work Area: Show hint messages when sorting results

### 📌 Bug Fixes
- Fix encoding detection
- Fix file checking
- Fix lemmatization of empty tokens
- Menu: Fix Preferences - Settings - POS Tagging - Tagsets - Preview Settings - POS Tagger
- Work Area: Fix Overview - Paragraph/Sentence Length

### ❌ Removals
- Remove Sacremoses's Penn Treebank tokenizer

### ⏫ Dependency Upgrades
- Upgrade Beautiful Soup to 4.8.1
- Upgrade botok (pybo) to 0.6.18
- Upgrade cChardet to 2.1.5
- Upgrade lxml to 4.4.2
- Upgrade Matplotlib to 3.1.2
- Upgrade NetworkX to 2.4
- Upgrade NumPy to 1.17.4
- Upgrade openpyxl to 3.0.2
- Upgrade PyQt to 5.13.2
- Upgrade pytest to 5.3.0
- Upgrade Sacremoses to 0.0.35
- Upgrade SciPy to 1.3.3
- Upgrade spaCy to 2.2.3
- Upgrade syntok to 1.2.2
- Upgrade underthesea to 1.1.17
- Upgrade WordCloud to 1.6.0

## [v1.2.0](https://github.com/BLKSerene/Wordless/releases/tag/v1.2.0) - 08/27/2019

### 🎉 New Features
- Add extra-stopwords's stop words
- Add NLTK's Punkt Sentence Tokenizer for Russian
- Add NLTK's Slovenian and Tajik stop words
- Add support for XML files
- Menu: Add Preferences - Settings - Figures - Line Chart / Word Cloud / Network Graph
- Work Area: Add Collocation/Colligation - Figure Settings - Graph Type - Network Graph
- Work Area: Add Concordancer - Clause No.
- Work Area: Add Concordancer - Generation Settings - Width Unit - Sentence/Clause
- Work Area: Add Overview - Count of Clauses / Clause Length / Paragraph/Sentence/Token Length (Standard Deviation)

### ✨ Improvements
- Check file permissions when exporting tables
- Update pybo's Tibetan tokenizers, POS tagger, and lemmatizer
- Update PyThaiNLP's Thai stop words
- Update Sacremoses's tokenizers and detokenizer

### 📌 Bug Fixes
- Fix NLTK's word tokenizers
- Menu: Fix Preferences - Settings - Stop Words - Preview - Count of Stop Words
- Work Area: Fix Collocation and Colligation
- Work Area: Fix Concordancer - Export Selected/All
- Work Area: Fix Concordancer - Sort Results
- Work Area: Fix Work Area - Search Settings / Search in Results

### ⏫ Dependency Upgrades
- Upgrade Beautiful Soup to 4.8.0
- Upgrade lxml to 4.4.1
- Upgrade Matplotlib to 3.1.1
- Upgrade nagisa to 0.2.4
- Upgrade NLTK to 3.4.5
- Upgrade NumPy to 1.17.0
- Upgrade openpyxl to 2.6.3
- Upgrade pybo to 0.6.7
- Upgrade PyInstaller to 4.0.dev0+46286a1f4
- Upgrade PyQt to 5.13.0
- Upgrade PyThaiNLP to 2.0.7
- Upgrade Python to 3.7.4
- Upgrade requests to 2.22.0
- Upgrade Sacremoses to 0.0.33
- Upgrade SciPy to 1.3.1
- Upgrade spaCy to 2.1.8
- Upgrade Underthesea to 1.1.16

## [v1.1.0](https://github.com/BLKSerene/Wordless/releases/tag/v1.1.0) - 03/31/2019

### 🎉 New Features
- Menu: Add Preferences - Settings - General - Font Settings

### ✨ Improvements
- Disable mouse wheel for combo boxes and spin boxes when they are not focused
- Update spaCy's sentencizer

### 📌 Bug Fixes
- File Area: Fix Open Folder
- Fix checking for updates on startup
- Fix spaCy's sentence tokenizers and word tokenizers
- Fix Wordless's Chinese and Japanese character tokenizers
- Menu: Fix Preferences - Settings - Sentence Tokenization / Word Tokenization / Word Detokenization / POS Tagging / Lemmatization - Preview
- Work Area: Fix Concordancer - Search in Results
- Work Area: Fix error messages when loading files
- Work Area: Fix Work Area - Search Settings - Context Settings

### ⏫ Dependency Upgrades
- Upgrade lxml to 4.3.3
- Upgrade PyQt to 5.12.1
- Upgrade Sacremoses to 0.0.13
- Upgrade spaCy to 2.1.3

## [v1.0.0](https://github.com/BLKSerene/Wordless/releases/tag/v1.0.0) - 03/20/2019

### 🎉 New Features
- First release

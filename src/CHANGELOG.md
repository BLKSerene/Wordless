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
- Add hint messages when exporting tables
- Add "Paragraph Length in Clause" to "Overview"
- Add "Paragraph" to "Generation Settings -> Width Unit" in "Concordancer"
- Add razdel's Russian sentenizer and word tokenizer
- Add "Sampling Method" to "Generation Settings" in "Concordancer"
- Add spaCy's Lithuanian and Norwegian Bokmål word tokenizer, POS tagger, and lemmatizer
- Add spaCy's Luxembourgish word tokenizer
- Add syntok's sentence segmenter and word tokenizer

### ✨ Improvements
- Display numbers and percentages in different columns
- Do not add borders to exported Excel workbooks due to performance issues
- Force consistent results for language detection
- Remove illegal characters when exporting tables to Excel workbooks
- Update error messages for file checking
- Update Sacremoses's Moses tokenizer and detokenizer

### 📌 Bug Fixes
- Fix encoding detection
- Fix file checking
- Fix lemmatization of empty tokens
- Fix "Paragraph Length" and "Sentence Length" in "Overview"
- Fix "Settings → POS Tagging → Tagsets → Preview Settings → POS Tagger"

### ❌ Removals
- Remove Sacremoses's Penn Treebank tokenizer

### ⏫ Dependency Upgrades
- Upgrade Beautiful Soup to 4.8.1
- Upgrade botok (pybo) to 0.6.10
- Upgrade cChardet to 2.1.5
- Upgrade NetworkX to 2.4
- Upgrade NumPy to 1.17.4
- Upgrade openpyxl to 3.0.1
- Upgrade PyQt to 5.13.2
- Upgrade pytest to 5.2.4
- Upgrade Sacremoses to 0.0.35
- Upgrade SciPy to 1.3.2
- Upgrade spaCy to 2.2.3
- Upgrade syntok to 1.2.2
- Upgrade underthesea to 1.1.17

## [v1.2.0](https://github.com/BLKSerene/Wordless/releases/tag/v1.2.0) - 08/27/2019

### 🎉 New Features
- Add "Clause No." to "Concordancer"
- Add "Sentence" and "Clause" to "Generation Settings -> Width Unit" in "Concordancer"
- Add "Count of Clauses", "Clause Length", and "Paragraph/Sentence/Token Length (Standard Deviation)" to "Overview"
- Add extra-stopwords's stop words
- Add "Network Graph" to "Figure Settings → Graph Type" in "Collocation" and "Colligation"
- Add NLTK's Punkt Sentence Tokenizer for Russian
- Add NLTK's Slovenian and Tajik stop words
- Add "Settings → Figures → Line Chart / Word Cloud / Network Graph"
- Add support for network graphs
- Add support for XML files

### ✨ Improvements
- Check file permissions when exporting tables
- Update pybo's Tibetan tokenizers, POS tagger, and lemmatizer
- Update PyThaiNLP's Thai stop words
- Update Sacremoses's tokenizers and detokenizer

### 📌 Bug Fixes
- Fix "Collocation" and "Colligation"
- Fix "Export Selected" and "Export All" in "Concordancer"
- Fix NLTK's word tokenizers
- Fix toggling of checkboxes in "Search Settings" and "Context Settings"
- Fix "Settings → Stop Words → Preview → Count of Stop Words"
- Fix "Sort Results" in "Concordancer"

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
- Add "Settings → General → Font Settings"

### ✨ Improvements
- Disable mouse wheel event when combo boxes and spin boxes are not focused
- Update hint messages
- Update layout
- Update spaCy's sentencizer

### 📌 Bug Fixes
- Fix "Check for Updates" on startup
- Fix "Context Settings"
- Fix error messages when loading files
- Fix "Open Folder"
- Fix "Search in Results" in "Concordancer"
- Fix "Settings → Sentence Tokenization / Word Tokenization / Word Detokenization / POS Tagging / Lemmatization → Preview"
- Fix spaCy's sentence tokenizers and word tokenizers
- Fix Wordless's Chinese and Japanese character tokenizers

### ⏫ Dependency Upgrades
- Upgrade lxml to 4.3.3
- Upgrade PyQt to 5.12.1
- Upgrade Sacremoses to 0.0.13
- Upgrade spaCy to 2.1.3

## [v1.0.0](https://github.com/BLKSerene/Wordless/releases/tag/v1.0.0) - 03/20/2019

### 🎉 New Features
- First release

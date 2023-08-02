<!--
# Wordless: Documentation - English
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

<div align="center"><h1>📖 Documentation</h1></div>

<span id="doc"></span>
## Table of Contents
- [1 Main Window](#doc-1)
- [2 File Area](#doc-2)
- [3 Work Area](#doc-3)
  - [3.1 Profiler](#doc-3-1)
  - [3.2 Concordancer](#doc-3-2)
  - [3.3 Parallel Concordancer](#doc-3-3)
  - [3.4 Dependency Parser](#doc-3-4)
  - [3.5 Wordlist Generator](#doc-3-5)
  - [3.6 N-gram Generator](#doc-3-6)
  - [3.7 Collocation Extractor](#doc-3-7)
  - [3.8 Colligation Extractor](#doc-3-8)
  - [3.9 Keyword Extractor](#doc-3-9)
- [4 Appendixes](#doc-4)
  - [4.1 Supported Languages](#doc-4-1)
  - [4.2 Supported File Types](#doc-4-2)
  - [4.3 Supported File Encodings](#doc-4-3)
  - [4.4 Supported Measures](#doc-4-4)
    - [4.4.1 Measures of Readability](#doc-4-4-1)
    - [4.4.2 Measures of Dispersion & Adjusted Frequency](#doc-4-4-2)
    - [4.4.3 Tests of Statistical Significance, Measures of Bayes Factor, & Measures of Effect Size](#doc-4-4-3)
- [5 References](#doc-5)

<span id="doc-1"></span>
## [1 Main Window](#doc)
The main window of *Wordless* is divided into several sections:

- **1.1 Menu Bar**<br>
  The *Menu Bar* resides at the top of the main window.

- **1.2 Work Area**<br>
  The *Work Area* resides at the upper half of the main window, just below *Menu Bar*.

  The *Work Area* is further divided into the *Results Area* on the left side and the *Settings Area* on the right side. You can click on the tabs to toggle between different modules.

- **1.3 File Area**<br>
  The *File Area* resides at the lower half of the main window, just above *Status Bar*.

- **1.4 Status Bar**<br>
  The *Status Bar* resides at the bottom of the main window.

  You can show/hide the *Status Bar* by checking/unchecking **Menu → Preferences → Show Status Bar**

You can modify the global scaling factor and font settings of the user interface via **Menu → Preferences → General → User Interface Settings**.

<span id="doc-2"></span>
## [2 File Area](#doc)
In most cases, the first thing to do in *Wordless* is open and select your files to be processed via **Menu → File → Open Files/Folder**.

Files are loaded, cached and selected automatically after being added to the *File Table*. **Only selected files will be processed by *Wordless***. You can drag and drop files around the *File Table* to change their orders, which would be reflected in the results.

By default, *Wordless* tries to detect the encoding and language settings of all files for you, you should double check and make sure that the settings of each and every file are correct. If you prefer changing file settings manually, you could uncheck **Auto-detect encodings** and/or **Auto-detect languages** in the *Open Files* dialog. The default file settings could be modified via **Menu → Preferences → Settings → Files → Default Settings**.

- **2.1 Open Files**<br>
  Add one single file or multiple files to the *File Table*.

  \* You can use the **Ctrl** key (**Command** key on macOS) and/or the **Shift** key to select multiple files.

- **2.2 Open Folder**<br>
  Add all files in the folder to the *File Table*.

  By default, all files in the chosen folder and the sub-folders of the chosen folder (and sub-folders of sub-folders, and so on) are added to the *File Table*. If you do not want to add files in sub-folders to the *File Table*, you could uncheck **Include files in sub-folders** in the *Open Files* dialog.

- **2.3 Reopen Closed Files**<br>
  Add file(s) that are closed the last time back to the *File Table*.

  \* The history of all closed files will be erased upon exit of *Wordless*.

- **2.4 Select All**<br>
  Select all files in the *File Table*.

- **2.5 Deselect All**<br>
  Deselect all files in the *File Table*.

- **2.6 Invert Selection**<br>
  Select files that are not currently selected and deselect files that are currently selected in the *File Table*.

- **2.7 Close Selected**<br>
  Remove files that are currently selected from the *File Table*.

- **2.8 Close All**<br>
  Remove all files from the *File Table*.

<span id="doc-3"></span>
## [3 Work Area](#doc)

<span id="doc-3-1"></span>
### [3.1 Profiler](#doc)
**Note:** Renamed from **Overview** to **Profiler** in *Wordless* 2.2.0

In *Profiler*, you can check and compare general linguistic features of different files.

All statistics are grouped into 5 tables for better readability: Readability, Counts, Type-token Ratios, Lengths, Length Breakdown.

- **3.1.1 Readability**<br>
  Readability statistics of each file calculated according to the different readability tests used. See section [4.4.1 Measures of Readability](#doc-4-4-1) for more details.

- **3.1.2 Counts**<br>
  - **3.1.2.1 Count of Paragraphs**<br>
    The number of paragraphs in each file. Each line in the file is counted as one paragraph. Blank lines and lines containing only spaces, tabs and other invisible characters are not counted.

  - **3.1.2.2 Count of Paragraphs %**<br>
    The percentage of the number of paragraphs in each file out of the total number of paragraphs in all files.

  - **3.1.2.3 Count of Sentences**<br>
    The number of sentences in each file. *Wordless* automatically applies the built-in sentence tokenizer according to the language of each file to calculate the number of sentences in each file. You can modify sentence tokenizer settings via **Menu → Preferences → Settings → Sentence Tokenization → Sentence Tokenizer Settings**.

  - **3.1.2.4 Count of Sentences %**<br>
    The percentage of the number of sentences in each file out of the total number of sentences in all files.

  - **3.1.2.5 Count of Sentence Segments**<br>
    The number of sentence segments in each file. Each part of sentence ending with one or more consecutive [terminal punctuation marks](https://en.wikipedia.org/wiki/Terminal_punctuation) (as per the [Unicode Standard](https://en.wikipedia.org/wiki/Unicode)) is counted as one sentence segment. See [here](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=[:Terminal_Punctuation=Yes:]) for the full list of terminal punctuation marks.

  - **3.1.2.6 Count of Sentence Segments %**<br>
    The percentage of the number of sentence segments in each file out of the total number of sentence segments in all files.

  - **3.1.2.7 Count of Tokens**<br>
    The number of tokens in each file. *Wordless* automatically applies the built-in word tokenizer according to the language of each file to calculate the number of tokens in each file. You can modify word tokenizer settings via **Menu → Preferences → Settings → Word Tokenization → Word Tokenizer Settings**.

    You can specify what should be counted as a "token" via **Token Settings** in the *Settings Area*

  - **3.1.2.8 Count of Tokens %**<br>
    The percentage of the number of tokens in each file out of the total number of tokens in all files.

  - **3.1.2.9 Count of Types**<br>
    The number of token types in each file.

  - **3.1.2.10 Count of Types %**<br>
    The percentage of the number of token types in each file out of the total number of token types in all files.

  - **3.1.2.11 Count of Syllables**<br>
    The number of syllables in each files. *Wordless* automatically applies the built-in syllable tokenizer according to the language of each file to calculate the number of syllable in each file. You can modify syllable tokenizer settings via **Menu → Preferences → Settings → Syllable Tokenization → Syllable Tokenizer Settings**.

  - **3.1.2.12 Count of Syllables %**<br>
    The percentage of the number of syllables in each file out of the total number of syllable in all files.

  - **3.1.2.13 Count of Characters**<br>
    The number of single characters in each file. Spaces, tabs and all other invisible characters are not counted.

  - **3.1.2.14 Count of Characters %**<br>
    The percentage of the number of characters in each file out of the total number of characters in all files.

- **3.1.3 Type-token Ratios**<br>
  - **3.1.3.1 Type-token Ratio**<br>
    The number of token types divided by the number of tokens in each file.

  - **3.1.3.2 Type-token Ratio (Standardized)**<br>
    Standardized type-token ratio. Each file is divided into several sub-sections with each one consisting of 1000 tokens by default and type-token ratios are calculated for each part. The standardized type-token ratio of each file is then averaged out with weights (number of tokens in each sub-section) over all sub-sections. You can change the number of tokens in each sub-section via **Menu → Preferences → Settings → Tables → Profiler → Number of tokens in each section when calculating standardized type-token ratio**.

- **3.1.4 Lengths**<br>
  - **3.1.4.1 Paragraph Length in Sentences / Sentence Segments / Tokens (Mean)**<br>
    The average value of paragraph lengths expressed in sentences / sentence segments / tokens.

  - **3.1.4.2 Paragraph Length in Sentences / Sentence Segments / Tokens (Standard Deviation)**<br>
    The standard deviation of paragraph lengths expressed in sentences / sentence segments / tokens.

  - **3.1.4.3 Paragraph Length in Sentences / Sentence Segments / Tokens (Variance)**<br>
    The variance of paragraph lengths expressed in sentences / sentence segments / tokens.

  - **3.1.4.4 Paragraph Length in Sentences / Sentence Segments / Tokens (Minimum)**<br>
    The minimum of paragraph lengths expressed in sentences / sentence segments / tokens.

  - **3.1.4.5 Paragraph Length in Sentences / Sentence Segments / Tokens (25th Percentile)**<br>
    The 25th percentile of paragraph lengths expressed in sentences / sentence segments / tokens.

  - **3.1.4.6 Paragraph Length in Sentences / Sentence Segments / Tokens (Median)**<br>
    The median of paragraph lengths expressed in sentences / sentence segments / tokens.

  - **3.1.4.7 Paragraph Length in Sentences / Sentence Segments / Tokens (75th Percentile)**<br>
    The 75th percentile of paragraph lengths expressed in sentences / sentence segments / tokens.

  - **3.1.4.8 Paragraph Length in Sentences / Sentence Segments / Tokens (Maximum)**<br>
    The maximum of paragraph lengths expressed in sentences / sentence segments / tokens.

  - **3.1.4.9 Paragraph Length in Sentences / Sentence Segments / Tokens (Range)**<br>
    The range of paragraph lengths expressed in sentences / sentence segments / tokens.

  - **3.1.4.10 Paragraph Length in Sentences / Sentence Segments / Tokens (Interquartile Range)**<br>
    The interquartile range of paragraph lengths expressed in sentences / sentence segments / tokens.

  - **3.1.4.11 Paragraph Length in Sentences / Sentence Segments / Tokens (Modes)**<br>
    The mode(s) of paragraph lengths expressed in sentences / sentence segments / tokens.

  - **3.1.4.12 Sentence / Sentence Segment Length in Tokens (Mean)**<br>
    The average value of sentence / sentence segment lengths expressed in tokens.

  - **3.1.4.13 Sentence / Sentence Segment Length in Tokens (Standard Deviation)**<br>
    The standard deviation of sentence / sentence segment lengths expressed in tokens.

  - **3.1.4.14 Sentence / Sentence Segment Length in Tokens (Variance)**<br>
    The variance of sentence / sentence segment lengths expressed in tokens.

  - **3.1.4.15 Sentence / Sentence Segment Length in Tokens (Minimum)**<br>
    The minimum of sentence / sentence segment lengths expressed in tokens.

  - **3.1.4.16 Sentence / Sentence Segment Length in Tokens (25th Percentile)**<br>
    The 25th percentile of sentence / sentence segment lengths expressed in tokens.

  - **3.1.4.17 Sentence / Sentence Segment Length in Tokens (Median)**<br>
    The median of sentence / sentence segment lengths expressed in tokens.

  - **3.1.4.18 Sentence / Sentence Segment Length in Tokens (75th Percentile)**<br>
    The 75th percentile of sentence / sentence segment lengths expressed in tokens.

  - **3.1.4.19 Sentence / Sentence Segment Length in Tokens (Maximum)**<br>
    The maximum of sentence / sentence segment lengths expressed in tokens.

  - **3.1.4.20 Sentence / Sentence Segment Length in Tokens (Range)**<br>
    The range of sentence / sentence segment lengths expressed in tokens.

  - **3.1.4.21 Sentence / Sentence Segment Length in Tokens (Interquartile Range)**<br>
    The interquartile range of sentence / sentence segment lengths expressed in tokens.

  - **3.1.4.22 Sentence / Sentence Segment Length in Tokens (Modes)**<br>
    The mode(s) of sentence / sentence segment lengths expressed in tokens.

  - **3.1.4.23 Token/Type Length in Syllables/Characters (Mean)**<br>
    The average value of token / token type lengths expressed in syllables/characters.

  - **3.1.4.24 Token/Type Length in Syllables/Characters (Standard Deviation)**<br>
    The standard deviation of token / token type lengths expressed in syllables/characters.

  - **3.1.4.25 Token/Type Length in Syllables/Characters (Variance)**<br>
    The variance of token / token type lengths expressed in syllables/characters.

  - **3.1.4.26 Token/Type Length in Syllables/Characters (Minimum)**<br>
    The minimum of token / token type lengths expressed in syllables/characters.

  - **3.1.4.27 Token/Type Length in Syllables/Characters (25th Percentile)**<br>
    The 25th percentile of token / token type lengths expressed in syllables/characters.

  - **3.1.4.28 Token/Type Length in Syllables/Characters (Median)**<br>
    The median of token / token type lengths expressed in syllables/characters.

  - **3.1.4.29 Token/Type Length in Syllables/Characters (75th Percentile)**<br>
    The 75th percentile of token / token type lengths expressed in syllables/characters.

  - **3.1.4.30 Token/Type Length in Syllables/Characters (Maximum)**<br>
    The maximum of token / token type lengths expressed in syllables/characters.

  - **3.1.4.31 Token/Type Length in Syllables/Characters (Range)**<br>
    The range of token / token type lengths expressed in syllables/characters.

  - **3.1.4.32 Token/Type Length in Syllables/Characters (Interquartile Range)**<br>
    The interquartile range of token / token type lengths expressed in syllables/characters.

  - **3.1.4.33 Token/Type Length in Syllables/Characters (Modes)**<br>
    The mode(s) of token / token type lengths expressed in syllables/characters.

  - **3.1.4.34 Syllable Length in Characters (Mean)**<br>
    The average value of syllable lengths expressed in characters.

  - **3.1.4.35 Syllable Length in Characters (Standard Deviation)**<br>
    The standard deviation of syllable lengths expressed in characters.

  - **3.1.4.36 Syllable Length in Characters (Variance)**<br>
    The variance of syllable lengths expressed in characters.

  - **3.1.4.37 Syllable Length in Characters (Minimum)**<br>
    The minimum of syllable lengths expressed in characters.

  - **3.1.4.38 Syllable Length in Characters (25th Percentile)**<br>
    The 25th percentile of syllable lengths expressed in characters.

  - **3.1.4.39 Syllable Length in Characters (Median)**<br>
    The median of syllable lengths expressed in characters.

  - **3.1.4.40 Syllable Length in Characters (75th Percentile)**<br>
    The 75th percentile of syllable lengths expressed in characters.

  - **3.1.4.41 Syllable Length in Characters (Maximum)**<br>
    The maximum of syllable lengths expressed in characters.

  - **3.1.4.42 Syllable Length in Characters (Range)**<br>
    The range of syllable lengths expressed in characters.

  - **3.1.4.43 Syllable Length in Characters (Interquartile Range)**<br>
    The interquartile range of Syllable lengths expressed in characters.

  - **3.1.4.44 Syllable Length in Characters (Modes)**<br>
    The mode(s) of syllable lengths expressed in characters.

- **3.1.5 Length Breakdown**<br>
  - **3.1.5.1 Count of n-token-long Sentences / Sentence Segments**<br>
    The number of n-token-long sentences / sentence segments, where n = 1, 2, 3, etc.

  - **3.1.5.2 Count of n-token-long Sentences / Sentence Segments %**<br>
    The percentage of the number of n-token-long sentences / sentence segments in each file out of the total number of n-token-long sentences / sentence segments in all files, where n = 1, 2, 3, etc.

  - **3.1.5.3 Count of n-syllable-long Tokens**<br>
    The number of n-syllable-long tokens, where n = 1, 2, 3, etc.

  - **3.1.5.4 Count of n-syllable-long Tokens %**<br>
    The percentage of the number of n-syllable-long tokens in each file out of the total number of n-syllable-long tokens in all files, where n = 1, 2, 3, etc.

  - **3.1.5.5 Count of n-character-long Tokens**<br>
    The number of n-character-long tokens, where n = 1, 2, 3, etc.

  - **3.1.5.6 Count of n-character-long Tokens %**<br>
    The percentage of the number of n-character-long tokens in each file out of the total number of n-character-long tokens in all files, where n = 1, 2, 3, etc.

<span id="doc-3-2"></span>
### [3.2 Concordancer](#doc)
In *Concordancer*, you can search for tokens in different files and generate concordance lines. You can adjust settings for data generation via **Generation Settings**.

After the concordance lines are generated and displayed in the table, you can sort the results by clicking **Sort Results** or search in results by clicking **Search in Results**, both buttons residing at the right corner of the *Results Area*.

You can generate concordance plots for all search terms. You can modify the settings for the generated figure via **Figure Settings**.

- **3.2.1 Left**<br>
  The context before each search term, which displays 10 tokens left to the **Node** by default. You can change this behavior via **Generation Settings**.

- **3.2.2 Node**<br>
  The search term(s) specified in **Search Settings → Search Term**.

- **3.2.3 Right**<br>
  The context after each search term, which displays 10 tokens right to the **Node** by default. You can change this behavior via **Generation Settings**.

- **3.2.4 Sentiment**<br>
  The sentiment of the **Node** combined with its context (**Left** and **Right**).

- **3.2.5 Token No.**<br>
  The position of the first token of **Node** in each file.

- **3.2.6 Token No. %**<br>
  The percentage of the position of the first token of **Node** in each file.

- **3.2.7 Sentence Segment No.**<br>
  The position of the sentence segment where the **Node** is found in each file.

- **3.2.8 Sentence Segment No. %**<br>
  The percentage of the position of the sentence segment where the **Node** is found in each file.

- **3.2.9 Sentence No.**<br>
  The position of the sentence where the **Node** is found in each file.

- **3.2.10 Sentence No. %**<br>
  The percentage of the position of the sentence where the **Node** is found in each file.

- **3.2.11 Paragraph No.**<br>
  The position of the paragraph where the **Node** is found in each file.

- **3.2.12 Paragraph No. %**<br>
  The percentage of the position of the paragraph where the **Node** is found in each file.

- **3.2.13 File**<br>
  The name of the file where the **Node** is found.

<span id="doc-3-3"></span>
### [3.3 Parallel Concordancer](#doc)
**Notes:**
1. Added in *Wordless* 2.0.0
2. Renamed from **Concordancer (Parallel Mode)** to **Parallel Concordancer** in *Wordless* 2.2.0

In *Parallel Concordancer*, you can search for tokens in parallel corpora and generate parallel concordance lines. You may leave **Search Settings → Search Term** blank so as to search for instances of additions and deletions.

After the parallel concordance lines are generated and displayed in the table, you can search in results by clicking **Search in Results** which resides at the right corner of the *Results Area*.

- **3.3.1 Parallel Unit No.**<br>
  The position of the alignment unit (paragraph) where the the search term is found.

- **3.3.2 Parallel Unit No. %**<br>
  The percentage of the position of the alignment unit (paragraph) where the the search term is found.

- **3.3.3 Parallel Units**<br>
  The parallel unit (paragraph) where the search term is found in each file.

<span id="doc-3-5"></span>
### [3.4 Dependency Parser](#doc)
**Note:** Added in *Wordless* 3.0.0

In *Dependency Parser*, you can search for all dependency relations associated with different tokens and calculate their dependency lengths (distances).

You can search in the results for the part that might be of interest to you by clicking **Search in Results** which resides at the right corner of the *Results Area*.

You can select lines in the *Results Area* and then click *Generate Figure* to show dependency graphs for all selected sentences. You can modify the settings for the generated figure via **Figure Settings** and decide how the figures should be displayed.

- **3.4.1 Head**<br>
  The token functioning as the head in the dependency structure.

- **3.4.2 Dependent**<br>
  The token functioning as the dependent in the dependency structure.

- **3.4.3 Dependency Length**<br>
  The dependency length (distance) between the head and dependent in the dependency structure. The dependency length is positive when the head follows the dependent and would be negative if the head precedes the dependent.

- **3.4.4 Dependency Length (Absolute)**<br>
  The absolute value of the dependency length (distance) between the head and dependent in the dependency structure. The absolute dependency length is always positive.

- **3.4.5 Sentence**<br>
  The sentence where the dependency structure is found.

- **3.4.6 Sentence No.**<br>
  The position of the sentence where the dependency structure is found.

- **3.4.7 Sentence No. %**<br>
  The percentage of the position of the sentence where the dependency structure is found.

- **3.4.8 File**<br>
  The name of the file where the dependency structure is found.

<span id="doc-3-5"></span>
### [3.5 Wordlist Generator](#doc)
**Note:** Renamed from **Wordlist** to **Wordlist Generator** in *Wordless* 2.2.0

In *Wordlist Generator*, you can generate wordlists for different files and calculate the raw frequency, relative frequency, dispersion and adjusted frequency for each token. You can disable the calculation of dispersion and/or adjusted frequency by setting **Generation Settings → Measures of Dispersion / Measure of Adjusted Frequency** to **None**.

You can further filter the results as you see fit by clicking **Filter Results** or search in the results for the part that might be of interest to you by clicking **Search in Results**, both buttons residing at the right corner of the *Results Area*.

You can generate line charts or word clouds for wordlists using any statistics. You can modify the settings for the generated figure via **Figure Settings**.

- **3.5.1 Rank**<br>
  The rank of the token sorted by its frequency in the first file in descending order (by default). You can sort the results again by clicking the column headers. You can use continuous numbering after tied ranks (eg. 1/1/1/2/2/3 instead of 1/1/1/4/4/6) by checking **Menu → Preferences → Settings → Tables → Rank Settings → Continue numbering after ties**.

- **3.5.2 Token**<br>
  You can specify what should be counted as a "token" via **Token Settings**.

- **3.5.3 Syllabification**<br>
  The syllabified form of each token.

  If the token happens to exist in the vocabulary of multiple languages, all syllabified forms with their applicable languages will be listed.

  If there is no syllable tokenization support for the language where the token is found, "No language support" is displayed instead. To check which languages have syllable tokenization support, please refer to section [4.1 Supported Languages](#doc-4-1).

- **3.5.4 Frequency**<br>
  The number of occurrences of the token in each file.

- **3.5.5 Dispersion**<br>
  The dispersion of the token in each file. You can change the measure of dispersion used via **Generation Settings → Measure of Dispersion**. See section [4.4.2 Measures of Dispersion & Adjusted Frequency](#doc-4-4-2) for more details.

- **3.5.6 Adjusted Frequency**<br>
  The adjusted frequency of the token in each file. You can change the measure of adjusted frequency used via **Generation Settings → Measure of Adjusted Frequency**. See section [4.4.2 Measures of Dispersion & Adjusted Frequency](#doc-4-4-2) for more details.

- **3.5.7 Number of Files Found**<br>
  The number of files in which the token appears at least once.

- **3.5.8 Number of Files Found %**<br>
  The percentage of the number of files in which the token appears at least once out of the total number of files that are cureently selected.

<span id="doc-3-6"></span>
### [3.6 N-gram Generator](#doc)
**Note:** Renamed from **N-gram** to **N-gram Generator** in *Wordless* 2.2.0

In *N-gram Generator*, you can search for n-grams (consecutive tokens) or skip-grams (non-consecutive tokens) in different files, count and compute the raw frequency and relative frequency of each n-gram/skip-gram, and calculate the dispersion and adjusted frequency for each n-gram/skip-gram using different measures. You can adjust the settings for the generated results via **Generation Settings**.  You can disable the calculation of dispersion and/or adjusted frequency by setting **Generation Settings → Measures of Dispersion / Measure of Adjusted Frequency** to **None**. To allow skip-grams in the results, check **Generation Settings → Allow skipped tokens** and modify the settings. You can also set constraints on the position of search terms in all n-grams via **Search Settings → Search Term Position**.

You can generate line charts or word clouds for n-grams using any statistics. You can modify the settings for the generated figure via **Figure Settings**.

You can further filter the results as you see fit by clicking **Filter Results** or search in the results for the part that might be of interest to you by clicking **Search in Results**, both buttons residing at the right corner of the *Results Area*.

- **3.6.1 Rank**<br>
  The rank of the n-gram sorted by its frequency in the first file in descending order (by default). You can sort the results again by clicking the column headers. You can use continuous numbering after tied ranks (eg. 1/1/1/2/2/3 instead of 1/1/1/4/4/6) by checking **Menu → Preferences → Settings → Tables → Rank Settings → Continue numbering after ties**.

- **3.6.2 N-gram**<br>
  You can specify what should be counted as a "n-gram" via **Token Settings**.

- **3.6.3 Frequency**<br>
  The number of occurrences of the n-gram in each file.

- **3.6.4 Dispersion**<br>
  The dispersion of the n-gram in each file. You can change the measure of dispersion used via **Generation Settings → Measure of Dispersion**. See section [4.4.2 Measures of Dispersion & Adjusted Frequency](#doc-4-4-2) for more details.

- **3.6.5 Adjusted Frequency**<br>
  The adjusted frequency of the n-gram in each file. You can change the measure of adjusted frequency used via **Generation Settings → Measure of Adjusted Frequency**. See section [4.4.2 Measures of Dispersion & Adjusted Frequency](#doc-4-4-2) for more details.

- **3.6.6 Number of Files Found**<br>
  The number of files in which the n-gram appears at least once.

- **3.6.7 Number of Files Found %**<br>
  The percentage of the number of files in which the n-gram appears at least once out of the total number of files that are currently selected.

<span id="doc-3-7"></span>
### [3.7 Collocation Extractor](#doc)
**Note:** Renamed from **Collocation** to **Collocation Extractor** in *Wordless* 2.2.0

In *Collocation Extractor*, you can search for patterns of collocation (tokens that co-occur more often than would be expected by chance) within a given collocational window (from 5 words to the left to 5 words to the right by default), conduct different tests of statistical significance on each pair of collocates and calculate the Bayes factor and effect size for each pair using different measures. You can adjust the settings for the generated results via **Generation Settings**. You can disable the calculation of statistical significance and/or Bayes factor and/or effect size by setting **Generation Settings → Test of Statistical Significance / Measures of Bayes Factor / Measure of Effect Size** to **None**.

You can generate line charts, word clouds, and network graphs for patterns of collocation using any statistics. You can modify the settings for the generated figure via **Figure Settings**.

You can further filter the results as you see fit by clicking **Filter Results** or search in the results for the part that might be of interest to you by clicking **Search in Results**, both buttons residing at the right corner of the *Results Area*.

- **3.7.1 Rank**<br>
  The rank of the collocating token sorted by the p-value of the significance test conducted on the node and the collocating token in the first file in ascending order (by default). You can sort the results again by clicking the column headers. You can use continuous numbering after tied ranks (eg. 1/1/1/2/2/3 instead of 1/1/1/4/4/6) by checking **Menu → Preferences → Settings → Tables → Rank Settings → Continue numbering after ties**.

- **3.7.2 Node**<br>
  The search term. You can specify what should be counted as a "token" via **Token Settings**.

- **3.7.3 Collocate**<br>
  The collocating token. You can specify what should be counted as a "token" via **Token Settings**.

- **3.7.4 Ln, ..., L3, L2, L1, R1, R2, R3, ..., Rn**<br>
  The number of co-occurrences of the node and the collocating token with the collocating token at the given position in each file.

- **3.7.5 Frequency**<br>
  The total number of co-occurrences of the node and the collocating token with the collocating token at all possible positions in each file.

- **3.7.6 Test Statistic**<br>
  The test statistic of the significance test conducted on the node and the collocating token in each file. You can change the test of statistical significance used via **Generation Settings → Test of Statistical Significance**. See section [4.4.3 Tests of Statistical Significance, Measures of Bayes Factor, & Measures of Effect Size](#doc-4-4-3) for more details.

  Please note that test statistic is not available for some tests of statistical significance.

- **3.7.7 p-value**<br>
  The p-value of the significance test conducted on the node and the collocating token in each file. You can change the test of statistical significance used via **Generation Settings → Test of Statistical Significance**. See section [4.4.3 Tests of Statistical Significance, Measures of Bayes Factor, & Measures of Effect Size](#doc-4-4-3) for more details.

- **3.7.8 Bayes Factor**<br>
  The Bayes factor the node and the collocating token in each file. You can change the measure of Bayes factor used via **Generation Settings → Measure of Bayes Factor**. See section [4.4.3 Tests of Statistical Significance, Measures of Bayes Factor, & Measures of Effect Size](#doc-4-4-3) for more details.

- **3.7.9 Effect Size**<br>
  The effect size of the node and the collocating token in each file. You can change the measure of effect size used via **Generation Settings → Measure of Effect Size**. See section [4.4.3 Tests of Statistical Significance, Measures of Bayes Factor, & Measures of Effect Size](#doc-4-4-3) for more details.

- **3.7.10 Number of Files Found**<br>
  The number of files in which the node and the collocating token co-occur at least once.

- **3.7.11 Number of Files Found %**<br>
  The percentage of the number of files in which the node and the collocating token co-occur at least once out of the total number of files that are currently selected.

<span id="doc-3-8"></span>
### [3.8 Colligation Extractor](#doc)
**Note:** Renamed from **Colligation** to **Colligation Extractor** in *Wordless* 2.2.0

In *Colligation Extractor*, you can search for patterns of colligation (parts of speech that co-occur more often than would be expected by chance) within a given collocational window (from 5 words to the left to 5 words to the right by default), conduct different tests of statistical significance on each pair of parts of speech and calculate the Bayes factor and effect size for each pair using different measures. You can adjust the settings for the generated data via **Generation Settings**. You can disable the calculation of statistical significance and/or Bayes factor and/or effect size by setting **Generation Settings → Test of Statistical Significance / Measures of Bayes Factor / Measure of Effect Size** to **None**.

*Wordless* will automatically apply its built-in part-of-speech tagger on every file that are not part-of-speech-tagged already according to the language of each file. If part-of-speech tagging is not supported for the given languages, the user should provide a file that has already been part-of-speech-tagged and make sure that the correct **Text Type** has been set on each file.

You can generate line charts or word clouds for patterns of colligation using any statistics. You can modify the settings for the generated figure via **Figure Settings**.

You can further filter the results as you see fit by clicking **Filter Results** or search in the results for the part that might be of interest to you by clicking **Search in Results**, both buttons residing at the right corner of the *Results Area*.

- **3.8.1 Rank**<br>
  The rank of the collocating part of speech sorted by the p-value of the significance test conducted on the node and the collocating part of speech in the first file in ascending order (by default). You can sort the results again by clicking the column headers. You can use continuous numbering after tied ranks (eg. 1/1/1/2/2/3 instead of 1/1/1/4/4/6) by checking **Menu → Preferences → Settings → Tables → Rank Settings → Continue numbering after ties**.

- **3.8.2 Node**<br>
  The search term. You can specify what should be counted as a "token" via **Token Settings**.

- **3.8.3 Collocate**<br>
  The collocating part of speech. You can specify what should be counted as a "token" via **Token Settings**.

- **3.8.4 Ln, ..., L3, L2, L1, R1, R2, R3, ..., Rn**<br>
  The number of co-occurrences of the node and the collocating part of speech with the collocating part of speech at the given position in each file.

- **3.8.5 Frequency**<br>
  The total number of co-occurrences of the node and the collocating part of speech with the collocating part of speech at all possible positions in each file.

- **3.8.6 Test Statistic**<br>
  The test statistic of the significance test conducted on the node and the collocating part of speech in each file. You can change the test of statistical significance used via **Generation Settings → Test of Statistical Significance**. See section [4.4.3 Tests of Statistical Significance, Measures of Bayes Factor, & Measures of Effect Size](#doc-4-4-3) for more details.

  Please note that test statistic is not available for some tests of statistical significance.

- **3.8.7 p-value**<br>
  The p-value of the significance test conducted on the node and the collocating part of speech in each file. You can change the test of statistical significance used via **Generation Settings → Test of Statistical Significance**. See section [4.4.3 Tests of Statistical Significance, Measures of Bayes Factor, & Measures of Effect Size](#doc-4-4-3) for more details.

- **3.8.8 Bayes Factor**<br>
  The Bayes factor of the node and the collocating part of speech in each file. You can change the measure of Bayes factor used via **Generation Settings → Measure of Bayes Factor**. See section [4.4.3 Tests of Statistical Significance, Measures of Bayes Factor, & Measures of Effect Size](#doc-4-4-3) for more details.
  
- **3.8.9 Effect Size**<br>
  The effect size of the node and the collocating part of speech in each file. You can change the measure of effect size used via **Generation Settings → Measure of Effect Size**. See section [4.4.3 Tests of Statistical Significance, Measures of Bayes Factor, & Measures of Effect Size](#doc-4-4-3) for more details.

- **3.8.10 Number of Files Found**<br>
  The number of files in which the node and the collocating part of speech co-occur at least once.

- **3.8.11 Number of Files Found %**<br>
  The percentage of the number of files in which the node and the collocating part of speech co-occur at least once out of the total number of file that are currently selected.

<span id="doc-3-9"></span>
### [3.9 Keyword Extractor](#doc)
**Note:** This module was originally named **Keyword** before *Wordless* 2.2

In *Keyword Extractor*, you can search for candidates of potential keywords (tokens that have far more or far less frequency in the observed file than in the reference file) in different files given a reference corpus, conduct different tests of statistical significance on each keyword and calculate the Bayes factor and effect size for each keyword using different measures. You can adjust the settings for the generated data via **Generation Settings**. You can disable the calculation of statistical significance and/or Bayes factor and/or effect size by setting **Generation Settings → Test of Statistical Significance / Measures of Bayes Factor / Measure of Effect Size** to **None**.

You can generate line charts or word clouds for keywords using any statistics. You can modify the settings for the generated figure via **Figure Settings**.

You can further filter the results as you see fit by clicking **Filter Results** or search in the results for the part that might be of interest to you by clicking **Search in Results**, both buttons residing at the right corner of the *Results Area*.

- **3.9.1 Rank**<br>
  The rank of the keyword sorted by the p-value of the significance test conducted on the keyword in the first file in ascending order (by default). You can sort the results again by clicking the column headers. You can use continuous numbering after tied ranks (eg. 1/1/1/2/2/3 instead of 1/1/1/4/4/6) by checking **Menu → Preferences → Settings → Tables → Rank Settings → Continue numbering after ties**.

- **3.9.2 Keyword**<br>
  The candidates of potential keywords. You can specify what should be counted as a "token" via **Token Settings**.

- **3.9.3 Frequency (in Reference File)**<br>
  The number of co-occurrences of the keywords in the reference file.

- **3.9.4 Frequency (in Observed Files)**<br>
  The number of co-occurrences of the keywords in each observed file.

- **3.9.5 Test Statistic**<br>
  The test statistic of the significance test conducted on the keyword in each file. You can change the test of statistical significance used via **Generation Settings → Test of Statistical Significance**. See section [4.4.3 Tests of Statistical Significance, Measures of Bayes Factor, & Measures of Effect Size](#doc-4-4-3) for more details.

  Please note that test statistic is not available for some tests of statistical significance.

- **3.9.6 p-value**<br>
  The p-value of the significance test conducted on the keyword in each file. You can change the test of statistical significance used via **Generation Settings → Test of Statistical Significance**. See section [4.4.3 Tests of Statistical Significance, Measures of Bayes Factor, & Measures of Effect Size](#doc-4-4-3) for more details.

- **3.9.7 Bayes Factor**<br>
  The Bayes factor of the keyword in each file. You can change the measure of Bayes factor used via **Generation Settings → Measure of Bayes Factor**. See section [4.4.3 Tests of Statistical Significance, Measures of Bayes Factor, & Measures of Effect Size](#doc-4-4-3) for more details.

- **3.9.8 Effect Size**<br>
  The effect size of on the keyword in each file. You can change the measure of effect size used via **Generation Settings → Measure of Effect Size**. See section [4.4.3 Tests of Statistical Significance, Measures of Bayes Factor, & Measures of Effect Size](#doc-4-4-3) for more details.

- **3.9.9 Number of Files Found**<br>
  The number of files in which the keyword appears at least once.

- **3.9.10 Number of Files Found %**<br>
  The percentage of the number of files in which the keyword appears at least once out of the total number of files that are currently selected.

<span id="doc-4"></span>
## [4 Appendixes](#doc)

<span id="doc-4-1"></span>
### [4.1 Supported Languages](#doc)

Language|Sentence Tokenization|Word Tokenization|Syllable Tokenization|Part-of-speech Tagging|Lemmatization|Stop Word List|Dependency Parsing
:------:|:-------------------:|:---------------:|:-------------------:|:--------------------:|:-----------:|:------------:|:----------------:
Afrikaans               |⭕️ |✔|✔|✖️|✖️|✔|✖️
Albanian                |⭕️ |✔|✔|✖️|✔|✖️|✖️
Amharic                 |⭕️ |✔|✖️|✖️|✖️|✖️|✖️
Arabic                  |⭕️ |✔|✖️|✖️|✖️|✔|✖️
Armenian                |⭕️ |✔|✖️|✖️|✔|✔|✖️
Assamese                |⭕️ |✔|✖️|✖️|✖️|✖️|✖️
Asturian                |⭕️ |⭕️ |✖️|✖️|✔|✖️|✖️
Azerbaijani             |⭕️ |✔|✖️|✖️|✖️|✔|✖️
Basque                  |⭕️ |✔|✖️|✖️|✖️|✔|✖️
Belarusian              |⭕️ |⭕️ |✔|✖️|✖️|✖️|✖️
Bengali                 |⭕️ |✔|✖️|✖️|✔|✔|✖️
Breton                  |⭕️ |⭕️ |✖️|✖️|✖️|✔|✖️
Bulgarian               |⭕️ |✔|✔|✖️|✔|✔|✖️
Burmese                 |⭕️ |⭕️ |✖️|✖️|✖️|✔|✖️
Catalan                 |✔|✔|✔|✔|✔|✔|✔
Chinese (Simplified)    |✔|✔|✖️|✔|✖️|✔|✔
Chinese (Traditional)   |✔|✔|✖️|✔|✖️|✔|✔
Croatian                |✔|✔|✔|✔|✔|✔|✔
Czech                   |✔|✔|✔|✖️|✔|✔|✖️
Danish                  |✔|✔|✔|✔|✔|✔|✔
Dutch                   |✔|✔|✔|✔|✔|✔|✔
English (Middle)        |⭕️ |⭕️ |✖️|✖️|✔|✖️|✖️
English (United Kingdom)|✔|✔|✔|✔|✔|✔|✔
English (United States) |✔|✔|✔|✔|✔|✔|✔
Esperanto               |⭕️ |⭕️ |✔|✖️|✖️|✔|✖️
Estonian                |✔|✔|✔|✖️|✔|✔|✖️
Finnish                 |✔|✔|✖️|✔|✔|✔|✔
French                  |✔|✔|✔|✔|✔|✔|✔
Galician                |⭕️ |⭕️ |✔|✖️|✔|✔|✖️
Ganda                   |⭕️ |✔|✖️|✖️|✖️|✖️|✖️
Georgian                |⭕️ |⭕️ |✖️|✖️|✔|✖️|✖️
German (Austria)        |✔|✔|✔|✔|✔|✔|✔
German (Germany)        |✔|✔|✔|✔|✔|✔|✔
German (Switzerland)    |✔|✔|✔|✔|✔|✔|✔
Greek (Ancient)         |⭕️ |✔|✖️|✖️|✔|✖️|✖️
Greek (Modern)          |✔|✔|✔|✔|✔|✔|✔
Gujarati                |⭕️ |✔|✖️|✖️|✖️|✔|✖️
Hausa                   |⭕️ |⭕️ |✖️|✖️|✖️|✔|✖️
Hebrew                  |⭕️ |✔|✖️|✖️|✖️|✔|✖️
Hindi                   |⭕️ |✔|✖️|✖️|✔|✔|✖️
Hungarian               |⭕️ |✔|✔|✖️|✔|✔|✖️
Icelandic               |⭕️ |✔|✔|✖️|✔|✖️|✖️
Indonesian              |⭕️ |✔|✔|✖️|✔|✔|✖️
Irish                   |⭕️ |✔|✖️|✖️|✔|✔|✖️
Italian                 |✔|✔|✔|✔|✔|✔|✔
Japanese                |✔|✔|✖️|✔|✔|✔|✔
Kannada                 |⭕️ |✔|✖️|✖️|✖️|✖️|✖️
Kazakh                  |⭕️ |⭕️ |✖️|✖️|✖️|✔|✖️
Khmer                   |✔|✔|✖️|✔|✖️|✖️|✖️
Korean                  |✔|✔|✖️|✔|✔|✔|✔
Kurdish                 |⭕️ |⭕️ |✖️|✖️|✖️|✔|✖️
Kyrgyz                  |⭕️ |✔|✖️|✖️|✖️|✖️|✖️
Latin                   |⭕️ |✔|✖️|✖️|✔|✔|✖️
Latvian                 |⭕️ |✔|✔|✖️|✔|✔|✖️
Ligurian                |⭕️ |✔|✖️|✖️|✖️|✖️|✖️
Lithuanian              |✔|✔|✔|✔|✔|✔|✔
Lugbara                 |⭕️ |⭕️ |✖️|✖️|✖️|✔|✖️
Luxembourgish           |⭕️ |✔|✖️|✖️|✔|✖️|✖️
Macedonian              |✔|✔|✖️|✔|✔|✖️|✔
Malay                   |⭕️ |✔|✖️|✖️|✔|✔|✖️
Malayalam               |✔|✔|✖️|✖️|✖️|✖️|✖️
Manx                    |⭕️ |⭕️ |✖️|✖️|✔|✖️|✖️
Marathi                 |⭕️ |✔|✖️|✖️|✖️|✔|✖️
Meitei                  |⭕️ |✔|✖️|✖️|✖️|✖️|✖️
Mongolian               |⭕️ |⭕️ |✔|✖️|✖️|✖️|✖️
Nepali                  |⭕️ |✔|✖️|✖️|✖️|✔|✖️
Norwegian Bokmål        |✔|✔|✔|✔|✔|✔|✔
Norwegian Nynorsk       |✔|⭕️ |✔|✖️|✔|✔|✖️
Oriya                   |⭕️ |✔|✖️|✖️|✖️|✖️|✖️
Persian                 |⭕️ |✔|✖️|✖️|✔|✔|✖️
Polish                  |✔|✔|✔|✔|✔|✔|✔
Portuguese (Brazil)     |✔|✔|✔|✔|✔|✔|✔
Portuguese (Portugal)   |✔|✔|✔|✔|✔|✔|✔
Punjabi (Gurmukhi)      |⭕️ |✔|✖️|✖️|✖️|✔|✖️
Romanian                |✔|✔|✔|✔|✔|✔|✔
Russian                 |✔|✔|✔|✔|✔|✔|✔
Sámi (Northern)         |⭕️ |⭕️ |✖️|✖️|✔|✖️|✖️
Sanskrit                |⭕️ |✔|✖️|✖️|✖️|✖️|✖️
Scottish Gaelic         |⭕️ |⭕️ |✖️|✖️|✔|✖️|✖️
Serbian (Cyrillic)      |⭕️ |✔|✔|✖️|✔|✖️|✖️
Serbian (Latin)         |⭕️ |✔|✔|✖️|✔|✖️|✖️
Sinhala                 |⭕️ |✔|✖️|✖️|✖️|✖️|✖️
Slovak                  |⭕️ |✔|✔|✖️|✔|✔|✖️
Slovenian               |✔|✔|✔|✔|✔|✔|✔
Somali                  |⭕️ |⭕️ |✖️|✖️|✖️|✔|✖️
Sorbian (Lower)         |⭕️ |✔|✖️|✖️|✖️|✖️|✖️
Sorbian (Upper)         |⭕️ |✔|✖️|✖️|✖️|✖️|✖️
Sotho (Southern)        |⭕️ |⭕️ |✖️|✖️|✖️|✔|✖️
Spanish                 |✔|✔|✔|✔|✔|✔|✔
Swahili                 |⭕️ |⭕️ |✖️|✖️|✔|✔|✖️
Swedish                 |✔|✔|✔|✔|✔|✔|✔
Tagalog                 |⭕️ |✔|✖️|✖️|✔|✔|✖️
Tajik                   |⭕️ |✔|✖️|✖️|✖️|✔|✖️
Tamil                   |⭕️ |✔|✖️|✖️|✖️|✖️|✖️
Tatar                   |⭕️ |✔|✖️|✖️|✖️|✖️|✖️
Telugu                  |⭕️ |✔|✔|✖️|✖️|✖️|✖️
Tetun Dili              |⭕️ |✔|✖️|✖️|✖️|✖️|✖️
Thai                    |✔|✔|✔|✔|✖️|✔|✖️
Tibetan                 |✔|✔|✖️|✔|✔|✖️|✖️
Tigrinya                |⭕️ |✔|✖️|✖️|✖️|✖️|✖️
Tswana                  |⭕️ |✔|✖️|✖️|✖️|✖️|✖️
Turkish                 |✔|✔|✖️|✖️|✔|✔|✖️
Ukrainian               |✔|✔|✔|✔|✔|✔|✔
Urdu                    |⭕️ |✔|✖️|✖️|✔|✔|✖️
Vietnamese              |✔|✔|✖️|✔|✖️|✔|✖️
Welsh                   |⭕️ |⭕️ |✖️|✖️|✔|✖️|✖️
Yoruba                  |⭕️ |✔|✖️|✖️|✖️|✔|✖️
Zulu                    |⭕️ |⭕️ |✔|✖️|✖️|✔|✖️
Other languages         |⭕️ |⭕️ |✖️|✖️|✖️|✖️|✖️

✔: Supported<br>
⭕️: Supported but falls back to the default English tokenizer<br>
✖️: Not supported

<span id="doc-4-2"></span>
### [4.2 Supported File Types](#doc)

File Type               |File Extensions
------------------------|-----------------
CSV files               |\*.csv
Excel workbooks         |\*.xlsx
HTML pages              |\*.htm, \*.html
PDF files               |\*.pdf
Text files              |\*.txt
Translation memory files|\*.tmx
Word documents          |\*.docx
XML files               |\*.xml

\* Microsoft 97-03 Word documents (\*.doc) and Microsoft 97-03 Excel Workbooks (\*.xls) are not supported.<br>
\* Non-text files will be converted to text files first before being added to the *File Table*. You can check the converted files under folder **imports** at the installation location of *Wordless* on your computer (as for macOS users, right click **Wordless.app**, select **Show Package Contents** and navigate to **Contents/MacOS/imports/**). You can change this location via **Menu → Preferences → Settings → General → Import → Temporary Files → Default Path**.
\* *Wordless* **could only extract text from text-searchable PDF files** and is not capable of converting scanned PDF files into text-searchable ones. And **it is not recommended to import PDF files**, for the accuracy of text extraction from PDF files could be quite low.

<span id="doc-4-3"></span>
### [4.3 Supported File Encodings](#doc)

Language               |File Encoding          |Auto-detection
-----------------------|-----------------------|:------------:
All languages          |UTF-8 without BOM      |✔
All languages          |UTF-8 with BOM         |✖️
All languages          |UTF-16 with BOM        |✔
All languages          |UTF-16BE without BOM   |✔
All languages          |UTF-16LE without BOM   |✔
All languages          |UTF-32 with BOM        |✔
All languages          |UTF-32BE without BOM   |✔
All languages          |UTF-32LE without BOM   |✔
All languages          |UTF-7                  |✔
Arabic                 |CP720                  |✔
Arabic                 |CP864                  |✔
Arabic                 |ISO-8859-6             |✔
Arabic                 |Mac OS                 |✔
Arabic                 |Windows-1256           |✔
Baltic languages       |CP775                  |✔
Baltic languages       |ISO-8859-13            |✔
Baltic languages       |Windows-1257           |✔
Celtic languages       |ISO-8859-14            |✔
Chinese                |GB18030                |✔
Chinese                |GBK                    |✔
Chinese (Simplified)   |GB2312                 |✔
Chinese (Simplified)   |HZ                     |✔
Chinese (Traditional)  |Big-5                  |✔
Chinese (Traditional)  |Big5-HKSCS             |✔
Chinese (Traditional)  |CP950                  |✔
Croatian               |Mac OS                 |✔
Cyrillic               |CP855                  |✔
Cyrillic               |CP866                  |✔
Cyrillic               |ISO-8859-5             |✔
Cyrillic               |Mac OS                 |✔
Cyrillic               |Windows-1251           |✔
English                |ASCII                  |✔
English                |EBCDIC 037             |✔
English                |CP437                  |✔
European               |HP Roman-8             |✔
European (Central)     |CP852                  |✔
European (Central)     |ISO-8859-2             |✔
European (Central)     |Mac OS Central European|✔
European (Central)     |Windows-1250           |✔
European (Northern)    |ISO-8859-4             |✔
European (Southern)    |ISO-8859-3             |✔
European (Southeastern)|ISO-8859-16            |✔
European (Western)     |EBCDIC 500             |✔
European (Western)     |CP850                  |✔
European (Western)     |CP858                  |✔
European (Western)     |CP1140                 |✔
European (Western)     |ISO-8859-1             |✔
European (Western)     |ISO-8859-15            |✔
European (Western)     |Mac OS Roman           |✔
European (Western)     |Windows-1252           |✔
French                 |CP863                  |✔
German                 |EBCDIC 273             |✔
Greek                  |CP737                  |✔
Greek                  |CP869                  |✔
Greek                  |CP875                  |✔
Greek                  |ISO-8859-7             |✔
Greek                  |Mac OS                 |✔
Greek                  |Windows-1253           |✔
Hebrew                 |CP856                  |✔
Hebrew                 |CP862                  |✔
Hebrew                 |EBCDIC 424             |✔
Hebrew                 |ISO-8859-8             |✔
Hebrew                 |Windows-1255           |✔
Icelandic              |CP861                  |✔
Icelandic              |Mac OS                 |✔
Japanese               |CP932                  |✔
Japanese               |EUC-JP                 |✔
Japanese               |EUC-JIS-2004           |✔
Japanese               |EUC-JISx0213           |✔
Japanese               |ISO-2022-JP            |✔
Japanese               |ISO-2022-JP-1          |✔
Japanese               |ISO-2022-JP-2          |✔
Japanese               |ISO-2022-JP-2004       |✔
Japanese               |ISO-2022-JP-3          |✔
Japanese               |ISO-2022-JP-EXT        |✔
Japanese               |Shift_JIS              |✔
Japanese               |Shift_JIS-2004         |✔
Japanese               |Shift_JISx0213         |✔
Kazakh                 |KZ-1048                |✔
Kazakh                 |PTCP154                |✔
Korean                 |EUC-KR                 |✔
Korean                 |ISO-2022-KR            |✔
Korean                 |JOHAB                  |✔
Korean                 |UHC                    |✔
Nordic languages       |CP865                  |✔
Nordic languages       |ISO-8859-10            |✔
Persian/Urdu           |Mac OS Farsi           |✔
Portuguese             |CP860                  |✔
Romanian               |Mac OS                 |✔
Russian                |KOI8-R                 |✔
Tajik                  |KOI8-T                 |✔
Thai                   |CP874                  |✔
Thai                   |ISO-8859-11            |✔
Thai                   |TIS-620                |✔
Turkish                |CP857                  |✔
Turkish                |EBCDIC 1026            |✔
Turkish                |ISO-8859-9             |✔
Turkish                |Mac OS                 |✔
Turkish                |Windows-1254           |✔
Ukrainian              |CP1125                 |✔
Ukrainian              |KOI8-U                 |✔
Urdu                   |CP1006                 |✔
Vietnamese             |CP1258                 |✔

<span id="doc-4-4"></span>
### [4.4 Supported Measures](#doc)

<span id="doc-4-4-1"></span>
#### [4.4.1 Measures of Readability](#doc)

The readability of a text depends on several variables including the average sentence length, average word length in characters, average word length in syllables, number of monosyllabic words, number of polysyllabic words, number of difficult words, etc.

It should be noted that some readability measures are **language-specific**, or applicable only to texts in languages for which *Wordless* have **built-in syllable tokenization support** (check [4.4.1](#doc-4-1) for reference), while others can be applied to texts in all languages.

These variables are used in the following formulas:<br>
**NumSentences**: Number of sentences in the text or sample<br>
**NumWords**: Number of words in the text or sample<br>
<span id="ref-num-words-dale-769"></span>**NumWordsDale₇₆₉**: Number of words outside the Dale list of 769 easy words ([Dale, 1931](#ref-dale-1931))<br>
<span id="ref-num-words-dale-3000"></span>**NumWordsDale₃₀₀₀**: Number of words outside the Dale list of 3000 easy words ([Dale & Chall, 1948b](#ref-dale-chall-1948b))<br>
<span id="ref-num-words-spache"></span>**NumWordsSpache**: Number of words outside the Spache word list ([Spache, 1974](#ref-spache-1974))<br>
**NumWords1Syl**: Number of monosyllabic words<br>
**NumWords3+Syls**: Number of words with 3 or more syllables<br>
**NumSyls**: Number of syllable in the text or sample<br>
**NumCharsAll**: Number of characters (including letters, CJK characters, etc., numerals, and punctuation marks) in the text or sample<br>
**NumCharsAlpha**: Number of alphabetic characters (letters, CJK characters, etc.) in the text or sample<br>
**NumCharsAlnum**: Number of alphanumeric characters (letters, CJK characters, etc., numerals) in the text or sample

<!--
Automated Arabic Readability Index:
    {\text{AARI} = 3.28 \times \text{NumCharsAlnum} + 1.43 \times \frac{\text{NumCharsAlnum}}{\text{NumWords}} + 1.24 \times \frac{\text{NumWords}}{\text{NumSentences}}}

Automated Readability Index:
    \begin{align*}
        \text{ARI} &= 0.5 \times \frac{\text{NumWords}}{\text{NumSentences}} + 4.71 \times \frac{\text{NumCharsAll}}{\text{NumWords}} - 21.43 \\
        \text{ARI}_{\text{Navy}} &= 0.37 \times \frac{\text{NumWords}}{\text{NumSentences}} + 5.84 \times \frac{\text{NumCharsAll}}{\text{NumWords}} - 26.01
    \end{align*} 

Bormuth's Cloze Mean & Grade Placement:
    \begin{align*}
        \text{M} = \; &0.886593 - 0.083640 \times \frac{\text{NumCharsAlpha}}{\text{NumWords}} + 0.161911 \times \left(\frac{\text{NumWordsDale}_{3000}}{\text{NumWords}}\right)^3 - \\
        &0.021401 \times \frac{\text{NumWords}}{\text{NumSentences}} + 0.000577 \times \left(\frac{\text{NumWords}}{\text{NumSentences}}\right)^2 - 0.000005 \times \left(\frac{\text{NumWords}}{\text{NumSentences}}\right)^3 \\
        \text{GP} = \; &4.275 + 12.881 \times \text{M} - 34.934 \times \text{M}^2 + 20.388 \times \text{M}^3 + 26.194 \times \text{C} - 2.046 \times \text{C}^2 - 11.767 \times \text{C}^3 - \\
        &44.285 \times \left(\text{M} \times \text{C}\right) + 97.620 \times \left(\text{M} \times \text{C}\right)^2 - 59.538 \times \left(\text{M} \times \text{C}\right)^3
    \end{align*}

Coleman-Liau Index:
    \begin{align*}
        \text{Estimated Cloze \ %} &= 141.8401 - 0.21459 \times \left(\frac{\text{NumCharsAlpha}}{\text{NumWords}} \times 100\right) + 1.079812 \times \left(\frac{\text{NumSentences}}{\text{NumWords}} \times 100\right) \\
        \text{Grade Level} &= -27.4004 \times \frac{\text{Estimated Cloze \; %}}{100} + 23.06395
    \end{align*}

Coleman's Readability Formula:
    \begin{align*}
        \text{Cloze \; %}_1 &= 1.29 \times \left(\frac{\text{NumWords1Syl}}{\text{NumWords}} \times 100\right) - 38.45 \\
        \text{Cloze \; %}_2 &= 1.16 \times \left(\frac{\text{NumWords1Syl}}{\text{NumWords}} \times 100\right) + 1.48 \times \left(\frac{\text{NumSentences}}{\text{NumWords}} \times 100\right) - 37.95 \\
        \text{Cloze \; %}_3 &= 1.07 \times \left(\frac{\text{NumWords1Syl}}{\text{NumWords}} \times 100\right) + 1.18 \times \left(\frac{\text{NumSentences}}{\text{NumWords}} \times 100\right) + 0.76 \times \left(\frac{\text{NumProns}}{\text{NumWords}} \times 100\right) - 34.02 \\
        \text{Cloze \; %}_4 &= 1.04 \times \left(\frac{\text{NumWords1Syl}}{\text{NumWords}} \times 100\right) + 1.06 \times \left(\frac{\text{NumSentences}}{\text{NumWords}} \times 100\right) + 0.56 \times \left(\frac{\text{NumProns}}{\text{NumWords}} \times 100\right) - 0.36 \times \left(\frac{\text{NumPreps}}{\text{NumWords}} \times 100\right) - 26.01
    \end{align*}

Dale-Chall Readability Formula:
    {\text{X}_{\text{c}50} = 0.1579 \times \left(\frac{\text{NumWordsDale}_{3000}}{\text{NumWords}} \times 100\right) + 0.0496 \times \frac{\text{NumWords}}{\text{NumSentences}} + 3.6365}

Dale-Chall Readability Formula (New):
    \text{X}_{\text{c}50} = 64 - 0.95 \times \left(\frac{\text{NumWordsDale}_{3000}}{\text{NumWords}} \times 100\right) - 0.69 \times \frac{\text{NumWords}}{\text{NumSentences}}

Danielson-Bryan's Readability Formula:
    \begin{align*}
        \text{Danielson-Bryan}_1 &= 1.0364 \times \frac{\text{NumCharsAll}}{\text{NumWords} - 1} + 0.0194 \times \frac{\text{NumCharsAll}}{\text{NumSentences}} - 0.6059 \\
        \text{Danielson-Bryan}_2 &= 131.059 - 10.364 \times \frac{\text{NumCharsAll}}{\text{NumWords} - 1} - 0.194 \times \frac{\text{NumCharsAll}}{\text{NumSentences}}
    \end{align*}

Degrees of Reading Power:
    \text{DRP} = 100 - (\lfloor \text{M} \times 100 + 0.5 \rfloor)

Devereux Readability Index:
    \text{Grade Placement} = 1.56 \times \frac{\text{NumCharsAll}}{\text{NumWords}} + 0.19 \times \frac{\text{NumWords}}{\text{NumSentences}} - 6.49

Easy Listening Formula:
    \text{ELF} = \frac{\text{NumSyls} - \text{NumWords}}{\text{NumSentences}}

Flesch-Kincaid Grade Level:
    \text{GL} = 0.39 \times \frac{\text{NumWords}}{\text{NumSentences}} + 11.8 \times \frac{\text{NumSyls}}{\text{NumWords}} - 15.59

Flesch Reading Ease:
    \begin{align*}
        \text{ASW} &= \frac{\text{NumSyls}}{\text{NumWords}} \qquad \text{ASL} = \frac{\text{NumWords}}{\text{NumSentences}} \\
        \text{RE} &= 206.835 - 0.846 \times (\text{ASW} \times 100) - 1.015 \times \text{ASL} \\
        \text{RE}_\text{Dutch-Douma} &= 206.84 - 77 \times \text{ASW} - 0.93 \times \text{ASL} \\
        \text{RE}_\text{Dutch-Brouwer} &= 195 - \frac{200}{3} \times \text{ASW} - 2 \times \text{ASL} \\
        \text{RE}_\text{French} &= 207 - 73.6 \times \text{ASW} - 1.015 \times \text{ASL} \\
        \text{RE}_\text{German} &= 180 - 58.5 \times \text{ASW} - \text{ASL} \\
        \text{RE}_\text{Italian} &= 217 - 60 \times \text{ASW} - 1.3 \times \text{ASL} \\
        \text{RE}_\text{Russian} &= 206.835 - 60.1 \times \text{ASW} - 1.3 \times \text{ASL} \\
        \text{RE}_{\text{Spanish-Fern}\acute{\text{a}}\text{ndez Huerta}} &= 206.84 - 60 \times \text{ASW} - 1.02 \times \text{ASL} \\
        \text{RE}_\text{Spanish-Szigriszt Pazos} &= 207 - 62.3 \times \text{ASW} - \text{ASL}
    \end{align*}

Flesch Reading Ease (Simplified):
    \text{RE} = 1.599 \times \left(\frac{\text{NumWords1Syl}}{\text{NumWords}} \times 100\right) - 1.015 \times \frac{\text{NumWords}}{\text{NumSentences}} - 31.517

FORCAST Grade Level:
    \text{RGL} = 20.43 - 0.11 \times \text{NumWords1Syl}

Fórmula de comprensibilidad de Gutiérrez de Polini:
    \text{CP} = 95.2 - 9.7 \times \frac{\text{NumCharsAlpha}}{\text{NumWords}} - 0.35 \times \frac{\text{NumWords}}{\text{NumSentences}}

Fórmula de Crawford:
    {\text{Grade Level} = \frac{\text{NumSentences}}{\text{NumWords}} \times 100 \times (-0.205) + \frac{\text{NumSyls}}{\text{NumWords}} \times 100 \times 0.049 - 3.407}

Fucks's Stilcharakteristik:
    \text{Stilcharakteristik} = \frac{\text{NumWords}}{\text{NumSentneces}} \times \frac{\text{NumSyls}}{\text{NumWords}}

Gulpease Index:
    \text{Gulpease Index} = 89 + \frac{300 \times \text{NumSentences} - 10 \times \text{NumCharsAlpha}}{\text{NumWords}}

Gunning Fog Index:
    \begin{align*}
        \text{Fog Index} &= 0.4 \times \left(\frac{\text{NumWords}}{\text{NumSentences}} + \frac{\text{NumHardWords}}{\text{NumWords}} \times 100\right) \\
        \text{Fog Index}_{\text{Navy}} &= \frac{\frac{\text{NumWords} + 2 \times \text{NumWords3+Syls}}{\text{NumSentences}} - 3}{2}
    \end{align*}

Legibilidad µ:
    \mu = \frac{\text{NumWords}}{\text{NumWords} - 1} \times \frac{\text{LenWordsAvg}}{\text{LenWordsVar}} \times 100

Lensear Write:
    \text{Score} = \text{NumWords1Syl} + 3 \times \text{NumSentences}

Lix:
    \text{Lix} = \frac{\text{NumWords}}{\text{NumSentences}} + 100 \times \frac{\text{NumLongWords}}{\text{NumWords}}

McAlpine EFLAW Readability Score:
    \text{EFLAW} = \frac{\text{NumWords} + \text{NumMiniWords}}{\text{NumSentences}}

OSMAN:
    \text{OSMAN} = 200.791 - 1.015 \times \frac{\text{NumWords}}{\text{NumSentences}} - 24.181 \times \frac{\text{NumLongWords} + \text{NumSyls} + \text{NumComplexWords} + \text{NumFaseehWords}}{\text{NumWords}}

Rix:
    \text{Rix} = \frac{\text{NumLongWords}}{\text{NumSentences}}

SMOG Grade:
    \text{g} = 3.1291 + 1.043 \times \sqrt{\text{NumWords3+Syls}}

Spache Grade Level:
    \begin{align*}
        \text{Grade Level} &= 0.141 \times \frac{100}{\text{NumSentences}} + 0.086 \times \left(\frac{\text{NumWordsDale}_{769}}{100} \times 100\right) + 0.839 \\
        \text{Grade Level}_{Revised} &= 0.121 \times \frac{100}{\text{NumSentences}} + 0.082 \times \left(\frac{\text{NumWordsSpache}}{100} \times 100\right) + 0.659
    \end{align*}

Wiener Sachtextformel:
    \begin{align*}
        \text{MS} &= \frac{\text{NumWords3+Syls}}{\text{NumWords}} \qquad \text{SL} = \frac{\text{NumWords}}{\text{NumSentences}} \\
        \text{IW} &= \frac{\text{NumLongWords}}{\text{NumWords}} \qquad \; \; \; \text{ES} = \frac{\text{NumWords1Syl}}{\text{NumWords}} \\
        \text{WSTF}_1 &= 0.1925 \times \text{MS} + 0.1672 \times \text{SL} + 0.1297 \times \text{IW} - 0.0327 \times \text{ES} - 0.875 \\
        \text{WSTF}_2 &= 0.2007 \times \text{MS} + 0.1682 \times \text{SL} + 0.1373 \times \text{IW} - 2.779 \\
        \text{WSTF}_3 &= 0.2963 \times \text{MS} + 0.1905 \times \text{SL} - 1.1144 \\
        \text{WSTF}_4 &= 0.2744 \times \text{MS} + 0.2656 \times \text{SL} - 1.693
    \end{align*}
-->

Measure of Readability|Formula
----------------------|-------
<span id="ref-aari"></span>Automated Arabic Readability Index<br>([Al-Tamimi et al., 2013](#ref-altamimi-et-al-2013))|![Formula](/doc/measures/readability/aari.svg)<br><br>* This measure applies only to **Arabic texts**.
<span id="ref-ari"></span>Automated Readability Index²<br>([Smith & Senter, 1967](#ref-smith-senter-1967)<br>Navy: [Kincaid et al., 1975](#ref-kincaid-et-al-1975))|![Formula](/doc/measures/readability/ari.svg)
<span id="ref-bormuths-cloze-mean-gp"></span>Bormuth's Cloze Mean & Grade Placement<br>([Bormuth, 1969](#ref-bormuth-1969))|![Formula](/doc/measures/readability/bormuths_cloze_mean_gp.svg)<br>where **C** is the cloze criterion score, whose value could be changed via **Menu → Preferences → Settings → Measures → Readability → Bormuth's Grade Placement - Cloze criterion score**<br><br>* This measure applies only to **English texts**.
<span id="ref-coleman-liau-index"></span>Coleman-Liau Index<br>([Coleman & Liau, 1975](#ref-coleman-liau-1975))|![Formula](/doc/measures/readability/coleman_liau_index.svg)
<span id="ref-colemans-readability-formula"></span>Coleman's Readability Formula¹²<br>([Coleman et al., 1976](#ref-coleman-et-al-1976))|![Formula](/doc/measures/readability/colemans_readability_formula.svg)<br>where **NumProns** is the number of pronouns and **NumPreps** is the number of Prepositions<br><br>* This measure applies only to **English texts**.
<span id="ref-dale-chall-readability-formula"></span>Dale-Chall Readability Formula<br>([Dale & Chall, 1948a](#ref-dale-chall-1948a); [Dale & Chall, 1948b](#ref-dale-chall-1948b))|![Formula](/doc/measures/readability/x_c50.svg)<br><br>* This measure applies only to **English texts**.
<span id="ref-dale-chall-readability-formula-new"></span>Dale-Chall Readability Formula (New)<br>([Chall & Dale, 1995](#ref-chall-dale-1995))|![Formula](/doc/measures/readability/x_c50_new.svg)<br><br>* This measure applies only to **English texts**.
<span id="ref-danielson-bryans-readability-formula"></span>Danielson-Bryan's Readability Formula²<br>([Danielson & Bryan, 1963](#ref-danielson-bryan-1963))|![Formula](/doc/measures/readability/danielson_bryans_readability_formula.svg)
<span id="ref-drp"></span>Degrees of Reading Power<br>([College Entrance Examination Board, 1981](#ref-college-entrance-examination-board-1981))|![Formula](/doc/measures/readability/drp.svg)<br>where **M** is *Bormuth's cloze mean*.<br><br>* This measure applies only to **English texts**.
<span id="ref-devereux-readability-index"></span>Devereux Readability Index<br>([Smith, 1961](#ref-smith-1961))|![Formula](/doc/measures/readability/devereux_readability_index.svg)
<span id="ref-elf"></span>Easy Listening Formula¹<br>([Fang, 1966](#ref-fang-1966))|![Formula](/doc/measures/readability/elf.svg)
<span id="ref-gl"></span>Flesch-Kincaid Grade Level¹<br>([Kincaid et al., 1975](#ref-kincaid-et-al-1975))|![Formula](/doc/measures/readability/gl.svg)
<span id="ref-re"></span>Flesch Reading Ease¹²<br>([Flesch, 1948](#ref-flesch-1948)<br>Dutch: [Douma, 1960](#ref-douma-1960); [Brouwer, 1963](#ref-brouwer-1963)<br>French: [Kandel & Moles, 1958](#ref-kandel-moles-1958)<br>German: [Amstad, 1978](#ref-amstad-1978)<br>Italian: [Franchina & Vacca, 1986](#ref-franchina-vacca-1986)<br>Russian: [Oborneva, 2006](#ref-oborneva-2006)<br>Spanish: [Fernández Huerta, 1959](#ref-fernandez-huerta-1959); [Szigriszt Pazos, 1993](#ref-szigrisze-pazos-1993))|![Formula](/doc/measures/readability/re.svg)
<span id="ref-re-simplified"></span>Flesch Reading Ease (Simplified)¹<br>([Farr et al., 1951](#ref-farr-et-al-1951))|![Formula](/doc/measures/readability/re_simplified.svg)
<span id="ref-rgl"></span>FORCAST Grade Level¹<br>([Caylor et al., 1973](#ref-caylor-et-al-1973))|![Formula](/doc/measures/readability/rgl.svg)<br><br>* A sample of 150 words is taken randomly from the text, thus the text should be **at least 150 words long**.
<span id="ref-cp"></span>Fórmula de comprensibilidad de Gutiérrez de Polini<br>([Gutiérrez de Polini, 1972](#ref-gutierrez-de-polini-1972))|![Formula](/doc/measures/readability/cp.svg)<br><br>* This measure applies only to **Spanish texts**.
<span id="ref-formula-de-crawford"></span>Fórmula de Crawford¹<br>([Crawford, 1985](#ref-crawford-1985))|![Formula](/doc/measures/readability/formula_de_crawford.svg)<br><br>* This measure applies only to **Spanish texts**.
<span id="ref-fuckss-stilcharakteristik"></span>Fucks's Stilcharakteristik¹<br>([Fucks, 1955](#ref-fucks-1955))|![Formula](/doc/measures/readability/fuckss_stilcharakteristik.svg)
<span id="ref-gulpease-index"></span>Gulpease Index<br>([Lucisano & Emanuela Piemontese, 1988](#ref-lucisano-emanuela-piemontese-1988))|![Formula](/doc/measures/readability/gulpease_index.svg)<br><br>* This measure applies only to **Italian texts**.
<span id="ref-fog-index"></span>Gunning Fog Index¹²<br>(English: [Gunning, 1968](#ref-gunning-1968)<br>Navy: [Kincaid et al., 1975](#ref-kincaid-et-al-1975)<br>Polish: [Pisarek, 1969](#ref-pisarek-1969))|![Formula](/doc/measures/readability/fog_index.svg)<br>where **NumHardWords** is the number of words with 3 or more syllables excluding all proper nouns and words with 3 syllables ending with *-ed* or *-es* for **English texts**, and the number of words with 4 or more syllables for **Polish texts**.<br><br>* This measure applies only to **English texts** and **Polish texts**.
<span id="ref-mu"></span>Legibilidad µ<br>([Muñoz Baquedano, 2006](#ref-munoz-baquedano-2006))|![Formula](/doc/measures/readability/mu.svg)<br>where **LenWordsAvg** is the average word length in letters, and **LenWordsVar** is the variance of word lengths in letters.<br><br>* This measure applies only to **Spanish texts**.<br>* The text should be **at least 2 words long**.
<span id="ref-lensear-write"></span>Lensear Write¹<br>([O’Hayre, 1966](#ref-o-hayre-1966))|![Formula](/doc/measures/readability/lensear_write.svg)<br>where **NumWords1Syl** is the number of monosyllabic words excluding *the*, *is*, *are*, *was*, *were*, and **NumSentences** is the number of sentences to the nearest period.<br><br>* This measure applies only to **English texts**.<br>* A sample of 100 words is taken randomly from the text.<br>* If the text is **shorter than 100 words**, **NumWords1Syl** and **NumSentences** need to be multiplied by 100 and then divided by the number of text.
<span id="ref-lix"></span>Lix<br>([Björnsson, 1968](#ref-bjornsson-1968))|![Formula](/doc/measures/readability/lix.svg)<br>where **NumLongWords** is the number of words with 7 or more letters.
<span id="ref-eflaw"></span>McAlpine EFLAW Readability Score<br>([Nirmaldasan, 2009](#ref-nirmaldasan-2009))|![Formula](/doc/measures/readability/eflaw.svg)<br><br>* This measure applies only to **English texts**.
<span id="ref-osman"></span>OSMAN<br>([El-Haj & Rayson, 2016](#ref-elhaj-rayson-2016))|![Formula](/doc/measures/readability/osman.svg)<br>where **NumLongWords** is the number of words with 6 or more letters, **NumComplexWords** is the number of words with 5 or more syllables, and **NumFaseehWords** is the number of complex words containing ء/ئ/ؤ/ذ/ظ or ending with وا/ون.<br><br>* This measure applies only to **Arabic texts**.<br>* The number of syllables in each Arabic word is estimated by adding the number of short syllables and twice the number of long and stress syllables.
<span id="ref-rix"></span>Rix<br>([Anderson, 1983](#ref-anderson-1983))|![Formula](/doc/measures/readability/rix.svg)<br>where **NumLongWords** is the number of words with 7 or more letters.
<span id="ref-smog-grade"></span>SMOG Grade¹<br>([McLaughlin, 1969](#ref-mclaughlin-1969))|![Formula](/doc/measures/readability/smog_grade.svg)<br><br>* A sample consisting of the first 10 sentences of the text, the last 10 sentences of the text, and 10 sentences at the middle of the text is taken from the text, thus the text should be **at least 30 sentences long**.
<span id="ref-spache-grade-level"></span>Spache Grade Level<br>([Spache, 1953](#ref-spache-1953)<br>Revised: [Spache, 1974](#ref-spache-1974))|![Formula](/doc/measures/readability/spache_grade_level.svg)<br><br>* Three samples each of 100 words are taken randomly from the text and the results are averaged out, thus the text should be **at least 100 words long**.
<span id="ref-wstf"></span>Wiener Sachtextformel¹²<br>([Bamberger & Vanecek, 1984](#ref-bamberger-vanecek-1984))|![Formula](/doc/measures/readability/wstf.svg)<br>where **NumLongWords** is the numbers of words with 7 or more letters.<br><br>* This measure applies only to **German texts**.

**Notes:**
1. Requires **built-in syllable tokenization support**
2. Has variants, which could be selected via **Menu - Preferences - Settings - Measures - Readability**

<span id="doc-4-4-2"></span>
#### [4.4.2 Measures of Dispersion & Adjusted Frequency](#doc)

For parts-based measures, each file is divided into **n** (whose value you could modify via **Menu → Preferences → Settings → Measures → Dispersion / Adjusted Frequency → General Settings → Divide each file into subsections**) sub-sections and the frequency of the word in each part is counted and denoted by **F₁**, **F₂**, **F₃**, ..., **Fₙ** respectively. The total frequency of the word in each file is denoted by **F** and the mean value of the frequencies over all sub-sections is denoted by **F̅**.

For distance-based measures, the distance between each pair of subsequent occurrences of the word is calculated and denoted by **d₁**, **d₂**, **d₃**, ..., **d<sub>F</sub>** respectively. The total number of tokens in each file is denoted by **N**.

Then, the dispersion and adjusted frequency of the word are calculated as follows:

<!--
Average Logarithmic Distance:
    \begin{align*}
        \text{ALD} &= \frac{1}{N} \times \sum_{i = 1}^{F}(d_i \times \log_{10}d_i) \\
        \text{f}_{\text{ALD}} &= \exp\left(-\sum_{i = 1}^{F}{\frac{d_i}{N} \times \ln\frac{d_i}{N}}\right)
    \end{align*}

Average Reduced Frequency:
    \text{ARF} = \text{f}_{\text{ARF}} = \frac{F}{N} \times \sum_{i = 1}^{F}\min\left\{d_i, \frac{N}{F}\right\}

Average Waiting Time:
    \begin{align*}
        \text{AWT} &= \frac{1}{2} \times \left(1 + \frac{1}{N} \times \sum_{i = 1}^{F}{d_i^2}\right) \\
        \text{f}_{\text{AWT}} &= \frac{N^2}{\sum_{i = 1}^F{d_i^2}}
    \end{align*}

Carroll's D₂ & Uₘ:
    \begin{align*}
        \text{H} &= \ln F - \frac{\sum_{i = 1}^n (F_i \times \ln F_i)}{F} \\
        \text{D}_2 &= \frac{\text{H}}{\ln n} \\
        \text{U}_\text{m} & = F \times \text{D}_2 + (1 - \text{D}_2) \times \frac{F}{n}
    \end{align*}

Engwall's FM:
    \text{FM} = \frac{F \times \text{R}}{n}

Gries's DP:
    \begin{align*}
        \text{DP} &= \frac{1}{2} \times \sum_{i = 1}^n \left|\frac{F_{i}}{F} - \frac{1}{n}\right| \\
        \text{DP}_{\text{norm}} &= \frac{\text{DP}}{1 - \frac{1}{n}}
    \end{align*}

Juilland's D & U:
    \begin{align*}
        \sigma &= \sqrt{\frac{\sum_{i = 1}^n (F_i - \overline{F})^2}{n}} \\
        \text{CV} &= \frac{\sigma}{\overline{F}} \\
        \text{D} &= 1- \frac{\text{CV}}{\sqrt{n - 1}} \\
        \text{U} &= \text{D} \times F
    \end{align*}

Kromer's UR:
    \text{U}_\text{R} = \sum_{i = 1}^n \psi(F_i + 1) + \text{C}

Lyne's D₃:
    \begin{align*}
        \chi^2 &= \sum_{i = 1}^n \frac{\left(F_i - \overline{F}\right)^2}{\overline{F}} \\
        \text{D}_3 &= \frac{1 - \chi^2}{4 \times F}
    \end{align*}

Rosengren's S & KF:
    \begin{align*}
        \text{KF} &= \frac{1}{n} \times \left(\sum_{i = 1}^n \sqrt{F_{i}}\right)^2 \\
        \text{S} &= \frac{\text{KF}}{F}
    \end{align*}

Zhang's Distributional Consistency:
    \text{DC} = \frac{\left(\frac{\sum_{i = 1}^n \sqrt{F_i}}{n}\right)^2}{\frac{\sum_{i = 1}^n}{n}}
-->

Measure of Dispersion (Parts-based)|Measure of Adjusted Frequency (Parts-based)|Formula
-----------------------------------|-------------------------------------------|-------
<span id="ref-carrolls-d2"></span>Carroll's D₂<br>([Carroll, 1970](#ref-carroll-1970))|<span id="ref-carrolls-um"></span>Carroll's Uₘ<br>([Carroll, 1970](#ref-carroll-1970))|![Formula](/doc/measures/dispersion_adjusted_frequency/carrolls_um.svg)
&nbsp;|<span id="ref-engwalls-fm"></span>Engwall's FM<br>([Engwall, 1974](#ref-engwall-1974))|![Formula](/doc/measures/dispersion_adjusted_frequency/engwalls_fm.svg)<br>where **R** is the number of sub-sections in which the word appears at least once.
<span id="ref-griess-dp"></span>Gries's DP<br>([Gries, 2008](#ref-gries-2008); [Lijffijt & Gries, 2012](#ref-lijffijt-gries-2012))||![Formula](/doc/measures/dispersion_adjusted_frequency/griess_dp.svg)<br><br>* Normalization is applied by default, which behavior you could change via **Menu → Preferences → Settings → Measures → Dispersion → Gries's DP → Apply normalization**.
<span id="ref-juillands-d"></span>Juilland's D<br>([Juilland & Chang-Rodrigues, 1964](#ref-juilland-chang-rodrigues-1964))|<span id="ref-juillands-u"></span>Juilland's U<br>([Juilland & Chang-Rodrigues, 1964](#ref-juilland-chang-rodrigues-1964))|![Formula](/doc/measures/dispersion_adjusted_frequency/juillands_u.svg)
&nbsp;|<span id="ref-kromers-ur"></span>Kromer's U<sub>R</sub><br>([Kromer, 2003](#ref-kromer-2003))|![Formula](/doc/measures/dispersion_adjusted_frequency/kromers_ur.svg)<br>where **ψ** is the [digamma function](https://en.wikipedia.org/wiki/Digamma_function), and **C** is the [Euler–Mascheroni constant](https://en.wikipedia.org/wiki/Euler%E2%80%93Mascheroni_constant).
<span id="ref-lynes-d3"></span>Lyne's D₃<br>([Lyne, 1985](#ref-lyne-1985))||![Formula](/doc/measures/dispersion_adjusted_frequency/lynes_d3.svg)
<span id="ref-rosengrens-s"></span>Rosengren's S<br>([Rosengren, 1971](#ref-rosengren-1971))|<span id="ref-rosengrens-kf"></span>Rosengren's KF<br>([Rosengren, 1971](#ref-rosengren-1971))|![Formula](/doc/measures/dispersion_adjusted_frequency/rosengrens_s.svg)
<span id="ref-zhangs-distributional-consistency"></span>Zhang's Distributional Consistency<br>([Zhang, 2004](#ref-zhang-2004))||![Formula](/doc/measures/dispersion_adjusted_frequency/zhangs_distributional_consistency.svg)

Measure of Dispersion (Distance-based)|Measure of Adjusted Frequency (Distance-based)|Formula
--------------------------------------|----------------------------------------------|-------
<span id="ref-ald"></span>Average Logarithmic Distance<br>([Savický & Hlaváčová, 2002](#ref-savicky-hlavacova-2002))|<span id="ref-fald"></span>Average Logarithmic Distance<br>([Savický & Hlaváčová, 2002](#ref-savicky-hlavacova-2002))|![Formula](/doc/measures/dispersion_adjusted_frequency/ald.svg)
<span id="ref-arf"></span>Average Reduced Frequency<br>([Savický & Hlaváčová, 2002](#ref-savicky-hlavacova-2002))|<span id="ref-farf"></span>Average Reduced Frequency<br>([Savický & Hlaváčová, 2002](#ref-savicky-hlavacova-2002))|![Formula](/doc/measures/dispersion_adjusted_frequency/arf.svg)
<span id="ref-awt"></span>Average Waiting Time<br>([Savický & Hlaváčová, 2002](#ref-savicky-hlavacova-2002))|<span id="ref-fawt"></span>Average Waiting Time<br>([Savický & Hlaváčová, 2002](#ref-savicky-hlavacova-2002))|![Formula](/doc/measures/dispersion_adjusted_frequency/awt.svg)

<span id="doc-4-4-3"></span>
#### [4.4.3 Tests of Statistical Significance, Measures of Bayes Factor, & Measures of Effect Size](#doc)

In order to calculate the statistical significance, Bayes factor, and effect size (except **Mann-Whitney U Test**, **Student's t-test (2-sample)**, and **Welch's t-test**) for two words in the same file (collocates) or for one specific word in two different files (keywords), two contingency tables must be constructed first, one for observed values, the other for expected values.

As for collocates (in *Collocation Extractor* and *Colligation Extractor*):

Observed Values|*Word 1*|Not *Word 1*|Row Total
--------------:|:------:|:----------:|:-------:
*Word 2*       |O₁₁     |O₁₂         |O₁ₓ
Not *Word 2*   |O₂₁     |O₂₂         |O₂ₓ
Column Total   |Oₓ₁     |Oₓ₂         |Oₓₓ

Expected Values|*Word 1*|Not *Word 1*
--------------:|:------:|:----------:
*Word 2*       |E₁₁     |E₁₂
Not *Word 2*   |E₂₁     |E₂₂

O₁₁: Number of occurrences of *Word 1* followed by *Word 2*.<br>
O₁₂: Number of occurrences of *Word 1* followed by any word except *Word 2*.<br>
O₂₁: Number of occurrences of any word except *Word 1* followed by *Word 2*.<br>
O₂₂: Number of occurrences of any word except *Word 1* followed by any word except *Word 2*.

As for keywords (in *Keyword Extractor*):

Observed Values|Observed File|Reference File|Row Total
--------------:|:-----------:|:------------:|:-------:
*Word w*       |O₁₁          |O₁₂           |O₁ₓ
*Not Word w*   |O₂₁          |O₂₂           |O₂ₓ
Column Total   |Oₓ₁          |Oₓ₂           |Oₓₓ

Expected Values|Observed File|Reference File
--------------:|:-----------:|:------------:
*Word w*       |E₁₁          |E₁₂
*Not Word w*   |E₂₁          |E₂₂

O₁₁: Number of occurrences of *Word w* in the observed file.<br>
O₁₂: Number of occurrences of *Word w* in the reference file.<br>
O₂₁: Number of occurrences of all words except *Word w* in the observed file.<br>
O₂₂: Number of occurrences of all words except *Word w* in the reference file.

To conduct **Mann-Whitney U Test**, **Student's t-test (2-sample)**, and **Welch's t-test** on a specific word, each column total is first divided into **n** (5 by default) sub-sections respectively. To be more specific, in *Collocation Extractor* and *Colligation Extractor*, all collocates where Word 1 appears as node and the other collocates where Word 1 does not appear as node are divided into **n** parts respectively. And in *Keyword Extractor*, all tokens in the observed file and all tokens in the reference files are equally divided into **n** parts respectively.

The frequencies of *Word 2* (in *Collocation Extractor* and *Colligation Extractor*) or *Word w* (in *Keyword Extractor*) in each sub-section of the 2 column totals are counted and denoted by **F₁₁**, **F₂₁**, **F₃₁**, ..., **Fₙ₁**, and **F₁₂**, **F₂₂**, **F₃₂**, ..., **Fₙ₂** respectively. The total frequency of *Word 2* (in *Collocation Extractor* and *Colligation Extractor*) or *Word w* (in *Keyword Extractor*) in the 2 column totals are denoted by **Fₓ₁** and **Fₓ₂** respectively. The mean value of the frequencies over all sub-sections in the 2 column totals are denoted by ![f_x1_bar](/doc/measures/f_x1_bar.svg) and ![f_x2_bar](/doc/measures/f_x2_bar.svg) respectively.

Then the test statistic, Bayes factor, and effect size are calculated as follows:

<!--
Log-likelihood Ratio:
    \begin{align*}
        \text{G} &= 2 \times \sum_{i = 1}^2 \sum_{j = 1}^2 \left(O_{ij} \times \ln \frac{O_{ij}}{E_{ij}}\right) \\
        \text{BF} &= \text{G} - \ln O_{xx}
    \end{align*}

Pearson's Chi-squared Test:
    \chi^2 = \sum_{i = 1}^2 \sum_{j = 1}^2 \frac{\left(O_{ij} - E{ij}\right)^2}{E_{ij}}

Student's t-test (1-sample):
    \text{t} = \frac{O_{11} - E_{11}}{\sqrt{O_{11} \times \left(1 - \frac{O_{11}}{O_{xx}}\right)}}

Student's t-test (2-sample):
    \begin{align*}
        \text{s}_1 &= \frac{\sum_{i = 1}^n (F_{i1} - \overline{F_{x1}})^2}{n - 1} \\
        \text{s}_2 &= \frac{\sum_{i = 1}^n (F_{i2} - \overline{F_{x2}})^2}{n - 1} \\
        \text{t} &= \frac{\overline{F_{x1}} - \overline{F_{x2}}}{\sqrt{\frac{\text{s}_1 - \text{s}_2}{n}}} \\
        \text{BF} &= \text{t}^2 - \ln(2 \times n)
    \end{align*}

z-score:
    \text{z} = \frac{O_{11} - E_{11}}{\sqrt{E_{11} \times \left(1 - \frac{E_{11}}{O_{xx}}\right)}}

z-score (Berry-Rogghe):
    \begin{align*}
        \text{p} &= \frac{O_{x1}}{O_{xx} - O_{1x}} \\
        \text{E} &= \text{p} \times O_{1x} \times \text{S} \\
        \text{z} &= \frac{O_{11} - \text{E}}{\sqrt{\text{E} \times (1 - \text{p})}}
    \end{align*}
-->

Test of Statistical Significance|Measure of Bayes Factor|Formula
--------------------------------|-----------------------|-------
<span id="ref-fishers-exact-test"></span>Fisher's Exact Test<br>([Pedersen, 1996](#ref-pedersen-1996))||See: [Fisher's exact test - Wikipedia](https://en.wikipedia.org/wiki/Fisher%27s_exact_test#Example)
<span id="ref-log-likehood-ratio-test"></span>Log-likelihood Ratio Test<br>([Dunning, 1993](#ref-dunning-1993))|Log-likelihood Ratio Test<br>([Wilson, 2013](#ref-wilson-2013))|![Formula](/doc/measures/statistical_significance/log_likehood_ratio_test.svg)
<span id="ref-mann-whiteney-u-test"></span>Mann-Whitney U Test<br>([Kilgarriff, 2001](#ref-kilgarriff-2001))||See: [Mann–Whitney U test - Wikipedia](https://en.wikipedia.org/wiki/Mann%E2%80%93Whitney_U_test#Calculations)
<span id="ref-pearsons-chi-squared-test"></span>Pearson's Chi-squared Test<br>([Hofland & Johanson, 1982](#ref-hofland-johanson-1982); [Oakes, 1998](#ref-oakes-1998))||![Formula](/doc/measures/statistical_significance/pearsons_chi_squared_test.svg)
<span id="ref-students-t-test-1-sample"></span>Student's t-test (1-sample)<br>([Church et al., 1991](#ref-church-et-al-1991))||![Formula](/doc/measures/statistical_significance/students_t_test_1_sample.svg)
<span id="ref-students-t-test-2-sample"></span>Student's t-test (2-sample)<br>([Paquot & Bestgen, 2009](#ref-paquot-bestgen-2009))|Student's t-test (2-sample)<br>([Wilson, 2013](#ref-wilson-2013))|![Formula](/doc/measures/statistical_significance/students_t_test_2_sample.svg)
<span id="ref-welchs-t-test"></span>Welch's t-test||* Same as Student's t-test (2-sample), but with different degrees of freedom (hence a different p-value).
<span id="ref-z-score"></span>z-score<br>([Dennis, 1964](#ref-dennis-1964))||![Formula](/doc/measures/statistical_significance/z_score.svg)
<span id="ref-z-score-berry-rogghes"></span>z-score (Berry-Rogghe)<br>([Berry-Rogghe, 1973](#ref-berry-rogghe-1973))||![Formula](/doc/measures/statistical_significance/z_score_berry_rogghe.svg)<br>where **S** is the average span size on both sides of the node word.

<!--
%DIFF:
    \text{%DIFF} = \frac{\left(\frac{O_{11}}{O_{x1}} - \frac{O_{12}}{O_{x2}}\right) \times 100}{\frac{O_{12}}{O_{x2}}}

Cubic Association Ratio:
    \text{IM}^3 = \log_{2} \frac{{O_{11}}^3}{E_{11}}

Dice's Coefficient:
    \text{DSC} = \frac{2 \times O_{11}}{O_{1x} + O_{x1}}

Difference Coefficient:
    \text{Difference Coefficient} = \frac{\frac{O_{11}}{O_{x1}} - \frac{O_{12}}{O_{x2}}}{\frac{O_{11}}{O_{x1}} + \frac{O_{12}}{O_{x2}}}

Jaccard Index:
    \text{J} = \frac{O_{11}}{O_{11} + O_{12} + O_{21}}

Kilgarriff's Ratio:
    \text{Kilgarriff's Ratio} = \frac{\frac{O_{11}}{O_{11} + O_{21}} \times 1000000 + \alpha}{\frac{O_{12}}{O_{12} + O_{22}} \times 1000000 + \alpha}

Log Ratio:
    \text{Log Ratio} = \log_{2} \frac{\frac{O_{11}}{O_{x1}}}{\frac{O_{12}}{O_{x2}}}

Log-Frequency Biased MD:
    \text{LFMD} = \log_{2} \frac{O_{11}}{E_{11}} + \log_{2} O_{11}

logDice:
    \text{logDice} = 14 + \log_{2} \frac{2 \times O_{11}}{O_{1x} + O_{x1}}

MI.log-f:
    \text{MI.log-f} = \log_{2} \frac{{O_{11}}^2}{E_{11}} \times \ln (O_{11} + 1)

Minimum Sensitivity:
    \text{S} = \min\left\{\frac{O_{11}}{O_{1x}},\;\frac{O_{11}}{O_{x1}}\right\}

Mutual Dependency:
    \text{MD} = \log_{2} \frac{{O_{11}}^2}{E_{11}}

Mutual Expectation:
    \text{ME} = O_{11} \times \frac{2 \times O_{11}}{O_{1x} + O_{x1}}

Mutual Information:
    \text{MI} = \sum_{i = 1}^n \sum_{j = 1}^n \left(\frac{O_{ij}}{O_{xx}} \times \log_{2} \frac{O_{ij}}{E_{ij}}\right)

Odds Ratio:
    \text{Odd's Ratio} = \frac{O_{11} \times O_{22}}{O_{12} \times O_{21}}

Pointwise Mutual Information:
    \text{PMI} = \log_{2} \frac{O_{11}}{E_{11}}

Poisson Collocation Measure:
    \text{sig} = \frac{O_{11} \times (\ln O_{11} - \ln E_{11} - 1)}{\ln O_{xx}}

Squared Phi Coefficient:
    \phi^2 = \frac{(O_{11} \times O_{22} - O_{12} \times O_{21})^2}{O_{1x} \times O_{2x} \times O_{x1} \times O_{x2}}
-->

Measure of Effect Size|Formula
----------------------|-------
<span id="ref-pct-diff"></span>%DIFF<br>([Gabrielatos & Marchi, 2012](#ref-gabrielatos-marchi-2012))|![Formula](/doc/measures/effect_size/pct_diff.svg)
Cubic Association Ratio<br>([Daille, 1994](#ref-daille-1994), [1995](#ref-daille-1995))|![Formula](/doc/measures/effect_size/im3.svg)
<span id="ref-dices-coeff"></span>Dice's Coefficient<br>([Smadja et al., 1996](#ref-smadja-et-al-1996))|![Formula](/doc/measures/effect_size/dices_coeff.svg)
<span id="ref-diff-coeff"></span>Difference Coefficient<br>([Hofland & Johanson, 1982](#ref-hofland-johanson-1982); [Gabrielatos, 2018](#ref-gabrielatos-2018))|![Formula](/doc/measures/effect_size/diff_coeff.svg)
<span id="ref-jaccard-index"></span>Jaccard Index<br>([Dunning, 1998](#ref-dunning-1998))|![Formula](/doc/measures/effect_size/jaccard_index.svg)
<span id="ref-kilgarriffs-ratio"></span>Kilgarriff's Ratio<br>([Kilgarriff, 2009](#ref-kilgarriff-2009))|![Formula](/doc/measures/effect_size/kilgarriffs_ratio.svg)<br>where **α** is the smoothing parameter, whose value could be changed via **Menu → Preferences → Settings → Measures → Effect Size → Kilgarriff's Ratio → Smoothing Parameter**.
<span id="ref-log-ratio"></span>Log Ratio<br>([Hardie, 2014](#ref-hardie-2014))|![Formula](/doc/measures/effect_size/log_ratio.svg)
<span id="ref-lfmd"></span>Log-Frequency Biased MD<br>([Thanopoulos et al., 2002](#ref-thanopoulos-et-al-2002))|![Formula](/doc/measures/effect_size/lfmd.svg)
<span id="ref-log-dice"></span>logDice<br>([Rychlý, 2008](#ref-rychly-2008))|![Formula](/doc/measures/effect_size/log_dice.svg)
<span id="ref-mi-log-f"></span>MI.log-f<br>([Lexical Computing Ltd., 2015](#ref-lexical-computing-ltd-2015); [Kilgarriff & Tugwell, 2002](#ref-kilgarriff-tugwell-2002))|![Formula](/doc/measures/effect_size/mi_log_f.svg)
<span id="ref-min-sensitivity"></span>Minimum Sensitivity<br>([Pedersen, 1998](#ref-pedersen-1998))|![Formula](/doc/measures/effect_size/min_sensitivity.svg)
<span id="ref-effect-size"></span>Mutual Dependency<br>([Thanopoulos et al., 2002](#ref-thanopoulos-et-al-2002))|![Formula](/doc/measures/effect_size/md.svg)
<span id="ref-me"></span>Mutual Expectation<br>([Dias et al., 1999](#ref-dias-et-al-1999))|![Formula](/doc/measures/effect_size/me.svg)
<span id="ref-mi"></span>Mutual Information<br>([Dunning, 1998](#ref-dunning-1998))|![Formula](/doc/measures/effect_size/mi.svg)
<span id="ref-odds-ratio"></span>Odds Ratio<br>([Pojanapunya & Todd, 2016](#ref-pojanapunya-todd-2016))|![Formula](/doc/measures/effect_size/odds_ratio.svg)
<span id="ref-pmi"></span>Pointwise Mutual Information<br>([Church & Hanks, 1990](#ref-church-hanks-1990))|![Formula](/doc/measures/effect_size/pmi.svg)
<span id="ref-poisson-collocation-measure"></span>Poisson Collocation Measure<br>([Quasthoff & Wolff, 2002](#ref-quasthoff-wolff-2002))|![Formula](/doc/measures/effect_size/poisson_collocation_measure.svg)
<span id="ref-squared-phi-coeff"></span>Squared Phi Coefficient<br>([Church & Gale, 1991](#ref-church-gale-1991))|![Formula](/doc/measures/effect_size/squared_phi_coeff.svg)

<span id="doc-5"></span>
## [5 References](#doc)
<span id="ref-altamimi-et-al-2013"></span>
[1] [**^**](#ref-aari) Al-Tamimi, A., Jaradat M., Aljarrah, N., & Ghanim, S. (2013). AARI: Automatic Arabic readability index. *The International Arab Journal of Information Technology*, *11*(4), pp. 370–378.<br>
<span id="ref-anderson-1983"></span>
[2] [**^**](#ref-re) Amstad, T. (1978). *Wie verständlich sind unsere Zeitungen?* [Unpublished doctoral dissertation]. University of Zurich.<br>
<span id="ref-anderson-1983"></span>
[3] [**^**](#ref-rix) Anderson, J. (1983). Lix and Rix: Variations on a little-known readability index. *Journal of Reading*, *26*(6), pp. 490–496.<br>
<span id="ref-bamberger-vanecek-1984"></span>
[4] [**^**](#ref-wstf) Bamberger, R., & Vanecek, E. (1984). *Lesen – Verstehen – Lernen – Schreiben*. Jugend und Volk.<br>
<span id="ref-berry-rogghe-1973"></span>
[5] [**^**](#ref-z-score-berry-rogghes) Berry-Rogghe, G. L. M. (1973). The computation of collocations and their relevance in lexical studies. In A. J. Aiken, R. W. Bailey, & N. Hamilton-Smith (Eds.), *The computer and literary studies* (pp. 103–112). Edinburgh University Press.<br>
<span id="ref-bormuth-1969"></span>
[6] [**^**](#ref-bormuths-cloze-mean-gp) Bormuth, J. R. (1969). *Development of readability analyses*. U.S. Department of Health, Education, and Welfare. http://files.eric.ed.gov/fulltext/ED029166.pdf<br>
<span id="ref-bjornsson-1968"></span>
[7] [**^**](#ref-lix) Björnsson, C.-H. (1968). *Läsbarhet*. Liber.<br>
<span id="ref-brouwer-1963"></span>
[8] [**^**](#ref-re) Brouwer, R. H. M. (1963). Onderzoek naar de leesmoeilijkheid van Nederlands proza. *Paedagogische studiën*, *40*, 454–464. https://objects.library.uu.nl/reader/index.php?obj=1874-205260&lan=en<br>
<span id="ref-carroll-1970"></span>
[9] [**^**](#ref-carrolls-d2)[**^**](#ref-carrolls-um) Carroll, J. B. (1970). An alternative to Juilland’s usage coefficient for lexical frequencies and a proposal for a standard frequency index. *Computer Studies in the Humanities and Verbal Behaviour*, *3*(2), 61–65. https://doi.org/10.1002/j.2333-8504.1970.tb00778.x<br>
<span id="ref-caylor-et-al-1973"></span>
[10] [**^**](#ref-rgl) Caylor, J. S., Sticht, T. G., Fox, L. C., & Ford, J. P. (1973). *Methodologies for determining reading requirements of military occupational specialties*. Human Resource Research Organization. https://files.eric.ed.gov/fulltext/ED074343.pdf<br>
<span id="ref-chall-dale-1995"></span>
[11] [**^**](#ref-dale-chall-readability-formula-new) Chall, J. S., & Dale, E. (1995). *Readability revisited: The new Dale-Chall readability formula*. Brookline Books.<br>
<span id="ref-church-gale-1991"></span>
[12] [**^**](#ref-squared-phi-coeff) Church, K. W., & Gale, W. A. (1991, September 29–October 1). Concordances for parallel text [Paper presentation]. Using Corpora: Seventh Annual Conference of the UW Centre for the New OED and Text Research, St. Catherine's College, Oxford, United Kingdom.<br>
<span id="ref-church-et-al-1991"></span>
[13] [**^**](#ref-students-t-test-1-sample) Church, K., Gale, W., Hanks, P., & Hindle, D. (1991). Using statistics in lexical analysis. In U. Zernik (Ed.), *Lexical acquisition: Exploiting on-line resources to build a lexicon* (pp. 115–164). Psychology Press.<br>
<span id="ref-church-hanks-1990"></span>
[14] [**^**](#ref-pmi) Church, K. W., & Hanks, P. (1990). Word association norms, mutual information, and lexicography. *Computational Linguistics*, *16*(1), 22–29.<br>
<span id="ref-coleman-liau-1975"></span>
[15] [**^**](#ref-coleman-liau-index) Coleman, M., & Liau, T. L. (1975). A computer readability formula designed for machine scoring. *Journal of Applied Psychology*, *60*(2), 283–284. https://doi.org/10.1037/h0076540<br>
<span id="ref-college-entrance-examination-board-1981"></span>
[16] [**^**](#ref-drp) College Entrance Examination Board. (1981). *Degrees of reading power brings the students and the text together*.<br>
<span id="ref-crawford-1985"></span>
[17] [**^**](#ref-formula-de-crawford) Crawford, A. N. (1985). Fórmula y gráfico para determinar la comprensibilidad de textos de nivel primario en castellano. *Lectura y Vida*, *6*(4). http://www.lecturayvida.fahce.unlp.edu.ar/numeros/a6n4/06_04_Crawford.pdf<br>
<span id="ref-daille-1994"></span>
[18] [**^**](#ref-im3) Daille, B. (1994). *Approche mixte pour l'extraction automatique de terminologie: statistiques lexicales et filtres linguistiques* [Doctoral thesis, Paris Diderot University]. Béatrice Daille. http://www.bdaille.com/index.php?option=com_docman&task=doc_download&gid=8&Itemid=<br>
<span id="ref-daille-1995"></span>
[19] [**^**](#ref-im3) Daille, B. (1995). Combined approach for terminology extraction: Lexical statistics and linguistic filtering. *UCREL technical papers* (Vol. 5). Lancaster University.<br>
<span id="ref-dale-1931"></span>
[20] [**^**](#ref-num-words-dale-769) [**^**](#ref-spache-grade-level) Dale, E. (1931). A comparison of two word lists. *Educational Research Bulletin*, *10*(18), 484–489.<br>
<span id="ref-dale-chall-1948a"></span>
[21] [**^**](#ref-dale-chall-readability-formula) Dale, E., & Chall, J. S. (1948a). A formula for predicting readability. *Educational Research Bulletin*, *27*(1), 11–20, 28.<br>
<span id="ref-dale-chall-1948b"></span>
[22] [**^**](#ref-num-words-dale-3000) [**^**](#ref-dale-chall-readability-formula) Dale, E., & Chall, J. S. (1948b). A formula for predicting readability: Instructions. *Educational Research Bulletin*, *27*(2), 37–54.<br>
<span id="ref-danielson-bryan-1963"></span>
[23] [**^**](#ref-danielson-bryans-readability-formula) Danielson, W. A., & Bryan, S. D. (1963). Computer automation of two readability formulas. *Journalism Quarterly*, *40*(2), 201–206. https://doi.org/10.1177/107769906304000207<br>
<span id="ref-dennis-1964"></span>
[24] [**^**](#ref-z-score) Dennis, S. F. (1964). The construction of a thesaurus automatically from a sample of text. In M. E. Stevens, V. E. Giuliano, & L. B. Heilprin (Eds.), *Proceedings of the symposium on statistical association methods for mechanized documentation* (pp. 61–148). National Bureau of Standards.<br>
<span id="ref-dias-et-al-1999"></span>
[25] [**^**](#ref-me) Dias, G., Guilloré, S., & Pereira Lopes, J. G. (1999). Language independent automatic acquisition of rigid multiword units from unrestricted text corpora. In A. Condamines, C. Fabre, & M. Péry-Woodley (Eds.), *TALN'99: 6ème Conférence Annuelle Sur le Traitement Automatique des Langues Naturelles* (pp. 333–339). TALN.<br>
<span id="ref-douma-1960"></span>
[26] [**^**](#ref-re) Douma, W. H. (1960). *De leesbaarheid van landbouwbladen: Een onderzoek naar en een toepassing van leesbaarheidsformules* [Readability of Dutch farm papers: A discussion and application of readability-formulas]. Afdeling sociologie en sociografie van de Landbouwhogeschool Wageningen. https://edepot.wur.nl/276323<br>
<span id="ref-dunning-1993"></span>
[27] [**^**](#ref-log-likehood-ratio-test) Dunning, T. E. (1993). Accurate methods for the statistics of surprise and coincidence. *Computational Linguistics*, *19*(1), 61–74.<br>
<span id="ref-dunning-1998"></span>
[28] [**^**](#ref-jaccard-index)[**^**](#ref-mi) Dunning, T. E. (1998). *Finding structure in text, genome and other symbolic sequences* [Doctoral dissertation, University of Sheffield]. arXiv. arxiv.org/pdf/1207.1847.pdf<br>
<span id="ref-elhaj-rayson-2016"></span>
[29] [**^**](#ref-osman) El-Haj, M., & Rayson, P. (2016). OSMAN: A novel Arabic readability metric. In N. Calzolari, K. Choukri, T. Declerck, S. Goggi, M. Grobelnik, B. Maegaard, J. Mariani, H. Mazo, A. Moreno, J. Odijk, & S. Piperidis (Eds.), *Proceedings of the Tenth International Conference on Language Resources and Evaluation (LREC 2016)* (pp. 250–255). European Language Resources Association. http://www.lrec-conf.org/proceedings/lrec2016/index.html<br>
<span id="ref-engwall-1974"></span>
[30] [**^**](#ref-engwalls-fm) Engwall, G. (1974). *Fréquence et distribution du vocabulaire dans un choix de romans français* [Unpublished doctoral dissertation]. Stockholm University.<br>
<span id="ref-fang-1966"></span>
[31] [**^**](#ref-elf) Fang, I. E. (1966). The easy listening formula. *Journal of Broadcasting*, *11*(1), 63–68. https://doi.org/10.1080/08838156609363529<br>
<span id="ref-farr-et-al-1951"></span>
[32] [**^**](#ref-re-simplified) Farr, J. N., Jenkins, J. J., & Paterson, D. G. (1951). Simplification of Flesch reading ease formula. *Journal of Applied Psychology*, *35*(5), 333–337. https://doi.org/10.1037/h0062427<br>
<span id="ref-fernandez-huerta-1959"></span>
[33] [**^**](#ref-re) Fernández Huerta, J. (1959). Medidas sencillas de lecturabilidad. *Consigna*, *214*, 29–32.<br>
<span id="ref-flesch-1948"></span>
[34] [**^**](#ref-re) Flesch, R. (1948). A new readability yardstick. *Journal of Applied Psychology*, *32*(3), 221–233. https://doi.org/10.1037/h0057532<br>
<span id="ref-flesch-1948"></span>
[35] [**^**](#ref-re) Franchina, V., & Vacca, R. (1986). Adaptation of Flesh readability index on a bilingual text written by the same author both in Italian and English languages. *Linguaggi*, *3*, 47–49.<br>
<span id="ref-fucks-1955"></span>
[36] [**^**](#ref-fuckss-stilcharakteristik) Fucks, W. (1955). *Unterschied des Prosastils von Dichtern und anderen Schriftstellern: ein Beispiel mathematischer Stilanalyse*. Bouvier.<br>
<span id="ref-gabrielatos-2018"></span>
[37] [**^**](#ref-diff-coeff) Gabrielatos, C. (2018). Keyness analysis: Nature, metrics and techniques. In C. Taylor & A. Marchi (Eds.), *Corpus approaches to discourse: A critical review* (pp. 225–258). Routledge.<br>
<span id="ref-gabrielatos-marchi-2012"></span>
[38] [**^**](#ref-pct-diff) Gabrielatos, C., & Marchi, A. (2012, September 13–14). *Keyness: Appropriate metrics and practical issues* [Conference session]. CADS International Conference 2012, University of Bologna, Italy.<br>
<span id="ref-gries-2008"></span>
[39] [**^**](#ref-griess-dp) Gries, S. T. (2008). Dispersions and adjusted frequencies in corpora. *International Journal of Corpus Linguistics*, *13*(4), 403–437. https://doi.org/10.1075/ijcl.13.4.02gri<br>
<span id="ref-gunning-1968"></span>
[40] [**^**](#ref-fog-index) Gunning, R. (1968). *The technique of clear writing* (revised ed.). McGraw-Hill Book Company.<br>
<span id="ref-gutierrez-de-polini-1972"></span>
[41] [**^**](#ref-cp) Gutiérrez de Polini, L. E. (1972). *Investigación sobre lectura en Venezuela* [Paper presentation]. Primeras Jornadas de Educación Primaria, Ministerio de Educación, Caracas, Venezuela.<br>
<span id="ref-hardie-2014"></span>
[42] [**^**](#ref-log-ratio) Hardie, A. (2014, April 28). *Log ratio: An informal introduction*. ESRC Centre for Corpus Approaches to Social Science (CASS). http://cass.lancs.ac.uk/log-ratio-an-informal-introduction/.<br>
<span id="ref-hofland-johanson-1982"></span>
[43] [**^**](#ref-pearsons-chi-squared-test)[**^**](#ref-diff-coeff) Hofland, K., & Johanson, S. (1982). *Word frequencies in British and American English*. Norwegian Computing Centre for the Humanities.<br>
<span id="ref-juilland-chang-rodrigues-1964"></span>
[44] [**^**](#ref-juillands-d)[**^**](#ref-juillands-u) Juilland, A., & Chang-Rodriguez, E. (1964). *Frequency dictionary of Spanish words*. Mouton.<br>
<span id="ref-kandel-moles-1958"></span>
[45] [**^**](#ref-re) Kandel, L., & Moles A. (1958). Application de l’indice de flesch la langue francaise [applying flesch index to french language]. *The Journal of Educational Research*, *21*, 283–287.<br>
<span id="ref-kilgarriff-2001"></span>
[46] [**^**](#ref-mann-whiteney-u-test) Kilgarriff, A. (2001). Comparing corpora. *International Journal of Corpus Linguistics*, *6*(1), 232–263. https://doi.org/10.1075/ijcl.6.1.05kil<br>
<span id="ref-kilgarriff-2009"></span>
[47] [**^**](#ref-kilgarriffs-ratio) Kilgarriff, A. (2009). Simple maths for keywords. In M. Mahlberg, V. González-Díaz, & C. Smith (Eds.), *Proceedings of the Corpus Linguistics Conference 2009* (p. 171). University of Liverpool.<br>
<span id="ref-kilgarriff-tugwell-2002"></span>
[48] [**^**](#ref-mi-log-f) Kilgarriff, A., & Tugwell, D. (2002). WASP-bench: An MT lexicographers' workstation supporting state-of-the-art lexical disambiguation. In *Proceedings of the 8th Machine Translation Summit* (pp. 187–190). European Association for Machine Translation.<br>
<span id="ref-kincaid-et-al-1975"></span>
[49] [**^**](#ref-ari) [**^**](#ref-gl) [**^**](#ref-fog-index) Kincaid, J. P., Fishburne, R. P., Rogers, R. L., & Chissom, B. S. (1975). *Derivation of new readability formulas (automated readability index, fog count, and Flesch reading ease formula) for Navy enlisted personnel* (Report No. RBR 8-75). Naval Air Station Memphis. https://apps.dtic.mil/sti/pdfs/ADA006655.pdf<br>
<span id="ref-kromer-2003"></span>
[50] [**^**](#ref-kromers-ur) Kromer, V. (2003). A usage measure based on psychophysical relations. *Journal of Quantitative Linguistics*, *10*(2), 177–186. https://doi.org/10.1076/jqul.10.2.177.16718<br>
<span id="ref-lexical-computing-ltd-2015"></span>
[51] [**^**](#ref-mi-log-f) Lexical Computing. (2015, July 8). *Statistics used in Sketch Engine*. Sketch Engine. https://www.sketchengine.eu/documentation/statistics-used-in-sketch-engine/<br>
<span id="ref-coleman-et-al-1976"></span>
[52] [**^**](#ref-colemans-readability-formula) Liau, T. L., Bassin, C. B., Martin, C. J., & Coleman, E. B. (1976). Modification of the Coleman readability formulas. *Journal of Reading Behavior*, *8*(4), 381–386. https://journals.sagepub.com/doi/pdf/10.1080/10862967609547193<br>
<span id="ref-lijffijt-gries-2012"></span>
[53] [**^**](#ref-griess-dp-norm) Lijffijt, J., & Gries, S. T. (2012). Correction to Stefan Th. Gries’ “dispersions and adjusted frequencies in corpora”. *International Journal of Corpus Linguistics*, *17*(1), 147–149. https://doi.org/10.1075/ijcl.17.1.08lij<br>
<span id="ref-lucisano-emanuela-piemontese-1988"></span>
[54] [**^**](#ref-gulpease-index) Lucisano, P., & Emanuela Piemontese, M. (1988). GULPEASE: A formula for the prediction of the difficulty of texts in Italian. *Scuola e Città*, *39*(3), pp. 110–124.<br>
<span id="ref-lyne-1985"></span>
[55] [**^**](#ref-lynes-d3) Lyne, A. A. (1985). Dispersion. In *The vocabulary of French business correspondence: Word frequencies, collocations, and problems of lexicometric method* (pp. 101–124). Slatkine/Champion.<br>
<span id="ref-mclaughlin-1969"></span>
[56] [**^**](#ref-smog-grade) McLaughlin, G. H. (1969). SMOG grading: A new readability formula. *Journal of Reading*, *12*(8), pp. 639–646.<br>
<span id="ref-munoz-baquedano-2006"></span>
[57] [**^**](#ref-mu) Muñoz Baquedano, M. (2006). Legibilidad y variabilidad de los textos. *Boletín de Investigación Educacional, Pontificia Universidad Católica de Chile*, *21*(2), 13–26.<br>
<span id="ref-nirmaldasan-2009"></span>
[58] [**^**](#ref-eflaw) Nirmaldasan. (2009, April 30). *McAlpine EFLAW readability score*. Readability Monitor. Retrieved November 15, 2022, from https://strainindex.wordpress.com/2009/04/30/mcalpine-eflaw-readability-score/<br>
<span id="ref-oakes-1998"></span>
[59] [**^**](#ref-pearsons-chi-squared-test) Oakes, M. P. (1998). *Statistics for Corpus Linguistics*. Edinburgh University Press.<br>
<span id="ref-oborneva-2006"></span>
[60] [**^**](#ref-re) Oborneva, I. V. (2006). *Автоматизированная оценка сложности учебных текстов на основе статистических параметров* [Doctoral dissertation, Institute for Strategy of Education Development of the Russian Academy of Education]. Freereferats.ru. https://static.freereferats.ru/_avtoreferats/01002881899.pdf?ver=3<br>
<span id="ref-o-hayre-1966"></span>
[61] [**^**](#ref-lensear-write) O’Hayre, J. (1966). *Gobbledygook has gotta go*. U.S. Government Printing Office. https://www.governmentattic.org/15docs/Gobbledygook_Has_Gotta_Go_1966.pdf<br>
<span id="ref-paquot-bestgen-2009"></span>
[62] [**^**](#ref-students-t-test-2-sample) Paquot, M., & Bestgen, Y. (2009). Distinctive words in academic writing: A comparison of three statistical tests for keyword extraction. *Language and Computers*, *68*, 247–269.<br>
<span id="ref-pedersen-1996"></span>
[63] [**^**](#ref-fishers-exact-test) Pedersen, T. (1996). Fishing for exactness. In T. Winn (Ed.), *Proceedings of the Sixth Annual South-Central Regional SAS Users' Group Conference* (pp. 188–200). The South–Central Regional SAS Users' Group.<br>
<span id="ref-pedersen-1998"></span>
[64] [**^**](#ref-min-sensitivity) Pedersen, T. (1998). Dependent bigram identification. In *Proceedings of the Fifteenth National Conference on Artificial Intelligence* (p. 1197). AAAI Press.<br>
<span id="ref-pisarek-1969"></span>
[65] [**^**](#ref-fog-index) Pisarek, W. (1969). Jak mierzyć zrozumiałość tekstu?. *Zeszyty Prasoznawcze*, *4*(42), 35–48.<br>
<span id="ref-pojanapunya-todd-2016"></span>
[66] [**^**](#ref-odds-ratio) Pojanapunya, P., & Todd, R. W. (2016). Log-likelihood and odds ratio keyness statistics for different purposes of keyword analysis. *Corpus Linguistics and Linguistic Theory*, *15*(1), pp. 133–167. https://doi.org/10.1515/cllt-2015-0030<br>
<span id="ref-quasthoff-wolff-2002"></span>
[67] [**^**](#ref-poisson-collocation-measure) Quasthoff, U., & Wolff, C. (2002). The poisson collocation measure and its applications. *Proceedings of 2nd International Workshop on Computational Approaches to Collocations*. IEEE.<br>
<span id="ref-rosengren-1971"></span>
[68] [**^**](#ref-rosengrens-s)[**^**](#ref-rosengrens-kf) Rosengren, I. (1971). The quantitative concept of language and its relation to the structure of frequency dictionaries. *Études de linguistique appliquée*, *1*, 103–127.<br>
<span id="ref-rychly-2008"></span>
[69] [**^**](#ref-log-dice) Rychlý, P. (2008). A lexicographyer-friendly association score. In P. Sojka & A. Horák (Eds.), *Proceedings of Second Workshop on Recent Advances in Slavonic Natural Languages Processing*. Masaryk University<br>
<span id="ref-savicky-hlavacova-2002"></span>
[70] [**^**](#ref-ald) [**^**](#ref-fald) [**^**](#ref-arf) [**^**](#ref-farf) [**^**](#ref-awt) [**^**](#ref-fawt) Savický, P., & Hlaváčová, J. (2002). Measures of word commonness. *Journal of Quantitative Linguistics*, *9*(3), 215–231. https://doi.org/10.1076/jqul.9.3.215.14124<br>
<span id="ref-smadja-et-al-1996"></span>
[71] [**^**](#ref-dices-coeff) Smadja, F., McKeown, K. R., & Hatzivassiloglou, V. (1996). Translating collocations for bilingual lexicons: A statistical approach. *Computational Linguistics*, *22*(1), pp. 1–38.<br>
<span id="ref-smith-1961"></span>
[72] [**^**](#ref-devereux-readability-index) Smith, E. A. (1961). Devereaux readability index. *Journal of Educational Research*, *54*(8), 298–303. https://doi.org/10.1080/00220671.1961.10882728<br>
<span id="ref-smith-senter-1967"></span>
[73] [**^**](#ref-ari) Smith, E. A., & Senter, R. J. (1967). *Automated readability index*. Aerospace Medical Research Laboratories. https://apps.dtic.mil/sti/pdfs/AD0667273.pdf<br>
<span id="ref-spache-1953"></span>
[74] [**^**](#ref-spache-grade-level) Spache, G. (1953). A new readability formula for primary-grade reading materials. *Elementary School Journal*, *53*(7), 410–413. https://doi.org/10.1086/458513<br>
<span id="ref-spache-1974"></span>
[75] [**^**](#ref-num-words-spache) [**^**](#ref-spache-grade-level) Spache, G. (1974). *Good reading for poor readers* (Rev. 9th ed.). Garrard.<br>
<span id="ref-szigrisze-pazos-1993"></span>
[76] [**^**](#ref-re) Szigriszt Pazos, F. (1993). *Sistemas predictivos de legibilidad del mensaje escrito: Formula de perspicuidad* [Doctoral dissertation, Complutense University of Madrid]. Biblos-e Archivo. https://repositorio.uam.es/bitstream/handle/10486/2488/3907_barrio_cantalejo_ines_maria.pdf?sequence=1&isAllowed=y<br>
<span id="ref-thanopoulos-et-al-2002"></span>
[77] [**^**](#ref-lfmd)[**^**](#ref-md) Thanopoulos, A., Fakotakis, N., & Kokkinakis, G. (2002). Comparative evaluation of collocation extraction metrics. In M. G. González & C. P. S. Araujo (Eds.), *Proceedings of the Third International Conference on Language Resources and Evaluation* (pp. 620–625). European Language Resources Association.<br>
<span id="ref-wilson-2013"></span>
[78] [**^**](#ref-log-likehood-ratio-test)[**^**](#ref-students-t-test-2-sample) Wilson, A. (2013). Embracing Bayes Factors for key item analysis in corpus linguistics. In M. Bieswanger & A. Koll-Stobbe (Eds.), *New Approaches to the Study of Linguistic Variability* (pp. 3–11). Peter Lang.<br>
<span id="ref-zhang-2004"></span>
[79] [**^**](#ref-zhangs-distributional-consistency) Zhang, H., Huang, C., & Yu, S. (2004). Distributional consistency: As a general method for defining a core lexicon. In M. T. Lino, M. F. Xavier, F. Ferreira, R. Costa, & R. Silva (Eds.), *Proceedings of Fourth International Conference on Language Resources and Evaluation* (pp. 1119–1122). European Language Resources Association.<br>

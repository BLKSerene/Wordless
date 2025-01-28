<!----------------------------------------------------------------------
# Documentation: Documentation - English
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
# --------------------------------------------------------------------->

<div align="center"><h1>📖 Documentation</h1></div>

<span id="doc"></span>
## Table of Contents
- [1 Main Window](#doc-1)
- [2 File Area](#doc-2)
- [3 Profiler](#doc-3)
- [4 Concordancer](#doc-4)
- [5 Parallel Concordancer](#doc-5)
- [6 Dependency Parser](#doc-6)
- [7 Wordlist Generator](#doc-7)
- [8 N-gram Generator](#doc-8)
- [9 Collocation Extractor](#doc-9)
- [10 Colligation Extractor](#doc-10)
- [11 Keyword Extractor](#doc-11)
- [12 Appendixes](#doc-12)
  - [12.1 Supported Languages](#doc-12-1)
  - [12.2 Supported File Types](#doc-12-2)
  - [12.3 Supported File Encodings](#doc-12-3)
  - [12.4 Supported Measures](#doc-12-4)
    - [12.4.1 Readability Formulas](#doc-12-4-1)
    - [12.4.2 Indicators of Lexical Density/Diversity](#doc-12-4-2)
    - [12.4.3 Measures of Dispersion and Adjusted Frequency](#doc-12-4-3)
    - [12.4.4 Tests of Statistical Significance, Measures of Bayes Factor, and Measures of Effect Size](#doc-12-4-4)
- [13 References](#doc-13)

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

  You can show/hide the *Status Bar* by checking/unchecking **Menu Bar → Preferences → Show Status Bar**

You can modify the global scaling factor and font settings of the user interface via **Menu Bar → Preferences → General → User Interface Settings**.

<span id="doc-2"></span>
## [2 File Area](#doc)
In most cases, the first thing to do in *Wordless* is open and select your files to be processed via **Menu Bar → File → Open Files/Folder**.

Files are loaded, cached and selected automatically after being added to the *File Table*. **Only selected files will be processed by *Wordless***. You can drag and drop files around the *File Table* to change their orders, which would be reflected in the results.

By default, *Wordless* would try to detect the encoding and language settings of all files for you, you should double check and make sure that the settings of each and every file are correct. If you prefer changing file settings manually, you could uncheck ***Open Files* dialog → Auto-detect encodings** and/or ***Open Files* dialog → Auto-detect languages**. The default file settings could be modified via **Menu Bar → Preferences → Settings → Files → Default Settings**. Additionally, you need to change ***Open Files* dialog → Tokenized** and ***Open Files* dialog → Tagged** options of each files according to whether or not the file has been tokenized or tagged. 

- **2.1 Menu Bar → File**<br>
  - **2.1.1 Open Files**<br>
    Open the *Open Files* dialog to add file(s) to the *File Table*.

  - **2.1.2 Reopen Closed Files**<br>
    Add file(s) that are closed the last time back to the *File Table*.

    \* The history of all closed files will be erased upon exit of *Wordless*.

  - **2.1.3 Select All**<br>
    Select all files in the *File Table*.

  - **2.1.4 Deselect All**<br>
    Deselect all files in the *File Table*.

  - **2.1.5 Invert Selection**<br>
    Select files that are not currently selected and deselect files that are currently selected in the *File Table*.

  - **2.1.6 Close Selected**<br>
    Remove files that are currently selected from the *File Table*.

  - **2.1.7 Close All**<br>
    Remove all files from the *File Table*.

- **2.2 *Open Files* dialog**<br>
  - **2.2.1 Add files**<br>
    Add one single file or multiple files into the table.

    \* You can use the **Ctrl** key (**Command** key on macOS) and/or the **Shift** key to select multiple files.

  - **2.2.2 Add folder**<br>
    Add all files in the folder into the table.

    By default, all files in the chosen folder and the subfolders of the chosen folder (and subfolders of subfolders, and so on) are added to the table. If you do not want to add files in subfolders to the table, you could uncheck **Include files in subfolders**.

  - **2.2.3 Remove files**<br>
    Remove the selected files from the table.

  - **2.2.4 Clear table**<br>
    Remove all files from the table.

  - **2.2.5 Auto-detect encodings**<br>
    Auto-detect the encodings of all files when they are added into the table. If the detection results are incorrect, you can manually modify encoding settings in the table.

  - **2.2.6 Auto-detect languages**<br>
    Auto-detect the languages of all files when they are added into the table. If the detection results are incorrect, you can manually modify language settings in the table.

  - **2.2.7 Include files in subfolders**<br>
    When adding a folder to the table, recursively add all files in the chosen folder and subfolders of the chosen folder (and subfolders of subfolders, and so on) into the table

<span id="doc-3"></span>
### [3 Profiler](#doc)
> [!NOTE]
> Renamed from **Overview** to **Profiler** in *Wordless* 2.2.0

In *Profiler*, you can check and compare general linguistic features of different files.

All statistics are grouped into 5 tables for better readability: Readability, Counts, Lexical Density/Diversity, Lengths, Length Breakdown.

- **3.1.1 Readability**<br>
  Readability statistics of each file calculated according to the different readability tests used. See section [12.4.1 Readability Formulas](#doc-12-4-1) for more details.

- **3.1.2 Counts**<br>
  - **3.1.2.1 Count of Paragraphs**<br>
    The number of paragraphs in each file. Each line in the file is counted as one paragraph. Blank lines and lines containing only spaces, tabs and other invisible characters are not counted.

  - **3.1.2.2 Count of Paragraphs %**<br>
    The percentage of the number of paragraphs in each file out of the total number of paragraphs in all files.

  - **3.1.2.3 Count of Sentences**<br>
    The number of sentences in each file. *Wordless* automatically applies the built-in sentence tokenizer according to the language of each file to calculate the number of sentences in each file. You can modify sentence tokenizer settings via **Menu Bar → Preferences → Settings → Sentence Tokenization → Sentence Tokenizer Settings**.

  - **3.1.2.4 Count of Sentences %**<br>
    The percentage of the number of sentences in each file out of the total number of sentences in all files.

  - **3.1.2.5 Count of Sentence Segments**<br>
    The number of sentence segments in each file. Each part of sentence ending with one or more consecutive [terminal punctuation marks](https://en.wikipedia.org/wiki/Terminal_punctuation) (as per the [Unicode Standard](https://en.wikipedia.org/wiki/Unicode)) is counted as one sentence segment. See [here](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=[:Terminal_Punctuation=Yes:]) for the full list of terminal punctuation marks.

  - **3.1.2.6 Count of Sentence Segments %**<br>
    The percentage of the number of sentence segments in each file out of the total number of sentence segments in all files.

  - **3.1.2.7 Count of Tokens**<br>
    The number of tokens in each file. *Wordless* automatically applies the built-in word tokenizer according to the language of each file to calculate the number of tokens in each file. You can modify word tokenizer settings via **Menu Bar → Preferences → Settings → Word Tokenization → Word Tokenizer Settings**.

    You can specify what should be counted as a "token" via **Token Settings** in the *Settings Area*

  - **3.1.2.8 Count of Tokens %**<br>
    The percentage of the number of tokens in each file out of the total number of tokens in all files.

  - **3.1.2.9 Count of Types**<br>
    The number of token types in each file.

  - **3.1.2.10 Count of Types %**<br>
    The percentage of the number of token types in each file out of the total number of token types in all files.

  - **3.1.2.11 Count of Syllables**<br>
    The number of syllables in each files. *Wordless* automatically applies the built-in syllable tokenizer according to the language of each file to calculate the number of syllable in each file. You can modify syllable tokenizer settings via **Menu Bar → Preferences → Settings → Syllable Tokenization → Syllable Tokenizer Settings**.

  - **3.1.2.12 Count of Syllables %**<br>
    The percentage of the number of syllables in each file out of the total number of syllable in all files.

  - **3.1.2.13 Count of Characters**<br>
    The number of single characters in each file. Spaces, tabs and all other invisible characters are not counted.

  - **3.1.2.14 Count of Characters %**<br>
    The percentage of the number of characters in each file out of the total number of characters in all files.

- **3.1.3 Lexical Density/Diversity**<br>
  Statistics of lexical density/diversity which reflect the the extend to which the vocabulary used in each file varies. See section [12.4.2 Indicators of Lexical Density/Diversity](#doc-12-4-2) for more details.

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

<span id="doc-4"></span>
### [4 Concordancer](#doc)
In *Concordancer*, you can search for tokens in different files and generate concordance lines. You can adjust settings for data generation via **Generation Settings**.

After the concordance lines are generated and displayed in the table, you can sort the results by clicking **Sort Results** or search in *Data Table* for parts that might be of interest to you by clicking **Search in results**. Highlight colors for sorting can be modified via **Menu Bar → Preferences → Settings → Tables → Concordancer → Sorting**.

You can generate concordance plots for all search terms. You can modify the settings for the generated figure via **Figure Settings**.

- **4.1 Left**<br>
  The context before each search term, which displays 10 tokens left to the **Node** by default. You can change this behavior via **Generation Settings**.

- **4.2 Node**<br>
  The search term(s) specified in **Search Settings → Search Term**.

- **4.3 Right**<br>
  The context after each search term, which displays 10 tokens right to the **Node** by default. You can change this behavior via **Generation Settings**.

- **4.4 Sentiment**<br>
  The sentiment of the **Node** combined with its context (**Left** and **Right**).

- **4.5 Token No.**<br>
  The position of the first token of **Node** in each file.

- **4.6 Token No. %**<br>
  The percentage of the position of the first token of **Node** in each file.

- **4.7 Sentence Segment No.**<br>
  The position of the sentence segment where the **Node** is found in each file.

- **4.8 Sentence Segment No. %**<br>
  The percentage of the position of the sentence segment where the **Node** is found in each file.

- **4.9 Sentence No.**<br>
  The position of the sentence where the **Node** is found in each file.

- **4.10 Sentence No. %**<br>
  The percentage of the position of the sentence where the **Node** is found in each file.

- **4.11 Paragraph No.**<br>
  The position of the paragraph where the **Node** is found in each file.

- **4.12 Paragraph No. %**<br>
  The percentage of the position of the paragraph where the **Node** is found in each file.

- **4.13 File**<br>
  The name of the file where the **Node** is found.

<span id="doc-5"></span>
### [5 Parallel Concordancer](#doc)
> [!NOTE]
> 1. Added in *Wordless* 2.0.0
> 1. Renamed from **Concordancer (Parallel Mode)** to **Parallel Concordancer** in *Wordless* 2.2.0

In *Parallel Concordancer*, you can search for tokens in parallel corpora and generate parallel concordance lines. You may leave **Search Settings → Search Term** blank so as to search for instances of additions and deletions.

You can search in *Data Table* for parts that might be of interest to you by clicking **Search in results**.

- **5.1 Parallel Unit No.**<br>
  The position of the alignment unit (paragraph) where the the search term is found.

- **5.2 Parallel Unit No. %**<br>
  The percentage of the position of the alignment unit (paragraph) where the the search term is found.

- **5.3 Parallel Units**<br>
  The parallel unit (paragraph) where the search term is found in each file.

  Highlight colors for search terms can be modified via **Menu Bar → Preferences → Settings → Tables → Parallel Concordancer → Highlight Color Settings**.

<span id="doc-6"></span>
### [6 Dependency Parser](#doc)
> [!NOTE]
> Added in *Wordless* 3.0.0

In *Dependency Parser*, you can search for all dependency relations associated with different tokens and calculate their dependency lengths (distances).

You can filter the results by clicking **Filter results** or search in *Data Table* for parts that might be of interest to you by clicking **Search in results**.

You can select lines in the *Results Area* and then click *Generate Figure* to show dependency graphs for all selected sentences. You can modify the settings for the generated figure via **Figure Settings** and decide how the figures should be displayed.

- **6.1 Head**<br>
  The token functioning as the head in the dependency structure.

- **6.2 Dependent**<br>
  The token functioning as the dependent in the dependency structure.

- **6.3 Dependency Length**<br>
  The dependency length (distance) between the head and dependent in the dependency structure. The dependency length is positive when the head follows the dependent and would be negative if the head precedes the dependent.

- **6.4 Dependency Length (Absolute)**<br>
  The absolute value of the dependency length (distance) between the head and dependent in the dependency structure. The absolute dependency length is always positive.

- **6.5 Sentence**<br>
  The sentence where the dependency structure is found.

  Highlight colors for the head and the dependent can be modified via **Menu Bar → Preferences → Settings → Tables → Dependency Parser → Highlight Color Settings**.

- **6.6 Sentence No.**<br>
  The position of the sentence where the dependency structure is found.

- **6.7 Sentence No. %**<br>
  The percentage of the position of the sentence where the dependency structure is found.

- **6.8 File**<br>
  The name of the file where the dependency structure is found.

<span id="doc-7"></span>
### [7 Wordlist Generator](#doc)
> [!NOTE]
> Renamed from **Wordlist** to **Wordlist Generator** in *Wordless* 2.2.0

In *Wordlist Generator*, you can generate wordlists for different files and calculate the raw frequency, relative frequency, dispersion and adjusted frequency for each token. You can disable the calculation of dispersion and/or adjusted frequency by setting **Generation Settings → Measures of Dispersion / Measure of Adjusted Frequency** to **None**.

You can filter the results by clicking **Filter results** or search in *Data Table* for parts that might be of interest to you by clicking **Search in results**.

You can generate line charts or word clouds for wordlists using any statistics. You can modify the settings for the generated figure via **Figure Settings**.

- **7.1 Rank**<br>
  The rank of the token sorted by its frequency in the first file in descending order (by default). You can sort the results again by clicking the column headers. You can use continuous numbering after tied ranks (eg. 1/1/1/2/2/3 instead of 1/1/1/4/4/6) by checking **Menu Bar → Preferences → Settings → Tables → Rank Settings → Continue numbering after ties**.

- **7.2 Token**<br>
  You can specify what should be counted as a "token" via **Token Settings**.

- **7.3 Syllabification**<br>
  The syllabified form of each token.

  If the token happens to exist in the vocabulary of multiple languages, all syllabified forms with their applicable languages will be listed.

  If there is no syllable tokenization support for the language where the token is found, "No language support" is displayed instead. To check which languages have syllable tokenization support, please refer to section [12.1 Supported Languages](#doc-12-1).

- **7.4 Frequency**<br>
  The number of occurrences of the token in each file.

- **7.5 Dispersion**<br>
  The dispersion of the token in each file. You can change the measure of dispersion used via **Generation Settings → Measure of Dispersion**. See section [12.4.3 Measures of Dispersion & Adjusted Frequency](#doc-12-4-3) for more details.

- **7.6 Adjusted Frequency**<br>
  The adjusted frequency of the token in each file. You can change the measure of adjusted frequency used via **Generation Settings → Measure of Adjusted Frequency**. See section [12.4.3 Measures of Dispersion & Adjusted Frequency](#doc-12-4-3) for more details.

- **7.7 Number of Files Found**<br>
  The number of files in which the token appears at least once.

- **7.8 Number of Files Found %**<br>
  The percentage of the number of files in which the token appears at least once out of the total number of files that are cureently selected.

<span id="doc-8"></span>
### [8 N-gram Generator](#doc)
> [!NOTE]
> Renamed from **N-gram** to **N-gram Generator** in *Wordless* 2.2.0

In *N-gram Generator*, you can search for n-grams (consecutive tokens) or skip-grams (non-consecutive tokens) in different files, count and compute the raw frequency and relative frequency of each n-gram/skip-gram, and calculate the dispersion and adjusted frequency for each n-gram/skip-gram using different measures. You can adjust the settings for the generated results via **Generation Settings**.  You can disable the calculation of dispersion and/or adjusted frequency by setting **Generation Settings → Measures of Dispersion / Measure of Adjusted Frequency** to **None**. To allow skip-grams in the results, check **Generation Settings → Allow skipped tokens** and modify the settings. You can also set constraints on the position of search terms in all n-grams via **Search Settings → Search Term Position**.

You can filter the results by clicking **Filter results** or search in *Data Table* for parts that might be of interest to you by clicking **Search in results**.

You can generate line charts or word clouds for n-grams using any statistics. You can modify the settings for the generated figure via **Figure Settings**.

- **8.1 Rank**<br>
  The rank of the n-gram sorted by its frequency in the first file in descending order (by default). You can sort the results again by clicking the column headers. You can use continuous numbering after tied ranks (eg. 1/1/1/2/2/3 instead of 1/1/1/4/4/6) by checking **Menu Bar → Preferences → Settings → Tables → Rank Settings → Continue numbering after ties**.

- **8.2 N-gram**<br>
  You can specify what should be counted as a "n-gram" via **Token Settings**.

- **8.3 Frequency**<br>
  The number of occurrences of the n-gram in each file.

- **8.4 Dispersion**<br>
  The dispersion of the n-gram in each file. You can change the measure of dispersion used via **Generation Settings → Measure of Dispersion**. See section [12.4.3 Measures of Dispersion & Adjusted Frequency](#doc-12-4-3) for more details.

- **8.5 Adjusted Frequency**<br>
  The adjusted frequency of the n-gram in each file. You can change the measure of adjusted frequency used via **Generation Settings → Measure of Adjusted Frequency**. See section [12.4.3 Measures of Dispersion & Adjusted Frequency](#doc-12-4-3) for more details.

- **8.6 Number of Files Found**<br>
  The number of files in which the n-gram appears at least once.

- **8.7 Number of Files Found %**<br>
  The percentage of the number of files in which the n-gram appears at least once out of the total number of files that are currently selected.

<span id="doc-9"></span>
### [9 Collocation Extractor](#doc)
> [!NOTE]
> Renamed from **Collocation** to **Collocation Extractor** in *Wordless* 2.2.0

In *Collocation Extractor*, you can search for patterns of collocation (tokens that co-occur more often than would be expected by chance) within a given collocational window (from 5 words to the left to 5 words to the right by default), conduct different tests of statistical significance on each pair of collocates and calculate the Bayes factor and effect size for each pair using different measures. You can adjust the settings for the generated results via **Generation Settings**. You can disable the calculation of statistical significance and/or Bayes factor and/or effect size by setting **Generation Settings → Test of Statistical Significance / Measures of Bayes Factor / Measure of Effect Size** to **None**.

You can filter the results by clicking **Filter results** or search in *Data Table* for parts that might be of interest to you by clicking **Search in results**.

You can generate line charts, word clouds, and network graphs for patterns of collocation using any statistics. You can modify the settings for the generated figure via **Figure Settings**.

- **9.1 Rank**<br>
  The rank of the collocating token sorted by the p-value of the significance test conducted on the node and the collocating token in the first file in ascending order (by default). You can sort the results again by clicking the column headers. You can use continuous numbering after tied ranks (eg. 1/1/1/2/2/3 instead of 1/1/1/4/4/6) by checking **Menu Bar → Preferences → Settings → Tables → Rank Settings → Continue numbering after ties**.

- **9.2 Node**<br>
  The search term. You can specify what should be counted as a "token" via **Token Settings**.

- **9.3 Collocate**<br>
  The collocating token. You can specify what should be counted as a "token" via **Token Settings**.

- **9.4 Ln, ..., L3, L2, L1, R1, R2, R3, ..., Rn**<br>
  The number of co-occurrences of the node and the collocating token with the collocating token at the given position in each file.

- **9.5 Frequency**<br>
  The total number of co-occurrences of the node and the collocating token with the collocating token at all possible positions in each file.

- **9.6 Test Statistic**<br>
  The test statistic of the significance test conducted on the node and the collocating token in each file. You can change the test of statistical significance used via **Generation Settings → Test of Statistical Significance**. See section [12.4.4 Tests of Statistical Significance, Measures of Bayes Factor, & Measures of Effect Size](#doc-12-4-4) for more details.

  Please note that test statistic is not available for some tests of statistical significance.

- **9.7 p-value**<br>
  The p-value of the significance test conducted on the node and the collocating token in each file. You can change the test of statistical significance used via **Generation Settings → Test of Statistical Significance**. See section [12.4.4 Tests of Statistical Significance, Measures of Bayes Factor, & Measures of Effect Size](#doc-12-4-4) for more details.

- **9.8 Bayes Factor**<br>
  The Bayes factor the node and the collocating token in each file. You can change the measure of Bayes factor used via **Generation Settings → Measure of Bayes Factor**. See section [12.4.4 Tests of Statistical Significance, Measures of Bayes Factor, & Measures of Effect Size](#doc-12-4-4) for more details.

- **9.9 Effect Size**<br>
  The effect size of the node and the collocating token in each file. You can change the measure of effect size used via **Generation Settings → Measure of Effect Size**. See section [12.4.4 Tests of Statistical Significance, Measures of Bayes Factor, & Measures of Effect Size](#doc-12-4-4) for more details.

- **9.10 Number of Files Found**<br>
  The number of files in which the node and the collocating token co-occur at least once.

- **9.11 Number of Files Found %**<br>
  The percentage of the number of files in which the node and the collocating token co-occur at least once out of the total number of files that are currently selected.

<span id="doc-10"></span>
### [10 Colligation Extractor](#doc)
> [!NOTE]
> Renamed from **Colligation** to **Colligation Extractor** in *Wordless* 2.2.0

In *Colligation Extractor*, you can search for patterns of colligation (parts of speech that co-occur more often than would be expected by chance) within a given collocational window (from 5 words to the left to 5 words to the right by default), conduct different tests of statistical significance on each pair of parts of speech and calculate the Bayes factor and effect size for each pair using different measures. You can adjust the settings for the generated data via **Generation Settings**. You can disable the calculation of statistical significance and/or Bayes factor and/or effect size by setting **Generation Settings → Test of Statistical Significance / Measures of Bayes Factor / Measure of Effect Size** to **None**.

*Wordless* will automatically apply its built-in part-of-speech tagger on every file that are not part-of-speech-tagged already according to the language of each file. If part-of-speech tagging is not supported for the given languages, the user should provide a file that has already been part-of-speech-tagged and make sure that the correct **Text Type** has been set on each file.

You can filter the results by clicking **Filter results** or search in *Data Table* for parts that might be of interest to you by clicking **Search in results**.

You can generate line charts or word clouds for patterns of colligation using any statistics. You can modify the settings for the generated figure via **Figure Settings**.

- **10.1 Rank**<br>
  The rank of the collocating part of speech sorted by the p-value of the significance test conducted on the node and the collocating part of speech in the first file in ascending order (by default). You can sort the results again by clicking the column headers. You can use continuous numbering after tied ranks (eg. 1/1/1/2/2/3 instead of 1/1/1/4/4/6) by checking **Menu Bar → Preferences → Settings → Tables → Rank Settings → Continue numbering after ties**.

- **10.2 Node**<br>
  The search term. You can specify what should be counted as a "token" via **Token Settings**.

- **10.3 Collocate**<br>
  The collocating part of speech. You can specify what should be counted as a "token" via **Token Settings**.

- **10.4 Ln, ..., L3, L2, L1, R1, R2, R3, ..., Rn**<br>
  The number of co-occurrences of the node and the collocating part of speech with the collocating part of speech at the given position in each file.

- **10.5 Frequency**<br>
  The total number of co-occurrences of the node and the collocating part of speech with the collocating part of speech at all possible positions in each file.

- **10.6 Test Statistic**<br>
  The test statistic of the significance test conducted on the node and the collocating part of speech in each file. You can change the test of statistical significance used via **Generation Settings → Test of Statistical Significance**. See section [12.4.4 Tests of Statistical Significance, Measures of Bayes Factor, & Measures of Effect Size](#doc-12-4-4) for more details.

  Please note that test statistic is not available for some tests of statistical significance.

- **10.7 p-value**<br>
  The p-value of the significance test conducted on the node and the collocating part of speech in each file. You can change the test of statistical significance used via **Generation Settings → Test of Statistical Significance**. See section [12.4.4 Tests of Statistical Significance, Measures of Bayes Factor, & Measures of Effect Size](#doc-12-4-4) for more details.

- **10.8 Bayes Factor**<br>
  The Bayes factor of the node and the collocating part of speech in each file. You can change the measure of Bayes factor used via **Generation Settings → Measure of Bayes Factor**. See section [12.4.4 Tests of Statistical Significance, Measures of Bayes Factor, & Measures of Effect Size](#doc-12-4-4) for more details.
  
- **10.9 Effect Size**<br>
  The effect size of the node and the collocating part of speech in each file. You can change the measure of effect size used via **Generation Settings → Measure of Effect Size**. See section [12.4.4 Tests of Statistical Significance, Measures of Bayes Factor, & Measures of Effect Size](#doc-12-4-4) for more details.

- **10.10 Number of Files Found**<br>
  The number of files in which the node and the collocating part of speech co-occur at least once.

- **10.11 Number of Files Found %**<br>
  The percentage of the number of files in which the node and the collocating part of speech co-occur at least once out of the total number of file that are currently selected.

<span id="doc-11"></span>
### [11 Keyword Extractor](#doc)
> [!NOTE]
> Renamed from **Keyword** to **Keyword Extractor** in *Wordless* 2.2

In *Keyword Extractor*, you can search for candidates of potential keywords (tokens that have far more or far less frequency in the observed corpus than in the reference corpus) in different files given a reference corpus, conduct different tests of statistical significance on each keyword and calculate the Bayes factor and effect size for each keyword using different measures. You can adjust the settings for the generated data via **Generation Settings**. You can disable the calculation of statistical significance and/or Bayes factor and/or effect size by setting **Generation Settings → Test of Statistical Significance / Measures of Bayes Factor / Measure of Effect Size** to **None**.

You can filter the results by clicking **Filter results** or search in *Data Table* for parts that might be of interest to you by clicking **Search in results**.

You can generate line charts or word clouds for keywords using any statistics. You can modify the settings for the generated figure via **Figure Settings**.

- **11.1 Rank**<br>
  The rank of the keyword sorted by the p-value of the significance test conducted on the keyword in the first file in ascending order (by default). You can sort the results again by clicking the column headers. You can use continuous numbering after tied ranks (eg. 1/1/1/2/2/3 instead of 1/1/1/4/4/6) by checking **Menu Bar → Preferences → Settings → Tables → Rank Settings → Continue numbering after ties**.

- **11.2 Keyword**<br>
  The potential keyword. You can specify what should be counted as a "token" via **Token Settings**.

- **11.3 Frequency (in Reference Corpora)**<br>
  The number of occurrences of the keyword in reference corpora.

- **11.4 Frequency (in Observed Corpus)**<br>
  The number of occurrences of the keyword in each observed corpus.

- **11.5 Test Statistic**<br>
  The test statistic of the significance test conducted on the keyword in each file. You can change the test of statistical significance used via **Generation Settings → Test of Statistical Significance**. See section [12.4.4 Tests of Statistical Significance, Measures of Bayes Factor, & Measures of Effect Size](#doc-12-4-4) for more details.

  Please note that test statistic is not available for some tests of statistical significance.

- **11.6 p-value**<br>
  The p-value of the significance test conducted on the keyword in each file. You can change the test of statistical significance used via **Generation Settings → Test of Statistical Significance**. See section [12.4.4 Tests of Statistical Significance, Measures of Bayes Factor, & Measures of Effect Size](#doc-12-4-4) for more details.

- **11.7 Bayes Factor**<br>
  The Bayes factor of the keyword in each file. You can change the measure of Bayes factor used via **Generation Settings → Measure of Bayes Factor**. See section [12.4.4 Tests of Statistical Significance, Measures of Bayes Factor, & Measures of Effect Size](#doc-12-4-4) for more details.

- **11.8 Effect Size**<br>
  The effect size of on the keyword in each file. You can change the measure of effect size used via **Generation Settings → Measure of Effect Size**. See section [12.4.4 Tests of Statistical Significance, Measures of Bayes Factor, & Measures of Effect Size](#doc-12-4-4) for more details.

- **11.9 Number of Files Found**<br>
  The number of files in which the keyword appears at least once.

- **11.10 Number of Files Found %**<br>
  The percentage of the number of files in which the keyword appears at least once out of the total number of files that are currently selected.

<span id="doc-12"></span>
## [12 Appendixes](#doc)

<span id="doc-12-1"></span>
### [12.1 Supported Languages](#doc)

Language|Sentence Token-ization|Word Token-ization|Syllable Token-ization|Part-of-speech Tagging|Lemma-tization|Stop Word List|Depen-dency Parsing|Senti-ment Analysis
:-----------------------:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:
Afrikaans                |✔|✔|✔|✔|✔|✖️|✔|✔
Albanian                 |⭕️ |✔|✔|✖️|✔|✖️|✖️|✔
Amharic                  |⭕️ |✔|✖️|✖️|✖️|✖️|✖️|✔
Arabic                   |✔|✔|✖️|✔|✔|✔|✔|✔
Armenian (Classical)     |✔|✔|✖️|✔|✔|✖️|✔|✖️
Armenian (Eastern)       |✔|✔|✖️|✔|✔|✖️|✔|✔
Armenian (Western)       |✔|✔|✖️|✔|✔|✖️|✔|✔
Assamese                 |⭕️ |✔|✖️|✖️|✖️|✖️|✖️|✔
Asturian                 |⭕️ |⭕️ |✖️|✖️|✔|✖️|✖️|✖️
Azerbaijani              |⭕️ |✔|✖️|✖️|✖️|✔|✖️|✔
Basque                   |✔|✔|✔|✔|✔|✔|✔|✔
Belarusian               |✔|✔|✔|✔|✔|✖️|✔|✔
Bengali                  |⭕️ |✔|✖️|✖️|✔|✔|✖️|✔
Bulgarian                |✔|✔|✔|✔|✔|✖️|✔|✔
Burmese                  |✔|✔|✖️|✖️|✖️|✖️|✖️|✔
Buryat (Russia)          |✔|✔|✖️|✔|✔|✖️|✔|✖️
Catalan                  |✔|✔|✔|✔|✔|✔|✔|✔
Chinese (Classical)      |✔|✔|✖️|✔|✔|✖️|✔|✖️
Chinese (Simplified)     |✔|✔|✖️|✔|✔|✔|✔|✔
Chinese (Traditional)    |✔|✔|✖️|✔|✔|✔|✔|✔
Church Slavonic (Old)    |✔|✔|✖️|✔|✔|✖️|✔|✖️
Coptic                   |✔|✔|✖️|✔|✔|✖️|✔|✖️
Croatian                 |✔|✔|✔|✔|✔|✖️|✔|✔
Czech                    |✔|✔|✔|✔|✔|✖️|✔|✔
Danish                   |✔|✔|✔|✔|✔|✔|✔|✔
Dutch                    |✔|✔|✔|✔|✔|✔|✔|✔
English (Middle)         |⭕️ |⭕️ |✖️|✖️|✔|✖️|✖️|✖️
English (Old)            |✔|✔|✖️|✔|✔|✖️|✔|✖️
English (United Kingdom) |✔|✔|✔|✔|✔|✔|✔|✔
English (United States)  |✔|✔|✔|✔|✔|✔|✔|✔
Erzya                    |✔|✔|✖️|✔|✔|✖️|✔|✖️
Esperanto                |⭕️ |⭕️ |✔|✖️|✖️|✖️|✖️|✔
Estonian                 |✔|✔|✔|✔|✔|✖️|✔|✔
Faroese                  |✔|✔|✖️|✔|✖️|✖️|✔|✖️
Finnish                  |✔|✔|✖️|✔|✔|✔|✔|✔
French                   |✔|✔|✔|✔|✔|✔|✔|✔
French (Old)             |✔|✔|✖️|✔|✔|✖️|✔|✖️
Galician                 |✔|✔|✔|✔|✔|✖️|✔|✔
Georgian                 |⭕️ |⭕️ |✖️|✖️|✔|✖️|✖️|✔
German (Austria)         |✔|✔|✔|✔|✔|✔|✔|✔
German (Germany)         |✔|✔|✔|✔|✔|✔|✔|✔
German (Switzerland)     |✔|✔|✔|✔|✔|✔|✔|✔
Gothic                   |✔|✔|✖️|✔|✔|✖️|✔|✖️
Greek (Ancient)          |✔|✔|✖️|✔|✔|✖️|✔|✖️
Greek (Modern)           |✔|✔|✔|✔|✔|✔|✔|✔
Gujarati                 |⭕️ |✔|✖️|✖️|✖️|✖️|✖️|✔
Hebrew (Ancient)         |✔|✔|✖️|✔|✔|✖️|✔|✖️
Hebrew (Modern)          |✔|✔|✖️|✔|✔|✔|✔|✔
Hindi                    |✔|✔|✖️|✔|✔|✖️|✔|✔
Hungarian                |✔|✔|✔|✔|✔|✔|✔|✔
Icelandic                |✔|✔|✔|✔|✔|✖️|✔|✔
Indonesian               |✔|✔|✔|✔|✔|✔|✔|✔
Irish                    |✔|✔|✖️|✔|✔|✖️|✔|✔
Italian                  |✔|✔|✔|✔|✔|✔|✔|✔
Japanese                 |✔|✔|✖️|✔|✔|✖️|✔|✔
Kannada                  |⭕️ |✔|✖️|✖️|✖️|✖️|✖️|✔
Kazakh                   |✔|✔|✖️|✔|✔|✔|✔|✔
Khmer                    |✔|✔|✖️|✔|✖️|✖️|✖️|✔
Korean                   |✔|✔|✖️|✔|✔|✖️|✔|✔
Kurdish (Kurmanji)       |✔|✔|✖️|✔|✔|✖️|✔|✔
Kyrgyz                   |✔|✔|✖️|✔|✔|✖️|✔|✔
Lao                      |✔|✔|✖️|✔|✖️|✔|✖️|✔
Latin                    |✔|✔|✖️|✔|✔|✖️|✔|✔
Latvian                  |✔|✔|✔|✔|✔|✖️|✔|✔
Ligurian                 |✔|✔|✖️|✔|✔|✖️|✔|✖️
Lithuanian               |✔|✔|✔|✔|✔|✖️|✔|✔
Luganda                  |⭕️ |✔|✖️|✖️|✖️|✖️|✖️|✔
Luxembourgish            |⭕️ |✔|✖️|✖️|✔|✖️|✖️|✔
Macedonian               |✔|✔|✖️|✔|✔|✖️|✔|✔
Malay                    |⭕️ |✔|✖️|✖️|✔|✖️|✖️|✔
Malayalam                |✔|✔|✖️|✖️|✖️|✖️|✖️|✔
Maltese                  |✔|✔|✖️|✔|✖️|✖️|✔|✔
Manx                     |✔|✔|✖️|✔|✔|✖️|✔|✖️
Marathi                  |✔|✔|✖️|✔|✔|✖️|✔|✔
Meitei (Meitei script)   |⭕️ |✔|✖️|✖️|✖️|✖️|✖️|✔
Mongolian                |⭕️ |⭕️ |✔|✖️|✖️|✖️|✖️|✔
Nepali                   |⭕️ |✔|✖️|✖️|✖️|✔|✖️|✔
Nigerian Pidgin          |✔|✔|✖️|✔|✔|✖️|✔|✖️
Norwegian (Bokmål)       |✔|✔|✔|✔|✔|✔|✔|✔
Norwegian (Nynorsk)      |✔|✔|✔|✔|✔|✖️|✔|✖️
Odia                     |⭕️ |✔|✖️|✖️|✖️|✖️|✖️|✔
Persian                  |✔|✔|✖️|✔|✔|✖️|✔|✔
Polish                   |✔|✔|✔|✔|✔|✖️|✔|✔
Pomak                    |✔|✔|✖️|✔|✔|✖️|✔|✖️
Portuguese (Brazil)      |✔|✔|✔|✔|✔|✔|✔|✔
Portuguese (Portugal)    |✔|✔|✔|✔|✔|✔|✔|✔
Punjabi (Gurmukhi script)|⭕️ |✔|✖️|✖️|✖️|✖️|✖️|✔
Romanian                 |✔|✔|✔|✔|✔|✔|✔|✔
Russian                  |✔|✔|✔|✔|✔|✔|✔|✔
Russian (Old)            |✔|✔|✖️|✔|✔|✖️|✔|✖️
Sámi (Northern)          |✔|✔|✖️|✔|✔|✖️|✔|✖️
Sanskrit                 |✔|✔|✖️|✔|✔|✖️|✔|✔
Scottish Gaelic          |✔|✔|✖️|✔|✔|✖️|✔|✔
Serbian (Cyrillic script)|⭕️ |✔|✔|✖️|✔|✖️|✖️|✔
Serbian (Latin script)   |✔|✔|✔|✔|✔|✖️|✔|✔
Sindhi                   |✔|✔|✖️|✔|✖️|✖️|✖️|✔
Sinhala                  |⭕️ |✔|✖️|✖️|✖️|✖️|✖️|✔
Slovak                   |✔|✔|✔|✔|✔|✖️|✔|✔
Slovene                  |✔|✔|✔|✔|✔|✔|✔|✔
Sorbian (Lower)          |⭕️ |✔|✖️|✖️|✖️|✖️|✖️|✖️
Sorbian (Upper)          |✔|✔|✖️|✔|✔|✖️|✔|✖️
Spanish                  |✔|✔|✔|✔|✔|✔|✔|✔
Swahili                  |⭕️ |⭕️ |✖️|✖️|✔|✖️|✖️|✔
Swedish                  |✔|✔|✔|✔|✔|✔|✔|✔
Tagalog                  |⭕️ |✔|✖️|✖️|✔|✖️|✖️|✔
Tajik                    |⭕️ |✔|✖️|✖️|✖️|✔|✖️|✔
Tamil                    |✔|✔|✖️|✔|✔|✖️|✔|✔
Tatar                    |⭕️ |✔|✖️|✖️|✖️|✖️|✖️|✔
Telugu                   |✔|✔|✔|✔|✖️|✖️|✔|✔
Tetun (Dili)             |⭕️ |✔|✖️|✖️|✖️|✖️|✖️|✖️
Thai                     |✔|✔|✔|✔|✖️|✔|✖️|✔
Tibetan                  |✔|✔|✖️|✔|✔|✖️|✖️|✖️
Tigrinya                 |⭕️ |✔|✖️|✖️|✖️|✖️|✖️|✔
Tswana                   |⭕️ |✔|✖️|✖️|✖️|✖️|✖️|✖️
Turkish                  |✔|✔|✖️|✔|✔|✔|✔|✔
Ukrainian                |✔|✔|✔|✔|✔|✖️|✔|✔
Urdu                     |✔|✔|✖️|✔|✔|✖️|✔|✔
Uyghur                   |✔|✔|✖️|✔|✔|✖️|✔|✔
Vietnamese               |✔|✔|✖️|✔|✖️|✖️|✔|✔
Welsh                    |✔|✔|✖️|✔|✔|✖️|✔|✔
Wolof                    |✔|✔|✖️|✔|✔|✖️|✔|✖️
Yoruba                   |⭕️ |✔|✖️|✖️|✖️|✖️|✖️|✔
Zulu                     |⭕️ |⭕️ |✔|✖️|✖️|✖️|✖️|✔
Other languages          |⭕️ |⭕️ |✖️|✖️|✖️|✖️|✖️|✖️

> [!NOTE]
> ✔: Supported<br>
> ⭕️: Supported but falls back to the default English (United States) tokenizer<br>
> ✖️: Not supported

<span id="doc-12-2"></span>
### [12.2 Supported File Types](#doc)

File Type                 |File Extensions|Remarks
--------------------------|---------------|-------
CSV files¹                |\*.csv         |
Excel workbooks¹²         |\*.xlsx        |Legacy Microsoft 97-2003 Excel Workbooks (\*.xls) are not supported.
HTML pages¹²              |\*.htm, \*.html|
Lyrics File¹              |\*.lrc         |[Simple LRC](https://en.wikipedia.org/wiki/LRC_(file_format)#Core_format) and [enhanced LRC](https://en.wikipedia.org/wiki/LRC_(file_format)#A2_extension_(Enhanced_LRC_format)) formats are supported.
PDF files¹²               |\*.pdf         |Text could only be extracted from **text-searchable PDF files**. There is no support for automatically converting scanned PDF files into text-searchable ones.
PowerPoint presentations¹²|\*.pptx        |Legacy Microsoft 97-2003 PowerPoint presentations (\*.ppt) are not supported.
Text files                |\*.txt         |
Translation memory files¹ |\*.tmx         |
Word documents¹²          |\*.docx        |Legacy Microsoft 97-2003 Word documents (\*.doc) are not supported.
XML files¹                |\*.xml         |

> [!IMPORTANT]
> 1. Non-TXT files will be automatically converted to TXT files when being imported into *Wordless*. You can check the converted files under folder **imports** at the installation location of *Wordless* on your computer (as for macOS users, right click **Wordless.app**, select **Show Package Contents** and navigate to **Contents/MacOS/imports/**). You can change this location via **Menu Bar → Preferences → Settings → General → Import → Temporary Files → Default path**.
> 1. It is **not recommended to directly import non-text files into *Wordless*** and the support for doing so is provided only for convenience, since accuracy of text extraction could never be guaranteed and unintended data loss might occur, for which reason users are encouraged to **convert their files using specialized tools and make their own choices** on which part of the data should be kept or discarded.

<span id="doc-12-3"></span>
### [12.3 Supported File Encodings](#doc)

Language               |File Encoding          |Auto-detection
-----------------------|-----------------------|:------------:
All languages          |UTF-8 without BOM      |✔
All languages          |UTF-8 with BOM         |✔
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

<!-- Only people's names are capitalized and case of measure names are preserved as in original papers -->
<span id="doc-12-4"></span>
### [12.4 Supported Measures](#doc)

<span id="doc-12-4-1"></span>
#### [12.4.1 Readability Formulas](#doc)
The readability of a text depends on several variables including the average sentence length, average word length in characters, average word length in syllables, number of monosyllabic words, number of polysyllabic words, number of difficult words, etc.

It should be noted that some readability measures are **language-specific**, or applicable only to texts in languages for which *Wordless* have **built-in syllable tokenization support** (check [12.1](#doc-12-1) for reference), while others can be applied to texts in all languages.

The following variables would be used in formulas:<br>
**NumSentences**: Number of sentences<br>
**NumWords**: Number of words<br>
**NumWordsSyl₁**: Number of monosyllabic words<br>
**NumWordsSylsₙ₊**: Number of words with n or more syllables<br>
**NumWordsLtrsₙ₊**: Number of words with n or more letters<br>
**NumWordsLtrsₙ₋**: Number of words with n or fewer letters<br>
**NumConjs**: Number of conjunctions<br>
**NumPreps**: Number of prepositions<br>
**NumProns**: Number of pronouns<br>
<span id="ref-num-words-dale-769"></span>**NumWordsDale₇₆₉**: Number of words outside the Dale list of 769 easy words ([Dale, 1931](#ref-dale-1931))<br>
<span id="ref-num-words-dale-3000"></span>**NumWordsDale₃₀₀₀**: Number of words outside the Dale list of 3000 easy words ([Dale & Chall, 1948b](#ref-dale-chall-1948b))<br>
<span id="ref-num-words-spache"></span>**NumWordsSpache**: Number of words outside the Spache word list ([Spache, 1974](#ref-spache-1974))<br>
**NumWordTypes**: Number of word types<br>
<span id="ref-num-word-types-bamberger-vanecek"></span>**NumWordTypesBambergerVanecek**: Number of word types outside the Bamberger-Vanecek's list of 1000 most common words ([Bamberger & Vanecek, 1984, pp. 176–179](#ref-bamberger-vanecek-1984))<br>
<span id="ref-num-word-types-dale-769"></span>**NumWordTypesDale₇₆₉**: Number of word types outside the Dale list of 769 easy words ([Dale, 1931](#ref-dale-1931))<br>
**NumSyls**: Number of syllables<br>
<span id="ref-num-syls-luong-nguyen-dinh-1000"></span>**NumSylsLuongNguyenDinh₁₀₀₀**: Number of syllables outside the Luong-Nguyen-Dinh list of 1000 most frequent syllables extracted from all easy documents of the corpus of Vietnamese text readability dataset on literature domain ([Luong et al., 2018](#ref-luong-et-al-2018))<br>
**NumCharsAll**: Number of characters (letters, CJK characters, etc., numerals, and punctuation marks)<br>
**NumCharsAlnum**: Number of alphanumeric characters (letters, CJK characters, etc., and numerals)<br>
**NumCharsAlpha**: Number of alphabetic characters (letters, CJK characters, etc.)

<!--
Al-Heeti's readability formula:
\begin{align*}
    \text{RD}_\text{Policy One} &= 4.41434307 \times \frac{\text{NumCharsAlpha}}{\text{NumWords}} - 13.46873475 \\
    \text{RD}_\text{Policy Two} &= 0.97569509 \times \frac{\text{NumCharsAlpha}}{\text{NumWords}} + 0.37237998 \times \frac{\text{NumWords}}{\text{NumSentences}} - 0.90451827 \times \frac{\text{NumWords}}{\text{NumWordTypes}} - 1.06000414
\end{align*}

Automated Arabic Readability Index:
    {\text{AARI} = 3.28 \times \text{NumCharsAlnum} + 1.43 \times \frac{\text{NumCharsAlnum}}{\text{NumWords}} + 1.24 \times \frac{\text{NumWords}}{\text{NumSentences}}}

Automated Readability Index:
    \begin{align*}
        \text{ARI} &= 0.5 \times \frac{\text{NumWords}}{\text{NumSentences}} + 4.71 \times \frac{\text{NumCharsAll}}{\text{NumWords}} - 21.43 \\
        \text{ARI}_{\text{Navy}} &= 0.37 \times \frac{\text{NumWords}}{\text{NumSentences}} + 5.84 \times \frac{\text{NumCharsAll}}{\text{NumWords}} - 26.01
    \end{align*} 

Bormuth's cloze mean & grade placement:
    \begin{align*}
        \text{M} = \; &0.886593 - 0.083640 \times \frac{\text{NumCharsAlpha}}{\text{NumWords}} + 0.161911 \times \left(\frac{\text{NumWordsDale}_{3000}}{\text{NumWords}}\right)^3 \\
        &- 0.021401 \times \frac{\text{NumWords}}{\text{NumSentences}} + 0.000577 \times \left(\frac{\text{NumWords}}{\text{NumSentences}}\right)^2 - 0.000005 \times \left(\frac{\text{NumWords}}{\text{NumSentences}}\right)^3 \\
        \text{GP} = \; &4.275 + 12.881 \times \text{M} - 34.934 \times \text{M}^2 + 20.388 \times \text{M}^3 + 26.194 \times \text{C} - 2.046 \times \text{C}^2 - 11.767 \times \text{C}^3 \\
        &- 44.285 \times \left(\text{M} \times \text{C}\right) + 97.620 \times \left(\text{M} \times \text{C}\right)^2 - 59.538 \times \left(\text{M} \times \text{C}\right)^3
    \end{align*}

Coleman-Liau index:
    \begin{align*}
        \text{Estimated cloze \ %} &= 141.8401 - 0.21459 \times \left(\frac{\text{NumCharsAlpha}}{\text{NumWords}} \times 100\right) + 1.079812 \times \left(\frac{\text{NumSentences}}{\text{NumWords}} \times 100\right) \\
        \text{Grade level} &= -27.4004 \times \frac{\text{Estimated cloze \; %}}{100} + 23.06395
    \end{align*}

Coleman's readability formula:
    \begin{align*}
        \text{Cloze \; %}_1 &= 1.29 \times \left(\frac{\text{NumWordsSyl}_1}{\text{NumWords}} \times 100\right) - 38.45 \\
        \text{Cloze \; %}_2 &= 1.16 \times \left(\frac{\text{NumWordsSyl}_1}{\text{NumWords}} \times 100\right) + 1.48 \times \left(\frac{\text{NumSentences}}{\text{NumWords}} \times 100\right) - 37.95 \\
        \text{Cloze \; %}_3 &= 1.07 \times \left(\frac{\text{NumWordsSyl}_1}{\text{NumWords}} \times 100\right) + 1.18 \times \left(\frac{\text{NumSentences}}{\text{NumWords}} \times 100\right) + 0.76 \times \left(\frac{\text{NumProns}}{\text{NumWords}} \times 100\right) - 34.02 \\
        \text{Cloze \; %}_4 &= 1.04 \times \left(\frac{\text{NumWordsSyl}_1}{\text{NumWords}} \times 100\right) + 1.06 \times \left(\frac{\text{NumSentences}}{\text{NumWords}} \times 100\right) + 0.56 \times \left(\frac{\text{NumProns}}{\text{NumWords}} \times 100\right) - 0.36 \times \left(\frac{\text{NumPreps}}{\text{NumWords}} \times 100\right) - 26.01
    \end{align*}

Crawford's readability formula:
    {\text{Grade level} = \frac{\text{NumSentences}}{\text{NumWords}} \times 100 \times (-0.205) + \frac{\text{NumSyls}}{\text{NumWords}} \times 100 \times 0.049 - 3.407}

Dale-Chall readability formula:
    \begin{align*}
        \text{X}_{\text{c50}} &= 0.1579 \times \left(\frac{\text{NumWordsDale}_{3000}}{\text{NumWords}} \times 100\right) + 0.0496 \times \frac{\text{NumWords}}{\text{NumSentences}} + 3.6365 \\
        \text{X}_{\text{c50-Powers-Sumner-Kearl}} &= 3.2672 + 0.1155 \times \left(\frac{\text{NumWordsDale}_{3000}}{\text{NumWords}} \times 100\right) + 0.0596 \times \frac{\text{NumWords}}{\text{NumSentences}} \\
        \text{X}_{\text{c50-new}} &= 64 - 0.95 \times \left(\frac{\text{NumWordsDale}_{3000}}{\text{NumWords}} \times 100\right) - 0.69 \times \frac{\text{NumWords}}{\text{NumSentences}}
    \end{align*}

Danielson-Bryan's readability formula:
    \begin{align*}
        \text{Danielson-Bryan}_1 &= 1.0364 \times \frac{\text{NumCharsAll}}{\text{NumWords} - 1} + 0.0194 \times \frac{\text{NumCharsAll}}{\text{NumSentences}} - 0.6059 \\
        \text{Danielson-Bryan}_2 &= 131.059 - 10.364 \times \frac{\text{NumCharsAll}}{\text{NumWords} - 1} - 0.194 \times \frac{\text{NumCharsAll}}{\text{NumSentences}}
    \end{align*}

Dawood's readability formula:
    {\text{Dawood} = -0.0533 \times \frac{\text{NumCharsAlpha}}{\text{NumWords}} - 0.2066 \times \frac{\text{NumWords}}{\text{NumSentences}} + 5.5543 \times \frac{\text{NumWords}}{\text{NumWordTypes}} - 1.0801}

Degrees of Reading Power:
    \text{DRP} = 100 - (\lfloor \text{M} \times 100 + 0.5 \rfloor)

Devereux Readability Index:
    \text{Grade placement} = 1.56 \times \frac{\text{NumCharsAll}}{\text{NumWords}} + 0.19 \times \frac{\text{NumWords}}{\text{NumSentences}} - 6.49

Dickes-Steiwer Handformel:
    {\text{Dickes-Steiwer} = 235.95993 - \ln \left(\frac{\text{NumCharsAlpha}}{\text{NumWords}} + 1\right) \times 73.021 - \ln \left(\frac{\text{NumWords}}{\text{NumSentences}} + 1\right) \times 12.56438 - \frac{\text{NumWordTypes}}{\text{NumWords}} \times 50.03293}

Easy Listening Formula:
    \text{ELF} = \frac{\text{NumSyls} - \text{NumWords}}{\text{NumSentences}}

Flesch-Kincaid grade level:
    \text{GL} = 0.39 \times \frac{\text{NumWords}}{\text{NumSentences}} + 11.8 \times \frac{\text{NumSyls}}{\text{NumWords}} - 15.59

Flesch reading ease:
    \begin{align*}
        \text{wl} &= \frac{\text{NumSyls}}{\text{NumWords}} \qquad \text{sl} = \frac{\text{NumWords}}{\text{NumSentences}} \\
        \text{RE} &= 206.835 - 84.6 \times \text{wl} - 1.015 \times \text{sl} \\
        \text{RE}_\text{Powers-Sumner-Kearl} &= -2.2029 + 4.55 \times \text{wl} + 0.0778 \times \text{sl} \\
        \text{RE}_\text{Dutch-Douma} &= 206.84 - 77 \times \text{wl} - 0.93 \times \text{sl} \\
        \text{RE}_\text{Dutch-Brouwer} &= 195 - \frac{200}{3} \times \text{wl} - 2 \times \text{sl} \\
        \text{RE}_\text{French} &= 207 - 73.6 \times \text{wl} - 1.015 \times \text{sl} \\
        \text{RE}_\text{German} &= 180 - 58.5 \times \text{wl} - \text{sl} \\
        \text{RE}_\text{Italian} &= 217 - 60 \times \text{wl} - 1.3 \times \text{sl} \\
        \text{RE}_\text{Russian} &= 206.835 - 60.1 \times \text{wl} - 1.3 \times \text{sl} \\
        \text{RE}_{\text{Spanish-Fern}\acute{\text{a}}\text{ndez Huerta}} &= 206.84 - 60 \times \text{wl} - 1.02 \times \text{sl} \\
        \text{RE}_\text{Spanish-Szigriszt Pazos} &= 207 - 62.3 \times \text{wl} - \text{sl} \\
        \text{RE}_\text{Ukrainian} &= 206.84 - 28.3 \times \text{wl} - 5.93 \times \text{sl}
    \end{align*}

Flesch reading ease (Farr-Jenkins-Paterson):
    \begin{align*}
        \text{RE} &= 1.599 \times \left(\frac{\text{NumWordsSyl}_1}{\text{NumWords}} \times 100\right) - 1.015 \times \frac{\text{NumWords}}{\text{NumSentences}} - 31.517 \\
        \text{RE}_\text{Farr-Jenkins-Paterson} &= 8.4335 - 0.0648 \times \left(\frac{\text{NumWordsSyl}_1}{\text{NumWords}} \times 100\right) + 0.0923 \times \frac{\text{NumWords}}{\text{NumSentences}}
    \end{align*}

FORCAST:
    \text{RGL} = 20.43 - 0.11 \times \text{NumWordsSyl}_1

Fucks's Stilcharakteristik:
    \text{Stilcharakteristik} = \frac{\text{NumWords}}{\text{NumSentneces}} \times \frac{\text{NumSyls}}{\text{NumWords}}

GULPEASE:
    \text{GULPEASE} = 89 + \frac{300 \times \text{NumSentences} - 10 \times \text{NumCharsAlpha}}{\text{NumWords}}

Gunning Fog Index:
    \begin{align*}
        \text{Fog Index} &= 0.4 \times \left(\frac{\text{NumWords}}{\text{NumSentences}} + \frac{\text{NumHardWords}}{\text{NumWords}} \times 100\right) \\
        \text{Fog Index}_\text{Powers-Sumner-Kearl} &= 3.0680 + 0.0877 \times \frac{\text{NumWords}}{\text{NumSentences}} + 0.0984 \times \left(\frac{\text{NumHardWords}}{\text{NumWords}} \times 100\right) \\
        \text{Fog Index}_\text{Navy} &= \frac{\frac{\text{NumWords} + 2 \times \text{NumWordsSyls}_{3+}}{\text{NumSentences}} - 3}{2} \\
        \text{Fog Index}_\text{Polish} &= \frac{\sqrt{\left(\frac{\text{NumWords}}{\text{NumSentences}}\right)^2 + \left(\frac{\text{NumHardWords}}{\text{NumWords}} \times 100\right)^2}}{2}
    \end{align*}

Gutiérrez de Polini's readability formula:
    \text{CP} = 95.2 - 9.7 \times \frac{\text{NumCharsAlpha}}{\text{NumWords}} - 0.35 \times \frac{\text{NumWords}}{\text{NumSentences}}

Legibilidad µ:
    \mu = \frac{\text{NumWords}}{\text{NumWords} - 1} \times \frac{\text{LenWordsAvg}}{\text{LenWordsVar}} \times 100

Lensear Write Formula:
    \text{Score} = \text{NumWordsSyl}_1 + 3 \times \text{NumSentences}

Lix:
    \text{Lix} = \frac{\text{NumWords}}{\text{NumSentences}} + 100 \times \frac{\text{NumWordsLtrs}_{7+}}{\text{NumWords}}

Lorge Readability Index:
    \begin{align*}
        \text{Lorge} &= \frac{\text{NumWords}}{\text{NumSentences}} \times 0.07 + \frac{\text{NumPreps}}{\text{NumWords}} \times 13.01 + \frac{\text{NumWordTypesDale}_\text{769}}{\text{NumWords}} \times 10.73 + 1.6126 \\
        \text{Lorge}_\text{corrected} &= \frac{\text{NumWords}}{\text{NumSentences}} \times 0.06 + \frac{\text{NumPreps}}{\text{NumWords}} \times 0.1 + \frac{\text{NumWordTypesDale}_\text{769}}{\text{NumWords}} \times 0.1 + 1.99
    \end{align*}

Luong-Nguyen-Dinh's readability formula:
    {\text{Readability} = 0.004 \times \frac{\text{NumCharsAlnum}}{\text{NumSentences}} + 0.1905 \times \frac{\text{NumCharsAlnum}}{\text{NumWords}} + 2.7147 \times \frac{\text{NumSylsLuongNguyenDinh}_\text{1000}}{\text{NumSyls}} - 0.7295}

McAlpine EFLAW Readability Score:
    \text{EFLAW} = \frac{\text{NumWords} + \text{NumWordsLtrs}_{3-}}{\text{NumSentences}}

neue Wiener Literaturformeln:
    \begin{align*}
        \text{sW} &= \frac{\text{NumWordTypesBambergerVanecek}}{\text{NumWordTypes}} \times 100 \\
        \text{S/100} &= \frac{\text{NumSentences}}{\text{NumWords}} \times 100 \qquad \text{MS} = \frac{\text{NumWordsSyls}_{3+}}{\text{NumWords}} \times 100 \\
        \text{SL} &= \frac{\text{NumWords}}{\text{NumSentences}} \qquad \qquad \; \; \; \text{IW} = \frac{\text{NumWordsLtrs}_{7+}}{\text{NumWords}} \times 100 \\
        \text{nWL}_1 &= 0.2032 \times \text{sW} - 0.1715 \times \text{S/100} + 0.1594 \times \text{MS} - 0.0746 \times \text{SL} - 0.145 \\
        \text{nWL}_2 &= 0.2081 \times \text{sW} - 0.207 \times \text{S/100} + 0.1772 \times \text{MS} + 0.7498 \\
        \text{nWL}_3 &= 0.2373 \times \text{MS} + 0.2433 \times \text{SL} + 0.1508 \times \text{IW} - 3.9203
    \end{align*}

neue Wiener Sachtextformel:
    \begin{align*}
        \text{MS} &= \frac{\text{NumWordsSyls}_{3+}}{\text{NumWords}} \times 100 \qquad \text{SL} = \frac{\text{NumWords}}{\text{NumSentences}} \\
        \text{IW} &= \frac{\text{NumWordsLtrs}_{7+}}{\text{NumWords}} \times 100 \qquad \text{ES} = \frac{\text{NumWordsSyl}_1}{\text{NumWords}} \times 100 \\
        \text{nWS}_1 &= 0.1935 \times \text{MS} + 0.1672 \times \text{SL} + 0.1297 \times \text{IW} - 0.0327 \times \text{ES} - 0.875 \\
        \text{nWS}_2 &= 0.2007 \times \text{MS} + 0.1682 \times \text{SL} + 0.1373 \times \text{IW} - 2.779 \\
        \text{nWS}_3 &= 0.2963 \times \text{MS} + 0.1905 \times \text{SL} - 1.1144
    \end{align*}

OSMAN:
    \text{OSMAN} = 200.791 - 1.015 \times \frac{\text{NumWords}}{\text{NumSentences}} - 24.181 \times \frac{\text{NumWordsLtrs}_{6+} + \text{NumSyls} + \text{NumWordsSyls}_{5+} + \text{NumFaseehWords}}{\text{NumWords}}

Rix:
    \text{Rix} = \frac{\text{NumWordsLtrs}_{7+}}{\text{NumSentences}}

SMOG Grading:
    \begin{align*}
        \text{g} &= 3.1291 + 1.043 \times \sqrt{\text{NumWordsSyls}_{3+}} \\
        \text{g}_\text{German} &= \sqrt{\frac{\text{NumWordsSyl}_{3+}}{\text{NumSentences}} \times 30} - 2
    \end{align*}

Spache readability formula:
    \begin{align*}
        \text{Grade level} &= 0.141 \times \frac{100}{\text{NumSentences}} + 0.086 \times \left(\frac{\text{NumWordsDale}_{769}}{100} \times 100\right) + 0.839 \\
        \text{Grade level}_{revised} &= 0.121 \times \frac{100}{\text{NumSentences}} + 0.082 \times \left(\frac{\text{NumWordsSpache}}{100} \times 100\right) + 0.659
    \end{align*}

Strain Index:
    \text{Strain Index} = \frac{\text{NumSyls}}{10}

Tränkle-Bailer's readability formula:
    \begin{align*}
        \text{Tr}\ddot{\text{a}}\text{nkle-Bailer}_1 &= 224.6814 - \ln{\frac{\text{NumCharsAlnum}}{\text{NumWords}}} \times 79.8304 - \ln{\frac{\text{NumWords}}{\text{NumSentences}}} \times 12.24032 - \text{NumPreps} \times 1.292857 \\
        \text{Tr}\ddot{\text{a}}\text{nkle-Bailer}_2 &= 234.1063 - \ln{\frac{\text{NumCharsAlnum}}{\text{NumWords}}} \times 96.11069 - \text{NumPreps} \times 2.05444 - \text{NumConjs} \times 1.02805
    \end{align*}

Tuldava's readability formula:
    \text{TD} = \frac{\text{NumSyls}}{\text{NumWords}} \times \ln \frac{\text{NumWords}}{\text{NumSentences}}

Wheeler-Smith's readability formula:
    \text{Wheeler-Smith} = \frac{\text{NumWords}}{\text{NumUnits}} \times \frac{\text{NumWordsSyls}_{2+}}{\text{NumWords}} \times 10
-->

Readability Formula|Formula|Supported Languages
-------------------|-------|:-----------------:
<span id="ref-rd"></span>Al-Heeti's readability formula¹<br>([Al-Heeti, 1984, pp. 102, 104, 106](#ref-al-heeti-1984))|![Formula](/doc/measures/readability/rd.svg)|**Arabic**
<span id="ref-aari"></span>Automated Arabic Readability Index<br>([Al-Tamimi et al., 2013](#ref-al-tamimi-et-al-2013))|![Formula](/doc/measures/readability/aari.svg)|**Arabic**
<span id="ref-ari"></span>Automated Readability Index¹<br>([Smith & Senter, 1967, p. 8](#ref-smith-senter-1967)<br>Navy: [Kincaid et al., 1975, p. 14](#ref-kincaid-et-al-1975))|![Formula](/doc/measures/readability/ari.svg)|All languages
<span id="ref-bormuths-cloze-mean-gp"></span>Bormuth's cloze mean & grade placement<br>([Bormuth, 1969, pp. 152, 160](#ref-bormuth-1969))|![Formula](/doc/measures/readability/bormuths_cloze_mean_gp.svg)<br>where **C** is the cloze criterion score, whose value could be modified via **Menu Bar → Preferences → Settings → Measures → Readability → Bormuth's Grade Placement → Cloze criterion score**|**English**
<span id="ref-coleman-liau-index"></span>Coleman-Liau index<br>([Coleman & Liau, 1975](#ref-coleman-liau-1975))|![Formula](/doc/measures/readability/coleman_liau_index.svg)|All languages
<span id="ref-colemans-readability-formula"></span>Coleman's readability formula¹<br>([Liau et al., 1976](#ref-liau-et-al-1976))|![Formula](/doc/measures/readability/colemans_readability_formula.svg)|All languages²³
<span id="ref-crawfords-readability-formula"></span>Crawford's readability formula<br>([Crawford, 1985](#ref-crawford-1985))|![Formula](/doc/measures/readability/crawfords_readability_formula.svg)|**Spanish**²
<span id="ref-x-c50"></span>Dale-Chall readability formula¹<br>([Dale & Chall, 1948a](#ref-dale-chall-1948a); [Dale & Chall, 1948b](#ref-dale-chall-1948b)<br>Powers-Sumner-Kearl: [Powers et al., 1958](#ref-powers-et-al-1958)<br>New: [Chall & Dale, 1995, p. 66](#ref-chall-dale-1995))|![Formula](/doc/measures/readability/x_c50.svg)|**English**
<span id="ref-danielson-bryans-readability-formula"></span>Danielson-Bryan's readability formula¹<br>([Danielson & Bryan, 1963](#ref-danielson-bryan-1963))|![Formula](/doc/measures/readability/danielson_bryans_readability_formula.svg)|All languages
<span id="ref-dawoods-readability-formula"></span>Dawood's readability formula<br>([Dawood, 1977](#ref-dawood-1977))|![Formula](/doc/measures/readability/dawoods_readability_formula.svg)|**Arabic**
<span id="ref-drp"></span>Degrees of Reading Power<br>([College Entrance Examination Board, 1981](#ref-college-entrance-examination-board-1981))|![Formula](/doc/measures/readability/drp.svg)<br>where **M** is *Bormuth's cloze mean*.|**English**
<span id="ref-devereux-readability-index"></span>Devereux Readability Index<br>([Smith, 1961](#ref-smith-1961))|![Formula](/doc/measures/readability/devereux_readability_index.svg)|All languages
<span id="ref-dickes-steiwer-handformel"></span>Dickes-Steiwer Handformel<br>([Dickes & Steiwer, 1977](#ref-dickes-steiwer-1977))|![Formula](/doc/measures/readability/dickes_steiwer_handformel.svg)|All languages
<span id="ref-elf"></span>Easy Listening Formula<br>([Fang, 1966](#ref-fang-1966))|![Formula](/doc/measures/readability/elf.svg)|All languages²
<span id="ref-gl"></span>Flesch-Kincaid grade level<br>([Kincaid et al., 1975, p. 14](#ref-kincaid-et-al-1975))|![Formula](/doc/measures/readability/gl.svg)|All languages²
<span id="ref-re"></span>Flesch reading ease¹<br>([Flesch, 1948](#ref-flesch-1948)<br>Powers-Sumner-Kearl: [Powers et al., 1958](#ref-powers-et-al-1958)<br>Dutch: [Douma, 1960, p. 453](#ref-douma-1960); [Brouwer, 1963](#ref-brouwer-1963)<br>French: [Kandel & Moles, 1958](#ref-kandel-moles-1958)<br>German: [Amstad, 1978](#ref-amstad-1978)<br>Italian: [Franchina & Vacca, 1986](#ref-franchina-vacca-1986)<br>Russian: [Oborneva, 2006, p. 13](#ref-oborneva-2006)<br>Spanish: [Fernández Huerta, 1959](#ref-fernandez-huerta-1959); [Szigriszt Pazos, 1993, p. 247](#ref-szigrisze-pazos-1993)<br>Ukrainian: [Partiko, 2001](#ref-partiko-2001))|![Formula](/doc/measures/readability/re.svg)|All languages²
<span id="ref-re-farr-jenkins-paterson"></span>Flesch reading ease (Farr-Jenkins-Paterson)¹<br>([Farr et al., 1951](#ref-farr-et-al-1951)<br>Powers-Sumner-Kearl: [Powers et al., 1958](#ref-powers-et-al-1958))|![Formula](/doc/measures/readability/re_farr_jenkins_paterson.svg)|All languages²
<span id="ref-rgl"></span>FORCAST<br>([Caylor & Sticht, 1973, p. 3](#ref-caylor-sticht-1973))|![Formula](/doc/measures/readability/rgl.svg)<br><br>* **A 150-word-long sample** would be taken randomly from the text, so the text should be **at least 150 words long**.|All languages²
<span id="ref-fuckss-stilcharakteristik"></span>Fucks's Stilcharakteristik<br>([Fucks, 1955](#ref-fucks-1955))|![Formula](/doc/measures/readability/fuckss_stilcharakteristik.svg)|All languages²
<span id="ref-gulpease"></span>GULPEASE<br>([Lucisano & Emanuela Piemontese, 1988](#ref-lucisano-emanuela-piemontese-1988))|![Formula](/doc/measures/readability/gulpease.svg)|**Italian**
<span id="ref-fog-index"></span>Gunning Fog Index¹<br>(English: [Gunning, 1968, p. 38](#ref-gunning-1968)<br>Powers-Sumner-Kearl: [Powers et al., 1958](#ref-powers-et-al-1958)<br>Navy: [Kincaid et al., 1975, p. 14](#ref-kincaid-et-al-1975)<br>Polish: [Pisarek, 1969](#ref-pisarek-1969))|![Formula](/doc/measures/readability/fog_index.svg)<br>where **NumHardWords** is the number of words with 3 or more syllables, except proper nouns and words with 3 syllables ending with *-ed* or *-es*, for **English texts**, and the number of words with 4 or more syllables in their base forms, except proper nouns, for **Polish texts**.|**English & Polish**²
<span id="ref-cp"></span>Gutiérrez de Polini's readability formula<br>([Gutiérrez de Polini, 1972](#ref-gutierrez-de-polini-1972))|![Formula](/doc/measures/readability/cp.svg)|**Spanish**
<span id="ref-mu"></span>Legibilidad µ<br>([Muñoz Baquedano, 2006](#ref-munoz-baquedano-2006))|![Formula](/doc/measures/readability/mu.svg)<br>where **LenWordsAvg** is the average word length in letters, and **LenWordsVar** is the variance of word lengths in letters.|**Spanish**
<span id="ref-lensear-write-formula"></span>Lensear Write Formula<br>([O’Hayre, 1966, p. 8](#ref-o-hayre-1966))|![Formula](/doc/measures/readability/lensear_write_formula.svg)<br>where **NumWords1Syl** is the number of monosyllabic words excluding *the*, *is*, *are*, *was*, *were*.<br><br>* **A 100-word-long sample** would be taken randomly from the text. If the text is **shorter than 100 words**, **NumWords1Syl** and **NumSentences** would be multiplied by 100 and then divided by **NumWords**.|**English**²
<span id="ref-lix"></span>Lix<br>([Björnsson, 1968](#ref-bjornsson-1968))|![Formula](/doc/measures/readability/lix.svg)|All languages
<span id="ref-lorge-readability-index"></span>Lorge Readability Index¹<br>([Lorge, 1944](#ref-lorge-1944)<br>Corrected: [Lorge, 1948](#ref-lorge-1948))|![Formula](/doc/measures/readability/lorge_readability_index.svg)|**English**³
<span id="ref-luong-nguyen-dinhs-readability-formula"></span>Luong-Nguyen-Dinh's readability formula<br>([Luong et al., 2018](#ref-luong-et-al-2018))|![Formula](/doc/measures/readability/luong_nguyen_dinhs_readability_formula.svg)<br><br>* The number of syllables is estimated by tokenizing the text by whitespace and counting the number of tokens excluding punctuation marks.|**Vietnamese**
<span id="ref-eflaw"></span>McAlpine EFLAW Readability Score<br>([McAlpine, 2006](#ref-mcalpine-2006))|![Formula](/doc/measures/readability/eflaw.svg)|**English**
<span id="ref-nwl"></span>neue Wiener Literaturformeln¹<br>([Bamberger & Vanecek, 1984, p. 82](#ref-bamberger-vanecek-1984))|![Formula](/doc/measures/readability/nwl.svg)|**German**²
<span id="ref-nws"></span>neue Wiener Sachtextformel¹<br>([Bamberger & Vanecek, 1984, pp. 83–84](#ref-bamberger-vanecek-1984))|![Formula](/doc/measures/readability/nws.svg)|**German**²
<span id="ref-osman"></span>OSMAN<br>([El-Haj & Rayson, 2016](#ref-elhaj-rayson-2016))|![Formula](/doc/measures/readability/osman.svg)<br>where **NumFaseehWords** is the number of words which have 5 or more syllables and contain ء/ئ/ؤ/ذ/ظ or end with وا/ون.<br><br>* The number of syllables in each word is estimated by adding up the number of short syllables and twice the number of long and stress syllables in each word.|**Arabic**
<span id="ref-rix"></span>Rix<br>([Anderson, 1983](#ref-anderson-1983))|![Formula](/doc/measures/readability/rix.svg)|All languages
<span id="ref-smog-grading"></span>SMOG Grading<br>([McLaughlin, 1969](#ref-mclaughlin-1969)<br>German: [Bamberger & Vanecek, 1984, p.78](#ref-bamberger-vanecek-1984))|![Formula](/doc/measures/readability/smog_grading.svg)<br><br>* A sample consisting of **the first 10 sentences, the last 10 sentences, and the 10 sentences at the middle of the text** would be taken from the text, so the text should be **at least 30 sentences long**.|All languages²
<span id="ref-spache-readability-formula"></span>Spache readability formula¹<br>([Spache, 1953](#ref-spache-1953)<br>Revised: [Spache, 1974](#ref-spache-1974))|![Formula](/doc/measures/readability/spache_readability_formula.svg)<br><br>* **Three 100-word-long samples** would be taken randomly from the text and the results would be averaged out, so the text should be **at least 100 words long**.|English
<span id="ref-strain-index"></span>Strain Index<br>([Nathaniel, 2017](#ref-nathaniel-2017))|![Formula](/doc/measures/readability/strain_index.svg)<br><br>* A sample consisting of **the first 3 sentences of the text** would be taken from the text, so the text should be **at least 3 sentences long**.|All languages²
<span id="ref-trankle-bailers-readability-formula"></span>Tränkle-Bailer's readability formula¹<br>([Tränkle & Bailer, 1984](#ref-trankle-bailer-1984))|![Formula](/doc/measures/readability/trankle_bailers_readability_formula.svg)<br><br>* **A 100-word-long sample** would be taken randomly from the text, so the text should be **at least 100 words long**.|All languages³
<span id="ref-td"></span>Tuldava's readability formula<br>([Tuldava, 1975](#ref-tuldava-1975))|![Formula](/doc/measures/readability/td.svg)|All languages²
<span id="ref-wheeler-smiths-readability-formula"></span>Wheeler-Smith's readability formula<br>([Wheeler & Smith, 1954](#ref-wheeler-smith-1954))|![Formula](/doc/measures/readability/wheeler_smiths_readability_formula.svg)<br>where **NumUnits** is the number of sentence segments ending in periods, question marks, exclamation marks, colons, semicolons, and dashes.|All languages²

> [!NOTE]
> 1. Variants available and can be selected via **Menu Bar → Preferences → Settings → Measures → Readability**
> 1. Requires **built-in syllable tokenization support**
> 1. Requires **built-in part-of-speech tagging support**

<span id="doc-12-4-2"></span>
#### [12.4.2 Indicators of Lexical Density/Diversity](#doc)
Lexical density/diversity is the measurement of the extent to which the vocabulary used in the text varies.

The following variables would be used in formulas:<br>
**fᵢ**: Frequency of the i-th token type ranked descendingly by frequencies<br>
**fₘₐₓ**: Maximum frequency among all token types<br>
**NumTypes**: Number of token types<br>
**NumTypes<sub>f</sub>**: Number of token types whose frequencies equal **f**<br>
**NumTokens**: Number of tokens<br>

<!--
Brunet's index:
    \text{W} = \text{NumTokens}^{\text{NumTypes}^{-0.172}}

Corrected TTR:
    \text{CTTR} = \frac{\text{NumTypes}}{\sqrt{2 \times \text{NumTokens}}}

Fisher's Index of Diversity:
    \alpha = -\frac{\text{NumTokens} \times \text{NumTypes}}{\text{NumTokens} \times W_{-1}\left(-\frac{\exp\left(-\frac{\text{NumTypes}}{\text{NumTokens}}\right) \times \text{NumTypes}}{\text{NumTokens}}\right) + \text{NumTypes}}

Herdan's vₘ:
    \text{v}_\text{m} = \frac{\sum_{f = 1}^{\text{f}_\text{max}}(\text{NumTypes}_f \times f^2)}{\text{NumTokens}^2} - \frac{1}{\text{NumTypes}}

Honoré's statistic:
    \text{R} = 100 \times \ln\frac{\text{NumTokens}}{1 - \frac{\text{NumTypes}_1}{\text{NumTypes}}

Lexical density:
    \text{Lexical density} = \frac{\text{NumContentWords}}{\text{NumTokens}}

LogTTR:
    \begin{align*}
        \text{LogTTR}_\text{Herdan} &= \frac{\ln{\text{NumTypes}}}{\ln{\text{NumTokens}}} \\
        \text{LogTTR}_\text{Somers} &= \frac{\ln{\ln{\text{NumTypes}}}}{\ln{\ln{\text{NumTokens}}}} \\
        \text{LogTTR}_\text{Rubet} &= \frac{\ln{\text{NumTypes}}}{\ln{\ln{\text{NumTokens}}}} \\
        \text{LogTTR}_\text{Maas} &= \frac{\ln{\text{NumTokens}} - \ln{\text{NumTypes}}}{\ln^2{\text{NumTokens}}} \\
        \text{LogTTR}_\text{Dugast} &= \frac{\ln^2{\text{NumTokens}}}{\ln{\text{NumTokens}} - \ln{\text{NumTypes}}}
    \end{align*}

Mean segmental TTR:
    \text{MSTTR} = \frac{\sum_{i = 1}^{n}\frac{\text{NumTypesSeg}_i}{\text{NumTokensSeg}_i}}{n}

Moving-average TTR:
    \text{MATTR} = \frac{\sum_{p = 1}^{\text{NumTokens} - w + 1}\frac{\text{NumTypesWindow}_p}{\text{NumTokensWindow}_p}}{\text{NumTokens} - w + 1}

Popescu-Mačutek-Altmann's B₁/B₂/B₃/B₄/B₅:
    \begin{align*}
        \text{L} &= \sum_{i = 1}^{\text{NumTypes} - 1}\sqrt{(\text{f}_i - \text{f}_{i + 1})^2 + 1} \\
        \text{L}_\text{min} &= \sqrt{(\text{NumTypes} - 1)^2 + (\text{f}_1 - 1)^2} \\
        \text{L}_\text{max} &= \sqrt{(\text{f}_1 - 1)^2 + 1} + \text{NumTypes} - 2 \\
        \text{B}_1 &= \frac{\text{L}}{\text{L}_\text{max}} \\
        \text{B}_2 &= \frac{\text{L} - \text{L}_\text{min}}{\text{L}_\text{max} - \text{L}_\text{min}} \\
        \text{B}_3 &= \frac{\text{NumTypes} - 1}{\text{L}} \\
        \text{B}_4 &= \frac{\text{f}_1 - 1}{\text{L}} \\
        \text{B}_5 &= \frac{\text{NumTypes}_1}{\text{L}}
    \end{align*}

Repeat rate:
    \begin{align*}
        \text{RR}_\text{rank-frequency distribution} &= \frac{\sum_{i = 1}^\text{NumTypes}\text{f}_i^2}{\text{NumTokens}^2} \\
        \text{RR}_\text{frequency spectrum} &= \frac{\sum_{f = 1}^{\text{f}_\text{max}}\text{NumTypes}_f^2}{\text{NumTypes}^2}
    \end{align*}

Root TTR:
    \text{RTTR} = \frac{\text{NumTypes}}{\sqrt{\text{NumTokens}}}

Shannon entropy:
    \begin{align*}
        \text{H}_\text{rank-frequency distribution} &= -\sum_{i = 1}^\text{NumTypes}\left(\frac{\text{f}_i}{\text{NumTokens}} \times \log_{2}\frac{\text{f}_i}{\text{NumTokens}}\right) \\
        \text{H}_\text{frequency spectrum} &= -\sum_{f = 1}^{\text{f}_\text{max}}\left(\frac{\text{NumTypes}_f}{\text{NumTypes}} \times \log_{2}\frac{\text{NumTypes}_f}{\text{NumTypes}}\right)
    \end{align*}

Simpleson's l:
    \text{l} = \frac{\sum_{f = 1}^{\text{f}_\text{max}}(\text{NumTypes}_f \times f^2) - \text{NumTokens}}{\text{NumTokens} \times (\text{NumTokens} - 1)}

Type-token ratio:
    \text{TTR} = \frac{\text{NumTypes}}{\text{NumTokens}}

Yule's characteristic K:
    \text{K} = 10000 \times \frac{\sum_{f = 1}^{\text{f}_\text{max}}(\text{NumTypes}_f \times f^2) - \text{NumTokens}}{\text{NumTokens}^2}

Yule's Index of Diversity:
    \text{Index of Diversity} = \frac{\text{NumTokens}^2}{\sum_{f = 1}^{\text{f}_\text{max}}(\text{NumTypes}_f \times f^2) - \text{NumTokens}}
-->

Indicator of Lexical Density/Diversity|Formula
--------------------------------------|-------
<span id="ref-brunets-index"></span>Brunet's index<br>([Brunet, 1978, p. 57](#ref-brunet-1978))|![Formula](/doc/measures/lexical_density_diversity/brunets_index.svg)
<span id="ref-cttr"></span>Corrected TTR<br>([Carroll, 1964, p. 54](#ref-carroll-1964))|![Formula](/doc/measures/lexical_density_diversity/cttr.svg)
<span id="ref-fishers-index-of-diversity"></span>Fisher's Index of Diversity<br>([Fisher et al., 1943](#ref-fisher-et-al-1943))|![Formula](/doc/measures/lexical_density_diversity/fishers_index_of_diversity.svg)<br>where *W*₋₁ is the -1 branch of the [Lambert W function](https://en.wikipedia.org/wiki/Lambert_W_function).
<span id="ref-herdans-vm"></span>Herdan's vₘ<br>([Herdan, 1955](#ref-herdan-1955))|![Formula](/doc/measures/lexical_density_diversity/herdans_vm.svg)
<span id="ref-hdd"></span>HD-D<br>([McCarthy & Jarvis, 2010](#ref-mccarthy-jarvis-2010))|For detailed calculation procedures, see reference.<br><br>The sample size could be modified via **Menu Bar → Preferences → Settings → Measures → Lexical Density/Diversity → HD-D → Sample size**.
<span id="ref-honores-stat"></span>Honoré's statistic<br>([Honoré, 1979](#ref-honore-1979))|![Formula](/doc/measures/lexical_density_diversity/honores_stat.svg)
<span id="ref-lexical-density"></span>Lexical density<br>([Halliday, 1989, p. 64](#ref-halliday-1989))|![Formula](/doc/measures/lexical_density_diversity/lexical_density.svg)<br>where **NumContentWords** is the number of content words. By default, all tokens whose universal part-of-speech tags assigned by built-in part-of-speech taggers are ADJ (adjectives), ADV (adverbs), INTJ (interjections), NOUN (nouns), PROPN (proper nouns), NUM (numerals), VERB (verbs), SYM (symbols), or X (others) are categorized as content words. For some built-in part-of-speech taggers, this behavior could be modified via **Menu Bar → Preferences → Settings → Part-of-speech Tagging → Tagsets → Mapping Settings → Content/Function Words**.
<span id="ref-logttr"></span>LogTTR¹<br>(Herdan: [Herdan, 1960, p. 28](#ref-herdan-1960)<br>Somers: [Somers, 1966](#ref-somers-1966)<br>Rubet: [Dugast, 1979](#ref-dugast-1979)<br>Maas: [Maas, 1972](#ref-maas-1972)<br>Dugast: [Dugast, 1978](#ref-dugast-1978); [Dugast, 1979](#ref-dugast-1979))|![Formula](/doc/measures/lexical_density_diversity/logttr.svg)
<span id="ref-msttr"></span>Mean segmental TTR<br>([Johnson, 1944](#ref-johnson-1944))|![Formula](/doc/measures/lexical_density_diversity/msttr.svg)<br>where **n** is the number of equal-sized segment, the length of which could be modified via **Menu Bar → Preferences → Settings → Measures → Lexical Density/Diversity → Mean Segmental TTR → Number of tokens in each segment**, **NumTypesSegᵢ** is the number of token types in the **i**-th segment, and **NumTokensSegᵢ** is the number of tokens in the **i**-th segment.
<span id="ref-mtld"></span>Measure of textual lexical diversity<br>([McCarthy, 2005, pp. 95–96, 99–100](#ref-mccarthy-2005); [McCarthy & Jarvis, 2010](#ref-mccarthy-jarvis-2010))|For detailed calculation procedures, see references.<br><br>The factor size could be modified via **Menu Bar → Preferences → Settings → Measures → Lexical Density/Diversity → Measure of Textual Lexical Diversity → Factor size**.
<span id="ref-mattr"></span>Moving-average TTR<br>([Covington & McFall, 2010](#ref-covington-mcfall-2010))|![Formula](/doc/measures/lexical_density_diversity/mattr.svg)<br>where **w** is the window size which could be modified via **Menu Bar → Preferences → Settings → Measures → Lexical Density/Diversity → Moving-average TTR → Window size**, **NumTypesWindowₚ** is the number of token types within the moving window starting at position **p**, and **NumTokensWindowₚ** is the number of tokens within the moving window starting at position **p**.
<span id="ref-popescu-macutek-altmanns-b1-b2-b3-b4-b5"></span>Popescu-Mačutek-Altmann's B₁/B₂/B₃/B₄/B₅<br>([Popescu et al., 2008](#ref-popescu-et-al-2008))|![Formula](/doc/measures/lexical_density_diversity/popescu_macutek_altmanns_b1_b2_b3_b4_b5.svg)
<span id="ref-popescus-r1"></span>Popescu's R₁<br>([Popescu, 2009, pp. 18, 30, 33](#ref-popescu-2009))|For detailed calculation procedures, see reference.
<span id="ref-popescus-r2"></span>Popescu's R₂<br>([Popescu, 2009, pp. 35–36, 38](#ref-popescu-2009))|For detailed calculation procedures, see reference.
<span id="ref-popescus-r3"></span>Popescu's R₃<br>([Popescu, 2009, pp. 48–49, 53](#ref-popescu-2009))|For detailed calculation procedures, see reference.
<span id="ref-popescus-r4"></span>Popescu's R₄<br>([Popescu, 2009, p. 57](#ref-popescu-2009))|For detailed calculation procedures, see reference.
<span id="ref-repeat-rate"></span>Repeat rate¹<br>([Popescu, 2009, p. 166](#ref-popescu-2009))|![Formula](/doc/measures/lexical_density_diversity/repeat_rate.svg)
<span id="ref-rttr"></span>Root TTR<br>([Guiraud, 1954](#ref-guiraud-1954))|![Formula](/doc/measures/lexical_density_diversity/rttr.svg)
<span id="ref-shannon-entropy"></span>Shannon entropy¹<br>([Popescu, 2009, p. 173](#ref-popescu-2009))|![Formula](/doc/measures/lexical_density_diversity/shannon_entropy.svg)
<span id="ref-simpsons-l"></span>Simpson's l<br>([Simpson, 1949](#ref-simpson-1949))|![Formula](/doc/measures/lexical_density_diversity/simpsons_l.svg)
<span id="ref-ttr"></span>Type-token ratio<br>([Johnson, 1944](#ref-johnson-1944))|![Formula](/doc/measures/lexical_density_diversity/ttr.svg)
<span id="ref-vocdd"></span>vocd-D<br>([Malvern et al., 2004, pp. 51, 56–57](#ref-malvern-et-al-2004))|For detailed calculation procedures, see reference.
<span id="ref-yules-characteristic-k"></span>Yule's characteristic K<br>([Yule, 1944, pp. 52–53](#ref-yule-1944))|![Formula](/doc/measures/lexical_density_diversity/yules_characteristic_k.svg)
<span id="ref-yules-index-of-diversity"></span>Yule's Index of Diversity<br>([Williams, 1970, p. 100](#ref-williams-1970))|![Formula](/doc/measures/lexical_density_diversity/yules_index_of_diversity.svg)

> [!NOTE]
> 1. Variants available and can be selected via **Menu Bar → Preferences → Settings → Measures → Lexical Density/Diversity**

<span id="doc-12-4-3"></span>
#### [12.4.3 Measures of Dispersion and Adjusted Frequency](#doc)

For parts-based measures, each file is divided into **n** (whose value you could modify via **Menu Bar → Preferences → Settings → Measures → Dispersion / Adjusted Frequency → General Settings → Divide each file into subsections**) sub-sections and the frequency of the word in each part is counted and denoted by **F₁**, **F₂**, **F₃**, ..., **Fₙ** respectively. The total frequency of the word in each file is denoted by **F** and the mean value of the frequencies over all sub-sections is denoted by **F̅**.

For distance-based measures, the distance between each pair of subsequent occurrences of the word is calculated and denoted by **d₁**, **d₂**, **d₃**, ..., **d<sub>F</sub>** respectively. The total number of tokens in each file is denoted by **N**.

Then, the dispersion and adjusted frequency of the word are calculated as follows:

<!--
Average logarithmic distance:
    \begin{align*}
        \text{ALD} &= \frac{1}{N} \times \sum_{i = 1}^{F}(d_i \times \log_{10}d_i) \\
        \text{f}_{\text{ALD}} &= \exp\left(-\sum_{i = 1}^{F}{\frac{d_i}{N} \times \ln\frac{d_i}{N}}\right)
    \end{align*}

Average reduced frequency:
    \text{ARF} = \text{f}_{\text{ARF}} = \frac{F}{N} \times \sum_{i = 1}^{F}\min\left\{d_i, \frac{N}{F}\right\}

Average waiting time:
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
&nbsp;|<span id="ref-engwalls-fm"></span>Engwall's FM<br>([Engwall, 1974, p. 53](#ref-engwall-1974))|![Formula](/doc/measures/dispersion_adjusted_frequency/engwalls_fm.svg)<br>where **R** is the number of sub-sections in which the word appears at least once.
<span id="ref-griess-dp"></span>Gries's DP<br>([Gries, 2008](#ref-gries-2008); [Lijffijt & Gries, 2012](#ref-lijffijt-gries-2012))||![Formula](/doc/measures/dispersion_adjusted_frequency/griess_dp.svg)<br><br>* Normalization is applied by default, which behavior could be modified via **Menu Bar → Preferences → Settings → Measures → Dispersion → Gries's DP → Apply normalization**.
<span id="ref-juillands-d"></span>Juilland's D<br>([Juilland & Chang-Rodrigues, 1964, p. LIII](#ref-juilland-chang-rodrigues-1964))|<span id="ref-juillands-u"></span>Juilland's U<br>([Juilland & Chang-Rodrigues, 1964, p. LXVIII](#ref-juilland-chang-rodrigues-1964))|![Formula](/doc/measures/dispersion_adjusted_frequency/juillands_u.svg)
&nbsp;|<span id="ref-kromers-ur"></span>Kromer's U<sub>R</sub><br>([Kromer, 2003](#ref-kromer-2003))|![Formula](/doc/measures/dispersion_adjusted_frequency/kromers_ur.svg)<br>where **ψ** is the [digamma function](https://en.wikipedia.org/wiki/Digamma_function) and **C** is the [Euler–Mascheroni constant](https://en.wikipedia.org/wiki/Euler%E2%80%93Mascheroni_constant).
<span id="ref-lynes-d3"></span>Lyne's D₃<br>([Lyne, 1985, p. 129](#ref-lyne-1985))||![Formula](/doc/measures/dispersion_adjusted_frequency/lynes_d3.svg)
<span id="ref-rosengrens-s"></span>Rosengren's S<br>([Rosengren, 1971](#ref-rosengren-1971))|<span id="ref-rosengrens-kf"></span>Rosengren's KF<br>([Rosengren, 1971](#ref-rosengren-1971))|![Formula](/doc/measures/dispersion_adjusted_frequency/rosengrens_s.svg)
<span id="ref-zhangs-distributional-consistency"></span>Zhang's Distributional Consistency<br>([Zhang, 2004](#ref-zhang-2004))||![Formula](/doc/measures/dispersion_adjusted_frequency/zhangs_distributional_consistency.svg)

Measure of Dispersion (Distance-based)|Measure of Adjusted Frequency (Distance-based)|Formula
--------------------------------------|----------------------------------------------|-------
<span id="ref-ald"></span>Average logarithmic distance<br>([Savický & Hlaváčová, 2002](#ref-savicky-hlavacova-2002))|<span id="ref-fald"></span>Average logarithmic distance<br>([Savický & Hlaváčová, 2002](#ref-savicky-hlavacova-2002))|![Formula](/doc/measures/dispersion_adjusted_frequency/ald.svg)
<span id="ref-arf"></span>Average reduced frequency<br>([Savický & Hlaváčová, 2002](#ref-savicky-hlavacova-2002))|<span id="ref-farf"></span>Average reduced frequency<br>([Savický & Hlaváčová, 2002](#ref-savicky-hlavacova-2002))|![Formula](/doc/measures/dispersion_adjusted_frequency/arf.svg)
<span id="ref-awt"></span>Average waiting time<br>([Savický & Hlaváčová, 2002](#ref-savicky-hlavacova-2002))|<span id="ref-fawt"></span>Average waiting time<br>([Savický & Hlaváčová, 2002](#ref-savicky-hlavacova-2002))|![Formula](/doc/measures/dispersion_adjusted_frequency/awt.svg)

<span id="doc-12-4-4"></span>
#### [12.4.4 Tests of Statistical Significance, Measures of Bayes Factor, and Measures of Effect Size](#doc)

In order to calculate the test statistics of tests of statistical significance, Bayes factors, and effect sizes (except **Mann-Whitney U test** and **Student's t-test (2-sample)**) for potential collocations in *Collocation Extractor* and *Colligation Extractor* and potential keywords in *Keyword Extractor*, two contingency tables must be constructed first. One for observed values and the other for expected values.

As for potential collocations in *Collocation Extractor* and *Colligation Extractor*:

Observed Values|*Word 2*           |Not *Word 2*       |Row Total
--------------:|:-----------------:|:-----------------:|:---------------------------------:
*Word 1*       |O₁₁                |O₁₂                |O₁ₓ = *O₁₁* + *O₁₂*
Not *Word 1*   |O₂₁                |O₂₂                |O₂ₓ = *O₂₁* + *O₂₂*
Column Total   |Oₓ₁ = *O₁₁* + *O₂₁*|Oₓ₂ = *O₁₂* + *O₂₂*|Oₓₓ = *O₁₁* + *O₁₂* + *O₂₁* + *O₂₂*

Expected Values|*Word 2*             |Not *Word 2*
--------------:|:-------------------:|:-------------------:
*Word 1*       |![E₁₁](/doc/e_11.svg)|![E₁₂](/doc/e_12.svg)
Not *Word 1*   |![E₂₁](/doc/e_21.svg)|![E₂₂](/doc/e_22.svg)

O₁₁: Number of occurrences of the *Word 1* followed by the *Word 2*.<br>
O₁₂: Number of occurrences of the *Word 1* followed by any word except the *Word 2*.<br>
O₂₁: Number of occurrences of any word except the *Word 1* followed by the *Word 2*.<br>
O₂₂: Number of occurrences of any word except the *Word 1* followed by any word except the *Word 2*.<br>
O₁ₓ: Total frequency of the *Word 1* in the corpus.<br>
Oₓ₁: Total frequency of the *Word 2* in the corpus.<br>
Oₓₓ: Size of the corpus

As for potential keywords in *Keyword Extractor*:

Observed Values|Observed Corpus    |Reference Corpus   |Row Total
--------------:|:-----------------:|:-----------------:|:---------------------------------:
*Word w*       |O₁₁                |O₁₂                |O₁ₓ = *O₁₁* + *O₁₂*
*Not Word w*   |O₂₁                |O₂₂                |O₂ₓ = *O₂₁* + *O₂₂*
Column Total   |Oₓ₁ = *O₁₁* + *O₂₁*|Oₓ₂ = *O₁₂* + *O₂₂*|Oₓₓ = *O₁₁* + *O₁₂* + *O₂₁* + *O₂₂*

Expected Values|Observed Corpus      |Reference Corpus
--------------:|:-------------------:|:-------------------:
*Word w*       |![E₁₁](/doc/e_11.svg)|![E₁₂](/doc/e_12.svg)
*Not Word w*   |![E₂₁](/doc/e_21.svg)|![E₂₂](/doc/e_22.svg)

O₁₁: Number of occurrences of the *Word w* in the observed corpus.<br>
O₁₂: Number of occurrences of the *Word w* in the reference corpus.<br>
O₂₁: Number of occurrences of all words except the *Word w* in the observed corpus.<br>
O₂₂: Number of occurrences of all words except the *Word w* in the reference corpus.<br>
Oₓ₁: Size of the observed corpus.<br>
Oₓ₂: Size of the reference corpus.

To conduct **Mann-Whitney U test** and **Student's t-test (2-sample)** on a potential keyword, all tokens in the observed corpus and reference corpus are equally divided into **n** parts respectively. The frequencies of the *Word w* in the **n** sub-sections in the observed corpus and reference corpus are counted and denoted by **F₁₁**, **F₂₁**, **F₃₁**, ..., **Fₙ₁** and **F₁₂**, **F₂₂**, **F₃₂**, ..., **Fₙ₂** respectively. The total frequencies of the *Word w* in the observed corpus and reference corpus are denoted by **Fₓ₁** and **Fₓ₂** respectively. The mean values of the frequencies of the *Word w* over the **n** sub-sections in the observed corpus and reference corpus are denoted by ![f_x1_bar](/doc/measures/f_x1_bar.svg) and ![f_x2_bar](/doc/measures/f_x2_bar.svg) respectively.

Then the test statistics, Bayes factors, and effect sizes are calculated as follows:

<!--
Log-likelihood ratio test:
    \begin{align*}
        \text{G} &= 2 \times \sum_{i = 1}^2 \sum_{j = 1}^2 \left(O_{ij} \times \ln \frac{O_{ij}}{E_{ij}}\right) \\
        \text{BF} &= \text{G} - \ln O_{xx}
    \end{align*}

Pearson's chi-squared test:
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

Z-test:
    \text{z} = \frac{O_{11} - E_{11}}{\sqrt{E_{11} \times \left(1 - \frac{E_{11}}{O_{xx}}\right)}}

Z-test (Berry-Rogghe):
    \begin{align*}
        \text{p} &= \frac{O_{x1}}{O_{xx} - O_{1x}} \\
        \text{E} &= \text{p} \times O_{1x} \times \text{S} \\
        \text{z} &= \frac{O_{11} - \text{E}}{\sqrt{\text{E} \times (1 - \text{p})}}
    \end{align*}
-->

Test of Statistical Significance|Measure of Bayes Factor|Formula|Collocation Extraction|Keyword Extraction
--------------------------------|-----------------------|-------|:--------------------:|:----------------:
<span id="ref-fishers-exact-test"></span>Fisher's exact test<br>([Pedersen, 1996](#ref-pedersen-1996); [Kilgarriff, 2001, p. 105](#ref-kilgarriff-2001))||See: [Fisher's exact test - Wikipedia](https://en.wikipedia.org/wiki/Fisher%27s_exact_test#Example)|✔|✔
<span id="ref-log-likehood-ratio-test"></span>Log-likelihood ratio test<br>([Dunning, 1993](#ref-dunning-1993); [Kilgarriff, 2001, p. 105](#ref-kilgarriff-2001))|Log-likelihood ratio test<br>([Wilson, 2013](#ref-wilson-2013))|![Formula](/doc/measures/statistical_significance/log_likehood_ratio_test.svg)|✔|✔
<span id="ref-mann-whiteney-u-test"></span>Mann-Whitney U test<br>([Kilgarriff, 2001, pp. 103–104](#ref-kilgarriff-2001))||See: [Mann–Whitney U test - Wikipedia](https://en.wikipedia.org/wiki/Mann%E2%80%93Whitney_U_test#Calculations)|✖️|✔
<span id="ref-pearsons-chi-squared-test"></span>Pearson's chi-squared test<br>([Hofland & Johansson, 1982, p. 12](#ref-hofland-johansson-1982); [Dunning, 1993, p. 63](#ref-dunning-1993); [Oakes, 1998, p. 25](#ref-oakes-1998))||![Formula](/doc/measures/statistical_significance/pearsons_chi_squared_test.svg)|✔|✔
<span id="ref-students-t-test-1-sample"></span>Student's t-test (1-sample)<br>([Church et al., 1991, pp. 120–126](#ref-church-et-al-1991))||![Formula](/doc/measures/statistical_significance/students_t_test_1_sample.svg)|✔|✖️
<span id="ref-students-t-test-2-sample"></span>Student's t-test (2-sample)<br>([Paquot & Bestgen, 2009, pp. 252–253](#ref-paquot-bestgen-2009))|Student's t-test (2-sample)<br>([Wilson, 2013](#ref-wilson-2013))|![Formula](/doc/measures/statistical_significance/students_t_test_2_sample.svg)|✖️|✔
<span id="ref-z-test"></span>Z-test<br>([Dennis, 1964, p. 69](#ref-dennis-1964))||![Formula](/doc/measures/statistical_significance/z_test.svg)|✔|✖️
<span id="ref-z-test-berry-rogghes"></span>Z-test (Berry-Rogghe)<br>([Berry-Rogghe, 1973](#ref-berry-rogghe-1973))||![Formula](/doc/measures/statistical_significance/z_test_berry_rogghe.svg)<br>where **S** is the average span size on both sides of the node word.|✔|✖️

<!--
Conditional probability:
    \text{P} = \frac{O_{11}}{O_{1x}} \times 100

ΔP:
    \Delta\text{P} = \frac{O_{11}}{O_{1x}} - \frac{O_{21}}{O_{2x}}

Dice-Sørensen coefficient:
    \text{DSC} = \frac{2 \times O_{11}}{O_{1x} + O_{x1}}

Difference coefficient:
    \text{Difference coefficient} = \frac{\frac{O_{11}}{O_{x1}} - \frac{O_{12}}{O_{x2}}}{\frac{O_{11}}{O_{x1}} + \frac{O_{12}}{O_{x2}}}

Jaccard index:
    \text{J} = \frac{O_{11}}{O_{11} + O_{12} + O_{21}}

Kilgarriff's ratio:
    \text{Kilgarriff's ratio} = \frac{\frac{O_{11}}{O_{x1}} \times 1000000 + \alpha}{\frac{O_{12}}{O_{x2}} \times 1000000 + \alpha}

logDice:
    \text{logDice} = 14 + \log_{2} \frac{2 \times O_{11}}{O_{1x} + O_{x1}}

Log Ratio:
    \text{Log Ratio} = \log_{2} \frac{\frac{O_{11}}{O_{x1}}}{\frac{O_{12}}{O_{x2}}}

MI.log-f:
    \text{MI.log-f} = \log_{2} \frac{O_{11}}{E_{11}} \times \ln (O_{11} + 1)

Minimum sensitivity:
    \text{S}_\text{min} = \min\left\{\frac{O_{11}}{O_{1x}},\;\frac{O_{11}}{O_{x1}}\right\}

Mutual Expectation:
    \text{ME} = O_{11} \times \frac{2 \times O_{11}}{O_{1x} + O_{x1}}

Mutual information:
    \text{MI} = \sum_{i = 1}^2 \sum_{j = 1}^2 \left(\frac{O_{ij}}{O_{xx}} \times \log_{base} \frac{O_{ij}}{E_{ij}}\right)

Mutual information (normalized):
    \text{NMI} = \frac{\sum_{i = 1}^2 \sum_{j = 1}^2 \left(\frac{O_{ij}}{O_{xx}} \times \log_{base} \frac{O_{ij}}{E_{ij}}\right)}{-\sum_{i = 1}^2 \sum_{j = 1}^2 \left(\frac{O_{ij}}{O_{xx}} \times \log_{base} \frac{O_{ij}}{O_{xx}}\right)}

μ-value:
    \mu = \frac{O_{11}}{E_{11}}

Odds ratio:
    \text{OR} = \frac{O_{11} \times O_{22}}{O_{12} \times O_{21}}

%DIFF:
    \text{%DIFF} = \frac{\left(\frac{O_{11}}{O_{x1}} - \frac{O_{12}}{O_{x2}}\right) \times 100}{\frac{O_{12}}{O_{x2}}}

Pointwise mutual information:
    \text{PMI} = \log_{base} \frac{O_{11}}{E_{11}}

Pointwise mutual information (cubic):
    \text{IM}^3 = \log_{base} \frac{{O_{11}}^3}{E_{11}}

Pointwise mutual information (normalized):
    \text{NPMI} = \frac{\log_{base} \frac{O_{11}}{E_{11}}}{-\log_{base} \frac{O_{11}}{O_{xx}}}

Pointwise mutual information (squared):
    \text{IM}^2 = \log_{base} \frac{{O_{11}}^2}{E_{11}}

Poisson collocation measure:
    \text{sig} = \frac{O_{11} \times (\ln O_{11} - \ln E_{11} - 1)}{\ln O_{xx}}

Relative risk:
    \text{RR} = \frac{O_{11} \times O_{x2}}{O_{12} \times O_{x1}}

Squared phi coefficient:
    \phi^2 = \frac{(O_{11} \times O_{22} - O_{12} \times O_{21})^2}{O_{1x} \times O_{2x} \times O_{x1} \times O_{x2}}
-->

Measure of Effect Size|Formula|Collocation Extraction|Keyword Extraction
----------------------|-------|:--------------------:|:----------------:
<span id="ref-conditional-probability"></span>Conditional probability<br>([Durrant, 2008, p. 84](#ref-durrant-2008))|![Formula](/doc/measures/effect_size/conditional_probability.svg)|✔|✖️
<span id="ref-delta-p"></span><br>ΔP<br>([Gries, 2013](#ref-gries-2013))|![Formula](/doc/measures/effect_size/delta_p.svg)|✔|✖️
<span id="ref-dice-sorensen-coeff"></span>Dice-Sørensen coefficient<br>([Smadja et al., 1996, p. 8](#ref-smadja-et-al-1996))|![Formula](/doc/measures/effect_size/dice_sorensen_coeff.svg)|✔|✖️
<span id="ref-diff-coeff"></span>Difference coefficient<br>([Hofland & Johansson, 1982, p. 14](#ref-hofland-johansson-1982); [Gabrielatos, 2018, p. 236](#ref-gabrielatos-2018))|![Formula](/doc/measures/effect_size/diff_coeff.svg)|✖️|✔
<span id="ref-jaccard-index"></span>Jaccard index<br>([Dunning, 1998, p. 48](#ref-dunning-1998))|![Formula](/doc/measures/effect_size/jaccard_index.svg)|✔|✖️
<span id="ref-kilgarriffs-ratio"></span>Kilgarriff's ratio<br>([Kilgarriff, 2009](#ref-kilgarriff-2009))|![Formula](/doc/measures/effect_size/kilgarriffs_ratio.svg)<br>where **α** is the smoothing parameter, whose value could be modified via **Menu Bar → Preferences → Settings → Measures → Effect Size → Kilgarriff's Ratio → Smoothing parameter**.|✖️|✔
<span id="ref-log-dice"></span>logDice<br>([Rychlý, 2008, p. 9](#ref-rychly-2008))|![Formula](/doc/measures/effect_size/log_dice.svg)|✔|✖️
<span id="ref-log-ratio"></span>Log Ratio<br>([Hardie, 2014](#ref-hardie-2014))|![Formula](/doc/measures/effect_size/log_ratio.svg)|✔|✔
<span id="ref-mi-log-f"></span>MI.log-f<br>([Kilgarriff & Tugwell, 2001](#ref-kilgarriff-tugwell-2001); [Lexical Computing Ltd., 2015, p. 4](#ref-lexical-computing-ltd-2015))|![Formula](/doc/measures/effect_size/mi_log_f.svg)|✔|✖️
<span id="ref-min-sensitivity"></span>Minimum sensitivity<br>([Pedersen & Bruce, 1996](#ref-pedersen-bruce-1996))|![Formula](/doc/measures/effect_size/min_sensitivity.svg)|✔|✖️
<span id="ref-me"></span>Mutual Expectation<br>([Dias et al., 1999](#ref-dias-et-al-1999))|![Formula](/doc/measures/effect_size/me.svg)|✔|✖️
<span id="ref-mi"></span>Mutual information<br>([Dunning, 1998, pp. 49–52](#ref-dunning-1998); [Kilgarriff, 2001, pp. 104–105](#ref-kilgarriff-2001))|![Formula](/doc/measures/effect_size/mi.svg)<br>where **base** is the base of the logarithm, whose value could be modified via **Menu Bar → Preferences → Settings → Measures → Effect Size → Mutual Information → Base of logarithm**.|✔|✔
<span id="ref-nmi"></span>Mutual information (normalized)<br>([Bouma, 2009](#ref-bouma-2009); [Kilgarriff, 2001, pp. 104–105](#ref-kilgarriff-2001))|![Formula](/doc/measures/effect_size/nmi.svg)<br>where **base** is the base of the logarithm, whose value could be modified via **Menu Bar → Preferences → Settings → Measures → Effect Size → Mutual Information (Normalized) → Base of logarithm**.|✔|✔
<span id="ref-mu-val"></span>μ-value<br>([Evert, 2005, p. 54](#ref-evert-2005))|![Formula](/doc/measures/effect_size/mu_val.svg)|✔|✖️
<span id="ref-or"></span>Odds ratio<br>([Pecina, 2005, p. 15](#ref-pecina-2005); [Pojanapunya & Todd, 2016](#ref-pojanapunya-todd-2016))|![Formula](/doc/measures/effect_size/or.svg)|✔|✔
<span id="ref-pct-diff"></span>%DIFF<br>([Gabrielatos & Marchi, 2011](#ref-gabrielatos-marchi-2011))|![Formula](/doc/measures/effect_size/pct_diff.svg)|✖️|✔
<span id="ref-pmi"></span>Pointwise mutual information<br>([Church & Hanks, 1990](#ref-church-hanks-1990); [Kilgarriff, 2001, pp. 104–105](#ref-kilgarriff-2001))|![Formula](/doc/measures/effect_size/pmi.svg)<br>where **base** is the base of the logarithm, whose value could be modified via **Menu Bar → Preferences → Settings → Measures → Effect Size → Pointwise Mutual Information → Base of logarithm**.|✔|✔
<span id="ref-im3"></span>Pointwise mutual information (cubic)¹<br>([Daille, 1994, p. 139](#ref-daille-1994); [Kilgarriff, 2001, pp. 104–105](#ref-kilgarriff-2001))|![Formula](/doc/measures/effect_size/im3.svg)<br>where **base** is the base of the logarithm, whose value could be modified via **Menu Bar → Preferences → Settings → Measures → Effect Size → Pointwise Mutual Information (Cubic) → Base of logarithm**.|✔|✔
<span id="ref-npmi"></span>Pointwise mutual information (normalized)<br>([Bouma, 2009](#ref-bouma-2009); [Kilgarriff, 2001, pp. 104–105](#ref-kilgarriff-2001))|![Formula](/doc/measures/effect_size/npmi.svg)<br>where **base** is the base of the logarithm, whose value could be modified via **Menu Bar → Preferences → Settings → Measures → Effect Size → Pointwise Mutual Information (Normalized) → Base of logarithm**.|✔|✔
<span id="ref-im2"></span>Pointwise mutual information (squared)¹<br>([Daille, 1995, p. 21](#ref-daille-1995); [Kilgarriff, 2001, pp. 104–105](#ref-kilgarriff-2001))|![Formula](/doc/measures/effect_size/im2.svg)<br>where **base** is the base of the logarithm, whose value could be modified via **Menu Bar → Preferences → Settings → Measures → Effect Size → Pointwise Mutual Information (Squared) → Base of logarithm**.|✔|✔
<span id="ref-poisson-collocation-measure"></span>Poisson collocation measure<br>([Quasthoff & Wolff, 2002](#ref-quasthoff-wolff-2002))|![Formula](/doc/measures/effect_size/poisson_collocation_measure.svg)|✔|✖️
<span id="ref-rr"></span>Relative risk<br>([Evert, 2005, p. 55](#ref-evert-2005); [Gries, 2010, p. 276](#ref-gries-2010))|![Formula](/doc/measures/effect_size/rr.svg)|✔|✔
<span id="ref-squared-phi-coeff"></span>Squared phi coefficient<br>([Church & Gale, 1991](#ref-church-gale-1991))|![Formula](/doc/measures/effect_size/squared_phi_coeff.svg)|✔|✖️

> [!NOTE]
> 1. The calculation of *Pointwise mutual information (squared)* and *pointwise mutual information (cubic)* are exactly the same as that of *Mutual Dependency* and *Log-frequency biased MD* respectively which were proposed in:<br><br>Thanopoulos, A., Fakotakis, N., & Kokkinakis, G. (2002). Comparative evaluation of collocation extraction metrics. In M. G. González & C. P. S. Araujo (Eds.), *Proceedings of the Third International Conference on Language Resources and Evaluation (LREC’02)* (pp. 620–625). European Language Resources Association.

<span id="doc-13"></span>
## [13 References](#doc)
<span id="ref-al-heeti-1984"></span>
1. [**^**](#ref-rd) Al-Heeti, K. N. (1984). *Judgment analysis technique applied to readability prediction of Arabic reading material* (Publication No. 8411458) [Doctoral dissertation, University of Northern Colorado]. ProQuest Dissertations and Theses Global.
<span id="ref-al-tamimi-et-al-2013"></span>
1. [**^**](#ref-aari) Al-Tamimi, A., Jaradat M., Aljarrah, N., & Ghanim, S. (2013). AARI: Automatic Arabic Readability Index. *The International Arab Journal of Information Technology*, *11*(4), 370–378.
<span id="ref-amstad-1978"></span>
1. [**^**](#ref-re) Amstad, T. (1978). *Wie verständlich sind unsere Zeitungen?* [Unpublished doctoral dissertation]. University of Zurich.
<span id="ref-anderson-1983"></span>
1. [**^**](#ref-rix) Anderson, J. (1983). Lix and Rix: Variations on a little-known readability index. *Journal of Reading*, *26*(6), 490–496.
<span id="ref-bamberger-vanecek-1984"></span>
1. [**^**](#ref-num-word-types-bamberger-vanecek) [**^**](#ref-nwl) [**^**](#ref-nws) [**^**](#ref-smog-grading) Bamberger, R., & Vanecek, E. (1984). *Lesen-verstehen-lernen-schreiben: Die schwierigkeitsstufen von texten in deutscher sprache*. Jugend und Volk.
<span id="ref-berry-rogghe-1973"></span>
1. [**^**](#ref-z-test-berry-rogghes) Berry-Rogghe, G. L. M. (1973). The computation of collocations and their relevance in lexical studies. In A. J. Aiken, R. W. Bailey, & N. Hamilton-Smith (Eds.), *The computer and literary studies* (pp. 103–112). Edinburgh University Press.
<span id="ref-bormuth-1969"></span>
1. [**^**](#ref-bormuths-cloze-mean-gp) Bormuth, J. R. (1969). *Development of readability analyses*. U.S. Department of Health, Education, and Welfare. http://files.eric.ed.gov/fulltext/ED029166.pdf
<span id="ref-bouma-2009"></span>
1. [**^**](#ref-nmi) [**^**](#ref-npmi) Bouma, G. (2009). Normalized (pointwise) mutual information in collocation extraction. In C. Chiarcos, R. Eckart de Castilho, & M. Stede (Eds.), *From form to meaning: processing texts automatically: Proceedings of the Biennial GSCL Conference 2009* (pp. 31–40). Gunter Narr Verlag.
<span id="ref-bjornsson-1968"></span>
1. [**^**](#ref-lix) Björnsson, C.-H. (1968). *Läsbarhet*. Liber.
<span id="ref-brouwer-1963"></span>
1. [**^**](#ref-re) Brouwer, R. H. M. (1963). Onderzoek naar de leesmoeilijkheid van Nederlands proza. *Paedagogische Studiën*, *40*, 454–464. https://objects.library.uu.nl/reader/index.php?obj=1874-205260&lan=en
<span id="ref-brunet-1978"></span>
1. [**^**](#ref-brunets-index) Brunet, E. (1978). *Le vocabulaire de Jean Giraudoux: Structure et evolution*. Slatkine.
<span id="ref-carroll-1964"></span>
1. [**^**](#ref-cttr) Carroll, J. B. (1964). *Language and thought*. Prentice-Hall.
<span id="ref-carroll-1970"></span>
1. [**^**](#ref-carrolls-d2) [**^**](#ref-carrolls-um) Carroll, J. B. (1970). An alternative to Juillands's usage coefficient for lexical frequencies. *ETS Research Bulletin Series*, *1970*(2), i–15. https://doi.org/10.1002/j.2333-8504.1970.tb00778.x
<span id="ref-caylor-sticht-1973"></span>
1. [**^**](#ref-rgl) Caylor, J. S., & Sticht, T. G. (1973). *Development of a simple readability index for job reading material*. Human Resource Research Organization. https://ia902703.us.archive.org/31/items/ERIC_ED076707/ERIC_ED076707.pdf
<span id="ref-chall-dale-1995"></span>
1. [**^**](#ref-x-c50) Chall, J. S., & Dale, E. (1995). *Readability revisited: The new Dale-Chall readability formula*. Brookline Books.
<span id="ref-church-gale-1991"></span>
1. [**^**](#ref-squared-phi-coeff) Church, K. W., & Gale, W. A. (1991, September 29–October 1). *Concordances for parallel text* [Paper presentation]. Using Corpora: Seventh Annual Conference of the UW Centre for the New OED and Text Research, St. Catherine's College, Oxford, United Kingdom.
<span id="ref-church-et-al-1991"></span>
1. [**^**](#ref-students-t-test-1-sample) Church, K., Gale, W., Hanks, P., & Hindle, D. (1991). Using statistics in lexical analysis. In U. Zernik (Ed.), *Lexical acquisition: Exploiting on-line resources to build a lexicon* (pp. 115–164). Psychology Press.
<span id="ref-church-hanks-1990"></span>
1. [**^**](#ref-pmi) Church, K. W., & Hanks, P. (1990). Word association norms, mutual information, and lexicography. *Computational Linguistics*, *16*(1), 22–29.
<span id="ref-coleman-liau-1975"></span>
1. [**^**](#ref-coleman-liau-index) Coleman, M., & Liau, T. L. (1975). A computer readability formula designed for machine scoring. *Journal of Applied Psychology*, *60*(2), 283–284. https://doi.org/10.1037/h0076540
<span id="ref-college-entrance-examination-board-1981"></span>
1. [**^**](#ref-drp) College Entrance Examination Board. (1981). *Degrees of reading power brings the students and the text together*.
<span id="ref-covington-mcfall-2010"></span>
1. [**^**](#ref-mattr) Covington, M. A., & McFall, J. D. (2010). Cutting the Gordian knot: The moving-average type-token ratio (MATTR). *Journal of Quantitative Linguistics*, *17*(2), 94–100. https://doi.org/10.1080/09296171003643098
<span id="ref-crawford-1985"></span>
1. [**^**](#ref-crawfords-readability-formula) Crawford, A. N. (1985). Fórmula y gráfico para determinar la comprensibilidad de textos de nivel primario en castellano. *Lectura y Vida*, *6*(4). http://www.lecturayvida.fahce.unlp.edu.ar/numeros/a6n4/06_04_Crawford.pdf
<span id="ref-daille-1994"></span>
1. [**^**](#ref-im3) Daille, B. (1994). *Approche mixte pour l'extraction automatique de terminologie: statistiques lexicales et filtres linguistiques* [Doctoral thesis, Paris Diderot University]. Béatrice Daille. http://www.bdaille.com/index.php?option=com_docman&task=doc_download&gid=8&Itemid=
<span id="ref-daille-1995"></span>
1. [**^**](#ref-im2) Daille, B. (1995). Combined approach for terminology extraction: Lexical statistics and linguistic filtering. *UCREL technical papers* (Vol. 5). Lancaster University.
<span id="ref-dale-1931"></span>
1. [**^**](#ref-num-words-dale-769) [**^**](#ref-num-word-types-dale-769) Dale, E. (1931). A comparison of two word lists. *Educational Research Bulletin*, *10*(18), 484–489.
<span id="ref-dale-chall-1948a"></span>
1. [**^**](#ref-x-c50) Dale, E., & Chall, J. S. (1948a). A formula for predicting readability. *Educational Research Bulletin*, *27*(1), 11–20, 28.
<span id="ref-dale-chall-1948b"></span>
1. [**^**](#ref-num-words-dale-3000) [**^**](#ref-x-c50) Dale, E., & Chall, J. S. (1948b). A formula for predicting readability: Instructions. *Educational Research Bulletin*, *27*(2), 37–54.
<span id="ref-danielson-bryan-1963"></span>
1. [**^**](#ref-danielson-bryans-readability-formula) Danielson, W. A., & Bryan, S. D. (1963). Computer automation of two readability formulas. *Journalism Quarterly*, *40*(2), 201–206. https://doi.org/10.1177/107769906304000207
<span id="ref-dawood-1977"></span>
1. [**^**](#ref-dawoods-readability-formula) Dawood, B.A.K. (1977). *The relationship between readability and selected language variables* [Unpublished master’s thesis]. University of Baghdad.
<span id="ref-dennis-1964"></span>
1. [**^**](#ref-z-test) Dennis, S. F. (1964). The construction of a thesaurus automatically from a sample of text. In M. E. Stevens, V. E. Giuliano, & L. B. Heilprin (Eds.), *Statistical association methods for mechanized documentation: Symposium proceedings* (pp. 61–148). National Bureau of Standards.
<span id="ref-dias-et-al-1999"></span>
1. [**^**](#ref-me) Dias, G., Guilloré, S., & Pereira Lopes, J. G. (1999). Language independent automatic acquisition of rigid multiword units from unrestricted text corpora. In A. Condamines, C. Fabre, & M. Péry-Woodley (Eds.), *TALN'99: 6ème Conférence Annuelle Sur le Traitement Automatique des Langues Naturelles* (pp. 333–339). TALN.
<span id="ref-dickes-steiwer-1977"></span>
1. [**^**](#ref-dickes-steiwer-handformel) Dickes, P. & Steiwer, L. (1977). Ausarbeitung von lesbarkeitsformeln für die deutsche sprache. *Zeitschrift für Entwicklungspsychologie und Pädagogische Psychologie*, *9*(1), 20–28.
<span id="ref-douma-1960"></span>
1. [**^**](#ref-re) Douma, W. H. (1960). *De leesbaarheid van landbouwbladen: Een onderzoek naar en een toepassing van leesbaarheidsformules* [Readability of Dutch farm papers: A discussion and application of readability-formulas]. Afdeling Sociologie en Sociografie van de Landbouwhogeschool Wageningen. https://edepot.wur.nl/276323
<span id="ref-dugast-1978"></span>
1. [**^**](#ref-logttr) Dugast, D. (1978). Sur quoi se fonde la notion d’étendue théoretique du vocabulaire? *Le Français Moderne*, *46*, 25–32.
<span id="ref-dugast-1979"></span>
1. [**^**](#ref-logttr) [**^**](#ref-logttr) Dugast, D. (1979). *Vocabulaire et stylistique: I théâtre et dialogue, travaux de linguistique quantitative*. Slatkine.
<span id="ref-dunning-1993"></span>
1. [**^**](#ref-log-likehood-ratio-test) [**^**](#ref-pearsons-chi-squared-test) Dunning, T. E. (1993). Accurate methods for the statistics of surprise and coincidence. *Computational Linguistics*, *19*(1), 61–74.
<span id="ref-dunning-1998"></span>
1. [**^**](#ref-jaccard-index) [**^**](#ref-mi) Dunning, T. E. (1998). *Finding structure in text, genome and other symbolic sequences* [Doctoral dissertation, University of Sheffield]. arXiv. https://arxiv.org/pdf/1207.1847
<span id="ref-durrant-2008"></span>
1. [**^**](#ref-conditional-probability) Durrant, P. (2008). *High frequency collocations and second language learning* [Doctoral dissertation, University of Nottingham]. Nottingham eTheses. https://eprints.nottingham.ac.uk/10622/1/final_thesis.pdf
<span id="ref-elhaj-rayson-2016"></span>
1. [**^**](#ref-osman) El-Haj, M., & Rayson, P. (2016). OSMAN: A novel Arabic readability metric. In N. Calzolari, K. Choukri, T. Declerck, S. Goggi, M. Grobelnik, B. Maegaard, J. Mariani, H. Mazo, A. Moreno, J. Odijk, & S. Piperidis (Eds.), *Proceedings of the Tenth International Conference on Language Resources and Evaluation (LREC 2016)* (pp. 250–255). European Language Resources Association. http://www.lrec-conf.org/proceedings/lrec2016/index.html
<span id="ref-engwall-1974"></span>
1. [**^**](#ref-engwalls-fm) Engwall, G. (1974). *Fréquence et distribution du vocabulaire dans un choix de romans français* [Unpublished doctoral dissertation]. Stockholm University.
<span id="ref-evert-2005"></span>
1. [**^**](#ref-mu-val) [**^**](#ref-rr) Evert, S. (2005). *The statistics of word cooccurrences: Word pairs and collocations* [Doctoral dissertation, University of Stuttgart]. OPUS - Online Publikationen der Universität Stuttgart. https://doi.org/10.18419/opus-2556
<span id="ref-fang-1966"></span>
1. [**^**](#ref-elf) Fang, I. E. (1966). The easy listening formula. *Journal of Broadcasting*, *11*(1), 63–68. https://doi.org/10.1080/08838156609363529
<span id="ref-farr-et-al-1951"></span>
1. [**^**](#ref-re-farr-jenkins-paterson) Farr, J. N., Jenkins, J. J., & Paterson, D. G. (1951). Simplification of Flesch reading ease formula. *Journal of Applied Psychology*, *35*(5), 333–337. https://doi.org/10.1037/h0062427
<span id="ref-fernandez-huerta-1959"></span>
1. [**^**](#ref-re) Fernández Huerta, J. (1959). Medidas sencillas de lecturabilidad. *Consigna*, *214*, 29–32.
<span id="ref-fisher-et-al-1943"></span>
1. [**^**](#ref-fishers-index-of-diversity) Fisher, R. A., Steven, A. C., & Williams, C. B. (1943). The relation between the number of species and the number of individuals in a random sample of an animal population. *Journal of Animal Ecology*, *12*(1), 42–58. https://doi.org/10.2307/1411
<span id="ref-flesch-1948"></span>
1. [**^**](#ref-re) Flesch, R. (1948). A new readability yardstick. *Journal of Applied Psychology*, *32*(3), 221–233. https://doi.org/10.1037/h0057532
<span id="ref-franchina-vacca-1986"></span>
1. [**^**](#ref-re) Franchina, V., & Vacca, R. (1986). Adaptation of Flesh readability index on a bilingual text written by the same author both in Italian and English languages. *Linguaggi*, *3*, 47–49.
<span id="ref-fucks-1955"></span>
1. [**^**](#ref-fuckss-stilcharakteristik) Fucks, W. (1955). *Unterschied des prosastils von dichtern und anderen schriftstellern: Ein beispiel mathematischer stilanalyse*. Bouvier.
<span id="ref-gabrielatos-2018"></span>
1. [**^**](#ref-diff-coeff) Gabrielatos, C. (2018). Keyness analysis: Nature, metrics and techniques. In C. Taylor & A. Marchi (Eds.), *Corpus approaches to discourse: A critical review* (pp. 225–258). Routledge.
<span id="ref-gabrielatos-marchi-2011"></span>
1. [**^**](#ref-pct-diff) Gabrielatos, C., & Marchi, A. (2011, November 5). *Keyness: Matching metrics to definitions* [Conference session]. Corpus Linguistics in the South 1, University of Portsmouth, United Kingdom. https://eprints.lancs.ac.uk/id/eprint/51449/4/Gabrielatos_Marchi_Keyness.pdf
<span id="ref-gries-2008"></span>
1. [**^**](#ref-griess-dp) Gries, S. T. (2008). Dispersions and adjusted frequencies in corpora. *International Journal of Corpus Linguistics*, *13*(4), 403–437. https://doi.org/10.1075/ijcl.13.4.02gri
<span id="ref-gries-2010"></span>
1. [**^**](#ref-rr) Gries, S. T. (2010). Useful statistics for corpus linguistics. In A. Sánchez Pérez & M. Almela Sánchez (Eds.), A mosaic of corpus linguistics: Selected papers (pp. 269–291). Peter Lang.
<span id="ref-gries-2013"></span>
1. [**^**](#ref-delta-p) Gries, S. T. (2013). 50-something years of work on collocations: What is or should be next …. *International Journal of Corpus Linguistics*, *18*(1), 137–165. https://doi.org/10.1075/ijcl.18.1.09gri
<span id="ref-guiraud-1954"></span>
1. [**^**](#ref-rttr) Guiraud, P. (1954). *Les caractères statistiques du vocabulaire: Essai de méthodologie*. Presses Universitaires de France.
<span id="ref-gunning-1968"></span>
1. [**^**](#ref-fog-index) Gunning, R. (1968). *The technique of clear writing* (revised ed.). McGraw-Hill Book Company.
<span id="ref-gutierrez-de-polini-1972"></span>
1. [**^**](#ref-cp) Gutiérrez de Polini, L. E. (1972). *Investigación sobre lectura en Venezuela* [Paper presentation]. Primeras Jornadas de Educación Primaria, Ministerio de Educación, Caracas, Venezuela.
<span id="ref-halliday-1989"></span>
1. [**^**](#ref-lexical-density) Halliday, M. A. K. (1989). *Spoken and written language* (2nd ed.). Oxford University Press.
<span id="ref-hardie-2014"></span>
1. [**^**](#ref-log-ratio) Hardie, A. (2014, April 28). *Log Ratio: An informal introduction*. ESRC Centre for Corpus Approaches to Social Science (CASS). http://cass.lancs.ac.uk/log-ratio-an-informal-introduction/
<span id="ref-herdan-1955"></span>
1. [**^**](#ref-herdans-vm) Herdan, G. (1955). A new derivation and interpretation of Yule's ‘Characteristic’ K. *Zeitschrift für Angewandte Mathematik und Physik (ZAMP)*, *6*(4), 332–339. https://doi.org/10.1007/BF01587632
<span id="ref-herdan-1960"></span>
1. [**^**](#ref-logttr) Herdan, G. (1960). *Type-token mathematics: A textbook of mathematical linguistics*. Mouton.
<span id="ref-hofland-johansson-1982"></span>
1. [**^**](#ref-pearsons-chi-squared-test) [**^**](#ref-diff-coeff) Hofland, K., & Johansson, S. (1982). *Word frequencies in British and American English*. Norwegian Computing Centre for the Humanities.
<span id="ref-honore-1979"></span>
1. [**^**](#ref-honores-stat) Honoré, A. (1979). Some simple measures of richness of vocabulary. *Association of Literary and
Linguistic Computing Bulletin*, *7*(2), 172–177.
<span id="ref-johnson-1944"></span>
1. [**^**](#ref-msttr) [**^**](#ref-ttr) Johnson, W. (1944). Studies in language behavior: I. a program of research. *Psychological Monographs*, *56*(2), 1–15. https://doi.org/10.1037/h0093508
<span id="ref-juilland-chang-rodrigues-1964"></span>
1. [**^**](#ref-juillands-d) [**^**](#ref-juillands-u) Juilland, A., & Chang-Rodriguez, E. (1964). *Frequency dictionary of Spanish words*. Mouton.
<span id="ref-kandel-moles-1958"></span>
1. [**^**](#ref-re) Kandel, L., & Moles, A. (1958). Application de l’indice de flesch à la langue française. *The Journal of Educational Research*, *21*, 283–287.
<span id="ref-kilgarriff-2001"></span>
1. [**^**](#ref-fishers-exact-test) [**^**](#ref-log-likehood-ratio-test) [**^**](#ref-mann-whiteney-u-test) [**^**](#ref-mi) [**^**](#ref-nmi) [**^**](#ref-pmi) [**^**](#ref-im3) [**^**](#ref-npmi) [**^**](#ref-im2) Kilgarriff, A. (2001). Comparing corpora. *International Journal of Corpus Linguistics*, *6*(1), 232–263. https://doi.org/10.1075/ijcl.6.1.05kil
<span id="ref-kilgarriff-2009"></span>
1. [**^**](#ref-kilgarriffs-ratio) Kilgarriff, A. (2009). Simple maths for keywords. In M. Mahlberg, V. González-Díaz, & C. Smith (Eds.), *Proceedings of the Corpus Linguistics Conference 2009 (CL2009)* (Article 171). University of Liverpool.
<span id="ref-kilgarriff-tugwell-2001"></span>
1. [**^**](#ref-mi-log-f) Kilgarriff, A., & Tugwell, D. (2001). WASP-bench: An MT lexicographers' workstation supporting state-of-the-art lexical disambiguation. In B. Maegaard (Ed.), *Proceedings of Machine Translation Summit VIII* (pp. 187–190). European Association for Machine Translation.
<span id="ref-kincaid-et-al-1975"></span>
1. [**^**](#ref-ari) [**^**](#ref-gl) [**^**](#ref-fog-index) Kincaid, J. P., Fishburne, R. P., Rogers, R. L., & Chissom, B. S. (1975). *Derivation of new readability formulas (automated readability index, fog count, and Flesch reading ease formula) for Navy enlisted personnel* (Report No. RBR 8-75). Naval Air Station Memphis. https://apps.dtic.mil/sti/pdfs/ADA006655.pdf
<span id="ref-kromer-2003"></span>
1. [**^**](#ref-kromers-ur) Kromer, V. (2003). A usage measure based on psychophysical relations. *Journal of Quantitative Linguistics*, *10*(2), 177–186. https://doi.org/10.1076/jqul.10.2.177.16718
<span id="ref-lexical-computing-ltd-2015"></span>
1. [**^**](#ref-mi-log-f) Lexical Computing. (2015, July 8). *Statistics used in Sketch Engine*. Sketch Engine. https://www.sketchengine.eu/documentation/statistics-used-in-sketch-engine/
<span id="ref-liau-et-al-1976"></span>
1. [**^**](#ref-colemans-readability-formula) Liau, T. L., Bassin, C. B., Martin, C. J., & Coleman, E. B. (1976). Modification of the Coleman readability formulas. *Journal of Reading Behavior*, *8*(4), 381–386. https://journals.sagepub.com/doi/pdf/10.1080/10862967609547193
<span id="ref-lijffijt-gries-2012"></span>
1. [**^**](#ref-griess-dp) Lijffijt, J., & Gries, S. T. (2012). Correction to Stefan Th. Gries’ “dispersions and adjusted frequencies in corpora”. *International Journal of Corpus Linguistics*, *17*(1), 147–149. https://doi.org/10.1075/ijcl.17.1.08lij
<span id="ref-lorge-1944"></span>
1. [**^**](#ref-lorge-readability-index) Lorge, I. (1944). Predicting readability. *Teachers College Record*, *45*, 404–419.
<span id="ref-lorge-1948"></span>
1. [**^**](#ref-lorge-readability-index) Lorge, I. (1948). The Lorge and Flesch readability formulae: A correction. *School and Society*, *67*, 141–142.
<span id="ref-lucisano-emanuela-piemontese-1988"></span>
1. [**^**](#ref-gulpease) Lucisano, P., & Emanuela Piemontese, M. (1988). GULPEASE: A formula for the prediction of the difficulty of texts in Italian. *Scuola e Città*, *39*(3), 110–124.
<span id="ref-luong-et-al-2018"></span>
1. [**^**](#ref-num-syls-luong-nguyen-dinh-1000) [**^**](#ref-luong-nguyen-dinhs-readability-formula) Luong, A.-V., Nguyen, D., & Dinh, D. (2018). A new formula for Vietnamese text readability assessment. In T. M. Phuong & M. L. Nguyen (Eds.), *Proceedings of 2018 10th International Conference on Knowledge and Systems Engineering (KSE)* (pp. 198–202). IEEE. https://doi.org/10.1109/KSE.2018.8573379
<span id="ref-lyne-1985"></span>
1. [**^**](#ref-lynes-d3) Lyne, A. A. (1985). *The vocabulary of French business correspondence: Word frequencies, collocations, and problems of lexicometric method*. Slatkine.
<span id="ref-malvern-et-al-2004"></span>
1. [**^**](#ref-vocdd) Malvern, D., Richards, B., Chipere, N., & Durán, P. (2004). *Lexical diversity and language development: Quantification and assessment*. Palgrave Macmillan.
<span id="ref-maas-1972"></span>
1. [**^**](#ref-logttr) Maas, H.-D. (1972). Über den zusammenhang zwischen wortschatzumfang und länge eines textes. *Zeitschrift für Literaturwissenschaft und Linguistik*, *2*(8), 73–96.
<span id="ref-mcalpine-2006"></span>
1. [**^**](#ref-eflaw) McAlpine, R. (2006). *From plain English to global English*. Journalism Online. Retrieved October 31, 2024, from https://www.angelfire.com/nd/nirmaldasan/journalismonline/fpetge.html
<span id="ref-mccarthy-2005"></span>
1. [**^**](#ref-mtld) McCarthy, P. M. (2005). *An assessment of the range and usefulness of lexical diversity measures and the potential of the measure of textual, lexical diversity (MTLD)* (Publication No. 3199485) [Doctoral dissertation, The University of Memphis]. ProQuest Dissertations and Theses Global.
<span id="ref-mccarthy-jarvis-2010"></span>
1. [**^**](#ref-hdd) [**^**](#ref-mtld) McCarthy, P. M., & Jarvis, S. (2010). MTLD, vocd-D, and HD-D: A validation study of sophisticated approaches to lexical diversity assessment. *Behavior Research Methods*, *42*(2), 381–392. https://doi.org/10.3758/BRM.42.2.381
<span id="ref-mclaughlin-1969"></span>
1. [**^**](#ref-smog-grading) McLaughlin, G. H. (1969). SMOG Grading: A new readability formula. *Journal of Reading*, *12*(8), 639–646.
<span id="ref-munoz-baquedano-2006"></span>
1. [**^**](#ref-mu) Muñoz Baquedano, M. (2006). Legibilidad y variabilidad de los textos. *Boletín de Investigación Educacional, Pontificia Universidad Católica de Chile*, *21*(2), 13–26.
<span id="ref-oakes-1998"></span>
1. [**^**](#ref-pearsons-chi-squared-test) Oakes, M. P. (1998). *Statistics for corpus linguistics*. Edinburgh University Press.
<span id="ref-oborneva-2006"></span>
1. [**^**](#ref-re) Oborneva, I. V. (2006). *Автоматизированная оценка сложности учебных текстов на основе статистических параметров* [Doctoral dissertation, Institute for Strategy of Education Development of the Russian Academy of Education]. Freereferats.ru. https://static.freereferats.ru/_avtoreferats/01002881899.pdf?ver=3
<span id="ref-o-hayre-1966"></span>
1. [**^**](#ref-lensear-write-formula) O’Hayre, J. (1966). *Gobbledygook has gotta go*. U.S. Government Printing Office. https://www.governmentattic.org/15docs/Gobbledygook_Has_Gotta_Go_1966.pdf
<span id="ref-paquot-bestgen-2009"></span>
1. [**^**](#ref-students-t-test-2-sample) Paquot, M., & Bestgen, Y. (2009). Distinctive words in academic writing: A comparison of three statistical tests for keyword extraction. *Language and Computers*, *68*, 247–269.
<span id="ref-partiko-2001"></span>
1. [**^**](#ref-re) Partiko, Z. V. (2001). *Zagal’ne redaguvannja. Normativni osnovi.* Afiša.
<span id="ref-pedersen-1996"></span>
1. [**^**](#ref-fishers-exact-test) Pedersen, T. (1996). Fishing for exactness. In T. Winn (Ed.), *Proceedings of the Sixth Annual South-Central Regional SAS Users' Group Conference* (pp. 188–200). The South–Central Regional SAS Users' Group.
<span id="ref-pedersen-bruce-1996"></span>
1. [**^**](#ref-min-sensitivity) Pedersen, T., & Bruce, R. (1996). What to infer from a description. In *Technical report 96-CSE-04*. Southern Methodist University.
<span id="ref-pecina-2005"></span>
1. [**^**](#ref-or) Pecina, P. (2005). An extensive empirical study of collocation extraction methods. In C. Callison-Burch & S. Wan (Eds.), *Proceedings of the Student Research Workshop* (pp. 13–18). Association for Computational Linguistics.
<span id="ref-pisarek-1969"></span>
1. [**^**](#ref-fog-index) Pisarek, W. (1969). Jak mierzyć zrozumiałość tekstu? *Zeszyty Prasoznawcze*, *4*(42), 35–48.
<span id="ref-pojanapunya-todd-2016"></span>
1. [**^**](#ref-or) Pojanapunya, P., & Todd, R. W. (2016). Log-likelihood and odds ratio keyness statistics for different purposes of keyword analysis. *Corpus Linguistics and Linguistic Theory*, *15*(1), 133–167. https://doi.org/10.1515/cllt-2015-0030
<span id="ref-popescu-et-al-2008"></span>
1. [**^**](#ref-popescu-macutek-altmanns-b1-b2-b3-b4-b5) Popescu I.-I., Mačutek, J, & Altmann, G. (2008). Word frequency and arc length. *Glottometrics*, *17*, 18–42.
<span id="ref-popescu-2009"></span>
1. [**^**](#ref-popescus-r1) [**^**](#ref-popescus-r2) [**^**](#ref-popescus-r3) [**^**](#ref-popescus-r4) [**^**](#ref-repeat-rate) [**^**](#ref-shannon-entropy) Popescu, I.-I. (2009). *Word frequency studies*. Mouton de Gruyter.
<span id="ref-powers-et-al-1958"></span>
1. [**^**](#ref-x-c50) [**^**](#ref-re) [**^**](#ref-re-farr-jenkins-paterson) [**^**](#ref-fog-index) Powers, R. D., Sumner, W. A., & Kearl, B. E. (1958). A recalculation of four adult readability formulas. *Journal of Educational Psychology*, *49*(2), 99–105. https://doi.org/10.1037/h0043254
<span id="ref-quasthoff-wolff-2002"></span>
1. [**^**](#ref-poisson-collocation-measure) Quasthoff, U., & Wolff, C. (2002). The poisson collocation measure and its applications. *Proceedings of 2nd International Workshop on Computational Approaches to Collocations*. IEEE.
<span id="ref-rosengren-1971"></span>
1. [**^**](#ref-rosengrens-s) [**^**](#ref-rosengrens-kf) Rosengren, I. (1971). The quantitative concept of language and its relation to the structure of frequency dictionaries. *Études de linguistique appliquée*, *1*, 103–127.
<span id="ref-rychly-2008"></span>
1. [**^**](#ref-log-dice) Rychlý, P. (2008). A lexicographyer-friendly association score. In P. Sojka & A. Horák (Eds.), *Proceedings of Second Workshop on Recent Advances in Slavonic Natural Languages Processing* (pp. 6–9). Masaryk University
<span id="ref-savicky-hlavacova-2002"></span>
1. [**^**](#ref-ald) [**^**](#ref-fald) [**^**](#ref-arf) [**^**](#ref-farf) [**^**](#ref-awt) [**^**](#ref-fawt) Savický, P., & Hlaváčová, J. (2002). Measures of word commonness. *Journal of Quantitative Linguistics*, *9*(3), 215–231. https://doi.org/10.1076/jqul.9.3.215.14124
<span id="ref-simpson-1949"></span>
1. [**^**](#ref-simpsons-l) Simpson, E. H. (1949). Measurement of diversity. *Nature*, *163*, 688. https://doi.org/10.1038/163688a0
<span id="ref-smadja-et-al-1996"></span>
1. [**^**](#ref-dice-sorensen-coeff) Smadja, F., McKeown, K. R., & Hatzivassiloglou, V. (1996). Translating collocations for bilingual lexicons: A statistical approach. *Computational Linguistics*, *22*(1), 1–38.
<span id="ref-smith-1961"></span>
1. [**^**](#ref-devereux-readability-index) Smith, E. A. (1961). Devereaux readability index. *Journal of Educational Research*, *54*(8), 298–303. https://doi.org/10.1080/00220671.1961.10882728
<span id="ref-smith-senter-1967"></span>
1. [**^**](#ref-ari) Smith, E. A., & Senter, R. J. (1967). *Automated readability index*. Aerospace Medical Research Laboratories. https://apps.dtic.mil/sti/pdfs/AD0667273.pdf
<span id="ref-nathaniel-2017"></span>
1. [**^**](#ref-strain-index) Nathaniel, W. S. (2017). *A quantitative analysis of media language* [Master’s thesis, Madurai Kamaraj University]. LAMBERT Academic Publishing.
<span id="ref-somers-1966"></span>
1. [**^**](#ref-logttr) Somers, H. H. (1966). Statistical methods in literary analysis. In J. Leeds (Ed.), *The computer and literary style* (pp. 128–140). Kent State University Press.
<span id="ref-spache-1953"></span>
1. [**^**](#ref-spache-readability-formula) Spache, G. (1953). A new readability formula for primary-grade reading materials. *Elementary School Journal*, *53*(7), 410–413. https://doi.org/10.1086/458513
<span id="ref-spache-1974"></span>
1. [**^**](#ref-num-words-spache) [**^**](#ref-spache-readability-formula) Spache, G. (1974). *Good reading for poor readers* (Rev. 9th ed.). Garrard.
<span id="ref-szigrisze-pazos-1993"></span>
1. [**^**](#ref-re) Szigriszt Pazos, F. (1993). *Sistemas predictivos de legibilidad del mensaje escrito: Formula de perspicuidad* [Doctoral dissertation, Complutense University of Madrid]. Biblos-e Archivo. https://repositorio.uam.es/bitstream/handle/10486/2488/3907_barrio_cantalejo_ines_maria.pdf?sequence=1&isAllowed=y
<span id="ref-trankle-bailer-1984"></span>
1. [**^**](#ref-trankle-bailers-readability-formula) Tränkle, U., & Bailer, H. (1984). Kreuzvalidierung und neuberechnung von lesbarkeitsformeln für die Deutsche sprache. *Zeitschrift für Entwicklungspsychologie und Pädagogische Psychologie*, *16*(3), 231–244.
<span id="ref-tuldava-1975"></span>
1. [**^**](#ref-td) Tuldava, J. (1975). Ob izmerenii trudnosti tekstov. *Uchenye zapiski Tartuskogo universiteta. Trudy po metodike prepodavaniya inostrannykh yazykov*, *345*, 102–120.
<span id="ref-wheeler-smith-1954"></span>
1. [**^**](#ref-wheeler-smiths-readability-formula) Wheeler, L. R., & Smith, E. H. (1954). A practical readability formula for the classroom teacher in the primary grades. *Elementary English*, *31*(7), 397–399.
<span id="ref-williams-1970"></span>
1. [**^**](#ref-yules-index-of-diversity) Williams, C. B. (1970). *Style and vocabulary: Numerical studies*. Griffin.
<span id="ref-wilson-2013"></span>
1. [**^**](#ref-log-likehood-ratio-test) [**^**](#ref-students-t-test-2-sample) Wilson, A. (2013). Embracing Bayes factors for key item analysis in corpus linguistics. In M. Bieswanger & A. Koll-Stobbe (Eds.), *New approaches to the study of linguistic variability* (pp. 3–11). Peter Lang.
<span id="ref-yule-1944"></span>
1. [**^**](#ref-yules-characteristic-k) Yule, G. U. (1944). *The statistical study of literary vocabulary*. Cambridge University Press.
<span id="ref-zhang-2004"></span>
1. [**^**](#ref-zhangs-distributional-consistency) Zhang, H., Huang, C., & Yu, S. (2004). Distributional Consistency: As a general method for defining a core lexicon. In M. T. Lino, M. F. Xavier, F. Ferreira, R. Costa, & R. Silva (Eds.), *Proceedings of Fourth International Conference on Language Resources and Evaluation* (pp. 1119–1122). European Language Resources Association.

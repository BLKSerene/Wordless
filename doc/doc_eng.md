<!--
# Wordless: Documentation - English
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

<div align="center"><h1>📖 Documentation - English</h1></div>

<span id="doc-eng"></span>
## Table of Contents
- 1 [Main Window](#doc-eng-1)
- 2 [File Area](#doc-eng-2)
- 3 [Work Area](#doc-eng-3)
    - 3.1 [Overview](#doc-eng-3-1)
    - 3.2 [Concordancer](#doc-eng-3-2)
    - 3.3 [Wordlist](#doc-eng-3-3)
    - 3.4 [N-gram](#doc-eng-3-4)
    - 3.5 [Collocation](#doc-eng-3-5)
    - 3.6 [Colligation](#doc-eng-3-6)
    - 3.7 [Keyword](#doc-eng-3-7)
- 4 [Appendixes](#doc-eng-4)
    - 4.1 [Supported Languages](#doc-eng-4-1)
    - 4.2 [Supported File Types](#doc-eng-4-2)
    - 4.3 [Supported File Encodings](#doc-eng-4-3)
    - 4.4 [Supported Measures](#doc-eng-4-4)
        - 4.4.1 [Measures of Readability](#doc-eng-4-4-1)
        - 4.4.2 [Measures of Dispersion & Adjusted Frequency](#doc-eng-4-4-2)
        - 4.4.3 [Tests of Statistical Significance & Measures of Effect Size](#doc-eng-4-4-3)
- 5 [References](#doc-eng-5)

<span id="doc-eng-1"></span>
## 1 Main Window [[Back to Contents]](#doc-eng)
The main window of *Wordless* is divided into several sections:

- **1.1 Menu Bar**<br>
    
- **1.2 Work Area**<br>
    The *Work Area* is further divided into the *Resutls Area* on the left side and the *Settings Area* on the right side.<br>
    You can click on the tabs at the top to toggle between different panels.

- **1.3 File Area**<br>
    The *File Area* is further divided into the *File Table* on the left side and the *Settings Area* on the right side.

- **1.4 Status Bar**<br>
    You can show/hide the *Status Bar* by checking/unchecking **Menu → Preferences → Show Status Bar**

<span id="doc-eng-2"></span>
## 2 File Area [[Back to Contents]](#doc-eng)
In most cases, the first thing to do in *Wordless* is open and select your files to be processed via **Menu → File → Open Files/Folder**.

Files are loaded, cached and selected automatically after being added to the *File Table*. **Only selected files will be processed by *Wordless***. You can drag and drop files around the *File Table* to change their orders, which would be reflected in the results.

By default, *Wordless* tries to detect the encoding and language settings of all files for you, you should double check and make sure that the settings of each and every file are correct. If you prefer changing file settings manually, you could uncheck **Auto-detect encodings** and/or **Auto-detect languages** in the *Open Files* dialog. The default file settings could be modified via **Menu → Preferences → Settings → Files → Default Settings**.

- **2.1 Open Files**<br>
    Add one single file or multiple files to the *File Table*.

    \* You can use the **Ctrl** key (**Command** key on macOS) and/or the **Shift** key to select multiple files.

- **2.2 Open Folder**<br>
    Add all files in the folder to the *File Table*.

    By default, all files in the chosen folder and the subfolders of the chosen folder (and subfolders of subfolders, and so on) are added to the *File Table*. If you do not want to add files in subfolders to the *File Table*, you could uncheck **Include files in subfolders** in the *Open Files* dialog.

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

<span id="doc-eng-3"></span>
## 3 Work Area [[Back to Contents]](#doc-eng)

<span id="doc-eng-3-1"></span>
### 3.1 Overview [[Back to Contents]](#doc-eng)
In *Overview*, you can check and compare general linguistic features of different files.

- **3.1.1 Automated Readability Index ~ Write Score**<br>
    Readability statistics of each file calculated according to the different readability tests used. See [Measures of Readability](#doc-eng-4-4-1) for more details.

- **3.1.2 Count of Paragraphs**<br>
    The number of paragraphs in each file. Each line in the file is counted as one paragraph. Blank lines and lines containing only spaces, tabs and other invisible characters are not counted.

- **3.1.3 Count of Paragraphs %**<br>
    The percentage of the number of paragraphs in each file out of the total number of paragraphs in all files.

- **3.1.4 Count of Sentences**<br>
    The number of sentences in each file. *Wordless* automatically applies the built-in sentence tokenizer according to the language of each file to calculate the number of sentences in each file. You can modify sentence tokenizer settings via **Menu → Preferences → Settings → Sentence Tokenization → Sentence Tokenizer Settings**.

- **3.1.5 Count of Sentences %**<br>
    The percentage of the number of sentences in each file out of the total number of sentences in all files.

- **3.1.6 Count of Tokens**<br>
    The number of tokens in each file. *Wordless* automatically applies the built-in word tokenizer according to the language of each file to calculate the number of tokens in each file. You can modify word tokenizer settings via **Menu → Preferences → Settings → Word Tokenization → Word Tokenizer Settings**.

    You can specify what should be counted as a "token" via **Token Settings** in the *Settings Area*

- **3.1.7 Count of Tokens %**<br>
    The percentage of the number of tokens in each file out of the total number of tokens in all files.

- **3.1.8 Count of Types**<br>
    The number of token types in each file.

- **3.1.9 Count of Types %**<br>
    The percentage of the number of token types in each file out of the total number of token types in all files.

- **3.1.10 Count of Syllables**<br>
    The number of syllables in each files. *Wordless* automatically applies the built-in syllable tokenizer according to the language of each file to calculate the number of syllable in each file. You can modify syllable tokenizer settings via **Menu → Preferences → Settings → Syllable Tokenization → Syllable Tokenizer Settings**.

- **3.1.11 Count of Syllables %**<br>
    The percentage of the number of syllables in each file out of the total number of syllable in all files.

- **3.1.12 Count of Characters**<br>
    The number of single characters in each file. Spaces, tabs and all other invisible characters are not counted.

- **3.1.13 Count of Characters %**<br>
    The percentage of the number of characters in each file out of the total number of characters in all files.

- **3.1.14 Type-token Ratio**<br>
    The number of token types divided by the number of tokens in each file.

- **3.1.15 Type-token Ratio (Standardized)**<br>
    Standardized type-token ratio. Each file is divided into several sub-sections with each one consisting of 1000 tokens by default and type-token ratios are calculated for each part. The standardized type-token ratio of each file is then averaged out over all sub-sections. You can change the number of tokens in each sub-section via **Generation Settings → Base of standardized type-token ratio**.

    The last section is discarded if the number of tokens in it is smaller than the base of standardized type-token ratio in order to prevent the result from being affected by outliers (extreme values).

- **3.1.16 Paragraph Length in Sentences (Mean)**<br>
    The average value of paragraph lengths expressed as the number of sentences.

- **3.1.17 Paragraph Length in Sentences (Standard Deviation)**<br>
    The standard deviation of paragraph lengths expressed as the number of sentences.

- **3.1.18 Paragraph Length in Sentences (Variance)**<br>
    The variance of paragraph lengths expressed as the number of sentences.

- **3.1.19 Paragraph Length in Sentences (Minimum)**<br>
    The minimum of paragraph lengths expressed as the number of sentences.

- **3.1.20 Paragraph Length in Sentences (25th Percentile)**<br>
    The 25th percentile of paragraph lengths expressed as the number of sentences.

- **3.1.21 Paragraph Length in Sentences (Median)**<br>
    The median of paragraph lengths expressed as the number of sentences.

- **3.1.22 Paragraph Length in Sentences (75th Percentile)**<br>
    The 75th percentile of paragraph lengths expressed as the number of sentences.

- **3.1.23 Paragraph Length in Sentences (Maximum)**<br>
    The maximum of paragraph lengths expressed as the number of sentences.

- **3.1.24 Paragraph Length in Sentences (Range)**<br>
    The range of paragraph lengths expressed as the number of sentences.

- **3.1.25 Paragraph Length in Sentences (Modes)**<br>
    The mode(s) of paragraph lengths expressed as the number of sentences.

- **3.1.26 Paragraph Length in Tokens (Mean)**<br>
    The average value of paragraph lengths expressed as number of tokens.

- **3.1.27 Paragraph Length in Tokens (Standard Deviation)**<br>
    The standard deviation of paragraph lengths expressed as number of tokens.

- **3.1.28 Paragraph Length in Tokens (Variance)**<br>
    The variance of paragraph lengths expressed as the number of tokens.

- **3.1.29 Paragraph Length in Tokens (Minimum)**<br>
    The minimum of paragraph lengths expressed as the number of tokens.

- **3.1.30 Paragraph Length in Tokens (25th Percentile)**<br>
    The 25th percentile of paragraph lengths expressed as the number of tokens.

- **3.1.31 Paragraph Length in Tokens (Median)**<br>
    The median of paragraph lengths expressed as the number of tokens.

- **3.1.32 Paragraph Length in Tokens (75th Percentile)**<br>
    The 75th percentile of paragraph lengths expressed as the number of tokens.

- **3.1.33 Paragraph Length in Tokens (Maximum)**<br>
    The maximum of paragraph lengths expressed as the number of tokens.

- **3.1.34 Paragraph Length in Tokens (Range)**<br>
    The range of paragraph lengths expressed as the number of tokens.

- **3.1.35 Paragraph Length in Tokens (Modes)**<br>
    The mode(s) of paragraph lengths expressed as the number of tokens.

- **3.1.36 Sentence Length in Tokens (Mean)**<br>
    The average value of sentence lengths expressed as number of tokens.

- **3.1.37 Sentence Length in Tokens (Standard Deviation)**<br>
    The standard deviation of sentence lengths expressed as number of tokens.

- **3.1.38 Sentence Length in Tokens (Variance)**<br>
    The variance of sentence lengths expressed as the number of tokens.

- **3.1.39 Sentence Length in Tokens (Minimum)**<br>
    The minimum of sentence lengths expressed as the number of tokens.

- **3.1.40 Sentence Length in Tokens (25th Percentile)**<br>
    The 25th percentile of sentence lengths expressed as the number of tokens.

- **3.1.41 Sentence Length in Tokens (Median)**<br>
    The median of sentence lengths expressed as the number of tokens.

- **3.1.42 Sentence Length in Tokens (75th Percentile)**<br>
    The 75th percentile of sentence lengths expressed as the number of tokens.

- **3.1.43 Sentence Length in Tokens (Maximum)**<br>
    The maximum of sentence lengths expressed as the number of tokens.

- **3.1.44 Sentence Length in Tokens (Range)**<br>
    The range of sentence lengths expressed as the number of tokens.

- **3.1.45 Sentence Length in Tokens (Modes)**<br>
    The mode(s) of sentence lengths expressed as the number of tokens.

- **3.1.46 Token Length in Syllables (Mean)**<br>
    The average value of token lengths expressed as number of syllables.

- **3.1.47 Token Length in Syllables (Standard Deviation)**<br>
    The standard deviation of token lengths expressed as number of syllables.

- **3.1.48 Token Length in Syllables (Variance)**<br>
    The variance of token lengths expressed as the number of syllables.

- **3.1.49 Token Length in Syllables (Minimum)**<br>
    The minimum of token lengths expressed as the number of syllables.

- **3.1.50 Token Length in Syllables (25th Percentile)**<br>
    The 25th percentile of token lengths expressed as the number of syllables.

- **3.1.51 Token Length in Syllables (Median)**<br>
    The median of token lengths expressed as the number of syllables.

- **3.1.52 Token Length in Syllables (75th Percentile)**<br>
    The 75th percentile of token lengths expressed as the number of syllables.

- **3.1.53 Token Length in Syllables (Maximum)**<br>
    The maximum of token lengths expressed as the number of syllables.

- **3.1.54 Token Length in Syllables (Range)**<br>
    The range of token lengths expressed as the number of syllables.

- **3.1.55 Token Length in Syllables (Modes)**<br>
    The mode(s) of token lengths expressed as the number of syllables.

- **3.1.56 Token Length in Characters (Mean)**<br>
    The average value of token lengths expressed as number of characters.

- **3.1.57 Token Length in Characters (Standard Deviation)**<br>
    The standard deviation of token lengths expressed as number of characters.

- **3.1.58 Token Length in Characters (Variance)**<br>
    The variance of token lengths expressed as the number of characters.

- **3.1.59 Token Length in Characters (Minimum)**<br>
    The minimum of token lengths expressed as the number of characters.

- **3.1.60 Token Length in Characters (25th Percentile)**<br>
    The 25th percentile of token lengths expressed as the number of characters.

- **3.1.61 Token Length in Characters (Median)**<br>
    The median of token lengths expressed as the number of characters.

- **3.1.62 Token Length in Characters (75th Percentile)**<br>
    The 75th percentile of token lengths expressed as the number of characters.

- **3.1.63 Token Length in Characters (Maximum)**<br>
    The maximum of token lengths expressed as the number of characters.

- **3.1.64 Token Length in Characters (Range)**<br>
    The range of token lengths expressed as the number of characters.

- **3.1.65 Token Length in Characters (Modes)**<br>
    The mode(s) of token lengths expressed as the number of characters.

- **3.1.66 Type Length in Syllables (Mean)**<br>
    The average value of token type lengths expressed as number of syllables.

- **3.1.67 Type Length in Syllables (Standard Deviation)**<br>
    The standard deviation of token type lengths expressed as number of syllables.

- **3.1.68 Type Length in Syllables (Variance)**<br>
    The variance of token type lengths expressed as the number of syllables.

- **3.1.69 Type Length in Syllables (Minimum)**<br>
    The minimum of token type lengths expressed as the number of syllables.

- **3.1.70 Type Length in Syllables (25th Percentile)**<br>
    The 25th percentile of token type lengths expressed as the number of syllables.

- **3.1.71 Type Length in Syllables (Median)**<br>
    The median of token type lengths expressed as the number of syllables.

- **3.1.72 Type Length in Syllables (75th Percentile)**<br>
    The 75th percentile of token type lengths expressed as the number of syllables.

- **3.1.73 Type Length in Syllables (Maximum)**<br>
    The maximum of token type lengths expressed as the number of syllables.

- **3.1.74 Type Length in Syllables (Range)**<br>
    The range of token type lengths expressed as the number of syllables.

- **3.1.75 Type Length in Syllables (Modes)**<br>
    The mode(s) of token type lengths expressed as the number of syllables.

- **3.1.76 Type Length in Characters (Mean)**<br>
    The average value of token type lengths expressed as number of characters.

- **3.1.77 Type Length in Characters (Standard Deviation)**<br>
    The standard deviation of token type lengths expressed as number of characters.

- **3.1.78 Type Length in Characters (Variance)**<br>
    The variance of token type lengths expressed as the number of characters.

- **3.1.79 Type Length in Characters (Minimum)**<br>
    The minimum of token type lengths expressed as the number of characters.

- **3.1.80 Type Length in Characters (25th Percentile)**<br>
    The 25th percentile of token type lengths expressed as the number of characters.

- **3.1.81 Type Length in Characters (Median)**<br>
    The median of token type lengths expressed as the number of characters.

- **3.1.82 Type Length in Characters (75th Percentile)**<br>
    The 75th percentile of token type lengths expressed as the number of characters.

- **3.1.83 Type Length in Characters (Maximum)**<br>
    The maximum of token type lengths expressed as the number of characters.

- **3.1.84 Type Length in Characters (Range)**<br>
    The range of token type lengths expressed as the number of characters.

- **3.1.85 Type Length in Characters (Modes)**<br>
    The mode(s) of token type lengths expressed as the number of characters.

- **3.1.86 Syllable Length in Characters (Mean)**<br>
    The average value of syllable lengths expressed as number of characters.

- **3.1.87 Syllable Length in Characters (Standard Deviation)**<br>
    The standard deviation of syllable lengths expressed as number of characters.

- **3.1.88 Syllable Length in Characters (Variance)**<br>
    The variance of syllable lengths expressed as the number of characters.

- **3.1.89 Syllable Length in Characters (Minimum)**<br>
    The minimum of syllable lengths expressed as the number of characters.

- **3.1.90 Syllable Length in Characters (25th Percentile)**<br>
    The 25th percentile of syllable lengths expressed as the number of characters.

- **3.1.91 Syllable Length in Characters (Median)**<br>
    The median of syllable lengths expressed as the number of characters.

- **3.1.92 Syllable Length in Characters (75th Percentile)**<br>
    The 75th percentile of syllable lengths expressed as the number of characters.

- **3.1.93 Syllable Length in Characters (Maximum)**<br>
    The maximum of syllable lengths expressed as the number of characters.

- **3.1.94 Syllable Length in Characters (Range)**<br>
    The range of syllable lengths expressed as the number of characters.

- **3.1.95 Syllable Length in Characters (Modes)**<br>
    The mode(s) of syllable lengths expressed as the number of characters.

- **3.1.96 Count of n-length Sentences**<br>
    The number of n-length sentences, where n = 1, 2, 3, etc.

- **3.1.97 Count of n-length Sentences %**<br>
    The percentage of the number of n-length sentences in each file out of the total number of n-length sentences in all files, where n = 1, 2, 3, etc.

- **3.1.98 Count of n-length Tokens**<br>
    Number of n-length tokens, where n = 1, 2, 3, etc.

- **3.1.99 Count of n-length Tokens %**<br>
    The percentage of the number of n-length tokens in each file out of the total number of n-length tokens in all files, where n = 1, 2, 3, etc.

![Overview - Table](/doc/overview/overview_table.png)

<span id="doc-eng-3-2"></span>
### 3.2 Concordancer [[Back to Contents]](#doc-eng)
In *Concordancer*, you can search for tokens in different files and generate concordance lines. You can adjust the settings for the generated results via **Generation Settings**.

After the concordance lines are generated and displayed in the table, you can sort the results by clicking **Sort Results** or search in results by clicking **Search in Results**, both buttons residing at the right corner of the *Results Area*.

You can generate concordance plots for all search terms. You can modify the settings for the generated figure via **Figure Settings**. By default, data in concordance plot are sorted by file. You can sort the data by search term instead via **Figure Settings → Sort Results by**.

- **3.2.1 Left**<br>
    The context before each search term, which displays 10 tokens left to the **Node** by default. You can change this behavior via **Generation Settings**.

- **3.2.2 Node**<br>
    The search term(s) specified in **Search Settings → Search Term**.

- **3.2.3 Right**<br>
    The context after each search term, which displays 10 tokens right to the **Node** by default. You can change this behavior via **Generation Settings**.

- **3.2.4 Token No.**<br>
    The position of the first token of **Node** in each file.

- **3.2.5 Token No. %**<br>
    The percentage of the position of the first token of **Node** in each file.

- **3.2.6 Sentence No.**<br>
    The position of the sentence in which the **Node** is found in each file.

- **3.2.7 Sentence No. %**<br>
    The percentage of the position of the sentence in which the **Node** is found in each file.

- **3.2.8 Paragraph No.**<br>
    The position of the paragraph in which the **Node** is found in each file.

- **3.2.9 Paragraph No. %**<br>
    The percentage of the position of the paragraph in which the **Node** is found in each file.

- **3.2.10 File**<br>
    The file in which the **Node** is found.

- **3.2.11 Sentiment**<br>
    The sentiment of the **Node** combined with its context (**Left** and **Right**).

![Concordance - Table](/doc/concordancer/concordancer_table.png)
![Concordance - Figure - File](/doc/concordancer/concordancer_fig_file.png)
![Concordance - Figure - Search Term](/doc/concordancer/concordancer_fig_search_term.png)

<span id="doc-eng-3-3"></span>
### 3.3 Wordlist [[Back to Contents]](#doc-eng)
In *Wordlist*, you can generate wordlists for different files and calculate the raw frequency, relative frequency, dispersion and adjusted frequency for each token.

You can further filter the results as you see fit by clicking **Filter Results** or search in the results for the part that might be of interest to you by clicking **Search in Results**, both buttons residing at the right corner of the *Results Area*.

You can generate line charts or word clouds for wordlists using any statistics. You can modify the settings for the generated figure via **Figure Settings**.

- **3.3.1 Rank**<br>
    The rank of the token sorted by its frequency in the first file in descending order (by default). You can sort the results again by clicking the column headers. 

- **3.3.2 Token**<br>
    You can specify what should be counted as a "token" via **Token Settings**.

- **3.3.3 Frequency**<br>
    The number of occurrences of the token in each file.

- **3.3.4 Dispersion**<br>
    The dispersion of the token in each file. You can change the measure of dispersion used via **Generation Settings → Measure of Dispersion**. See [Measures of Dispersion & Adjusted Frequency](#doc-eng-4-4-2) for more details.

- **3.3.5 Adjusted Frequency**<br>
    The adjusted frequency of the token in each file. You can change the measure of adjusted frequency used via **Generation Settings → Measure of Adjusted Frequency**. See [Measures of Dispersion & Adjusted Frequency](#doc-eng-4-4-2) for more details.

- **3.3.6 Number of Files Found**<br>
    The number of files in which the token appears at least once.

- **3.3.7 Number of Files Found %**<br>
    The percentage of the number of files in which the token appears at least once out of the total number of files that are cureently selected.

![Wordlist - Table](/doc/wordlist/wordlist_table.png)
![Wordlist - Figure - Line Chart](/doc/wordlist/wordlist_fig_line_chart.png)
![Wordlist - Figure - Word Cloud](/doc/wordlist/wordlist_fig_word_cloud.png)

<span id="doc-eng-3-4"></span>
### 3.4 N-gram [[Back to Contents]](#doc-eng)
In *N-gram*, you can search for n-grams (consecutive tokens) or skip-grams (non-consecutive tokens) in different files, count and compute the raw frequency and relative frequency of each n-gram/skip-gram, and calculate the dispersion and adjusted frequency for each n-gram/skip-gram using different measures.  You can adjust the settings for the generated results via **Generation Settings**. To allow skip-grams in the results, check **Generation Settings → Allow skipped tokens** and modify the settings. You can also set constraints on the position of search terms in all n-grams via **Search Settings → Search Term Position**.

It is possible to disable searching altogether and generate an exhausted list of n-grams/skip-grams by unchecking **Search Settings** for each file, but it is not recommended to do so, since the processing speed might be too slow.

You can generate line charts or word clouds for n-grams using any statistics. You can modify the settings for the generated figure via **Figure Settings**.

You can further filter the results as you see fit by clicking **Filter Results** or search in the results for the part that might be of interest to you by clicking **Search in Results**, both buttons residing at the right corner of the *Results Area*.

- **3.4.1 Rank**<br>
    The rank of the n-gram sorted by its frequency in the first file in descending order (by default). You can sort the results again by clicking the column headers. 

- **3.4.2 N-gram**<br>
    You can specify what should be counted as a "n-gram" via **Token Settings**.

- **3.4.3 Frequency**<br>
    The number of occurrences of the n-gram in each file.

- **3.4.4 Dispersion**<br>
    The dispersion of the n-gram in each file. You can change the measure of dispersion used via **Generation Settings → Measure of Dispersion**. See [Measures of Dispersion & Adjusted Frequency](#doc-eng-4-4-2) for more details.

- **3.4.5 Adjusted Frequency**<br>
    The adjusted frequency of the n-gram in each file. You can change the measure of adjusted frequency used via **Generation Settings → Measure of Adjusted Frequency**. See [Measures of Dispersion & Adjusted Frequency](#doc-eng-4-4-2) for more details.

- **3.4.6 Number of Files Found**<br>
    The number of files in which the n-gram appears at least once.

- **3.4.7 Number of Files Found %**<br>
    The percentage of the number of files in which the n-gram appears at least once out of the total number of files that are currently selected.

![N-gram - Table](/doc/ngram/ngram_table.png)
![N-gram - Figure - Line Chart](/doc/ngram/ngram_fig_line_chart.png)
![N-gram - Figure - Word Cloud](/doc/ngram/ngram_fig_word_cloud.png)

<span id="doc-eng-3-5"></span>
### 3.5 Collocation [[Back to Contents]](#doc-eng)
In *Collocation*, you can search for patterns of collocation (tokens that co-occur more often than would be expected by chance) within a given collocational window (from 5 words to the left to 5 words to the right by default), conduct different tests of statistical significance on each pair of collocates and calculate the effect size for each pair using different measures. You can adjust the settings for the generated results via **Generation Settings**.

It is possible to disable searching altogether and generate an exhausted list of patterns of collocation by unchecking **Search Settings** for each file, but it is not recommended to do so, since the processing speed might be too slow.

You can generate line charts, word clouds, and network graphs for patterns of collocation using any statistics. You can modify the settings for the generated figure via **Figure Settings**.

You can further filter the results as you see fit by clicking **Filter Results** or search in the results for the part that might be of interest to you by clicking **Search in Results**, both buttons residing at the right corner of the *Results Area*.

- **3.5.1 Rank**<br>
    The rank of the collocating token sorted by the p-value of the significance test conducted on the node and the collocating token in the first file in ascending order (by default). You can sort the results again by clicking the column headers. 

- **3.5.2 Node**<br>
    The search term. You can specify what should be counted as a "token" via **Token Settings**.

- **3.5.3 Collocate**<br>
    The collocating token. You can specify what should be counted as a "token" via **Token Settings**.

- **3.5.4 Ln, ... , L3, L2, L1, R1, R2, R3, ... , Rn**<br>
    The number of co-occurrences of the node and the collocating token with the collocating token at the given position in each file.

- **3.5.5 Frequency**<br>
    The total number of co-occurrences of the node and the collocating token with the collocating token at all possible positions in each file.

- **3.5.6 Test Statistic**<br>
    The test statistic of the significance test conducted on the node and the collocating token in each file. You can change the test of statistical significance used via **Generation Settings → Test of Statistical Significance**. See [Tests of Statistical Significance & Measures of Effect Size](#doc-eng-4-4-3) for more details.

    Please note that test statistic is not avilable for some tests of statistical significance.

- **3.5.7 p-value**<br>
    The p-value of the significance test conducted on the node and the collocating token in each file. You can change the test of statistical significance used via **Generation Settings → Test of Statistical Significance**. See [Tests of Statistical Significance & Measures of Effect Size](#doc-eng-4-4-3) for more details.

- **3.5.8 Bayes Factor**<br>
    The bayes factor of the significance test conducted on the node and the collocating token in each file. You can change the test of statistical significance used via **Generation Settings → Test of Statistical Significance**. See [Tests of Statistical Significance & Measures of Effect Size](#doc-eng-4-4-3) for more details.

    Please note that bayes factor is not avilable for some tests of statistical significance.

- **3.5.9 Effect Size**<br>
    The effect size of the node and the collocating token in each file. You can change the measure of effect size used via **Generation Settings → Measure of Effect Size**. See [Tests of Statistical Significance & Measures of Effect Size](#doc-eng-4-4-3) for more details.

- **3.5.10 Number of Files Found**<br>
    The number of files in which the node and the collocating token co-occur at least once.

- **3.5.11 Number of Files Found %**<br>
    The percentage of the number of files in which the node and the collocating token co-occur at least once out of the total number of files that are currently selected.

![Collocation - Table](/doc/collocation/collocation_table.png)
![Collocation - Figure - Line Chart](/doc/collocation/collocation_fig_line_chart.png)
![Collocation - Figure - Word Cloud](/doc/collocation/collocation_fig_word_cloud.png)
![Collocation - Figure - Network Graph](/doc/collocation/collocation_fig_network_graph.png)

<span id="doc-eng-3-6"></span>
### 3.6 Colligation [[Back to Contents]](#doc-eng)
In *Colligation*, you can search for patterns of colligation (parts of speech that co-occur more often than would be expected by chance) within a given collocational window (from 5 words to the left to 5 words to the right by default), conduct different tests of statistical significance on each pair of parts of speech and calculate the effect size for each pair using different measures. You can adjust the settings for the generated data via **Generation Settings**.

*Wordless* will automatically apply its built-in POS tagger on every file that are not POS-tagged already according to the language of each file. If POS-tagging is not supported for the given languages, the user should provide a file that has already been POS-tagged and make sure that the correct **Text Type** has been set on each file.

It is possible to disable searching altogether and generate an exhausted list of patterns of colligation by unchecking **Search Settings** for each file, but it is not recommended to do so, since the processing speed might be to slow.

You can generate line charts or word clouds for patterns of colligation using any statistics. You can modify the settings for the generated figure via **Figure Settings**.

You can further filter the results as you see fit by clicking **Filter Results** or search in the results for the part that might be of interest to you by clicking **Search in Results**, both buttons residing at the right corner of the *Results Area*.

- **3.6.1 Rank**<br>
    The rank of the collocating part of speech sorted by the p-value of the significance test conducted on the node and the collocating part of speech in the first file in ascending order (by default). You can sort the results again by clicking the column headers. 

- **3.6.2 Node**<br>
    The search term. You can specify what should be counted as a "token" via **Token Settings**.

- **3.6.3 Collocate**<br>
    The collocating part of speech. You can specify what should be counted as a "token" via **Token Settings**.

- **3.6.4 Ln, ... , L3, L2, L1, R1, R2, R3, ... , Rn**<br>
    The number of co-occurrences of the node and the collocating part of speech with the collocating part of speech at the given position in each file.

- **3.6.5 Frequency**<br>
    The total number of co-occurrences of the node and the collocating part of speech with the collocating part of speech at all possible positions in each file.

- **3.6.6 Test Statistic**<br>
    The test statistic of the significance test conducted on the node and the collocating part of speech in each file. You can change the test of statistical significance used via **Generation Settings → Test of Statistical Significance**. See [Tests of Statistical Significance & Measures of Effect Size](#doc-eng-4-4-3) for more details.

    Please note that test statistic is not avilable for some tests of statistical significance.

- **3.6.7 p-value**<br>
    The p-value of the significance test conducted on the node and the collocating part of speech in each file. You can change the test of statistical significance used via **Generation Settings → Test of Statistical Significance**. See [Tests of Statistical Significance & Measures of Effect Size](#doc-eng-4-4-3) for more details.

- **3.6.8 Bayes Factor**<br>
    The bayes factor of the significance test conducted on the node and the collocating part of speech in each file. You can change the test of statistical significance used via **Generation Settings → Test of Statistical Significance**. See [Tests of Statistical Significance & Measures of Effect Size](#doc-eng-4-4-3) for more details.

    Please note that bayes factor is not avilable for some tests of statistical significance.

- **3.6.9 Effect Size**<br>
    The effect size of the node and the collocating part of speech in each file. You can change the measure of effect size used via **Generation Settings → Measure of Effect Size**. See [Tests of Statistical Significance & Measures of Effect Size](#doc-eng-4-4-3) for more details.

- **3.6.10 Number of Files Found**<br>
    The number of files in which the node and the collocating part of speech co-occur at least once.

- **3.6.11 Number of Files Found %**<br>
    The percentage of the number of files in which the node and the collocating part of speech co-occur at least once out of the total number of file that are currently selected.

![Colligation - Table](/doc/colligation/colligation_table.png)
![Colligation - Figure - Line Chart](/doc/colligation/colligation_fig_line_chart.png)
![Colligation - Figure - Word Cloud](/doc/colligation/colligation_fig_word_cloud.png)
![Colligation - Figure - Network Graph](/doc/colligation/colligation_fig_network_graph.png)

<span id="doc-eng-3-7"></span>
### 3.7 Keyword [[Back to Contents]](#doc-eng)
In *Keyword*, you can search for candidates of potential keywords (tokens that have far more or far less frequency in the observed file than in the reference file) in different files given a reference corpus, conduct different tests of statistical significance on each keyword and calculate the effect size for each keyword using different measures. You can adjust the settings for the generated data via **Generation Settings**.

You can generate line charts or word clouds for keywords using any statistics. You can modify the settings for the generated figure via **Figure Settings**.

You can further filter the results as you see fit by clicking **Filter Results** or search in the results for the part that might be of interest to you by clicking **Search in Results**, both buttons residing at the right corner of the *Results Area*.

- **3.7.1 Rank**<br>
    The rank of the keyword sorted by the p-value of the significance test conducted on the keyword in the first file in ascending order (by default). You can sort the results again by clicking the column headers. 

- **3.7.2 Keyword**<br>
    The candidates of potantial keywords. You can specify what should be counted as a "token" via **Token Settings**.

- **3.7.3 Frequency (in Reference File)**<br>
    The number of co-occurrences of the keywords in the reference file.

- **3.7.4 Frequency (in Observed Files)**<br>
    The number of co-occurrences of the keywords in each observed file.

- **3.7.5 Test Statistic**<br>
    The test statistic of the significance test conducted on the keyword in each file. You can change the test of statistical significance used via **Generation Settings → Test of Statistical Significance**. See [Tests of Statistical Significance & Measures of Effect Size](#doc-eng-4-4-3) for more details.

- **3.7.6 p-value**<br>
    The p-value of the significance test conducted on the keyword in each file. You can change the test of statistical significance used via **Generation Settings → Test of Statistical Significance**. See [Tests of Statistical Significance & Measures of Effect Size](#doc-eng-4-4-3) for more details.

- **3.7.7 Bayes Factor**<br>
    The bayes factor of the significance test conducted on the keyword in each file. You can change the test of statistical significance used via **Generation Settings → Test of Statistical Significance**. See [Tests of Statistical Significance & Measures of Effect Size](#doc-eng-4-4-3) for more details.

    Please note that bayes factor is not avilable for some tests of statistical significance.

- **3.7.8 Effect Size**<br>
    The effect size of on the keyword in each file. You can change the measure of effect size used via **Generation Settings → Measure of Effect Size**. See [Tests of Statistical Significance & Measures of Effect Size](#doc-eng-4-4-3) for more details.

- **3.7.9 Number of Files Found**<br>
    The number of files in which the keyword appears at least once.

- **3.7.10 Number of Files Found %**<br>
    The percentage of the number of files in which the keyword appears at least once out of the total number of files that are currently selected.

![Keyword - Table](/doc/keyword/keyword_table.png)
![Keyword - Figure - Line Chart](/doc/keyword/keyword_fig_line_chart.png)
![Keyword - Figure - Word Cloud](/doc/keyword/keyword_fig_word_cloud.png)

<span id="doc-eng-4"></span>
## 4 Appendixes [[Back to Contents]](#doc-eng)

<span id="doc-eng-4-1"></span>
### 4.1 Supported Languages [[Back to Contents]](#doc-eng)

Language|Sentence Tokenization|Word Tokenization|Syllable Tokenization|POS Tagging|Lemmatization|Stop Words
:------:|:-------------------:|:---------------:|:-------------------:|:---------:|:-----------:|:--------:
Afrikaans               |✔|✔|✔|✖️|✖️|✔
Akkadian                |⭕️ |⭕️ |✖️|✖️|✖️|✔
Albanian                |✔|✔|✔|✖️|✖️|✔
Amharic                 |✔|✔|✖️|✖️|✖️|✔
Arabic                  |✔|✔|✖️|✖️|✖️|✔
Arabic (Standard)       |⭕️ |⭕️ |✖️|✖️|✖️|✔
Armenian                |✔|✔|✖️|✖️|✖️|✔
Assamese                |⭕️ |✔|✖️|✖️|✖️|✖️
Asturian                |⭕️ |⭕️ |✖️|✖️|✔|✖️
Azerbaijani             |✔|✔|✖️|✖️|✖️|✔
Basque                  |✔|✔|✖️|✖️|✖️|✔
Belarusian              |⭕️ |⭕️ |✔|✖️|✖️|✔
Bengali                 |✔|✔|✖️|✖️|✔|✔
Breton                  |⭕️ |⭕️ |✖️|✖️|✖️|✔
Bulgarian               |✔|✔|✔|✖️|✔|✔
Catalan                 |✔|✔|✖️|✔|✔|✔
Chinese (Simplified)    |✔|✔|✖️|✔|✖️|✔
Chinese (Traditional)   |✔|✔|✖️|✔|✖️|✔
Coptic                  |⭕️ |⭕️ |✖️|✖️|✖️|✔
Croatian                |✔|✔|✔|✖️|✔|✔
Czech                   |✔|✔|✔|✖️|✔|✔
Danish                  |✔|✔|✔|✔|✔|✔
Dutch                   |✔|✔|✔|✔|✔|✔
English (Middle)        |⭕️ |⭕️ |✖️|✖️|✖️|✔
English (Old)           |⭕️ |⭕️ |✖️|✖️|✖️|✔
English (United Kingdom)|✔|✔|✔|✔|✔|✔
English (United States) |✔|✔|✔|✔|✔|✔
Esperanto               |⭕️ |⭕️ |✔|✖️|✖️|✔
Estonian                |✔|✔|✔|✖️|✔|✔
Finnish                 |✔|✔|✖️|✖️|✖️|✔
French                  |✔|✔|✔|✔|✔|✔
French (Old)            |⭕️ |⭕️ |✖️|✖️|✖️|✔
Galician                |⭕️ |⭕️ |✔|✖️|✔|✔
German (Austria)        |✔|✔|✔|✔|✔|✔
German (Germany)        |✔|✔|✔|✔|✔|✔
German (Middle High)    |⭕️ |⭕️ |✖️|✖️|✖️|✔
German (Switzerland)    |✔|✔|✔|✔|✔|✔
Greek (Ancient)         |✔|✔|✖️|✖️|✔|✔
Greek (Modern)          |✔|✔|✔|✔|✔|✔
Gujarati                |✔|✔|✖️|✖️|✖️|✔
Hausa                   |⭕️ |⭕️ |✖️|✖️|✖️|✔
Hebrew                  |✔|✔|✖️|✖️|✖️|✔
Hindi                   |✔|✔|✖️|✖️|✖️|✔
Hungarian               |✔|✔|✔|✖️|✔|✔
Icelandic               |✔|✔|✔|✖️|✖️|✔
Indonesian              |✔|✔|✔|✖️|✔|✔
Irish                   |✔|✔|✖️|✖️|✔|✔
Italian                 |✔|✔|✔|✔|✔|✔
Japanese                |✔|✔|✖️|✔|✔|✔
Kannada                 |✔|✔|✖️|✖️|✖️|✔
Kazakh                  |⭕️ |⭕️ |✖️|✖️|✖️|✔
Korean                  |⭕️ |⭕️ |✖️|✖️|✖️|✔
Kurdish                 |⭕️ |⭕️ |✖️|✖️|✖️|✔
Kyrgyz                  |✔|✔|✖️|✖️|✖️|✔
Latin                   |⭕️ |⭕️ |✖️|✖️|✖️|✔
Latvian                 |✔|✔|✔|✖️|✖️|✔
Ligurian                |✔|✔|✖️|✖️|✖️|✔
Lithuanian              |✔|✔|✔|✔|✔|✔
Luxembourgish           |✔|✔|✖️|✖️|✔|✔
Macedonian              |✔|✔|✖️|✔|✔|✔
Malay                   |⭕️ |⭕️ |✖️|✖️|✖️|✔
Malayalam               |✔|✔|✖️|✖️|✖️|✔
Manx                    |⭕️ |⭕️ |✖️|✖️|✔|✖️
Marathi                 |✔|✔|✖️|✖️|✖️|✔
Marathi (Old)           |⭕️ |⭕️ |✖️|✖️|✖️|✔
Meitei                  |⭕️ |✔|✖️|✖️|✖️|✖️
Mongolian               |⭕️ |⭕️ |✔|✖️|✖️|✔
Nepali                  |✔|✔|✖️|✖️|✖️|✔
Norse (Old)             |⭕️ |⭕️ |✖️|✖️|✖️|✔
Norwegian Bokmål        |✔|✔|✔|✔|✔|✔
Norwegian Nynorsk       |✔|⭕️ |✔|✖️|✖️|✔
Oriya                   |⭕️ |✔|✖️|✖️|✖️|✖️
Persian                 |✔|✔|✖️|✖️|✔|✔
Polish                  |✔|✔|✔|✔|✔|✔
Portuguese (Brazil)     |✔|✔|✔|✔|✔|✔
Portuguese (Portugal)   |✔|✔|✔|✔|✔|✔
Punjabi                 |⭕️ |✔|✖️|✖️|✖️|✔
Romanian                |✔|✔|✔|✔|✔|✔
Russian                 |✔|✔|✔|✔|✔|✔
Sanskrit                |✔|✔|✖️|✖️|✖️|✔
Scottish Gaelic         |⭕️ |⭕️ |✖️|✖️|✔|✖️
Serbian (Cyrillic)      |✔|✔|✔|✖️|✔|✔
Serbian (Latin)         |✔|✔|✔|✖️|✖️|✔
Sinhala                 |✔|✔|✖️|✖️|✖️|✔
Slovak                  |✔|✔|✔|✖️|✔|✔
Slovenian               |✔|✔|✔|✖️|✔|✔
Somali                  |⭕️ |⭕️ |✖️|✖️|✖️|✔
Sotho (Southern)        |⭕️ |⭕️ |✖️|✖️|✖️|✔
Spanish                 |✔|✔|✔|✔|✔|✔
Swahili                 |⭕️ |⭕️ |✖️|✖️|✖️|✔
Swedish                 |✔|✔|✔|✖️|✔|✔
Tagalog                 |✔|✔|✖️|✖️|✔|✔
Tajik                   |⭕️ |✔|✖️|✖️|✖️|✔
Tamil                   |✔|✔|✖️|✖️|✖️|✔
Tatar                   |✔|✔|✖️|✖️|✖️|✔
Telugu                  |✔|✔|✔|✖️|✖️|✔
Tetun Dili              |⭕️ |✔|✖️|✖️|✖️|✖️
Thai                    |✔|✔|✔|✔|✖️|✔
Tibetan                 |✔|✔|✖️|✔|✔|✖️
Tigrinya                |✔|✔|✖️|✖️|✖️|✔
Tswana                  |✔|✔|✖️|✖️|✖️|✔
Turkish                 |✔|✔|✖️|✖️|✔|✔
Ukrainian               |✔|✔|✔|✔|✔|✔
Urdu                    |✔|✔|✖️|✖️|✔|✔
Vietnamese              |✔|✔|✖️|✔|✖️|✔
Welsh                   |⭕️ |⭕️ |✖️|✖️|✔|✖️
Yoruba                  |✔|✔|✖️|✖️|✖️|✔
Zulu                    |⭕️ |⭕️ |✔|✖️|✖️|✔
Other Languages         |⭕️ |⭕️ |✖️|✖️|✖️|✖️

✔: Supported<br>
⭕️: Supported but falls back to the default English tokenizer<br>
✖️: Not supported

<span id="doc-eng-4-2"></span>
### 4.2 Supported File Types [[Back to Contents]](#doc-eng)

File Type               |File Extension(s)
------------------------|-----------------
CSV File                |\*.csv
HTML Page               |\*.htm, \*.html
Microsoft Word Document |\*.docx
Microsoft Excel Workbook|\*.xlsx
Text File               |\*.txt
Translation Memory File |\*.tmx
XML File                |\*.xml

\* Microsoft 97-03 Word documents (\*.doc) and Microsoft 97-03 Excel Workbooks (\*.xls) are not supported.<br>
\* Non-text files will be converted to text files first before being added to the *File Table*. You can check the converted files under folder **Import** at the installation location of *Wordless* on your computer (as for macOS users, right click **Wordless.app**, select **Show Package Contents** and navigate to **Contents/MacOS/Import/**). You can change this location via **Menu → Preferences → Settings → Import → Temporary Files → Default Path**.

<span id="doc-eng-4-3"></span>
### 4.3 Supported File Encodings [[Back to Contents]](#doc-eng)

Language|File Encoding|Auto-detection
--------|-------------|:------------:
All Languages           |UTF-8 without BOM      |✔
All Languages           |UTF-8 with BOM         |✔
All Languages           |UTF-16 with BOM        |✔
All Languages           |UTF-16BE without BOM   |✔
All Languages           |UTF-16LE without BOM   |✔
All Languages           |UTF-32 with BOM        |✔
All Languages           |UTF-32BE without BOM   |✔
All Languages           |UTF-32LE without BOM   |✔
All Languages           |UTF-7                  |✔
Arabic                  |CP720                  |✔
Arabic                  |CP864                  |✔
Arabic                  |ISO-8859-6             |✔
Arabic                  |Mac OS                 |✔
Arabic                  |Windows-1256           |✔
Baltic Languages        |CP775                  |✔
Baltic Languages        |ISO-8859-13            |✔
Baltic Languages        |Windows-1257           |✔
Celtic Languages        |ISO-8859-14            |✔
Chinese                 |GB18030                |✔
Chinese                 |GBK                    |✔
Chinese (Simplified)    |GB2312                 |✔
Chinese (Simplified)    |HZ                     |✔
Chinese (Traditional)   |Big-5                  |✔
Chinese (Traditional)   |Big5-HKSCS             |✔
Chinese (Traditional)   |CP950                  |✔
Croatian                |Mac OS                 |✔
Cyrillic                |CP855                  |✔
Cyrillic                |CP866                  |✔
Cyrillic                |ISO-8859-5             |✔
Cyrillic                |Mac OS                 |✔
Cyrillic                |Windows-1251           |✔
English                 |ASCII                  |✔
English                 |EBCDIC 037             |✔
English                 |CP437                  |✔
European                |HP Roman-8             |✔
European (Central)      |CP852                  |✔
European (Central)      |ISO-8859-2             |✔
European (Central)      |Mac OS Central European|✔
European (Central)      |Windows-1250           |✔
European (Northern)     |ISO-8859-4             |✔
European (Southern)     |ISO-8859-3             |✔
European (South-Eastern)|ISO-8859-16            |✔
European (Western)      |EBCDIC 500             |✔
European (Western)      |CP850                  |✔
European (Western)      |CP858                  |✔
European (Western)      |CP1140                 |✔
European (Western)      |ISO-8859-1             |✔
European (Western)      |ISO-8859-15            |✔
European (Western)      |Mac OS Roman           |✔
European (Western)      |Windows-1252           |✔
French                  |CP863                  |✔
German                  |EBCDIC 273             |✔
Greek                   |CP737                  |✔
Greek                   |CP869                  |✔
Greek                   |CP875                  |✔
Greek                   |ISO-8859-7             |✔
Greek                   |Mac OS                 |✔
Greek                   |Windows-1253           |✔
Hebrew                  |CP856                  |✔
Hebrew                  |CP862                  |✔
Hebrew                  |EBCDIC 424             |✔
Hebrew                  |ISO-8859-8             |✔
Hebrew                  |Windows-1255           |✔
Icelandic               |CP861                  |✔
Icelandic               |Mac OS                 |✔
Japanese                |CP932                  |✔
Japanese                |EUC-JP                 |✔
Japanese                |EUC-JIS-2004           |✔
Japanese                |EUC-JISx0213           |✔
Japanese                |ISO-2022-JP            |✔
Japanese                |ISO-2022-JP-1          |✔
Japanese                |ISO-2022-JP-2          |✔
Japanese                |ISO-2022-JP-2004       |✔
Japanese                |ISO-2022-JP-3          |✔
Japanese                |ISO-2022-JP-EXT        |✔
Japanese                |Shift_JIS              |✔
Japanese                |Shift_JIS-2004         |✔
Japanese                |Shift_JISx0213         |✔
Kazakh                  |KZ-1048                |✔
Kazakh                  |PTCP154                |✔
Korean                  |EUC-KR                 |✔
Korean                  |ISO-2022-KR            |✔
Korean                  |JOHAB                  |✔
Korean                  |UHC                    |✔
Nordic Languages        |CP865                  |✔
Nordic Languages        |ISO-8859-10            |✔
Persian/Urdu            |Mac OS Farsi           |✔
Portuguese              |CP860                  |✔
Romanian                |Mac OS                 |✔
Russian                 |KOI8-R                 |✔
Tajik                   |KOI8-T                 |✔
Thai                    |CP874                  |✔
Thai                    |ISO-8859-11            |✔
Turkish                 |CP857                  |✔
Turkish                 |EBCDIC 1026            |✔
Turkish                 |ISO-8859-9             |✔
Turkish                 |Mac OS                 |✔
Turkish                 |Windows-1254           |✔
Ukrainian               |CP1125                 |✔
Ukrainian               |KOI8-U                 |✔
Urdu                    |CP1006                 |✔
Vietnamese              |CP1258                 |✔

<span id="doc-eng-4-4"></span>
### 4.4 Supported Measures [[Back to Contents]](#doc-eng)

<span id="doc-eng-4-4-1"></span>
#### 4.4.1 Measures of Readability [[Back to Contents]](#doc-eng)

The readability of a text depends on several variables including the average sentence length, average word length in characters, average word length in syllables, number of monosyllabic words, number of polysyllabic words, number of difficult words, etc.

It should be noted that **some readability tests can only be applied to English texts, or to texts in languages for which Wordless have built-in syllable tokenization support** (check [4.4.1](#doc-eng-4-1) for reference), while others can be applied to files of all languages.

These variables are used in the following formulas:<br>
**NumSentences**: the number of sentences in the text or sample<br>
**NumWords**: the number of words in the text or sample<br>
**NumSyls**: the number of syllable in the text or sample<br>
**NumCharsAll**: the number of characters (including letters, CJK characters, etc., numerals, and punctuations) in the text or sample<br>
**NumCharsAlphanumeric**: the number of alphanumeric chracters (letters, CJK characters, etc., numerals) in the text or sample<br>
**NumCharsAlphabetic**: the number of alphabetic characters (letters, CJK characters, etc.) in the text or sample

<!--
Automated Readability Index:
    \begin{align*}
        ARI = 0.5 \times \left(\frac{NumWords}{NumSentences}\right) + 4.71 \times \left(\frac{NumCharsAll}{NumWords}\right) - 21.43
    \end{align*}

Coleman-Liau Index:
    \begin{align*}
        Estimated \ Cloze \ % &= 141.8401 - 0.21459 \times \left(\frac{NumCharsAlphabetic}{NumWords} \times 100\right) + 1.079812 \times \left(\frac{NumSentences}{NumWords} \times 100\right) \\
        Grade \ Level &= -27.4004 \times \left(\frac{Estimated \ Cloze \ %}{100}\right) + 23.06395
    \end{align*}

Dale-Chall Readability Score:
    \begin{align*}
        X_{c50} = 0.1579 \times \left(\frac{NumDifficultWords}{NumWords}\right) + 0.0496 \times \left(\frac{NumWords}{NumSentences}\right) + 3.6365
    \end{align*}

Devereux Readability Index:
    \begin{align*}
        Grade \ Placement = 1.56 \times \left(\frac{NumCharsAll}{NumWords}\right) + 0.19 \times \left(\frac{NumWords}{NumSentences}\right) - 6.49
    \end{align*}

Flesch Reading Ease:
    \begin{align*}
        RE = 206.835 - 0.846 \times \left(\frac{NumSyls}{NumWords} \times 100\right) - 1.015 \times \left(\frac{NumWords}{NumSentences}\right)
    \end{align*}

Flesch Reading Ease (Simplified):
    \begin{align*}
        RE = 1.599 \times \left(\frac{NumWords1Syl}{NumWords} \times 100\right) - 1.015 \times \left(\frac{NumWords}{NumSentences}\right) - 31.517
    \end{align*}

Flesch-Kincaid Grade Level:
    \begin{align*}
        GL = 0.39 \times \left(\frac{NumWords}{NumSentences}\right) + 11.8 \times \left(\frac{NumSyls}{NumWords}\right) - 15.59
    \end{align*}

FORCAST Grade Level:
    \begin{align*}
        RGL = 20.43 - 0.11 \times NumWords1Syl
    \end{align*}

Gunning Fog Index:
    \begin{align*}
        Fog \ Index = 0.4 \times \left(\frac{NumWords}{NumSentences} + \frac{NumHardWords}{NumWords} \times 100\right)
    \end{align*}

SMOG Grade:
    \begin{align*}
        g = 3.1291 + 1.043 \times (\sqrt{NumWordsPolysyllabic})
    \end{align*}

Spache Grade Level:
    \begin{align*}
        Grade \ Level = 0.141 \times \left(\frac{100}{NumSentences}\right) + 0.086 \times \left(\frac{NumDifficultWords}{100} \times 100\right) + 0.839
    \end{align*}

Write Score:
    \begin{align*}
        Score = NumWords1Syl + 3 \times NumSentences
    \end{align*}
-->

Measure of Readability|Formula
----------------------|-------
Automated Readability Index      [[1]](#doc-eng-5-1)  |![Formula](/doc/measures/readability/ari.png)
Coleman-Liau Index               [[2]](#doc-eng-5-2)  |![Formula](/doc/measures/readability/coleman_liau_index.png)
Dale-Chall Readibility Score     [[3]](#doc-eng-5-3)[[4]](#doc-eng-5-4)|![Formula](/doc/measures/readability/dale_chall_readability_score.png)<br>where **NumDifficultWords** is the number of words outside the Dale list of 3000 easy words [[4]](#doc-eng-5-4)<br><br>* This test applies only to **English texts**.
Devereux Readability Index       [[5]](#doc-eng-5-5)  |![Formula](/doc/measures/readability/devereux_readability_index.png)
Flesch Reading Ease              [[6]](#doc-eng-5-6)  |![Formula](/doc/measures/readability/re.png)<br>* This test requires **built-in syllable tokenization support**.
Flesch Reading Ease (Simplified) [[7]](#doc-eng-5-7)  |![Formula](/doc/measures/readability/re_simplified.png)<br>where NumWords1Syl is the number of monosyllabic words<br><br>* This test requires **built-in syllable tokenization support**.
Flesch-Kincaid Grade Level       [[8]](#doc-eng-5-8)  |![Formula](/doc/measures/readability/flesch_kincaid_grade_level.png)<br>* This test requires **built-in syllable tokenization support**.
FORCAST Grade Level              [[9]](#doc-eng-5-9)  |![Formula](/doc/measures/readability/rgl.png)<br>where **NumWords1Syl** is the number of monosyllabic words<br><br>* This test requires **built-in syllable tokenization support**.<br>* **A sample of 150 words** is taken randomly from the text, thus the text must be at least 150 words long.
Gunning Fog Index                [[10]](#doc-eng-5-10)|![Formula](/doc/measures/readability/fog_index.png)<br>where **NumHardWords** is the number of words with 3 or more syllables excluding all proper nouns and words with 3 syllables which end with *-ed* or *-es*<br><br>* This test applies only to **English texts**.
SMOG Grade                       [[11]](#doc-eng-5-11)|![Formula](/doc/measures/readability/smog_grade.png)<br>where **NumWordsPolysyllabic** is the number of words with 3 or more syllables<br><br>* **A sample consisting of the first 10 sentences of the text, the last 10 sentences of the text, and 10 sentences at the middle of the text** is taken from the text, thus the text must be at least 30 sentences long.
Spache Grade Level               [[12]](#doc-eng-5-12)[[13]](#doc-eng-5-13)|![Formula](/doc/measures/readability/spache_grade_level.png)<br>where **NumDifficultWords** is the number of words outside the Dale list of 769 easy words [[13]](#doc-eng-5-13)<br><br>* This test requires **built-in syllable tokenization support**.<br>* **Three samples each of 100 words** are taken randomly from the text and the mean of the three scores is calculated, thus the text must be at least 100 words long.
Write Score                      [[14]](#doc-eng-5-14)|![Formula](/doc/measures/readability/write_score.png)<br>where **NumWords1Syl** is the number of monosyllabic words excluding *the*, *is*, *are*, *was*, *were*<br><br>* This test applies only to **English texts**.<br>* **A sample of 100 words** is taken randomly from the text, thus the text must be at least 100 words long.

<span id="doc-eng-4-4-2"></span>
#### 4.4.2 Measures of Dispersion & Adjusted Frequency [[Back to Contents]](#doc-eng)

The dispersion and adjusted frequency of a word in each file is calculated by first dividing each file into **n** (5 by default) sub-sections and the frequency of the word in each part is counted, which are denoted by **F₁**, **F₂**, **F₃** ... **Fn**. The total frequency of the word in each file is denoted by **F**. The mean value of the frequencies over all sub-sections is denoted by ![f-bar](/doc/measures/f_bar.png).

Then, the dispersion and adjusted frequency of the word will be calcuated as follows:

<!--
Carroll's D₂:
    \begin{align*}
        H &= \ln F - \frac{\sum_{i = 1}^n \times \ln F_{i}}{F} \\
        D_2 &= \frac{H}{\ln n}
    \end{align*}

Gries's DP:
    \begin{align*}
        DP = \frac{1}{2} \times \sum_{i = 1}^n \left|\frac{F_{i}}{F} - \frac{1}{n}\right|
    \end{align*}

Gries's DPnorm:
    \begin{align*}
        DP &= \frac{1}{2} \times \sum_{i = 1}^n \left|\frac{F_{i}}{F} - \frac{1}{n}\right| \\
        DP_{norm} &= \frac{DP}{1 - \frac{1}{n}}
    \end{align*}

Juilland's D:
    \begin{align*}
        \sigma &= \sqrt{\frac{\sum_{i = 1}^n \left(F_i - \overline{F}\right)^2}{n}} \\
        CV &= \frac{\sigma}{\overline{F}} \\
        D &= \frac{1 - CV}{\sqrt{n - 1}}
    \end{align*}

Lyne's D₃:
    \begin{align*}
        \chi^2 &= \sum_{i = 1}^n \frac{\left(F_i - \frac{F}{i}\right)^2}{\frac{F}{i}} \\
        D_3 &= \frac{1 - \chi^2}{4 \times F}
    \end{align*}

Rosengren's S:
    \begin{align*}
        KF &= \frac{1}{n} \times \left(\sum_{i = 1}^n \sqrt{F_{i}}\right)^2 \\
        S &= \frac{KF}{F}
    \end{align*}

Zhang's Distributional Consistency:
    \begin{align*}
        DC = \frac{\left(\frac{\sum_{i = 1}^n \sqrt{F_i}}{n}\right)^2}{\frac{\sum_{i = 1}^n}{n}}
    \end{align*}
-->

Measure of Dispersion|Formula
---------------------|-------
Carroll's D₂                       [[15]](#doc-eng-5-15)|![Formula](/doc/measures/dispersion/carrolls_d2.png)
Gries's DP                         [[16]](#doc-eng-5-16)|![Formula](/doc/measures/dispersion/griess_dp.png)
Gries's DPnorm                     [[17]](#doc-eng-5-17)|![Formula](/doc/measures/dispersion/griess_dp_norm.png)
Juilland's D                       [[18]](#doc-eng-5-18)|![Formula](/doc/measures/dispersion/juillands_d.png)
Lyne's D₃                          [[19]](#doc-eng-5-19)|![Formula](/doc/measures/dispersion/lynes_d3.png)
Rosengren's S                      [[20]](#doc-eng-5-20)|![Formula](/doc/measures/dispersion/rosengrens_s.png)
Zhang's Distributional Consistency [[21]](#doc-eng-5-21)|![Formula](/doc/measures/dispersion/zhangs_distributional_consistency.png)

<!--
Carroll's Um:
    \begin{align*}
        H &= \ln F - \frac{\sum_{i = 1}^n \times \ln F_{i}}{F} \\
        D_2 &= \frac{H}{\ln n} \\
        U_m & = F \times D_2 + \left(1 - D_2\right) \times \frac{F}{n}
    \end{align*}

Engwall's FM:
    \begin{align*}
        FM = \frac{F \times R}{n}
    \end{align*}

Juilland's U:
    \begin{align*}
        \sigma &= \sqrt{\frac{\sum_{i = 1}^n \left(F_i - \overline{F}\right)^2}{n}} \\
        CV &= \frac{\sigma}{\overline{F}} \\
        D &= \frac{1 - CV}{\sqrt{n - 1}} \\
        U &= D \times F
    \end{align*}

Kromer's UR:
    \begin{align*}
        U_R = \sum_{i = 1}^n \psi\left(F_i + 1\right) + C
    \end{align*}

Rosengren's KF:
    \begin{align*}
        KF &= \frac{1}{n} \times \left(\sum_{i = 1}^n \sqrt{F_i}\right)^2
    \end{align*}
-->

Measure of Adjusted Frequency|Formula
-----------------------------|-------
Carroll's Um   [[15]](#doc-eng-5-15)|![Formula](/doc/measures/adjusted_freq/carrolls_um.png)
Engwall's FM   [[22]](#doc-eng-5-22)|![Formula](/doc/measures/adjusted_freq/engwalls_fm.png)<br>where **R** is the number of sub-sections in which the word appears at least once
Juilland's U   [[18]](#doc-eng-5-18)|![Formula](/doc/measures/adjusted_freq/juillands_u.png)
Kromer's UR    [[23]](#doc-eng-5-23)|![Formula](/doc/measures/adjusted_freq/kromers_ur.png)<br>where **ψ** is the [digamma function](https://en.wikipedia.org/wiki/Digamma_function), **C** is the [Euler–Mascheroni constant](https://en.wikipedia.org/wiki/Euler%E2%80%93Mascheroni_constant)
Rosengren's KF [[20]](#doc-eng-5-20)|![Formula](/doc/measures/adjusted_freq/rosengrens_kf.png)

<span id="doc-eng-4-4-3"></span>
#### 4.4.3 Tests of Statistical Significance & Measures of Effect Size [[Back to Contents]](#doc-eng)

To calculate the statistical significance, bayes factor and effect size (except **Student's t-test (Two-sample)** and **Mann-Whitney U Test**) for two words in the same file (collocates) or one specific word in two different files (keywords), two contingency tables must be constructed first, one for observed values, the other for expected values.

As for collocates (in *Collocation* and *Colligation*):

Observed Values|Word 1                       |Not Word 1                   |Row Total
--------------:|:---------------------------:|:---------------------------:|:---------------------------:
Word 2         |![o11](/doc/measures/o11.png)|![o12](/doc/measures/o12.png)|![o1x](/doc/measures/o1x.png)
Not Word 2     |![o21](/doc/measures/o21.png)|![o22](/doc/measures/o22.png)|![o2x](/doc/measures/o2x.png)
Column Total   |![ox1](/doc/measures/ox1.png)|![ox2](/doc/measures/ox2.png)|![oxx](/doc/measures/oxx.png)

Expected Values|Word 1                       |Not Word 1
--------------:|:---------------------------:|:---------------------------:
Word 2         |![e11](/doc/measures/e11.png)|![e12](/doc/measures/e12.png) 
Not Word 2     |![e21](/doc/measures/e21.png)|![e22](/doc/measures/e22.png)

![o11](/doc/measures/o11.png): Number of occurrences of Word 1 followed by Word 2<br>
![o12](/doc/measures/o12.png): Number of occurrences of Word 1 followed by any word except Word 2<br>
![o21](/doc/measures/o21.png): Number of occurrences of any word except Word 1 followed by Word 2<br>
![o22](/doc/measures/o22.png): Number of occurrences of any word except Word 1 followed by any word except Word 2

As for keywords (in *Keyword*):

Observed Values|Observed File                |Reference File               |Row Total
--------------:|:---------------------------:|:---------------------------:|:---------------------------:
Word *w*       |![o11](/doc/measures/o11.png)|![o12](/doc/measures/o12.png)|![o1x](/doc/measures/o1x.png)
Not Word *w*   |![o21](/doc/measures/o21.png)|![o22](/doc/measures/o22.png)|![o2x](/doc/measures/o2x.png)
Column Total   |![ox1](/doc/measures/ox1.png)|![ox2](/doc/measures/ox2.png)|![oxx](/doc/measures/oxx.png)

Expected Values|Observed File                |Reference File
--------------:|:---------------------------:|:---------------------------:
Word *w*       |![e11](/doc/measures/e11.png)|![e12](/doc/measures/e12.png) 
Not Word *w*   |![e21](/doc/measures/e21.png)|![e22](/doc/measures/e22.png)

![o11](/doc/measures/o11.png): Number of occurrences of Word *w* in the observed file<br>
![o12](/doc/measures/o12.png): Number of occurrences of Word *w* in the reference file<br>
![o21](/doc/measures/o21.png): Number of occurrences of all words except Word *w* in the observed file<br>
![o22](/doc/measures/o22.png): Number of occurrences of all words except Word *w* in the reference file

To conduct **Student's t-test (Two-sample)** or **Mann-Whitney U Test** on a specific word, the observed file and the reference file are first divided into **n** (5 by default) sub-sections respectively. Then, the frequencies of the word in each sub-section of the observed file and the reference file are counted and denoted by **FO₁**, **FO₂**, **FO₃** ... **FOn** and **FR₁**, **FR₂**, **FR₃** ... **FRn** respectively. The total frequency of the word in the observed file and the reference file are denoted by **FO** and **FR** respectively. The mean value of the frequencies over all sub-sections of the observed file and the reference file are denoted by ![fo-bar](/doc/measures/fo_bar.png) and ![fr-bar](/doc/measures/fr_bar.png) respectively.

<!--
Berry-Rogghe's z-score:
    \begin{align*}
        p &= \frac{C_{x1}}{C_{xx} - C_{1x}} \\
        E &= p \times C_{1x} \times S \\
        z &= \frac{C_{11} - E}{\sqrt{E \times \left(1 - p\right)}}
    \end{align*}

Log-likelihood Ratio:
    \begin{align*}
        G &= 2 \times \sum_{i = 1}^2 \sum_{j = 1}^2 \left(O_{ij} \times \ln \frac{O_{ij}}{E_{ij}}\right)
    \end{align*}

Pearson's Chi-squared Test:
    \begin{align*}
        \chi^2 = \sum_{i = 1}^2 \sum_{j = 1}^2 \frac{\left(O_{ij} - E{ij}\right)^2}{E_{ij}}
    \end{align*}

Student's t-test (1-sample):
    \begin{align*}
        t = \frac{O_{11} - E_{11}}{\sqrt{O_{11} \times \left(1 - \frac{O_{11}}{O_{xx}}\right)}}
    \end{align*}

Student's t-test (2-sample):
    \begin{align*}
        s_1 &= \frac{\sum_{i = 1}^n \left(FO_i - \overline{FO}\right)^2}{n - 1} \\
        s_2 &= \frac{\sum_{i = 1}^n \left(FR_i - \overline{FR}\right)^2}{n - 1} \\
        t &= \frac{\overline{FO} - \overline{FR}}{\sqrt{\frac{s_1 - s_2}{n}}}
    \end{align*}

z-score:
    \begin{align*}
        z = \frac{O_{11} - E_{11}}{\sqrt{E_{11} \times \left(1 - \frac{E_{11}}{O_{xx}}\right)}}
    \end{align*}
-->

Then the statistical significance, bayes factor and effect size will be calculated as follows:

Test of Statistical Significance|Formula
--------------------------------|-------
Berry-Rogghe's z-score      [[24]](#doc-eng-5-24)|![Formula](/doc/measures/statistical_significance/berry_rogghes_z_score.png)<br>where **S** is the average span size on both sides of the node word.
Fisher's Exact Test         [[25]](#doc-eng-5-25)|See: [Fisher's exact test - Wikipedia](https://en.wikipedia.org/wiki/Fisher%27s_exact_test#Example)
Log-likelihood Ratio        [[26]](#doc-eng-5-26)|![Formula](/doc/measures/statistical_significance/log_likehood_ratio_test.png)
Mann-Whitney U Test         [[27]](#doc-eng-5-27)|See: [Mann–Whitney U test - Wikipedia](https://en.wikipedia.org/wiki/Mann%E2%80%93Whitney_U_test#Calculations)
Pearson's Chi-squared Test  [[28]](#doc-eng-5-28)[[29]](#doc-eng-5-29)|![Formula](/doc/measures/statistical_significance/pearsons_chi_squared_test.png)
Student's t-test (1-sample) [[30]](#doc-eng-5-30)|![Formula](/doc/measures/statistical_significance/students_t_test_1_sample.png)
Student's t-test (2-sample) [[31]](#doc-eng-5-31)|![Formula](/doc/measures/statistical_significance/students_t_test_2_sample.png)
z-score                     [[32]](#doc-eng-5-32)|![Formula](/doc/measures/statistical_significance/z_score.png)

<!--
Log-likelihood Ratio:
    \begin{align*}
        G &= 2 \times \sum_{i = 1}^2 \sum_{j = 1}^2 \left(O_{ij} \times \ln \frac{O_{ij}}{E_{ij}}\right) \\
        BF &= G - \ln O_{xx}
    \end{align*}

Student's t-test (2-sample):
    \begin{align*}
        s_1 &= \frac{\sum_{i = 1}^n \left(FO_i - \overline{FO}\right)^2}{n - 1} \\
        s_2 &= \frac{\sum_{i = 1}^n \left(FR_i - \overline{FR}\right)^2}{n - 1} \\
        t &= \frac{\overline{FO} - \overline{FR}}{\sqrt{\frac{s_1 - s_2}{n}}} \\
        BF & = t^2 \times \ln n
    \end{align*}
-->

Measure of Bayes Factor|Formula
-----------------------|-------
Log-likelihood Ratio        [[33]](#doc-eng-5-33)|![Formula](/doc/measures/bayes_factor/log_likehood_ratio_test.png)
Student's t-test (2-sample) [[33]](#doc-eng-5-33)|![Formula](/doc/measures/bayes_factor/students_t_test_2_sample.png)

<!--
%DIFF:
    \begin{align*}
        \%DIFF = \frac{\left(\frac{O_{11}}{O_{x1}} - \frac{O_{12}}{O_{x2}}\right) \times 100}{\frac{O_{12}}{O_{x2}}}
    \end{align*}

Cubic Association Ratio:
    \begin{align*}
        IM^3 = \log_{2} \frac{{O_{11}}^3}{E_{11}}
    \end{align*}

Dice's Coefficient:
    \begin{align*}
        DSC &= \frac{2 \times O_{11}}{O_{1x} + O_{x1}}
    \end{align*}

Difference Coefficient:
    \begin{align*}
        Difference \ Coefficient = \frac{\frac{O_{11}}{O_{x1}} - \frac{O_{12}}{O_{x2}}}{\frac{O_{11}}{O_{x1}} + \frac{O_{12}}{O_{x2}}}
    \end{align*}

Jaccard Index:
    \begin{align*}
        J = \frac{O_{11}}{O_{11} + O_{12} + O_{21}}
    \end{align*}

Kilgarriff's Ratio:
    \begin{align*}
        Kilgarriff's \ Ratio = \frac{\frac{O_{11}}{O_{11} + O_{21}} \times 1000000 + \alpha}{\frac{O_{12}}{O_{12} + O_{22}} \times 1000000 + \alpha}
    \end{align*}

Log Ratio:
    \begin{align*}
        Log \ Ratio = \log_{2} \frac{\frac{O_{11}}{O_{x1}}}{\frac{O_{12}}{O_{x2}}}
    \end{align*}

Log-Frequency Biased MD:
    \begin{align*}
        LFMD = \log_{2} \frac{O_{11}}{E_{11}} + \log_{2} O_{11}
    \end{align*}

logDice:
    \begin{align*}
        logDice = 14 + \log_{2} \frac{2 \times O_{11}}{O_{1x} + O_{x1}}
    \end{align*}

MI.log-f:
    \begin{align*}
        \text{MI.log-f} = \log_{2} \frac{{O_{11}}^2}{E_{11}} \times \ln (O_{11} + 1)
    \end{align*}

Minimum Sensitivity:
    \begin{align*}
        S = \min\left\{\frac{O_{11}}{O_{1x}} \text{, } \frac{O_{11}}{O_{x1}}\right\}
    \end{align*}

Mutual Dependency:
    \begin{align*}
        MD = \log_{2} \frac{{O_{11}}^2}{E_{11}}
    \end{align*}

Mutual Expectation:
    \begin{align*}
        ME = O_{11} \times \frac{2 \times O_{11}}{O_{1x} + O_{x1}}
    \end{align*}

Mutual Information:
    \begin{align*}
        MI = \sum_{i = 1}^n \sum_{j = 1}^n (\frac{O_{ij}}{O_{xx}} \times \log_{2} \frac{O_{ij}}{E_{ij}})
    \end{align*}

Odds Ratio:
    \begin{align*}
        Odd's \ Ratio = \frac{O_{11} \times O_{22}}{O_{12} \times O_{21}}
    \end{align*}

Pointwise Mutual Information:
    \begin{align*}
        PMI = \log_{2} \frac{O_{11}}{E_{11}}
    \end{align*}

Poisson Collocation Measure:
    \begin{align*}
        sig = \frac{O_{11}(\ln O_{11} - \ln E_{11} - 1)}{\ln O_{xx}}
    \end{align*}

Squared Phi Coefficient:
    \begin{align*}
        \phi^2 = \frac{(O_{11} \times O_{22} - O_{12} \times O_{21})^2}{O_{1x} \times O_{2x} \times O_{x1} \times O_{x2}}
    \end{align*}
-->

Measure of Effect Size|Formula
----------------------|-------
%DIFF                        [[34]](#doc-eng-5-34)|![Formula](/doc/measures/effect_size/pct_diff.png)
Cubic Association Ratio      [[35]](#doc-eng-5-35)[[36]](#doc-eng-5-36)|![Formula](/doc/measures/effect_size/im3.png)
Dice's Coefficient           [[37]](#doc-eng-5-37)|![Formula](/doc/measures/effect_size/dices_coeff.png)
Difference Coefficient       [[28]](#doc-eng-5-28)[[38]](#doc-eng-5-38)|![Formula](/doc/measures/effect_size/diff_coeff.png)
Jaccard Index                [[39]](#doc-eng-5-39)|![Formula](/doc/measures/effect_size/jaccard_index.png)
Kilgarriff's Ratio           [[40]](#doc-eng-5-40)|![Formula](/doc/measures/effect_size/kilgarriffs_ratio.png)<br>where **α** is the smoothing parameter, which is 1 by default.<br>You can change the value of **α** via **Menu → Preferences → Settings → Measures →<br>Effect Size → Kilgarriff's Ratio → Smoothing Parameter**.
Log Ratio                    [[41]](#doc-eng-5-41)|![Formula](/doc/measures/effect_size/log_ratio.png)
Log-Frequency Biased MD      [[42]](#doc-eng-5-42)|![Formula](/doc/measures/effect_size/lfmd.png)
logDice                      [[43]](#doc-eng-5-43)|![Formula](/doc/measures/effect_size/log_dice.png)
MI.log-f                     [[39]](#doc-eng-5-39)[[44]](#doc-eng-5-44)|![Formula](/doc/measures/effect_size/mi_log_f.png)
Minimum Sensitivity          [[45]](#doc-eng-5-45)|![Formula](/doc/measures/effect_size/min_sensitivity.png)
Mutual Dependency            [[42]](#doc-eng-5-42)|![Formula](/doc/measures/effect_size/md.png)
Mutual Expectation           [[46]](#doc-eng-5-46)|![Formula](/doc/measures/effect_size/me.png)
Mutual Information           [[47]](#doc-eng-5-47)|![Formula](/doc/measures/effect_size/mi.png)
Odds Ratio                   [[48]](#doc-eng-5-48)|![Formula](/doc/measures/effect_size/odds_ratio.png)
Pointwise Mutual Information [[49]](#doc-eng-5-49)|![Formula](/doc/measures/effect_size/pmi.png)
Poisson Collocation Measure  [[50]](#doc-eng-5-50)|![Formula](/doc/measures/effect_size/poisson_collocation_measure.png)
Squared Phi Coefficient      [[51]](#doc-eng-5-51)|![Formula](/doc/measures/effect_size/squared_phi_coeff.png)

<span id="doc-eng-5"></span>
## 5 References [[Back to Contents]](#doc-eng)

<span id="doc-eng-5-1"></span>
[1] Smith, E. A., & Senter, R. J. (1967). Automated readability index. Aerospace Medical Research Laboratories. https://apps.dtic.mil/sti/pdfs/AD0667273.pdf<br>
<span id="doc-eng-5-2"></span>
[2] Coleman, M., & Liau, T. L. (1975). A computer readability formula designed for machine scoring. *Journal of Applied Psychology*, *60*(2), 283–284. https://doi.org/10.1037/h0076540<br>
<span id="doc-eng-5-3"></span>
[3] Dale, E., & Chall, J. S. (1948). A formula for predicting readability. *Educational Research Bulletin*, *27*(1), 11–20, 28.<br>
<span id="doc-eng-5-4"></span>
[4] Dale, E., & Chall, J. S. (1948). A formula for predicting readability: Instructions. *Educational Research Bulletin*, *27*(2), 37–54.<br>
<span id="doc-eng-5-5"></span>
[5] Smith, E. A. (1961). Devereaux readability index. *Journal of Educational Research*, *54*(8), 298–303. https://doi.org/10.1080/00220671.1961.10882728<br>
<span id="doc-eng-5-6"></span>
[6] Flesch, R. (1948). A new readability yardstick. *Journal of Applied Psychology*, *32*(3), 221–233. https://doi.org/10.1037/h0057532<br>
<span id="doc-eng-5-7"></span>
[7] Farr, J. N., Jenkins, J. J., & Paterson, D. G. (1951). Simplification of Flesch reading ease formula. *Journal of Applied Psychology*, *35*(5), 333–337. https://doi.org/10.1037/h0062427<br>
<span id="doc-eng-5-8"></span>
[8] Kincaid, J. P., Fishburne, R. P., Rogers, R. L., & Chissom, B. S. (1975). Derivation of new readability formulas (automated readability index, fog count, and Flesch reading ease formula) for navy enlisted personnel. Naval Air Station Memphis. https://apps.dtic.mil/sti/pdfs/ADA006655.pdf<br>
<span id="doc-eng-5-9"></span>
[9] Caylor, J. S., Sticht, T. G., Fox, L. C., & Ford, J. P. (1973). Methodologies for determining reading requirements of military occupational specialties. Human Resource Research Organization. https://files.eric.ed.gov/fulltext/ED074343.pdf<br>
<span id="doc-eng-5-10"></span>
[10] Gunning, R. (1968). The technique of clear writing (revised ed.). McGraw-Hill Book Company.<br>
<span id="doc-eng-5-11"></span>
[11] McLaughlin, G. H. (1969). SMOG grading: A new readability formula. *Journal of Reading*, *12*(8), pp. 639–646. <br>
<span id="doc-eng-5-12"></span>
[12] Dale, E. (1931). A comparison of two word lists. *Educational Research Bulletin*, *10*(18), 484–489.<br>
<span id="doc-eng-5-13"></span>
[13] Spache, G. (1953). A new readability formula for primary-grade reading materials. *Elementary School Journal*, *53*(7), 410–413. https://doi.org/10.1086/458513<br>
<span id="doc-eng-5-14"></span>
[14] O’Hayre, J. (1966). Gobbledygook has gotta go. U.S. Government Printing Office. https://www.governmentattic.org/15docs/Gobbledygook_Has_Gotta_Go_1966.pdf<br>
<span id="doc-eng-5-15"></span>
[15] Carroll, J. B. (1970). An alternative to Juilland’s usage coefficient for lexical frequencies and a proposal for a standard frequency index. *Computer Studies in the Humanities and Verbal Behaviour*, *3*(2), 61–65. https://doi.org/10.1002/j.2333-8504.1970.tb00778.x<br>
<span id="doc-eng-5-16"></span>
[16] Gries, S. T. (2008). Dispersions and adjusted frequencies in corpora. *International Journal of Corpus Linguistics*, *13*(4), 403–437. https://doi.org/10.1075/ijcl.13.4.02gri<br>
<span id="doc-eng-5-17"></span>
[17] Lijffijt, J., & Gries, S. T. (2012). Correction to Stefan Th. Gries’ “dispersions and adjusted frequencies in corpora”. *International Journal of Corpus Linguistics*, *17*(1), 147–149. https://doi.org/10.1075/ijcl.17.1.08lij<br>
<span id="doc-eng-5-18"></span>
[18] Juilland, A., & Chang-Rodriguez, E. (1964). Frequency dictionary of spanish words. Mouton.<br>
<span id="doc-eng-5-19"></span>
[19] Lyne, A. A. (1985). Dispersion. In *The vocabulary of French business correspondence: Word frequencies, collocations, and problems of lexicometric method* (pp. 101–124). Slatkine/Champion.<br>
<span id="doc-eng-5-20"></span>
[20] Rosengren, I. (1971). The quantitative concept of language and its relation to the structure of frequency dictionaries. *Études de linguistique appliquée*, *1*, 103–127.<br>
<span id="doc-eng-5-21"></span>
[21] Zhang, H., Huang, C., & Yu, S. (2004). Distributional consistency: As a general method for defining a core lexicon. In M. T. Lino, M. F. Xavier, F. Ferreira, R. Costa, & R. Silva (Eds.), *Proceedings of Fourth International Conference on Language Resources and Evaluation* (pp. 1119–1122). European Language Resources Association.<br>
<span id="doc-eng-5-22"></span>
[22] Engwall, G. (1974). Fréquence et distribution du vocabulaire dans un choix de romans français [Unpublished doctoral dissertation]. Stockholm University.<br>
<span id="doc-eng-5-23"></span>
[23] Kromer, V. (2003). A usage measure based on psychophysical relations. *Journal of Quatitative Linguistics*, *10*(2), 177–186. https://doi.org/10.1076/jqul.10.2.177.16718<br>
<span id="doc-eng-5-24"></span>
[24] Berry-Rogghe, G. L. M. (1973). The computation of collocations and their relevance in lexical studies. In A. J. Aiken, R. W. Bailey, & N. Hamilton-Smith (Eds.), *The computer and literary studies* (pp. 103–112). Edinburgh University Press.<br>
<span id="doc-eng-5-25"></span>
[25] Pedersen, T. (1996). Fishing for exactness. In T. Winn (Ed.), *Proceedings of the Sixth Annual South-Central Regional SAS Users' Group Conference* (pp. 188-200). The South–Central Regional SAS Users' Group.<br>
<span id="doc-eng-5-26"></span>
[26] Dunning, T. E. (1993). Accurate methods for the statistics of surprise and coincidence. *Computational Linguistics*, *19*(1), 61–74.<br>
<span id="doc-eng-5-27"></span>
[27] Kilgarriff, A. (2001). Comparing corpora. *International Journal of Corpus Linguistics*, *6*(1), 232–263. https://doi.org/10.1075/ijcl.6.1.05kil<br>
<span id="doc-eng-5-28"></span>
[28] Hofland, K., & Johanson, S. (1982). *Word frequencies in British and American English*. Norwegian Computing Centre for the Humanities.<br>
<span id="doc-eng-5-29"></span>
[29] Oakes, M. P. (1998). *Statistics for Corpus Linguistics*. Edinburgh University Press.<br>
<span id="doc-eng-5-30"></span>
[30] Church, K., Gale, W., Hanks P., & Hindle D. (1991). Using statistics in lexical analysis. In U. Zernik (Ed.), *Lexical acquisition: Exploiting on-line resources to build a lexicon* (pp. 115–164). Psychology Press.<br>
<span id="doc-eng-5-31"></span>
[31] Paquot, M., & Bestgen, Y. (2009). Distinctive words in academic writing: A comparison of three statistical tests for keyword extraction. *Language and Computers*, *68*, 247–269.<br>
<span id="doc-eng-5-32"></span>
[32] Dennis, S. F. (1964). The construction of a thesaurus automatically from a sample of text. In M. E. Stevens, V. E. Giuliano, & L. B. Heilprin (Eds.), *Proceedings of the symposium on statistical association methods for mechanized documentation* (pp. 61–148). National Bureau of Standards.<br>
<span id="doc-eng-5-33"></span>
[33] Wilson, A. (2013). Embracing Bayes Factors for key item analysis in corpus linguistics. In M. Bieswanger, & A. Koll-Stobbe (Eds.), *New Approaches to the Study of Linguistic Variability* (pp. 3–11). Peter Lang.<br>
<span id="doc-eng-5-34"></span>
[34] Gabrielatos, C., & Marchi, A. (2012, September 13–14). Keyness: Appropriate metrics and practical issues [Conference session]. CADS International Conference 2012, University of Bologna, Italy.<br>
<span id="doc-eng-5-35"></span>
[35] Daille, B. (1994). Approche mixte pour l'extraction automatique de terminologie: statistiques lexicales et filtres linguistiques [Doctoral thesis, Université Paris 7]. Béatrice Daille. http://www.bdaille.com/index.php?option=com_docman&task=doc_download&gid=8&Itemid=<br>
<span id="doc-eng-5-36"></span>
[36] Daille, B. (1995). Combined approach for terminology extraction: Lexical statistics and linguistic filtering. UCREL technical papers (Vol. 5). Lancaster University.<br>
<span id="doc-eng-5-37"></span>
[37] Smadja, F., McKeown, K. R., & Hatzivassiloglou, V. (1996). Translating collocations for bilingual lexicons: A statistical approach. *Computational Linguistics*, *22*(1), pp. 1–38.<br>
<span id="doc-eng-5-38"></span>
[38] Gabrielatos, C. (2018). Keyness analysis: Nature, metrics and techniques. In C. Taylor & A. Marchi (Eds.), *Corpus approaches to discourse: A critical review* (pp. 225–258). Routledge.<br>
<span id="doc-eng-5-39"></span>
[39] Lexical Computing Ltd. (2015, July 8). Statistics used in Sketch Engine. Retrieved November 26, 2018 from https://www.sketchengine.eu/documentation/statistics-used-in-sketch-engine/<br>
<span id="doc-eng-5-40"></span>
[40] Kilgarriff, A. (2009). Simple maths for keywords. In M. Mahlberg, V. González-Díaz, & C. Smith (Eds.), *Proceedings of the Corpus Linguistics Conference 2009* (p. 171). University of Liverpool.<br>
<span id="doc-eng-5-41"></span>
[41] Hardie, A. (2014, April 28). Log ratio: An informal introduction. ESRC Centre for Corpus Approaches to Social Science (CASS). http://cass.lancs.ac.uk/log-ratio-an-informal-introduction/.<br>
<span id="doc-eng-5-42"></span>
[42] Thanopoulos, A., Fakotakis, N., Kokkinakis, G. (2002). Comparative evaluation of collocation extraction metrics. In M. G. González, & C. P. S. Araujo (Eds.), *Proceedings of the Third International Conference on Language Resources and Evaluation* (pp. 620–625). European Language Resources Association.<br>
<span id="doc-eng-5-43"></span>
[43] Rychlý, P. (2008). A lexicographyer-friendly association score. In P. Sojka, & A. Horák (Eds.), *Proceedings of Second Workshop on Recent Advances in Slavonic Natural Languages Processing*. Masaryk University<br>
<span id="doc-eng-5-44"></span>
[44] Kilgarriff, A., & Tugwell, D. (2002). WASP-bench – an MT lexicographers' workstation supporting state-of-the-art lexical disambiguation. In *Proceedings of the 8th Machine Translation Summit* (pp. 187–190). European Association for Machine Translation.<br>
<span id="doc-eng-5-45"></span>
[45] Pedersen, T. (1998). Dependent bigram identification. In *Proceedings of the Fifteenth National Conference on Artificial Intelligence* (p. 1197). AAAI Press.<br>
<span id="doc-eng-5-46"></span>
[46] Dias, G., Guilloré, S., & Pereira Lopes, J. G. (1999). Language independent automatic acquisition of rigid multiword units from unrestricted text corpora. In A. Condamines, C. Fabre, & M. Péry-Woodley (Eds.), *TALN'99: 6ème Conférence Annuelle Sur le Traitement Automatique des Langues Naturelles* (pp. 333–339). TALN.<br>
<span id="doc-eng-5-47"></span>
[47] Dunning, T. E. (1998). Finding structure in text, genome and other symbolic sequences [Doctoral dissertation, University of Sheffield]. arXiv. arxiv.org/pdf/1207.1847.pdf<br>
<span id="doc-eng-5-48"></span>
[48] Pojanapunya, P., & Todd, R. W. (2016). Log-likelihood and odds ratio keyness statistics for different purposes of keyword analysis. *Corpus Linguistics and Lingustic Theory*, *15*(1), pp. 133–167. https://doi.org/10.1515/cllt-2015-0030<br>
<span id="doc-eng-5-49"></span>
[49] Church, K. W., & Hanks, P. (1990). Word association norms, mutual information, and lexicography. *Computational Linguistics*, *16*(1), 22–29.<br>
<span id="doc-eng-5-50"></span>
[50] Quasthoff, U., & Wolff, C. (2002). The poisson collocation measure and its applications. *Proceedings of 2nd International Workshop on Computational Approaches to Collocations*. IEEE.<br>
<span id="doc-eng-5-51"></span>
[51] Church, K. W., & Gale, W. A. (1991, September 29–October 1). Concordances for parallel text [Paper presentation]. Using Corpora: Seventh Annual Conference of the UW Centre for the New OED and Text Research, St. Catherine's College, Oxford, United Kingdom.<br>

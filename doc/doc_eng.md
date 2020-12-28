<!--
# Wordless: Documentation - English
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
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
        - 4.4.1 [Measures of Dispersion & Adjusted Frequency](#doc-eng-4-4-1)
        - 4.4.2 [Tests of Statistical Significance & Measures of Effect Size](#doc-eng-4-4-2)
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
In most cases, the first thing to do in *Wordless* is open and select your files to be processed via **Menu → File** or by clicking the buttons residing under the *File Table*.

Files are selected by default after being added to the *File Table*. **Only selected files will be processed by Wordless**. You can drag and drop files around the *File Table* to change their orders, which will be reflected in the results produced by Wordless.

By default, Wordless will try to detect the language, text type and encoding of the file, you should check and make sure that the settings of each and every file is correct. If you do not want Wordless to detect the settings for you and prefer setting them manually, you can change the settings in **Auto-detection Settings** in the *Settings Area*.

- **2.1 Add File(s)**<br>
    Add one single file or multiple files to the *File Table*.

    \* You can use the **Ctrl** key (**Command** key on macOS) and/or the **Shift** key to select multiple files.

- **2.2 Add Folder**<br>
    Add all files in the folder to the *File Table*.

    By default, all files in subfolders (and subfolders of subfolders, and so on) will also be added to the *File Table*. If you do not want to add files in subfolders to the *File Table*, uncheck **Folder Settings → Subfolders** in the *Settings Area*.

- **2.3 Reopen Closed File(s)**<br>
    Add file(s) that are closed the last time back to the *File Table*.

    \* The history of all closed files will be erased upon exit of *Wordless*.

- **2.4 Select All**<br>
    Select all files in the *File Table*.

- **2.5 Invert Selection**<br>
    Select all files that are not currently selected and deselect all currently selected files in the *File Table*.

- **2.6 Deselect All**<br>
    Deselect all files in the *File Table*.

- **2.7 Close Selected**<br>
    Remove all currently selected files in the *File Table*.

- **2.8 Close All**<br>
    Remove all files in the *File Table*.

<span id="doc-eng-3"></span>
## 3 Work Area [[Back to Contents]](#doc-eng)

<span id="doc-eng-3-1"></span>
### 3.1 Overview [[Back to Contents]](#doc-eng)
In *Overview*, you can check/compare the language features of different files.

- **3.1.1 Count of Paragraphs**<br>
    Number of paragraphs in each file. Each line in the file will be counted as one paragraph. Blank lines and lines containing only spaces, tabs and other invisible characters are ignored.

- **3.1.2 Count of Sentences**<br>
    Number of sentences in each file. *Wordless* will automatically apply the built-in sentence tokenizer according to the language of each file in order to calculate the number of sentences in each file. You can change the sentence tokenizer settings via **Menu → Preferences → Settings → Sentence Tokenization → Sentence Tokenizer Settings**.

- **3.1.3 Count of Clauses**<br>
    Number of clauses (delimited by commas, colons, semi-colons, question marks, exclamations marks, quotes, em-dashes, etc.) in each file. *Wordless* will automatically apply the built-in clause tokenizer according to the language of each file in order to calculate the number of clauses in each file.

- **3.1.4 Count of Tokens**<br>
    Number of tokens in each file. *Wordless* will automatically apply the built-in word tokenizer according to the language of each file in order to calculate the number of tokens in each file. You can change the word tokenizer settings via **Menu → Preferences → Settings → Word Tokenization → Word Tokenizer Settings**.

    You can specify what should be counted as a "token" via **Token Settings** in the *Settings Area*

- **3.1.5 Count of Types**<br>
    Number of token types in each file.

- **3.1.6 Count of Characters**<br>
    Number of single characters in each file. Spaces, tabs and all other invisible characters are ignored.

- **3.1.7 Type-Token Ratio**<br>
    Number of token types divided by number of tokens.

- **3.1.8 Type-Token Ratio (Standardized)**<br>
    Standardized type-token ratio. Each file will be divided into several sub-sections with each one consisting of 1000 tokens by default and type-token ratio will be calculated for each part. The standardized type-token ratio of each file is then averaged out over all sub-sections. You can change the number of tokens in each sub-section via **Generation Settings → Base of standardized type-token ratio**.

    The last section will be discarded if the number of tokens in it is smaller than the base of standardized type-token ratio in order to prevent the result from being affected by outliers (extreme values).

- **3.1.9 Paragraph Length in Sentence (Mean)**<br>
    The average value of paragraph length expressed as the number of sentences.

- **3.1.10 Paragraph Length in Sentence (Standard Deviation)**<br>
    The standard deviation of paragraph length expressed as the number of sentences.

- **3.1.11 Paragraph Length in Token (Mean)**<br>
    The average value of paragraph length expressed as number of tokens.

- **3.1.12 Paragraph Length in Token (Standard Deviation)**<br>
    The standard deviation of paragraph length expressed as number of tokens.

- **3.1.13 Sentence Length in Token (Mean)**<br>
    The average value of sentence length expressed as number of tokens.

- **3.1.14 Sentence Length in Token (Standard Deviation)**<br>
    The standard deviation of sentence length expressed as number of tokens.

- **3.1.15 Clause Length in Token (Mean)**<br>
    The average value of clause length expressed as number of tokens.

- **3.1.16 Clause Length in Token (Standard Deviation)**<br>
    The standard deviation of clause length expressed as number of tokens.

- **3.1.17 Token Length in Character (Mean)**<br>
    The average value of token length expressed as number of characters.

- **3.1.18 Token Length in Character (Standard Deviation)**<br>
    The standard deviation of token length expressed as number of characters.

- **3.1.19 Type Length in Character (Mean)**<br>
    The average value of type length expressed as number of characters.

- **3.1.20 Type Length in Character (Standard Deviation)**<br>
    The standard deviation of type length expressed as number of characters.

- **3.1.21 Count of n-length Tokens**<br>
    Number of n-length tokens, where n = 1, 2, 3, etc.

![Overview Table](/doc/overview/overview_table.png)

<span id="doc-eng-3-2"></span>
### 3.2 Concordancer [[Back to Contents]](#doc-eng)
In *Concordancer*, you can search for any token in different files and generate concordance lines. You can adjust the settings for the generated data via **Generation Settings**.

After the concordance lines are generated and displayed in the table, you can sort the results by clicking **Sort Results** or search in results by clicking **Search in Results**, both buttons residing at the right corner of the *Results Area*.

In addition, you can generate concordance plots for any search term. You can modify the settings for the generated figure via **Figure Settings**. By default, data in concordance plot are sorted by file. You can sort the data by search term instead via **Figure Settings → Sort Results by**.

- **3.2.1 Left**<br>
    The context before each search term, which displays 10 tokens left to the **Node** by default. You can change this behavior via **Generation Settings**.

- **3.2.2 Node**<br>
    Nodes are search terms specified in **Search Settings → Search Term**.

- **3.2.3 Right**<br>
    The context after each search term, which displays 10 tokens right to the **Node** by default. You can change this behavior via **Generation Settings**.

- **3.2.4 Token No.**<br>
    The position of the first token of **Node** in each file.

- **3.2.5 Clause No.**<br>
    The position of the clause in which the **Node** is found in each file.

- **3.2.6 Sentence No.**<br>
    The position of the sentence in which the **Node** is found in each file.

- **3.2.7 Paragraph No.**<br>
    The position of the paragraph in which the **Node** is found in each file.

- **3.2.8 File**<br>
    The file in which the **Node** is found.

![Concordance Table](/doc/concordancer/concordancer_table.png)
![Concordance Figure - File](/doc/concordancer/concordancer_fig_file.png)
![Concordance Figure - Search Term](/doc/concordancer/concordancer_fig_search_term.png)

<span id="doc-eng-3-3"></span>
### 3.3 Wordlist [[Back to Contents]](#doc-eng)
In *Wordlist*, you can generate wordlists for different files and calculate the raw frequency, relative frequency, dispersion and adjusted frequency for each token.

In addition, you can generate line charts or word clouds for wordlists using any statistics. You can modify the settings for the generated figure via **Figure Settings**.

Lastly, you can further filter the results as you see fit by clicking **Filter Results** or search in the results for the part that might be of interest to you by clicking **Search in Results**, both buttons residing at the right corner of the *Results Area*.

- **3.3.1 Rank**<br>
    The rank of the token sorted by its frequency in the first file in descending order (by default). You can sort the results again by clicking the column headers. 

- **3.3.2 Token**<br>
    You can specify what should be counted as a "token" via **Token Settings**.

- **3.3.3 Frequency**<br>
    The number of occurrences of the token in each file.

- **3.3.4 Dispersion**<br>
    The dispersion of the token in each file. You can change the measure of dispersion used via **Generation Settings → Measure of Dispersion**. See [Measures of Dispersion & Adjusted Frequency](#doc-eng-supported-measures-dispersion-adjusted-freq) for more details.

- **3.3.5 Adjusted Frequency**<br>
    The adjusted frequency of the token in each file. You can change the measure of adjusted frequency used via **Generation Settings → Measure of Adjusted Frequency**. See [Measures of Dispersion & Adjusted Frequency](#doc-eng-supported-measures-dispersion-adjusted-freq) for more details.

- **3.3.6 Number of Files Found**<br>
    The number of files in which the token appears at least once.

![Wordlist Table](/doc/wordlist/wordlist_table.png)
![Wordlist Figure - Line Chart](/doc/wordlist/wordlist_fig_line_chart.png)
![Wordlist Figure - Word Cloud](/doc/wordlist/wordlist_fig_word_cloud.png)

<span id="doc-eng-3-4"></span>
### 3.4 N-gram [[Back to Contents]](#doc-eng)
In *N-gram*, you can search for n-grams (consecutive tokens) or skip-grams (non-consecutive tokens) in different files, count and compute the raw frequency and relative frequency of each n-gram/skip-gram, and calculate the dispersion and adjusted frequency for each n-gram/skip-gram using different measures.  You can adjust the settings for the generated data via **Generation Settings**. To allow skip-grams in the results, check **Generation Settings → Allow skipped tokens** and modify the settings. You can also set constraints on the position of search terms in all n-grams via **Search Settings → Search Term Position**.

It is possible to disable searching altogether and generate an exhausted list of n-grams/skip-grams by unchecking **Search Settings** for each file, but it is not recommended to do so, since the processing speed might be to slow.

In addition, you can generate line charts or word clouds for n-grams using any statistics. You can modify the settings for the generated figure via **Figure Settings**.

Lastly, you can further filter the results as you see fit by clicking **Filter Results** or search in the results for the part that might be of interest to you by clicking **Search in Results**, both buttons residing at the right corner of the *Results Area*.

- **3.4.1 Rank**<br>
    The rank of the n-gram sorted by its frequency in the first file in descending order (by default). You can sort the results again by clicking the column headers. 

- **3.4.2 N-gram**<br>
    You can specify what should be counted as a "n-gram" via **Token Settings**.

- **3.4.3 Frequency**<br>
    The number of occurrences of the n-gram in each file.

- **3.4.4 Dispersion**<br>
    The dispersion of the n-gram in each file. You can change the measure of dispersion used via **Generation Settings → Measure of Dispersion**. See [Measures of Dispersion & Adjusted Frequency](#doc-eng-supported-measures-dispersion-adjusted-freq) for more details.

- **3.4.5 Adjusted Frequency**<br>
    The adjusted frequency of the n-gram in each file. You can change the measure of adjusted frequency used via **Generation Settings → Measure of Adjusted Frequency**. See [Measures of Dispersion & Adjusted Frequency](#doc-eng-supported-measures-dispersion-adjusted-freq) for more details.

- **3.4.6 Number of Files Found**<br>
    The number of files in which the n-gram appears at least once.

![N-gram Table](/doc/ngram/ngram_table.png)
![N-gram Figure - Line Chart](/doc/ngram/ngram_fig_line_chart.png)
![N-gram Figure - Word Cloud](/doc/ngram/ngram_fig_word_cloud.png)

<span id="doc-eng-3-5"></span>
### 3.5 Collocation [[Back to Contents]](#doc-eng)
In *Collocation*, you can search for patterns of collocation (tokens that co-occur more often than would be expected by chance) within a given collocational window (from 5 words to the left to 5 words to the right by default), conduct different tests of statistical significance on each pair of tokens and calculate the effect size for each pair using different measures. You can adjust the settings for the generated data via **Generation Settings**.

It is possible to disable searching altogether and generate an exhausted list of patterns of collocation by unchecking **Search Settings** for each file, but it is not recommended to do so, since the processing speed might be to slow.

In addition, you can generate line charts or word clouds for patterns of collocation using any statistics. You can modify the settings for the generated figure via **Figure Settings**.

Lastly, you can further filter the results as you see fit by clicking **Filter Results** or search in the results for the part that might be of interest to you by clicking **Search in Results**, both buttons residing at the right corner of the *Results Area*.

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
    The test statistic of the significance test conducted on the node and the collocating token in each file. You can change the test of statistical significance used via **Generation Settings → Test of Statistical Significance**. See [Tests of Statistical Significance & Measures of Effect Size](#doc-eng-supported-measures-statistical-significance-effect-size) for more details.

    Please note that test statistic is not avilable for some tests of statistical significance.

- **3.5.7 p-value**<br>
    The p-value of the significance test conducted on the node and the collocating token in each file. You can change the test of statistical significance used via **Generation Settings → Test of Statistical Significance**. See [Tests of Statistical Significance & Measures of Effect Size](#doc-eng-supported-measures-statistical-significance-effect-size) for more details.

- **3.5.8 Bayes Factor**<br>
    The bayes factor of the significance test conducted on the node and the collocating token in each file. You can change the test of statistical significance used via **Generation Settings → Test of Statistical Significance**. See [Tests of Statistical Significance & Measures of Effect Size](#doc-eng-supported-measures-statistical-significance-effect-size) for more details.

    Please note that bayes factor is not avilable for some tests of statistical significance.

- **3.5.9 Effect Size**<br>
    The effect size of the node and the collocating token in each file. You can change the measure of effect size used via **Generation Settings → Measure of Effect Size**. See [Tests of Statistical Significance & Measures of Effect Size](#doc-eng-supported-measures-statistical-significance-effect-size) for more details.

- **3.5.10 Number of Files Found**<br>
    The number of files in which the the node and the collocating token co-occur at least once.

![Collocation Table](/doc/collocation/collocation_table.png)
![Collocation Figure - Line Chart](/doc/collocation/collocation_fig_line_chart.png)
![Collocation Figure - Word Cloud](/doc/collocation/collocation_fig_word_cloud.png)
![Collocation Figure - Network Graph](/doc/collocation/collocation_fig_network_graph.png)

<span id="doc-eng-3-6"></span>
### 3.6 Colligation [[Back to Contents]](#doc-eng)
In *Colligation*, you can search for patterns of colligation (parts of speech that co-occur more often than would be expected by chance) within a given collocational window (from 5 words to the left to 5 words to the right by default), conduct different tests of statistical significance on each pair of parts of speech and calculate the effect size for each pair using different measures. You can adjust the settings for the generated data via **Generation Settings**.

*Wordless* will automatically apply its built-in POS tagger on every file that are not POS-tagged already according to the language of each file. If POS-tagging is not supported for the given languages, the user should provide a file that has already been POS-tagged and make sure that the correct **Text Type** has been set on each file.

It is possible to disable searching altogether and generate an exhausted list of patterns of colligation by unchecking **Search Settings** for each file, but it is not recommended to do so, since the processing speed might be to slow.

In addition, you can generate line charts or word clouds for patterns of colligation using any statistics. You can modify the settings for the generated figure via **Figure Settings**.

Lastly, you can further filter the results as you see fit by clicking **Filter Results** or search in the results for the part that might be of interest to you by clicking **Search in Results**, both buttons residing at the right corner of the *Results Area*.

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
    The test statistic of the significance test conducted on the node and the collocating part of speech in each file. You can change the test of statistical significance used via **Generation Settings → Test of Statistical Significance**. See [Tests of Statistical Significance & Measures of Effect Size](#doc-eng-supported-measures-statistical-significance-effect-size) for more details.

    Please note that test statistic is not avilable for some tests of statistical significance.

- **3.6.7 p-value**<br>
    The p-value of the significance test conducted on the node and the collocating part of speech in each file. You can change the test of statistical significance used via **Generation Settings → Test of Statistical Significance**. See [Tests of Statistical Significance & Measures of Effect Size](#doc-eng-supported-measures-statistical-significance-effect-size) for more details.

- **3.6.8 Bayes Factor**<br>
    The bayes factor of the significance test conducted on the node and the collocating part of speech in each file. You can change the test of statistical significance used via **Generation Settings → Test of Statistical Significance**. See [Tests of Statistical Significance & Measures of Effect Size](#doc-eng-supported-measures-statistical-significance-effect-size) for more details.

    Please note that bayes factor is not avilable for some tests of statistical significance.

- **3.6.9 Effect Size**<br>
    The effect size of the node and the collocating part of speech in each file. You can change the measure of effect size used via **Generation Settings → Measure of Effect Size**. See [Tests of Statistical Significance & Measures of Effect Size](#doc-eng-supported-measures-statistical-significance-effect-size) for more details.

- **3.6.10 Number of Files Found**<br>
    The number of files in which the the node and the collocating part of speech co-occur at least once.

![Colligation Table](/doc/colligation/colligation_table.png)
![Colligation Figure - Line Chart](/doc/colligation/colligation_fig_line_chart.png)
![Colligation Figure - Word Cloud](/doc/colligation/colligation_fig_word_cloud.png)
![Colligation Figure - Network Graph](/doc/colligation/colligation_fig_network_graph.png)

<span id="doc-eng-3-7"></span>
### 3.7 Keyword [[Back to Contents]](#doc-eng)
In *Keyword*, you can search for candidates of potential keywords (tokens that have far more or far less frequency in the observed file than in the reference file) in different files given a reference corpus, conduct different tests of statistical significance on each keyword and calculate the effect size for each keyword using different measures. You can adjust the settings for the generated data via **Generation Settings**.

In addition, you can generate line charts or word clouds for keywords using any statistics. You can modify the settings for the generated figure via **Figure Settings**.

Lastly, you can further filter the results as you see fit by clicking **Filter Results** or search in the results for the part that might be of interest to you by clicking **Search in Results**, both buttons residing at the right corner of the *Results Area*.

- **3.7.1 Rank**<br>
    The rank of the keyword sorted by the p-value of the significance test conducted on the keyword in the first file in ascending order (by default). You can sort the results again by clicking the column headers. 

- **3.7.2 Keyword**<br>
    The candidates of potantial keywords. You can specify what should be counted as a "token" via **Token Settings**.

- **3.7.3 Frequency (in Reference File)**<br>
    The number of co-occurrences of the keywords in the reference file.

- **3.7.4 Frequency (in Observed Files)**<br>
    The number of co-occurrences of the keywords in each observed file.

- **3.7.5 Test Statistic**<br>
    The test statistic of the significance test conducted on the keyword in each file. You can change the test of statistical significance used via **Generation Settings → Test of Statistical Significance**. See [Tests of Statistical Significance & Measures of Effect Size](#doc-eng-supported-measures-statistical-significance-effect-size) for more details.

- **3.7.6 p-value**<br>
    The p-value of the significance test conducted on the keyword in each file. You can change the test of statistical significance used via **Generation Settings → Test of Statistical Significance**. See [Tests of Statistical Significance & Measures of Effect Size](#doc-eng-supported-measures-statistical-significance-effect-size) for more details.

- **3.7.7 Bayes Factor**<br>
    The bayes factor of the significance test conducted on the keyword in each file. You can change the test of statistical significance used via **Generation Settings → Test of Statistical Significance**. See [Tests of Statistical Significance & Measures of Effect Size](#doc-eng-supported-measures-statistical-significance-effect-size) for more details.

    Please note that bayes factor is not avilable for some tests of statistical significance.

- **3.7.8 Effect Size**<br>
    The effect size of on the keyword in each file. You can change the measure of effect size used via **Generation Settings → Measure of Effect Size**. See [Tests of Statistical Significance & Measures of Effect Size](#doc-eng-supported-measures-statistical-significance-effect-size) for more details.

- **3.7.9 Number of Files Found**<br>
    The number of files in which the keyword appears at least once.

![Keyword Table](/doc/keyword/keyword_table.png)
![Keyword Figure - Line Chart](/doc/keyword/keyword_fig_line_chart.png)
![Keyword Figure - Word Cloud](/doc/keyword/keyword_fig_word_cloud.png)

<span id="doc-eng-4"></span>
## 4 Appendixes [[Back to Contents]](#doc-eng)

<span id="doc-eng-4-1"></span>
### 4.1 Supported Languages [[Back to Contents]](#doc-eng)

Languages|Sentence Tokenization|Word Tokenization|Word Detokenization|POS Tagging|Lemmatization|Stop Words
:-------:|:-------------------:|:---------------:|:-----------------:|:---------:|:-----------:|:--------:
Afrikaans            |✔|✔|⭕️ |✖️|✖️|✔️
Albanian             |✔|✔|⭕️ |✖️|✖️|✔️
Arabic               |✔|✔️|⭕️ |✖️|✖️|✔️
Armenian             |✔|✔|⭕️ |✖️|✖️|✔️
Asturian             |⭕️ |⭕️ |⭕️ |✖️|✔️|✖️
Azerbaijani          |⭕️ |⭕️ |⭕️ |✖️|✖️|✔️
Basque               |✔|✔|⭕️ |✖️|✖️|✔️
Belarusian           |⭕️ |⭕️ |⭕️ |✖️|✖️|✔️
Bengali              |✔|✔️|⭕️ |✖️|✖️|✔️
Breton               |⭕️ |⭕️ |⭕️ |✖️|✖️|✔️
Bulgarian            |✔|✔️|⭕️ |✖️|✔️|✔️
Catalan              |✔|✔️|✔️|✖️|✔️|✔️
Chinese (Simplified) |✔|✔️|✔️|✔️|✖️|✔️
Chinese (Traditional)|✔|✔️|✔️|✔️|✖️|✔️
Croatian             |✔|✔️|⭕️ |✖️|✖️|✔️
Czech                |✔|✔️|✔️|✖️|✔️|✔️
Danish               |✔|✔️|⭕️ |✔️|✔️|✔️
Dutch                |✔|✔️|✔️|✔️|✔️|✔️
English              |✔|✔️|✔️|✔️|✔️|✔️
Esperanto            |⭕️ |⭕️ |⭕️ |✖️|✖️|✔️
Estonian             |✔|✔️|⭕️ |✖️|✔️|✔️
Finnish              |✔|✔️|✔️|✖️|✖️|✔️
French               |✔|✔️|✔️|✔️|✔️|✔️
Galician             |⭕️ |⭕️ |⭕️ |✖️|✔️|✔️
German               |✔|✔️|✔️|✔️|✔️|✔️
Greek (Ancient)      |⭕️ |⭕️ |⭕️ |✖️|✔️|✔️
Greek (Modern)       |✔|✔️|✔️|✔️|✔️|✔️
Gujarati             |✔|✔|⭕️ |✖️|✖️|✔️
Hausa                |⭕️ |⭕️ |⭕️ |✖️|✖️|✔️
Hebrew               |✔|✔️|⭕️ |✖️|✖️|✔️
Hindi                |✔|✔️|⭕️ |✖️|✖️|✔️
Hungarian            |✔|✔️|✔️|✖️|✔️|✔️
Icelandic            |✔|✔️|✔️|✖️|✖️|✔️
Indonesian           |✔|✔️|⭕️ |✖️|✖️|✔️
Irish                |✔|✔️|✔️|✖️|✔️|✔️
Italian              |✔|✔️|✔️|✔️|✔️|✔️
Japanese             |✔|✔|✔️|✔️|✖️|✔️
Kannada              |✔|✔️|⭕️ |✖️|✖️|✔️
Kazakh               |⭕️ |⭕️ |⭕️ |✖️|✖️|✔️
Korean               |⭕️ |⭕️ |⭕️ |✖️|✖️|✔️
Kurdish              |⭕️ |⭕️ |⭕️ |✖️|✖️|✔️
Latin                |⭕️ |⭕️ |⭕️ |✖️|✖️|✔️
Latvian              |✔|✔️|✔️|✖️|✖️|✔️
Ligurian             |✔|✔️|⭕️ |✖️|✖️|✔️
Lithuanian           |✔️|✔️|✔️|✔️|✔️|✔️
Luxembourgish        |✔️|✔️|⭕️ |✖️|✖️|✔️
Malay                |⭕️ |⭕️ |⭕️ |✖️|✖️|✔️
Malayalam            |✔️|✔️|⭕️ |✖️|✖️|✔️
Manx                 |⭕️ |⭕️ |⭕️ |✖️|✔️|✖️
Marathi              |⭕️ |✔️|⭕️ |✖️|✖️|✔️
Mongolian            |⭕️ |⭕️ |⭕️ |✖️|✖️|✔️
Nepali               |✔|✔|⭕️ |✖️|✖️|✔️
Norwegian Bokmål     |✔|✔️|⭕️ |✔️|✔️|✔️
Norwegian Nynorsk    |✔|⭕️ |⭕️ |✖️|✖️|✔️
Persian              |✔|✔️|⭕️ |✖️|✔️|✔️
Polish               |✔|✔️|✔️|✔️|✔️|✔️
Portuguese           |✔|✔️|✔️|✔️|✔️|✔️
Romanian             |✔|✔️|✔️|✔️|✔️|✔️
Russian              |✔️|✔️|✔️|✔️|✔️|✔️
Scottish Gaelic      |⭕️ |⭕️ |⭕️ |✖️|✔️|✖️
Serbian (Cyrillic)   |⭕️ |✔️|⭕️ |✖️|✖️|✔️
Serbian (Latin)      |⭕️ |✔️|⭕️ |✖️|✖️|✔️
Sinhala              |✔|✔️|⭕️ |✖️|✖️|✔️
Slovak               |✔|✔️|✔️|✖️|✔️|✔️
Slovenian            |✔|✔️|✔️|✖️|✔️|✔️
Sotho (Southern)     |⭕️ |⭕️ |⭕️ |✖️|✖️|✔️
Spanish              |✔|✔️|✔️|✔️|✔️|✔️
Swahili              |⭕️ |⭕️ |⭕️ |✖️|✖️|✔️
Swedish              |✔|✔️|✔️|✖️|✔️|✔️
Tagalog              |✔|✔️|⭕️ |✖️|✖️|✔️
Tajik                |⭕️ |✔️|⭕️ |✖️|✖️|✔️
Tamil                |✔|✔️|✔️|✖️|✖️|✔️
Tatar                |✔|✔️|⭕️ |✖️|✖️|✔️
Telugu               |✔|✔️|⭕️ |✖️|✖️|✔️
Thai                 |✔|✔️|✔️|✔️|✖️|✔️
Tibetan              |⭕️ |✔️|✔️|✔️|✔️|✖️
Turkish              |✔|✔️|⭕️ |✖️|✖️|✔️
Ukrainian            |✔|✔️|⭕️ |✔️|✔️|✔️
Urdu                 |✔|✔️|⭕️ |✖️|✖️|✔️
Vietnamese           |✔|✔️|⭕️ |✔️|✖️|✔️
Welsh                |⭕️ |⭕️ |⭕️ |✖️|✔️|✖️
Yoruba               |✔|✔|⭕️ |✖️|✖️|✔️
Zulu                 |⭕️ |⭕️ |⭕️ |✖️|✖️|✔️
Other Languages      |⭕️ |⭕️ |⭕️ |✖️|✖️|✖️

✔: Supported<br>
⭕️: Supported but falls back to the default English tokenizer<br>
✖️: Not supported

<span id="doc-eng-4-2"></span>
### 4.2 Supported File Types [[Back to Contents]](#doc-eng)

File Types|File Extensions
----------|--------------
Text File               |\*.txt
Microsoft Word Document |\*.docx
Microsoft Excel Workbook|\*.xlsx
CSV File                |\*.csv
HTML Page               |\*.htm, \*.html
XML File                |\*.xml
Translation Memory File |\*.tmx
Lyrics File             |\*.lrc

\* Microsoft 97-03 Word documents (\*.doc) are not supported.<br>
\* Non-text files will be converted to text files first before being added to the *File Table*. You can check the converted files under folder **Import** at the installation location of *Wordless* on your computer (as for macOS users, right click **Wordless.app**, select **Show Package Contents** and navigate to **Contents/MacOS/Import/**). You can change this location via **Menu → Preferences → Settings → Import → Temporary Files → Default Path**.

<span id="doc-eng-4-3"></span>
### 4.3 Supported File Encodings [[Back to Contents]](#doc-eng)

Languages|File Encodings|Auto-detection
---------|--------------|:------------:
All Languages|UTF-8 without BOM   |✔
All Languages|UTF-8 with BOM      |✔
All Languages|UTF-16 with BOM     |✔
All Languages|UTF-16BE without BOM|✖
All Languages|UTF-16LE without BOM|✖
All Languages|UTF-32 with BOM     |✖
All Languages|UTF-32BE without BOM|✖
All Languages|UTF-32LE without BOM|✖
All Languages|UTF-7               |✖
All Languages|CP65001             |✖
Arabic|CP720        |✖
Arabic|CP864        |✖
Arabic|ISO-8859-6   |✔
Arabic|Mac OS Arabic|✖
Arabic|Windows-1256 |✔
Baltic Languages|CP775       |✖
Baltic Languages|ISO-8859-13 |✖
Baltic Languages|Windows-1257|✖
Celtic Languages|ISO-8859-14|✖
Central European|CP852                  |✔
Central European|ISO-8859-2             |✔
Central European|Mac OS Central European|✔
Central European|Windows-1250           |✔
Chinese              |GB18030   |✔
Chinese              |GBK       |✖
Chinese (Simplified) |GB2312    |✖
Chinese (Simplified) |HZ        |✔
Chinese (Traditional)|Big-5     |✔
Chinese (Traditional)|Big5-HKSCS|✖
Chinese (Traditional)|CP950     |✖
Croatian|Mac OS Croatian|✖
Cyrillic|CP855          |✔
Cyrillic|CP866          |✔
Cyrillic|ISO-8859-5     |✔
Cyrillic|Mac OS Cyrillic|✔
Cyrillic|Windows-1251   |✔
English|ASCII     |✔
English|EBCDIC 037|✖
English|CP437     |✖
Esperanto/Maltese|ISO-8859-3|✔
European|HP Roman-8|✖
French|CP863|✖
German|EBCDIC 273|✖
Greek|CP737       |✖
Greek|CP869       |✖
Greek|CP875       |✖
Greek|ISO-8859-7  |✔
Greek|Mac OS Greek|✖
Greek|Windows-1253|✔
Hebrew|CP856       |✖
Hebrew|CP862       |✖
Hebrew|EBCDIC 424  |✖
Hebrew|ISO-8859-8  |✔
Hebrew|Windows-1255|✔
Icelandic|CP861           |✖
Icelandic|Mac OS Icelandic|✖
Japanese|CP932           |✔
Japanese|EUC-JP          |✔
Japanese|EUC-JIS-2004    |✖
Japanese|EUC-JISx0213    |✖
Japanese|ISO-2022-JP     |✔
Japanese|ISO-2022-JP-1   |✖
Japanese|ISO-2022-JP-2   |✖
Japanese|ISO-2022-JP-2004|✖
Japanese|ISO-2022-JP-3   |✖
Japanese|ISO-2022-JP-EXT |✖
Japanese|Shift_JIS       |✔
Japanese|Shift_JIS-2004  |✖
Japanese|Shift_JISx0213  |✖
Kazakh|KZ-1048|✖
Kazakh|PTCP154|✖
Korean|EUC-KR     |✖
Korean|ISO-2022-KR|✔
Korean|JOHAB      |✖
Korean|UHC        |✔
Nordic Languages|CP865      |✖
Nordic Languages|ISO-8859-10|✔
North European|ISO-8859-4|✔
Persian/Urdu|Mac OS Farsi|✖
Portuguese|CP860|✖
Romanian|Mac OS Romanian|✖
Russian|KOI8-R|✔
South-Eastern European|ISO-8859-16|✔
Tajik|KOI8-T|✖
Thai|CP874      |✖
Thai|ISO-8859-11|✖
Thai|TIS-620    |✔
Turkish|CP857         |✖
Turkish|EBCDIC 1026   |✖
Turkish|ISO-8859-9    |✔
Turkish|Mac OS Turkish|✖
Turkish|Windows-1254  |✖
Ukrainian|CP1125|✖
Ukrainian|KOI8-U|✖
Urdu|CP1006|✖
Vietnamese|CP1258|✖
Western European|EBCDIC 500  |✖
Western European|CP850       |✖
Western European|CP858       |✖
Western European|CP1140      |✖
Western European|ISO-8859-1  |✔
Western European|ISO-8859-15 |✔
Western European|Mac OS Roman|✖
Western European|Windows-1252|✔

<span id="doc-eng-4-4"></span>
### 4.4 Supported Measures [[Back to Contents]](#doc-eng)

<span id="doc-eng-4-4-1"></span>
#### 4.4.1 Measures of Dispersion & Adjusted Frequency [[Back to Contents]](#doc-eng)

The dispersion and adjusted frequency of a word in each file is calculated by first dividing each file into **n** (5 by default) sub-sections and the frequency of the word in each part is counted, which are denoted by **F₁**, **F₂**, **F₃** ... **Fn**. The total frequency of the word in each file is denoted by **F**. The mean value of the frequencies over all sub-sections is denoted by ![F-bar](/doc/measures/f_bar.gif).

Then, the dispersion and adjusted frequency of the word will be calcuated as follows:

<!--
Juilland's D:
    \begin{align*}
        CV &= \frac{\sum_{i = 1}^{n}(F_{i} - \bar{F})^{2}}{\bar{F}} \\
        \text{D} &= \frac{1 - CV}{\sqrt{i - 1}}
    \end{align*}

Carroll's D₂:
    \begin{align*}
        H &= \ln F - \frac{\sum_{i = 1}^{n} \times \ln F_{i}}{F} \\
        \text{D}_{2} &= \frac{H}{\ln n}
    \end{align*}

Lyne's D₃:
    \begin{align*}
        \chi^{2} &= \sum_{i = 1}^{n}\frac{(F_{i} - \frac{F}{i})^{2}}{\frac{F}{i}} \\
        \text{D}_{3} &= \frac{1 - \chi^{2}}{4F}
    \end{align*}

Rosengren's S:
    \begin{align*}
        KF &= \frac{1}{n}(\sum_{i = 1}^{n}\sqrt{F_{i}})^{2} \\
        \text{S} &= \frac{KF}{F}
    \end{align*}

Zhang's Distributional Consistency:
    \begin{align*}
        \text{DC} &= \frac{(\frac{\sum_{i = 1}^{n}\sqrt{F_{i}}}{n})^{2}}{\frac{\sum_{i = 1}^{n}}{n}}
    \end{align*}

Gries's DP:
    \begin{align*}
        \text{DP} &= \frac{1}{2}\sum_{i = 1}^{n}|\frac{F_{i}}{F} - \frac{1}{n}|
    \end{align*}

Gries's DPnorm:
    \begin{align*}
        DP &= \frac{1}{2}\sum_{i = 1}^{n}|\frac{F_{i}}{F} - \frac{1}{n}| \\
        \text{DP}_\text{norm} &= \frac{DP}{1 - \frac{1}{n}}
    \end{align*}
-->

Measures of Dispersion|Formulas
----------------------|-------
Juilland's D   [[1]](#doc-eng-supported-measures-works-cited-1)|![Juilland's D](/doc/measures/dispersion/juillands_d.gif)
Carroll's D₂   [[2]](#doc-eng-supported-measures-works-cited-2)|![Carroll's D₂](/doc/measures/dispersion/carrolls_d2.gif)
Lyne's D₃      [[3]](#doc-eng-supported-measures-works-cited-3)|![Lyne's D₃](/doc/measures/dispersion/lynes_d3.gif)
Rosengren's S  [[4]](#doc-eng-supported-measures-works-cited-4)|![Rosengren's S](/doc/measures/dispersion/rosengrens_s.gif)
Zhang's Distributional Consistency [[5]](#doc-eng-supported-measures-works-cited-5)|![Zhang's Distributional Consistency](/doc/measures/dispersion/zhangs_distributional_consistency.gif)
Gries's DP     [[6]](#doc-eng-supported-measures-works-cited-6)|![Gries's DP](/doc/measures/dispersion/griess_dp.gif)
Gries's DPnorm [[7]](#doc-eng-supported-measures-works-cited-7)|![Gries's DPnorm](/doc/measures/dispersion/griess_dp_norm.gif)

<!--
Juilland's U:
    \begin{align*}
        CV &= \frac{\sum_{i = 1}^{n}(F_{i} - \bar{F})^{2}}{\bar{F}} \\
        D &= \frac{1 - CV}{\sqrt{i - 1}} \\
        \text{U} &= D \times F
    \end{align*}

Carroll's Um:
    \begin{align*}
        H &= \ln F - \frac{\sum_{i = 1}^{n} \times \ln F_{i}}{F} \\
        D_{2} &= \frac{H}{\ln n} \\
        \text{U}_{m} & = F \times D_{2} + (1 - D_{2}) \times \frac{F}{n}
    \end{align*}

Rosengren's KF:
    \begin{align*}
        \text{KF} &= \frac{1}{n}(\sum_{i = 1}^{n}\sqrt{F_{i}})^{2}
    \end{align*}

Engwall's FM:
    \begin{align*}
        \text{FM} = \frac{F \times R}{n}
    \end{align*}

Kromer's UR:
    \begin{align*}
        \text{U}_\text{R} = \sum_{i = 1}^{n}\psi(F_{i} + 1) + C
    \end{align*}
-->

Measures of Adjusted Frequency|Formulas
----------------------|-------
Juilland's U   [[1]](#doc-eng-supported-measures-works-cited-1)|![Juilland's U](/doc/measures/adjusted_freq/juillands_u.gif)
Carroll's Um   [[2]](#doc-eng-supported-measures-works-cited-2)|![Carroll's Um](/doc/measures/adjusted_freq/carrolls_um.gif)
Rosengren's KF [[4]](#doc-eng-supported-measures-works-cited-4)|![Rosengren's KF](/doc/measures/adjusted_freq/rosengrens_kf.gif)
Engwall's FM   [[8]](#doc-eng-supported-measures-works-cited-8)|![Engwall's FM](/doc/measures/adjusted_freq/engwalls_fm.gif)<br>where **R** is the number of sub-sections in which the word appears at least once
Kromer's UR    [[9]](#doc-eng-supported-measures-works-cited-9)|![Kromer's UR](/doc/measures/adjusted_freq/kromers_ur.gif)<br>where **ψ** is the [digamma function](https://en.wikipedia.org/wiki/Digamma_function), **C** is the [Euler–Mascheroni constant](https://en.wikipedia.org/wiki/Euler%E2%80%93Mascheroni_constant)

<span id="doc-eng-4-4-2"></span>
#### 4.4.2 Tests of Statistical Significance & Measures of Effect Size [[Back to Contents]](#doc-eng)

To calculate the statistical significance, bayes factor and effect size (except **Student's t-test (Two-sample)** and **Mann-Whitney U Test**) for two words in the same file (collocates) or one specific word in two different files (keywords), two contingency tables must be constructed first, one for observed values, the other for expected values.

As for collocates (in *Collocation* and *Colligation*):

Observed Values|Word 1                       |Not Word 1                   |Row Total
--------------:|:---------------------------:|:---------------------------:|:---------------------------:
Word 2         |![o11](/doc/measures/o11.gif)|![o12](/doc/measures/o12.gif)|![o1x](/doc/measures/o1x.gif)
Not Word 2     |![o21](/doc/measures/o21.gif)|![o22](/doc/measures/o22.gif)|![o2x](/doc/measures/o2x.gif)
Column Total   |![ox1](/doc/measures/ox1.gif)|![ox2](/doc/measures/ox2.gif)|![oxx](/doc/measures/oxx.gif)

Expected Values|Word 1                       |Not Word 1
--------------:|:---------------------------:|:---------------------------:
Word 2         |![e11](/doc/measures/e11.gif)|![e12](/doc/measures/e12.gif) 
Not Word 2     |![e21](/doc/measures/e21.gif)|![e22](/doc/measures/e22.gif)

![o11](/doc/measures/o11.gif): Number of occurrences of Word 1 followed by Word 2<br>
![o12](/doc/measures/o12.gif): Number of occurrences of Word 1 followed by any word except Word 2<br>
![o21](/doc/measures/o21.gif): Number of occurrences of any word except Word 1 followed by Word 2<br>
![o22](/doc/measures/o22.gif): Number of occurrences of any word except Word 1 followed by any word except Word 2

As for keywords (in *Keyword*):

Observed Values|Observed File                |Reference File               |Row Total
--------------:|:---------------------------:|:---------------------------:|:---------------------------:
Word *w*       |![o11](/doc/measures/o11.gif)|![o12](/doc/measures/o12.gif)|![o1x](/doc/measures/o1x.gif)
Not Word *w*   |![o21](/doc/measures/o21.gif)|![o22](/doc/measures/o22.gif)|![o2x](/doc/measures/o2x.gif)
Column Total   |![ox1](/doc/measures/ox1.gif)|![ox2](/doc/measures/ox2.gif)|![oxx](/doc/measures/oxx.gif)

Expected Values|Observed File                |Reference File
--------------:|:---------------------------:|:---------------------------:
Word *w*       |![e11](/doc/measures/e11.gif)|![e12](/doc/measures/e12.gif) 
Not Word *w*   |![e21](/doc/measures/e21.gif)|![e22](/doc/measures/e22.gif)

![o11](/doc/measures/o11.gif): Number of occurrences of Word *w* in the observed file<br>
![o12](/doc/measures/o12.gif): Number of occurrences of Word *w* in the reference file<br>
![o21](/doc/measures/o21.gif): Number of occurrences of all words except Word *w* in the observed file<br>
![o22](/doc/measures/o22.gif): Number of occurrences of all words except Word *w* in the reference file

To conduct **Student's t-test (Two-sample)** or **Mann-Whitney U Test** on a specific word, the observed file and the reference file are first divided into **n** (5 by default) sub-sections respectively. Then, the frequencies of the word in each sub-section of the observed file and the reference file are counted and denoted by **FO₁**, **FO₂**, **FO₃** ... **FOn** and **FR₁**, **FR₂**, **FR₃** ... **FRn** respectively. The total frequency of the word in the observed file and the reference file are denoted by **FO** and **FR** respectively. The mean value of the frequencies over all sub-sections of the observed file and the reference file are denoted by ![FO-bar](/doc/measures/fo_bar.gif) and ![FR-bar](/doc/measures/fr_bar.gif) respectively.

<!--
z-score:
    \begin{align*}
        \text{z} = \frac{O_{11} - E_{11}}{\sqrt{E_{11} \times (1 - \frac{E_{11}}{O_{xx}}))}}
    \end{align*}

Student's t-test (One-sample):
    \begin{align*}
        \text{t} = \frac{O_{11} - E_{11}}{\sqrt{O_{11} \times (1 - \frac{O_{11}}{O_{xx}}))}}
    \end{align*}

Student's t-test (Two-sample):
    \begin{align*}
        s_{1} &= \frac{\sum_{i = 1}^{n}(FO_{i} - \bar{FO})^{2}}{n - 1} \\
        s_{2} &= \frac{\sum_{i = 1}^{n}(FR_{i} - \bar{FR})^{2}}{n - 1} \\
        \text{t} &= \frac{\bar{FO} - \bar{FR}}{\sqrt{\frac{s_{1} - s_{2}}{n}}}
    \end{align*}

Pearson's Chi-squared Test:
    \begin{align*}
        \chi^{2} = \sum_{i = 1}^{2} \sum_{j = 1}^{2}\frac{(O_{ij} - E{ij})^{2}}{E_{ij}}
    \end{align*}

Log-likelihood Ratio:
    \begin{align*}
        \text{G} &= 2\sum_{i = 1}^{2} \sum_{j = 1}^{2}(O_{ij} \times \ln \frac{O_{ij}}{E_{ij}})
    \end{align*}
-->

Then the statistical significance, bayes factor and effect size will be calculated as follows:

Tests of Statistical Significance|Formulas
---------------------------------|--------
z-score                       [[10]](#doc-eng-supported-measures-works-cited-10)[[11]](#doc-eng-supported-measures-works-cited-11)|![z-score](/doc/measures/statistical_significance/z_score.gif)
Student's t-test (One-sample) [[12]](#doc-eng-supported-measures-works-cited-12)|![Student's t-test (One-sample)](/doc/measures/statistical_significance/students_t_test_1_sample.gif)
Student's t-test (Two-sample) [[13]](#doc-eng-supported-measures-works-cited-13)|![Student's t-test (Two-sample)](/doc/measures/statistical_significance/students_t_test_2_sample.gif)
Pearson's Chi-squared Test    [[14]](#doc-eng-supported-measures-works-cited-14)[[15]](#doc-eng-supported-measures-works-cited-15)|![Pearson's Chi-squared Test](/doc/measures/statistical_significance/pearsons_chi_squared_test.gif)
Log-likelihood Ratio          [[16]](#doc-eng-supported-measures-works-cited-16)|![Log-likelihood Ratio](/doc/measures/statistical_significance/log_likehood_ratio_test.gif)
Fisher's Exact Test           [[17]](#doc-eng-supported-measures-works-cited-17)|See: [Fisher's exact test - Wikipedia](https://en.wikipedia.org/wiki/Fisher%27s_exact_test#Example)
Mann-Whitney U Test          [[18]](#doc-eng-supported-measures-works-cited-18)|See: [Mann–Whitney U test - Wikipedia](https://en.wikipedia.org/wiki/Mann%E2%80%93Whitney_U_test#Calculations)

<!--
Student's t-test (Two-sample):
    \begin{align*}
        s_{1} &= \frac{\sum_{i = 1}^{n}(FO_{i} - \bar{FO})^{2}}{n - 1} \\
        s_{2} &= \frac{\sum_{i = 1}^{n}(FR_{i} - \bar{FR})^{2}}{n - 1} \\
        t &= \frac{\bar{FO} - \bar{FR}}{\sqrt{\frac{s_{1} - s_{2}}{n}}} \\
        \text{BF} & = t^{2} - \ln n
    \end{align*}

Log-likelihood Ratio:
    \begin{align*}
        G &= 2\sum_{i = 1}^{2} \sum_{j = 1}^{2}(O_{ij} \times \ln \frac{O_{ij}}{E_{ij}}) \\
        \text{BF} &= G - \ln O_{xx}
    \end{align*}
-->

Measures of Bayes Factor|Formulas
------------------------|--------
Student's t-test (Two-sample) [[19]](#doc-eng-supported-measures-works-cited-19)|![Student's t-test (Two-sample)](/doc/measures/bayes_factor/students_t_test_2_sample.gif)
Log-likelihood Ratio          [[19]](#doc-eng-supported-measures-works-cited-19)|![Log-likelihood Ratio](/doc/measures/bayes_factor/log_likehood_ratio_test.gif)

<!--
Pointwise Mutual Information:
    \begin{align*}
        \text{PMI} &= \log_{2} \frac{O_{11}}{E_{11}}
    \end{align*}

Mutual Dependency:
    \begin{align*}
        \text{MD} &= \log_{2} \frac{O_{11}^{2}}{E_{11}}
    \end{align*}

Log-Frequency Biased MD:
    \begin{align*}
        \text{LFMD} &= \log_{2} \frac{O_{11}}{E_{11}} + \log_{2} O_{11}
    \end{align*}

Cubic Association Ratio:
    \begin{align*}
        \text{IM}^{3} &= \log_{2} \frac{O_{11}^{3}}{E_{11}}
    \end{align*}

MI.log-f:
    \begin{align*}
        \text{MI.log-f} &= \log_{2} \frac{O_{11}^{2}}{E_{11}} \times \ln (O_{11} + 1)
    \end{align*}

Mutual Information:
    \begin{align*}
        \text{MI} &= \sum_{i = 1}^{n}\sum_{j = 1}^{n} (\frac{O_{ij}}{O_{xx}} \times \log_{2} \frac{O_{ij}}{E_{ij}})
    \end{align*}

Squared Phi Coefficient:
    \begin{align*}
        \phi^{2} &= \frac{(O_{11}O_{22} - O_{12}O_{21})^{2}}{O_{1x}O_{2x}O_{x1}O_{x2}}
    \end{align*}

Dice's Coefficient:
    \begin{align*}
        \text{DSC} &= \frac{2 \times O_{11}}{O_{1x} + O_{x1}}
    \end{align*}

logDice:
    \begin{align*}
        \text{logDice} &= 14 + \log_{2} \frac{2 \times O_{11}}{O_{1x} + O_{x1}}
    \end{align*}

Mutual Expectation:
    \begin{align*}
        \text{ME} &= O_{11} \times \frac{2 \times O_{11}}{O_{1x} + O_{x1}}
    \end{align*}

Jaccard Index:
    \begin{align*}
        \text{J} &= \frac{O_{11}}{O_{11} + O_{12} + O_{21}}
    \end{align*}

Minimum Sensitivity:
    \begin{align*}
        \text{S} &= \min \{\frac{O_{11}}{O_{1x}} \text{, } \frac{O_{11}}{O_{x1}}\}
    \end{align*}

Poisson Collocation Measure:
    \begin{align*}
        \text{sig} &= \frac{O_{11}(\ln O_{11} - \ln E_{11} - 1)}{\ln O_{xx}}
    \end{align*}

Kilgarriff's Ratio:
    \begin{align*}
        \text{Kilgarriff's Ratio} &= \frac{\frac{O_{11}}{O_{11} + O_{21}} \times 1000000 + \alpha}{\frac{O_{12}}{O_{12} + O_{22}} \times 1000000 + \alpha}
    \end{align*}

Odds Ratio:
    \begin{align*}
        \text{Odd's Ratio} &= \frac{O_{11} \times O_{22}}{O_{12} \times O_{21}}
    \end{align*}

Log Ratio:
    \begin{align*}
        \text{Log Ratio} &= \log_{2} \frac{\frac{O_{11}}{O_{x1}}}{\frac{O_{12}}{O_{x2}}}
    \end{align*}

Difference Coefficient:
    \begin{align*}
        \text{Difference Coefficient} &= \frac{\frac{O_{11}}{O_{x1}} - \frac{O_{12}}{O_{x2}}}{\frac{O_{11}}{O_{x1}} + \frac{O_{12}}{O_{x2}}}
    \end{align*}

%DIFF:
    \begin{align*}
        \text{\%DIFF} &= \frac{(\frac{O_{11}}{O_{x1}} - \frac{O_{12}}{O_{x2}}) \times 100}{\frac{O_{12}}{O_{x2}}}
    \end{align*}
-->

Measures of Effect Size|Formulas
-----------------------|--------
Pointwise Mutual Information [[20]](#doc-eng-supported-measures-works-cited-20)|![Pointwise Mutual Information](/doc/measures/effect_size/pmi.gif)
Mutual Dependency            [[21]](#doc-eng-supported-measures-works-cited-21)|![Mutual Dependency](/doc/measures/effect_size/md.gif)
Log-Frequency Biased MD      [[21]](#doc-eng-supported-measures-works-cited-21)|![Log-Frequency Biased MD](/doc/measures/effect_size/lfmd.gif)
Cubic Association Ratio      [[22]](#doc-eng-supported-measures-works-cited-22)[[23]](#doc-eng-supported-measures-works-cited-23)|![Cubic Association Ratio](/doc/measures/effect_size/im3.gif)
MI.log-f                     [[24]](#doc-eng-supported-measures-works-cited-24)[[25]](#doc-eng-supported-measures-works-cited-25)|![MI.log-f](/doc/measures/effect_size/mi_log_f.gif)
Mutual Information           [[26]](#doc-eng-supported-measures-works-cited-26)|![Mutual Information](/doc/measures/effect_size/mi.gif)
Squared Phi Coefficient      [[27]](#doc-eng-supported-measures-works-cited-27)|![Squared Phi Coefficient](/doc/measures/effect_size/squared_phi_coeff.gif)
Dice's Coefficient           [[28]](#doc-eng-supported-measures-works-cited-28)|![Dice's Coefficient](/doc/measures/effect_size/dices_coeff.gif)
logDice                      [[29]](#doc-eng-supported-measures-works-cited-29)|![logDice](/doc/measures/effect_size/log_dice.gif)
Mutual Expectation           [[30]](#doc-eng-supported-measures-works-cited-30)|![Mutual Expectation](/doc/measures/effect_size/me.gif)
Jaccard Index                [[24]](#doc-eng-supported-measures-works-cited-24)|![Jaccard Index](/doc/measures/effect_size/jaccard_index.gif)
Minimum Sensitivity          [[31]](#doc-eng-supported-measures-works-cited-34)|![Minimum Sensitivity](/doc/measures/effect_size/min_sensitivity.gif)
Poisson Collocation Measure  [[32]](#doc-eng-supported-measures-works-cited-32)|![Poisson Collocation Measure](/doc/measures/effect_size/poisson_collocation_measure.gif)
Kilgarriff's Ratio           [[33]](#doc-eng-supported-measures-works-cited-33)|![Kilgarriff's Ratio](/doc/measures/effect_size/kilgarriffs_ratio.gif)<br>where **α** is the smoothing parameter, which is 1 by default.<br>You can change the value of **α** via **Menu → Preferences → Settings → Measures →<br>Effect Size → Kilgarriff's Ratio → Smoothing Parameter**.
Odds Ratio                   [[34]](#doc-eng-supported-measures-works-cited-34)|![Odds Ratio](/doc/measures/effect_size/odds_ratio.gif)
Log Ratio                    [[35]](#doc-eng-supported-measures-works-cited-35)|![Log Ratio](/doc/measures/effect_size/log_ratio.gif)
Difference Coefficient       [[14]](#doc-eng-supported-measures-works-cited-14)[[36]](#doc-eng-supported-measures-works-cited-36)|![Difference Coefficient](/doc/measures/effect_size/diff_coeff.gif)
%DIFF                        [[37]](#doc-eng-supported-measures-works-cited-37)|![%DIFF](/doc/measures/effect_size/pct_diff.gif)

<span id="doc-eng-5"></span>
## 5 References [[Back to Contents]](#doc-eng)

<span id="doc-eng-supported-measures-works-cited-1"></span>
[1] Juilland, A., & Chang-Rodriguez, E. (1964). Frequency dictionary of spanish words. Mouton.<br>
<span id="doc-eng-supported-measures-works-cited-2"></span>
[2] Carroll, J. B. (1970). An alternative to Juilland’s usage coefficient for lexical frequencies and a proposal for a standard frequency index. *Computer Studies in the Humanities and Verbal Behaviour*, *3*(2), 61–65. https://doi.org/10.1002/j.2333-8504.1970.tb00778.x<br>
<span id="doc-eng-supported-measures-works-cited-3"></span>
[3] Lyne, A. A. (1985). Dispersion. In *The vocabulary of French business correspondence: Word frequencies, collocations, and problems of lexicometric method* (pp. 101–124). Slatkine/Champion.<br>
<span id="doc-eng-supported-measures-works-cited-4"></span>
[4] Rosengren, I. (1971). The quantitative concept of language and its relation to the structure of frequency dictionaries. *Études de linguistique appliquée*, *1*, 103–127.<br>
<span id="doc-eng-supported-measures-works-cited-5"></span>
[5] Zhang, H., Huang, C., & Yu, S. (2004). Distributional consistency: As a general method for defining a core lexicon. In M. T. Lino, M. F. Xavier, F. Ferreira, R. Costa, & R. Silva (Eds.), *Proceedings of Fourth International Conference on Language Resources and Evaluation* (pp. 1119–1122). European Language Resources Association.<br>
<span id="doc-eng-supported-measures-works-cited-6"></span>
[6] Gries, S. T. (2008). Dispersions and adjusted frequencies in corpora. *International Journal of Corpus Linguistics*, *13*(4), 403–437. https://doi.org/10.1075/ijcl.13.4.02gri<br>
<span id="doc-eng-supported-measures-works-cited-7"></span>
[7] Lijffijt, J., & Gries, S. T. (2012). Correction to Stefan Th. Gries’ “dispersions and adjusted frequencies in corpora” *International Journal of Corpus Linguistics*, *17*(1), 147–149. https://doi.org/10.1075/ijcl.17.1.08lij<br>
<span id="doc-eng-supported-measures-works-cited-8"></span>
[8] Engwall, G. (1974). Fréquence et distribution du vocabulaire dans un choix de romans français [Unpublished doctoral dissertation]. Stockholm University.<br>
<span id="doc-eng-supported-measures-works-cited-9"></span>
[9] Kromer, V. (2003). A usage measure based on psychophysical relations. *Journal of Quatitative Linguistics*, *10*(2), 177–186. https://doi.org/10.1076/jqul.10.2.177.16718<br>
<span id="doc-eng-supported-measures-works-cited-10"></span>
[10] Dennis, S. F. (1964). The construction of a thesaurus automatically from a sample of text. In M. E. Stevens, V. E. Giuliano, & L. B. Heilprin (Eds.), *Proceedings of the symposium on statistical association methods for mechanized documentation* (pp. 61–148). National Bureau of Standards.<br>
<span id="doc-eng-supported-measures-works-cited-11"></span>
[11] Berry-Rogghe, G. L. M. (1973). The computation of collocations and their relevance in lexical studies. In A. J. Aiken, R. W. Bailey, & N. Hamilton-Smith (Eds.), *The computer and literary studies* (pp. 103–112). Edinburgh University Press.<br>
<span id="doc-eng-supported-measures-works-cited-12"></span>
[12] Church, K., Gale, W, Hanks P, & Hindle D. (1991). Using statistics in lexical analysis. In U. Zernik (Ed.), *Lexical acquisition: Exploiting on-line resources to build a lexicon* (pp. 115–164). Psychology Press.<br>
<span id="doc-eng-supported-measures-works-cited-13"></span>
[13] Paquot, M., & Bestgen, Y. (2009). Distinctive words in academic writing: A comparison of three statistical tests for keyword extraction *Language and Computers*, *68*, 247–269.<br>
<span id="doc-eng-supported-measures-works-cited-14"></span>
[14] Hofland, K., & Johanson, S. (1982). *Word frequencies in British and American English*. Norwegian Computing Centre for the Humanities.<br>
<span id="doc-eng-supported-measures-works-cited-15"></span>
[15] Oakes, M. P. (1998). *Statistics for Corpus Linguistics*. Edinburgh University Press.<br>
<span id="doc-eng-supported-measures-works-cited-16"></span>
[16] Dunning, T. E. (1993). Finding structure in text, genome and other symbolic sequences. *Computational Linguistics*, *19*(1), 61–74.<br>
<span id="doc-eng-supported-measures-works-cited-17"></span>
[17] Pedersen, T. (1996). Fishing for exactness. In T. Winn (Ed.), *Proceedings of the Sixth Annual South-Central Regional SAS Users' Group Conference* (pp. 188-200). The South–Central Regional SAS Users' Group.<br>
<span id="doc-eng-supported-measures-works-cited-18"></span>
[18] Kilgarriff, A. (2001). Comparing corpora. *International Journal of Corpus Linguistics*, *6*(1), 232–263. https://doi.org/10.1075/ijcl.6.1.05kil<br>
<span id="doc-eng-supported-measures-works-cited-19"></span>
[19] Wilson, A. (2013). Embracing Bayes Factors for key item analysis in corpus linguistics. In M. Bieswanger, & A. Koll-Stobbe (Eds.), *New Approaches to the Study of Linguistic Variability* (pp. 3–11). Peter Lang.<br>
<span id="doc-eng-supported-measures-works-cited-20"></span>
[20] Church, K. W., & Hanks, P. (1990). Word association norms, mutual information, and lexicography. *Computational Linguistics*, *16*(1), 22–29.<br>
<span id="doc-eng-supported-measures-works-cited-21"></span>
[21] Thanopoulos, A, Fakotakis, N., Kokkinakis, G. (2002). Comparative evaluation of collocation extraction metrics. In M. G. González, & C. P. S. Araujo (Eds.), *Proceedings of the Third International Conference on Language Resources and Evaluation* (pp. 620–625). European Language Resources Association.<br>
<span id="doc-eng-supported-measures-works-cited-22"></span>
[22] Daille, B. (1994). Approche mixte pour l'extraction automatique de terminologie: statistiques lexicales et filtres linguistiques [Doctoral thesis, Université Paris 7]. Béatrice Daille. http://www.bdaille.com/index.php?option=com_docman&task=doc_download&gid=8&Itemid=<br>
<span id="doc-eng-supported-measures-works-cited-23"></span>
[23] Daille, B. (1995). Combined approach for terminology extraction: Lexical statistics and linguistic filtering. UCREL technical papers (Vol. 5). Lancaster University.<br>
<span id="doc-eng-supported-measures-works-cited-24"></span>
[24] Lexical Computing Ltd. (2015, July 8). Statistics used in Sketch Engine. Retrieved November 26, 2018 from https://www.sketchengine.eu/documentation/statistics-used-in-sketch-engine/<br>
<span id="doc-eng-supported-measures-works-cited-25"></span>
[25] Kilgarriff, A., & Tugwell, D. (2002). WASP-bench – an MT lexicographers' workstation supporting state-of-the-art lexical disambiguation. In *Proceedings of the 8th Machine Translation Summit* (pp. 187–190). European Association for Machine Translation.<br>
<span id="doc-eng-supported-measures-works-cited-26"></span>
[26] Dunning, T. E. (1998). Finding structure in text, genome and other symbolic sequences [Doctoral dissertation, University of Sheffield]. arXiv. arxiv.org/pdf/1207.1847.pdf<br>
<span id="doc-eng-supported-measures-works-cited-27"></span>
[27] Church, K. W., & Gale, W. A. (1991, September 29–October 1). Concordances for parallel text [Paper presentation]. Using Corpora: Seventh Annual Conference of the UW Centre for the New OED and Text Research, St. Catherine's College, Oxford, United Kingdom.<br>
<span id="doc-eng-supported-measures-works-cited-28"></span>
[28] Smadja, F., McKeown, K. R., & Hatzivassiloglou, V. (1996). Translating collocations for bilingual lexicons: A statistical approach. *Computational Linguistics*, *22*(1), pp. 1–38.<br>
<span id="doc-eng-supported-measures-works-cited-29"></span>
[29] Rychlý, P. (2008). A lexicographyer-friendly association score. In P. Sojka, & A. Horák (Eds.), *Proceedings of Second Workshop on Recent Advances in Slavonic Natural Languages Processing*. Masaryk University<br>
<span id="doc-eng-supported-measures-works-cited-30"></span>
[30] Dias, G., Guilloré, S., & Pereira Lopes, J. G. (1999). Language independent automatic acquisition of rigid multiword units from unrestricted text corpora. In A. Condamines, C. Fabre, & M. Péry-Woodley (Eds.), *TALN'99: 6ème Conférence Annuelle Sur le Traitement Automatique des Langues Naturelles* (pp. 333–339). TALN.<br>
<span id="doc-eng-supported-measures-works-cited-31"></span>
[31] Pedersen, T. (1998). Dependent bigram identification. In *Proceedings of the Fifteenth National Conference on Artificial Intelligence* (p. 1197). AAAI Press.<br>
<span id="doc-eng-supported-measures-works-cited-32"></span>
[32] Quasthoff, U, & Wolff, C. (2002). The poisson collocation measure and its applications. *Proceedings of 2nd International Workshop on Computational Approaches to Collocations*. IEEE.<br>
<span id="doc-eng-supported-measures-works-cited-33"></span>
[33] Kilgarriff, A. (2009). Simple maths for keywords. In M. Mahlberg, V. González-Díaz, & C. Smith (Eds.), *Proceedings of the Corpus Linguistics Conference 2009* (p. 171). University of Liverpool.<br>
<span id="doc-eng-supported-measures-works-cited-34"></span>
[34] Pojanapunya, P., & Todd, R. W. (2016). Log-likelihood and odds ratio keyness statistics for different purposes of keyword analysis. *Corpus Linguistics and Lingustic Theory*, *15*(1), pp. 133–167. https://doi.org/10.1515/cllt-2015-0030<br>
<span id="doc-eng-supported-measures-works-cited-35"></span>
[35] Hardie, A. (2014, April 28). Log ratio: An informal introduction. ESRC Centre for Corpus Approaches to Social Science (CASS). http://cass.lancs.ac.uk/log-ratio-an-informal-introduction/.<br>
<span id="doc-eng-supported-measures-works-cited-36"></span>
[36] Gabrielatos, C. (2018). Keyness analysis: Nature, metrics and techniques. In C. Taylor & A. Marchi (Eds.), *Corpus approaches to discourse: A critical review* (pp. 225–258). Routledge.<br>
<span id="doc-eng-supported-measures-works-cited-37"></span>
[37] Gabrielatos, C., & Marchi, A. (2012, September 13–14). Keyness: Appropriate metrics and practical issues [Conference session]. CADS International Conference 2012, University of Bologna, Italy.

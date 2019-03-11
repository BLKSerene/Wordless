<!--
# Wordless: README
#
# Copyright (C) 2018-2019  Ye Lei (叶磊))
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
-->

<div align="center"><img src="/doc/wordless_logo.png" alt="logo"></div>

---
Wordless is an integrated corpus tool with multi-language support for the study of language, literature and translation designed and developed by Ye Lei (叶磊), MA student in interpreting studies at Shanghai International Studies University (上海外国语大学).

## License
    Copyright (C) 2018-2019  Ye Lei (叶磊)

    This project is licensed under GNU GPLv3.
    For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt

    All other rights reserved.

## Citing
If you publish work that uses Wordless, please cite as follows.

MLA (8th Edition):

    Ye Lei. Wordless, version 1.0, 2019, https://github.com/BLKSerene/Wordless.

APA (6th Edition):

    Ye, L. (2019) Wordless (Version 1.0) [Computer Software]. Retrieved from https://github.com/BLKSerene/Wordless

GB (GB/T 7714—2015):

    叶磊. Wordless version 1.0[CP]. (2019). https://github.com/BLKSerene/Wordless.

<span id="doc"></span>
## Documentation
[English Documentation](#doc-eng)
* [Supported Languages](#doc-eng-supported-langs)
* [Supported File Types](#doc-eng-supported-file-types)
* [Supported Measures](#doc-eng-supported-measures)
* [Main Window](#doc-eng-main-window)
* [File Area](#doc-eng-file-area)
* [Overview](#doc-eng-overview)
* [Concordancer](#doc-eng-concordancer)

[中文文档](#doc-zho)

## Need Help?
If you encounter a problem, find a bug or require any further information, feel free to ask questions, submit bug reports or provide feedback by [creating an issue](https://github.com/BLKSerene/Wordless/issues/new) on Github if you fail to find the answer by searching [existing issues](https://github.com/BLKSerene/Wordless/issues) first.

If you need to post sample texts or other information that cannot be shared or you do not want to share publicly, you may [send me an email](mailto:blkserene@gmail.com).

Home Page: https://github.com/BLKSerene/Wordless<br>
Documentation: https://github.com/BLKSerene/Wordless#documentation<br>
Email: blkserene@gmail.com<br>
[WeChat](https://www.wechat.com/en/) Official Account: Wordless<br>

**Important Note**: I CANNOT GUARANTEE that all emails will always be checked or replied in time. I WILL NOT REPLY to irrelevant emails and I reserve the right to BLOCK AND/OR REPORT people who send me spam emails.

## Contributing
If you have an interest in helping the development of Wordless, you may contribute bug fixes, enhancements or new features by [creating a pull request](https://github.com/BLKSerene/Wordless/pulls) on Github.

Besides, you may contribute by submitting enhancement proposals or feature requests, write tutorials or [Github Wiki](https://github.com/BLKSerene/Wordless/wiki) for Wordless, or helping me translate Wordless and its documentation to other languages.

## Donating
If you would like to support the development of Wordless, you may donate via PayPal, Alipay or WeChat.

PayPal|Alipay|WeChat
------|------|------
[![PayPal](/src/imgs/donating_paypal.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=V2V54NYE2YD32)|![Alipay](/src/imgs/donating_alipay.png)|![WeChat](/src/imgs/donating_wechat.png)

**Important Note**: I WILL NOT PROVIDE refund services, private email/phone support, information concerning my social media, gurantees on bug fixes, enhancements, new features or new releases of Wordless, invoices, receipts or detailed weekly/monthly/yearly/etc. spending report for donation.

## Acknowledgments
Wordless stands on the shoulders of giants. Thus, I would like to extend my thanks to the following open-source projects:

### General
1. [Python](https://www.python.org/) by Guido van Rossum, Python Software Foundation
2. [PyQt](https://www.riverbankcomputing.com/software/pyqt/intro) by Riverbank Computing Limited

### Natural Language Processing
1. [jieba](https://github.com/fxsjy/jieba) by Sun Junyi
2. [nagisa](https://github.com/taishi-i/nagisa) by Taishi Ikeda (池田大志)
3. [NLTK](http://www.nltk.org/) by Steven Bird, Liling Tan
4. [pybo](https://github.com/Esukhia/pybo) by Hélios Drupchen Hildt
5. [pymorphy2](https://github.com/kmike/pymorphy2/) by Mikhail Korobov
6. [PyThaiNLP](https://github.com/PyThaiNLP/pythainlp) by Wannaphong Phatthiyaphaibun (วรรณพงษ์ ภัททิยไพบูลย์)
7. [SacreMoses](https://github.com/alvations/sacremoses) by Liling Tan
8. [spaCy](https://spacy.io/) by Matthew Honnibal, Ines Montani
9. [Underthesea](https://github.com/undertheseanlp/underthesea) by Vu Anh

### Plotting
1. [Matplotlib](https://matplotlib.org/) by Matplotlib Development Team
2. [wordcloud](https://amueller.github.io/word_cloud/) by Andreas Christian Mueller

### Miscellaneous
1. [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) by Leonard Richardson
2. [cChardet](https://github.com/PyYoshi/cChardet) by Yoshihiro Misawa
3. [chardet](https://github.com/chardet/chardet) by Daniel Blanchard
4. [langdetect](https://github.com/Mimino666/langdetect) by Michal Mimino Danilak
5. [langid.py](https://github.com/saffsd/langid.py) by Marco Lui
6. [lxml](https://lxml.de/) by Stefan Behnel
7. [NumPy](http://www.numpy.org/) by NumPy Developers
8. [openpyxl](https://openpyxl.readthedocs.io/en/stable/) by Eric Gazoni, Charlie Clark
9. [PyInstaller](http://www.pyinstaller.org/) by Hartmut Goebel
10. [python-docx](https://github.com/python-openxml/python-docx) by Steve Canny
11. [requests](http://python-requests.org) by Kenneth Reitz
12. [SciPy](https://www.scipy.org/) by SciPy Developers
13. [xlrd](https://github.com/python-excel/xlrd) by Stephen John Machin

### Data
1. [grk-stoplist](https://github.com/pharos-alexandria/grk-stoplist) by Annette von Stockhausen
2. [lemmalist-greek](https://github.com/stenskjaer/lemmalist-greek) by Michael Stenskjær Christensen
3. [Lemmatization Lists](https://github.com/michmech/lemmatization-lists) by Michal Boleslav Měchura
4. [Stopwords ISO](https://github.com/stopwords-iso/stopwords-iso) by Gene Diaz

<span id="doc-eng"></span>
## Documentation - English
<span id="doc-eng-supported-langs"></span>
### Supported Languages [[Back to Contents]](#doc)
Languages|Sentence Tokenization|Word Tokenization|Word Detokenization|POS Tagging|Lemmatization|Stop Words
:-------:|:-------------------:|:---------------:|:-----------------:|:---------:|:-----------:|:--------:
Afrikaans            |⭕️ |✔|⭕️ |✖️|✖️|✔️
Albanian             |⭕️ |✔|⭕️ |✖️|✖️|✔️
Arabic               |⭕️ |✔️|⭕️ |✖️|✖️|✔️
Armenian             |⭕️ |⭕️ |⭕️ |✖️|✖️|✔️
Asturian             |⭕️ |⭕️ |⭕️ |✖️|✔️|✖️
Azerbaijani          |⭕️ |⭕️ |⭕️ |✖️|✖️|✔️
Basque               |⭕️ |⭕️ |⭕️ |✖️|✖️|✔️
Bengali              |⭕️ |✔️|⭕️ |✖️|✖️|✖️
Breton               |⭕️ |⭕️ |⭕️ |✖️|✖️|✔️
Bulgarian            |⭕️ |✔️|⭕️ |✖️|✔️|✔️
Catalan              |⭕️ |✔️|✔️|✖️|✔️|✔️
Chinese (Simplified) |✔|✔️|✔️|✔️|✖️|✔️
Chinese (Traditional)|✔|✔️|✔️|✔️|✖️|✔️
Croatian             |⭕️ |✔️|⭕️ |✖️|✖️|✔️
Czech                |✔|✔️|✔️|✖️|✔️|✔️
Danish               |✔|✔️|⭕️ |✖️|✖️|✔️
Dutch                |✔|✔️|✔️|✔️|✔️|✔️
English              |✔|✔️|✔️|✔️|✔️|✔️
Esperanto            |⭕️ |⭕️ |⭕️ |✖️|✖️|✔️
Estonian             |✔|⭕️ |⭕️ |✖️|✔️|✔️
Finnish              |✔|✔️|✔️|✖️|✖️|✔️
French               |✔|✔️|✔️|✔️|✔️|✔️
Galician             |⭕️ |⭕️ |⭕️ |✖️|✔️|✔️
German               |✔|✔️|✔️|✔️|✔️|✔️
Greek (Ancient)      |⭕️ |⭕️ |⭕️ |✖️|✔️|✔️
Greek (Modern)       |✔|✔️|✔️|✔️|✔️|✔️
Hausa                |⭕️ |⭕️ |⭕️ |✖️|✖️|✔️
Hebrew               |⭕️ |✔️|⭕️ |✖️|✖️|✔️
Hindi                |⭕️ |✔️|⭕️ |✖️|✖️|✔️
Hungarian            |⭕️ |✔️|✔️|✖️|✔️|✔️
Icelandic            |⭕️ |✔️|✔️|✖️|✖️|✔️
Indonesian           |⭕️ |✔️|⭕️ |✖️|✖️|✔️
Irish                |⭕️ |✔️|⭕️ |✖️|✔️|✔️
Italian              |✔|⭕️ |⭕️ |✔️|✔️|✔️
Japanese             |✔|⭕️ |✔️|✔️|✖️|✔️
Kannada              |⭕️ |✔️|⭕️ |✖️|✖️|✔️
Kazakh               |⭕️ |⭕️ |⭕️ |✖️|✖️|✔️
Korean               |⭕️ |⭕️ |⭕️ |✖️|✖️|✔️
Kurdish              |⭕️ |⭕️ |⭕️ |✖️|✖️|✔️
Latin                |⭕️ |⭕️ |⭕️ |✖️|✖️|✔️
Latvian              |⭕️ |✔️|✔️|✖️|✖️|✔️
Lithuanian           |⭕️ |✔️|⭕️ |✖️|✖️|✔️
Malay                |⭕️ |⭕️ |⭕️ |✖️|✖️|✔️
Manx                 |⭕️ |⭕️ |⭕️ |✖️|✔️|✖️
Marathi              |⭕️ |⭕️ |⭕️ |✖️|✖️|✔️
Nepali               |⭕️ |⭕️ |⭕️ |✖️|✖️|✔️
Norwegian Bokmål     |✔|✔️|⭕️ |✖️|✖️|✔️
Norwegian Nynorsk    |✔|⭕️ |⭕️ |✖️|✖️|✔️
Persian              |⭕️ |✔️|⭕️ |✖️|✔️|✔️
Polish               |✔|✔️|✔️|✖️|✖️|✔️
Portuguese           |✔|✔️|✔️|✔️|✔️|✔️
Romanian             |⭕️ |✔️|✔️|✖️|✔️|✔️
Russian              |⭕️ |✔️|✔️|✔️|✔️|✔️
Scottish Gaelic      |⭕️ |⭕️ |⭕️ |✖️|✔️|✖️
Sinhala              |⭕️ |✔️|⭕️ |✖️|✖️|✔️
Slovak               |⭕️ |✔️|✔️|✖️|✔️|✔️
Slovenian            |✔|✔️|✔️|✖️|✔️|✔️
Sotho (Southern)     |⭕️ |⭕️ |⭕️ |✖️|✖️|✔️
Spanish              |✔|✔️|✔️|✔️|✔️|✔️
Swahili              |⭕️ |⭕️ |⭕️ |✖️|✖️|✔️
Swedish              |✔|✔️|✔️|✖️|✔️|✔️
Tagalog              |⭕️ |✔️|⭕️ |✖️|✖️|✔️
Tajik                |⭕️ |✔️|⭕️ |✖️|✖️|✖️
Tamil                |⭕️ |✔️|✔️|✖️|✖️|✔️
Tatar                |⭕️ |✔️|⭕️ |✖️|✖️|✔️
Telugu               |⭕️ |✔️|⭕️ |✖️|✖️|✔️
Thai                 |✔|✔️|✔️|✔️|✖️|✔️
Tibetan              |⭕️ |✔️|✔️|✔️|✔️|✖️
Turkish              |✔|✔️|⭕️ |✖️|✖️|✔️
Ukrainian            |⭕️ |✔️|⭕️ |✔️|✔️|✔️
Urdu                 |⭕️ |✔️|⭕️ |✖️|✖️|✔️
Vietnamese           |✔|✔️|⭕️ |✔️|✖️|✔️
Welsh                |⭕️ |⭕️ |⭕️ |✖️|✔️|✖️
Yoruba               |⭕️ |⭕️ |⭕️ |✖️|✖️|✔️
Zulu                 |⭕️ |⭕️ |⭕️ |✖️|✖️|✔️
Other Languages      |⭕️ |⭕️ |⭕️ |✖️|✖️|✖️

✔: Supported<br>
⭕️: Supported but falls back to the default English tokenizer<br>
✖️: Not supported

<span id="doc-eng-supported-file-types"></span>
### Supported File Types [[Back to Contents]](#doc)
File Types|File Extensions
----------|--------------
Text Files              |\*.txt
Microsoft Word Documents|\*.docx
Microsoft Excel Workbook|\*.xls, \*.xlsx
CSV Files               |\*.csv
HTML Pages              |\*.htm, \*.html
Translation Memory Files|\*.tmx
Lyrics Files            |\*.lrc

\* Microsoft 97-03 Word documents (\*.doc) are not supported.<br>
\* Non-text files will be converted to text files first before being added to the *File Table*. You can check the converted files under folder **Import** at the installation location of *Wordless* on your computer (as for macOS users, right click **Wordless.app**, select **Show Package Contents** and navigate to **Contents/MacOS/Import/**). You can change this location via **Menu → Preferences → Settings → Import → Temporary Files → Default Path**.

<span id="doc-eng-supported-measures"></span>
### Supported Measures [[Back to Contents]](#doc)

#### Measures of Dispersion

The dispersion of a word in each file is calculated by first dividing each file into **n** (5 by default) sub-sections and the frequency of the word in each part is counted, which are denoted by **F₁**, **F₂**, **F₃** ... **Fn**. The total frequency of the word in each file is denoted by **F**. The mean value of the frequencies in all sub-sections is denoted by ![F-bar](https://latex.codecogs.com/gif.latex?%5Cbar%7BF%7D) Then, the dispersion of the word will be calcuated as follows.

<!--
Juilland's D:
    \begin{align*}
        CV &= \frac{\sum_{i = 1}^{n}(F_{i} - \bar{F})^{2}}{\bar{F}} \\
        D &= \frac{1 - CV}{\sqrt{i - 1}}
    \end{align*}

Carroll's D₂:
    \begin{align*}
        H &= \log_{e}F - \frac{\sum_{i = 1}^{n} * \log_{e}F_{i}}{F} \\
        D_{2} &= \frac{H}{\log_{e}n}
    \end{align*}

Lyne's D₃:
    \begin{align*}
        \chi^{2} &= \sum_{i = 1}^{n}\frac{(F_{i} - \frac{F}{i})^{2}}{\frac{F}{i}} \\
        D_{3} &= \frac{1 - \chi^{2}}{4F}
    \end{align*}

Rosengren's S:
    \begin{align*}
        KF &= \frac{1}{n}\sum_{i = 1}^{n}(\sqrt{F_{i}})^{2} \\
        S &= \frac{KF}{F}
    \end{align*}

Zhang's Distributional Consistency:
    \begin{align*}
        DC &= \frac{(\frac{\sum_{i = 1}^{n}\sqrt{F_{i}}}{n})^{2}}{\frac{\sum_{i = 1}^{n}}{n}}
    \end{align*}

Gries's DP:
    \begin{align*}
        DP &= \frac{1}{2}\sum_{i = 1}^{n}|\frac{F_{i}}{F} - \frac{1}{n}|
    \end{align*}

Gries's DPnorm:
    \begin{align*}
        DP &= \frac{1}{2}\sum_{i = 1}^{n}|\frac{F_{i}}{F} - \frac{1}{n}| \\
        DPnorm &= \frac{DP}{1 - \frac{1}{n}}
    \end{align*}
-->

Measures of Dispersion|Formula
----------------------|-------
Juilland's D|![Juilland's D](/doc/measures_dispersion/juillands_d.gif)
Carroll's D₂|![Carroll's D₂](/doc/measures_dispersion/carrolls_d2.gif)
Lyne's D₃|![Lyne's D₃](/doc/measures_dispersion/lynes_d3.gif)
Rosengren's S|![Rosengren's S](/doc/measures_dispersion/rosengrens_s.gif)
Zhang's Distributional Consistency|![Zhang's Distributional Consistency](/doc/measures_dispersion/zhangs_distributional_consistency.gif)
Gries's DP|![Gries's DP](/doc/measures_dispersion/griess_dp.gif)
Gries's DPnorm|![Gries's DPnorm](/doc/measures_dispersion/griess_dp_norm.gif)

<span id="doc-eng-main-window"></span>
### Main Window [[Back to Contents]](#doc)
The main window of *Wordless* is divided into several sections:

1. **Menu Bar**<br>
    
2. **Work Area**:<br>
    The *Work Area* is further divided into the *Resutls Area* on the left side and the *Settings Area* on the right side.<br>
    You can click on the tabs at the top to toggle between different panels.

3. **File Area**:<br>
    The *File Area* is further divided into the *File Table* on the left side and the *Settings Area* on the right side.

4. **Status Bar**:<br>
    You can show/hide the *Status Bar* by checking/unchecking **Menu → Preferences → Show Status Bar**

<span id="doc-eng-file-area"></span>
### File Area [[Back to Contents]](#doc)
In most cases, the first thing to do in *Wordless* is open and select your files to be processed via **Menu → File** or by clicking the buttons residing under the *File Table*.

Files are selected by default after being added to the *File Table*. **Only selected files will be processed by Wordless**. You can drag and drop files around the *File Table* to change their orders, which will be reflected in the results produced by Wordless.

By default, Wordless will try to detect the language, text type and encoding of the file, you should check and make sure that the settings of each and every file is correct. If you do not want Wordless to detect the settings for you and prefer setting them manually, you can change the settings in **Auto-detection Settings** in the *Settings Area*.

1. **Add File(s)**:<br>
    Add one single file or multiple files to the *File Table*.

    \* You can use the **Ctrl** key (**Command** key on macOS) and/or the **Shift** key to select multiple files.

2. **Add Folder**:<br>
    Add all files in the folder to the *File Table*.

    By default, all files in subfolders (and subfolders of subfolders, and so on) will also be added to the *File Table*. If you do not want to add files in subfolders to the *File Table*, uncheck **Folder Settings → Subfolders** in the *Settings Area*.

3. **Reopen Closed File(s)**:<br>
    Add file(s) that are closed the last time back to the *File Table*.

    \* The history of all closed files will be erased upon exit of *Wordless*.

4. **Select All**:<br>
    Select all files in the *File Table*.

5. **Invert Selection**:<br>
    Select all files that are not currently selected and deselect all currently selected files in the *File Table*.

6. **Deselect All**:<br>
    Deselect all files in the *File Table*.

7. **Close Selected**:<br>
    Remove all currently selected files in the *File Table*.

8. **Close All**:<br>
    Remove all files in the *File Table*.

<span id="doc-eng-overview"></span>
### Overview [[Back to Contents]](#doc)
In *Overview*, you can check/compare the language features of different files.

1. **Count of Paragraphs**:<br>
    Number of paragraphs in each file. Each line in the file will be counted as one paragraph. Blank lines and lines containing only spaces, tabs and other invisible characters are ignored.

2. **Count of Sentences**:<br>
    Number of sentences in each file. *Wordless* will automatically apply the built-in sentence tokenizer according to the language of each file in order to calculate the number of sentences in each file. You can change the sentence tokenizer settings via **Menu → Preferences → Settings → Sentence Tokenization → Sentence Tokenizer Settings**.

3. **Count of Tokens**:<br>
    Number of tokens in each file. *Wordless* will automatically apply the built-in word tokenizer according to the language of each file in order to calculate the number of tokens in each file. You can change the word tokenizer settings via **Menu → Preferences → Settings → Word Tokenization → Word Tokenizer Settings**.

    You can tell *Wordless* what should be counted as a "token" by modifying **Token Settings** in the *Settings Area*

4. **Count of Types**:<br>
    Number of token types in each file.

5. **Count of Caracters**:<br>
    Number of single characters in each file. Spaces, tabs and all other invisible characters are ignored.

6. **Type-Token Ratio**:<br>
    Number of token types divided by number of tokens.

7. **Type-Token Ratio (Standardized)**:<br>
    Standardized type-token ratio. Each file will be divided into several sub-sections with each one consisting of 1000 tokens by default and type-token ratio will be calculated for each part. The standardized type-token ratio of each file is then averaged out over all sub-sections. You can change the number of tokens in each sub-section via **Generation Settings → Base of standardized type-token ratio**.

    The last section will be discarded if the number of tokens in it is smaller than the base of standardized type-token ratio in order to prevent the result from being affected by outliers (extreme values).

8. **Average Paragraph Length (in Sentence)**:<br>
    Number of sentences divided by number of paragraphs.

9. **Average Paragraph Length (in Token)**:<br>
    Number of Tokens divided by number of paragraphs.

10. **Average Sentence Length (in Token)**:<br>
    Number of tokens divided by number of sentences.

11. **Average Token Length (in Character)**:<br>
    Number of characters divided by number of tokens.

12. **Count of n-length Tokens**:<br>
    Number of n-length tokens, where n = 1, 2, 3, etc.

![Overview Table](/doc/overview_table.png)

<span id="doc-eng-concordancer"></span>
### Concordancer [[Back to Contents]](#doc)
In *Concordancer*, you can search for any token in different files and generate concordance lines or plots.

After the concordance lines are generated and displayed in the table, you can sort the results by clicking **Sort Results** or search in results by clicking **Search in Results** at the upper right corner of the *Results Area*.

By default, data in concordance plot are sorted by file. You can tell Wordless to sort the data by search term instead via **Figure Settings → Sort Results by**.

1. **Left**:<br>
    The context before each search term, which displays 10 tokens left to the **Node** by default. You can change this behavior via **Generation Settings**.
2. **Node**:<br>
    Nodes are search terms specified in **Search Settings → Search Term**.
3. **Right**:<br>
    The context after each search term, which displays 10 tokens right to the **Node** by default. You can change this behavior via **Generation Settings**.
4. **Token No.**<br>
    The position of the first token of **Node** in each file.
5. **Sentence No.**<br>
    The position of the sentence in which the **Node** is found in each file.
6. **Paragraph No.**<br>
    The position of the paragraph in which the **Node** is found in each file.
7. **File**<br>
    The file in which the **Node** is found.

![Concordance Table](/doc/concordancer_table.png)
![Concordance Figure](/doc/concordancer_fig.png)

<span id="doc-zho"></span>
## Documentation - Chinese (Simplified)
Editing...

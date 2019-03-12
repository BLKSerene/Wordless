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
* [Supported Text Types](#doc-eng-supported-text-types)
* [Supported File Types](#doc-eng-supported-file-types)
* [Supported File Encodings](#doc-eng-supported-file-encodings)
* [Supported Measures](#doc-eng-supported-measures)
* [Main Window](#doc-eng-main-window)
* [File Area](#doc-eng-file-area)
* [Overview](#doc-eng-overview)
* [Concordancer](#doc-eng-concordancer)
* [Wordlist](#doc-eng-wordlist)
* [N-grams](#doc-eng-ngrams)

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

<span id="doc-eng-supported-text-types"></span>
### Supported Text Types [[Back to Contents]](#doc)

You can specify your custom POS/Non-POS tags via **Menu → Preferences → Settings → Tags**.

Text Types|Auto-detection
----------|:------------:
Untokenized / Untagged        |✔
Untokenized / Tagged (Non-POS)|✔
Tokenized / Untagged          |✖
Tokenized / Tagged (POS)      |✔
Tokenized / Tagged (Non-POS)  |✖
Tokenized / Tagged (Both)     |✔

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

<span id="doc-eng-supported-file-encodings"></span>
### Supported File Encodings [[Back to Contents]](#doc)

Languages|File Encodings|Auto-detection
---------|--------------|:------------:
All Languages|UTF-8 Without BOM               |✔
All Languages|UTF-8 with BOM                  |✔
All Languages|UTF-16 with BOM                 |✔
All Languages|UTF-16 Big Endian Without BOM   |✖
All Languages|UTF-16 Little Endian Without BOM|✖
All Languages|UTF-32 with BOM                 |✖
All Languages|UTF-32 Big Endian Without BOM   |✖
All Languages|UTF-32 Little Endian Without BOM|✖
All Languages|UTF-7                           |✖
All Languages|CP65001                         |✖
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
Chinese|GB18030|✔
Chinese|GBK    |✖
Chinese (Simplified)|GB2312|✖
Chinese (Simplified)|HZ    |✔
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
Persian|Mac OS Farsi|✖
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
Urdu|CP1006      |✖
Urdu|Mac OS Farsi|✖
Vietnamese|CP1258|✖
Western European|EBCDIC 500  |✖
Western European|CP850       |✖
Western European|CP858       |✖
Western European|CP1140      |✖
Western European|ISO-8859-1  |✔
Western European|ISO-8859-15 |✔
Western European|Mac OS Roman|✖
Western European|Windows-1252|✔

<span id="doc-eng-supported-measures"></span>
### Supported Measures [[Back to Contents]](#doc)

<span id="doc-eng-supported-measures-dispersion-adjusted-freq"></span>
#### Measures of Dispersion & Adjusted Frequency

The dispersion and adjusted frequency of a word in each file is calculated by first dividing each file into **n** (5 by default) sub-sections and the frequency of the word in each part is counted, which are denoted by **F₁**, **F₂**, **F₃** ... **Fn**. The total frequency of the word in each file is denoted by **F**. The mean value of the frequencies over all sub-sections is denoted by ![F-bar](/doc/measures/f_bar.gif).

Then, the dispersion and adjusted frequency of the word will be calcuated as follows:

<!--
Juilland's D:
    \begin{align*}
        CV &= \frac{\sum_{i = 1}^{n}(F_{i} - \bar{F})^{2}}{\bar{F}} \\
        D &= \frac{1 - CV}{\sqrt{i - 1}}
    \end{align*}

Carroll's D₂:
    \begin{align*}
        H &= \ln F - \frac{\sum_{i = 1}^{n} \times \ln F_{i}}{F} \\
        D_{2} &= \frac{H}{\ln n}
    \end{align*}

Lyne's D₃:
    \begin{align*}
        \chi^{2} &= \sum_{i = 1}^{n}\frac{(F_{i} - \frac{F}{i})^{2}}{\frac{F}{i}} \\
        D_{3} &= \frac{1 - \chi^{2}}{4F}
    \end{align*}

Rosengren's S:
    \begin{align*}
        KF &= \frac{1}{n}(\sum_{i = 1}^{n}\sqrt{F_{i}})^{2} \\
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

Measures of Dispersion|Formulas
----------------------|-------
Juilland's D|![Juilland's D](/doc/measures/dispersion/juillands_d.gif)
Carroll's D₂|![Carroll's D₂](/doc/measures/dispersion/carrolls_d2.gif)
Lyne's D₃|![Lyne's D₃](/doc/measures/dispersion/lynes_d3.gif)
Rosengren's S|![Rosengren's S](/doc/measures/dispersion/rosengrens_s.gif)
Zhang's Distributional Consistency|![Zhang's Distributional Consistency](/doc/measures/dispersion/zhangs_distributional_consistency.gif)
Gries's DP|![Gries's DP](/doc/measures/dispersion/griess_dp.gif)
Gries's DPnorm|![Gries's DPnorm](/doc/measures/dispersion/griess_dp_norm.gif)

**Works Cited**:<br>
[1] Juilland, Alphonse and Eugenio Chang-Rodriguez. Frequency Dictionary of Spanish Words, Mouton, 1964.<br>
[2] Carroll, John B. "An alternative to Juilland’s usage coefficient for lexical frequencies and a proposal for a standard frequency index." Computer Studies in the Humanities and Verbal Behaviour, vol.3, no. 2, 1970, pp. 61-65.<br>
[3] Lyne, A. A. "Dispersion." The Vocabulary of French Business Correspondence. Slatkine-Champion, 1985, pp. 101-24.<br>
[4] Rosengren, Inger. "The quantitative concept of language and its relation to the structure of frequency dictionaries." Études de linguistique appliquée, no. 1, 1971, pp. 103-27.<br>
[5] Zhang Huarui, et al. "Distributional Consistency: As a General Method for Defining a Core Lexicon." Proceedings of Fourth International Conference on Language Resources and Evaluation, Lisbon, 26-28 May 2004.<br>
[6] Gries, Stefan Th. "Dispersions and Adjusted Frequencies in Corpora." International Journal of Corpus Linguistics, vol. 13, no. 4, 2008, pp. 403-37.<br>
[7] Lijffijt, Jefrey and Stefan Th. Gries. "Correction to Stefan Th. Gries’ “Dispersions and adjusted frequencies in corpora”" International Journal of Corpus Linguistics, vol. 17, no. 1, 2012, pp. 147-49.

<!--
Juilland's U:
    \begin{align*}
        CV &= \frac{\sum_{i = 1}^{n}(F_{i} - \bar{F})^{2}}{\bar{F}} \\
        D &= \frac{1 - CV}{\sqrt{i - 1}} \\
        U &= D \times F
    \end{align*}

Carroll's Um:
    \begin{align*}
        H &= \ln F - \frac{\sum_{i = 1}^{n} \times \ln F_{i}}{F} \\
        D_{2} &= \frac{H}{\ln n} \\
        Um & = F \times D_{2} + (1 - D_{2}) \times \frac{F}{n}
    \end{align*}

Rosengren's KF:
    \begin{align*}
        KF &= \frac{1}{n}(\sum_{i = 1}^{n}\sqrt{F_{i}})^{2}
    \end{align*}

Engwall's FM:
    \begin{align*}
        FM = \frac{F \times R}{n}
    \end{align*}

Kromer's UR:
    \begin{align*}
        UR = \sum_{i = 1}^{n}\psi(F_{i} + 1) + C
    \end{align*}
-->

Measures of Adjusted Frequency|Formulas
----------------------|-------
Juilland's U|![Juilland's U](/doc/measures/adjusted_freq/juillands_u.gif)
Carroll's Um|![Carroll's Um](/doc/measures/adjusted_freq/carrolls_um.gif)
Rosengren's KF|![Rosengren's KF](/doc/measures/adjusted_freq/rosengrens_kf.gif)
Engwall's FM|![Engwall's FM](/doc/measures/adjusted_freq/engwalls_fm.gif)<br>where **R** is the number of sub-sections in which the word appears at least once
Kromer's UR|![Kromer's UR](/doc/measures/adjusted_freq/kromers_ur.gif)<br>where ψ is the digamma function, C is the Euler–Mascheroni constant

**Works Cited**:<br>
[1] Juilland, Alphonse and Eugenio Chang-Rodriguez. Frequency Dictionary of Spanish Words, Mouton, 1964.<br>
[2] Carroll, John B. "An alternative to Juilland’s usage coefficient for lexical frequencies and a proposal for a standard frequency index." Computer Studies in the Humanities and Verbal Behaviour, vol.3, no. 2, 1970, pp. 61-65.<br>
[3] Rosengren, Inger. "The Quantitative Concept of Language and Its Relation to The Structure of Frequency Dictionaries." Études De Linguistique Appliquée, n.s.1, 1971, pp. 103-27.<br>
[4] Engwall, Gunnel. "Fréquence Et Distribution Du Vocabulaire Dans Un Choix De Romans Français." Dissertation, Stockholm University, 1974.<br>
[5] Kromer, Victor. "A Usage Measure Based on Psychophysical Relations." Journal of Quatitative Linguistics, vol. 10, no. 2, 2003, pp. 177-186.

<span id="doc-eng-supported-tests-statistical_significance"></span>
#### Tests of Statistical Significance

To calculate the statistical significance and bayes factor (except **Student's t-test (Two-sample)** and **Mann-Whiteney U Test**) for two words in the same file (collocates) or one specific word in two different files (keywords), two contingency tables must be constructed first, one for observed values, the other for expected values.

As for collocates (in *Collocation* and *Colligation*):

Observed Values|Word 1                       |Not Word 1                   |Row Total
--------------:|:---------------------------:|:---------------------------:|:---------------------------:
Word 2         |![c11](/doc/measures/c11.gif)|![c12](/doc/measures/c12.gif)|![c1x](/doc/measures/c1x.gif)
Not Word 2     |![c21](/doc/measures/c21.gif)|![c22](/doc/measures/c22.gif)|![c2x](/doc/measures/c2x.gif)
Column Total   |![cx1](/doc/measures/cx1.gif)|![cx2](/doc/measures/cx2.gif)|![cxx](/doc/measures/cxx.gif)

Expected Values|Word 1                       |Not Word 1
--------------:|:---------------------------:|:---------------------------:
Word 2         |![e11](/doc/measures/e11.gif)|![e12](/doc/measures/e12.gif) 
Not Word 2     |![e21](/doc/measures/e21.gif)|![e22](/doc/measures/e22.gif)

![c11](/doc/measures/c11.gif): Number of occurrences of Word 1 followed by Word 2<br>
![c12](/doc/measures/c12.gif): Number of occurrences of Word 1 followed by any word except Word 2<br>
![c21](/doc/measures/c21.gif): Number of occurrences of any word except Word 1 followed by Word 2<br>
![c22](/doc/measures/c22.gif): Number of occurrences of any word except Word 1 followed by any word except Word 2<br>

As for keywords (in *Keywords*):

Observed Values|Observed File                |Reference File               |Row Total
--------------:|:---------------------------:|:---------------------------:|:---------------------------:
Word *w*       |![c11](/doc/measures/c11.gif)|![c12](/doc/measures/c12.gif)|![c1x](/doc/measures/c1x.gif)
Not Word *w*   |![c21](/doc/measures/c21.gif)|![c22](/doc/measures/c22.gif)|![c2x](/doc/measures/c2x.gif)
Column Total   |![cx1](/doc/measures/cx1.gif)|![cx2](/doc/measures/cx2.gif)|![cxx](/doc/measures/cxx.gif)

Expected Values|Observed File                |Reference File
--------------:|:---------------------------:|:---------------------------:
Word *w*       |![e11](/doc/measures/e11.gif)|![e12](/doc/measures/e12.gif) 
Not Word *w*   |![e21](/doc/measures/e21.gif)|![e22](/doc/measures/e22.gif)

![c11](/doc/measures/c11.gif): Number of occurrences of Word *w* in the observed file<br>
![c12](/doc/measures/c12.gif): Number of occurrences of Word *w* in the reference file<br>
![c21](/doc/measures/c21.gif): Number of occurrences of all words except Word *w* in the observed file<br>
![c22](/doc/measures/c22.gif): Number of occurrences of all words except Word *w* in the reference file<br>

To conduct **Student's t-test (Two-sample)** or **Mann-Whiteney U Test** on a specific word, the observed file and the reference file are first divided into **n** (5 by default) sub-sections respectively. Then, the frequencies of the word in each sub-section of the observed file and the reference file are counted and denoted by **FO₁**, **FO₂**, **FO₃** ... **FOn** and **FR₁**, **FR₂**, **FR₃** ... **FRn** respectively. The total frequency of the word in the observed file and the reference file are denoted by **FO** and **FR** respectively. The mean value of the frequencies over all sub-sections of the observed file and the reference file are denoted by ![FO-bar](/doc/measures/fo_bar.gif) and ![FR-bar](/doc/measures/fr_bar.gif) respectively.

<!--
z-score:
    \begin{align*}
        z = \frac{C_{11} - E_{11}}{\sqrt{E_{11} \times (1 - \frac{E_{11}}{C_{xx}}))}}
    \end{align*}

Student's t-test (One-sample):
    \begin{align*}
        t = \frac{C_{11} - E_{11}}{\sqrt{C_{11} \times (1 - \frac{C_{11}}{C_{xx}}))}}
    \end{align*}

Student's t-test (Two-sample):
    \begin{align*}
        s_{1} &= \frac{\sum_{i = 1}^{n}(FO_{i} - \bar{FO})^{2}}{n - 1} \\
        s_{2} &= \frac{\sum_{i = 1}^{n}(FR_{i} - \bar{FR})^{2}}{n - 1} \\
        t &= \frac{\bar{FO} - \bar{FR}}{\sqrt{\frac{s_{1} - s_{2}}{n}}}
    \end{align*}

Pearson's Chi-squared Test:
    \begin{align*}
        \chi^{2} = \sum_{i = 1}^{2} \sum_{j = 1}^{2}\frac{(C_{ij} - E{ij})^{2}}{E_{ij}}
    \end{align*}

Log-likelihood Ratio:
    \begin{align*}
        G &= 2\sum_{i = 1}^{2} \sum_{j = 1}^{2}(C_{ij} \times \ln \frac{C_{ij}}{E_{ij}})
    \end{align*}
-->

Then the statistical significance and bayes factor will be calculated as follows:

Tests of Statistical Significance|Formulas
---------------------------------|--------
z-score                      |![z-score](/doc/measures/statistical_significance/z_score.gif)
Student's t-test (One-sample)|![Student's t-test (One-sample)](/doc/measures/statistical_significance/students_t_test_1_sample.gif)
Student's t-test (Two-sample)|![Student's t-test (Two-sample)](/doc/measures/statistical_significance/students_t_test_2_sample.gif)
Pearson's Chi-squared Test   |![Pearson's Chi-squared Test](/doc/measures/statistical_significance/pearsons_chi_squared_test.gif)
Log-likelihood Ratio         |![Log-likelihood Ratio](/doc/measures/statistical_significance/log_likehood_ratio_test.gif)
Fisher's Exact Test          |See: [Fisher's exact test - Wikipedia](https://en.wikipedia.org/wiki/Fisher%27s_exact_test#Example)
Mann-Whiteney U Test         |See: [Mann–Whitney U test - Wikipedia](https://en.wikipedia.org/wiki/Mann%E2%80%93Whitney_U_test#Calculations)

**Works Cited**:<br>
[1] Dennis, S. F. "The Construction of a Thesaurus Automatically from a Sample of Text." Proceedings of the Symposium on Statistical Association Methods For Mechanized Documentation, Washington, D.C., 17 March, 1964, edited by Stevens, M. E., et at., National Bureau of Standards, 1965, pp. 61-148.<br>
[2] Berry-rogghe, Godelieve L. M. "The Computation of Collocations and their Relevance in Lexical Studies." The computer and literary studies, edited by Aitken, A. J., Edinburgh UP, 1973, pp. 103-112.<br>
[3] Church, Kenneth Ward, et al. "Using Statistics in Lexical Analysis." Lexical Acquisition: Exploiting On-Line Resources to Build a Lexicon, edited by Uri Zernik, Psychology Press, 1991, pp. 115-64.<br>
[4] Paquot, Magali and Yves Bestgen. "Distinctive Words in Academic Writing: A Comparison of Three Statistical Tests for Keyword Extraction." Language and Computers, vol.68, 2009, pp. 247-269.<br>
[5] Hofland, Knut and Stig Johansson. Word Frequencies in British and American English. Norwegian Computing Centre for the Humanities, 1982.<br>
[6] Oakes, Michael P. Statistics for Corpus Linguistics. Edinburgh UP, 1998.<br>
[7] Dunning, Ted Emerson. "Accurate Methods for the Statistics of Surprise and Coincidence." Computational Linguistics, vol. 19, no. 1, Mar. 1993, pp. 61-74.<br>
[8] Pedersen, Ted. "Fishing for Exactness." Proceedings of the South-Central SAS Users Group Conference, 27-29 Oct. 1996, Austin.<br>
[9] Kilgarriff, Adam. "Comparing Corpora." International Journal of Corpus Linguistics, vol.6, no.1, Nov. 2001, pp. 232-263.

<!--
Student's t-test (Two-sample):
    \begin{align*}
        s_{1} &= \frac{\sum_{i = 1}^{n}(FO_{i} - \bar{FO})^{2}}{n - 1} \\
        s_{2} &= \frac{\sum_{i = 1}^{n}(FR_{i} - \bar{FR})^{2}}{n - 1} \\
        t &= \frac{\bar{FO} - \bar{FR}}{\sqrt{\frac{s_{1} - s_{2}}{n}}} \\
        BF & = t^{2} - \ln n
    \end{align*}

Log-likelihood Ratio:
    \begin{align*}
        G &= 2\sum_{i = 1}^{2} \sum_{j = 1}^{2}(C_{ij} \times \ln \frac{C_{ij}}{E_{ij}}) \\
        BF &= G - \ln C_{xx}
    \end{align*}
-->

Bayes Factor|Formulas
------------|--------
Student's t-test (Two-sample)|![Student's t-test (Two-sample)](/doc/measures/bayes_factor/students_t_test_2_sample.gif)
Log-likelihood Ratio         |![Log-likelihood Ratio](/doc/measures/bayes_factor/log_likehood_ratio_test.gif)

**Work Cited**:
[1] Wilson, Andrew. "Embracing Bayes Factors for Key Item Analysis in Corpus Linguistics." New Approaches to the Study of Linguistic Variability, edited by Markus Bieswanger and Amei Koll-Stobbe, Peter Lang, 2013, pp. 3-11.

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

    You can specify what should be counted as a "token" via **Token Settings** in the *Settings Area*

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

![Overview Table](/doc/overview/overview_table.png)

<span id="doc-eng-concordancer"></span>
### Concordancer [[Back to Contents]](#doc)
In *Concordancer*, you can search for any token in different files and generate concordance lines or plots.

After the concordance lines are generated and displayed in the table, you can sort the results by clicking **Sort Results** or search in results by clicking **Search in Results**, both buttons residing at the right corner of the *Results Area*.

By default, data in concordance plot are sorted by file. You can sort the data by search term instead via **Figure Settings → Sort Results by**.

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

![Concordance Table](/doc/concordancer/concordancer_table.png)
![Concordance Figure - File](/doc/concordancer/concordancer_fig_file.png)
![Concordance Figure - Search Term](/doc/concordancer/concordancer_fig_search_term.png)

<span id="doc-eng-wordlist"></span>
### Wordlist [[Back to Contents]](#doc)
In *Wordlist*, you can generate wordlists for different files.

In addition, you can generate line charts or word clouds for wordlists. You can modify the settings for the generated figure via **Figure Settings**.

You can filter the results by clicking **Filter Results** or search in results by clicking **Search in Results**, both buttons residing at the right corner of the *Results Area*.

1. **Rank**:<br>
    The rank of the token sorted by its frequency in the first file in descending order (by default). You can sort the results again by clicking the column headers. 

2. **Tokens**:<br>
    You can specify what should be counted as a "token" via **Token Settings**.

3. **Frequency**:<br>
    The number of occurrences of the token in each file.

4. **Dispersion**:<br>
    The dispersion of the token in each file. You can change the measure of dispersion via **Generation Settings → Measure of Dispersion**. See [Measures of Dispersion & Adjusted Frequency](#doc-eng-supported-measures-dispersion-adjusted-freq) for more details.

5. **Adjusted Frequency**:<br>
    The adjusted frequency of the token in each file. You can change the measure of adjusted frequency via **Generation Settings → Measure of Adjusted Frequency**. See [Measures of Dispersion & Adjusted Frequency](#doc-eng-supported-measures-dispersion-adjusted-freq) for more details.

6. **Number of Files Found**:<br>
    The number of files in which the token appears at least once.

![Wordlist Table](/doc/wordlist/wordlist_table.png)
![Wordlist Figure - Line Chart](/doc/wordlist/wordlist_fig_line_chart.png)
![Wordlist Figure - Word Cloud](/doc/wordlist/wordlist_fig_word_cloud.png)

<span id="doc-eng-ngrams"></span>
### N-grams [[Back to Contents]](#doc)
In *N-grams*, you can search for n-grams (consecutive tokens) or skip-grams (non-consecutive tokens) in different files. To allow skip-grams in the results, check **Generation Settings → Allow skipped tokens** and modify the settings. You can set constraints on the position of the search term in all n-grams via **Search Settings → Search Term Position**.

In addition, you can generate line charts or word clouds for n-grams. You can modify the settings for the generated figure via **Figure Settings**.

It is possible to disable searching altogether and generate an exhausted list of n-grams by unchecking **Search Settings** for each file, but it is not recommended to do so, since the processing speed might be to slow.

You can filter the results by clicking **Filter Results** or search in results by clicking **Search in Results**, both buttons residing at the right corner of the *Results Area*.

1. **Rank**:<br>
    The rank of the n-gram sorted by its frequency in the first file in descending order (by default). You can sort the results again by clicking the column headers. 

2. **N-grams**:<br>
    You can specify what should be counted as a "n-gram" via **Token Settings**.

3. **Frequency**:<br>
    The number of occurrences of the n-gram in each file.

4. **Dispersion**:<br>
    The dispersion of the n-gram in each file. You can change the measure of dispersion via **Generation Settings → Measure of Dispersion**. See [Measures of Dispersion & Adjusted Frequency](#doc-eng-supported-measures-dispersion-adjusted-freq) for more details.

5. **Adjusted Frequency**:<br>
    The adjusted frequency of the n-gram in each file. You can change the measure of adjusted frequency via **Generation Settings → Measure of Adjusted Frequency**. See [Measures of Dispersion & Adjusted Frequency](#doc-eng-supported-measures-dispersion-adjusted-freq) for more details.

6. **Number of Files Found**:<br>
    The number of files in which the n-gram appears at least once.

![N-grams Table](/doc/ngrams/ngrams_table.png)
![N-grams Figure - Line Chart](/doc/ngrams/ngrams_fig_line_chart.png)
![N-grams Figure - Word Cloud](/doc/ngrams/ngrams_fig_word_cloud.png)

<span id="doc-zho"></span>
## Documentation - Chinese (Simplified)
Editing...

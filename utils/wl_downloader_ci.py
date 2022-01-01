#
# Wordless: Downloader - CI
#
# Copyright (C) 2018-2022  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import nltk
import spacy

# Download spaCy models
spacy.cli.download('ca_core_news_sm')
spacy.cli.download('zh_core_web_sm')
spacy.cli.download('da_core_news_sm')
spacy.cli.download('nl_core_news_sm')
spacy.cli.download('en_core_web_sm')
spacy.cli.download('fr_core_news_sm')
spacy.cli.download('de_core_news_sm')
spacy.cli.download('el_core_news_sm')
spacy.cli.download('it_core_news_sm')
spacy.cli.download('lt_core_news_sm')
spacy.cli.download('mk_core_news_sm')
spacy.cli.download('nb_core_news_sm')
spacy.cli.download('pl_core_news_sm')
spacy.cli.download('pt_core_news_sm')
spacy.cli.download('ro_core_news_sm')
spacy.cli.download('ru_core_news_sm')
spacy.cli.download('es_core_news_sm')

# Download NLTK data
## Corpora
nltk.download('stopwords')
nltk.download('wordnet')
## Taggers
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_ru')
## Tokenizers
nltk.download('punkt')
## Misc
nltk.download('perluniprops')

# ----------------------------------------------------------------------
# Utilities: Downloader - CI
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
# ----------------------------------------------------------------------

import nltk
import spacy

# Download spaCy models
spacy.cli.download('ca_core_news_sm')
spacy.cli.download('zh_core_web_sm')
spacy.cli.download('hr_core_news_sm')
spacy.cli.download('da_core_news_sm')
spacy.cli.download('nl_core_news_sm')
spacy.cli.download('en_core_web_sm')
spacy.cli.download('fi_core_news_sm')
spacy.cli.download('fr_core_news_sm')
spacy.cli.download('de_core_news_sm')
spacy.cli.download('el_core_news_sm')
spacy.cli.download('it_core_news_sm')
spacy.cli.download('ja_core_news_sm')
spacy.cli.download('lt_core_news_sm')
spacy.cli.download('mk_core_news_sm')
spacy.cli.download('nb_core_news_sm')
spacy.cli.download('pl_core_news_sm')
spacy.cli.download('pt_core_news_sm')
spacy.cli.download('ro_core_news_sm')
spacy.cli.download('ru_core_news_sm')
spacy.cli.download('es_core_news_sm')
spacy.cli.download('sv_core_news_sm')
spacy.cli.download('uk_core_news_sm')

# Download NLTK data
# Corpora
nltk.download('omw-1.4')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('words')
# Taggers
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_ru')
# Tokenizers
nltk.download('punkt')
# Misc
nltk.download('perluniprops')

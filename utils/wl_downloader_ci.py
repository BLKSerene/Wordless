# ----------------------------------------------------------------------
# Utilities: Downloader - CI
# Copyright (C) 2018-2024  Ye Lei (叶磊)
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

import platform
import subprocess

import nltk
import spacy
import stanza

# Run command line tools on CI
def run_cli(commands):
    platform_os = platform.system()

    if platform_os == 'Windows':
        subprocess.run(['python', '-m'] + commands, check = True)
    else:
        try:
            if platform_os == 'Darwin':
                subprocess.run(['python3', '-m'] + commands, check = True)
            elif platform_os == 'Linux':
                subprocess.run(['python3.10', '-m'] + commands, check = True)
        except subprocess.CalledProcessError:
            subprocess.run(['python', '-m'] + commands, check = True)

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

# Download models
spacy.cli.download('en_core_web_trf')
stanza.download('en', processors = ['tokenize', 'pos', 'lemma', 'depparse', 'sentiment'])

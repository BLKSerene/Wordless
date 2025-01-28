# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Buryat (Russia)
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
# ----------------------------------------------------------------------

from tests.tests_nlp.tests_stanza import test_stanza

def test_stanza_bxr():
    results_pos_tag = [('Буряад', 'ADJ'), ('хэлэн', 'NOUN'), ('(', 'PUNCT'), ('буряад', 'ADJ'), ('-', 'PUNCT'), ('монгол', 'NOUN'), ('хэлэн', 'NOUN'), (')', 'PUNCT'), ('Алтайн', 'ADJ'), ('хэлэнэй', 'NOUN'), ('изагуурай', 'NOUN'), ('буряад', 'ADJ'), ('арад', 'NOUN'), ('түмэнһөө', 'NOUN'), ('хэрэглэгдэжэ', 'VERB'), ('бай', 'AUX'), ('монгол', 'NOUN'), ('хэлэнэй', 'NOUN'), ('бүлэгэй', 'NOUN'), ('xэлэн', 'NOUN'), ('-аялгуу', 'VERB'), ('юм', 'PART'), ('.', 'PUNCT')]

    test_stanza.wl_test_stanza(
        lang = 'bxr',
        results_sentence_tokenize = ['Буряад хэлэн (буряад-монгол хэлэн) Алтайн хэлэнэй изагуурай буряад арад түмэнһөө хэрэглэгдэжэ бай монгол хэлэнэй бүлэгэй xэлэн-аялгуу юм.', 'Бүгэдэ Найрамдаха Буряад Улас, Эрхүү можо, Забайкалиин хизаар, Усть-Ордын болон Агын тойрогууд, мүн Монгол Уласай хойто аймагууд, Хитадай зүүн-хойто орондо ажаһуудаг буряадууд хэлэлсэдэг.', 'Орос гүрэндэ (1989 оной тоололгоор) 376 мянга оршом хүн буряадаар дуугардаг.', 'Буряадай 86,6%-нь буряад хэлые, 13,3%-нь ород хэлые эхэ (түрэлхи) хэлэн гэһэн байна.', 'Баруун (эхирэд, булагад), дундада (алайр, түнхэн), зүүн (хори), урда (сонгоол, сартуул) гэхэ мэтэ аялгуутай.'],
        results_word_tokenize = ['Буряад', 'хэлэн', '(', 'буряад', '-', 'монгол', 'хэлэн', ')', 'Алтайн', 'хэлэнэй', 'изагуурай', 'буряад', 'арад', 'түмэнһөө', 'хэрэглэгдэжэ', 'бай', 'монгол', 'хэлэнэй', 'бүлэгэй', 'xэлэн', '-аялгуу', 'юм', '.'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['буряад', 'хэлэн', '(', 'буряад', '-', 'монгол', 'хэлэн', ')', 'алтайн', 'хэлэн', 'изаг', 'буряад', 'арад', 'түмэн', 'хэрэглэ', 'бай', 'монгол', 'хэлэн', 'бүлэг', 'xэлэн', '-аял', 'юм', '.'],
        results_dependency_parse = [('Буряад', 'хэлэн', 'amod', 1), ('хэлэн', 'хэлэн', 'nsubj', 5), ('(', 'хэлэн', 'punct', -1), ('буряад', 'хэлэн', 'amod', 3), ('-', 'буряад', 'punct', -1), ('монгол', 'хэлэн', 'amod', 1), ('хэлэн', 'хэлэн', 'root', 0), (')', 'хэлэн', 'punct', -1), ('Алтайн', 'хэлэнэй', 'amod', 1), ('хэлэнэй', 'изагуурай', 'nmod', 1), ('изагуурай', 'арад', 'nmod', 2), ('буряад', 'арад', 'amod', 1), ('арад', 'түмэнһөө', 'nmod', 1), ('түмэнһөө', 'хэрэглэгдэжэ', 'obj', 1), ('хэрэглэгдэжэ', 'xэлэн', 'acl', 5), ('бай', 'хэрэглэгдэжэ', 'aux', -1), ('монгол', 'хэлэнэй', 'amod', 1), ('хэлэнэй', 'бүлэгэй', 'nmod', 1), ('бүлэгэй', 'xэлэн', 'nmod', 1), ('xэлэн', '-аялгуу', 'obj', 1), ('-аялгуу', 'хэлэн', 'parataxis', -14), ('юм', '-аялгуу', 'discourse', -1), ('.', '-аялгуу', 'punct', -2)]
    )

if __name__ == '__main__':
    test_stanza_bxr()

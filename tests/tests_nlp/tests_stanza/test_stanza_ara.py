# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Stanza - Arabic
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

from tests.tests_nlp.tests_stanza import test_stanza

def test_stanza_ara():
    test_stanza.wl_test_stanza(
        lang = 'ara',
        results_sentence_tokenize = ['ٱللُّغَةُ ٱلْعَرَبِيَّة هي أكثر اللغات السامية تحدثًا، وإحدى أكثر اللغات انتشاراً في العالم، يتحدثها أكثر من 467 مليون نسمة.(1) ويتوزع متحدثوها في الوطن العربي، بالإضافة إلى العديد من المناطق الأخرى المجاورة كالأحواز وتركيا وتشاد ومالي والسنغال وإرتيريا وإثيوبيا وجنوب السودان وإيران. وبذلك فهي تحتل المركز الرابع أو الخامس من حيث اللغات الأكثر انتشارًا في العالم، وهي تحتل المركز الثالث تبعًا لعدد الدول التي تعترف بها كلغة رسمية؛ إذ تعترف بها 27 دولة كلغة رسمية، واللغة الرابعة من حيث عدد المستخدمين على الإنترنت. اللغةُ العربيةُ ذات أهمية قصوى لدى المسلمين، فهي عندَهم لغةٌ مقدسة إذ أنها لغة القرآن، وهي لغةُ الصلاة وأساسيةٌ في القيام بالعديد من العبادات والشعائرِ الإسلامية. العربيةُ هي أيضاً لغة شعائرية رئيسية لدى عدد من الكنائس المسيحية في الوطن العربي، كما كُتبَت بها كثير من أهمِّ الأعمال الدينية والفكرية اليهودية في العصور الوسطى. ارتفعتْ مكانةُ اللغةِ العربية إثْرَ انتشارِ الإسلام بين الدول إذ أصبحت لغة السياسة والعلم والأدب لقرون طويلة في الأراضي التي حكمها المسلمون. وللغة العربية تأثير مباشر وغير مباشر على كثير من اللغات الأخرى في العالم الإسلامي، كالتركية والفارسية والأمازيغية والكردية والأردية والماليزية والإندونيسية والألبانية وبعض اللغات الإفريقية الأخرى مثل الهاوسا والسواحيلية والتجرية والأمهرية والصومالية، وبعض اللغات الأوروبية وخاصةً المتوسطية كالإسبانية والبرتغالية والمالطية والصقلية؛ ودخلت الكثير من مصطلحاتها في اللغة الإنجليزية واللغات الأخرى، مثل أدميرال والتعريفة والكحول والجبر وأسماء النجوم.', 'كما أنها تُدرَّس بشكل رسمي أو غير رسمي في الدول الإسلامية والدول الإفريقية المحاذية للوطن العربي.'],
        results_word_tokenize = ['ٱللُّغَة', 'ُ', 'ٱلْعَرَبِيَّة', 'هي', 'أكثر', 'اللغات', 'السامية', 'تحدثًا', '،', 'وإحدى', 'أكثر', 'اللغات', 'انتشاراً', 'في', 'العالم', '،', 'يتحدثها', 'أكثر', 'من', '467', 'مليون', 'نسمة', '.', '(', '1', ')'],
        results_pos_tag = [('ٱللُّغَة', 'U---------'), ('ُ', 'U---------'), ('ٱلْعَرَبِيَّة', 'U---------'), ('هي', 'SP---3FS1-'), ('أكثر', 'A-----MS1R'), ('اللغات', 'N------P2D'), ('السامية', 'N------S2D'), ('تحدثًا', 'N------S4I'), ('،', 'G---------'), ('و', 'C---------'), ('إحدى', 'N------S1R'), ('أكثر', 'A-----MS2R'), ('اللغات', 'N------P2D'), ('انتشاراً', 'N------S4I'), ('في', 'P---------'), ('العالم', 'N------S2D'), ('،', 'G---------'), ('يتحدث', 'VIIA-3MS--'), ('ها', 'SP---3FS4-'), ('أكثر', 'A-----MS1I'), ('من', 'P---------'), ('467', 'Q---------'), ('مليون', 'QM-----S4R'), ('نسمة', 'N------S2I'), ('.', 'G---------'), ('(', 'G---------'), ('1', 'Q---------'), (')', 'G---------')],
        results_pos_tag_universal = [('ٱللُّغَة', 'X'), ('ُ', 'X'), ('ٱلْعَرَبِيَّة', 'X'), ('هي', 'PRON'), ('أكثر', 'ADJ'), ('اللغات', 'NOUN'), ('السامية', 'NOUN'), ('تحدثًا', 'NOUN'), ('،', 'PUNCT'), ('و', 'CCONJ'), ('إحدى', 'NOUN'), ('أكثر', 'ADJ'), ('اللغات', 'NOUN'), ('انتشاراً', 'NOUN'), ('في', 'ADP'), ('العالم', 'NOUN'), ('،', 'PUNCT'), ('يتحدث', 'VERB'), ('ها', 'PRON'), ('أكثر', 'ADJ'), ('من', 'ADP'), ('467', 'NUM'), ('مليون', 'NUM'), ('نسمة', 'NOUN'), ('.', 'PUNCT'), ('(', 'PUNCT'), ('1', 'NUM'), (')', 'PUNCT')],
        results_lemmatize = ['ٱللُّغَة', 'ُ', 'ٱلْعَرَبِيَّة', 'هُوَ', 'أَكثَر', 'لُغَة', 'سَامِيَّة', 'تَحَدُّث', '،', 'وَ', 'إِحدَى', 'أَكثَر', 'لُغَة', 'اِنتِشَار', 'فِي', 'عَالَم', '،', 'تَحَدَّث', 'هُوَ', 'أَكثَر', 'مِن', '467', 'مِليُون', 'نَسَمَة', '.', '(', '1', ')'],
        results_dependency_parse = [('ٱللُّغَة', 'أكثر', 'nsubj', 4), ('ُ', 'ٱللُّغَة', 'nmod', -1), ('ٱلْعَرَبِيَّة', 'ُ', 'nmod', -1), ('هي', 'أكثر', 'obl', 1), ('أكثر', 'أكثر', 'root', 0), ('اللغات', 'أكثر', 'nmod', -1), ('السامية', 'اللغات', 'nmod', -1), ('تحدثًا', 'أكثر', 'obl', -3), ('،', 'تحدثًا', 'punct', -1), ('و', 'يتحدث', 'cc', 8), ('إحدى', 'أكثر', 'conj', -6), ('أكثر', 'إحدى', 'amod', -1), ('اللغات', 'أكثر', 'nmod', -1), ('انتشاراً', 'اللغات', 'nmod', -1), ('في', 'العالم', 'case', 1), ('العالم', 'انتشاراً', 'nmod', -2), ('،', 'العالم', 'punct', -1), ('يتحدث', 'أكثر', 'conj', -13), ('ها', 'يتحدث', 'obj', -1), ('أكثر', 'يتحدث', 'nsubj', -2), ('من', '467', 'case', 1), ('467', 'أكثر', 'nummod', -2), ('مليون', '467', 'nummod', -1), ('نسمة', 'مليون', 'nmod', -1), ('.', 'أكثر', 'punct', -20), ('(', '1', 'punct', 1), ('1', 'أكثر', 'dep', -22), (')', '1', 'punct', -1)]
    )

if __name__ == '__main__':
    test_stanza_ara()

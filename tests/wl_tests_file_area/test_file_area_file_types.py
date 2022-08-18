# ----------------------------------------------------------------------
# Wordless: Tests - File Area - File Types
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
# ----------------------------------------------------------------------

import glob
import os
import time

from PyQt5.QtCore import QObject

from tests import wl_test_init
from wordless import wl_file_area
from wordless.wl_dialogs import wl_dialogs_misc

main = wl_test_init.Wl_Test_Main()

def add_file(file_paths, update_gui):
    def open_file(err_msg, files_to_open):
        assert not err_msg

        # Untokenized & Untagged
        if files_to_open[-1]['path'].endswith('XML File (4).xml'):
            files_to_open[-1]['tokenized'] = False
            files_to_open[-1]['tagged'] = False
        # Tokenized & Untagged
        elif files_to_open[-1]['path'].endswith('XML File (5).xml'):
            files_to_open[-1]['tokenized'] = True
            files_to_open[-1]['tagged'] = False

        wl_file_area.Wl_Worker_Open_Files(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(main, text = ''),
            update_gui = update_gui,
            files_to_open = files_to_open,
            file_type = 'observed'
        ).run()

        print(f'Done! (In {round(time.time() - time_start, 2)} seconds)')

    time_start = time.time()

    for file_path in file_paths:
        print(f'Opening file "{os.path.split(file_path)[1]}"...')

        table = QObject()
        table.files_to_open = []

        wl_file_area.Wl_Worker_Add_Files(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(main, text = ''),
            update_gui = open_file,
            file_paths = [file_path],
            table = table
        ).run()

def test_file_area_file_types():
    # Clean cached files
    for file in glob.glob('imports/*.*'):
        os.remove(file)

    # Disable encoding detection
    main.settings_custom['file_area']['dialog_open_files']['auto_detect_encodings'] = False

    # File types (Non-XML)
    files_non_xml = glob.glob('tests/files/wl_file_area/file_types/*.*')
    files_non_xml = [file for file in files_non_xml if not file.endswith('.xml')]

    add_file(
        file_paths = files_non_xml,
        update_gui = update_gui_file_types
    )

    # File types (XML)
    for i in range(5):
        if i in [0, 3, 4]:
            main.settings_custom['files']['tags']['xml_tag_settings'] = [
                ['Non-embedded', 'Paragraph', '<p>', '</p>'],
                ['Non-embedded', 'Paragraph', '<head>', '</head>'],
                ['Non-embedded', 'Sentence', '<s>', '</s>'],
                ['Non-embedded', 'Word', '<w>', '</w>'],
                ['Non-embedded', 'Word', '<c>', '</c>']
            ]
        # XML tags unfound
        elif i == 1:
            main.settings_custom['files']['tags']['xml_tag_settings'] = [
                ['Non-embedded', 'Paragraph', '<pp>', '</pp>'],
                ['Non-embedded', 'Sentence', '<ss>', '</ss>'],
                ['Non-embedded', 'Word', '<ww>', '</ww>'],
            ]
        # XML tags unspecified
        elif i == 2:
            main.settings_custom['files']['tags']['xml_tag_settings'] = []

        add_file(
            file_paths = glob.glob('tests/files/wl_file_area/file_types/*.xml'),
            update_gui = update_gui_file_types
        )

    # UnicodeDecodeError
    add_file(
        file_paths = glob.glob('tests/files/wl_file_area/unicode_decode_error/*.*'),
        update_gui = update_gui_unicode_decode_error
    )

    # Tags
    for file_path in glob.glob('tests/files/wl_file_area/tags/*.*'):
        if file_path.endswith('untokenized_untagged.txt'):
            main.settings_custom['files']['default_settings']['tokenized'] = False
            main.settings_custom['files']['default_settings']['tagged'] = False
        elif file_path.endswith('untokenized_tagged.txt'):
            main.settings_custom['files']['default_settings']['tokenized'] = False
            main.settings_custom['files']['default_settings']['tagged'] = True
        elif file_path.endswith('tokenized_untagged.txt'):
            main.settings_custom['files']['default_settings']['tokenized'] = True
            main.settings_custom['files']['default_settings']['tagged'] = False
        elif file_path.endswith('tokenized_tagged.txt'):
            main.settings_custom['files']['default_settings']['tokenized'] = True
            main.settings_custom['files']['default_settings']['tagged'] = True

        add_file(
            file_paths = [file_path],
            update_gui = update_gui_tags
        )

def update_gui_file_types(err_msg, new_files):
    assert not err_msg

    # Non-TMX files
    if len(new_files) == 1:
        file_name = os.path.split(new_files[0]['path'])[1]
        file_text = new_files[0]['text']

        print(file_text.tokens_multilevel)
        print(file_text.tokens_flat)
        print(file_text.tags)
        print(file_text.offsets_paras)
        print(file_text.offsets_sentences)

        # CSV files
        if file_name == 'CSV File.txt':
            assert file_text.tokens_multilevel == [[], [], [['3', '-', '2', '3', '-', '3']], [], [], [['6', '-', '2', '6', '-', '3']], [], []]
            assert file_text.tokens_flat == ['3', '-', '2', '3', '-', '3', '6', '-', '2', '6', '-', '3']
            assert file_text.offsets_paras == [0, 0, 0, 6, 6, 6, 12, 12]
            assert file_text.offsets_sentences == [0, 6]
        # Excel workbooks
        elif file_name == 'Excel Workbook.txt':
            assert file_text.tokens_multilevel == [[], [['B2', '&', 'C2', 'D2']], [['B3', '&', 'B4', 'C3', 'D3']], [['C4', 'D4']], [['B5', 'C5', 'D5']], [], [], [['B2', '&', 'C2', 'D2']], [['B3', '&', 'B4', 'C3', 'D3']], [['C4', 'D4']], [['B5', 'C5', 'D5']]]
            assert file_text.tokens_flat == ['B2', '&', 'C2', 'D2', 'B3', '&', 'B4', 'C3', 'D3', 'C4', 'D4', 'B5', 'C5', 'D5', 'B2', '&', 'C2', 'D2', 'B3', '&', 'B4', 'C3', 'D3', 'C4', 'D4', 'B5', 'C5', 'D5']
            assert file_text.offsets_paras == [0, 0, 4, 9, 11, 14, 14, 14, 18, 23, 25]
            assert file_text.offsets_sentences == [0, 4, 9, 11, 14, 18, 23, 25]
        # HTML pages
        elif file_name == 'HTML Page.txt':
            assert file_text.tokens_multilevel == [[], [], [['This', 'is', 'a', 'title']], [], [], [['Hello', 'world', '!']], [], []]
            assert file_text.tokens_flat == ['This', 'is', 'a', 'title', 'Hello', 'world', '!']
            assert file_text.offsets_paras == [0, 0, 0, 4, 4, 4, 7, 7]
            assert file_text.offsets_sentences == [0, 4]
        # PDF files
        elif file_name == 'PDF File.txt':
            assert file_text.tokens_multilevel == [[['Lorem', 'ipsum', 'dolor', 'sit', 'amet', ',', 'consetetur', 'sadipscing', 'elitr', ',', 'sed', 'diam', 'nonumy', 'eirmod']], [['tempor', 'invidunt', 'ut', 'labore', 'et', 'dolore', 'magna', 'aliquyam', 'erat', ',', 'sed', 'diam', 'voluptua', '.'], ['At', 'vero']], [['eos', 'et', 'accusam', 'et', 'justo', 'duo', 'dolores', 'et', 'ea', 'rebum', '.'], ['Stet', 'clita', 'kasd', 'gubergren', ',', 'no', 'sea', 'taki-']], [['mata', 'sanctus', 'est', 'Lorem', 'ipsum', 'dolor', 'sit', 'amet', '.'], ['Lorem', 'ipsum', 'dolor', 'sit', 'amet', ',', 'consetetur']], [['sadipscing', 'elitr', ',', 'sed', 'diam', 'nonumy', 'eirmod', 'tempor', 'invidunt', 'ut', 'labore', 'et', 'dolore', 'magna']], [['aliquyam', 'erat', ',', 'sed', 'diam', 'voluptua', '.'], ['At', 'vero', 'eos', 'et', 'accusam', 'et', 'justo', 'duo', 'dolores', 'et', 'ea']], [['rebum', '.'], ['Stet', 'clita', 'kasd', 'gubergren', ',', 'no', 'sea', 'takimata', 'sanctus', 'est', 'Lorem', 'ipsum', 'dolor', 'sit']], [['amet', '.']], [['1']]]
            assert file_text.tokens_flat == ['Lorem', 'ipsum', 'dolor', 'sit', 'amet', ',', 'consetetur', 'sadipscing', 'elitr', ',', 'sed', 'diam', 'nonumy', 'eirmod', 'tempor', 'invidunt', 'ut', 'labore', 'et', 'dolore', 'magna', 'aliquyam', 'erat', ',', 'sed', 'diam', 'voluptua', '.', 'At', 'vero', 'eos', 'et', 'accusam', 'et', 'justo', 'duo', 'dolores', 'et', 'ea', 'rebum', '.', 'Stet', 'clita', 'kasd', 'gubergren', ',', 'no', 'sea', 'taki-', 'mata', 'sanctus', 'est', 'Lorem', 'ipsum', 'dolor', 'sit', 'amet', '.', 'Lorem', 'ipsum', 'dolor', 'sit', 'amet', ',', 'consetetur', 'sadipscing', 'elitr', ',', 'sed', 'diam', 'nonumy', 'eirmod', 'tempor', 'invidunt', 'ut', 'labore', 'et', 'dolore', 'magna', 'aliquyam', 'erat', ',', 'sed', 'diam', 'voluptua', '.', 'At', 'vero', 'eos', 'et', 'accusam', 'et', 'justo', 'duo', 'dolores', 'et', 'ea', 'rebum', '.', 'Stet', 'clita', 'kasd', 'gubergren', ',', 'no', 'sea', 'takimata', 'sanctus', 'est', 'Lorem', 'ipsum', 'dolor', 'sit', 'amet', '.', '1']
            assert file_text.offsets_paras == [0, 14, 30, 49, 65, 79, 97, 113, 115]
            assert file_text.offsets_sentences == [0, 14, 28, 30, 41, 49, 58, 65, 79, 86, 97, 99, 113, 115]
        # Word documents
        elif file_name == 'Word Document.txt':
            assert file_text.tokens_multilevel == [[], [], [['Heading']], [], [], [['This', 'is', 'the', 'first', 'sentence', '.'], ['This', 'is', 'the', 'second', 'sentence', '.']], [], [], [['This', 'is', 'the', 'third', 'sentence', '.']], [], [['2', '-', '2', '&', '2', '-', '3', '2', '-', '4']], [['3', '-', '2', '&', '4', '-', '2', '3', '-', '3', '3', '-', '4']], [['4', '-', '3', '4', '-', '4']], [['5', '-', '2', '5', '-', '3', '5', '-', '4', '5', '-', '4', '-', '1', '5', '-', '4', '-', '2', '5', '-', '4', '-', '3', '5', '-', '4', '-', '4']], [], [], []]
            assert file_text.tokens_flat == ['Heading', 'This', 'is', 'the', 'first', 'sentence', '.', 'This', 'is', 'the', 'second', 'sentence', '.', 'This', 'is', 'the', 'third', 'sentence', '.', '2', '-', '2', '&', '2', '-', '3', '2', '-', '4', '3', '-', '2', '&', '4', '-', '2', '3', '-', '3', '3', '-', '4', '4', '-', '3', '4', '-', '4', '5', '-', '2', '5', '-', '3', '5', '-', '4', '5', '-', '4', '-', '1', '5', '-', '4', '-', '2', '5', '-', '4', '-', '3', '5', '-', '4', '-', '4']
            assert file_text.offsets_paras == [0, 0, 0, 1, 1, 1, 13, 13, 13, 19, 19, 29, 42, 48, 77, 77, 77]
            assert file_text.offsets_sentences == [0, 1, 7, 13, 19, 29, 42, 48]
        # XML files
        elif file_name == 'XML File.xml':
            assert file_text.tokens_multilevel == [[['FACTSHEET', 'WHAT', 'IS', 'AIDS', '?']], [['AIDS', '(', 'Acquired', 'Immune', 'Deficiency', 'Syndrome', ')', 'is', 'a', 'condition', 'caused', 'by', 'a', 'virus', 'called', 'HIV', '(', 'Human', 'Immuno', 'Deficiency', 'Virus', ')', '.'], ['This', 'virus', 'affects', 'the', 'body', "'s", 'defence', 'system', 'so', 'that', 'it', 'can', 'not', 'fight', 'infection', '.']]]
            assert file_text.tokens_flat == ['FACTSHEET', 'WHAT', 'IS', 'AIDS', '?', 'AIDS', '(', 'Acquired', 'Immune', 'Deficiency', 'Syndrome', ')', 'is', 'a', 'condition', 'caused', 'by', 'a', 'virus', 'called', 'HIV', '(', 'Human', 'Immuno', 'Deficiency', 'Virus', ')', '.', 'This', 'virus', 'affects', 'the', 'body', "'s", 'defence', 'system', 'so', 'that', 'it', 'can', 'not', 'fight', 'infection', '.']
            assert file_text.offsets_paras == [0, 5]
            assert file_text.offsets_sentences == [0, 5, 28]
        # XML tags unfound or unspecified
        elif file_name in ['XML File (2).xml', 'XML File (3).xml']:
            assert file_text.tokens_multilevel == [[], [], [['FACTSHEET', 'WHAT', 'IS', 'AIDS', '?']], [['AIDS', '(', 'Acquired', 'Immune', 'Deficiency', 'Syndrome)is', 'a', 'condition', 'caused', 'by', 'a', 'virus', 'called', 'HIV', '(', 'Human', 'Immuno', 'Deficiency', 'Virus', ')', '.']], [['This', 'virus', 'affects', 'the', 'body', "'s", 'defence', 'system', 'so', 'that', 'it', 'can', 'not', 'fight', 'infection', '.']]]
            assert file_text.tokens_flat == ['FACTSHEET', 'WHAT', 'IS', 'AIDS', '?', 'AIDS', '(', 'Acquired', 'Immune', 'Deficiency', 'Syndrome)is', 'a', 'condition', 'caused', 'by', 'a', 'virus', 'called', 'HIV', '(', 'Human', 'Immuno', 'Deficiency', 'Virus', ')', '.', 'This', 'virus', 'affects', 'the', 'body', "'s", 'defence', 'system', 'so', 'that', 'it', 'can', 'not', 'fight', 'infection', '.']
            assert file_text.offsets_paras == [0, 0, 0, 5, 26]
            assert file_text.offsets_sentences == [0, 5, 26]
        # Untokenized & Untagged
        elif file_name == 'XML File (4).xml':
            assert file_text.tokens_multilevel == [[['<', 'bncDoc', 'xml', ':', 'id="A00"><teiHeader><fileDesc><titleStmt><title', '>', '['], ['ACET', 'factsheets', '&', 'amp', ';', 'newsletters', ']', '.'], ['Sample', 'containing', 'about', '6688', 'words', 'of', 'miscellanea', '(', 'domain', ':', 'social', 'science', ')', '<', '/title><respStmt><resp', '>', 'Data', 'capture', 'and', 'transcription', '<', '/resp><name', '>', 'Oxford', 'University', 'Press', '<', '/name', '>', '<', '/respStmt></titleStmt><editionStmt><edition', '>', 'BNC', 'XML', 'Edition', ',', 'December', '2006</edition></editionStmt><extent', '>', '6688', 'tokens', ';', '6708', 'w', '-', 'units', ';', '423', 's', '-', 'units', '<', '/extent><publicationStmt><distributor', '>', 'Distributed', 'under', 'licence', 'by', 'Oxford', 'University', 'Computing', 'Services', 'on', 'behalf', 'of', 'the', 'BNC', 'Consortium.</distributor><availability', '>', 'This', 'material', 'is', 'protected', 'by', 'international', 'copyright', 'laws', 'and', 'may', 'not', 'be', 'copied', 'or', 'redistributed', 'in', 'any', 'way', '.'], ['Consult', 'the', 'BNC', 'Web', 'Site', 'at', 'http://www.natcorp.ox.ac.uk', 'for', 'full', 'licencing', 'and', 'distribution', 'conditions.</availability><idno', 'type="bnc">A00</idno><idno', 'type="old', '"', '>', 'AidFct', '<', '/idno></publicationStmt><sourceDesc><bibl><title', '>', '['], ['ACET', 'factsheets', '&', 'amp', ';', 'newsletters', ']', '.'], ['<', '/title', '>', '<', 'imprint', 'n="AIDSCA1"><publisher', '>', 'Aids', 'Care', 'Education', '&', 'amp', ';', 'Training', '<', '/publisher', '>', '<', 'pubPlace', '>', 'London', '<', '/pubPlace', '>', '<', 'date', 'value="1991', '-', '09', '"', '>', '1991', '-', '09', '<', '/date', '>', '<', '/imprint', '>', '<', '/bibl></sourceDesc></fileDesc><encodingDesc><tagsDecl><namespace', 'name=""><tagUsage', 'gi="c', '"', 'occurs="810"/><tagUsage', 'gi="div', '"', 'occurs="43"/><tagUsage', 'gi="head', '"', 'occurs="45"/><tagUsage', 'gi="hi', '"', 'occurs="24"/><tagUsage', 'gi="item', '"', 'occurs="43"/><tagUsage', 'gi="label', '"', 'occurs="10"/><tagUsage', 'gi="list', '"', 'occurs="8"/><tagUsage', 'gi="mw', '"', 'occurs="31"/><tagUsage', 'gi="p', '"', 'occurs="118"/><tagUsage', 'gi="pb', '"', 'occurs="2"/><tagUsage', 'gi="s', '"', 'occurs="423"/><tagUsage', 'gi="w', '"', 'occurs="6708"/></namespace></tagsDecl></encodingDesc><profileDesc><creation', 'date="1991">1991', '-', '09', '<', '/creation><textClass><catRef', 'targets="WRI', 'ALLTIM3', 'ALLAVA2', 'ALLTYP5', 'WRIAAG0', 'WRIAD0', 'WRIASE0', 'WRIATY2', 'WRIAUD3', 'WRIDOM4', 'WRILEV2', 'WRIMED3', 'WRIPP5', 'WRISAM5', 'WRISTA2', 'WRITAS3"/><classCode', 'scheme="DLEE">W', 'nonAc', ':', 'medicine</classCode><keywords><term', '>', 'Health', '<', '/term><term', '>', 'Sex', '<', '/term></keywords></textClass></profileDesc><revisionDesc><change', 'date="2006', '-', '10', '-', '21', '"', 'who="#OUCS">Tag', 'usage', 'updated', 'for', 'BNC', '-', 'XML</change><change', 'date="2000', '-', '12', '-', '13', '"', 'who="#OUCS">Last', 'check', 'for', 'BNC', 'World', 'first', 'release</change><change', 'date="2000', '-', '09', '-', '06', '"', 'who="#OUCS">Redo', 'tagusage', 'tables</change><change', 'date="2000', '-', '09', '-', '01', '"', 'who="#OUCS">Check', 'all', 'tagcounts</change><change', 'date="2000', '-', '06', '-', '23', '"', 'who="#OUCS">Resequenced', 's', '-', 'units', 'and', 'added', 'headers</change><change', 'date="2000', '-', '01', '-', '21', '"', 'who="#OUCS">Added', 'date', 'info</change><change', 'date="2000', '-', '01', '-', '09', '"', 'who="#OUCS">Updated', 'all', 'catrefs</change><change', 'date="2000', '-', '01', '-', '08', '"', 'who="#OUCS">Manually', 'updated', 'tagcounts', ',', 'titlestmt', ',', 'and', 'title', 'in', 'source</change><change', 'date="1999', '-', '09', '-', '13', '"', 'who="#UCREL">POS', 'codes', 'revised', 'for', 'BNC-2', ';', 'header', 'updated</change><change', 'date="1994', '-', '11', '-', '24', '"', 'who="#dominic">Initial', 'accession', 'to', 'corpus</change></revisionDesc></teiHeader', '>']], [['<', 'wtext', 'type="NONAC"><div', 'level="1', '"', 'n="1', '"', 'type="leaflet"><head', 'type="MAIN', '"', '>']], [['<', 's', 'n="1"><w', 'c5="NN1', '"', 'hw="factsheet', '"', 'pos="SUBST">FACTSHEET', '<', '/w><w', 'c5="DTQ', '"', 'hw="what', '"', 'pos="PRON">WHAT', '<', '/w><w', 'c5="VBZ', '"', 'hw="be', '"', 'pos="VERB">IS', '<', '/w><w', 'c5="NN1', '"', 'hw="aids', '"', 'pos="SUBST">AIDS</w><c', 'c5="PUN">?</c></s></head><p', '>']], [['<', 's', 'n="2"><hi', 'rend="bo"><w', 'c5="NN1', '"', 'hw="aids', '"', 'pos="SUBST">AIDS', '<', '/w><c', 'c5="PUL">(</c><w', 'c5="VVN', '-', 'AJ0', '"', 'hw="acquire', '"', 'pos="VERB">Acquired', '<', '/w><w', 'c5="AJ0', '"', 'hw="immune', '"', 'pos="ADJ">Immune', '<', '/w><w', 'c5="NN1', '"', 'hw="deficiency', '"', 'pos="SUBST">Deficiency', '<', '/w><w', 'c5="NN1', '"', 'hw="syndrome', '"', 'pos="SUBST">Syndrome</w><c', 'c5="PUR">)</c></hi><w', 'c5="VBZ', '"', 'hw="be', '"', 'pos="VERB">is', '<', '/w><w', 'c5="AT0', '"', 'hw="a', '"', 'pos="ART">a', '<', '/w><w', 'c5="NN1', '"', 'hw="condition', '"', 'pos="SUBST">condition', '<', '/w><w', 'c5="VVN', '"', 'hw="cause', '"', 'pos="VERB">caused', '<', '/w><w', 'c5="PRP', '"', 'hw="by', '"', 'pos="PREP">by', '<', '/w><w', 'c5="AT0', '"', 'hw="a', '"', 'pos="ART">a', '<', '/w><w', 'c5="NN1', '"', 'hw="virus', '"', 'pos="SUBST">virus', '<', '/w><w', 'c5="VVN', '"', 'hw="call', '"', 'pos="VERB">called', '<', '/w><w', 'c5="NP0', '"', 'hw="hiv', '"', 'pos="SUBST">HIV', '<', '/w><c', 'c5="PUL">(</c><w', 'c5="AJ0', '-', 'NN1', '"', 'hw="human', '"', 'pos="ADJ">Human', '<', '/w><w', 'c5="NN1', '"', 'hw="immuno', '"', 'pos="SUBST">Immuno', '<', '/w><w', 'c5="NN1', '"', 'hw="deficiency', '"', 'pos="SUBST">Deficiency', '<', '/w><w', 'c5="NN1', '"', 'hw="virus', '"', 'pos="SUBST">Virus</w><c', 'c5="PUR">)</c><c', 'c5="PUN">.</c></s', '>']], [['<', 's', 'n="3"><w', 'c5="DT0', '"', 'hw="this', '"', 'pos="ADJ">This', '<', '/w><w', 'c5="NN1', '"', 'hw="virus', '"', 'pos="SUBST">virus', '<', '/w><w', 'c5="VVZ', '"', 'hw="affect', '"', 'pos="VERB">affects', '<', '/w><w', 'c5="AT0', '"', 'hw="the', '"', 'pos="ART">the', '<', '/w><w', 'c5="NN1', '"', 'hw="body', '"', 'pos="SUBST">body</w><w', 'c5="POS', '"', 'hw=', '"', "'s", '"', 'pos="UNC', '"', '>', "'s", '<', '/w><w', 'c5="NN1', '"', 'hw="defence', '"', 'pos="SUBST">defence', '<', '/w><w', 'c5="NN1', '"', 'hw="system', '"', 'pos="SUBST">system', '<', '/w><mw', 'c5="CJS"><w', 'c5="AV0', '"', 'hw="so', '"', 'pos="ADV">so', '<', '/w><w', 'c5="CJT', '"', 'hw="that', '"', 'pos="CONJ">that', '<', '/w></mw><w', 'c5="PNP', '"', 'hw="it', '"', 'pos="PRON">it', '<', '/w><w', 'c5="VM0', '"', 'hw="can', '"', 'pos="VERB">can</w><w', 'c5="XX0', '"', 'hw="not', '"', 'pos="ADV">not', '<', '/w><w', 'c5="VVI', '"', 'hw="fight', '"', 'pos="VERB">fight', '<', '/w><w', 'c5="NN1', '"', 'hw="infection', '"', 'pos="SUBST">infection</w><c', 'c5="PUN">.</c></s></p', '>']]]
            assert file_text.tokens_flat == ['<', 'bncDoc', 'xml', ':', 'id="A00"><teiHeader><fileDesc><titleStmt><title', '>', '[', 'ACET', 'factsheets', '&', 'amp', ';', 'newsletters', ']', '.', 'Sample', 'containing', 'about', '6688', 'words', 'of', 'miscellanea', '(', 'domain', ':', 'social', 'science', ')', '<', '/title><respStmt><resp', '>', 'Data', 'capture', 'and', 'transcription', '<', '/resp><name', '>', 'Oxford', 'University', 'Press', '<', '/name', '>', '<', '/respStmt></titleStmt><editionStmt><edition', '>', 'BNC', 'XML', 'Edition', ',', 'December', '2006</edition></editionStmt><extent', '>', '6688', 'tokens', ';', '6708', 'w', '-', 'units', ';', '423', 's', '-', 'units', '<', '/extent><publicationStmt><distributor', '>', 'Distributed', 'under', 'licence', 'by', 'Oxford', 'University', 'Computing', 'Services', 'on', 'behalf', 'of', 'the', 'BNC', 'Consortium.</distributor><availability', '>', 'This', 'material', 'is', 'protected', 'by', 'international', 'copyright', 'laws', 'and', 'may', 'not', 'be', 'copied', 'or', 'redistributed', 'in', 'any', 'way', '.', 'Consult', 'the', 'BNC', 'Web', 'Site', 'at', 'http://www.natcorp.ox.ac.uk', 'for', 'full', 'licencing', 'and', 'distribution', 'conditions.</availability><idno', 'type="bnc">A00</idno><idno', 'type="old', '"', '>', 'AidFct', '<', '/idno></publicationStmt><sourceDesc><bibl><title', '>', '[', 'ACET', 'factsheets', '&', 'amp', ';', 'newsletters', ']', '.', '<', '/title', '>', '<', 'imprint', 'n="AIDSCA1"><publisher', '>', 'Aids', 'Care', 'Education', '&', 'amp', ';', 'Training', '<', '/publisher', '>', '<', 'pubPlace', '>', 'London', '<', '/pubPlace', '>', '<', 'date', 'value="1991', '-', '09', '"', '>', '1991', '-', '09', '<', '/date', '>', '<', '/imprint', '>', '<', '/bibl></sourceDesc></fileDesc><encodingDesc><tagsDecl><namespace', 'name=""><tagUsage', 'gi="c', '"', 'occurs="810"/><tagUsage', 'gi="div', '"', 'occurs="43"/><tagUsage', 'gi="head', '"', 'occurs="45"/><tagUsage', 'gi="hi', '"', 'occurs="24"/><tagUsage', 'gi="item', '"', 'occurs="43"/><tagUsage', 'gi="label', '"', 'occurs="10"/><tagUsage', 'gi="list', '"', 'occurs="8"/><tagUsage', 'gi="mw', '"', 'occurs="31"/><tagUsage', 'gi="p', '"', 'occurs="118"/><tagUsage', 'gi="pb', '"', 'occurs="2"/><tagUsage', 'gi="s', '"', 'occurs="423"/><tagUsage', 'gi="w', '"', 'occurs="6708"/></namespace></tagsDecl></encodingDesc><profileDesc><creation', 'date="1991">1991', '-', '09', '<', '/creation><textClass><catRef', 'targets="WRI', 'ALLTIM3', 'ALLAVA2', 'ALLTYP5', 'WRIAAG0', 'WRIAD0', 'WRIASE0', 'WRIATY2', 'WRIAUD3', 'WRIDOM4', 'WRILEV2', 'WRIMED3', 'WRIPP5', 'WRISAM5', 'WRISTA2', 'WRITAS3"/><classCode', 'scheme="DLEE">W', 'nonAc', ':', 'medicine</classCode><keywords><term', '>', 'Health', '<', '/term><term', '>', 'Sex', '<', '/term></keywords></textClass></profileDesc><revisionDesc><change', 'date="2006', '-', '10', '-', '21', '"', 'who="#OUCS">Tag', 'usage', 'updated', 'for', 'BNC', '-', 'XML</change><change', 'date="2000', '-', '12', '-', '13', '"', 'who="#OUCS">Last', 'check', 'for', 'BNC', 'World', 'first', 'release</change><change', 'date="2000', '-', '09', '-', '06', '"', 'who="#OUCS">Redo', 'tagusage', 'tables</change><change', 'date="2000', '-', '09', '-', '01', '"', 'who="#OUCS">Check', 'all', 'tagcounts</change><change', 'date="2000', '-', '06', '-', '23', '"', 'who="#OUCS">Resequenced', 's', '-', 'units', 'and', 'added', 'headers</change><change', 'date="2000', '-', '01', '-', '21', '"', 'who="#OUCS">Added', 'date', 'info</change><change', 'date="2000', '-', '01', '-', '09', '"', 'who="#OUCS">Updated', 'all', 'catrefs</change><change', 'date="2000', '-', '01', '-', '08', '"', 'who="#OUCS">Manually', 'updated', 'tagcounts', ',', 'titlestmt', ',', 'and', 'title', 'in', 'source</change><change', 'date="1999', '-', '09', '-', '13', '"', 'who="#UCREL">POS', 'codes', 'revised', 'for', 'BNC-2', ';', 'header', 'updated</change><change', 'date="1994', '-', '11', '-', '24', '"', 'who="#dominic">Initial', 'accession', 'to', 'corpus</change></revisionDesc></teiHeader', '>', '<', 'wtext', 'type="NONAC"><div', 'level="1', '"', 'n="1', '"', 'type="leaflet"><head', 'type="MAIN', '"', '>', '<', 's', 'n="1"><w', 'c5="NN1', '"', 'hw="factsheet', '"', 'pos="SUBST">FACTSHEET', '<', '/w><w', 'c5="DTQ', '"', 'hw="what', '"', 'pos="PRON">WHAT', '<', '/w><w', 'c5="VBZ', '"', 'hw="be', '"', 'pos="VERB">IS', '<', '/w><w', 'c5="NN1', '"', 'hw="aids', '"', 'pos="SUBST">AIDS</w><c', 'c5="PUN">?</c></s></head><p', '>', '<', 's', 'n="2"><hi', 'rend="bo"><w', 'c5="NN1', '"', 'hw="aids', '"', 'pos="SUBST">AIDS', '<', '/w><c', 'c5="PUL">(</c><w', 'c5="VVN', '-', 'AJ0', '"', 'hw="acquire', '"', 'pos="VERB">Acquired', '<', '/w><w', 'c5="AJ0', '"', 'hw="immune', '"', 'pos="ADJ">Immune', '<', '/w><w', 'c5="NN1', '"', 'hw="deficiency', '"', 'pos="SUBST">Deficiency', '<', '/w><w', 'c5="NN1', '"', 'hw="syndrome', '"', 'pos="SUBST">Syndrome</w><c', 'c5="PUR">)</c></hi><w', 'c5="VBZ', '"', 'hw="be', '"', 'pos="VERB">is', '<', '/w><w', 'c5="AT0', '"', 'hw="a', '"', 'pos="ART">a', '<', '/w><w', 'c5="NN1', '"', 'hw="condition', '"', 'pos="SUBST">condition', '<', '/w><w', 'c5="VVN', '"', 'hw="cause', '"', 'pos="VERB">caused', '<', '/w><w', 'c5="PRP', '"', 'hw="by', '"', 'pos="PREP">by', '<', '/w><w', 'c5="AT0', '"', 'hw="a', '"', 'pos="ART">a', '<', '/w><w', 'c5="NN1', '"', 'hw="virus', '"', 'pos="SUBST">virus', '<', '/w><w', 'c5="VVN', '"', 'hw="call', '"', 'pos="VERB">called', '<', '/w><w', 'c5="NP0', '"', 'hw="hiv', '"', 'pos="SUBST">HIV', '<', '/w><c', 'c5="PUL">(</c><w', 'c5="AJ0', '-', 'NN1', '"', 'hw="human', '"', 'pos="ADJ">Human', '<', '/w><w', 'c5="NN1', '"', 'hw="immuno', '"', 'pos="SUBST">Immuno', '<', '/w><w', 'c5="NN1', '"', 'hw="deficiency', '"', 'pos="SUBST">Deficiency', '<', '/w><w', 'c5="NN1', '"', 'hw="virus', '"', 'pos="SUBST">Virus</w><c', 'c5="PUR">)</c><c', 'c5="PUN">.</c></s', '>', '<', 's', 'n="3"><w', 'c5="DT0', '"', 'hw="this', '"', 'pos="ADJ">This', '<', '/w><w', 'c5="NN1', '"', 'hw="virus', '"', 'pos="SUBST">virus', '<', '/w><w', 'c5="VVZ', '"', 'hw="affect', '"', 'pos="VERB">affects', '<', '/w><w', 'c5="AT0', '"', 'hw="the', '"', 'pos="ART">the', '<', '/w><w', 'c5="NN1', '"', 'hw="body', '"', 'pos="SUBST">body</w><w', 'c5="POS', '"', 'hw=', '"', "'s", '"', 'pos="UNC', '"', '>', "'s", '<', '/w><w', 'c5="NN1', '"', 'hw="defence', '"', 'pos="SUBST">defence', '<', '/w><w', 'c5="NN1', '"', 'hw="system', '"', 'pos="SUBST">system', '<', '/w><mw', 'c5="CJS"><w', 'c5="AV0', '"', 'hw="so', '"', 'pos="ADV">so', '<', '/w><w', 'c5="CJT', '"', 'hw="that', '"', 'pos="CONJ">that', '<', '/w></mw><w', 'c5="PNP', '"', 'hw="it', '"', 'pos="PRON">it', '<', '/w><w', 'c5="VM0', '"', 'hw="can', '"', 'pos="VERB">can</w><w', 'c5="XX0', '"', 'hw="not', '"', 'pos="ADV">not', '<', '/w><w', 'c5="VVI', '"', 'hw="fight', '"', 'pos="VERB">fight', '<', '/w><w', 'c5="NN1', '"', 'hw="infection', '"', 'pos="SUBST">infection</w><c', 'c5="PUN">.</c></s></p', '>']
            assert file_text.offsets_paras == [0, 361, 372, 403, 539]
            assert file_text.offsets_sentences == [0, 7, 15, 103, 125, 133, 361, 372, 403, 539]
        # Tokenized & Untagged
        elif file_name == 'XML File (5).xml':
            assert file_text.tokens_multilevel == [[['<bncDoc', 'xml:id="A00"><teiHeader><fileDesc><titleStmt><title>', '[ACET', 'factsheets', '&amp;', 'newsletters].'], ['Sample', 'containing', 'about', '6688', 'words', 'of', 'miscellanea', '(domain:', 'social', 'science)', '</title><respStmt><resp>', 'Data', 'capture', 'and', 'transcription', '</resp><name>', 'Oxford', 'University', 'Press', '</name>', '</respStmt></titleStmt><editionStmt><edition>BNC', 'XML', 'Edition,', 'December', '2006</edition></editionStmt><extent>', '6688', 'tokens;', '6708', 'w-units;', '423', 's-units', '</extent><publicationStmt><distributor>Distributed', 'under', 'licence', 'by', 'Oxford', 'University', 'Computing', 'Services', 'on', 'behalf', 'of', 'the', 'BNC', 'Consortium.</distributor><availability>', 'This', 'material', 'is', 'protected', 'by', 'international', 'copyright', 'laws', 'and', 'may', 'not', 'be', 'copied', 'or', 'redistributed', 'in', 'any', 'way.'], ['Consult', 'the', 'BNC', 'Web', 'Site', 'at', 'http://www.natcorp.ox.ac.uk', 'for', 'full', 'licencing', 'and', 'distribution', 'conditions.</availability><idno', 'type="bnc">A00</idno><idno', 'type="old">', 'AidFct', '</idno></publicationStmt><sourceDesc><bibl><title>', '[ACET', 'factsheets', '&amp;', 'newsletters].'], ['</title>', '<imprint', 'n="AIDSCA1"><publisher>', 'Aids', 'Care', 'Education', '&amp;', 'Training', '</publisher>', '<pubPlace>', 'London', '</pubPlace>', '<date', 'value="1991-09">', '1991-09', '</date>', '</imprint>', '</bibl></sourceDesc></fileDesc><encodingDesc><tagsDecl><namespace', 'name=""><tagUsage', 'gi="c"', 'occurs="810"/><tagUsage', 'gi="div"', 'occurs="43"/><tagUsage', 'gi="head"', 'occurs="45"/><tagUsage', 'gi="hi"', 'occurs="24"/><tagUsage', 'gi="item"', 'occurs="43"/><tagUsage', 'gi="label"', 'occurs="10"/><tagUsage', 'gi="list"', 'occurs="8"/><tagUsage', 'gi="mw"', 'occurs="31"/><tagUsage', 'gi="p"', 'occurs="118"/><tagUsage', 'gi="pb"', 'occurs="2"/><tagUsage', 'gi="s"', 'occurs="423"/><tagUsage', 'gi="w"', 'occurs="6708"/></namespace></tagsDecl></encodingDesc><profileDesc><creation', 'date="1991">1991-09', '</creation><textClass><catRef', 'targets="WRI', 'ALLTIM3', 'ALLAVA2', 'ALLTYP5', 'WRIAAG0', 'WRIAD0', 'WRIASE0', 'WRIATY2', 'WRIAUD3', 'WRIDOM4', 'WRILEV2', 'WRIMED3', 'WRIPP5', 'WRISAM5', 'WRISTA2', 'WRITAS3"/><classCode', 'scheme="DLEE">W', 'nonAc:', 'medicine</classCode><keywords><term>', 'Health', '</term><term>', 'Sex', '</term></keywords></textClass></profileDesc><revisionDesc><change', 'date="2006-10-21"', 'who="#OUCS">Tag', 'usage', 'updated', 'for', 'BNC-XML</change><change', 'date="2000-12-13"', 'who="#OUCS">Last', 'check', 'for', 'BNC', 'World', 'first', 'release</change><change', 'date="2000-09-06"', 'who="#OUCS">Redo', 'tagusage', 'tables</change><change', 'date="2000-09-01"', 'who="#OUCS">Check', 'all', 'tagcounts</change><change', 'date="2000-06-23"', 'who="#OUCS">Resequenced', 's-units', 'and', 'added', 'headers</change><change', 'date="2000-01-21"', 'who="#OUCS">Added', 'date', 'info</change><change', 'date="2000-01-09"', 'who="#OUCS">Updated', 'all', 'catrefs</change><change', 'date="2000-01-08"', 'who="#OUCS">Manually', 'updated', 'tagcounts,', 'titlestmt,', 'and', 'title', 'in', 'source</change><change', 'date="1999-09-13"', 'who="#UCREL">POS', 'codes', 'revised', 'for', 'BNC-2;', 'header', 'updated</change><change', 'date="1994-11-24"', 'who="#dominic">Initial', 'accession', 'to', 'corpus</change></revisionDesc></teiHeader>']], [['<wtext', 'type="NONAC"><div', 'level="1"', 'n="1"', 'type="leaflet"><head', 'type="MAIN">']], [['<s', 'n="1"><w', 'c5="NN1"', 'hw="factsheet"', 'pos="SUBST">FACTSHEET', '</w><w', 'c5="DTQ"', 'hw="what"', 'pos="PRON">WHAT', '</w><w', 'c5="VBZ"', 'hw="be"', 'pos="VERB">IS', '</w><w', 'c5="NN1"', 'hw="aids"', 'pos="SUBST">AIDS</w><c', 'c5="PUN">?</c></s></head><p>']], [['<s', 'n="2"><hi', 'rend="bo"><w', 'c5="NN1"', 'hw="aids"', 'pos="SUBST">AIDS', '</w><c', 'c5="PUL">(</c><w', 'c5="VVN-AJ0"', 'hw="acquire"', 'pos="VERB">Acquired', '</w><w', 'c5="AJ0"', 'hw="immune"', 'pos="ADJ">Immune', '</w><w', 'c5="NN1"', 'hw="deficiency"', 'pos="SUBST">Deficiency', '</w><w', 'c5="NN1"', 'hw="syndrome"', 'pos="SUBST">Syndrome</w><c', 'c5="PUR">)</c></hi><w', 'c5="VBZ"', 'hw="be"', 'pos="VERB">is', '</w><w', 'c5="AT0"', 'hw="a"', 'pos="ART">a', '</w><w', 'c5="NN1"', 'hw="condition"', 'pos="SUBST">condition', '</w><w', 'c5="VVN"', 'hw="cause"', 'pos="VERB">caused', '</w><w', 'c5="PRP"', 'hw="by"', 'pos="PREP">by', '</w><w', 'c5="AT0"', 'hw="a"', 'pos="ART">a', '</w><w', 'c5="NN1"', 'hw="virus"', 'pos="SUBST">virus', '</w><w', 'c5="VVN"', 'hw="call"', 'pos="VERB">called', '</w><w', 'c5="NP0"', 'hw="hiv"', 'pos="SUBST">HIV', '</w><c', 'c5="PUL">(</c><w', 'c5="AJ0-NN1"', 'hw="human"', 'pos="ADJ">Human', '</w><w', 'c5="NN1"', 'hw="immuno"', 'pos="SUBST">Immuno', '</w><w', 'c5="NN1"', 'hw="deficiency"', 'pos="SUBST">Deficiency', '</w><w', 'c5="NN1"', 'hw="virus"', 'pos="SUBST">Virus</w><c', 'c5="PUR">)</c><c', 'c5="PUN">.</c></s>']], [['<s', 'n="3"><w', 'c5="DT0"', 'hw="this"', 'pos="ADJ">This', '</w><w', 'c5="NN1"', 'hw="virus"', 'pos="SUBST">virus', '</w><w', 'c5="VVZ"', 'hw="affect"', 'pos="VERB">affects', '</w><w', 'c5="AT0"', 'hw="the"', 'pos="ART">the', '</w><w', 'c5="NN1"', 'hw="body"', 'pos="SUBST">body</w><w', 'c5="POS"', 'hw="\'s"', 'pos="UNC">\'s', '</w><w', 'c5="NN1"', 'hw="defence"', 'pos="SUBST">defence', '</w><w', 'c5="NN1"', 'hw="system"', 'pos="SUBST">system', '</w><mw', 'c5="CJS"><w', 'c5="AV0"', 'hw="so"', 'pos="ADV">so', '</w><w', 'c5="CJT"', 'hw="that"', 'pos="CONJ">that', '</w></mw><w', 'c5="PNP"', 'hw="it"', 'pos="PRON">it', '</w><w', 'c5="VM0"', 'hw="can"', 'pos="VERB">can</w><w', 'c5="XX0"', 'hw="not"', 'pos="ADV">not', '</w><w', 'c5="VVI"', 'hw="fight"', 'pos="VERB">fight', '</w><w', 'c5="NN1"', 'hw="infection"', 'pos="SUBST">infection</w><c', 'c5="PUN">.</c></s></p>']]]
            assert file_text.tokens_flat == ['<bncDoc', 'xml:id="A00"><teiHeader><fileDesc><titleStmt><title>', '[ACET', 'factsheets', '&amp;', 'newsletters].', 'Sample', 'containing', 'about', '6688', 'words', 'of', 'miscellanea', '(domain:', 'social', 'science)', '</title><respStmt><resp>', 'Data', 'capture', 'and', 'transcription', '</resp><name>', 'Oxford', 'University', 'Press', '</name>', '</respStmt></titleStmt><editionStmt><edition>BNC', 'XML', 'Edition,', 'December', '2006</edition></editionStmt><extent>', '6688', 'tokens;', '6708', 'w-units;', '423', 's-units', '</extent><publicationStmt><distributor>Distributed', 'under', 'licence', 'by', 'Oxford', 'University', 'Computing', 'Services', 'on', 'behalf', 'of', 'the', 'BNC', 'Consortium.</distributor><availability>', 'This', 'material', 'is', 'protected', 'by', 'international', 'copyright', 'laws', 'and', 'may', 'not', 'be', 'copied', 'or', 'redistributed', 'in', 'any', 'way.', 'Consult', 'the', 'BNC', 'Web', 'Site', 'at', 'http://www.natcorp.ox.ac.uk', 'for', 'full', 'licencing', 'and', 'distribution', 'conditions.</availability><idno', 'type="bnc">A00</idno><idno', 'type="old">', 'AidFct', '</idno></publicationStmt><sourceDesc><bibl><title>', '[ACET', 'factsheets', '&amp;', 'newsletters].', '</title>', '<imprint', 'n="AIDSCA1"><publisher>', 'Aids', 'Care', 'Education', '&amp;', 'Training', '</publisher>', '<pubPlace>', 'London', '</pubPlace>', '<date', 'value="1991-09">', '1991-09', '</date>', '</imprint>', '</bibl></sourceDesc></fileDesc><encodingDesc><tagsDecl><namespace', 'name=""><tagUsage', 'gi="c"', 'occurs="810"/><tagUsage', 'gi="div"', 'occurs="43"/><tagUsage', 'gi="head"', 'occurs="45"/><tagUsage', 'gi="hi"', 'occurs="24"/><tagUsage', 'gi="item"', 'occurs="43"/><tagUsage', 'gi="label"', 'occurs="10"/><tagUsage', 'gi="list"', 'occurs="8"/><tagUsage', 'gi="mw"', 'occurs="31"/><tagUsage', 'gi="p"', 'occurs="118"/><tagUsage', 'gi="pb"', 'occurs="2"/><tagUsage', 'gi="s"', 'occurs="423"/><tagUsage', 'gi="w"', 'occurs="6708"/></namespace></tagsDecl></encodingDesc><profileDesc><creation', 'date="1991">1991-09', '</creation><textClass><catRef', 'targets="WRI', 'ALLTIM3', 'ALLAVA2', 'ALLTYP5', 'WRIAAG0', 'WRIAD0', 'WRIASE0', 'WRIATY2', 'WRIAUD3', 'WRIDOM4', 'WRILEV2', 'WRIMED3', 'WRIPP5', 'WRISAM5', 'WRISTA2', 'WRITAS3"/><classCode', 'scheme="DLEE">W', 'nonAc:', 'medicine</classCode><keywords><term>', 'Health', '</term><term>', 'Sex', '</term></keywords></textClass></profileDesc><revisionDesc><change', 'date="2006-10-21"', 'who="#OUCS">Tag', 'usage', 'updated', 'for', 'BNC-XML</change><change', 'date="2000-12-13"', 'who="#OUCS">Last', 'check', 'for', 'BNC', 'World', 'first', 'release</change><change', 'date="2000-09-06"', 'who="#OUCS">Redo', 'tagusage', 'tables</change><change', 'date="2000-09-01"', 'who="#OUCS">Check', 'all', 'tagcounts</change><change', 'date="2000-06-23"', 'who="#OUCS">Resequenced', 's-units', 'and', 'added', 'headers</change><change', 'date="2000-01-21"', 'who="#OUCS">Added', 'date', 'info</change><change', 'date="2000-01-09"', 'who="#OUCS">Updated', 'all', 'catrefs</change><change', 'date="2000-01-08"', 'who="#OUCS">Manually', 'updated', 'tagcounts,', 'titlestmt,', 'and', 'title', 'in', 'source</change><change', 'date="1999-09-13"', 'who="#UCREL">POS', 'codes', 'revised', 'for', 'BNC-2;', 'header', 'updated</change><change', 'date="1994-11-24"', 'who="#dominic">Initial', 'accession', 'to', 'corpus</change></revisionDesc></teiHeader>', '<wtext', 'type="NONAC"><div', 'level="1"', 'n="1"', 'type="leaflet"><head', 'type="MAIN">', '<s', 'n="1"><w', 'c5="NN1"', 'hw="factsheet"', 'pos="SUBST">FACTSHEET', '</w><w', 'c5="DTQ"', 'hw="what"', 'pos="PRON">WHAT', '</w><w', 'c5="VBZ"', 'hw="be"', 'pos="VERB">IS', '</w><w', 'c5="NN1"', 'hw="aids"', 'pos="SUBST">AIDS</w><c', 'c5="PUN">?</c></s></head><p>', '<s', 'n="2"><hi', 'rend="bo"><w', 'c5="NN1"', 'hw="aids"', 'pos="SUBST">AIDS', '</w><c', 'c5="PUL">(</c><w', 'c5="VVN-AJ0"', 'hw="acquire"', 'pos="VERB">Acquired', '</w><w', 'c5="AJ0"', 'hw="immune"', 'pos="ADJ">Immune', '</w><w', 'c5="NN1"', 'hw="deficiency"', 'pos="SUBST">Deficiency', '</w><w', 'c5="NN1"', 'hw="syndrome"', 'pos="SUBST">Syndrome</w><c', 'c5="PUR">)</c></hi><w', 'c5="VBZ"', 'hw="be"', 'pos="VERB">is', '</w><w', 'c5="AT0"', 'hw="a"', 'pos="ART">a', '</w><w', 'c5="NN1"', 'hw="condition"', 'pos="SUBST">condition', '</w><w', 'c5="VVN"', 'hw="cause"', 'pos="VERB">caused', '</w><w', 'c5="PRP"', 'hw="by"', 'pos="PREP">by', '</w><w', 'c5="AT0"', 'hw="a"', 'pos="ART">a', '</w><w', 'c5="NN1"', 'hw="virus"', 'pos="SUBST">virus', '</w><w', 'c5="VVN"', 'hw="call"', 'pos="VERB">called', '</w><w', 'c5="NP0"', 'hw="hiv"', 'pos="SUBST">HIV', '</w><c', 'c5="PUL">(</c><w', 'c5="AJ0-NN1"', 'hw="human"', 'pos="ADJ">Human', '</w><w', 'c5="NN1"', 'hw="immuno"', 'pos="SUBST">Immuno', '</w><w', 'c5="NN1"', 'hw="deficiency"', 'pos="SUBST">Deficiency', '</w><w', 'c5="NN1"', 'hw="virus"', 'pos="SUBST">Virus</w><c', 'c5="PUR">)</c><c', 'c5="PUN">.</c></s>', '<s', 'n="3"><w', 'c5="DT0"', 'hw="this"', 'pos="ADJ">This', '</w><w', 'c5="NN1"', 'hw="virus"', 'pos="SUBST">virus', '</w><w', 'c5="VVZ"', 'hw="affect"', 'pos="VERB">affects', '</w><w', 'c5="AT0"', 'hw="the"', 'pos="ART">the', '</w><w', 'c5="NN1"', 'hw="body"', 'pos="SUBST">body</w><w', 'c5="POS"', 'hw="\'s"', 'pos="UNC">\'s', '</w><w', 'c5="NN1"', 'hw="defence"', 'pos="SUBST">defence', '</w><w', 'c5="NN1"', 'hw="system"', 'pos="SUBST">system', '</w><mw', 'c5="CJS"><w', 'c5="AV0"', 'hw="so"', 'pos="ADV">so', '</w><w', 'c5="CJT"', 'hw="that"', 'pos="CONJ">that', '</w></mw><w', 'c5="PNP"', 'hw="it"', 'pos="PRON">it', '</w><w', 'c5="VM0"', 'hw="can"', 'pos="VERB">can</w><w', 'c5="XX0"', 'hw="not"', 'pos="ADV">not', '</w><w', 'c5="VVI"', 'hw="fight"', 'pos="VERB">fight', '</w><w', 'c5="NN1"', 'hw="infection"', 'pos="SUBST">infection</w><c', 'c5="PUN">.</c></s></p>']
            assert file_text.offsets_paras == [0, 216, 222, 240, 318]
            assert file_text.offsets_sentences == [0, 6, 69, 90, 216, 222, 240, 318]

        assert file_text.tags == [[] for i in file_text.tokens_flat]
    # TMX files
    elif len(new_files) == 2:
        file_text_src = new_files[0]['text']
        file_text_tgt = new_files[1]['text']

        # Source files
        print(file_text_src.lang)
        print(file_text_src.tokens_multilevel)
        print(file_text_src.tokens_flat)
        print(file_text_src.tags)
        print(file_text_src.offsets_paras)
        print(file_text_src.offsets_sentences)

        assert file_text_src.lang == 'eng_us'
        assert file_text_src.tokens_multilevel == [[['Hello', 'world', '!']]]
        assert file_text_src.tokens_flat == ['Hello', 'world', '!']
        assert file_text_src.offsets_paras == [0]
        assert file_text_src.offsets_sentences == [0]

        # Target files
        print(file_text_tgt.lang)
        print(file_text_tgt.tokens_multilevel)
        print(file_text_tgt.tokens_flat)
        print(file_text_tgt.tags)
        print(file_text_tgt.offsets_paras)
        print(file_text_tgt.offsets_sentences)

        assert file_text_tgt.lang == 'fra'
        assert file_text_tgt.tokens_multilevel == [[['Bonjour', 'tout', 'le', 'monde', '!']]]
        assert file_text_tgt.tokens_flat == ['Bonjour', 'tout', 'le', 'monde', '!']
        assert file_text_tgt.offsets_paras == [0]
        assert file_text_tgt.offsets_sentences == [0]

def update_gui_unicode_decode_error(err_msg, new_files):
    assert not err_msg

    assert new_files[0]['encoding'] == 'utf_8'

def update_gui_tags(err_msg, new_files):
    assert not err_msg

    file_name = os.path.split(new_files[0]['path'])[1]
    file_text = new_files[0]['text']

    print(file_text.tokens_multilevel)
    print(file_text.tokens_flat)
    print(file_text.tags)
    print(file_text.offsets_paras)
    print(file_text.offsets_sentences)

    if file_name == 'untokenized_untagged.txt':
        assert file_text.tokens_multilevel == [[], [], [['This', '<', 'TAG', '>', 'is', 'the', 'first', 'sentence', '.'], ['This', 'is', 'the', 'second', 'sentence', '.']], [], [], [['This', 'is', 'the', 'third', 'sentence', '.']], [], []]
        assert file_text.tokens_flat == ['This', '<', 'TAG', '>', 'is', 'the', 'first', 'sentence', '.', 'This', 'is', 'the', 'second', 'sentence', '.', 'This', 'is', 'the', 'third', 'sentence', '.']
        assert file_text.tags == [[] for i in file_text.tokens_flat]
        assert file_text.offsets_paras == [0, 0, 0, 15, 15, 15, 21, 21]
        assert file_text.offsets_sentences == [0, 9, 15]
    elif file_name == 'untokenized_tagged.txt':
        assert file_text.tokens_multilevel == [[['']], [], [['This', 'is', 'the', 'first', 'sentence', '.'], ['This', 'is', 'the', 'second', 'sentence', '.']], [], [], [['This', 'is', 'the', 'third', 'sentence', '.']], [], []]
        assert file_text.tokens_flat == ['', 'This', 'is', 'the', 'first', 'sentence', '.', 'This', 'is', 'the', 'second', 'sentence', '.', 'This', 'is', 'the', 'third', 'sentence', '.']
        assert file_text.tags == [['<TAG1>'], ['<TAG2>'], ['</TAG2>'], [], [], [], [], ['_TAG3'], [], [], [], [], [], [], [], [], [], [], ['<TAG4>', '</TAG4>']]
        assert file_text.offsets_paras == [0, 1, 1, 13, 13, 13, 19, 19]
        assert file_text.offsets_sentences == [0, 1, 7, 13]
    elif file_name == 'tokenized_untagged.txt':
        assert file_text.tokens_multilevel == [[], [], [['This', '<TAG>is', 'the', 'first', 'sentence', '.'], ['This', 'is', 'the', 'second', 'sentence', '.']], [], [], [['This', 'is', 'the', 'third', 'sentence', '.']], [], []]
        assert file_text.tokens_flat == ['This', '<TAG>is', 'the', 'first', 'sentence', '.', 'This', 'is', 'the', 'second', 'sentence', '.', 'This', 'is', 'the', 'third', 'sentence', '.']
        assert file_text.tags == [[] for i in file_text.tokens_flat]
        assert file_text.offsets_paras == [0, 0, 0, 12, 12, 12, 18, 18]
        assert file_text.offsets_sentences == [0, 6, 12]
    elif file_name == 'tokenized_tagged.txt':
        assert file_text.tokens_multilevel == [[['']], [], [['This', 'is', 'the', 'first', 'sentence', '.'], ['This', 'is', 'the', 'second', 'sentence', '.']], [], [], [['This', 'is', 'the', 'third', 'sentence', '.']], [], []]
        assert file_text.tokens_flat == ['', 'This', 'is', 'the', 'first', 'sentence', '.', 'This', 'is', 'the', 'second', 'sentence', '.', 'This', 'is', 'the', 'third', 'sentence', '.']
        assert file_text.tags == [['<TAG1>'], ['<TAG2>'], ['</TAG2>'], [], [], [], [], ['_TAG3RunningToken_TAG3'], [], [], [], [], [], [], [], [], [], [], ['<TAG4>', '</TAG4>']]
        assert file_text.offsets_paras == [0, 1, 1, 13, 13, 13, 19, 19]
        assert file_text.offsets_sentences == [0, 1, 7, 13]

    assert len(file_text.tokens_flat) == len(file_text.tags)

if __name__ == '__main__':
    test_file_area_file_types()

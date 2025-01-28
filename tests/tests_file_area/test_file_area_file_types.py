# ----------------------------------------------------------------------
# Tests: File area - File types
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

import glob
import os
import time

from PyQt5.QtCore import QObject

from tests import wl_test_init
from wordless import wl_file_area
from wordless.wl_dialogs import wl_dialogs_misc
from wordless.wl_nlp import wl_texts

main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')

def add_file(file_paths, update_gui, file_type = 'observed'):
    def open_file(err_msg, files_to_open):
        assert not err_msg

        # Untokenized & Untagged
        if files_to_open[-1]['path'].endswith('xml (4).xml'):
            files_to_open[-1]['tokenized'] = False
            files_to_open[-1]['tagged'] = False
        # Tokenized & Untagged
        elif files_to_open[-1]['path'].endswith('xml (5).xml'):
            files_to_open[-1]['tokenized'] = True
            files_to_open[-1]['tagged'] = False

        wl_file_area.Wl_Worker_Open_Files(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(main, text = ''),
            update_gui = update_gui,
            files_to_open = files_to_open,
            file_type = file_type
        ).run()

        print(f'Done! (In {round(time.time() - time_start, 2)} seconds)\n')

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
    wl_test_init.clean_import_caches()

    # Disable auto-detection
    main.settings_custom['file_area']['dialog_open_files']['auto_detect_encodings'] = False
    main.settings_custom['file_area']['dialog_open_files']['auto_detect_langs'] = False

    # File types (Non-XML)
    files_non_xml = glob.glob('tests/files/wl_file_area/file_types/*.*')
    files_non_xml = [file for file in files_non_xml if not file.endswith('.xml')]

    add_file(
        file_paths = files_non_xml,
        update_gui = update_gui_file_types
    )

    # Modify default file settings for XML files
    main.settings_custom['files']['default_settings']['tokenized'] = True
    main.settings_custom['files']['default_settings']['tagged'] = True

    # File types (XML)
    for i in range(5):
        match i:
            case 0 | 3 | 4:
                main.settings_custom['files']['tags']['xml_tag_settings'] = [
                    ['Non-embedded', 'Paragraph', '<p>', '</p>'],
                    ['Non-embedded', 'Paragraph', '<head>', '</head>'],
                    ['Non-embedded', 'Sentence', '<s>', '</s>'],
                    ['Non-embedded', 'Word', '<w>', '</w>'],
                    ['Non-embedded', 'Word', '<c>', '</c>']
                ]
            # XML tags unfound
            case 1:
                main.settings_custom['files']['tags']['xml_tag_settings'] = [
                    ['Non-embedded', 'Paragraph', '<pp>', '</pp>'],
                    ['Non-embedded', 'Sentence', '<ss>', '</ss>'],
                    ['Non-embedded', 'Word', '<ww>', '</ww>'],
                ]
            # XML tags unspecified
            case 2:
                main.settings_custom['files']['tags']['xml_tag_settings'] = []

        add_file(
            file_paths = glob.glob('tests/files/wl_file_area/file_types/*.xml'),
            update_gui = update_gui_file_types
        )

    main.settings_custom['files']['default_settings']['tokenized'] = False
    main.settings_custom['files']['default_settings']['tagged'] = False

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

        tokens = file_text.to_token_texts()
        tags = file_text.get_token_properties('tag', flat = True)

        print(tokens)

        match file_name:
            # CSV files
            case 'csv.txt':
                assert tokens == [[], [], [[['3-2', '3-3']]], [], [], [[['6-2', '6-3']]], [], []]
            # Excel workbooks
            case 'xlsx.txt':
                assert tokens == [[], [[['B2', '&', 'C2', 'D2']]], [[['B3', '&', 'B4', 'C3', 'D3']]], [[['C4', 'D4']]], [[['5', 'B5', 'C5', 'D5']]]]
            # HTML pages
            case 'html.txt':
                assert tokens == [[], [], [[['This', 'is', 'a', 'title']]], [], [], [[['Hello', 'world', '!']]], [], []]
            # Lyrics files
            case 'lrc.txt':
                assert tokens == [[], [[['Lyrics', 'line', '1']]], [[['Lyrics', 'line', '2', '(', 'with', 'invalid', 'time', 'tags', ')']]], [[['Repeating', 'lyrics', 'line', '3', '&', '5', '(', 'with', 'whitespace', ')']]], [[['Repeating', 'lyrics', 'line', '4', '&', '6']]], [[['Repeating', 'lyrics', 'line', '3', '&', '5', '(', 'with', 'whitespace', ')']]], [[['Repeating', 'lyrics', 'line', '4', '&', '6']]], [], [[['Lyrics', 'line', '7', '(', '3-digit', 'after', 'seconds', ')']]], [[['Lyrics', 'line', '8', '(', 'colon', 'separator', 'after', 'seconds', ')']]], [[['Lyrics', 'line', '9', '[', 'with', 'lyrics', 'in', 'square', 'brackets', 'at', 'the', 'end', ']']]], [[['Lyrics', 'line', '10', '(', 'with', 'word', 'time', 'tags', ')']]], [[['<', 'With', 'lyrics', 'in', 'angle', 'brackets', 'at', 'the', 'beginning', '>', 'Lyrics', 'line', '11', '<', 'with', 'lyrics', 'in', 'angle', 'brackets', 'at', 'the', 'end', ')']]], []]
            # PDF files
            case 'pdf.txt':
                assert tokens == [[[['Lorem', 'ipsum', 'dolor', 'sit', 'amet', ','], ['consetetur', 'sadipscing', 'elitr', ','], ['sed', 'diam', 'nonumy', 'eirmod']]], [[['tempor', 'invidunt', 'ut', 'labore', 'et', 'dolore', 'magna', 'aliquyam', 'erat', ','], ['sed', 'diam', 'voluptua', '.']], [['At', 'vero']]], [[['eos', 'et', 'accusam', 'et', 'justo', 'duo', 'dolores', 'et', 'ea', 'rebum', '.']], [['Stet', 'clita', 'kasd', 'gubergren', ','], ['no', 'sea', 'taki-']]], [[['mata', 'sanctus', 'est', 'Lorem', 'ipsum', 'dolor', 'sit', 'amet', '.']], [['Lorem', 'ipsum', 'dolor', 'sit', 'amet', ','], ['consetetur']]], [[['sadipscing', 'elitr', ','], ['sed', 'diam', 'nonumy', 'eirmod', 'tempor', 'invidunt', 'ut', 'labore', 'et', 'dolore', 'magna']]], [[['aliquyam', 'erat', ','], ['sed', 'diam', 'voluptua', '.']], [['At', 'vero', 'eos', 'et', 'accusam', 'et', 'justo', 'duo', 'dolores', 'et', 'ea']]], [[['rebum', '.']], [['Stet', 'clita', 'kasd', 'gubergren', ','], ['no', 'sea', 'takimata', 'sanctus', 'est', 'Lorem', 'ipsum', 'dolor', 'sit']]], [[['amet', '.']]], [[['1']]]]
            # PowerPoint presentations
            case 'pptx.txt':
                assert tokens == [[[['Slide', '1', 'title']]], [[['Slide', '1', 'subtitle']]], [[['Slide', '2', 'title']]], [[['Slide', '2', 'paragraph', '1']]], [], [[['Slide', '2', 'paragraph', '2']]], [[['Slide', '2', 'paragraph', '3']]], [], [[['Slide', '3', 'title']]], [[['Slide', '3', 'text', 'box']]]]
            # Word documents
            case 'docx.txt':
                assert tokens == [[], [[['Heading']]], [], [], [[['This', 'is', 'the', 'first', 'sentence', '.']], [['This', 'is', 'the', 'second', 'sentence', '.']]], [[['This', 'is', 'the', 'third', 'sentence', '.']]], [], [], [[['2-2/3', '2-4']]], [[['3/4-2', '3-3', '3-4']]], [[['4-3', '4-4', '4-4-1/2', '4-4-3/5', '4-4-4', '4-4-6']]], [], []]
            # XML files
            case 'xml.xml':
                assert tokens == [[[['FACTSHEET', 'WHAT', 'IS', 'AIDS', '?']]], [[['AIDS', '(', 'Acquired', 'Immune', 'Deficiency', 'Syndrome', ')', 'is', 'a', 'condition', 'caused', 'by', 'a', 'virus', 'called', 'HIV', '(', 'Human', 'Immuno', 'Deficiency', 'Virus', ')', '.']], [['This', 'virus', 'affects', 'the', 'body', "'s", 'defence', 'system', 'so', 'that', 'it', 'can', 'not', 'fight', 'infection', '.']]]]
            # XML tags unfound or unspecified
            case 'xml (2).xml' | 'xml (3).xml':
                assert tokens == [[], [], [[['FACTSHEET', 'WHAT', 'IS', 'AIDS', '?']]], [[['AIDS', '(', 'Acquired', 'Immune', 'Deficiency', 'Syndrome', ')', 'is', 'a', 'condition', 'caused', 'by', 'a', 'virus', 'called', 'HIV', '(', 'Human', 'Immuno', 'Deficiency', 'Virus', ')', '.']]], [[['This', 'virus', 'affects', 'the', 'body', "'s", 'defence', 'system', 'so', 'that', 'it', 'can', 'not', 'fight', 'infection', '.']]]]
            # Untokenized & Untagged
            case 'xml (4).xml':
                assert tokens == [[[['<', 'bncDoc', 'xml', ':'], ['id=', "''", 'A00', "''", '>', '<', 'teiHeader', '>', '<', 'fileDesc', '>', '<', 'titleStmt', '>', '<', 'title', '>', '[', 'ACET', 'factsheets', '&', 'amp', ';'], ['newsletters', ']', '.']], [['Sample', 'containing', 'about', '6688', 'words', 'of', 'miscellanea', '(', 'domain', ':'], ['social', 'science', ')', '<', '/title', '>', '<', 'respStmt', '>', '<', 'resp', '>', 'Data', 'capture', 'and', 'transcription', '<', '/resp', '>', '<', 'name', '>', 'Oxford', 'University', 'Press', '<', '/name', '>', '<', '/respStmt', '>', '<', '/titleStmt', '>', '<', '/fileDesc', '>', '<', '/teiHeader', '>']]], [[['<', 'wtext', 'type=', "''", 'NONAC', "''", '>', '<', 'div', 'level=', "''", '1', "''", 'n=', "''", '1', "''", 'type=', "''", 'leaflet', "''", '>', '<', 'head', 'type=', "''", 'MAIN', "''", '>']]], [[['<', 's', 'n=', "''", '1', "''", '>', '<', 'w', 'c5=', "''", 'NN1', "''", 'hw=', "''", 'factsheet', "''", 'pos=', "''", 'SUBST', "''", '>', 'FACTSHEET', '<', '/w', '>', '<', 'w', 'c5=', "''", 'DTQ', "''", 'hw=', "''", 'what', "''", 'pos=', "''", 'PRON', "''", '>', 'WHAT', '<', '/w', '>', '<', 'w', 'c5=', "''", 'VBZ', "''", 'hw=', "''", 'be', "''", 'pos=', "''", 'VERB', "''", '>', 'IS', '<', '/w', '>', '<', 'w', 'c5=', "''", 'NN1', "''", 'hw=', "''", 'aids', "''", 'pos=', "''", 'SUBST', "''", '>', 'AIDS', '<', '/w', '>', '<', 'c', 'c5=', "''", 'PUN', "''", '>', '?'], ['<', '/c', '>', '<', '/s', '>', '<', '/head', '>', '<', 'p', '>']]], [[['<', 's', 'n=', "''", '2', "''", '>', '<', 'hi', 'rend=', "''", 'bo', "''", '>', '<', 'w', 'c5=', "''", 'NN1', "''", 'hw=', "''", 'aids', "''", 'pos=', "''", 'SUBST', "''", '>', 'AIDS', '<', '/w', '>', '<', 'c', 'c5=', "''", 'PUL', "''", '>', '(', '<', '/c', '>', '<', 'w', 'c5=', "''", 'VVN-AJ0', "''", 'hw=', "''", 'acquire', "''", 'pos=', "''", 'VERB', "''", '>', 'Acquired', '<', '/w', '>', '<', 'w', 'c5=', "''", 'AJ0', "''", 'hw=', "''", 'immune', "''", 'pos=', "''", 'ADJ', "''", '>', 'Immune', '<', '/w', '>', '<', 'w', 'c5=', "''", 'NN1', "''", 'hw=', "''", 'deficiency', "''", 'pos=', "''", 'SUBST', "''", '>', 'Deficiency', '<', '/w', '>', '<', 'w', 'c5=', "''", 'NN1', "''", 'hw=', "''", 'syndrome', "''", 'pos=', "''", 'SUBST', "''", '>', 'Syndrome', '<', '/w', '>', '<', 'c', 'c5=', "''", 'PUR', "''", '>', ')', '<', '/c', '>', '<', '/hi', '>', '<', 'w', 'c5=', "''", 'VBZ', "''", 'hw=', "''", 'be', "''", 'pos=', "''", 'VERB', "''", '>', 'is', '<', '/w', '>', '<', 'w', 'c5=', "''", 'AT0', "''", 'hw=', "''", 'a', "''", 'pos=', "''", 'ART', "''", '>', 'a', '<', '/w', '>', '<', 'w', 'c5=', "''", 'NN1', "''", 'hw=', "''", 'condition', "''", 'pos=', "''", 'SUBST', "''", '>', 'condition', '<', '/w', '>', '<', 'w', 'c5=', "''", 'VVN', "''", 'hw=', "''", 'cause', "''", 'pos=', "''", 'VERB', "''", '>', 'caused', '<', '/w', '>', '<', 'w', 'c5=', "''", 'PRP', "''", 'hw=', "''", 'by', "''", 'pos=', "''", 'PREP', "''", '>', 'by', '<', '/w', '>', '<', 'w', 'c5=', "''", 'AT0', "''", 'hw=', "''", 'a', "''", 'pos=', "''", 'ART', "''", '>', 'a', '<', '/w', '>', '<', 'w', 'c5=', "''", 'NN1', "''", 'hw=', "''", 'virus', "''", 'pos=', "''", 'SUBST', "''", '>', 'virus', '<', '/w', '>', '<', 'w', 'c5=', "''", 'VVN', "''", 'hw=', "''", 'call', "''", 'pos=', "''", 'VERB', "''", '>', 'called', '<', '/w', '>', '<', 'w', 'c5=', "''", 'NP0', "''", 'hw=', "''", 'hiv', "''", 'pos=', "''", 'SUBST', "''", '>', 'HIV', '<', '/w', '>', '<', 'c', 'c5=', "''", 'PUL', "''", '>', '(', '<', '/c', '>', '<', 'w', 'c5=', "''", 'AJ0-NN1', "''", 'hw=', "''", 'human', "''", 'pos=', "''", 'ADJ', "''", '>', 'Human', '<', '/w', '>', '<', 'w', 'c5=', "''", 'NN1', "''", 'hw=', "''", 'immuno', "''", 'pos=', "''", 'SUBST', "''", '>', 'Immuno', '<', '/w', '>', '<', 'w', 'c5=', "''", 'NN1', "''", 'hw=', "''", 'deficiency', "''", 'pos=', "''", 'SUBST', "''", '>', 'Deficiency', '<', '/w', '>', '<', 'w', 'c5=', "''", 'NN1', "''", 'hw=', "''", 'virus', "''", 'pos=', "''", 'SUBST', "''", '>', 'Virus', '<', '/w', '>', '<', 'c', 'c5=', "''", 'PUR', "''", '>', ')', '<', '/c', '>', '<', 'c', 'c5=', "''", 'PUN', "''", '>', '.'], ['<', '/c', '>', '<', '/s', '>']]], [[['<', 's', 'n=', "''", '3', "''", '>', '<', 'w', 'c5=', "''", 'DT0', "''", 'hw=', "''", 'this', "''", 'pos=', "''", 'ADJ', "''", '>', 'This', '<', '/w', '>', '<', 'w', 'c5=', "''", 'NN1', "''", 'hw=', "''", 'virus', "''", 'pos=', "''", 'SUBST', "''", '>', 'virus', '<', '/w', '>', '<', 'w', 'c5=', "''", 'VVZ', "''", 'hw=', "''", 'affect', "''", 'pos=', "''", 'VERB', "''", '>', 'affects', '<', '/w', '>', '<', 'w', 'c5=', "''", 'AT0', "''", 'hw=', "''", 'the', "''", 'pos=', "''", 'ART', "''", '>', 'the', '<', '/w', '>', '<', 'w', 'c5=', "''", 'NN1', "''", 'hw=', "''", 'body', "''", 'pos=', "''", 'SUBST', "''", '>', 'body', '<', '/w', '>', '<', 'w', 'c5=', "''", 'POS', "''", 'hw=', "''", "'s", "''", 'pos=', "''", 'UNC', "''", '>', "'s", '<', '/w', '>', '<', 'w', 'c5=', "''", 'NN1', "''", 'hw=', "''", 'defence', "''", 'pos=', "''", 'SUBST', "''", '>', 'defence', '<', '/w', '>', '<', 'w', 'c5=', "''", 'NN1', "''", 'hw=', "''", 'system', "''", 'pos=', "''", 'SUBST', "''", '>', 'system', '<', '/w', '>', '<', 'mw', 'c5=', "''", 'CJS', "''", '>', '<', 'w', 'c5=', "''", 'AV0', "''", 'hw=', "''", 'so', "''", 'pos=', "''", 'ADV', "''", '>', 'so', '<', '/w', '>', '<', 'w', 'c5=', "''", 'CJT', "''", 'hw=', "''", 'that', "''", 'pos=', "''", 'CONJ', "''", '>', 'that', '<', '/w', '>', '<', '/mw', '>', '<', 'w', 'c5=', "''", 'PNP', "''", 'hw=', "''", 'it', "''", 'pos=', "''", 'PRON', "''", '>', 'it', '<', '/w', '>', '<', 'w', 'c5=', "''", 'VM0', "''", 'hw=', "''", 'can', "''", 'pos=', "''", 'VERB', "''", '>', 'can', '<', '/w', '>', '<', 'w', 'c5=', "''", 'XX0', "''", 'hw=', "''", 'not', "''", 'pos=', "''", 'ADV', "''", '>', 'not', '<', '/w', '>', '<', 'w', 'c5=', "''", 'VVI', "''", 'hw=', "''", 'fight', "''", 'pos=', "''", 'VERB', "''", '>', 'fight', '<', '/w', '>', '<', 'w', 'c5=', "''", 'NN1', "''", 'hw=', "''", 'infection', "''", 'pos=', "''", 'SUBST', "''", '>', 'infection', '<', '/w', '>', '<', 'c', 'c5=', "''", 'PUN', "''", '>', '.'], ['<', '/c', '>', '<', '/s', '>', '<', '/p', '>']]]]
            # Tokenized & Untagged
            case 'xml (5).xml':
                assert tokens == [[[['<bncDoc', 'xml:id="A00"><teiHeader><fileDesc><titleStmt><title>', '[ACET', 'factsheets', '&amp;'], ['newsletters].']], [['Sample', 'containing', 'about', '6688', 'words', 'of', 'miscellanea', '(domain:'], ['social', 'science)', '</title><respStmt><resp>', 'Data', 'capture', 'and', 'transcription', '</resp><name>', 'Oxford', 'University', 'Press', '</name>', '</respStmt></titleStmt></fileDesc></teiHeader>']]], [[['<wtext', 'type="NONAC"><div', 'level="1"', 'n="1"', 'type="leaflet"><head', 'type="MAIN">']]], [[['<s', 'n="1"><w', 'c5="NN1"', 'hw="factsheet"', 'pos="SUBST">FACTSHEET', '</w><w', 'c5="DTQ"', 'hw="what"', 'pos="PRON">WHAT', '</w><w', 'c5="VBZ"', 'hw="be"', 'pos="VERB">IS', '</w><w', 'c5="NN1"', 'hw="aids"', 'pos="SUBST">AIDS</w><c', 'c5="PUN">?</c></s></head><p>']]], [[['<s', 'n="2"><hi', 'rend="bo"><w', 'c5="NN1"', 'hw="aids"', 'pos="SUBST">AIDS', '</w><c', 'c5="PUL">(</c><w', 'c5="VVN-AJ0"', 'hw="acquire"', 'pos="VERB">Acquired', '</w><w', 'c5="AJ0"', 'hw="immune"', 'pos="ADJ">Immune', '</w><w', 'c5="NN1"', 'hw="deficiency"', 'pos="SUBST">Deficiency', '</w><w', 'c5="NN1"', 'hw="syndrome"', 'pos="SUBST">Syndrome</w><c', 'c5="PUR">)</c></hi><w', 'c5="VBZ"', 'hw="be"', 'pos="VERB">is', '</w><w', 'c5="AT0"', 'hw="a"', 'pos="ART">a', '</w><w', 'c5="NN1"', 'hw="condition"', 'pos="SUBST">condition', '</w><w', 'c5="VVN"', 'hw="cause"', 'pos="VERB">caused', '</w><w', 'c5="PRP"', 'hw="by"', 'pos="PREP">by', '</w><w', 'c5="AT0"', 'hw="a"', 'pos="ART">a', '</w><w', 'c5="NN1"', 'hw="virus"', 'pos="SUBST">virus', '</w><w', 'c5="VVN"', 'hw="call"', 'pos="VERB">called', '</w><w', 'c5="NP0"', 'hw="hiv"', 'pos="SUBST">HIV', '</w><c', 'c5="PUL">(</c><w', 'c5="AJ0-NN1"', 'hw="human"', 'pos="ADJ">Human', '</w><w', 'c5="NN1"', 'hw="immuno"', 'pos="SUBST">Immuno', '</w><w', 'c5="NN1"', 'hw="deficiency"', 'pos="SUBST">Deficiency', '</w><w', 'c5="NN1"', 'hw="virus"', 'pos="SUBST">Virus</w><c', 'c5="PUR">)</c><c', 'c5="PUN">.</c></s>']]], [[['<s', 'n="3"><w', 'c5="DT0"', 'hw="this"', 'pos="ADJ">This', '</w><w', 'c5="NN1"', 'hw="virus"', 'pos="SUBST">virus', '</w><w', 'c5="VVZ"', 'hw="affect"', 'pos="VERB">affects', '</w><w', 'c5="AT0"', 'hw="the"', 'pos="ART">the', '</w><w', 'c5="NN1"', 'hw="body"', 'pos="SUBST">body</w><w', 'c5="POS"', 'hw="\'s"', 'pos="UNC">\'s', '</w><w', 'c5="NN1"', 'hw="defence"', 'pos="SUBST">defence', '</w><w', 'c5="NN1"', 'hw="system"', 'pos="SUBST">system', '</w><mw', 'c5="CJS"><w', 'c5="AV0"', 'hw="so"', 'pos="ADV">so', '</w><w', 'c5="CJT"', 'hw="that"', 'pos="CONJ">that', '</w></mw><w', 'c5="PNP"', 'hw="it"', 'pos="PRON">it', '</w><w', 'c5="VM0"', 'hw="can"', 'pos="VERB">can</w><w', 'c5="XX0"', 'hw="not"', 'pos="ADV">not', '</w><w', 'c5="VVI"', 'hw="fight"', 'pos="VERB">fight', '</w><w', 'c5="NN1"', 'hw="infection"', 'pos="SUBST">infection</w><c', 'c5="PUN">.</c></s></p>']]]]

        assert tags == [None] * file_text.num_tokens
    # TMX files
    elif len(new_files) == 2:
        file_text_src = new_files[0]['text']
        file_text_tgt = new_files[1]['text']

        tokens_src = file_text_src.to_token_texts()
        tags_src = file_text_src.get_token_properties('tag', flat = True)

        # Source files
        print(file_text_src.lang)
        print(tokens_src)

        assert file_text_src.lang == 'eng_us'
        assert tokens_src == [[[['Hello', 'world', '!']]]]
        assert tags_src == [None] * 3

        # Target files
        tokens_tgt = file_text_tgt.to_token_texts()
        tags_tgt = file_text_tgt.get_token_properties('tag', flat = True)

        print(file_text_tgt.lang)
        print(tokens_tgt)

        # Avoid loading spaCy's French model
        assert file_text_tgt.lang == 'eng_gb'
        assert tokens_tgt == [[[['Bonjour', 'tout', 'le', 'monde', '!']]]]
        assert tags_tgt == [None] * 5

def update_gui_unicode_decode_error(err_msg, new_files):
    assert not err_msg

    assert new_files[0]['encoding'] == 'utf_8'

def update_gui_tags(err_msg, new_files):
    assert not err_msg

    file_name = os.path.split(new_files[0]['path'])[1]
    file_text = new_files[0]['text']

    tokens = file_text.to_token_texts()
    tags = file_text.get_token_properties('tag', flat = True)

    print(tokens)
    print(tags)

    match file_name:
        case 'untokenized_untagged.txt':
            assert tokens == [[], [], [[['This', '<', 'TAG', '>', 'is', 'the', 'first', 'sentence', '.']], [['This', 'is', 'the', 'second', 'sentence', '.']]], [], [], [[['This', 'is', 'the', 'third', 'sentence', '.']]], [], []]
            assert tags == [None] * file_text.num_tokens
        case 'untokenized_tagged.txt':
            assert tokens == [[[['This', 'is', 'the', 'first', 'sentence', '.']], [['This', 'is', 'the', 'second', 'sentence', '.']], [['This', 'is', 'the', 'third', 'sentence', '.']]]]
            assert tags == ['<TAG1><TAG2>', '</TAG2>', '', '', '', '', '_TAG3', '', '', '', '', '', '', '', '', '', '', '<TAG4></TAG4>']
        case 'tokenized_untagged.txt':
            assert tokens == [[], [], [[['This', '<TAG>is', 'the', 'first', 'sentence', '.']], [['This', 'is', 'the', 'second', 'sentence', '.']]], [], [], [[['This', 'is', 'the', 'third', 'sentence', '.']]], [], []]
            assert tags == [None] * file_text.num_tokens
        case 'tokenized_tagged.txt':
            assert tokens == [[], [], [[['This', 'is', 'the', 'first', 'sentence', '.']], [['This', 'is', 'the', 'second', 'sentence', '.']]], [], [], [[['This', 'is', 'the', 'third', 'sentence', '.']]], [], []]
            assert tags == ['<TAG1><TAG2>', '</TAG2>', '', '', '', '', '_TAG3RunningToken_TAG3', '', '', '', '', '', '', '', '', '', '', '<TAG4></TAG4>']

    assert len(tags) == file_text.num_tokens

def test_file_area_misc():
    wl_test_init.clean_import_caches()

    main.settings_custom['file_area']['dialog_open_files']['auto_detect_encodings'] = False
    main.settings_custom['file_area']['dialog_open_files']['auto_detect_langs'] = False

    main.settings_custom['files']['default_settings']['encoding'] = 'utf_8'
    main.settings_custom['files']['default_settings']['lang'] = 'vie'
    main.settings_custom['files']['default_settings']['tokenized'] = True
    main.settings_custom['files']['default_settings']['tagged'] = False

    # Check if underscores in tokenized Vietnamese files are removed
    add_file(
        file_paths = ['tests/files/wl_file_area/misc/vie_tokenized.txt'],
        update_gui = update_gui_misc,
        file_type = 'observed'
    )
    add_file(
        file_paths = ['tests/files/wl_file_area/misc/vie_tokenized.txt'],
        update_gui = update_gui_misc,
        file_type = 'ref'
    )

def update_gui_misc(err_msg, new_files):
    assert not err_msg

    file_text = new_files[0]['text']

    print(file_text.tokens_multilevel)

    for para in file_text.tokens_multilevel:
        for sentence in para:
            for sentence_seg in sentence:
                for token in sentence_seg:
                    assert not wl_texts.RE_VIE_TOKENIZED.search(token)

if __name__ == '__main__':
    test_file_area_file_types()
    test_file_area_misc()

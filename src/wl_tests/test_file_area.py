# ----------------------------------------------------------------------
# Wordless: Tests - File Area
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

from wl_dialogs import wl_dialogs_misc
from wl_tests import wl_test_init

import wl_file_area

main = wl_test_init.Wl_Test_Main()

def add_file(file_paths, update_gui):
    def open_file(err_msg, files_to_open):
        assert not err_msg

        # Untokenized & Untagged
        if files_to_open[-1]['path'].endswith('XML File (4).xml'):
            files_to_open[-1]['tokenized'] = 'No'
            files_to_open[-1]['tagged'] = 'No'
        # Tokenized & Untagged
        elif files_to_open[-1]['path'].endswith('XML File (5).xml'):
            files_to_open[-1]['tokenized'] = 'Yes'
            files_to_open[-1]['tagged'] = 'No'

        wl_file_area.Wl_Worker_Open_Files(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(main, text = ''),
            update_gui = update_gui,
            files_to_open = files_to_open
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

def test_file_area():
    # Clean cached files
    for file in glob.glob('imports/*.*'):
        os.remove(file)

    # Disable encoding detection
    main.settings_custom['file_area']['dialog_open_files']['auto_detect_encodings'] = False

    # File types (Non-XML)
    files_non_xml = glob.glob('wl_tests_files/wl_file_area/file_types/*.*')
    files_non_xml = [file for file in files_non_xml if not file.endswith('.xml')]

    add_file(
        file_paths = files_non_xml,
        update_gui = update_gui_file_types
    )

    # File types (XML)
    for i in range(5):
        if i in [0, 3, 4]:
            main.settings_custom['tags']['tags_xml'] = [
                ['Non-embedded', 'Paragraph', '<p>', '</p>'],
                ['Non-embedded', 'Paragraph', '<head>', '</head>'],
                ['Non-embedded', 'Sentence', '<s>', '</s>'],
                ['Non-embedded', 'Word', '<w>', '</w>'],
                ['Non-embedded', 'Word', '<c>', '</c>']
            ]
        # XML tags unfound
        elif i == 1:
            main.settings_custom['tags']['tags_xml'] = [
                ['Non-embedded', 'Paragraph', '<pp>', '</pp>'],
                ['Non-embedded', 'Sentence', '<ss>', '</ss>'],
                ['Non-embedded', 'Word', '<ww>', '</ww>'],
            ]
        # XML tags unspecified
        elif i == 2:
            main.settings_custom['tags']['tags_xml'] = []

        add_file(
            file_paths = glob.glob('wl_tests_files/wl_file_area/file_types/*.xml'),
            update_gui = update_gui_file_types
        )

    # UnicodeDecodeError
    add_file(
        file_paths = glob.glob('wl_tests_files/wl_file_area/unicode_decode_error/*.*'),
        update_gui = update_gui_unicode_decode_error
    )

    # Tags
    for file_path in glob.glob('wl_tests_files/wl_file_area/tags/*.*'):
        if file_path.endswith('untokenized_untagged.txt'):
            main.settings_custom['files']['default_settings']['tokenized'] = 'No'
            main.settings_custom['files']['default_settings']['tagged'] = 'No'
        elif file_path.endswith('untokenized_tagged.txt'):
            main.settings_custom['files']['default_settings']['tokenized'] = 'No'
            main.settings_custom['files']['default_settings']['tagged'] = 'Yes'
        elif file_path.endswith('tokenized_untagged.txt'):
            main.settings_custom['files']['default_settings']['tokenized'] = 'Yes'
            main.settings_custom['files']['default_settings']['tagged'] = 'No'
        elif file_path.endswith('tokenized_tagged.txt'):
            main.settings_custom['files']['default_settings']['tokenized'] = 'Yes'
            main.settings_custom['files']['default_settings']['tagged'] = 'Yes'

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
            assert file_text.tokens_multilevel == [[['[', 'ACET', 'factsheets', '&', 'newsletters', ']', '.'], ['Sample', 'containing', 'about', '6688', 'words', 'of', 'miscellanea', '(', 'domain', ':', 'social', 'science', ')', 'Data', 'capture', 'and', 'transcription', 'Oxford', 'University', 'Press', 'BNC', 'XML', 'Edition', ',', 'December', '2006', '6688', 'tokens', ';', '6708', 'w', '-', 'units', ';', '423', 's', '-', 'units', 'Distributed', 'under', 'licence', 'by', 'Oxford', 'University', 'Computing', 'Services', 'on', 'behalf', 'of', 'the', 'BNC', 'Consortium', '.'], ['This', 'material', 'is', 'protected', 'by', 'international', 'copyright', 'laws', 'and', 'may', 'not', 'be', 'copied', 'or', 'redistributed', 'in', 'any', 'way', '.'], ['Consult', 'the', 'BNC', 'Web', 'Site', 'at', 'http://www.natcorp.ox.ac.uk', 'for', 'full', 'licencing', 'and', 'distribution', 'conditions', '.', 'A00'], ['AidFct', '[', 'ACET', 'factsheets', '&', 'newsletters', ']', '.'], ['Aids', 'Care', 'Education', '&', 'Training', 'London', '1991', '-', '09', '1991', '-', '09', 'W', 'nonAc', ':', 'medicine', 'Health', 'Sex', 'Tag', 'usage', 'updated', 'for', 'BNC', '-', 'XMLLast', 'check', 'for', 'BNC', 'World', 'first', 'releaseRedo', 'tagusage', 'tablesCheck', 'all', 'tagcountsResequenced', 's', '-', 'units', 'and', 'added', 'headersAdded', 'date', 'infoUpdated', 'all', 'catrefsManually', 'updated', 'tagcounts', ',', 'titlestmt', ',', 'and', 'title', 'in', 'sourcePOS', 'codes', 'revised', 'for', 'BNC-2', ';', 'header', 'updatedInitial', 'accession', 'to', 'corpus']], [], [['FACTSHEET', 'WHAT', 'IS', 'AIDS', '?']], [['AIDS', '(', 'Acquired', 'Immune', 'Deficiency', 'Syndrome)is', 'a', 'condition', 'caused', 'by', 'a', 'virus', 'called', 'HIV', '(', 'Human', 'Immuno', 'Deficiency', 'Virus', ')', '.']], [['This', 'virus', 'affects', 'the', 'body', "'s", 'defence', 'system', 'so', 'that', 'it', 'can', 'not', 'fight', 'infection', '.']]]
            assert file_text.tokens_flat == ['[', 'ACET', 'factsheets', '&', 'newsletters', ']', '.', 'Sample', 'containing', 'about', '6688', 'words', 'of', 'miscellanea', '(', 'domain', ':', 'social', 'science', ')', 'Data', 'capture', 'and', 'transcription', 'Oxford', 'University', 'Press', 'BNC', 'XML', 'Edition', ',', 'December', '2006', '6688', 'tokens', ';', '6708', 'w', '-', 'units', ';', '423', 's', '-', 'units', 'Distributed', 'under', 'licence', 'by', 'Oxford', 'University', 'Computing', 'Services', 'on', 'behalf', 'of', 'the', 'BNC', 'Consortium', '.', 'This', 'material', 'is', 'protected', 'by', 'international', 'copyright', 'laws', 'and', 'may', 'not', 'be', 'copied', 'or', 'redistributed', 'in', 'any', 'way', '.', 'Consult', 'the', 'BNC', 'Web', 'Site', 'at', 'http://www.natcorp.ox.ac.uk', 'for', 'full', 'licencing', 'and', 'distribution', 'conditions', '.', 'A00', 'AidFct', '[', 'ACET', 'factsheets', '&', 'newsletters', ']', '.', 'Aids', 'Care', 'Education', '&', 'Training', 'London', '1991', '-', '09', '1991', '-', '09', 'W', 'nonAc', ':', 'medicine', 'Health', 'Sex', 'Tag', 'usage', 'updated', 'for', 'BNC', '-', 'XMLLast', 'check', 'for', 'BNC', 'World', 'first', 'releaseRedo', 'tagusage', 'tablesCheck', 'all', 'tagcountsResequenced', 's', '-', 'units', 'and', 'added', 'headersAdded', 'date', 'infoUpdated', 'all', 'catrefsManually', 'updated', 'tagcounts', ',', 'titlestmt', ',', 'and', 'title', 'in', 'sourcePOS', 'codes', 'revised', 'for', 'BNC-2', ';', 'header', 'updatedInitial', 'accession', 'to', 'corpus', 'FACTSHEET', 'WHAT', 'IS', 'AIDS', '?', 'AIDS', '(', 'Acquired', 'Immune', 'Deficiency', 'Syndrome)is', 'a', 'condition', 'caused', 'by', 'a', 'virus', 'called', 'HIV', '(', 'Human', 'Immuno', 'Deficiency', 'Virus', ')', '.', 'This', 'virus', 'affects', 'the', 'body', "'s", 'defence', 'system', 'so', 'that', 'it', 'can', 'not', 'fight', 'infection', '.']
            assert file_text.offsets_paras == [0, 166, 166, 171, 192]
            assert file_text.offsets_sentences == [0, 7, 60, 79, 94, 102, 166, 171, 192]
        # Tokenized & Untagged
        elif file_name == 'XML File (5).xml':
            assert file_text.tokens_multilevel == [[['[ACET', 'factsheets', '&', 'newsletters].'], ['Sample', 'containing', 'about', '6688', 'words', 'of', 'miscellanea', '(domain:', 'social', 'science)', 'Data', 'capture', 'and', 'transcription', 'Oxford', 'University', 'Press', 'BNC', 'XML', 'Edition,', 'December', '2006', '6688', 'tokens;', '6708', 'w-units;', '423', 's-units', 'Distributed', 'under', 'licence', 'by', 'Oxford', 'University', 'Computing', 'Services', 'on', 'behalf', 'of', 'the', 'BNC', 'Consortium.'], ['This', 'material', 'is', 'protected', 'by', 'international', 'copyright', 'laws', 'and', 'may', 'not', 'be', 'copied', 'or', 'redistributed', 'in', 'any', 'way.'], ['Consult', 'the', 'BNC', 'Web', 'Site', 'at', 'http://www.natcorp.ox.ac.uk', 'for', 'full', 'licencing', 'and', 'distribution', 'conditions.A00', 'AidFct', '[ACET', 'factsheets', '&', 'newsletters].'], ['Aids', 'Care', 'Education', '&', 'Training', 'London', '1991-09', '1991-09', 'W', 'nonAc:', 'medicine', 'Health', 'Sex', 'Tag', 'usage', 'updated', 'for', 'BNC-XMLLast', 'check', 'for', 'BNC', 'World', 'first', 'releaseRedo', 'tagusage', 'tablesCheck', 'all', 'tagcountsResequenced', 's-units', 'and', 'added', 'headersAdded', 'date', 'infoUpdated', 'all', 'catrefsManually', 'updated', 'tagcounts,', 'titlestmt,', 'and', 'title', 'in', 'sourcePOS', 'codes', 'revised', 'for', 'BNC-2;', 'header', 'updatedInitial', 'accession', 'to', 'corpus']], [], [['FACTSHEET', 'WHAT', 'IS', 'AIDS?']], [['AIDS', '(Acquired', 'Immune', 'Deficiency', 'Syndrome)is', 'a', 'condition', 'caused', 'by', 'a', 'virus', 'called', 'HIV', '(Human', 'Immuno', 'Deficiency', 'Virus).']], [['This', 'virus', 'affects', 'the', "body's", 'defence', 'system', 'so', 'that', 'it', 'cannot', 'fight', 'infection.']]]
            assert file_text.tokens_flat == ['[ACET', 'factsheets', '&', 'newsletters].', 'Sample', 'containing', 'about', '6688', 'words', 'of', 'miscellanea', '(domain:', 'social', 'science)', 'Data', 'capture', 'and', 'transcription', 'Oxford', 'University', 'Press', 'BNC', 'XML', 'Edition,', 'December', '2006', '6688', 'tokens;', '6708', 'w-units;', '423', 's-units', 'Distributed', 'under', 'licence', 'by', 'Oxford', 'University', 'Computing', 'Services', 'on', 'behalf', 'of', 'the', 'BNC', 'Consortium.', 'This', 'material', 'is', 'protected', 'by', 'international', 'copyright', 'laws', 'and', 'may', 'not', 'be', 'copied', 'or', 'redistributed', 'in', 'any', 'way.', 'Consult', 'the', 'BNC', 'Web', 'Site', 'at', 'http://www.natcorp.ox.ac.uk', 'for', 'full', 'licencing', 'and', 'distribution', 'conditions.A00', 'AidFct', '[ACET', 'factsheets', '&', 'newsletters].', 'Aids', 'Care', 'Education', '&', 'Training', 'London', '1991-09', '1991-09', 'W', 'nonAc:', 'medicine', 'Health', 'Sex', 'Tag', 'usage', 'updated', 'for', 'BNC-XMLLast', 'check', 'for', 'BNC', 'World', 'first', 'releaseRedo', 'tagusage', 'tablesCheck', 'all', 'tagcountsResequenced', 's-units', 'and', 'added', 'headersAdded', 'date', 'infoUpdated', 'all', 'catrefsManually', 'updated', 'tagcounts,', 'titlestmt,', 'and', 'title', 'in', 'sourcePOS', 'codes', 'revised', 'for', 'BNC-2;', 'header', 'updatedInitial', 'accession', 'to', 'corpus', 'FACTSHEET', 'WHAT', 'IS', 'AIDS?', 'AIDS', '(Acquired', 'Immune', 'Deficiency', 'Syndrome)is', 'a', 'condition', 'caused', 'by', 'a', 'virus', 'called', 'HIV', '(Human', 'Immuno', 'Deficiency', 'Virus).', 'This', 'virus', 'affects', 'the', "body's", 'defence', 'system', 'so', 'that', 'it', 'cannot', 'fight', 'infection.']
            assert file_text.offsets_paras == [0, 134, 134, 138, 155]
            assert file_text.offsets_sentences == [0, 4, 46, 64, 82, 134, 138, 155]

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

        assert file_text_src.lang == 'eng_gb'
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
    test_file_area()

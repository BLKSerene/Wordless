# ----------------------------------------------------------------------
# Tests: Results - Filter
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

from PyQt5 import QtWidgets

from tests import wl_test_init
from wordless.wl_dialogs import wl_dialogs_misc
from wordless.wl_results import wl_results_filter

main = wl_test_init.Wl_Test_Main()

settings = {
    'test_sync': False,
    'test_min': 0, 'test_min_no_limit': True,
    'test_max': 0, 'test_max_no_limit': True
}

def test_widgets_filter():
    layout = wl_results_filter.widgets_filter(
        main,
        label = 'test',
        val_min = 0, val_max = 0,
        settings = settings, filter_name = 'test'
    )

    layout.load_settings(settings_load = settings)
    layout.checkbox_sync.setChecked(True)

def test_widgets_filter_measures():
    wl_results_filter.widgets_filter_measures(
        main,
        label = 'test',
        settings = settings, filter_name = 'test'
    )

    main.wl_settings.wl_settings_changed.emit()

def test_widgets_filter_p_val():
    wl_results_filter.widgets_filter_p_val(main, settings = settings)

    main.wl_settings.wl_settings_changed.emit()

def test_add_layouts_filters():
    wl_results_filter.add_layouts_filters(
        main,
        layouts_filters = [QtWidgets.QGridLayout() for _ in range(2)],
        layout_filters = QtWidgets.QGridLayout()
    )

def test_get_filter_min_max():
    wl_results_filter.get_filter_min_max(settings = settings, filter_name = 'test')

def test_wl_dialog_results_filter():
    dialog = wl_results_filter.Wl_Dialog_Results_Filter(
        main,
        table = wl_test_init.Wl_Test_Table(main, tab = 'dependency_parser')
    )

    dialog.layouts_filters.append(wl_results_filter.widgets_filter(
        dialog,
        label = 'test',
        val_min = 0, val_max = 0,
        settings = settings, filter_name = 'test'
    ))
    dialog.layouts_filters.append(wl_results_filter.widgets_filter(
        dialog,
        label = 'test',
        val_min = 0, val_max = 0,
        settings = settings, filter_name = 'test'
    ))
    dialog.layouts_filters[-1].combo_box_freq_position = QtWidgets.QComboBox()

    dialog.load_settings(defaults = True)
    dialog.load_settings(defaults = False)
    dialog.file_to_filter_changed()
    dialog.show()

table_dependency_parser = table = wl_test_init.Wl_Test_Table(
    main,
    headers = (
        'Head',
        'Dependent',
        'Dependency Relation',
        'Dependency Distance',
        'Dependency Distance (Absolute)',
        'File'
    ),
    tab = 'dependency_parser'
)

def test_wl_dialog_results_filter_dependency_parser():
    dialog = wl_results_filter.Wl_Dialog_Results_Filter_Dependency_Parser(
        main,
        table = table_dependency_parser
    )

    dialog.load_settings(defaults = True)
    dialog.load_settings(defaults = False)
    dialog.filter()
    dialog.update_gui('')

def test_wl_worker_results_filter_dependency_parser():
    for col in range(table_dependency_parser.model().columnCount()):
        table_dependency_parser.set_item(0, col, 'test')
        table_dependency_parser.model().item(0, col).tokens_filter = 'test'

    dialog = wl_results_filter.Wl_Dialog_Results_Filter_Dependency_Parser(
        main,
        table = table_dependency_parser
    )

    worker = wl_results_filter.Wl_Worker_Results_Filter_Dependency_Parser(
        main,
        dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(main, ''),
        dialog = dialog
    )

    main.settings_custom['dependency_parser']['results_filter']['len_head_min_no_limit'] = False
    main.settings_custom['dependency_parser']['results_filter']['len_head_min'] = 100
    worker.run()
    worker.stop()
    worker.run()

table_wordlist_generator = wl_test_init.Wl_Test_Table(
    main,
    headers = (
        'Token',
        'Syllabified Form',
        '[Total]\nFrequency',
        "[Total]\nJuilland's D",
        "[Total]\nJuilland's U",
        'Number of\nFiles Found'
    ),
    tab = 'wordlist_generator'
)

table_ngram_generator = wl_test_init.Wl_Test_Table(
    main,
    headers = (
        'N-gram',
        '[Total]\nFrequency',
        "[Total]\nJuilland's D",
        "[Total]\nJuilland's U",
        'Number of\nFiles Found',
    ),
    tab = 'ngram_generator'
)

def test_wl_dialog_results_filter_wordlist_generator():
    dialog = wl_results_filter.Wl_Dialog_Results_Filter_Wordlist_Generator(
        main,
        table = table_wordlist_generator
    )

    dialog.load_settings(defaults = True)
    dialog.load_settings(defaults = False)
    dialog.filter()
    dialog.update_gui('')

    dialog = wl_results_filter.Wl_Dialog_Results_Filter_Wordlist_Generator(
        main,
        table = table_ngram_generator
    )

    dialog.load_settings(defaults = True)
    dialog.load_settings(defaults = False)
    dialog.filter()
    dialog.update_gui('')

def test_wl_worker_results_filter_wordlist_generator():
    for col in range(table_wordlist_generator.model().columnCount()):
        table_wordlist_generator.set_item(0, col, 'test')
        table_wordlist_generator.model().item(0, col).tokens_filter = 'test'

    dialog = wl_results_filter.Wl_Dialog_Results_Filter_Wordlist_Generator(
        main,
        table = table_wordlist_generator
    )

    worker = wl_results_filter.Wl_Worker_Results_Filter_Wordlist_Generator(
        main,
        dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(main, ''),
        dialog = dialog
    )

    main.settings_custom['wordlist_generator']['results_filter']['len_token_min_no_limit'] = False
    main.settings_custom['wordlist_generator']['results_filter']['len_token_min'] = 100
    worker.run()
    worker.stop()
    worker.run()

    for col in range(table_ngram_generator.model().columnCount()):
        table_ngram_generator.set_item(0, col, 'test')
        table_ngram_generator.model().item(0, col).tokens_filter = 'test'

    dialog = wl_results_filter.Wl_Dialog_Results_Filter_Wordlist_Generator(
        main,
        table = table_ngram_generator
    )

    worker = wl_results_filter.Wl_Worker_Results_Filter_Wordlist_Generator(
        main,
        dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(main, ''),
        dialog = dialog
    )

    worker.run()

table_collocation_extractor = wl_test_init.Wl_Test_Table(
    main,
    headers = (
        'Node',
        'Collocate',
        '[Total]\nFrequency',
        '[Total]\nχ2',
        '[Total]\np-value',
        '[Total]\nBayes Factor',
        '[Total]\nPMI',
        'Number of\nFiles Found'
    ),
    tab = 'collocation_extractor'
)

table_colligation_extractor = wl_test_init.Wl_Test_Table(
    main,
    headers = (
        'Node',
        'Collocate',
        '[Total]\nR1',
        '[Total]\nFrequency',
        '[Total]\nχ2',
        '[Total]\np-value',
        '[Total]\nBayes Factor',
        '[Total]\nPMI',
        'Number of\nFiles Found'
    ),
    tab = 'colligation_extractor'
)

table_keyword_extractor = wl_test_init.Wl_Test_Table(
    main,
    headers = (
        'Keyword',
        '[Total]\nFrequency',
        '[Total]\nχ2',
        '[Total]\np-value',
        '[Total]\nBayes Factor',
        '[Total]\nOR',
        'Number of\nFiles Found'
    ),
    tab = 'keyword_extractor'
)

def test_wl_dialog_results_filter_collocation_extractor():
    dialog = wl_results_filter.Wl_Dialog_Results_Filter_Collocation_Extractor(
        main,
        table = table_collocation_extractor
    )

    dialog.load_settings(defaults = True)
    dialog.load_settings(defaults = False)
    dialog.filter()
    dialog.update_gui('')

    dialog = wl_results_filter.Wl_Dialog_Results_Filter_Collocation_Extractor(
        main,
        table = table_colligation_extractor
    )

    dialog.load_settings(defaults = True)
    dialog.load_settings(defaults = False)
    dialog.filter()
    dialog.update_gui('')

    dialog = wl_results_filter.Wl_Dialog_Results_Filter_Collocation_Extractor(
        main,
        table = table_keyword_extractor
    )

    dialog.load_settings(defaults = True)
    dialog.load_settings(defaults = False)
    dialog.filter()
    dialog.update_gui('')

def test_wl_worker_results_filter_collocation_extractor():
    for col in range(table_collocation_extractor.model().columnCount()):
        table_collocation_extractor.set_item(0, col, 'test')
        table_collocation_extractor.model().item(0, col).tokens_filter = 'test'

    dialog = wl_results_filter.Wl_Dialog_Results_Filter_Collocation_Extractor(
        main,
        table = table_collocation_extractor
    )

    worker = wl_results_filter.Wl_Worker_Results_Filter_Collocation_Extractor(
        main,
        dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(main, ''),
        dialog = dialog
    )

    main.settings_custom['collocation_extractor']['results_filter']['len_node_min_no_limit'] = False
    main.settings_custom['collocation_extractor']['results_filter']['len_node_min'] = 100
    main.settings_custom['collocation_extractor']['results_filter']['freq_position'] = 'Total'
    worker.run()
    worker.stop()
    worker.run()

    dialog = wl_results_filter.Wl_Dialog_Results_Filter_Collocation_Extractor(
        main,
        table = table_colligation_extractor
    )

    worker = wl_results_filter.Wl_Worker_Results_Filter_Collocation_Extractor(
        main,
        dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(main, ''),
        dialog = dialog
    )

    main.settings_custom['colligation_extractor']['results_filter']['freq_position'] = 'R1'
    worker.run()

    dialog = wl_results_filter.Wl_Dialog_Results_Filter_Collocation_Extractor(
        main,
        table = table_keyword_extractor
    )

    worker = wl_results_filter.Wl_Worker_Results_Filter_Collocation_Extractor(
        main,
        dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(main, ''),
        dialog = dialog
    )

    worker.run()

if __name__ == '__main__':
    test_widgets_filter()
    test_widgets_filter_measures()
    test_widgets_filter_p_val()
    test_add_layouts_filters()
    test_get_filter_min_max()

    test_wl_dialog_results_filter()
    test_wl_dialog_results_filter_dependency_parser()
    test_wl_worker_results_filter_dependency_parser()
    test_wl_dialog_results_filter_wordlist_generator()
    test_wl_worker_results_filter_wordlist_generator()
    test_wl_dialog_results_filter_collocation_extractor()
    test_wl_worker_results_filter_collocation_extractor()

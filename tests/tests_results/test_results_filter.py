# ----------------------------------------------------------------------
# Tests: Results - Filter results
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

from PyQt5.QtWidgets import QComboBox, QGridLayout

from tests import wl_test_init
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
        layouts_filters = [QGridLayout() for _ in range(2)],
        layout_filters = QGridLayout()
    )

def test_get_filter_min_max():
    wl_results_filter.get_filter_min_max(settings = settings, filter_name = 'test')

def test_wl_dialog_results_filter():
    dialog_results_filter = wl_results_filter.Wl_Dialog_Results_Filter(
        main,
        table = wl_test_init.Wl_Test_Table(main, tab = 'dependency_parser')
    )

    dialog_results_filter.layouts_filters.append(wl_results_filter.widgets_filter(
        dialog_results_filter,
        label = 'test',
        val_min = 0, val_max = 0,
        settings = settings, filter_name = 'test'
    ))
    dialog_results_filter.layouts_filters.append(wl_results_filter.widgets_filter(
        dialog_results_filter,
        label = 'test',
        val_min = 0, val_max = 0,
        settings = settings, filter_name = 'test'
    ))
    dialog_results_filter.layouts_filters[-1].combo_box_freq_position = QComboBox()

    dialog_results_filter.load_settings(defaults = True)
    dialog_results_filter.load_settings(defaults = False)
    dialog_results_filter.file_to_filter_changed()
    dialog_results_filter.show()

def test_wl_dialog_results_filter_dependency_parser():
    dialog_results_filter_dependency_parser = wl_results_filter.Wl_Dialog_Results_Filter_Dependency_Parser(
        main,
        table = wl_test_init.Wl_Test_Table(main, tab = 'dependency_parser')
    )

    dialog_results_filter_dependency_parser.load_settings(defaults = True)
    dialog_results_filter_dependency_parser.load_settings(defaults = False)
    dialog_results_filter_dependency_parser.filter_results()
    dialog_results_filter_dependency_parser.update_gui('')

def test_wl_dialog_results_filter_wordlist_generator():
    dialog_results_filter_wordlist_generator = wl_results_filter.Wl_Dialog_Results_Filter_Wordlist_Generator(
        main,
        table = wl_test_init.Wl_Test_Table(main, tab = 'wordlist_generator')
    )

    dialog_results_filter_wordlist_generator.load_settings(defaults = True)
    dialog_results_filter_wordlist_generator.load_settings(defaults = False)
    dialog_results_filter_wordlist_generator.filter_results()
    dialog_results_filter_wordlist_generator.update_gui('')

    dialog_results_filter_ngram_generator = wl_results_filter.Wl_Dialog_Results_Filter_Wordlist_Generator(
        main,
        table = wl_test_init.Wl_Test_Table(main, tab = 'ngram_generator')
    )

    dialog_results_filter_ngram_generator.load_settings(defaults = True)
    dialog_results_filter_ngram_generator.load_settings(defaults = False)
    dialog_results_filter_ngram_generator.filter_results()
    dialog_results_filter_ngram_generator.update_gui('')

def test_wl_dialog_results_filter_collocation_extractor():
    dialog_results_filter_collocation_extractor = wl_results_filter.Wl_Dialog_Results_Filter_Collocation_Extractor(
        main,
        table = wl_test_init.Wl_Test_Table(main, tab = 'collocation_extractor')
    )

    dialog_results_filter_collocation_extractor.load_settings(defaults = True)
    dialog_results_filter_collocation_extractor.load_settings(defaults = False)
    dialog_results_filter_collocation_extractor.filter_results()
    dialog_results_filter_collocation_extractor.update_gui('')

    dialog_results_filter_colligation_extractor = wl_results_filter.Wl_Dialog_Results_Filter_Collocation_Extractor(
        main,
        table = wl_test_init.Wl_Test_Table(main, tab = 'colligation_extractor')
    )

    dialog_results_filter_colligation_extractor.load_settings(defaults = True)
    dialog_results_filter_colligation_extractor.load_settings(defaults = False)
    dialog_results_filter_colligation_extractor.filter_results()
    dialog_results_filter_colligation_extractor.update_gui('')

    dialog_results_filter_keyword_extractor = wl_results_filter.Wl_Dialog_Results_Filter_Collocation_Extractor(
        main,
        table = wl_test_init.Wl_Test_Table(main, tab = 'keyword_extractor')
    )

    dialog_results_filter_keyword_extractor.load_settings(defaults = True)
    dialog_results_filter_keyword_extractor.load_settings(defaults = False)
    dialog_results_filter_keyword_extractor.filter_results()
    dialog_results_filter_keyword_extractor.update_gui('')

if __name__ == '__main__':
    test_widgets_filter()
    test_widgets_filter_measures()
    test_widgets_filter_p_val()
    test_add_layouts_filters()
    test_get_filter_min_max()

    test_wl_dialog_results_filter()
    test_wl_dialog_results_filter_dependency_parser()
    test_wl_dialog_results_filter_wordlist_generator()
    test_wl_dialog_results_filter_collocation_extractor()

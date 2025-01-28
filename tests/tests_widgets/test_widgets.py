# ----------------------------------------------------------------------
# Tests: Widgets - Widgets
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

from PyQt5.QtWidgets import QTableView

from tests import wl_test_init
from wordless.wl_widgets import wl_widgets

main = wl_test_init.Wl_Test_Main()

def test_wl_dialog_context_settings():
    dialog_context_settings = wl_widgets.Wl_Dialog_Context_Settings(main, tab = 'concordancer')
    dialog_context_settings.multi_search_mode_changed()

    dialog_context_settings.incl_group_box.setChecked(True)
    dialog_context_settings.excl_group_box.setChecked(True)
    dialog_context_settings.token_settings_changed()

    dialog_context_settings.incl_group_box.setChecked(False)
    dialog_context_settings.excl_group_box.setChecked(False)
    dialog_context_settings.token_settings_changed()

    dialog_context_settings.load_settings(defaults = True)

    dialog_context_settings.settings_custom['incl']['context_window_left'] = -1
    dialog_context_settings.settings_custom['incl']['context_window_right'] = -1
    dialog_context_settings.settings_custom['excl']['context_window_left'] = -1
    dialog_context_settings.settings_custom['excl']['context_window_right'] = -1
    dialog_context_settings.load_settings(defaults = False)

    dialog_context_settings.settings_custom['incl']['context_window_left'] = 1
    dialog_context_settings.settings_custom['incl']['context_window_right'] = 1
    dialog_context_settings.settings_custom['excl']['context_window_left'] = 1
    dialog_context_settings.settings_custom['excl']['context_window_right'] = 1
    dialog_context_settings.load_settings(defaults = False)

    dialog_context_settings.incl_spin_box_context_window_left.setPrefix('L')
    dialog_context_settings.incl_spin_box_context_window_right.setPrefix('L')
    dialog_context_settings.excl_spin_box_context_window_left.setPrefix('L')
    dialog_context_settings.excl_spin_box_context_window_right.setPrefix('L')
    dialog_context_settings.save_settings()

    dialog_context_settings.incl_spin_box_context_window_left.setPrefix('R')
    dialog_context_settings.incl_spin_box_context_window_right.setPrefix('R')
    dialog_context_settings.excl_spin_box_context_window_left.setPrefix('R')
    dialog_context_settings.excl_spin_box_context_window_right.setPrefix('R')
    dialog_context_settings.save_settings()

def test_wl_widgets_token_settings():
    (
        checkbox_words, _, _, _, _, _,
        _, _, _,
        checkbox_assign_pos_tags, checkbox_ignore_tags, checkbox_use_tags
    ) = wl_widgets.wl_widgets_token_settings(main)

    checkbox_words.setChecked(True)
    checkbox_words.setChecked(False)

    checkbox_assign_pos_tags.setChecked(True)
    checkbox_assign_pos_tags.setChecked(False)

    checkbox_ignore_tags.setChecked(True)
    checkbox_ignore_tags.setChecked(False)

    checkbox_use_tags.setChecked(True)
    checkbox_use_tags.setChecked(False)

def test_wl_widgets_token_settings_concordancer():
    _, checkbox_assign_pos_tags, checkbox_ignore_tags, checkbox_use_tags = wl_widgets.wl_widgets_token_settings_concordancer(main)

    checkbox_assign_pos_tags.setChecked(True)
    checkbox_assign_pos_tags.setChecked(False)

    checkbox_ignore_tags.setChecked(True)
    checkbox_ignore_tags.setChecked(False)

    checkbox_use_tags.setChecked(True)
    checkbox_use_tags.setChecked(False)

def test_wl_widgets_search_settings():
    (
        _, checkbox_multi_search_mode,
        _, line_edit_search_term, _, _,
        _, _, _, _, checkbox_match_without_tags, checkbox_match_tags
    ) = wl_widgets.wl_widgets_search_settings(main, tab = 'concordancer')

    line_edit_search_term.setText('test')
    checkbox_multi_search_mode.setChecked(True)
    checkbox_multi_search_mode.setChecked(False)

    token_settings = main.settings_custom['concordancer']['token_settings']

    token_settings['use_tags'] = True
    checkbox_match_tags.token_settings_changed()

    token_settings['ignore_tags'] = False
    token_settings['use_tags'] = False
    checkbox_match_without_tags.setChecked(False)
    checkbox_match_tags.setChecked(False)
    checkbox_match_tags.token_settings_changed()

    checkbox_match_without_tags.setChecked(True)

    checkbox_match_tags.setChecked(True)
    checkbox_match_tags.setChecked(False)

def test_wl_widgets_search_settings_tokens():
    wl_widgets.wl_widgets_search_settings_tokens(main, tab = 'dependency_parser')

def test_wl_widgets_context_settings():
    wl_widgets.wl_widgets_context_settings(main, tab = 'concordancer')

def test_wl_widgets_measures_wordlist_ngram_generation():
    wl_widgets.wl_widgets_measures_wordlist_ngram_generation(main)

def test_wl_widgets_measures_collocation_keyword_extraction():
    wl_widgets.wl_widgets_measures_collocation_keyword_extraction(main, extraction_type = 'collocation')
    wl_widgets.wl_widgets_measures_collocation_keyword_extraction(main, extraction_type = 'keyword')

def test_wl_widgets_table_settings():
    table = QTableView()
    table.table_settings = {'show_pct_data': True, 'show_cum_data': True, 'show_breakdown_file': True}
    table.is_empty = lambda: False
    table.toggle_pct_data = lambda: None
    table.toggle_cum_data = lambda: None
    table.toggle_breakdown_file = lambda: None

    wl_widgets.wl_widgets_table_settings(main, tables = [table])

def test_wl_widgets_table_settings_span_position():
    table = QTableView()
    table.table_settings = {
        'show_pct_data': True,
        'show_cum_data': True,
        'show_breakdown_span_position': True,
        'show_breakdown_file': True
    }
    table.is_empty = lambda: False
    table.toggle_pct_data_span_position = lambda: None
    table.toggle_cum_data = lambda: None
    table.toggle_breakdown_span_position = lambda: None
    table.toggle_breakdown_file_span_position = lambda: None

    wl_widgets.wl_widgets_table_settings_span_position(main, tables = [table])

def test_wl_combo_box_file_fig_settings():
    main.settings_custom['file_area']['files_open'] = [{'selected': True, 'name': 'test'}]

    combo_box_file_fig_settings = wl_widgets.Wl_Combo_Box_File_Fig_Settings(main)
    combo_box_file_fig_settings.wl_files_changed()

    combo_box_file_fig_settings.clear()
    combo_box_file_fig_settings.addItem('test')
    combo_box_file_fig_settings.wl_files_changed()

def test_wl_widgets_fig_settings():
    (
        _, combo_box_graph_type,
        _, _, _, combo_box_use_data, _, _
    ) = wl_widgets.wl_widgets_fig_settings(main, tab = 'wordlist_generator')

    combo_box_graph_type.setCurrentText('Line chart')
    combo_box_graph_type.setCurrentText(combo_box_graph_type.itemText(1))

    combo_box_graph_type.setCurrentText('Line chart')
    combo_box_use_data.setCurrentText('Frequency')
    combo_box_use_data.setCurrentText(combo_box_use_data.itemText(1))

    main.settings_custom['wordlist_generator']['fig_settings']['use_data'] = combo_box_use_data.itemText(0)
    combo_box_use_data.measures_changed()
    main.settings_custom['wordlist_generator']['fig_settings']['use_data'] = 'test'
    combo_box_use_data.measures_changed()

    _, _,  _, _, _, combo_box_use_data, _, _ = wl_widgets.wl_widgets_fig_settings(main, tab = 'collocation_extractor')

    main.settings_custom['collocation_extractor']['fig_settings']['use_data'] = combo_box_use_data.itemText(0)
    combo_box_use_data.measures_changed()
    main.settings_custom['collocation_extractor']['fig_settings']['use_data'] = 'test'
    combo_box_use_data.measures_changed()

    _, _,  _, _, _, combo_box_use_data, _, _ = wl_widgets.wl_widgets_fig_settings(main, tab = 'keyword_extractor')

    main.settings_custom['keyword_extractor']['fig_settings']['use_data'] = combo_box_use_data.itemText(0)
    combo_box_use_data.measures_changed()
    main.settings_custom['keyword_extractor']['fig_settings']['use_data'] = 'test'
    combo_box_use_data.measures_changed()

def test_wl_widgets_fig_settings_dependency_parsing():
    checkbox_show_pos_tags, _, _, _, _, _, _ = wl_widgets.wl_widgets_fig_settings_dependency_parsing(main)

    checkbox_show_pos_tags.setChecked(True)
    checkbox_show_pos_tags.setChecked(False)

def test_wl_widgets_num_sub_sections():
    wl_widgets.wl_widgets_num_sub_sections(main)

def test_wl_widgets_use_data_freq():
    wl_widgets.wl_widgets_use_data_freq(main)

def test_wl_widgets_direction():
    wl_widgets.wl_widgets_direction(main)

if __name__ == '__main__':
    test_wl_dialog_context_settings()

    test_wl_widgets_token_settings()
    test_wl_widgets_token_settings_concordancer()

    test_wl_widgets_search_settings()
    test_wl_widgets_context_settings()

    test_wl_widgets_measures_wordlist_ngram_generation()
    test_wl_widgets_measures_collocation_keyword_extraction()

    test_wl_widgets_table_settings()
    test_wl_widgets_table_settings_span_position()

    test_wl_combo_box_file_fig_settings()
    test_wl_widgets_fig_settings()
    test_wl_widgets_fig_settings_dependency_parsing()

    test_wl_widgets_num_sub_sections()
    test_wl_widgets_use_data_freq()
    test_wl_widgets_direction()

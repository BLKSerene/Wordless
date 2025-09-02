# ----------------------------------------------------------------------
# Tests: Figures - Figures
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

import os

import pytest

from tests import wl_test_init
from wordless.wl_figs import wl_figs
from wordless.wl_utils import wl_excs

def test_restore_matplotlib_rcparams():
    wl_figs.restore_matplotlib_rcparams()

def test_get_data_ranks():
    data_files_items = [(str(i), i) for i in range(100)]
    fig_settings_1_50 = {
        'rank_min_no_limit': True,
        'rank_max_no_limit': False,
        'rank_max': 50
    }
    fig_settings_50_100 = {
        'rank_min_no_limit': False,
        'rank_max_no_limit': True,
        'rank_min': 50,
    }

    assert wl_figs.get_data_ranks(data_files_items, fig_settings_1_50) == [(str(i), i) for i in range(50)]
    assert wl_figs.get_data_ranks(data_files_items, fig_settings_50_100) == [(str(i), i) for i in range(49, 100)]

def test_generate_line_chart():
    main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')
    wl_test_init.select_test_files(main, no_files = (0, 1))

    data_files_items = [
        (str(i), [i, i])
        for i in range(100)
    ]

    wl_figs.generate_line_chart(
        main,
        data_files_items = data_files_items,
        fig_settings = {
            'rank_min_no_limit': True,
            'rank_max_no_limit': True,
            'use_cumulative': True,
            'use_pct': True,
            'use_data': 'Frequency'
        },
        file_names_selected = main.wl_file_area.get_selected_file_names(),
        label_x = 'test'
    )

    wl_figs.generate_line_chart(
        main,
        data_files_items = data_files_items,
        fig_settings = {
            'rank_min_no_limit': True,
            'rank_max_no_limit': True,
            'use_cumulative': True,
            'use_pct': False,
            'use_data': 'Frequency'
        },
        file_names_selected = main.wl_file_area.get_selected_file_names(),
        label_x = 'test'
    )

    wl_figs.generate_line_chart(
        main,
        data_files_items = data_files_items,
        fig_settings = {
            'rank_min_no_limit': True,
            'rank_max_no_limit': True,
            'use_cumulative': False,
            'use_pct': True,
            'use_data': 'Frequency'
        },
        file_names_selected = main.wl_file_area.get_selected_file_names(),
        label_x = 'test'
    )

    wl_figs.generate_line_chart(
        main,
        data_files_items = data_files_items,
        fig_settings = {
            'rank_min_no_limit': True,
            'rank_max_no_limit': True,
            'use_cumulative': False,
            'use_pct': False,
            'use_data': 'Frequency'
        },
        file_names_selected = main.wl_file_area.get_selected_file_names(),
        label_x = 'test'
    )

    wl_figs.generate_line_chart(
        main,
        data_files_items = data_files_items,
        fig_settings = {
            'rank_min_no_limit': True,
            'rank_max_no_limit': True,
            'use_data': 'test'
        },
        file_names_selected = main.wl_file_area.get_selected_file_names(),
        label_x = 'test'
    )

def test_generate_word_cloud():
    # Reload main to avoid file being reloaded
    main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')
    wl_test_init.select_test_files(main, no_files = (0, 1))

    data_file_items = [
        (str(i), i)
        for i in range(100)
    ]

    main.settings_custom['figs']['word_clouds']['font_settings']['font'] = 'Droid Sans Mono'
    main.settings_custom['figs']['word_clouds']['font_settings']['relative_scaling'] = -0.01
    main.settings_custom['figs']['word_clouds']['font_settings']['font_color'] = 'Monochrome'
    main.settings_custom['figs']['word_clouds']['bg_settings']['bg_color_transparent'] = True
    main.settings_custom['figs']['word_clouds']['mask_settings']['mask_settings'] = True
    main.settings_custom['figs']['word_clouds']['mask_settings']['mask_path'] = ''

    with pytest.raises(wl_excs.Wl_Exc_Word_Cloud_Mask_Nonexistent):
        wl_figs.generate_word_cloud(
            main,
            data_file_items = data_file_items,
            fig_settings = {
                'rank_min_no_limit': True,
                'rank_max_no_limit': True,
                'use_data': 'p-value'
            }
        )

    main.settings_custom['figs']['word_clouds']['mask_settings']['mask_path'] = os.path.split(__file__)[0]

    with pytest.raises(wl_excs.Wl_Exc_Word_Cloud_Mask_Is_Dir):
        wl_figs.generate_word_cloud(
            main,
            data_file_items = data_file_items,
            fig_settings = {
                'rank_min_no_limit': True,
                'rank_max_no_limit': True,
                'use_data': 'p-value'
            }
        )

    main.settings_custom['figs']['word_clouds']['mask_settings']['mask_path'] = __file__

    with pytest.raises(wl_excs.Wl_Exc_Word_Cloud_Mask_Unsupported):
        wl_figs.generate_word_cloud(
            main,
            data_file_items = data_file_items,
            fig_settings = {
                'rank_min_no_limit': True,
                'rank_max_no_limit': True,
                'use_data': 'p-value'
            }
        )

    main.settings_custom['figs']['word_clouds']['font_settings']['relative_scaling'] = 0.5
    main.settings_custom['figs']['word_clouds']['font_settings']['font'] = 'GNU Unifont'
    main.settings_custom['figs']['word_clouds']['font_settings']['font_color'] = 'Colormap'
    main.settings_custom['figs']['word_clouds']['bg_settings']['bg_color_transparent'] = False
    main.settings_custom['figs']['word_clouds']['mask_settings']['mask_settings'] = False

    wl_figs.generate_word_cloud(
        main,
        data_file_items = data_file_items,
        fig_settings = {
            'rank_min_no_limit': True,
            'rank_max_no_limit': True,
            'use_data': 'p-value'
        }
    )

    main.settings_custom['figs']['word_clouds']['font_settings']['font'] = 'Custom'
    main.settings_custom['figs']['word_clouds']['font_settings']['font_path'] = ''

    with pytest.raises(wl_excs.Wl_Exc_Word_Cloud_Font_Nonexistent):
        wl_figs.generate_word_cloud(
            main,
            data_file_items = data_file_items,
            fig_settings = {
                'rank_min_no_limit': True,
                'rank_max_no_limit': True,
                'use_data': 'p-value'
            }
        )

    main.settings_custom['figs']['word_clouds']['font_settings']['font_path'] = os.path.split(__file__)[0]

    with pytest.raises(wl_excs.Wl_Exc_Word_Cloud_Font_Is_Dir):
        wl_figs.generate_word_cloud(
            main,
            data_file_items = data_file_items,
            fig_settings = {
                'rank_min_no_limit': True,
                'rank_max_no_limit': True,
                'use_data': 'p-value'
            }
        )

    main.settings_custom['figs']['word_clouds']['font_settings']['font_path'] = __file__

    with pytest.raises(wl_excs.Wl_Exc_Word_Cloud_Font_Unsupported):
        wl_figs.generate_word_cloud(
            main,
            data_file_items = data_file_items,
            fig_settings = {
                'rank_min_no_limit': True,
                'rank_max_no_limit': True,
                'use_data': 'p-value'
            }
        )

def test_generate_network_graph():
    # Reload main to avoid file being reloaded
    main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')
    wl_test_init.select_test_files(main, no_files = (0, 1))

    data_file_items = [
        ((str(node), str(collocate)), node * collocate)
        for node in range(10)
        for collocate in range(10)
    ]

    main.settings_custom['figs']['network_graphs']['node_settings']['same_as_node_color'] = True

    wl_figs.generate_network_graph(
        main,
        data_file_items = data_file_items,
        fig_settings  = {
            'rank_min_no_limit': True,
            'rank_max_no_limit': True,
            'use_data': 'p-value'
        }
    )

    main.settings_custom['figs']['network_graphs']['node_settings']['same_as_node_color'] = False

    wl_figs.generate_network_graph(
        main,
        data_file_items = data_file_items,
        fig_settings  = {
            'rank_min_no_limit': True,
            'rank_max_no_limit': True,
            'use_data': 'test'
        }
    )

def test_show_fig():
    wl_figs.show_fig()

if __name__ == '__main__':
    test_restore_matplotlib_rcparams()
    test_get_data_ranks()

    test_generate_line_chart()
    test_generate_word_cloud()
    test_generate_network_graph()

    test_show_fig()

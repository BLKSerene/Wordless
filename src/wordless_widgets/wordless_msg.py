#
# Wordless: Widgets - Message
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

def wordless_msg_generate_table_success(main):
    main.statusBar().showMessage(main.tr('The table has been successfully generated.'))

def wordless_msg_generate_fig_success(main):
    main.statusBar().showMessage(main.tr('The figure has been successfully generated.'))

def wordless_msg_generate_table_error(main):
    main.statusBar().showMessage(main.tr('An error occured while the table is being generated!'))

def wordless_msg_generate_fig_error(main):
    main.statusBar().showMessage(main.tr('An error occured while the figure is being generated!'))

def wordless_msg_results_filter_success(main):
    main.statusBar().showMessage(main.tr('The results in the table has been successfully filtered.'))

def wordless_msg_results_search_success(main, search_results):
    if len(search_results) == 0:
        main.statusBar().showMessage(main.tr('No items found.'))
    elif len(search_results) == 1:
        main.statusBar().showMessage(main.tr('Found 1 item.'))
    else:
        main.statusBar().showMessage(main.tr(f'Found {len(search_results):,} items.'))

def wordless_msg_results_search_error(main):
    main.statusBar().showMessage(main.tr('An error occured during searching!'))

def wordless_msg_results_sort(main):
    main.statusBar().showMessage(main.tr('The results in the table has been successfully sorted.'))

def wordless_msg_import_list_success(main, num_prev, num_cur):
    num_imported = num_cur - num_prev

    if num_imported == 0:
        main.statusBar().showMessage(main.tr('No items were imported into the list.'))
    elif num_imported == 1:
        main.statusBar().showMessage(main.tr('1 item has been successfully imported into the list.'))
    else:
        main.statusBar().showMessage(main.tr(f'{num_imported:,} items have been successfully imported into the list.'))

def wordless_msg_import_list_error(main):
    main.statusBar().showMessage(main.tr('An error occured during import!'))

# ----------------------------------------------------------------------
# Wordless: Checks - Work area
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

import importlib
import traceback

from PyQt5 import QtCore
from PyQt5 import QtGui

from wordless.wl_dialogs import (
    wl_dialogs,
    wl_dialogs_errs
)
from wordless.wl_utils import (
    wl_conversion,
    wl_excs, wl_misc
)

_tr = QtCore.QCoreApplication.translate

def wl_status_bar_missing_search_terms(main):
    main.statusBar().showMessage(_tr('wl_checks_work_area', 'The search term is missing.'))

def wl_status_bar_err_fatal(main):
    main.statusBar().showMessage(_tr('wl_checks_work_area', 'A fatal error has just occurred.'))

def check_search_terms(parent, search_settings, show_warning = True):
    if (
        (
            not search_settings['multi_search_mode']
            and search_settings['search_term'].strip()
        ) or (
            search_settings['multi_search_mode']
            and any((search_term.strip() for search_term in search_settings['search_terms']))
        )
    ):
        search_terms_ok = True
    else:
        search_terms_ok = False

        if show_warning:
            wl_dialogs.Wl_Dialog_Info_Simple(
                parent,
                title = _tr('wl_checks_work_area', 'Missing Search Term'),
                text = _tr('wl_checks_work_area', '''
                    <div>You have not specified any search term yet.</div>
                    <br>
                    <div>Please specify a search term in <b>Search Settings → Search term</b>.</div>
                '''),
                icon = 'warning'
            ).open()

            wl_status_bar_missing_search_terms(wl_misc.find_wl_main(parent))

    return search_terms_ok

NLP_UTILS = {
    'syl_tokenizers': _tr('wl_checks_work_area', 'Syllable tokenization'),
    'pos_taggers': _tr('wl_checks_work_area', 'Part-of-speech tagging'),
    'lemmatizers': _tr('wl_checks_work_area', 'Lemmatization'),
    'dependency_parsers': _tr('wl_checks_work_area', 'Dependency parsing')
}

def check_nlp_support(parent, nlp_utils, files = None, ref = False):
    support_ok = True
    nlp_utils_no_support = []
    main = wl_misc.find_wl_main(parent)

    if files is None:
        if ref:
            files = tuple(main.wl_file_area_ref.get_selected_files())
        else:
            files = tuple(main.wl_file_area.get_selected_files())

    for nlp_util in nlp_utils:
        # Check POS tagging support for untagged files only
        if nlp_util == 'pos_taggers':
            for file in files:
                if not file['tagged'] and file['lang'] not in main.settings_global[nlp_util]:
                    nlp_utils_no_support.append([nlp_util, file])
        else:
            for file in files:
                if file['lang'] not in main.settings_global[nlp_util]:
                    nlp_utils_no_support.append([nlp_util, file])

    if nlp_utils_no_support:
        dialog_err_files = wl_dialogs_errs.Wl_Dialog_Err_Files(parent, title = _tr('wl_checks_work_area', 'No Language Support'))
        dialog_err_files.table_err_files.model().setHorizontalHeaderLabels((
            _tr('wl_checks_work_area', 'Type of Language Support'),
            _tr('wl_checks_work_area', 'File Name'),
            _tr('wl_checks_work_area', 'Language')
        ))

        dialog_err_files.label_err.set_text(_tr('wl_checks_work_area', '''
            <div>Data analysis cannot be carried out because language support is unavailable for the following corpora. Please check your language settings or use another corpus.</div>
        '''))

        dialog_err_files.table_err_files.model().setRowCount(len(nlp_utils_no_support))
        dialog_err_files.table_err_files.disable_updates()

        for i, (nlp_util, file) in enumerate(nlp_utils_no_support):
            dialog_err_files.table_err_files.model().setItem(
                i, 0,
                QtGui.QStandardItem(_tr('wl_checks_work_area', NLP_UTILS[nlp_util]))
            )
            dialog_err_files.table_err_files.model().setItem(
                i, 1,
                QtGui.QStandardItem(file['name'])
            )
            dialog_err_files.table_err_files.model().setItem(
                i, 2,
                QtGui.QStandardItem(wl_conversion.to_lang_text(main, file['lang']))
            )

        dialog_err_files.table_err_files.enable_updates()
        dialog_err_files.open()

        main.statusBar().showMessage(_tr('wl_checks_work_area', 'Language support is unavailable.'))

        support_ok = False

    return support_ok

def check_results(parent, err_msg, results):
    results_ok = True
    main = wl_misc.find_wl_main(parent)

    match err_msg:
        case '':
            if not any(results):
                wl_dialogs.Wl_Dialog_Info_Simple(
                    parent,
                    title = _tr('wl_checks_work_area', 'No Results'),
                    text = _tr('wl_checks_work_area', '''
                        <div>Data processing has completed successfully, but there are no results to display.</div>
                        <br>
                        <div>You may change your settings and try again.</div>
                    '''),
                    icon = 'warning'
                ).open()

                main.statusBar().showMessage(_tr('wl_checks_work_area', 'No results to display.'))

                results_ok = False
        case 'aborted':
            results_ok = False
        case _:
            wl_dialogs_errs.Wl_Dialog_Err_Fatal(parent, err_msg).open()
            wl_status_bar_err_fatal(main)

            results_ok = False

    return results_ok

def check_results_download_model(parent, err_msg, model_name = ''):
    results_ok = True

    try:
        if model_name:
            importlib.import_module(model_name)
    except ModuleNotFoundError:
        results_ok = False

        # Show import error if the error message is empty
        if not err_msg:
            err_msg = traceback.format_exc()

    if err_msg:
        wl_dialogs_errs.Wl_Dialog_Err_Download_Model(parent, err_msg).open()
        wl_misc.find_wl_main(parent).statusBar().showMessage(_tr('wl_checks_work_area', 'A network error occurred while downloading the model.'))

        results_ok = False

    return results_ok

def check_postprocessing(parent, err_msg):
    results_ok = True

    if err_msg == 'aborted':
        results_ok = False
    elif err_msg:
        results_ok = False

        wl_dialogs_errs.Wl_Dialog_Err_Fatal(parent, err_msg).open()
        wl_status_bar_err_fatal(wl_misc.find_wl_main(parent))

    return results_ok

def check_err(parent, err_msg):
    if err_msg:
        wl_dialogs_errs.Wl_Dialog_Err_Fatal(parent, err_msg).open()
        wl_status_bar_err_fatal(wl_misc.find_wl_main(parent))

def check_err_table(main, err_msg):
    check_err(main, err_msg)

    if not err_msg:
        main.statusBar().showMessage(_tr('wl_checks_work_area', 'Table generated successfully.'))

def check_err_fig(main, err_msg):
    check_err(main, err_msg)

    if not err_msg:
        main.statusBar().showMessage(_tr('wl_checks_work_area', 'Figure generated successfully.'))

def check_err_fig_word_cloud(main, err):
    if isinstance(err, wl_excs.Wl_Exc_Word_Cloud_Mask_Nonexistent):
        main.statusBar().showMessage(_tr('wl_checks_work_area', 'The mask image for generating the word cloud cannot be found.'))
    elif isinstance(err, wl_excs.Wl_Exc_Word_Cloud_Mask_Is_Dir):
        main.statusBar().showMessage(_tr('wl_checks_work_area', 'The mask image for generating the word cloud is a folder rather than a file.'))
    elif isinstance(err, wl_excs.Wl_Exc_Word_Cloud_Mask_Unsupported):
        main.statusBar().showMessage(_tr('wl_checks_work_area', 'The mask image for generating the word cloud is not supported.'))
    elif isinstance(err, wl_excs.Wl_Exc_Word_Cloud_Font_Nonexistent):
        main.statusBar().showMessage(_tr('wl_checks_work_area', 'The font file for generating the word cloud cannot be found.'))
    elif isinstance(err, wl_excs.Wl_Exc_Word_Cloud_Font_Is_Dir):
        main.statusBar().showMessage(_tr('wl_checks_work_area', 'The font file for generating the word cloud is a folder rather than a file.'))
    elif isinstance(err, wl_excs.Wl_Exc_Word_Cloud_Font_Unsupported):
        main.statusBar().showMessage(_tr('wl_checks_work_area', 'The font file for generating the word cloud is not supported.'))

def check_err_exp_table(parent, err_msg, file_path):
    main = wl_misc.find_wl_main(parent)

    match err_msg:
        case '':
            wl_dialogs.Wl_Dialog_Info_Simple(
                parent,
                title = _tr('wl_checks_work_area', 'Export Completed'),
                text = _tr('wl_checks_work_area', '''
                    <div>The table has been successfully exported to "{}".</div>
                ''').format(file_path)
            ).open()

            main.statusBar().showMessage(_tr('wl_checks_work_area', 'Table exported successfully.'))
        case 'permission_err':
            wl_dialogs.Wl_Dialog_Info_Simple(
                parent,
                title = _tr('wl_checks_work_area', 'File Access Denied'),
                text = _tr('wl_checks_work_area', '''
                    <div>Access to "{}" is denied. Please specify another location or close the file and try again.</div>
                ''').format(file_path),
                icon = 'critical'
            ).open()

            main.statusBar().showMessage(_tr('wl_checks_work_area', 'File access denied.'))
        case 'aborted':
            pass
        case _:
            wl_dialogs_errs.Wl_Dialog_Err_Fatal(parent, err_msg).open()

            wl_status_bar_err_fatal(main)

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

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QStandardItem

from wordless.wl_dialogs import wl_dialogs_errs, wl_msg_boxes
from wordless.wl_utils import wl_conversion

_tr = QCoreApplication.translate

def wl_msg_box_missing_search_terms(main):
    wl_msg_boxes.Wl_Msg_Box_Warning(
        main,
        title = _tr('wl_checks_work_area', 'Missing Search Terms'),
        text = _tr('wl_checks_work_area', '''
            <div>
                You have not specified any search terms yet, please enter one in the input box under "<span style="color: #F00; font-weight: bold;">Search term</span>" first.
            </div>
        ''')
    ).open()

def wl_msg_box_no_results(main):
    wl_msg_boxes.Wl_Msg_Box_Warning(
        main,
        title = _tr('wl_checks_work_area', 'No Results'),
        text = _tr('wl_checks_work_area', '''
            <div>Data processing has completed successfully, but there are no results to display.</div>
            <div>You can change your settings and try again.</div>
        ''')
    ).open()

def wl_status_bar_msg_lang_support_unavailable(main):
    main.statusBar().showMessage(_tr('wl_checks_work_area', 'Language support unavailable!'))

def wl_status_bar_msg_missing_search_terms(main):
    main.statusBar().showMessage(_tr('wl_checks_work_area', 'Missing search terms!'))

def wl_status_bar_msg_success_download_model(main):
    main.statusBar().showMessage(_tr('wl_checks_work_area', 'Model downloaded successfully.'))

def wl_status_bar_msg_success_generate_table(main):
    main.statusBar().showMessage(_tr('wl_checks_work_area', 'Table generated successfully.'))

def wl_status_bar_msg_success_generate_fig(main):
    main.statusBar().showMessage(_tr('wl_checks_work_area', 'Figure generated successfully.'))

def wl_status_bar_msg_success_exp_table(main):
    main.statusBar().showMessage(_tr('wl_checks_work_area', 'Table exported successfully.'))

def wl_status_bar_msg_success_no_results(main):
    main.statusBar().showMessage(_tr('wl_checks_work_area', 'No results to display.'))

def wl_status_bar_msg_err_download_model(main):
    main.statusBar().showMessage(_tr('wl_checks_work_area', 'A network error occurred while downloading the model!'))

def wl_status_bar_msg_err_fatal(main):
    main.statusBar().showMessage(_tr('wl_checks_work_area', 'A fatal error has just occurred!'))

def wl_status_bar_msg_file_access_denied(main):
    main.statusBar().showMessage(_tr('wl_checks_work_area', 'File access denied!'))

def check_search_terms(main, search_settings, show_warning = True):
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
            wl_msg_box_missing_search_terms(main)
            wl_status_bar_msg_missing_search_terms(main)

    return search_terms_ok

NLP_UTILS = {
    'syl_tokenizers': _tr('wl_checks_work_area', 'Syllable tokenization'),
    'pos_taggers': _tr('wl_checks_work_area', 'Part-of-speech tagging'),
    'lemmatizers': _tr('wl_checks_work_area', 'Lemmatization'),
    'dependency_parsers': _tr('wl_checks_work_area', 'Dependency parsing')
}

def check_nlp_support(main, nlp_utils, files = None, ref = False):
    support_ok = True
    nlp_utils_no_support = []

    if files is None:
        if ref:
            files = list(main.wl_file_area_ref.get_selected_files())
        else:
            files = list(main.wl_file_area.get_selected_files())

    for nlp_util in nlp_utils:
        # Check pos tagging support for untagged files only
        if nlp_util == 'pos_taggers':
            for file in files:
                if not file['tagged'] and file['lang'] not in main.settings_global[nlp_util]:
                    nlp_utils_no_support.append([nlp_util, file])
        else:
            for file in files:
                if file['lang'] not in main.settings_global[nlp_util]:
                    nlp_utils_no_support.append([nlp_util, file])

    if nlp_utils_no_support:
        dialog_err_files = wl_dialogs_errs.Wl_Dialog_Err_Files(main, title = _tr('wl_checks_work_area', 'No Language Support'))
        dialog_err_files.table_err_files.model().setHorizontalHeaderLabels([
            _tr('wl_checks_work_area', 'Type of Language Support'),
            _tr('wl_checks_work_area', 'File Name'),
            _tr('wl_checks_work_area', 'Language')
        ])

        dialog_err_files.label_err.set_text(_tr('wl_checks_work_area', '''
            <div>
                The process cannot be done because language support is unavailable for the following files. Please check your language settings or try again with files of different languages.
            </div>
        '''))

        dialog_err_files.table_err_files.model().setRowCount(len(nlp_utils_no_support))
        dialog_err_files.table_err_files.disable_updates()

        for i, (nlp_util, file) in enumerate(nlp_utils_no_support):
            dialog_err_files.table_err_files.model().setItem(
                i, 0,
                QStandardItem(_tr('wl_checks_work_area', NLP_UTILS[nlp_util]))
            )
            dialog_err_files.table_err_files.model().setItem(
                i, 1,
                QStandardItem(file['name'])
            )
            dialog_err_files.table_err_files.model().setItem(
                i, 2,
                QStandardItem(wl_conversion.to_lang_text(main, file['lang']))
            )

        dialog_err_files.table_err_files.enable_updates()
        dialog_err_files.open()

        wl_status_bar_msg_lang_support_unavailable(main)

        support_ok = False

    return support_ok

def check_results(main, err_msg, results):
    results_ok = True

    if err_msg:
        results_ok = False

        wl_dialogs_errs.Wl_Dialog_Err_Fatal(main, err_msg).open()
        wl_status_bar_msg_err_fatal(main)
    elif not any(results):
        results_ok = False

        wl_msg_box_no_results(main)
        wl_status_bar_msg_success_no_results(main)

    return results_ok

def check_results_download_model(main, err_msg, model_name = ''):
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
        # Use exec_() instead of open() here to prevent the dialog from being hidden on OS X 10.11 with PyQt 5.10
        wl_dialogs_errs.Wl_Dialog_Err_Download_Model(main, err_msg).exec_()
        wl_status_bar_msg_err_download_model(main)

        results_ok = False

    return results_ok

def check_postprocessing(main, err_msg):
    results_ok = True

    if err_msg:
        results_ok = False

        wl_dialogs_errs.Wl_Dialog_Err_Fatal(main, err_msg).open()
        wl_status_bar_msg_err_fatal(main)

    return results_ok

def check_err(main, err_msg):
    if err_msg:
        wl_dialogs_errs.Wl_Dialog_Err_Fatal(main, err_msg).open()
        wl_status_bar_msg_err_fatal(main)

def check_err_table(main, err_msg):
    check_err(main, err_msg)

    if not err_msg:
        wl_status_bar_msg_success_generate_table(main)

def check_err_fig(main, err_msg):
    check_err(main, err_msg)

    if not err_msg:
        wl_status_bar_msg_success_generate_fig(main)

def check_err_exp_table(main, err_msg, file_path):
    # Use exec_() instead of open() here to prevent the dialog from being hidden on OS X 10.11 with PyQt 5.10
    if err_msg:
        if err_msg == 'permission_err':
            wl_msg_boxes.Wl_Msg_Box_Info(
                main,
                title = _tr('wl_checks_work_area', 'File Access Denied'),
                text = _tr('wl_checks_work_area', '''
                    <div>Access to "{}" is denied, please specify another location or close the file and try again.</div>
                ''').format(file_path)
            ).exec_()
        else:
            wl_dialogs_errs.Wl_Dialog_Err_Fatal(main, err_msg).exec_()

        wl_status_bar_msg_file_access_denied(main)
    else:
        wl_msg_boxes.Wl_Msg_Box_Info(
            main,
            title = _tr('wl_checks_work_area', 'Export Completed'),
            text = _tr('wl_checks_work_area', '''
                <div>The table has been successfully exported to "{}".</div>
            ''').format(file_path)
        ).exec_()

        wl_status_bar_msg_success_exp_table(main)

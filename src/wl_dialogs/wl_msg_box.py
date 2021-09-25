#
# Wordless: Dialogs - Message Box
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wl_checking import wl_checking_misc

class Wl_Msg_Box(QMessageBox):
    def __init__(self, main, icon, title, text):
        super().__init__(
            icon,
            title,
            f'''
                {main.settings_global['styles']['style_dialog']}
                <body>
                    {text}
                </body>
            ''',
            parent = main
        )

class Wl_Msg_Box_Info(Wl_Msg_Box):
    def __init__(self, main, title, text):
        super().__init__(main = main,
                         icon = QMessageBox.Information,
                         title = title,
                         text = text)

class Wl_Msg_Box_Info_Help(Wl_Msg_Box):
    def __init__(self, main, title, text):
        super().__init__(main = main,
                         icon = QMessageBox.Information,
                         title = title,
                         text = text)

        self.setTextFormat(Qt.RichText)
        self.setTextInteractionFlags(Qt.TextBrowserInteraction)

class Wl_Msg_Box_Warning(Wl_Msg_Box):
    def __init__(self, main, title, text):
        super().__init__(main = main,
                         icon = QMessageBox.Warning,
                         title = title,
                         text = text)

def wl_msg_box_question(main, title, text):
    reply = QMessageBox.question(
        main,
        main.tr(title),
        main.tr(f'''
            {main.settings_global['styles']['style_dialog']}
            <body>
                {text}
            </body>
        '''),
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )

    if reply == QMessageBox.Yes:
        return True
    else:
        return False

# Reset settings
def wl_msg_box_reset_layouts(main):
    return wl_msg_box_question(
        main = main,
        title = main.tr('Reset Layouts'),
        text = main.tr(f'''
            <div>Do you really want to reset all layouts to their default settings?</div>
        ''')
    )

def wl_msg_box_restore_default_settings(main):
    return wl_msg_box_question(
        main = main,
        title = main.tr('Restore default settings'),
        text = main.tr(f'''
            <div>Do you really want to reset all settings to their defaults?</div>
        ''')
    )

def wl_msg_box_reset_all_settings(main):
    return wl_msg_box_question(
        main = main,
        title = main.tr('Reset All Settings'),
        text = main.tr(f'''
            <div>Do you really want to reset all settings to their defaults?</div>
            <div><b>Warning: This will affect settings on all pages!</b></div>
        ''')
    )

def wl_msg_box_reset_mappings(main):
    return wl_msg_box_question(
        main = main,
        title = main.tr('Reset Mappings'),
        text = main.tr(f'''
            <div>Do you really want to reset all mappings to their defaults?</div>
            <div><b>Note: This will only affect the mapping settings in the currently shown table.</b></div>
        ''')
    )

def wl_msg_box_reset_all_mappings(main):
    return wl_msg_box_question(
        main = main,
        title = main.tr('Reset All Mappings'),
        text = main.tr(f'''
            <div>Do you really want to reset all mappings to their defaults?</div>
            <div><b>Warning: This will affect the mapping settings in all tables!</b></div>
        ''')
    )

# Files
def wl_msg_box_duplicate_file_name(main):
    Wl_Msg_Box_Warning(
        main = main,
        title = main.tr('Duplicate File Name'),
        text = main.tr(f'''
            <div>There is already a file with the same name in the file area.</div>
            <div>Please specify a different file name.</div>
        ''')
    ).open()

def wl_msg_box_no_files_selected(main):
    Wl_Msg_Box_Warning(
        main = main,
        title = main.tr('No Files Selected'),
        text = main.tr('''
            <div>There are no files being currently opened and selected.</div>
            <div>Please open files first or check your file settings.</div>
        ''')
    ).open()

def wl_msg_box_identical_src_tgt_files(main):
    Wl_Msg_Box_Warning(
        main = main,
        title = main.tr('Identical source and target files'),
        text = main.tr('''
            <div>The source and target file you have specified are identical. Please check your settings and try again.</div>
        ''')
    ).open()

def wl_msg_box_missing_ref_files(main):
    Wl_Msg_Box_Warning(
        main = main,
        title = main.tr('Missing Reference Files'),
        text = main.tr('''
            <div>You have not specified any reference files yet.</div>
        ''')
    ).open()

def wl_msg_box_missing_observed_files(main):
    Wl_Msg_Box_Warning(
        main = main,
        title = main.tr('Missing Observed Files'),
        text = main.tr('''
            <div>You have specified reference files, but you have not opened and selected any observed files yet.</div>
        ''')
    ).open()

def wl_msg_box_invalid_xml_file(main):
    Wl_Msg_Box_Warning(
        main = main,
        title = main.tr('Invalid XML File'),
        text = main.tr('''
            <div>If the input is an XML file, it must be both tokenized and tagged.</div>
        ''')
    ).open()

# Search terms
def wl_msg_box_missing_search_terms(main):
    Wl_Msg_Box_Warning(
        main = main,
        title = main.tr('Missing Search Terms'),
        text = main.tr('''
            <div>
                You have not specified any search terms yet, please enter one in the input box under "<span style="color: #F00; font-weight: bold;">Search Term</span>" first.
            </div>
        ''')
    ).open()

def wl_msg_box_missing_search_terms_optional(main):
    Wl_Msg_Box_Warning(
        main = main,
        title = main.tr('Missing Search Terms'),
        text = main.tr('''
            <div>
                You have not specified any search terms yet, please enter one in the input box under "<span style="color: #F00; font-weight: bold;">Search Term</span>" first.
            </div>

            <div>
                Or, you can disable searching altogether by unchecking "<span style="color: #F00; font-weight: bold;">Search Settings</span>", which will then generate all possible results, but it is not recommended to do so since the processing speed might be too slow.
            </div>
        ''')
    ).open()

def wl_msg_box_missing_search_terms_concordancer_parallel(main):
    return wl_msg_box_question(
        main = main,
        title = main.tr('Empty Search Terms'),
        text = main.tr(f'''
            <div>You have not specified any search terms. Do you want to search for additions in the target file?</div>
        ''')
    )

def wl_msg_box_duplicate_search_terms(main):
    Wl_Msg_Box_Warning(
        main = main,
        title = main.tr('Duplicate Search Terms'),
        text = main.tr(f'''
            <div>The search term that you have specified already exists in the list!</div>
        ''')
    ).open()

# Results
def wl_msg_box_no_results(main):
    Wl_Msg_Box_Warning(
        main = main,
        title = main.tr('No Results'),
        text = main.tr('''
            <div>Data processing has completed successfully, but there are no results to display.</div>
            <div>You can change your settings and try again.</div>
        ''')
    ).open()

def wl_msg_box_no_search_results(main):
    Wl_Msg_Box_Warning(
        main = main,
        title = main.tr('No Search Results'),
        text = main.tr('''
            <div>Searching has completed successfully, but there are no results found.</div>
            <div>You can change your settings and try again.</div>
        ''')
    ).open()

# Export
def wl_msg_box_export_list(main, file_path):
    Wl_Msg_Box_Info(
        main = main,
        title = main.tr('Export Completed'),
        text = main.tr(f'''
            <div>The list has been successfully exported to "{file_path}".</div>
        ''')
    ).open()

def wl_msg_box_export_table_success(main, file_path):
    Wl_Msg_Box_Info(
        main = main,
        title = main.tr('Export Completed'),
        text = main.tr(f'''
            <div>The table has been successfully exported to "{file_path}".</div>
        ''')
    ).open()

def wl_msg_box_export_table_error(main, file_path):
    Wl_Msg_Box_Info(
        main = main,
        title = main.tr('Export Error'),
        text = main.tr(f'''
            <div>Access to "{file_path}" is denied, please specify another location or close the file and try again.</div>
        ''')
    ).open()

# Settings - General
def wl_msg_box_path_not_exist(main, path):
    Wl_Msg_Box_Warning(
        main = main,
        title = main.tr('Invalid Path'),
        text = main.tr(f'''
            <div>The specified path "{path}" does not exist!</div>
            <div>Please check your settings and try again.</div>
        '''),
    ).open()

def wl_msg_box_path_not_dir(main, path):
    Wl_Msg_Box_Warning(
        main = main,
        title = main.tr('Invalid Path'),
        text = main.tr(f'''
            <div>The specified path "{path}" should be a directory, not a file!</div>
            <div>Please check your settings and try again.</div>
        '''),
    ).open()

def wl_msg_box_path_not_exist_confirm(main, path):
    reply = QMessageBox.question(
        main,
        main.tr('Path Not Exist'),
        main.tr(f'''
            {main.settings_global['styles']['style_dialog']}
            <body>
                <div>The specified path "{path}" does not exist.</div>

                <div>Do you want to create the directory?</div>
            </body>
        '''),
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )

    if reply == QMessageBox.Yes:
        wl_checking_misc.check_dir(path)

    return reply

# Settings - Files - Tags
def wl_msg_box_duplicate_tags(main):
    Wl_Msg_Box_Warning(
        main = main,
        title = main.tr('Duplicate Tags'),
        text = main.tr(f'''
            <div>The tag that you have specified already exists in the table!</div>
        ''')
    ).open()

def wl_msg_box_empty_opening_tag(main):
    Wl_Msg_Box_Warning(
        main = main,
        title = main.tr('Empty Opening Tag'),
        text = main.tr(f'''
            <div>The opening tag should not be left empty!</div>
        ''')
    ).open()

def wl_msg_box_invalid_xml_tag(main):
    Wl_Msg_Box_Warning(
        main = main,
        title = main.tr('Invalid XML Tag'),
        text = main.tr(f'''
            <div>The specified XML tag is invalid!</div>
        ''')
    ).open()

# Settings - Stop Word Lists
def wl_msg_box_duplicate_stop_words(main):
    Wl_Msg_Box_Warning(
        main = main,
        title = main.tr('Duplicate Stop Words'),
        text = main.tr(f'''
            <div>The stop word that you have specified already exists in the list!</div>
        ''')
    ).open()

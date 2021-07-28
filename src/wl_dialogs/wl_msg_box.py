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

# Duplicates
def wl_msg_box_duplicate_file_name(main):
    QMessageBox.warning(
        main,
        main.tr('Duplicate File Name'),
        main.tr(f'''
            {main.settings_global['styles']['style_dialog']}
            <body>
                <div>There is already a file with the same name in the file area.</div>
                <div>Please specify a different file name.</div>
            </body>
        '''),
        QMessageBox.Ok
    )

def wl_msg_box_duplicate_search_terms(main):
    QMessageBox.warning(
        main,
        main.tr('Duplicate Search Terms'),
        main.tr(f'''
            {main.settings_global['styles']['style_dialog']}
            <body>
                <div>The search term you have entered already exists in the list!</div>
            </body>
        ''')
    )

def wl_msg_box_duplicate_tags(main):
    QMessageBox.warning(
        main,
        main.tr('Duplicate Tags'),
        main.tr(f'''
            {main.settings_global['styles']['style_dialog']}
            <body>
                <div>The (pair of) tag you have entered already exists in the table!</div>
            </body>
        ''')
    )

def wl_msg_box_duplicate_stop_words(main):
    QMessageBox.warning(
        main,
        main.tr('Duplicate Stop Words'),
        main.tr(f'''
            {main.settings_global['styles']['style_dialog']}
            <body>
                <div>The stop word you have entered already exists in the list!</div>
            </body>
        ''')
    )

# Reset settings
def wl_msg_box_reset_settings(main):
    reply = QMessageBox.question(
        main,
        main.tr('Reset Settings'),
        main.tr(f'''
            {main.settings_global['styles']['style_dialog']}
            <body>
                <div>Do you really want to reset all settings to their defaults?</div>
            </body>
        '''),
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )

    if reply == QMessageBox.Yes:
        return True
    else:
        return False

def wl_msg_box_reset_all_settings(main):
    reply = QMessageBox.question(
        main,
        main.tr('Reset All Settings'),
        main.tr(f'''
            {main.settings_global['styles']['style_dialog']}
            <body>
                <div>Do you really want to reset all settings to their defaults?</div>
                <div><b>Warning: This will affect settings on all pages!</b></div>
            </body>
        '''),
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )

    if reply == QMessageBox.Yes:
        return True
    else:
        return False

def wl_msg_box_reset_mappings(main):
    reply = QMessageBox.question(
        main,
        main.tr('Reset Mappings'),
        main.tr(f'''
            {main.settings_global['styles']['style_dialog']}
            <body>
                <div>Do you really want to reset all mappings to their defaults?</div>
                <div><b>Note: This will only affect the mapping settings in the currently shown table.</b></div>
            </body>
        '''),
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )

    if reply == QMessageBox.Yes:
        return True
    else:
        return False

def wl_msg_box_reset_all_mappings(main):
    reply = QMessageBox.question(
        main,
        main.tr('Reset All Mappings'),
        main.tr(f'''
            {main.settings_global['styles']['style_dialog']}
            <body>
                <div>Do you really want to reset all mappings to their defaults?</div>
                <div><b>Warning: This will affect the mapping settings in all tables!</b></div>
            </body>
        '''),
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )

    if reply == QMessageBox.Yes:
        return True
    else:
        return False

def wl_msg_box_reset_layouts(main):
    reply = QMessageBox.question(
        main,
        main.tr('Reset Layouts'),
        main.tr(f'''
            {main.settings_global['styles']['style_dialog']}
            <body>
                <div>Do you really want to reset all layouts to their default settings?</div>
            </body>
        '''),
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )

    if reply == QMessageBox.Yes:
        return True
    else:
        return False

# Files
class Wl_Msg_Box_No_Files_Selected(Wl_Msg_Box_Warning):
    def __init__(self, main):
        super().__init__(
            main = main,
            title = main.tr('No Files Selected'),
            text = main.tr('''
                <div>There are no files being currently opened and selected.</div>
                <div>Please open files first or check your file settings.</div>
            ''')
        )

def wl_msg_box_no_files_selected(main):
    msg_box_no_files_selected = Wl_Msg_Box_No_Files_Selected(main)

    msg_box_no_files_selected.open()

class Wl_Msg_Box_Identical_Src_Tgt_Files(Wl_Msg_Box_Warning):
    def __init__(self, main):
        super().__init__(
            main = main,
            title = main.tr('Identical source and target files'),
            text = main.tr('''
                <div>The source and target file you have specified are identical. Please check your settings and try again.</div>
            ''')
        )

def wl_msg_box_identical_src_tgt_files(main):
    msg_box_identical_src_tgt_files = Wl_Msg_Box_Identical_Src_Tgt_Files(main)

    msg_box_identical_src_tgt_files.open()

class Wl_Msg_Box_Missing_Ref_Files(Wl_Msg_Box_Warning):
    def __init__(self, main):
        super().__init__(
            main = main,
            title = main.tr('Missing Reference Files'),
            text = main.tr('''
                <div>You have not specified any reference files yet.</div>
            ''')
        )

def wl_msg_box_missing_ref_files(main):
    msg_box_missing_ref_files = Wl_Msg_Box_Missing_Ref_Files(main)

    msg_box_missing_ref_files.open()

class Wl_Msg_Box_Missing_Observed_Files(Wl_Msg_Box_Warning):
    def __init__(self, main):
        super().__init__(
            main = main,
            title = main.tr('Missing Observed Files'),
            text = main.tr('''
                <div>You have specified reference files, but you have not opened and selected any observed files yet.</div>
            ''')
        )

def wl_msg_box_missing_observed_files(main):
    msg_box_missing_observed_files = Wl_Msg_Box_Missing_Observed_Files(main)

    msg_box_missing_observed_files.open()

class Wl_Msg_Box_Invalid_Xml_File(Wl_Msg_Box_Warning):
    def __init__(self, main):
        super().__init__(
            main = main,
            title = main.tr('Invalid XML File'),
            text = main.tr('''
                <div>If the input is an XML file, it must be both tokenized and tagged.</div>
            ''')
        )

def wl_msg_box_invalid_xml_file(main):
    msg_box_invalid_xml_file = Wl_Msg_Box_Invalid_Xml_File(main)

    msg_box_invalid_xml_file.open()

# Search terms
class Wl_Msg_Box_Missing_Search_Terms(Wl_Msg_Box_Warning):
    def __init__(self, main):
        super().__init__(
            main = main,
            title = main.tr('Missing Search Terms'),
            text = main.tr('''
                <div>
                    You have not specified any search terms yet, please enter one in the input box under "<span style="color: #F00; font-weight: bold;">Search Term</span>" first.
                </div>
            ''')
        )

def wl_msg_box_missing_search_terms(main):
    msg_box_missing_search_terms = Wl_Msg_Box_Missing_Search_Terms(main)

    msg_box_missing_search_terms.open()

class Wl_Msg_Box_Missing_Search_Terms_Optional(Wl_Msg_Box_Warning):
    def __init__(self, main):
        super().__init__(
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
        )

def wl_msg_box_missing_search_terms_optional(main):
    msg_box_missing_search_terms_optional = Wl_Msg_Box_Missing_Search_Terms_Optional(main)

    msg_box_missing_search_terms_optional.open()

def wl_msg_box_missing_search_terms_concordancer_parallel(main):
    reply = QMessageBox.question(
        main,
        main.tr('Empty Search Terms'),
        main.tr(f'''
            {main.settings_global['styles']['style_dialog']}
            <body>
                <div>You have not specified any search terms. Do you want to search for additions in the target file?</div>
            </body>
        '''),
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )

    if reply == QMessageBox.Yes:
        return True
    else:
        return False

# Results
class Wl_Msg_Box_No_Results(Wl_Msg_Box_Warning):
    def __init__(self, main):
        super().__init__(
            main = main,
            title = main.tr('No Results'),
            text = main.tr('''
                <div>Data processing has completed successfully, but there are no results to display.</div>
                <div>You can change your settings and try again.</div>
            ''')
        )

def wl_msg_box_no_results(main):
    msg_box_no_results = Wl_Msg_Box_No_Results(main)

    msg_box_no_results.open()

class Wl_Msg_Box_No_Search_Results(Wl_Msg_Box_Warning):
    def __init__(self, main):
        super().__init__(
            main = main,
            title = main.tr('No Search Results'),
            text = main.tr('''
                <div>Searching has completed successfully, but there are no results found.</div>
                <div>You can change your settings and try again.</div>
            ''')
        )

def wl_msg_box_no_search_results(main):
    msg_box_no_search_results = Wl_Msg_Box_No_Search_Results(main)

    msg_box_no_search_results.open()

# Export
def wl_msg_box_export_list(main, file_path):
    QMessageBox.information(
        main,
        main.tr('Export Completed'),
        main.tr(f'''
            {main.settings_global['styles']['style_dialog']}
            <body>
                <div>The list has been successfully exported to "{file_path}".</div>
            </body>
        '''),
        QMessageBox.Ok
    )

def wl_msg_box_export_table_success(main, file_path):
    QMessageBox.information(
        main,
        main.tr('Export Completed'),
        main.tr(f'''
            {main.settings_global['styles']['style_dialog']}
            <body>
                <div>The table has been successfully exported to "{file_path}".</div>
            </body>
        '''),
        QMessageBox.Ok
    )

def wl_msg_box_export_table_error(main, file_path):
    QMessageBox.warning(
        main,
        main.tr('Export Error'),
        main.tr(f'''
            {main.settings_global['styles']['style_dialog']}
            <body>
                <div>Access to "{file_path}" is denied, please specify another location or close the file and try again.</div>
            </body>
        '''),
        QMessageBox.Ok
    )

# Settings
def wl_msg_box_path_not_exist(main, path):
    QMessageBox.warning(
        main,
        main.tr('Invalid Path'),
        main.tr(f'''
            {main.settings_global['styles']['style_dialog']}
            <body>
                <div>The specified path "{path}" does not exist!</div>
                <div>Please check your settings and try again.</div>
            </body>
        '''),
        QMessageBox.Ok
    )

def wl_msg_box_path_not_dir(main, path):
    QMessageBox.warning(
        main,
        main.tr('Invalid Path'),
        main.tr(f'''
            {main.settings_global['styles']['style_dialog']}
            <body>
                <div>The specified path "{path}" should be a directory, not a file!</div>
                <div>Please check your settings and try again.</div>
            </body>
        '''),
        QMessageBox.Ok
    )

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

def wl_msg_box_invalid_xml_tags(main):
    QMessageBox.warning(
        main,
        main.tr('Invalid XML Tags'),
        main.tr(f'''
            {main.settings_global['styles']['style_dialog']}
            <body>
                <div>You must specify at least one (pair of) tag for each level of XML files!</div>
            </body>
        '''),
        QMessageBox.Ok
    )

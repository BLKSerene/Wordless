#
# Wordless: Dialogs - Message Box
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_checking import wordless_checking_misc

class Wordless_Msg_Box(QMessageBox):
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

class Wordless_Msg_Box_Info(Wordless_Msg_Box):
    def __init__(self, main, title, text):
        super().__init__(main = main,
                         icon = QMessageBox.Information,
                         title = title,
                         text = text)

class Wordless_Msg_Box_Info_Help(Wordless_Msg_Box):
    def __init__(self, main, title, text):
        super().__init__(main = main,
                         icon = QMessageBox.Information,
                         title = title,
                         text = text)

        self.setTextFormat(Qt.RichText)
        self.setTextInteractionFlags(Qt.TextBrowserInteraction)

class Wordless_Msg_Box_Warning(Wordless_Msg_Box):
    def __init__(self, main, title, text):
        super().__init__(main = main,
                         icon = QMessageBox.Warning,
                         title = title,
                         text = text)

# Duplicates
def wordless_msg_box_duplicate_file_name(main):
    QMessageBox.warning(main,
                        main.tr('Duplicate File Name'),
                        main.tr(f'''
                            {main.settings_global['styles']['style_dialog']}
                            <body>
                                <div>There is already a file with the same name in the file area.</div>
                                <div>Please specify a different file name.</div>
                            </body>
                        '''),
                        QMessageBox.Ok)

def wordless_msg_box_duplicate_search_terms(main):
    QMessageBox.warning(main,
                        main.tr('Duplicate Search Terms'),
                        main.tr(f'''
                            {main.settings_global['styles']['style_dialog']}
                            <body>
                                <div>The search term you have entered already exists in the list!</div>
                            </body>
                        '''))

def wordless_msg_box_duplicate_tags(main):
    QMessageBox.warning(main,
                        main.tr('Duplicate Tags'),
                        main.tr(f'''
                            {main.settings_global['styles']['style_dialog']}
                            <body>
                                <div>The (pair of) tag you have entered already exists in the table!</div>
                            </body>
                        '''))

def wordless_msg_box_duplicate_stop_words(main):
    QMessageBox.warning(main,
                        main.tr('Duplicate Stop Words'),
                        main.tr(f'''
                            {main.settings_global['styles']['style_dialog']}
                            <body>
                                <div>The stop word you have entered already exists in the list!</div>
                            </body>
                        '''))

# Reset settings
def wordless_msg_box_reset_settings(main):
    reply = QMessageBox.question(main,
                                 main.tr('Reset Settings'),
                                 main.tr(f'''
                                     {main.settings_global['styles']['style_dialog']}
                                     <body>
                                         <div>Do you really want to reset all settings to their defaults?</div>
                                     </body>
                                 '''),
                                 QMessageBox.Yes | QMessageBox.No,
                                 QMessageBox.No)

    if reply == QMessageBox.Yes:
        return True
    else:
        return False

def wordless_msg_box_reset_all_settings(main):
    reply = QMessageBox.question(main,
                                 main.tr('Reset All Settings'),
                                 main.tr(f'''
                                     {main.settings_global['styles']['style_dialog']}
                                     <body>
                                         <div>Do you really want to reset all settings to their defaults?</div>
                                         <div><b>Warning: This will affect settings on all pages!</b></div>
                                     </body>
                                 '''),
                                 QMessageBox.Yes | QMessageBox.No,
                                 QMessageBox.No)

    if reply == QMessageBox.Yes:
        return True
    else:
        return False

def wordless_msg_box_reset_mappings(main):
    reply = QMessageBox.question(main,
                                 main.tr('Reset Mappings'),
                                 main.tr(f'''
                                     {main.settings_global['styles']['style_dialog']}
                                     <body>
                                         <div>Do you really want to reset all mappings to their defaults?</div>
                                         <div><b>Note: This will only affect the mapping settings in the currently shown table.</b></div>
                                     </body>
                                 '''),
                                 QMessageBox.Yes | QMessageBox.No,
                                 QMessageBox.No)

    if reply == QMessageBox.Yes:
        return True
    else:
        return False

def wordless_msg_box_reset_all_mappings(main):
    reply = QMessageBox.question(main,
                                 main.tr('Reset All Mappings'),
                                 main.tr(f'''
                                     {main.settings_global['styles']['style_dialog']}
                                     <body>
                                         <div>Do you really want to reset all mappings to their defaults?</div>
                                         <div><b>Warning: This will affect the mapping settings in all tables!</b></div>
                                     </body>
                                 '''),
                                 QMessageBox.Yes | QMessageBox.No,
                                 QMessageBox.No)

    if reply == QMessageBox.Yes:
        return True
    else:
        return False

def wordless_msg_box_reset_layouts(main):
    reply = QMessageBox.question(main,
                                 main.tr('Reset Layouts'),
                                 main.tr(f'''
                                     {main.settings_global['styles']['style_dialog']}
                                     <body>
                                         <div>Do you really want to reset all layouts to their default settings?</div>
                                     </body>
                                 '''),
                                 QMessageBox.Yes | QMessageBox.No,
                                 QMessageBox.No)

    if reply == QMessageBox.Yes:
        return True
    else:
        return False

# Files
class Wordless_Msg_Box_No_Files_Selected(Wordless_Msg_Box_Warning):
    def __init__(self, main):
        super().__init__(
            main = main,
            title = main.tr('No Files Selected'),
            text = main.tr('''
                <div>There are no files being currently selected.</div>
                <div>Please check and try again.</div>
            ''')
        )

def wordless_msg_box_no_files_selected(main):
    msg_box_no_files_selected = Wordless_Msg_Box_No_Files_Selected(main)

    msg_box_no_files_selected.open()

class Wordless_Msg_Box_Missing_Observed_File(Wordless_Msg_Box_Warning):
    def __init__(self, main):
        super().__init__(
            main = main,
            title = main.tr('Missing Observed File'),
            text = main.tr('''
                <div>You have specified your reference file, but you haven't selected any observed file yet.</div>
            ''')
        )

def wordless_msg_box_missing_observed_file(main):
    msg_box_missing_observed_file = Wordless_Msg_Box_Missing_Observed_File(main)

    msg_box_missing_observed_file.open()

# Search Terms
class Wordless_Msg_Box_Missing_Search_Term(Wordless_Msg_Box_Warning):
    def __init__(self, main):
        super().__init__(
            main = main,
            title = main.tr('Missing Search Term'),
            text = main.tr('''
                <div>
                    You haven't specify any search term yet, please enter one in the input box under "<span style="color: #F00; font-weight: bold;">Search Term</span>" first.
                </div>
            ''')
        )

def wordless_msg_box_missing_search_term(main):
    msg_box_missing_search_term = Wordless_Msg_Box_Missing_Search_Term(main)

    msg_box_missing_search_term.open()

class Wordless_Msg_Box_Missing_Search_Term_Optional(Wordless_Msg_Box_Warning):
    def __init__(self, main):
        super().__init__(
            main = main,
            title = main.tr('Missing Search Term'),
            text = main.tr('''
                <div>
                    You haven't specified any search term yet, please enter one in the input box under "<span style="color: #F00; font-weight: bold;">Search Term</span>" first.
                </div>

                <div>
                    Or, you can disable searching altogether by unchecking "<span style="color: #F00; font-weight: bold;">Search Settings</span>", which will then generate all possible results, but it is not recommended to do so since the processing speed might be too slow.
                </div>
            ''')
        )

def wordless_msg_box_missing_search_term_optional(main):
    msg_box_missing_search_term_optional = Wordless_Msg_Box_Missing_Search_Term_Optional(main)

    msg_box_missing_search_term_optional.open()

# Results
class Wordless_Msg_Box_No_Results(Wordless_Msg_Box_Warning):
    def __init__(self, main):
        super().__init__(
            main = main,
            title = main.tr('No Results'),
            text = main.tr('''
                <div>Data processing has completed successfully, but there are no results to display.</div>
                <div>You can change your settings and try again.</div>
            ''')
        )

def wordless_msg_box_no_results(main):
    msg_box_no_results = Wordless_Msg_Box_No_Results(main)

    msg_box_no_results.open()

class Wordless_Msg_Box_No_Search_Results(Wordless_Msg_Box_Warning):
    def __init__(self, main):
        super().__init__(
            main = main,
            title = main.tr('No Search Results'),
            text = main.tr('''
                <div>Searching has completed successfully, but there are no results found.</div>
                <div>You can change your settings and try again.</div>
            ''')
        )

def wordless_msg_box_no_search_results(main):
    msg_box_no_search_results = Wordless_Msg_Box_No_Search_Results(main)

    msg_box_no_search_results.open()

# Export
def wordless_msg_box_export_list(main, file_path):
    QMessageBox.information(main,
                            main.tr('Export Completed'),
                            main.tr(f'''
                                {main.settings_global['styles']['style_dialog']}
                                <body>
                                    <div>The list has been successfully exported to "{file_path}".</div>
                                </body>
                            '''),
                            QMessageBox.Ok)

def wordless_msg_box_export_table_success(main, file_path):
    QMessageBox.information(main,
                            main.tr('Export Completed'),
                            main.tr(f'''
                                {main.settings_global['styles']['style_dialog']}
                                <body>
                                    <div>The table has been successfully exported to "{file_path}".</div>
                                </body>
                            '''),
                            QMessageBox.Ok)

def wordless_msg_box_export_table_error(main, file_path):
    QMessageBox.warning(main,
                            main.tr('Export Error'),
                            main.tr(f'''
                                {main.settings_global['styles']['style_dialog']}
                                <body>
                                    <div>Access to "{file_path}" is denied, please specify another location or close the file and try again.</div>
                                </body>
                            '''),
                            QMessageBox.Ok)

# Settings
def wordless_msg_box_path_not_exist(main, path):
    QMessageBox.warning(main,
                        main.tr('Invalid Path'),
                        main.tr(f'''
                            {main.settings_global['styles']['style_dialog']}
                            <body>
                                <div>The specified path "{path}" does not exist!</div>
                                <div>Please change your settings and try again.</div>
                            </body>
                        '''),
                        QMessageBox.Ok)

def wordless_msg_box_path_not_dir(main, path):
    QMessageBox.warning(main,
                        main.tr('Invalid Path'),
                        main.tr(f'''
                            {main.settings_global['styles']['style_dialog']}
                            <body>
                                <div>The specified path "{path}" should be a directory, not a file!</div>
                                <div>Please change your settings and try again.</div>
                            </body>
                        '''),
                        QMessageBox.Ok)

def wordless_msg_box_path_not_exist_confirm(main, path):
    reply = QMessageBox.question(main,
                                 main.tr('Path Not Exist'),
                                 main.tr(f'''
                                     {main.settings_global['styles']['style_dialog']}
                                     <body>
                                         <div>The specified path "{path}" does not exist.</div>
                                         <div>Do you want to create the directory?</div>
                                     </body>
                                 '''),
                                 QMessageBox.Yes | QMessageBox.No,
                                 QMessageBox.No)

    if reply == QMessageBox.Yes:
        wordless_checking_misc.check_dir(path)

    return reply

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

class Wordless_Message_Box(QMessageBox):
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

class Wordless_Message_Box_Info(Wordless_Message_Box):
    def __init__(self, main, title, text):
        super().__init__(main = main,
                         icon = QMessageBox.Information,
                         title = title,
                         text = text)

class Wordless_Message_Box_Info_Help(Wordless_Message_Box):
    def __init__(self, main, title, text):
        super().__init__(main = main,
                         icon = QMessageBox.Information,
                         title = title,
                         text = text)

        self.setTextFormat(Qt.RichText)
        self.setTextInteractionFlags(Qt.TextBrowserInteraction)

class Wordless_Message_Box_Warning(Wordless_Message_Box):
    def __init__(self, main, title, text):
        super().__init__(main = main,
                         icon = QMessageBox.Warning,
                         title = title,
                         text = text)

# Files
def wordless_message_text_file_error(files, text_singular, text_plural):
    message_text = ''

    if files:
        if len(files) == 1:
            message_text = text_singular
        else:
            message_text = text_plural

        message_text = f'''
            <div>{message_text}</div>
            <ul>{''.join([f'<li>{file}</li>' for file in files])}</ul>
        '''

    return message_text

def wordless_message_box_file_error_on_opening(main,
                                               files_duplicate,
                                               files_empty,
                                               files_unsupported,
                                               files_parsing_error):
    message = ''

    message += wordless_message_text_file_error(
        files_duplicate,
        text_singular = main.tr('The following file has already been opened:'),
        text_plural = main.tr('The following files have already been opened:'))

    message += wordless_message_text_file_error(
        files_empty,
        text_singular = main.tr('The following file is empty:'),
        text_plural = main.tr('The following files are empty:'))

    message += wordless_message_text_file_error(
        files_unsupported,
        text_singular = main.tr('Failed to open the following file because the file type is not currently supported:'),
        text_plural = main.tr('Failed to open the following files because the file types are not currently supported:'))

    message += wordless_message_text_file_error(
        files_parsing_error,
        text_singular = main.tr('Failed to parse the following file due to an encoding error:'),
        text_plural = main.tr('Failed to parse the following files due to encoding errors:'))

    if message:
        QMessageBox.information(main,
                                main.tr('Error Opening File'),
                                main.tr(f'''
                                    {main.settings_global['styles']['style_dialog']}
                                    <body>
                                        <div>
                                            An error occurred while opening the files, so some files are skipped and they will not be added to the file area.
                                        </div>
                                        {message}
                                    </body>
                                '''),
                                QMessageBox.Ok)

def wordless_message_box_file_error_on_startup(main,
                                               files_missing,
                                               files_empty):
    message = ''

    message += wordless_message_text_file_error(
        files_missing,
        text_singular = main.tr('The following file no longer exists in its original location:'),
        text_plural = main.tr('The following files no longer exist in their original locations:'))

    message += wordless_message_text_file_error(
        files_empty,
        text_singular = main.tr('The following file is empty:'),
        text_plural = main.tr('The following files are empty:'))

    if message:
        QMessageBox.information(main,
                                main.tr('Error Loading File'),
                                main.tr(f'''
                                    {main.settings_global['styles']['style_dialog']}
                                    <body>
                                        <div>
                                            An error occurred while loading the files on startup, so some files are skipped and they will be removed from the file area.
                                        </div>
                                        {message}
                                    </body>
                                '''),
                                QMessageBox.Ok)

def wordless_message_box_file_error_on_importing(main,
                                                 files_empty,
                                                 files_loading_error):
    message = ''

    message += wordless_message_text_file_error(
        files_empty,
        text_singular = main.tr('The following file is empty:'),
        text_plural = main.tr('The following files are empty:'))

    message += wordless_message_text_file_error(
        files_loading_error,
        text_singular = main.tr('Failed to load the following file due to an encoding error:'),
        text_plural = main.tr('Failed to load the following files due to encoding errors:'))

    if message:
        QMessageBox.information(main,
                                main.tr('Error Importing File'),
                                main.tr(f'''
                                    {main.settings_global['styles']['style_dialog']}
                                    <body>
                                        <div>
                                            An error occurred while importing the files, so some files are skipped and will not be imported into the list.
                                        </div>
                                        {message}
                                    </body>
                                '''),
                                QMessageBox.Ok)

def wordless_message_box_file_error_on_loading(main,
                                               files_missing,
                                               files_empty,
                                               files_loading_error):
    message = ''

    message += wordless_message_text_file_error(
        files_missing,
        text_singular = main.tr('The following file no longer exists in its original location:'),
        text_plural = main.tr('The following files no longer exist in their original locations:'))

    message += wordless_message_text_file_error(
        files_empty,
        text_singular = main.tr('The following file is empty:'),
        text_plural = main.tr('The following files are empty:'))

    message += wordless_message_text_file_error(
        files_loading_error,
        text_singular = main.tr('Failed to load the following file due to an encoding error:'),
        text_plural = main.tr('Failed to load the following files due to encoding errors:'))

    if message:
        QMessageBox.information(main,
                                main.tr('Error Loading File'),
                                main.tr(f'''
                                    {main.settings_global['styles']['style_dialog']}
                                    <body>
                                        <div>
                                            An error occurred while loading the files, so some files will be removed from the file area. Please check your settings and try again.
                                        </div>
                                        {message}
                                    </body>
                                '''),
                                QMessageBox.Ok)

def wordless_message_box_file_error_on_loading_colligation(main,
                                                           files_unsupported_pos_tagging):
    message = ''

    message += wordless_message_text_file_error(
        files_unsupported_pos_tagging,
        text_singular = main.tr('The built-in POS taggers currently have no support for the language of the following file, please check your settings or provide a file that has already been POS-tagged.'),
        text_plural = main.tr('The built-in POS taggers currently have no support for the languages of the following files, please check your settings or provide files that have already been POS-tagged.'))

    if message:
        QMessageBox.information(main,
                                main.tr('Error Loading File'),
                                main.tr(f'''
                                    {main.settings_global['styles']['style_dialog']}
                                    <body>
                                        {message}
                                    </body>
                                '''),
                                QMessageBox.Ok)

def wordless_message_box_detection_failed(main,
                                          files_detection_failed_encoding,
                                          files_detection_failed_text_type,
                                          files_detection_failed_lang):
    message = ''

    message += wordless_message_text_file_error(
        files_detection_failed_encoding,
        text_singular = main.tr('Failed to detect the encoding of the following file:'),
        text_plural = main.tr('Failed to detect the encodings of the following files:'))

    message += wordless_message_text_file_error(
        files_detection_failed_text_type,
        text_singular = main.tr('Failed to detect the text type of the following file:'),
        text_plural = main.tr('Failed to detect the text types of the following files:'))

    message += wordless_message_text_file_error(
        files_detection_failed_lang,
        text_singular = main.tr('Failed to detect the language of the following file:'),
        text_plural = main.tr('Failed to detect the languages of the following files:'))

    if message:
        QMessageBox.information(main,
                                main.tr('Auto-detection Failed'),
                                main.tr(f'''
                                    {main.settings_global['styles']['style_dialog']}
                                    <body>
                                        <div>
                                            An error occurred during auto-detection. Pleas change the settings of some files manually.
                                        </div>
                                        {message}
                                    </body>
                                '''),
                                QMessageBox.Ok)

# Duplicates
def wordless_message_box_duplicate_file_name(main):
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

def wordless_message_box_duplicate_search_terms(main):
    QMessageBox.warning(main,
                        main.tr('Duplicate Search Terms'),
                        main.tr(f'''
                            {main.settings_global['styles']['style_dialog']}
                            <body>
                                <div>The search term you have entered already exists in the list!</div>
                            </body>
                        '''))

def wordless_message_box_duplicate_tags(main):
    QMessageBox.warning(main,
                        main.tr('Duplicate Tags'),
                        main.tr(f'''
                            {main.settings_global['styles']['style_dialog']}
                            <body>
                                <div>The (pair of) tag you have entered already exists in the table!</div>
                            </body>
                        '''))

def wordless_message_box_duplicate_stop_words(main):
    QMessageBox.warning(main,
                        main.tr('Duplicate Stop Words'),
                        main.tr(f'''
                            {main.settings_global['styles']['style_dialog']}
                            <body>
                                <div>The stop word you have entered already exists in the list!</div>
                            </body>
                        '''))

# Resettings
def wordless_message_box_reset_settings(main):
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

    return reply

def wordless_message_box_reset_layouts(main):
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

    return reply

# Files
class Wordless_Message_Box_No_Files_Selected(Wordless_Message_Box_Warning):
    def __init__(self, main):
        super().__init__(
            main = main,
            title = main.tr('No Files Selected'),
            text = main.tr('''
                <div>There are no files being currently selected.</div>
                <div>Please check and try again.</div>
            ''')
        )

class Wordless_Message_Box_Missing_Observed_File(Wordless_Message_Box_Warning):
    def __init__(self, main):
        super().__init__(
            main = main,
            title = main.tr('Missing Observed File'),
            text = main.tr('''
                <div>You have specified your reference file, but you haven't selected any observed file yet.</div>
            ''')
        )

def wordless_message_box_no_files_selected(main):
    message_box_no_files_selected = Wordless_Message_Box_No_Files_Selected(main)

    message_box_no_files_selected.open()

def wordless_message_box_missing_observed_files(main):
    message_box_missing_observed_files = Wordless_Message_Box_Missing_Observed_Files(main)

    message_box_missing_observed_files.open()

# Search Terms
class Wordless_Message_Box_Missing_Search_Term(Wordless_Message_Box_Warning):
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

class Wordless_Message_Box_Missing_Search_Term_Optional(Wordless_Message_Box_Warning):
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

def wordless_message_box_missing_search_term(main):
    message_box_missing_search_term = Wordless_Message_Box_Missing_Search_Term(main)

    message_box_missing_search_term.open()

def wordless_message_box_missing_search_term_optional(main):
    message_box_missing_search_term_optional = Wordless_Message_Box_Missing_Search_Term_Optional(main)

    message_box_missing_search_term_optional.open()

# Results
class Wordless_Message_Box_No_Results(Wordless_Message_Box_Warning):
    def __init__(self, main):
        super().__init__(
            main = main,
            title = main.tr('No Results'),
            text = main.tr('''
                <div>Data generation completed successfully, but there are no results to show.</div>
                <div>You can change your settings and try again.</div>
            ''')
        )

def wordless_message_box_no_results(main):
    message_box_no_results = Wordless_Message_Box_No_Results(main)

    message_box_no_results.open()

def wordless_message_box_no_search_results(main):
    QMessageBox.information(main,
                            main.tr('No Search Results'),
                            main.tr(f'''
                                {main.settings_global['styles']['style_dialog']}
                                <body>
                                    <div>There is nothing that could be found in the table.</div>
                                </body>
                            '''),
                            QMessageBox.Ok)

# Export
def wordless_message_box_export_search_terms(main, file_path):
    QMessageBox.information(main,
                            main.tr('Export Completed'),
                            main.tr(f'''
                                {main.settings_global['styles']['style_dialog']}
                                <body>
                                    <div>The search terms have been successfully exported to "{file_path}".</div>
                                </body>
                            '''),
                            QMessageBox.Ok)

def wordless_message_box_export_table(main, file_path):
    QMessageBox.information(main,
                            main.tr('Export Completed'),
                            main.tr(f'''
                                {main.settings_global['styles']['style_dialog']}
                                <body>
                                    <div>The table has been successfully exported to "{file_path}".</div>
                                </body>
                            '''),
                            QMessageBox.Ok)

def wordless_message_box_export_stop_words(main, file_path):
    QMessageBox.information(main,
                            main.tr('Export Completed'),
                            main.tr(f'''
                                {main.settings_global['styles']['style_dialog']}
                                <body>
                                    <div>The stop words have been successfully exported to "{file_path}".</div>
                                </body>
                            '''),
                            QMessageBox.Ok)

# Settings
def wordless_message_box_path_not_exist(main, path):
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

def wordless_message_box_path_not_dir(main, path):
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

def wordless_message_box_path_not_exist_confirm(main, path):
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

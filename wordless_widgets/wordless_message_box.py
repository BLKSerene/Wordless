#
# Wordless: Widgets - Message Box
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

class Wordless_Message_Box_Info(QMessageBox):
    def __init__(self, main, title, text):
        super().__init__(
            QMessageBox.Information,
            title,
            f'''
                {main.settings_global['styles']['style_dialog']}
                <body>
                    {text}
                </body>
            ''',
            parent = main)

        self.setTextFormat(Qt.RichText)
        self.setTextInteractionFlags(Qt.TextBrowserInteraction)

def wordless_message_box_exit(main):
    reply = QMessageBox.question(main,
                                 main.tr('Exit Confirmation'),
                                 main.tr(f'''{main.settings_global['styles']['style_dialog']}
                                             <body>
                                                 <div>Do you really want to quit?</div>
                                                 <div><span style="color: #F00; font-weight: bold;">Note</span>: All unsaved data and figures will be lost.</div>
                                             </body>
                                         '''),
                                 QMessageBox.Yes | QMessageBox.No,
                                 QMessageBox.No)

    return reply

# Files
def wordless_message_box_error_files(main,
                                     files_missing = [],
                                     files_duplicate = [],
                                     files_empty = [],
                                     files_unsupported = [],
                                     files_encoding_error = [],
                                     files_loading_error = []):
    message = ''

    if (files_missing or
        files_duplicate or
        files_empty or
        files_unsupported or
        files_encoding_error or
        files_loading_error):
        if files_missing:
            list_files = ''.join([f'<li>{file}</li>' for file in files_missing])

            if len(files_missing) == 1:
                message += main.tr(f'''
                               <div>The following file no longer exists in its original location:</div>
                               <ul>{list_files}</ul>
                           ''')
            else:
                message += main.tr(f'''
                               <div>The following files no longer exists in their original location:</div>
                               <ol>{list_files}</ol>
                           ''')

        if files_duplicate:
            list_files = ''.join([f'<li>{file}</li>' for file in files_duplicate])

            if len(files_duplicate) == 1:
                message += main.tr(f'''
                               <div>The following file has already been opened:</div>
                               <ul>{list_files}</ul>
                           ''')
            else:
                message += main.tr(f'''
                               <div>The following files have already been opened:</div>
                               <ol>{list_files}</ol>
                           ''')

        if files_empty:
            list_files = ''.join([f'<li>{file}</li>' for file in files_empty])

            if len(files_empty) == 1:
                message += main.tr(f'''
                               <div>The following file is empty:</div>
                               <ul>{list_files}</ul>
                           ''')
            else:
                message += main.tr(f'''
                               <div>The following files are empty:</div>
                               <ol>{list_files}</ol>
                           ''')

        if files_unsupported:
            list_files = ''.join([f'<li>{file}</li>' for file in files_unsupported])

            if len(files_unsupported) == 1:
                message += main.tr(f'''
                               <div>Failed to open the following file because the file type is not currently supported:</div>
                               <ul>{list_files}</ul>
                           ''')
            else:
                message += main.tr(f'''
                               <div>Failed to open the following files because the file types are not currently supported:</div>
                               <ol>{list_files}</ol>
                           ''')

        if files_encoding_error:
            list_files = ''.join([f'<li>{file}</li>' for file in files_encoding_error])

            if len(files_encoding_error) == 1:
                message += main.tr(f'''
                               <div>Failed to open the following file due to an encoding error:</div>
                               <ul>{list_files}</ul>
                           ''')
            else:
                message += main.tr(f'''
                               <div>Failed to open the following files due to encoding errors:</div>
                               <ol>{list_files}</ol>
                           ''')

        if files_loading_error:
            list_files = ''.join([f'<li>{file}</li>' for file in files_loading_error])

            if len(files_loading_error) == 1:
                message += main.tr(f'''
                               <div>Failed to read the following file due to an encoding error:</div>
                               <ul>{list_files}</ul>
                           ''')
            else:
                message += main.tr(f'''
                               <div>Failed to read the following files due to encoding errors:</div>
                               <ol>{list_files}</ol>
                           ''')

        QMessageBox.information(main,
                                main.tr('Loading Error'),
                                main.tr(f'''
                                    {main.settings_global['styles']['style_dialog']}
                                    <body>
                                        {message}
                                    </body>
                                '''),
                                QMessageBox.Ok)

def wordless_message_box_error_ref_file(main):
    QMessageBox.warning(main,
                        main.tr('Loading Error'),
                        main.tr(f'''
                            {main.settings_global['styles']['style_dialog']}
                            <body>
                                <div>An error occurred during loading of the reference file!</div>
                                <div>Please check and try again.</div>
                            </body>
                        '''),
                        QMessageBox.Ok)

def wordless_message_box_auto_detection_failed(main,
                                               files_encoding_detection_failed,
                                               files_lang_detection_failed):
    message = ''

    if files_encoding_detection_failed or files_lang_detection_failed:
        if files_encoding_detection_failed:
            list_files = ''.join([f'<li>{file}</li>' for file in files_encoding_detection_failed])

            if len(files_encoding_detection_failed) == 1:
                message += main.tr(f'''
                               <div>Failed to detect the encoding of the following file:</div>
                               <ul>{list_files}</ul>
                           ''')
            else:
                message += main.tr(f'''
                               <div>Failed to detect the encodings of the following files:</div>
                               <ol>{list_files}</ol>
                           ''')

        if files_lang_detection_failed:
            list_files = ''.join([f'<li>{file}</li>' for file in files_lang_detection_failed])

            if len(files_lang_detection_failed) == 1:
                message += main.tr(f'''
                               <div>Failed to detect the language of the following file:</div>
                               <ul>{list_files}</ul>
                           ''')
            else:
                message += main.tr(f'''
                               <div>Failed to detect the languages of the following files:</div>
                               <ol>{list_files}</ol>
                           ''')

        QMessageBox.information(main,
                                main.tr('Auto-detection Failed'),
                                main.tr(f'''
                                    {main.settings_global['styles']['style_dialog']}
                                    <body>
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
                                <div>There is already a file with the same name that has been loaded into Wordless.</div>
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

def wordless_message_box_no_files_selected(main):
    QMessageBox.warning(main,
                        main.tr('No Files Selected'),
                        main.tr(f'''
                            {main.settings_global['styles']['style_dialog']}
                            <body>
                                <div>There are no files being currently selected!</div>
                                <div>Please check and try again.</div>
                            </body>
                        '''),
                        QMessageBox.Ok)

def wordless_message_box_missing_ref_file(main):
    QMessageBox.warning(main,
                        main.tr('Missing Reference File'),
                        main.tr(f'''
                            {main.settings_global['styles']['style_dialog']}
                            <body>
                                <div>Please open and select your reference file first!</div>
                            </body>
                        '''),
                        QMessageBox.Ok)

def wordless_message_box_missing_observed_files(main):
    QMessageBox.warning(main,
                        main.tr('Missing Observed File(s)'),
                        main.tr(f'''
                            {main.settings_global['styles']['style_dialog']}
                            <body>
                                <div>Please open and select your observed file(s) first!</div>
                            </body>
                        '''),
                        QMessageBox.Ok)

# Search Terms
def wordless_message_box_empty_search_term(main):
    QMessageBox.warning(main,
                        main.tr('Empty Search Term'),
                        main.tr(f'''
                            {main.settings_global['styles']['style_dialog']}
                            <body>
                                <div>You haven't specify any search term yet, please enter one in the input box under "<span style="color: #F00; font-weight: bold;">Search Term</span>" first.
                                </div>
                            </body>
                        '''),
                        QMessageBox.Ok)

def wordless_message_box_empty_search_term_optional(main):
    QMessageBox.warning(main,
                        main.tr('Empty Search Term'),
                        main.tr(f'''
                            {main.settings_global['styles']['style_dialog']}
                            <body>
                                <div>You haven't specify any search term yet, please enter one in the input box under "<span style="color: #F00; font-weight: bold;">Search Term</span>" first.
                                </div>

                                <div>
                                    Or, you can disable searching altogether by unchecking "<span style="color: #F00; font-weight: bold;">Search Settings</span>", which will then generate all possible results, but it is not recommended to do so since the processing speed might be too slow.
                                </div>
                            </body>
                        '''),
                        QMessageBox.Ok)

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

# Results
def wordless_message_box_no_results_table(main):
    QMessageBox.information(main,
                            main.tr('No Search Results'),
                            main.tr(f'''
                                {main.settings_global['styles']['style_dialog']}
                                <body>
                                    <div>There is nothing to be shown in the table.</div>
                                    <div>You might want to change your search term(s) and/or your settings, and then try again.</div>
                                </body>
                            '''),
                            QMessageBox.Ok)

def wordless_message_box_no_results_plot(main):
    QMessageBox.information(main,
                            main.tr('No Search Results'),
                            main.tr(f'''
                                {main.settings_global['styles']['style_dialog']}
                                <body>
                                    <div>There is nothing to be shown in the figure.</div>
                                    <div>You might want to change your search term(s) and/or your settings, and then try again.</div>
                                </body>
                            '''),
                            QMessageBox.Ok)

# Export
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

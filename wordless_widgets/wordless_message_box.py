#
# Wordless: Message Boxes
#
# Copyright (C) 2018-2019 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_utils import wordless_checking

# Files
def wordless_message_box_error_open_files(main,
                                          files_missing = [],
                                          files_duplicate = [],
                                          files_empty = [],
                                          files_unsupported = [],
                                          files_encoding_error = []):
    message = ''

    if files_missing or files_duplicate or files_empty or files_unsupported or files_encoding_error:
        if files_missing:
            list_files = ''.join([f'<li>{file}</li>' for file in files_missing])

            if len(files_missing) == 1:
                message += main.tr(f'''
                               <p>The following file no longer exists in its original location:</p>
                               <ul>{list_files}</ul>
                           ''')
            else:
                message += main.tr(f'''
                               <p>The following files no longer exists in their original location:</p>
                               <ol>{list_files}</ol>
                           ''')

        if files_duplicate:
            list_files = ''.join([f'<li>{file}</li>' for file in files_duplicate])

            if len(files_duplicate) == 1:
                message += main.tr(f'''
                               <p>The following file has already been opened:</p>
                               <ul>{list_files}</ul>
                           ''')
            else:
                message += main.tr(f'''
                               <p>The following files have already been opened:</p>
                               <ol>{list_files}</ol>
                           ''')

        if files_empty:
            list_files = ''.join([f'<li>{file}</li>' for file in files_empty])

            if len(files_empty) == 1:
                message += main.tr(f'''
                               <p>The following file is empty:</p>
                               <ul>{list_files}</ul>
                           ''')
            else:
                message += main.tr(f'''
                               <p>The following files are empty:</p>
                               <ol>{list_files}</ol>
                           ''')

        if files_unsupported:
            list_files = ''.join([f'<li>{file}</li>' for file in files_unsupported])

            if len(files_unsupported) == 1:
                message += main.tr(f'''
                               <p>Failed to open the following file because the file type is not currently supported:</p>
                               <ul>{list_files}</ul>
                           ''')
            else:
                message += main.tr(f'''
                               <p>Failed to open the following files because the file types are not currently supported:</p>
                               <ol>{list_files}</ol>
                           ''')

        if files_encoding_error:
            list_files = ''.join([f'<li>{file}</li>' for file in files_encoding_error])

            if len(files_encoding_error) == 1:
                message += main.tr(f'''
                               <p>Failed to open the following file due to an encoding error:</p>
                               <ul>{list_files}</ul>
                           ''')
            else:
                message += main.tr(f'''
                               <p>Failed to open the following files due to encoding errors:</p>
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

def wordless_message_box_auto_detection_failed(main,
                                               files_encoding_detection_failed,
                                               files_lang_detection_failed):
    message = ''

    if files_encoding_detection_failed or files_lang_detection_failed:
        if files_encoding_detection_failed:
            list_files = ''.join([f'<li>{file}</li>' for file in files_encoding_detection_failed])

            if len(files_encoding_detection_failed) == 1:
                message += main.tr(f'''
                               <p>Failed to detect the encoding of the following file:</p>
                               <ul>{list_files}</ul>
                           ''')
            else:
                message += main.tr(f'''
                               <p>Failed to detect the encodings of the following files:</p>
                               <ol>{list_files}</ol>
                           ''')

        if files_lang_detection_failed:
            list_files = ''.join([f'<li>{file}</li>' for file in files_lang_detection_failed])

            if len(files_lang_detection_failed) == 1:
                message += main.tr(f'''
                               <p>Failed to detect the language of the following file:</p>
                               <ul>{list_files}</ul>
                           ''')
            else:
                message += main.tr(f'''
                               <p>Failed to detect the languages of the following files:</p>
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
                                <p>There is already a file with the same name that has been loaded into Wordless.</p>
                                <p>Please specify a different file name.</p>
                            </body>
                        '''),
                        QMessageBox.Ok)

def wordless_message_box_duplicate_search_terms(main):
    QMessageBox.warning(main,
                        main.tr('Duplicate Search Terms'),
                        main.tr(f'''
                            {main.settings_global['styles']['style_dialog']}
                            <body>
                                <p>The search term you have entered already exists in the list!</p>
                            </body>
                        '''))

def wordless_message_box_duplicate_tags(main):
    QMessageBox.warning(main,
                        main.tr('Duplicate Tags'),
                        main.tr(f'''
                            {main.settings_global['styles']['style_dialog']}
                            <body>
                                <p>The (pair of) tag you have entered already exists in the table!</p>
                            </body>
                        '''))

def wordless_message_box_duplicate_stop_words(main):
    QMessageBox.warning(main,
                        main.tr('Duplicate Stop Words'),
                        main.tr(f'''
                            {main.settings_global['styles']['style_dialog']}
                            <body>
                                <p>The stop word you have entered already exists in the list!</p>
                            </body>
                        '''))

# Tabs
def wordless_message_box_restore_default_settings(main):
    reply = QMessageBox.question(main,
                                 main.tr('Restore Default Settings'),
                                 main.tr(f'''
                                     {main.settings_global['styles']['style_dialog']}
                                     <body>
                                         <p>Do you really want to reset all settings to defaults?</p>
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
                                <p>There are no files being currently selected!</p>
                                <p>Please check and try again.</p>
                            </body>
                        '''),
                        QMessageBox.Ok)

def wordless_message_box_missing_ref_file(main):
    QMessageBox.warning(main,
                        main.tr('Missing Reference File'),
                        main.tr(f'''
                            {main.settings_global['styles']['style_dialog']}
                            <body>
                                <p>Please open and select your reference file first!</p>
                            </body>
                        '''),
                        QMessageBox.Ok)

def wordless_message_box_missing_observed_files(main):
    QMessageBox.warning(main,
                        main.tr('Missing Observed File(s)'),
                        main.tr(f'''
                            {main.settings_global['styles']['style_dialog']}
                            <body>
                                <p>Please open and select your observed file(s) first!</p>
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
                                <p>Please enter your search term(s) first!</p>
                            </body>
                        '''),
                        QMessageBox.Ok)

def wordless_message_box_no_search_results(main):
    QMessageBox.information(main,
                            main.tr('No Search Results'),
                            main.tr(f'''
                                {main.settings_global['styles']['style_dialog']}
                                <body>
                                    <p>There is nothing that could be found in the table.</p>
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
                                    <p>There is nothing to be shown in the table.</p>
                                    <p>You might want to change your search term(s) and/or your settings, and then try again.</p>
                                </body>
                            '''),
                            QMessageBox.Ok)

def wordless_message_box_no_results_plot(main):
    QMessageBox.information(main,
                            main.tr('No Search Results'),
                            main.tr(f'''
                                {main.settings_global['styles']['style_dialog']}
                                <body>
                                    <p>There is nothing to be shown in the figure.</p>
                                    <p>You might want to change your search term(s) and/or your settings, and then try again.</p>
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
                                    <p>The table has been successfully exported to "{file_path}".</p>
                                </body>
                            '''),
                            QMessageBox.Ok)

def wordless_message_box_export_search_terms(main, file_path):
    QMessageBox.information(main,
                            main.tr('Export Completed'),
                            main.tr(f'''
                                {main.settings_global['styles']['style_dialog']}
                                <body>
                                    <p>The search terms have been successfully exported to "{file_path}".</p>
                                </body>
                            '''),
                            QMessageBox.Ok)

def wordless_message_box_export_stop_words(main, file_path):
    QMessageBox.information(main,
                            main.tr('Export Completed'),
                            main.tr(f'''
                                {main.settings_global['styles']['style_dialog']}
                                <body>
                                    <p>The stop words have been successfully exported to "{file_path}".</p>
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
                                <p>The specified path "{path}" does not exist!</p>
                                <p>Please change your settings and try again.</p>
                            </body>
                        '''),
                        QMessageBox.Ok)

def wordless_message_box_path_not_dir(main, path):
    QMessageBox.warning(main,
                        main.tr('Invalid Path'),
                        main.tr(f'''
                            {main.settings_global['styles']['style_dialog']}
                            <body>
                                <p>The specified path "{path}" should be a directory, not a file!</p>
                                <p>Please change your settings and try again.</p>
                            </body>
                        '''),
                        QMessageBox.Ok)

def wordless_message_box_path_not_exist_confirm(main, path):
    reply = QMessageBox.question(main,
                                 main.tr('Path Not Exist'),
                                 main.tr(f'''
                                     {main.settings_global['styles']['style_dialog']}
                                     <body>
                                         <p>The specified path "{path}" does not exist.</p>
                                         <p>Do you want to create the directory?</p>
                                     </body>
                                 '''),
                                 QMessageBox.Yes | QMessageBox.No,
                                 QMessageBox.No)

    if reply == QMessageBox.Yes:
        wordless_checking.check_dir(path)

    return reply

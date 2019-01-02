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

def wordless_message_box_no_files_selected(main):
    QMessageBox.warning(main,
                        main.tr('No Files Selected'),
                        main.tr(f'''{main.settings_global['styles']['style_dialog']}
                                    <body>
                                        <p>There are no files being currently selected!</p>
                                        <p>Please check and try again.</p>
                                    </body>
                                '''),
                        QMessageBox.Ok)

def wordless_message_box_missing_ref_file(main):
    QMessageBox.warning(main,
                        main.tr('Missing Reference File'),
                        main.tr(f'''{main.settings_global['styles']['style_dialog']}
                                    <body>
                                        <p>Please open and select your reference file first!</p>
                                    </body>
                                '''),
                        QMessageBox.Ok)

def wordless_message_box_missing_observed_files(main):
    QMessageBox.warning(main,
                        main.tr('Missing Observed File(s)'),
                        main.tr(f'''{main.settings_global['styles']['style_dialog']}
                                    <body>
                                        <p>Please open and select your observed file(s) first!</p>
                                    </body>
                                '''),
                        QMessageBox.Ok)

def wordless_message_box_path_not_dir(main, path):
    QMessageBox.warning(main,
                        main.tr('Invalid Path'),
                        main.tr(f'''{main.settings_global['styles']['style_dialog']}
                                    <body>
                                        <p>The specified path "{path}" should be a directory, not a file!</p>
                                        <p>Please change your settings and try again.</p>
                                    </body>
                                '''),
                        QMessageBox.Ok)

def wordless_message_box_path_not_exist(main, path):
    QMessageBox.warning(main,
                        main.tr('Invalid Path'),
                        main.tr(f'''{main.settings_global['styles']['style_dialog']}
                                    <body>
                                        <p>The specified path "{path}" does not exist!</p>
                                        <p>Please change your settings and try again.</p>
                                    </body>
                                '''),
                        QMessageBox.Ok)

def wordless_message_box_path_not_exist_confirm(main, path):
    reply = QMessageBox.question(main,
                                 main.tr('Path Not Exist'),
                                 main.tr(f'''{main.settings_global['styles']['style_dialog']}
                                             <body>
                                                 <p>The specified path "{path}" does not exist.</p>
                                                 <p>Do you want to create the directory?</p>
                                             </body>
                                         '''),
                                 QMessageBox.Yes | QMessageBox.No,
                                 QMessageBox.No)

    return reply

def wordless_message_box_restore_default_settings(main):
    reply = QMessageBox.question(main,
                                 main.tr('Restore Default Settings'),
                                 main.tr(f'''{main.settings_global['styles']['style_dialog']}
                                             <body>
                                                 <p>Do you really want to reset all settings to defaults?</p>
                                             </body>
                                         '''),
                                 QMessageBox.Yes | QMessageBox.No,
                                 QMessageBox.No)

    return reply

def wordless_message_box_empty_file(main, file_path):
    QMessageBox.warning(main,
                        main.tr('Empty File'),
                        main.tr(f'''{main.settings_global['styles']['style_dialog']}
                                    <body>
                                        <p>The specified file "{file_path}" is empty!</p>
                                        <p>Please check and try again.</p>
                                    </body>
                                '''),
                        QMessageBox.Ok)

def wordless_message_box_empty_search_term(main):
    QMessageBox.warning(main,
                        main.tr('Empty Search Term'),
                        main.tr(f'''{main.settings_global['styles']['style_dialog']}
                                    <body>
                                        <p>Please enter your search term(s) first!</p>
                                    </body>
                                '''),
                        QMessageBox.Ok)

def wordless_message_box_no_search_results(main):
    QMessageBox.information(main,
                            main.tr('No Search Results'),
                            main.tr(f'''{main.settings_global['styles']['style_dialog']}
                                        <body>
                                            <p>There is nothing that could be found in the table.</p>
                                        </body>
                                    '''),
                            QMessageBox.Ok)

def wordless_message_box_no_results_table(main):
    QMessageBox.information(main,
                            main.tr('No Search Results'),
                            main.tr(f'''{main.settings_global['styles']['style_dialog']}
                                        <body>
                                            <p>There is nothing to be shown in the table.</p>
                                            <p>You might want to change your search term(s) and/or your settings, and then try again.</p>
                                        </body>
                                    '''),
                            QMessageBox.Ok)

def wordless_message_box_no_results_plot(main):
    QMessageBox.information(main,
                            main.tr('No Search Results'),
                            main.tr(f'''{main.settings_global['styles']['style_dialog']}
                                        <body>
                                            <p>There is nothing to be shown in the figure.</p>
                                            <p>You might want to change your search term(s) and/or your settings, and then try again.</p>
                                        </body>
                                    '''),
                            QMessageBox.Ok)

def wordless_message_box_export_completed_search_terms(main, file_path):
    QMessageBox.information(main,
                            main.tr('Export Completed'),
                            main.tr(f'''{main.settings_global['styles']['style_dialog']}
                                        <body>
                                            <p>The search terms has been successfully exported to "{file_path}".</p>
                                        </body>
                                    '''),
                            QMessageBox.Ok)

def wordless_message_box_export_completed_table(main, file_path):
    QMessageBox.information(main,
                            main.tr('Export Completed'),
                            main.tr(f'''{main.settings_global['styles']['style_dialog']}
                                        <body>
                                            <p>The table has been successfully exported to "{file_path}".</p>
                                        </body>
                                    '''),
                            QMessageBox.Ok)

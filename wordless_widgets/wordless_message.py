#
# Wordless: Messages
#
# Copyright (C) 2018-2019 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

def wordless_message_generate_table_success(main):
	main.status_bar.showMessage(main.tr('The table has been successfully generated.'))

def wordless_message_generate_table_error(main):
	main.status_bar.showMessage(main.tr('Error occured during table generation!'))

def wordless_message_filter_table_done(main):
	main.status_bar.showMessage(main.tr('The results in the table has been successfully filtered.'))

def wordless_message_sort_results(main):
	main.status_bar.showMessage(main.tr('The results in the table has been successfully sorted.'))

def wordless_message_generate_plot_success(main):
	main.status_bar.showMessage(main.tr('The plot has been successfully generated.'))

def wordless_message_generate_plot_error(main):
	main.status_bar.showMessage(main.tr('Error occured during plot generation!'))

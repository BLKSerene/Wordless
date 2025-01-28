# ----------------------------------------------------------------------
# Tests: Checks - Work area
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

from tests import wl_test_init
from wordless.wl_checks import wl_checks_work_area

main = wl_test_init.Wl_Test_Main()

def test_wl_msg_box_missing_search_terms():
    wl_checks_work_area.wl_msg_box_missing_search_terms(main)

def test_wl_msg_box_no_results():
    wl_checks_work_area.wl_msg_box_no_results(main)

def test_wl_status_bar_msg_lang_support_unavailable():
    wl_checks_work_area.wl_status_bar_msg_lang_support_unavailable(main)

def test_wl_status_bar_msg_missing_search_terms():
    wl_checks_work_area.wl_status_bar_msg_missing_search_terms(main)

def test_wl_status_bar_msg_success_download_model():
    wl_checks_work_area.wl_status_bar_msg_success_download_model(main)

def test_wl_status_bar_msg_success_generate_table():
    wl_checks_work_area.wl_status_bar_msg_success_generate_table(main)

def test_wl_status_bar_msg_success_generate_fig():
    wl_checks_work_area.wl_status_bar_msg_success_generate_fig(main)

def test_wl_status_bar_msg_success_exp_table():
    wl_checks_work_area.wl_status_bar_msg_success_exp_table(main)

def test_wl_status_bar_msg_success_no_results():
    wl_checks_work_area.wl_status_bar_msg_success_no_results(main)

def test_wl_status_bar_msg_err_download_model():
    wl_checks_work_area.wl_status_bar_msg_err_download_model(main)

def test_wl_status_bar_msg_err_fatal():
    wl_checks_work_area.wl_status_bar_msg_err_fatal(main)

def test_wl_status_bar_msg_file_access_denied():
    wl_checks_work_area.wl_status_bar_msg_file_access_denied(main)

def test_check_search_terms():
    assert wl_checks_work_area.check_search_terms(main, {
        'multi_search_mode': False,
        'search_term': 'test',
        'search_terms': []
    })
    assert not wl_checks_work_area.check_search_terms(main, {
        'multi_search_mode': False,
        'search_term': '',
        'search_terms': ['test']
    })

    assert wl_checks_work_area.check_search_terms(main, {
        'multi_search_mode': True,
        'search_term': '',
        'search_terms': ['test']
    })
    assert not wl_checks_work_area.check_search_terms(main, {
        'multi_search_mode': True,
        'search_term': 'test',
        'search_terms': []
    })

def test_check_nlp_support():
    file_eng_us = {'selected': True, 'name': 'test', 'lang': 'eng_us', 'tagged': False}
    file_other = {'selected': True, 'name': 'test', 'lang': 'other', 'tagged': False}

    assert wl_checks_work_area.check_nlp_support(
        main,
        nlp_utils = ['pos_taggers'],
        files = [file_eng_us]
    )
    assert wl_checks_work_area.check_nlp_support(
        main,
        nlp_utils = ['lemmatizers'],
        files = [file_eng_us]
    )
    assert not wl_checks_work_area.check_nlp_support(
        main,
        nlp_utils = ['pos_taggers'],
        files = [file_other]
    )
    assert not wl_checks_work_area.check_nlp_support(
        main,
        nlp_utils = ['lemmatizers'],
        files = [file_other]
    )

    main.settings_custom['file_area']['files_open'] = [file_eng_us]
    main.settings_custom['file_area']['files_open_ref'] = [file_other]

    assert wl_checks_work_area.check_nlp_support(main, nlp_utils = ['pos_taggers'])
    assert not wl_checks_work_area.check_nlp_support(main, nlp_utils = ['pos_taggers'], ref = True)

def test_check_results():
    assert wl_checks_work_area.check_results(main, '', 'test')
    assert not wl_checks_work_area.check_results(main, 'test', '')
    assert not wl_checks_work_area.check_results(main, '', '')

def test_check_results_download_model():
    assert wl_checks_work_area.check_results_download_model(main, '', 'test')

def test_check_postprocessing():
    assert wl_checks_work_area.check_postprocessing(main, '')
    assert not wl_checks_work_area.check_postprocessing(main, 'test')

def test_check_err_table():
    wl_checks_work_area.check_err_table(main, '')
    wl_checks_work_area.check_err_table(main, 'test')

def test_check_err_fig():
    wl_checks_work_area.check_err_fig(main, '')
    wl_checks_work_area.check_err_fig(main, 'test')

if __name__ == '__main__':
    test_wl_msg_box_missing_search_terms()
    test_wl_msg_box_no_results()

    test_wl_status_bar_msg_lang_support_unavailable()
    test_wl_status_bar_msg_lang_support_unavailable()
    test_wl_status_bar_msg_missing_search_terms()
    test_wl_status_bar_msg_success_generate_table()
    test_wl_status_bar_msg_success_generate_fig()
    test_wl_status_bar_msg_success_exp_table()
    test_wl_status_bar_msg_success_no_results()
    test_wl_status_bar_msg_err_download_model()
    test_wl_status_bar_msg_err_fatal()
    test_wl_status_bar_msg_file_access_denied()

    test_check_search_terms()
    test_check_nlp_support()
    test_check_results()
    test_check_results_download_model()
    test_check_postprocessing()
    test_check_err_table()
    test_check_err_fig()

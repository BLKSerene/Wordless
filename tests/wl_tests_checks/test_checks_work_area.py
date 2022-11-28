# ----------------------------------------------------------------------
# Wordless: Tests - Checks - Work Area
# Copyright (C) 2018-2022  Ye Lei (叶磊)
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

from tests import wl_test_init
from wordless.wl_checks import wl_checks_work_area

main = wl_test_init.Wl_Test_Main()

def test_check_search_terms():
    assert wl_checks_work_area.check_search_terms(main, {
        'multi_search_mode': False,
        'search_term': 'test',
        'search_terms': []
    })
    assert wl_checks_work_area.check_search_terms(main, {
        'multi_search_mode': True,
        'search_term': '',
        'search_terms': ['test']
    })
    assert not wl_checks_work_area.check_search_terms(main, {
        'multi_search_mode': False,
        'search_term': '',
        'search_terms': ['test']
    }, show_warning = False)

    assert not wl_checks_work_area.check_search_terms(main, {
        'multi_search_mode': True,
        'search_term': 'test',
        'search_terms': []
    }, show_warning = False)

def test_check_nlp_support():
    assert wl_checks_work_area.check_nlp_support(
        main,
        files = [{'lang': 'eng_us'}],
        nlp_utils = ['word_tokenizers']
    )

def test_check_results():
    assert wl_checks_work_area.check_results(main, '', 'test')
    assert not wl_checks_work_area.check_results(main, 'test', '')

if __name__ == '__main__':
    test_check_search_terms()
    test_check_nlp_support()
    test_check_results()

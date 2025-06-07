# ----------------------------------------------------------------------
# Tests: Settings - Tables
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
from wordless.wl_settings import wl_settings_tables

main = wl_test_init.Wl_Test_Main()

def test_wl_settings_tables():
    settings_tables = wl_settings_tables.Wl_Settings_Tables(main)
    settings_tables.load_settings()
    settings_tables.load_settings(defaults = True)
    settings_tables.apply_settings()

def test_wl_settings_tables_profiler():
    settings_tables_profiler = wl_settings_tables.Wl_Settings_Tables_Profiler(main)
    settings_tables_profiler.load_settings()
    settings_tables_profiler.load_settings(defaults = True)
    settings_tables_profiler.apply_settings()

def test_wl_settings_tables_concordancer():
    settings_tables_concordancer = wl_settings_tables.Wl_Settings_Tables_Concordancer(main)
    settings_tables_concordancer.load_settings()
    settings_tables_concordancer.load_settings(defaults = True)
    settings_tables_concordancer.apply_settings()

def test_wl_settings_tables_parallel_concordancer():
    settings_tables_parallel_concordancer = wl_settings_tables.Wl_Settings_Tables_Parallel_Concordancer(main)
    settings_tables_parallel_concordancer.load_settings()
    settings_tables_parallel_concordancer.load_settings(defaults = True)
    settings_tables_parallel_concordancer.apply_settings()

def test_wl_settings_tables_dependency_parser():
    settings_tables_dependency_parser = wl_settings_tables.Wl_Settings_Tables_Dependency_Parser(main)
    settings_tables_dependency_parser.load_settings()
    settings_tables_dependency_parser.load_settings(defaults = True)
    settings_tables_dependency_parser.apply_settings()

def test_wl_settings_tables_wordlist_generator():
    settings_tables_wordlist_generator = wl_settings_tables.Wl_Settings_Tables_Wordlist_Generator(main)
    settings_tables_wordlist_generator.load_settings()
    settings_tables_wordlist_generator.load_settings(defaults = True)
    settings_tables_wordlist_generator.apply_settings()

def test_wl_settings_tables_ngram_generator():
    settings_tables_ngram_generator = wl_settings_tables.Wl_Settings_Tables_Ngram_Generator(main)
    settings_tables_ngram_generator.load_settings()
    settings_tables_ngram_generator.load_settings(defaults = True)
    settings_tables_ngram_generator.apply_settings()

def test_wl_settings_tables_collocation_extractor():
    settings_tables_collocation_extractor = wl_settings_tables.Wl_Settings_Tables_Collocation_Extractor(main)
    settings_tables_collocation_extractor.load_settings()
    settings_tables_collocation_extractor.load_settings(defaults = True)
    settings_tables_collocation_extractor.apply_settings()

def test_wl_settings_tables_colligation_extractor():
    settings_tables_colligation_extractor = wl_settings_tables.Wl_Settings_Tables_Colligation_Extractor(main)
    settings_tables_colligation_extractor.load_settings()
    settings_tables_colligation_extractor.load_settings(defaults = True)
    settings_tables_colligation_extractor.apply_settings()

def test_wl_settings_tables_keyword_extractor():
    settings_tables_keyword_extractor = wl_settings_tables.Wl_Settings_Tables_Keyword_Extractor(main)
    settings_tables_keyword_extractor.load_settings()
    settings_tables_keyword_extractor.load_settings(defaults = True)
    settings_tables_keyword_extractor.apply_settings()

if __name__ == '__main__':
    test_wl_settings_tables()
    test_wl_settings_tables_profiler()
    test_wl_settings_tables_concordancer()
    test_wl_settings_tables_parallel_concordancer()
    test_wl_settings_tables_dependency_parser()
    test_wl_settings_tables_wordlist_generator()
    test_wl_settings_tables_ngram_generator()
    test_wl_settings_tables_collocation_extractor()
    test_wl_settings_tables_colligation_extractor()
    test_wl_settings_tables_keyword_extractor()

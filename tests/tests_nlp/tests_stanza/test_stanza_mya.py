# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Burmese
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

from tests.tests_nlp.tests_stanza import test_stanza

def test_stanza_mya():
    test_stanza.wl_test_stanza(
        lang = 'mya',
        results_sentence_tokenize = ['မြန်မာဘာသာစကား (အင်္ဂလိပ်: Myanmar Language)သည် မြန်မာနိုင်ငံ၏ ရုံးသုံး ဘာသာစကားဖြစ်သည်။', 'ဗမာလူမျိုးနှင့် ဗမာနွယ်ဝင်(ဓနု၊ အင်းသား၊ တောင်ရိုးနှင့် ယော)တို့၏ ဇာတိစကားဖြစ်သည်။', 'ဗမာလူမျိုးတို့သည် တိဘက်-ဗမာနွယ် ဘာသာစကားများ (Tibeto-Burman Languages) ပြောဆိုသည့် လူမျိုးနွယ်စုကြီးမှ အကြီးဆုံးသော လူမျိုးဖြစ်သည်။', 'လူဦးရေ ၃၈သန်းကျော်ခန့်သည် မြန်မာဘာသာစကားကို မိခင်ဘာသာစကား အနေဖြင့် သုံး၍ မြန်မာတိုင်းရင်သားများသည် ဒုတိယဘာသာစကား အနေဖြင့် သုံးသည်။'],
        results_word_tokenize = ['မြန်မာ', 'ဘာသာ', 'စကား', '(', 'အင်္ဂလိပ်', ':', 'Myanmar', 'Language)', 'သည်', 'မြန်မာ', 'နိုင်ငံ', '၏', 'ရုံးသုံး', 'ဘာသာ', 'စကား', 'ဖြစ်', 'သည်', '။']
    )

if __name__ == '__main__':
    test_stanza_mya()

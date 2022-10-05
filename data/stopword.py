# ----------------------------------------------------------------------
# Data: stopword
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
# along with this program.  If not, see <http:#www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

# pylint: disable=pointless-string-statement

num123 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
numFas = ['۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹', '۰']
numKor = ['０', '１', '２', '３', '４', '５', '６', '７', '８', '９']
numMya = ['၀', '၁', '၂', '၃', '၄', '၅', '၆', '၇', '၈', '၉']
numTel = ['౦', '౧', '౨', '౩', '౪', '౫', '౬', '౭', '౮', '౯']

''' Copyright 2016 Liam Doherty

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http:#www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

''' This list is frequency sorted. That means it can be sliced from the bottom
and be less agressive in excluding stopwords '''

afr = ['die', 'het', 'en', 'sy', 'nie', 'was', 'hy', 'te', 'is', 'ek', 'om', 'hulle', 'in', 'my', '\'n', 'vir', 'toe', 'haar', 'van', 'dit', 'op', 'se', 'wat', 'met', 'gaan', 'baie', 'ons', 'jy', 'na', 'maar', 'hom', 'so', 'n', 'huis', 'kan', 'aan', 'dat', 'daar', 'sal', 'jou', 'gesê', 'by', 'kom', 'een', 'ma', 'as', 'son', 'groot', 'begin', 'al']

'''
The MIT License (MIT)

Copyright (c) 2016 Gene Diaz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the 'Software'), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

ara = ['،', 'ّآض', 'آمينَ', 'آه', 'آهاً', 'آي', 'أ', 'أب', 'أجل', 'أجمع', 'أخ', 'أخذ', 'أصبح', 'أضحى', 'أقبل', 'أقل', 'أكثر', 'ألا', 'أم', 'أما', 'أمامك', 'أمامكَ', 'أمسى', 'أمّا', 'أن', 'أنا', 'أنت', 'أنتم', 'أنتما', 'أنتن', 'أنتِ', 'أنشأ', 'أنّى', 'أو', 'أوشك', 'أولئك', 'أولئكم', 'أولاء', 'أولالك', 'أوّهْ', 'أي', 'أيا', 'أين', 'أينما', 'أيّ', 'أَنَّ', 'أََيُّ', 'أُفٍّ', 'إذ', 'إذا', 'إذاً', 'إذما', 'إذن', 'إلى', 'إليكم', 'إليكما', 'إليكنّ', 'إليكَ', 'إلَيْكَ', 'إلّا', 'إمّا', 'إن', 'إنّما', 'إي', 'إياك', 'إياكم', 'إياكما', 'إياكن', 'إيانا', 'إياه', 'إياها', 'إياهم', 'إياهما', 'إياهن', 'إياي', 'إيهٍ', 'إِنَّ', 'ا', 'ابتدأ', 'اثر', 'اجل', 'احد', 'اخرى', 'اخلولق', 'اذا', 'اربعة', 'ارتدّ', 'استحال', 'اطار', 'اعادة', 'اعلنت', 'اف', 'اكثر', 'اكد', 'الألاء', 'الألى', 'الا', 'الاخيرة', 'الان', 'الاول', 'الاولى', 'التى', 'التي', 'الثاني', 'الثانية', 'الذاتي', 'الذى', 'الذي', 'الذين', 'السابق', 'الف', 'اللائي', 'اللاتي', 'اللتان', 'اللتيا', 'اللتين', 'اللذان', 'اللذين', 'اللواتي', 'الماضي', 'المقبل', 'الوقت', 'الى', 'اليوم', 'اما', 'امام', 'امس', 'ان', 'انبرى', 'انقلب', 'انه', 'انها', 'او', 'اول', 'اي', 'ايار', 'ايام', 'ايضا', 'ب', 'بات', 'باسم', 'بان', 'بخٍ', 'برس', 'بسبب', 'بسّ', 'بشكل', 'بضع', 'بطآن', 'بعد', 'بعض', 'بك', 'بكم', 'بكما', 'بكن', 'بل', 'بلى', 'بما', 'بماذا', 'بمن', 'بن', 'بنا', 'به', 'بها', 'بي', 'بيد', 'بين', 'بَسْ', 'بَلْهَ', 'بِئْسَ', 'تانِ', 'تانِك', 'تبدّل', 'تجاه', 'تحوّل', 'تلقاء', 'تلك', 'تلكم', 'تلكما', 'تم', 'تينك', 'تَيْنِ', 'تِه', 'تِي', 'ثلاثة', 'ثم', 'ثمّ', 'ثمّة', 'ثُمَّ', 'جعل', 'جلل', 'جميع', 'جير', 'حار', 'حاشا', 'حاليا', 'حاي', 'حتى', 'حرى', 'حسب', 'حم', 'حوالى', 'حول', 'حيث', 'حيثما', 'حين', 'حيَّ', 'حَبَّذَا', 'حَتَّى', 'حَذارِ', 'خلا', 'خلال', 'دون', 'دونك', 'ذا', 'ذات', 'ذاك', 'ذانك', 'ذانِ', 'ذلك', 'ذلكم', 'ذلكما', 'ذلكن', 'ذو', 'ذوا', 'ذواتا', 'ذواتي', 'ذيت', 'ذينك', 'ذَيْنِ', 'ذِه', 'ذِي', 'راح', 'رجع', 'رويدك', 'ريث', 'رُبَّ', 'زيارة', 'سبحان', 'سرعان', 'سنة', 'سنوات', 'سوف', 'سوى', 'سَاءَ', 'سَاءَمَا', 'شبه', 'شخصا', 'شرع', 'شَتَّانَ', 'صار', 'صباح', 'صفر', 'صهٍ', 'صهْ', 'ضد', 'ضمن', 'طاق', 'طالما', 'طفق', 'طَق', 'ظلّ', 'عاد', 'عام', 'عاما', 'عامة', 'عدا', 'عدة', 'عدد', 'عدم', 'عسى', 'عشر', 'عشرة', 'علق', 'على', 'عليك', 'عليه', 'عليها', 'علًّ', 'عن', 'عند', 'عندما', 'عوض', 'عين', 'عَدَسْ', 'عَمَّا', 'غدا', 'غير', 'ـ', 'ف', 'فان', 'فلان', 'فو', 'فى', 'في', 'فيم', 'فيما', 'فيه', 'فيها', 'قال', 'قام', 'قبل', 'قد', 'قطّ', 'قلما', 'قوة', 'كأنّما', 'كأين', 'كأيّ', 'كأيّن', 'كاد', 'كان', 'كانت', 'كذا', 'كذلك', 'كرب', 'كل', 'كلا', 'كلاهما', 'كلتا', 'كلم', 'كليكما', 'كليهما', 'كلّما', 'كلَّا', 'كم', 'كما', 'كي', 'كيت', 'كيف', 'كيفما', 'كَأَنَّ', 'كِخ', 'لئن', 'لا', 'لات', 'لاسيما', 'لدن', 'لدى', 'لعمر', 'لقاء', 'لك', 'لكم', 'لكما', 'لكن', 'لكنَّما', 'لكي', 'لكيلا', 'للامم', 'لم', 'لما', 'لمّا', 'لن', 'لنا', 'له', 'لها', 'لو', 'لوكالة', 'لولا', 'لوما', 'لي', 'لَسْتَ', 'لَسْتُ', 'لَسْتُم', 'لَسْتُمَا', 'لَسْتُنَّ', 'لَسْتِ', 'لَسْنَ', 'لَعَلَّ', 'لَكِنَّ', 'لَيْتَ', 'لَيْسَ', 'لَيْسَا', 'لَيْسَتَا', 'لَيْسَتْ', 'لَيْسُوا', 'لَِسْنَا', 'ما', 'ماانفك', 'مابرح', 'مادام', 'ماذا', 'مازال', 'مافتئ', 'مايو', 'متى', 'مثل', 'مذ', 'مساء', 'مع', 'معاذ', 'مقابل', 'مكانكم', 'مكانكما', 'مكانكنّ', 'مكانَك', 'مليار', 'مليون', 'مما', 'ممن', 'من', 'منذ', 'منها', 'مه', 'مهما', 'مَنْ', 'مِن', 'نحن', 'نحو', 'نعم', 'نفس', 'نفسه', 'نهاية', 'نَخْ', 'نِعِمّا', 'نِعْمَ', 'ها', 'هاؤم', 'هاكَ', 'هاهنا', 'هبّ', 'هذا', 'هذه', 'هكذا', 'هل', 'هلمَّ', 'هلّا', 'هم', 'هما', 'هن', 'هنا', 'هناك', 'هنالك', 'هو', 'هي', 'هيا', 'هيت', 'هيّا', 'هَؤلاء', 'هَاتانِ', 'هَاتَيْنِ', 'هَاتِه', 'هَاتِي', 'هَجْ', 'هَذا', 'هَذانِ', 'هَذَيْنِ', 'هَذِه', 'هَذِي', 'هَيْهَاتَ', 'و', 'وا', 'واحد', 'واضاف', 'واضافت', 'واكد', 'وان', 'واهاً', 'واوضح', 'وراءَك', 'وفي', 'وقال', 'وقالت', 'وقد', 'وقف', 'وكان', 'وكانت', 'ولا', 'ولم', 'ومن', 'وهو', 'وهي', 'ويكأنّ', 'وَيْ', 'وُشْكَانََ', 'يكون', 'يمكن', 'يوم', 'ّأيّان']

# Copyright (c) 2017 Peter Graham, contributors. Released under the Apache-2.0 license.

hye = ['այդ', 'այլ', 'այն', 'այս', 'դու', 'դուք', 'եմ', 'են', 'ենք', 'ես', 'եք', 'է', 'էի', 'էին', 'էինք', 'էիր', 'էիք', 'էր', 'ըստ', 'թ', 'ի', 'ին', 'իսկ', 'իր', 'կամ', 'համար', 'հետ', 'հետո', 'մենք', 'մեջ', 'մի', 'ն', 'նա', 'նաև', 'նրա', 'նրանք', 'որ', 'որը', 'որոնք', 'որպես', 'ու', 'ում', 'պիտի', 'վրա', 'և']

# Copyright (c) 2017 Peter Graham, contributors. Released under the Apache-2.0 license.

eus = ['al', 'anitz', 'arabera', 'asko', 'baina', 'bat', 'batean', 'batek', 'bati', 'batzuei', 'batzuek', 'batzuetan', 'batzuk', 'bera', 'beraiek', 'berau', 'berauek', 'bere', 'berori', 'beroriek', 'beste', 'bezala', 'da', 'dago', 'dira', 'ditu', 'du', 'dute', 'edo', 'egin', 'ere', 'eta', 'eurak', 'ez', 'gainera', 'gu', 'gutxi', 'guzti', 'haiei', 'haiek', 'haietan', 'hainbeste', 'hala', 'han', 'handik', 'hango', 'hara', 'hari', 'hark', 'hartan', 'hau', 'hauei', 'hauek', 'hauetan', 'hemen', 'hemendik', 'hemengo', 'hi', 'hona', 'honek', 'honela', 'honetan', 'honi', 'hor', 'hori', 'horiei', 'horiek', 'horietan', 'horko', 'horra', 'horrek', 'horrela', 'horretan', 'horri', 'hortik', 'hura', 'izan', 'ni', 'noiz', 'nola', 'non', 'nondik', 'nongo', 'nor', 'nora', 'ze', 'zein', 'zen', 'zenbait', 'zenbat', 'zer', 'zergatik', 'ziren', 'zituen', 'zu', 'zuek', 'zuen', 'zuten']

'''
The MIT License (MIT)

Copyright (c) 2016 Gene Diaz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

ben = ['অতএব', 'অথচ', 'অথবা', 'অনুযায়ী', 'অনেক', 'অনেকে', 'অনেকেই', 'অন্তত', 'অন্য', 'অবধি', 'অবশ্য', 'অর্থাত', 'আই', 'আগামী', 'আগে', 'আগেই', 'আছে', 'আজ', 'আদ্যভাগে', 'আপনার', 'আপনি', 'আবার', 'আমরা', 'আমাকে', 'আমাদের', 'আমার', 'আমি', 'আর', 'আরও', 'ই', 'ইত্যাদি', 'ইহা', 'উচিত', 'উত্তর', 'উনি', 'উপর', 'উপরে', 'এ', 'এঁদের', 'এঁরা', 'এই', 'একই', 'একটি', 'একবার', 'একে', 'এক্', 'এখন', 'এখনও', 'এখানে', 'এখানেই', 'এটা', 'এটাই', 'এটি', 'এত', 'এতটাই', 'এতে', 'এদের', 'এব', 'এবং', 'এবার', 'এমন', 'এমনকী', 'এমনি', 'এর', 'এরা', 'এল', 'এস', 'এসে', 'ঐ', 'ও', 'ওঁদের', 'ওঁর', 'ওঁরা', 'ওই', 'ওকে', 'ওখানে', 'ওদের', 'ওর', 'ওরা', 'কখনও', 'কত', 'কবে', 'কমনে', 'কয়েক', 'কয়েকটি', 'করছে', 'করছেন', 'করতে', 'করবে', 'করবেন', 'করলে', 'করলেন', 'করা', 'করাই', 'করায়', 'করার', 'করি', 'করিতে', 'করিয়া', 'করিয়ে', 'করে', 'করেই', 'করেছিলেন', 'করেছে', 'করেছেন', 'করেন', 'কাউকে', 'কাছ', 'কাছে', 'কাজ', 'কাজে', 'কারও', 'কারণ', 'কি', 'কিংবা', 'কিছু', 'কিছুই', 'কিন্তু', 'কী', 'কে', 'কেউ', 'কেউই', 'কেখা', 'কেন', 'কোটি', 'কোন', 'কোনও', 'কোনো', 'ক্ষেত্রে', 'কয়েক', 'খুব', 'গিয়ে', 'গিয়েছে', 'গিয়ে', 'গুলি', 'গেছে', 'গেল', 'গেলে', 'গোটা', 'চলে', 'চান', 'চায়', 'চার', 'চালু', 'চেয়ে', 'চেষ্টা', 'ছাড়া', 'ছাড়াও', 'ছিল', 'ছিলেন', 'জন', 'জনকে', 'জনের', 'জন্য', 'জন্যওজে', 'জানতে', 'জানা', 'জানানো', 'জানায়', 'জানিয়ে', 'জানিয়েছে', 'জে', 'জ্নজন', 'টি', 'ঠিক', 'তখন', 'তত', 'তথা', 'তবু', 'তবে', 'তা', 'তাঁকে', 'তাঁদের', 'তাঁর', 'তাঁরা', 'তাঁাহারা', 'তাই', 'তাও', 'তাকে', 'তাতে', 'তাদের', 'তার', 'তারপর', 'তারা', 'তারৈ', 'তাহলে', 'তাহা', 'তাহাতে', 'তাহার', 'তিনঐ', 'তিনি', 'তিনিও', 'তুমি', 'তুলে', 'তেমন', 'তো', 'তোমার', 'থাকবে', 'থাকবেন', 'থাকা', 'থাকায়', 'থাকে', 'থাকেন', 'থেকে', 'থেকেই', 'থেকেও', 'দিকে', 'দিতে', 'দিন', 'দিয়ে', 'দিয়েছে', 'দিয়েছেন', 'দিলেন', 'দু', 'দুই', 'দুটি', 'দুটো', 'দেওয়া', 'দেওয়ার', 'দেওয়া', 'দেখতে', 'দেখা', 'দেখে', 'দেন', 'দেয়', 'দ্বারা', 'ধরা', 'ধরে', 'ধামার', 'নতুন', 'নয়', 'না', 'নাই', 'নাকি', 'নাগাদ', 'নানা', 'নিজে', 'নিজেই', 'নিজেদের', 'নিজের', 'নিতে', 'নিয়ে', 'নিয়ে', 'নেই', 'নেওয়া', 'নেওয়ার', 'নেওয়া', 'নয়', 'পক্ষে', 'পর', 'পরে', 'পরেই', 'পরেও', 'পর্যন্ত', 'পাওয়া', 'পাচ', 'পারি', 'পারে', 'পারেন', 'পি', 'পেয়ে', 'পেয়্র্', 'প্রতি', 'প্রথম', 'প্রভৃতি', 'প্রযন্ত', 'প্রাথমিক', 'প্রায়', 'প্রায়', 'ফলে', 'ফিরে', 'ফের', 'বক্তব্য', 'বদলে', 'বন', 'বরং', 'বলতে', 'বলল', 'বললেন', 'বলা', 'বলে', 'বলেছেন', 'বলেন', 'বসে', 'বহু', 'বা', 'বাদে', 'বার', 'বি', 'বিনা', 'বিভিন্ন', 'বিশেষ', 'বিষয়টি', 'বেশ', 'বেশি', 'ব্যবহার', 'ব্যাপারে', 'ভাবে', 'ভাবেই', 'মতো', 'মতোই', 'মধ্যভাগে', 'মধ্যে', 'মধ্যেই', 'মধ্যেও', 'মনে', 'মাত্র', 'মাধ্যমে', 'মোট', 'মোটেই', 'যখন', 'যত', 'যতটা', 'যথেষ্ট', 'যদি', 'যদিও', 'যা', 'যাঁর', 'যাঁরা', 'যাওয়া', 'যাওয়ার', 'যাওয়া', 'যাকে', 'যাচ্ছে', 'যাতে', 'যাদের', 'যান', 'যাবে', 'যায়', 'যার', 'যারা', 'যিনি', 'যে', 'যেখানে', 'যেতে', 'যেন', 'যেমন', 'র', 'রকম', 'রয়েছে', 'রাখা', 'রেখে', 'লক্ষ', 'শুধু', 'শুরু', 'সঙ্গে', 'সঙ্গেও', 'সব', 'সবার', 'সমস্ত', 'সম্প্রতি', 'সহ', 'সহিত', 'সাধারণ', 'সামনে', 'সি', 'সুতরাং', 'সে', 'সেই', 'সেখান', 'সেখানে', 'সেটা', 'সেটাই', 'সেটাও', 'সেটি', 'স্পষ্ট', 'স্বয়ং', 'হইতে', 'হইবে', 'হইয়া', 'হওয়া', 'হওয়ায়', 'হওয়ার', 'হচ্ছে', 'হত', 'হতে', 'হতেই', 'হন', 'হবে', 'হবেন', 'হয়', 'হয়তো', 'হয়নি', 'হয়ে', 'হয়েই', 'হয়েছিল', 'হয়েছে', 'হয়েছেন', 'হল', 'হলে', 'হলেই', 'হলেও', 'হলো', 'হাজার', 'হিসাবে', 'হৈলে', 'হোক', 'হয়']

# Copyright (c) 2017 Peter Graham, contributors. Released under the Apache-2.0 license.

bre = ['a', 'ainda', 'alem', 'ambas', 'ambos', 'antes', 'ao', 'aonde', 'aos', 'apos', 'aquele', 'aqueles', 'as', 'assim', 'com', 'como', 'contra', 'contudo', 'cuja', 'cujas', 'cujo', 'cujos', 'da', 'das', 'de', 'dela', 'dele', 'deles', 'demais', 'depois', 'desde', 'desta', 'deste', 'dispoe', 'dispoem', 'diversa', 'diversas', 'diversos', 'do', 'dos', 'durante', 'e', 'ela', 'elas', 'ele', 'eles', 'em', 'entao', 'entre', 'essa', 'essas', 'esse', 'esses', 'esta', 'estas', 'este', 'estes', 'ha', 'isso', 'isto', 'logo', 'mais', 'mas', 'mediante', 'menos', 'mesma', 'mesmas', 'mesmo', 'mesmos', 'na', 'nao', 'nas', 'nem', 'nesse', 'neste', 'nos', 'o', 'os', 'ou', 'outra', 'outras', 'outro', 'outros', 'pelas', 'pelo', 'pelos', 'perante', 'pois', 'por', 'porque', 'portanto', 'propios', 'proprio', 'quais', 'qual', 'qualquer', 'quando', 'quanto', 'que', 'quem', 'quer', 'se', 'seja', 'sem', 'sendo', 'seu', 'seus', 'sob', 'sobre', 'sua', 'suas', 'tal', 'tambem', 'teu', 'teus', 'toda', 'todas', 'todo', 'todos', 'tua', 'tuas', 'tudo', 'um', 'uma', 'umas', 'uns']

# Copyright (c) 2017 Peter Graham, contributors. Released under the Apache-2.0 license.

bul = ['а', 'автентичен', 'аз', 'ако', 'ала', 'бе', 'без', 'беше', 'би', 'бивш', 'бивша', 'бившо', 'бил', 'била', 'били', 'било', 'благодаря', 'близо', 'бъдат', 'бъде', 'бяха', 'в', 'вас', 'ваш', 'ваша', 'вероятно', 'вече', 'взема', 'ви', 'вие', 'винаги', 'внимава', 'време', 'все', 'всеки', 'всички', 'всичко', 'всяка', 'във', 'въпреки', 'върху', 'г', 'ги', 'главен', 'главна', 'главно', 'глас', 'го', 'година', 'години', 'годишен', 'д', 'да', 'дали', 'два', 'двама', 'двамата', 'две', 'двете', 'ден', 'днес', 'дни', 'до', 'добра', 'добре', 'добро', 'добър', 'докато', 'докога', 'дори', 'досега', 'доста', 'друг', 'друга', 'други', 'е', 'евтин', 'едва', 'един', 'една', 'еднаква', 'еднакви', 'еднакъв', 'едно', 'екип', 'ето', 'живот', 'за', 'забавям', 'зад', 'заедно', 'заради', 'засега', 'заспал', 'затова', 'защо', 'защото', 'и', 'из', 'или', 'им', 'има', 'имат', 'иска', 'й', 'каза', 'как', 'каква', 'какво', 'както', 'какъв', 'като', 'кога', 'когато', 'което', 'които', 'кой', 'който', 'колко', 'която', 'къде', 'където', 'към', 'лесен', 'лесно', 'ли', 'лош', 'м', 'май', 'малко', 'ме', 'между', 'мек', 'мен', 'месец', 'ми', 'много', 'мнозина', 'мога', 'могат', 'може', 'мокър', 'моля', 'момента', 'му', 'н', 'на', 'над', 'назад', 'най', 'направи', 'напред', 'например', 'нас', 'не', 'него', 'нещо', 'нея', 'ни', 'ние', 'никой', 'нито', 'нищо', 'но', 'нов', 'нова', 'нови', 'новина', 'някои', 'някой', 'няколко', 'няма', 'обаче', 'около', 'освен', 'особено', 'от', 'отгоре', 'отново', 'още', 'пак', 'по', 'повече', 'повечето', 'под', 'поне', 'поради', 'после', 'почти', 'прави', 'пред', 'преди', 'през', 'при', 'пък', 'първата', 'първи', 'първо', 'пъти', 'равен', 'равна', 'с', 'са', 'сам', 'само', 'се', 'сега', 'си', 'син', 'скоро', 'след', 'следващ', 'сме', 'смях', 'според', 'сред', 'срещу', 'сте', 'съм', 'със', 'също', 'т', 'т.н.', 'тази', 'така', 'такива', 'такъв', 'там', 'твой', 'те', 'тези', 'ти', 'то', 'това', 'тогава', 'този', 'той', 'толкова', 'точно', 'три', 'трябва', 'тук', 'тъй', 'тя', 'тях', 'у', 'утре', 'харесва', 'хиляди', 'ч', 'часа', 'че', 'често', 'чрез', 'ще', 'щом', 'юмрук', 'я', 'як']

# Copyright (c) 2017 Peter Graham, contributors. Released under the Apache-2.0 license.

cat = ['a', 'abans', 'ací', 'ah', 'així', 'això', 'al', 'aleshores', 'algun', 'alguna', 'algunes', 'alguns', 'alhora', 'allà', 'allí', 'allò', 'als', 'altra', 'altre', 'altres', 'amb', 'ambdues', 'ambdós', 'apa', 'aquell', 'aquella', 'aquelles', 'aquells', 'aquest', 'aquesta', 'aquestes', 'aquests', 'aquí', 'baix', 'cada', 'cadascuna', 'cadascunes', 'cadascuns', 'cadascú', 'com', 'contra', 'd\'un', 'd\'una', 'd\'unes', 'd\'uns', 'dalt', 'de', 'del', 'dels', 'des', 'després', 'dins', 'dintre', 'donat', 'doncs', 'durant', 'e', 'eh', 'el', 'els', 'em', 'en', 'encara', 'ens', 'entre', 'eren', 'es', 'esta', 'estaven', 'esteu', 'està', 'estàvem', 'estàveu', 'et', 'etc', 'ets', 'fins', 'fora', 'gairebé', 'ha', 'han', 'has', 'havia', 'he', 'hem', 'heu', 'hi', 'ho', 'i', 'igual', 'iguals', 'ja', 'l\'hi', 'la', 'les', 'li', 'li\'n', 'llavors', 'm\'he', 'ma', 'mal', 'malgrat', 'mateix', 'mateixa', 'mateixes', 'mateixos', 'me', 'mentre', 'meu', 'meus', 'meva', 'meves', 'molt', 'molta', 'moltes', 'molts', 'mon', 'mons', 'més', 'n\'he', 'n\'hi', 'ne', 'ni', 'no', 'nogensmenys', 'només', 'nosaltres', 'nostra', 'nostre', 'nostres', 'o', 'oh', 'oi', 'on', 'pas', 'pel', 'pels', 'per', 'perquè', 'però', 'poc', 'poca', 'pocs', 'poques', 'potser', 'propi', 'qual', 'quals', 'quan', 'quant', 'que', 'quelcom', 'qui', 'quin', 'quina', 'quines', 'quins', 'què', 's\'ha', 's\'han', 'sa', 'semblant', 'semblants', 'ses', 'seu', 'seus', 'seva', 'seves', 'si', 'sobre', 'sobretot', 'solament', 'sols', 'son', 'sons', 'sota', 'sou', 'sóc', 'són', 't\'ha', 't\'han', 't\'he', 'ta', 'tal', 'també', 'tampoc', 'tan', 'tant', 'tanta', 'tantes', 'teu', 'teus', 'teva', 'teves', 'ton', 'tons', 'tot', 'tota', 'totes', 'tots', 'un', 'una', 'unes', 'uns', 'us', 'va', 'vaig', 'vam', 'van', 'vas', 'veu', 'vosaltres', 'vostra', 'vostre', 'vostres', 'érem', 'éreu', 'és']

'''
Copyright (c) 2011, David Przybilla, Chris Umbel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

zho = ['的', '地', '得', '和', '跟', '与', '及', '向', '并', '等', '更', '已', '含', '做', '我', '你', '他', '她', '们', '某', '该', '各', '每', '这', '那', '哪', '什', '么', '谁', '年', '月', '日', '时', '分', '秒', '几', '多', '来', '在', '就', '又', '很', '呢', '吧', '吗', '了', '嘛', '哇', '儿', '哼', '啊', '嗯', '是', '着', '都', '不', '说', '也', '看', '把', '还', '个', '有', '小', '到', '一', '为', '中', '于', '对', '会', '之', '第', '此', '或', '共', '按', '请']

# Copyright (c) 2017 Peter Graham, contributors. Released under the Apache-2.0 license.

hrv = ['a', 'ako', 'ali', 'bi', 'bih', 'bila', 'bili', 'bilo', 'bio', 'bismo', 'biste', 'biti', 'bumo', 'da', 'do', 'duž', 'ga', 'hoće', 'hoćemo', 'hoćete', 'hoćeš', 'hoću', 'i', 'iako', 'ih', 'ili', 'iz', 'ja', 'je', 'jedna', 'jedne', 'jedno', 'jer', 'jesam', 'jesi', 'jesmo', 'jest', 'jeste', 'jesu', 'jim', 'joj', 'još', 'ju', 'kada', 'kako', 'kao', 'koja', 'koje', 'koji', 'kojima', 'koju', 'kroz', 'li', 'me', 'mene', 'meni', 'mi', 'mimo', 'moj', 'moja', 'moje', 'mu', 'na', 'nad', 'nakon', 'nam', 'nama', 'nas', 'naš', 'naša', 'naše', 'našeg', 'ne', 'nego', 'neka', 'neki', 'nekog', 'neku', 'nema', 'netko', 'neće', 'nećemo', 'nećete', 'nećeš', 'neću', 'nešto', 'ni', 'nije', 'nikoga', 'nikoje', 'nikoju', 'nisam', 'nisi', 'nismo', 'niste', 'nisu', 'njega', 'njegov', 'njegova', 'njegovo', 'njemu', 'njezin', 'njezina', 'njezino', 'njih', 'njihov', 'njihova', 'njihovo', 'njim', 'njima', 'njoj', 'nju', 'no', 'o', 'od', 'odmah', 'on', 'ona', 'oni', 'ono', 'ova', 'pa', 'pak', 'po', 'pod', 'pored', 'prije', 's', 'sa', 'sam', 'samo', 'se', 'sebe', 'sebi', 'si', 'smo', 'ste', 'su', 'sve', 'svi', 'svog', 'svoj', 'svoja', 'svoje', 'svom', 'ta', 'tada', 'taj', 'tako', 'te', 'tebe', 'tebi', 'ti', 'to', 'toj', 'tome', 'tu', 'tvoj', 'tvoja', 'tvoje', 'u', 'uz', 'vam', 'vama', 'vas', 'vaš', 'vaša', 'vaše', 'već', 'vi', 'vrlo', 'za', 'zar', 'će', 'ćemo', 'ćete', 'ćeš', 'ću', 'što']

# Copyright (c) 2017 Peter Graham, contributors. Released under the Apache-2.0 license.

ces = ['a', 'aby', 'ahoj', 'aj', 'ale', 'anebo', 'ani', 'ano', 'asi', 'aspoň', 'atd', 'atp', 'ačkoli', 'až', 'bez', 'beze', 'blízko', 'bohužel', 'brzo', 'bude', 'budem', 'budeme', 'budete', 'budeš', 'budou', 'budu', 'by', 'byl', 'byla', 'byli', 'bylo', 'byly', 'bys', 'být', 'během', 'chce', 'chceme', 'chcete', 'chceš', 'chci', 'chtít', 'chtějí', 'chut\'', 'chuti', 'co', 'což', 'cz', 'daleko', 'další', 'den', 'deset', 'devatenáct', 'devět', 'dnes', 'do', 'dobrý', 'docela', 'dva', 'dvacet', 'dvanáct', 'dvě', 'dál', 'dále', 'děkovat', 'děkujeme', 'děkuji', 'ho', 'hodně', 'i', 'jak', 'jakmile', 'jako', 'jakož', 'jde', 'je', 'jeden', 'jedenáct', 'jedna', 'jedno', 'jednou', 'jedou', 'jeho', 'jehož', 'jej', 'jejich', 'její', 'jelikož', 'jemu', 'jen', 'jenom', 'jestli', 'jestliže', 'ještě', 'jež', 'ji', 'jich', 'jimi', 'jinak', 'jiné', 'již', 'jsem', 'jseš', 'jsi', 'jsme', 'jsou', 'jste', 'já', 'jí', 'jím', 'jíž', 'k', 'kam', 'kde', 'kdo', 'kdy', 'když', 'ke', 'kolik', 'kromě', 'kterou', 'která', 'které', 'který', 'kteří', 'kvůli', 'mají', 'mezi', 'mi', 'mne', 'mnou', 'mně', 'moc', 'mohl', 'mohou', 'moje', 'moji', 'možná', 'musí', 'my', 'má', 'málo', 'mám', 'máme', 'máte', 'máš', 'mé', 'mí', 'mít', 'mě', 'můj', 'může', 'na', 'nad', 'nade', 'napište', 'naproti', 'načež', 'naše', 'naši', 'ne', 'nebo', 'nebyl', 'nebyla', 'nebyli', 'nebyly', 'nedělají', 'nedělá', 'nedělám', 'neděláme', 'neděláte', 'neděláš', 'neg', 'nejsi', 'nejsou', 'nemají', 'nemáme', 'nemáte', 'neměl', 'není', 'nestačí', 'nevadí', 'než', 'nic', 'nich', 'nimi', 'nové', 'nový', 'nula', 'nám', 'námi', 'nás', 'náš', 'ním', 'ně', 'něco', 'nějak', 'někde', 'někdo', 'němu', 'němuž', 'o', 'od', 'ode', 'on', 'ona', 'oni', 'ono', 'ony', 'osm', 'osmnáct', 'pak', 'patnáct', 'po', 'pod', 'podle', 'pokud', 'potom', 'pouze', 'pozdě', 'pořád', 'pravé', 'pro', 'prostě', 'prosím', 'proti', 'proto', 'protože', 'proč', 'první', 'pta', 'pět', 'před', 'přes', 'přese', 'při', 'přičemž', 're', 'rovně', 's', 'se', 'sedm', 'sedmnáct', 'si', 'skoro', 'smí', 'smějí', 'snad', 'spolu', 'sta', 'sto', 'strana', 'sté', 'své', 'svých', 'svým', 'svými', 'ta', 'tady', 'tak', 'takhle', 'taky', 'také', 'takže', 'tam', 'tamhle', 'tamhleto', 'tamto', 'tato', 'tebe', 'tebou', 'ted\'', 'tedy', 'ten', 'tento', 'teto', 'ti', 'tipy', 'tisíc', 'tisíce', 'to', 'tobě', 'tohle', 'toho', 'tohoto', 'tom', 'tomto', 'tomu', 'tomuto', 'toto', 'trošku', 'tu', 'tuto', 'tvoje', 'tvá', 'tvé', 'tvůj', 'ty', 'tyto', 'téma', 'tím', 'tímto', 'tě', 'těm', 'těmu', 'třeba', 'tři', 'třináct', 'u', 'určitě', 'už', 'v', 'vaše', 'vaši', 've', 'vedle', 'večer', 'vlastně', 'vy', 'vám', 'vámi', 'vás', 'váš', 'více', 'však', 'všechno', 'všichni', 'vůbec', 'vždy', 'z', 'za', 'zatímco', 'zač', 'zda', 'zde', 'ze', 'zprávy', 'zpět', 'čau', 'či', 'článku', 'články', 'čtrnáct', 'čtyři', 'šest', 'šestnáct', 'že']

'''
Creative Commons – Attribution / ShareAlike 3.0 license
http:#creativecommons.org/licenses/by-sa/3.0/

List based on frequently used words in subtitles in 2012.

Thanks to
opensubtitles.org
https:#invokeit.wordpress.com/frequency-word-lists/#comment-9707
'''

dan = ['er', 'jeg', 'det', 'du', 'ikke', 'i', 'at', 'en', 'og', 'har', 'vi', 'til', 'på', 'hvad', 'med', 'mig', 'så', 'for', 'de', 'dig', 'der', 'den', 'han', 'kan', 'af', 'vil', 'var', 'her', 'et', 'skal', 'ved', 'nu', 'men', 'om', 'ja', 'som', 'nej', 'min', 'noget', 'ham', 'hun', 'bare', 'kom', 'være', 'din', 'hvor', 'dem', 'ud', 'os', 'hvis', 'må', 'se', 'godt', 'have', 'fra', 'ville', 'okay', 'lige', 'op', 'alle', 'lad', 'hvorfor', 'sig', 'hvordan', 'få', 'kunne', 'eller', 'hvem', 'man', 'bliver', 'havde', 'da', 'ingen', 'efter', 'når', 'alt', 'jo', 'to', 'mit', 'ind', 'hej', 'aldrig', 'lidt', 'nogen', 'over', 'også', 'mand', 'far', 'skulle', 'selv', 'får', 'hans', 'ser', 'vores', 'jer', 'sådan', 'dit', 'kun', 'deres', 'ned', 'mine', 'komme', 'tage', 'denne', 'sige', 'dette', 'blive', 'helt', 'fordi', 'end', 'tag', 'før', 'fik', 'dine']

'''
Copyright (c) 2011, Chris Umbel, Martijn de Boer, Damien van Holten

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

# This dutch wordlist has been parsed from a list created by Damien van Holten
# source: http:#www.damienvanholten.com/blog/dutch-stop-words/

nld = ['aan', 'af', 'al', 'alles', 'als', 'altijd', 'andere', 'ben', 'bij', 'daar', 'dan', 'dat', 'de', 'der', 'deze', 'die', 'dit', 'doch', 'doen', 'door', 'dus', 'een', 'eens', 'en', 'er', 'ge', 'geen', 'geweest', 'haar', 'had', 'heb', 'hebben', 'heeft', 'hem', 'het', 'hier', 'hij', 'hoe', 'hun', 'iemand', 'iets', 'ik', 'in', 'is', 'ja', 'je ', 'kan', 'kon', 'kunnen', 'maar', 'me', 'meer', 'men', 'met', 'mij', 'mijn', 'moet', 'na', 'naar', 'niet', 'niets', 'nog', 'nu', 'of', 'om', 'omdat', 'ons', 'ook', 'op', 'over', 'reeds', 'te', 'tegen', 'toch', 'toen', 'tot', 'u', 'uit', 'uw', 'van', 'veel', 'voor', 'want', 'waren', 'was', 'wat', 'we', 'wel', 'werd', 'wezen', 'wie', 'wij', 'wil', 'worden', 'zal', 'ze', 'zei', 'zelf', 'zich', 'zij', 'zijn', 'zo', 'zonder', 'zou']

'''
Copyright (c) 2011, Chris Umbel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

eng = ['about', 'after', 'all', 'also', 'am', 'an', 'and', 'another', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'between', 'both', 'but', 'by', 'came', 'can', 'come', 'could', 'did', 'do', 'each', 'for', 'from', 'get', 'got', 'has', 'had', 'he', 'have', 'her', 'here', 'him', 'himself', 'his', 'how', 'if', 'in', 'into', 'is', 'it', 'like', 'make', 'many', 'me', 'might', 'more', 'most', 'much', 'must', 'my', 'never', 'now', 'of', 'on', 'only', 'or', 'other', 'our', 'out', 'over', 'said', 'same', 'should', 'since', 'some', 'still', 'such', 'take', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they', 'this', 'those', 'through', 'to', 'too', 'under', 'up', 'very', 'was', 'way', 'we', 'well', 'were', 'what', 'where', 'which', 'while', 'who', 'with', 'would', 'you', 'your', 'a', 'i']

# Copyright (c) 2017 Peter Graham, contributors. Released under the Apache-2.0 license.

epo = ['adiaŭ', 'ajn', 'al', 'ankoraŭ', 'antaŭ', 'aŭ', 'bonan', 'bonvole', 'bonvolu', 'bv', 'ci', 'cia', 'cian', 'cin', 'd-ro', 'da', 'de', 'dek', 'deka', 'do', 'doktor\'', 'doktoro', 'du', 'dua', 'dum', 'eble', 'ekz', 'ekzemple', 'en', 'estas', 'estis', 'estos', 'estu', 'estus', 'eĉ', 'f-no', 'feliĉan', 'for', 'fraŭlino', 'ha', 'havas', 'havis', 'havos', 'havu', 'havus', 'he', 'ho', 'hu', 'ili', 'ilia', 'ilian', 'ilin', 'inter', 'io', 'ion', 'iu', 'iujn', 'iun', 'ja', 'jam', 'je', 'jes', 'k', 'kaj', 'ke', 'kio', 'kion', 'kiu', 'kiujn', 'kiun', 'kvankam', 'kvar', 'kvara', 'kvazaŭ', 'kvin', 'kvina', 'la', 'li', 'lia', 'lian', 'lin', 'malantaŭ', 'male', 'malgraŭ', 'mem', 'mi', 'mia', 'mian', 'min', 'minus', 'naŭ', 'naŭa', 'ne', 'nek', 'nenio', 'nenion', 'neniu', 'neniun', 'nepre', 'ni', 'nia', 'nian', 'nin', 'nu', 'nun', 'nur', 'ok', 'oka', 'oni', 'onia', 'onian', 'onin', 'plej', 'pli', 'plu', 'plus', 'por', 'post', 'preter', 's-no', 's-ro', 'se', 'sed', 'sep', 'sepa', 'ses', 'sesa', 'si', 'sia', 'sian', 'sin', 'sinjor\'', 'sinjorino', 'sinjoro', 'sub', 'super', 'supren', 'sur', 'tamen', 'tio', 'tion', 'tiu', 'tiujn', 'tiun', 'tra', 'tri', 'tria', 'tuj', 'tute', 'unu', 'unua', 've', 'verŝajne', 'vi', 'via', 'vian', 'vin', 'ĉi', 'ĉio', 'ĉion', 'ĉiu', 'ĉiujn', 'ĉiun', 'ĉu', 'ĝi', 'ĝia', 'ĝian', 'ĝin', 'ĝis', 'ĵus', 'ŝi', 'ŝia', 'ŝin']

# Copyright (c) 2017 Peter Graham, contributors. Released under the Apache-2.0 license.

est = ['aga', 'ei', 'et', 'ja', 'jah', 'kas', 'kui', 'kõik', 'ma', 'me', 'mida', 'midagi', 'mind', 'minu', 'mis', 'mu', 'mul', 'mulle', 'nad', 'nii', 'oled', 'olen', 'oli', 'oma', 'on', 'pole', 'sa', 'seda', 'see', 'selle', 'siin', 'siis', 'ta', 'te', 'ära']

'''
The MIT License (MIT)
Copyright (c) 2018 Espen Klem

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

''' This list is frequency sorted. That means it can be sliced from the bottom
and be less agressive in excluding stopwords '''

fin = ['ja', 'on', 'oli', 'hän', 'vuonna', 'myös', 'joka', 'se', 'sekä', 'sen', 'mutta', 'ei', 'ovat', 'hänen', 'n', 'kanssa', 'vuoden', 'jälkeen', 'että', 's', 'tai', 'jonka', 'jossa', 'mukaan', 'kun', 'muun', 'muassa', 'hänet', 'olivat', 'kuitenkin', 'noin', 'vuosina', 'aikana', 'lisäksi', 'kaksi', 'kuin', 'ollut', 'the', 'myöhemmin', 'eli', 'vain', 'teki', 'mm', 'jotka', 'ennen', 'ensimmäinen', 'a', '9', 'jo', 'kuten', 'yksi', 'ensimmäisen', 'vastaan', 'tämän', 'vuodesta', 'sitä', 'voi', 'luvun', 'luvulla', 'of', 'ole', 'kauden', 'osa', 'esimerkiksi', 'jolloin', 'yli', 'de', 'kaudella', 'eri', 'sillä', 'kolme', 'he', 'vuotta']

'''
 Copyright (c) 2014, Ismaël Héry

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in
 all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 THE SOFTWARE.
 '''

fra = ['être', 'avoir', 'faire', 'a', 'au', 'aux', 'avec', 'ce', 'ces', 'dans', 'de', 'des', 'du', 'elle', 'en', 'et', 'eux', 'il', 'je', 'la', 'le', 'leur', 'lui', 'ma', 'mais', 'me', 'même', 'mes', 'moi', 'mon', 'ne', 'nos', 'notre', 'nous', 'on', 'ou', 'où', 'par', 'pas', 'pour', 'qu', 'que', 'qui', 'sa', 'se', 'ses', 'son', 'sur', 'ta', 'te', 'tes', 'toi', 'ton', 'tu', 'un', 'une', 'vos', 'votre', 'vous', 'c', 'd', 'j', 'l', 'à', 'm', 'n', 's', 't', 'y', 'été', 'étée', 'étées', 'étés', 'étant', 'suis', 'es', 'est', 'sommes', 'êtes', 'sont', 'serai', 'seras', 'sera', 'serons', 'serez', 'seront', 'serais', 'serait', 'serions', 'seriez', 'seraient', 'étais', 'était', 'étions', 'étiez', 'étaient', 'fus', 'fut', 'fûmes', 'fûtes', 'furent', 'sois', 'soit', 'soyons', 'soyez', 'soient', 'fusse', 'fusses', 'fût', 'fussions', 'fussiez', 'fussent', 'ayant', 'eu', 'eue', 'eues', 'eus', 'ai', 'as', 'avons', 'avez', 'ont', 'aurai', 'auras', 'aura', 'aurons', 'aurez', 'auront', 'aurais', 'aurait', 'aurions', 'auriez', 'auraient', 'avais', 'avait', 'avions', 'aviez', 'avaient', 'eut', 'eûmes', 'eûtes', 'eurent', 'aie', 'aies', 'ait', 'ayons', 'ayez', 'aient', 'eusse', 'eusses', 'eût', 'eussions', 'eussiez', 'eussent', 'ceci', 'cela', 'cet', 'cette', 'ici', 'ils', 'les', 'leurs', 'quel', 'quels', 'quelle', 'quelles', 'sans', 'soi']

# Copyright (c) 2017 Peter Graham, contributors. Released under the Apache-2.0 license.

glg = ['a', 'alí', 'ao', 'aos', 'aquel', 'aquela', 'aquelas', 'aqueles', 'aquilo', 'aquí', 'as', 'así', 'aínda', 'ben', 'cando', 'che', 'co', 'coa', 'coas', 'comigo', 'con', 'connosco', 'contigo', 'convosco', 'cos', 'cun', 'cunha', 'cunhas', 'cuns', 'da', 'dalgunha', 'dalgunhas', 'dalgún', 'dalgúns', 'das', 'de', 'del', 'dela', 'delas', 'deles', 'desde', 'deste', 'do', 'dos', 'dun', 'dunha', 'dunhas', 'duns', 'e', 'el', 'ela', 'elas', 'eles', 'en', 'era', 'eran', 'esa', 'esas', 'ese', 'eses', 'esta', 'estaba', 'estar', 'este', 'estes', 'estiven', 'estou', 'está', 'están', 'eu', 'facer', 'foi', 'foron', 'fun', 'había', 'hai', 'iso', 'isto', 'la', 'las', 'lle', 'lles', 'lo', 'los', 'mais', 'me', 'meu', 'meus', 'min', 'miña', 'miñas', 'moi', 'na', 'nas', 'neste', 'nin', 'no', 'non', 'nos', 'nosa', 'nosas', 'noso', 'nosos', 'nun', 'nunha', 'nunhas', 'nuns', 'nós', 'o', 'os', 'ou', 'para', 'pero', 'pode', 'pois', 'pola', 'polas', 'polo', 'polos', 'por', 'que', 'se', 'senón', 'ser', 'seu', 'seus', 'sexa', 'sido', 'sobre', 'súa', 'súas', 'tamén', 'tan', 'te', 'ten', 'ter', 'teu', 'teus', 'teñen', 'teño', 'ti', 'tido', 'tiven', 'tiña', 'túa', 'túas', 'un', 'unha', 'unhas', 'uns', 'vos', 'vosa', 'vosas', 'voso', 'vosos', 'vós', 'á', 'é', 'ó', 'ós']

'''
The MIT License (MIT)

Copyright (c) 2016 Gene Diaz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

deu = ['a', 'ab', 'aber', 'ach', 'acht', 'achte', 'achten', 'achter', 'achtes', 'ag', 'alle', 'allein', 'allem', 'allen', 'aller', 'allerdings', 'alles', 'allgemeinen', 'als', 'also', 'am', 'an', 'ander', 'andere', 'anderem', 'anderen', 'anderer', 'anderes', 'anderm', 'andern', 'anderr', 'anders', 'au', 'auch', 'auf', 'aus', 'ausser', 'ausserdem', 'außer', 'außerdem', 'b', 'bald', 'bei', 'beide', 'beiden', 'beim', 'beispiel', 'bekannt', 'bereits', 'besonders', 'besser', 'besten', 'bin', 'bis', 'bisher', 'bist', 'c', 'd', 'd.h', 'da', 'dabei', 'dadurch', 'dafür', 'dagegen', 'daher', 'dahin', 'dahinter', 'damals', 'damit', 'danach', 'daneben', 'dank', 'dann', 'daran', 'darauf', 'daraus', 'darf', 'darfst', 'darin', 'darum', 'darunter', 'darüber', 'das', 'dasein', 'daselbst', 'dass', 'dasselbe', 'davon', 'davor', 'dazu', 'dazwischen', 'daß', 'dein', 'deine', 'deinem', 'deinen', 'deiner', 'deines', 'dem', 'dementsprechend', 'demgegenüber', 'demgemäss', 'demgemäß', 'demselben', 'demzufolge', 'den', 'denen', 'denn', 'denselben', 'der', 'deren', 'derer', 'derjenige', 'derjenigen', 'dermassen', 'dermaßen', 'derselbe', 'derselben', 'des', 'deshalb', 'desselben', 'dessen', 'deswegen', 'dich', 'die', 'diejenige', 'diejenigen', 'dies', 'diese', 'dieselbe', 'dieselben', 'diesem', 'diesen', 'dieser', 'dieses', 'dir', 'doch', 'dort', 'drei', 'drin', 'dritte', 'dritten', 'dritter', 'drittes', 'du', 'durch', 'durchaus', 'durfte', 'durften', 'dürfen', 'dürft', 'e', 'eben', 'ebenso', 'ehrlich', 'ei', 'ei, ', 'eigen', 'eigene', 'eigenen', 'eigener', 'eigenes', 'ein', 'einander', 'eine', 'einem', 'einen', 'einer', 'eines', 'einig', 'einige', 'einigem', 'einigen', 'einiger', 'einiges', 'einmal', 'eins', 'elf', 'en', 'ende', 'endlich', 'entweder', 'er', 'ernst', 'erst', 'erste', 'ersten', 'erster', 'erstes', 'es', 'etwa', 'etwas', 'euch', 'euer', 'eure', 'eurem', 'euren', 'eurer', 'eures', 'f', 'folgende', 'früher', 'fünf', 'fünfte', 'fünften', 'fünfter', 'fünftes', 'für', 'g', 'gab', 'ganz', 'ganze', 'ganzen', 'ganzer', 'ganzes', 'gar', 'gedurft', 'gegen', 'gegenüber', 'gehabt', 'gehen', 'geht', 'gekannt', 'gekonnt', 'gemacht', 'gemocht', 'gemusst', 'genug', 'gerade', 'gern', 'gesagt', 'geschweige', 'gewesen', 'gewollt', 'geworden', 'gibt', 'ging', 'gleich', 'gott', 'gross', 'grosse', 'grossen', 'grosser', 'grosses', 'groß', 'große', 'großen', 'großer', 'großes', 'gut', 'gute', 'guter', 'gutes', 'h', 'hab', 'habe', 'haben', 'habt', 'hast', 'hat', 'hatte', 'hatten', 'hattest', 'hattet', 'heisst', 'her', 'heute', 'hier', 'hin', 'hinter', 'hoch', 'hätte', 'hätten', 'i', 'ich', 'ihm', 'ihn', 'ihnen', 'ihr', 'ihre', 'ihrem', 'ihren', 'ihrer', 'ihres', 'im', 'immer', 'in', 'indem', 'infolgedessen', 'ins', 'irgend', 'ist', 'j', 'ja', 'jahr', 'jahre', 'jahren', 'je', 'jede', 'jedem', 'jeden', 'jeder', 'jedermann', 'jedermanns', 'jedes', 'jedoch', 'jemand', 'jemandem', 'jemanden', 'jene', 'jenem', 'jenen', 'jener', 'jenes', 'jetzt', 'k', 'kam', 'kann', 'kannst', 'kaum', 'kein', 'keine', 'keinem', 'keinen', 'keiner', 'keines', 'kleine', 'kleinen', 'kleiner', 'kleines', 'kommen', 'kommt', 'konnte', 'konnten', 'kurz', 'können', 'könnt', 'könnte', 'l', 'lang', 'lange', 'leicht', 'leide', 'lieber', 'los', 'm', 'machen', 'macht', 'machte', 'mag', 'magst', 'mahn', 'mal', 'man', 'manche', 'manchem', 'manchen', 'mancher', 'manches', 'mann', 'mehr', 'mein', 'meine', 'meinem', 'meinen', 'meiner', 'meines', 'mensch', 'menschen', 'mich', 'mir', 'mit', 'mittel', 'mochte', 'mochten', 'morgen', 'muss', 'musst', 'musste', 'mussten', 'muß', 'mußt', 'möchte', 'mögen', 'möglich', 'mögt', 'müssen', 'müsst', 'müßt', 'n', 'na', 'nach', 'nachdem', 'nahm', 'natürlich', 'neben', 'nein', 'neue', 'neuen', 'neun', 'neunte', 'neunten', 'neunter', 'neuntes', 'nicht', 'nichts', 'nie', 'niemand', 'niemandem', 'niemanden', 'noch', 'nun', 'nur', 'o', 'ob', 'oben', 'oder', 'offen', 'oft', 'ohne', 'ordnung', 'p', 'q', 'r', 'recht', 'rechte', 'rechten', 'rechter', 'rechtes', 'richtig', 'rund', 's', 'sa', 'sache', 'sagt', 'sagte', 'sah', 'satt', 'schlecht', 'schluss', 'schon', 'sechs', 'sechste', 'sechsten', 'sechster', 'sechstes', 'sehr', 'sei', 'seid', 'seien', 'sein', 'seine', 'seinem', 'seinen', 'seiner', 'seines', 'seit', 'seitdem', 'selbst', 'sich', 'sie', 'sieben', 'siebente', 'siebenten', 'siebenter', 'siebentes', 'sind', 'so', 'solang', 'solche', 'solchem', 'solchen', 'solcher', 'solches', 'soll', 'sollen', 'sollst', 'sollt', 'sollte', 'sollten', 'sondern', 'sonst', 'soweit', 'sowie', 'später', 'startseite', 'statt', 'steht', 'suche', 't', 'tag', 'tage', 'tagen', 'tat', 'teil', 'tel', 'tritt', 'trotzdem', 'tun', 'u', 'uhr', 'um', 'und', 'und?', 'uns', 'unse', 'unsem', 'unsen', 'unser', 'unsere', 'unserer', 'unses', 'unter', 'v', 'vergangenen', 'viel', 'viele', 'vielem', 'vielen', 'vielleicht', 'vier', 'vierte', 'vierten', 'vierter', 'viertes', 'vom', 'von', 'vor', 'w', 'wahr?', 'wann', 'war', 'waren', 'warst', 'wart', 'warum', 'was', 'weg', 'wegen', 'weil', 'weit', 'weiter', 'weitere', 'weiteren', 'weiteres', 'welche', 'welchem', 'welchen', 'welcher', 'welches', 'wem', 'wen', 'wenig', 'wenige', 'weniger', 'weniges', 'wenigstens', 'wenn', 'wer', 'werde', 'werden', 'werdet', 'weshalb', 'wessen', 'wie', 'wieder', 'wieso', 'will', 'willst', 'wir', 'wird', 'wirklich', 'wirst', 'wissen', 'wo', 'woher', 'wohin', 'wohl', 'wollen', 'wollt', 'wollte', 'wollten', 'worden', 'wurde', 'wurden', 'während', 'währenddem', 'währenddessen', 'wäre', 'würde', 'würden', 'x', 'y', 'z', 'z.b', 'zehn', 'zehnte', 'zehnten', 'zehnter', 'zehntes', 'zeit', 'zu', 'zuerst', 'zugleich', 'zum', 'zunächst', 'zur', 'zurück', 'zusammen', 'zwanzig', 'zwar', 'zwei', 'zweite', 'zweiten', 'zweiter', 'zweites', 'zwischen', 'zwölf', 'über', 'überhaupt', 'übrigens']

# Copyright (c) 2017 Peter Graham, contributors. Released under the Apache-2.0 license.

ell = ['αλλα', 'αν', 'αντι', 'απο', 'αυτα', 'αυτεσ', 'αυτη', 'αυτο', 'αυτοι', 'αυτοσ', 'αυτουσ', 'αυτων', 'για', 'δε', 'δεν', 'εαν', 'ειμαι', 'ειμαστε', 'ειναι', 'εισαι', 'ειστε', 'εκεινα', 'εκεινεσ', 'εκεινη', 'εκεινο', 'εκεινοι', 'εκεινοσ', 'εκεινουσ', 'εκεινων', 'ενω', 'επι', 'η', 'θα', 'ισωσ', 'κ', 'και', 'κατα', 'κι', 'μα', 'με', 'μετα', 'μη', 'μην', 'να', 'ο', 'οι', 'ομωσ', 'οπωσ', 'οσο', 'οτι', 'παρα', 'ποια', 'ποιεσ', 'ποιο', 'ποιοι', 'ποιοσ', 'ποιουσ', 'ποιων', 'που', 'προσ', 'πωσ', 'σε', 'στη', 'στην', 'στο', 'στον', 'τα', 'την', 'τησ', 'το', 'τον', 'τοτε', 'του', 'των', 'ωσ']

''' MIT License

Copyright (c) 2020 Stopwords ISO

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the 'Software'), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. '''

guj = ['અંગે', 'અંદર', 'અથવા', 'અને', 'અમને', 'અમારું', 'અમે', 'અહીં', 'આ', 'આગળ', 'આથી', 'આનું', 'આને', 'આપણને', 'આપણું', 'આપણે', 'આપી', 'આર', 'આવી', 'આવે', 'ઉપર', 'ઉભા', 'ઊંચે', 'ઊભું', 'એ', 'એક', 'એન', 'એના', 'એનાં', 'એની', 'એનું', 'એને', 'એનો', 'એમ', 'એવા', 'એવાં', 'એવી', 'એવું', 'એવો', 'ઓછું', 'કંઈક', 'કઈ', 'કયું', 'કયો', 'કરતાં', 'કરવું', 'કરી', 'કરીએ', 'કરું', 'કરે', 'કરેલું', 'કર્યા', 'કર્યાં', 'કર્યું', 'કર્યો', 'કાંઈ', 'કે', 'કેટલું', 'કેમ', 'કેવી', 'કેવું', 'કોઈ', 'કોઈક', 'કોણ', 'કોણે', 'કોને', 'ક્યાં', 'ક્યારે', 'ખૂબ', 'ગઈ', 'ગયા', 'ગયાં', 'ગયું', 'ગયો', 'ઘણું', 'છ', 'છતાં', 'છીએ', 'છું', 'છે', 'છેક', 'છો', 'જ', 'જાય', 'જી', 'જે', 'જેટલું', 'જેને', 'જેમ', 'જેવી', 'જેવું', 'જેવો', 'જો', 'જોઈએ', 'જ્યાં', 'જ્યારે', 'ઝાઝું', 'તને', 'તમને', 'તમારું', 'તમે', 'તા', 'તારાથી', 'તારામાં', 'તારું', 'તું', 'તે', 'તેં', 'તેઓ', 'તેણે', 'તેથી', 'તેના', 'તેની', 'તેનું', 'તેને', 'તેમ', 'તેમનું', 'તેમને', 'તેવી', 'તેવું', 'તો', 'ત્યાં', 'ત્યારે', 'થઇ', 'થઈ', 'થઈએ', 'થતા', 'થતાં', 'થતી', 'થતું', 'થતો', 'થયા', 'થયાં', 'થયું', 'થયેલું', 'થયો', 'થવું', 'થાઉં', 'થાઓ', 'થાય', 'થી', 'થોડું', 'દરેક', 'ન', 'નં', 'નં.', 'નથી', 'નહિ', 'નહી', 'નહીં', 'ના', 'ની', 'નીચે', 'નું', 'ને', 'નો', 'પછી', 'પણ', 'પર', 'પરંતુ', 'પહેલાં', 'પાછળ', 'પાસે', 'પોતાનું', 'પ્રત્યેક', 'ફક્ત', 'ફરી', 'ફરીથી', 'બંને', 'બધા', 'બધું', 'બની', 'બહાર', 'બહુ', 'બાદ', 'બે', 'મને', 'મા', 'માં', 'માટે', 'માત્ર', 'મારું', 'મી', 'મૂકવું', 'મૂકી', 'મૂક્યા', 'મૂક્યાં', 'મૂક્યું', 'મેં', 'રહી', 'રહે', 'રહેવું', 'રહ્યા', 'રહ્યાં', 'રહ્યો', 'રીતે', 'રૂ.', 'રૂા', 'લેતા', 'લેતું', 'લેવા', 'વગેરે', 'વધુ', 'શકે', 'શા', 'શું', 'સરખું', 'સામે', 'સુધી', 'હતા', 'હતાં', 'હતી', 'હતું', 'હવે', 'હશે', 'હશો', 'હા', 'હું', 'હો', 'હોઈ', 'હોઈશ', 'હોઈશું', 'હોય', 'હોવા']

''' Copyright 2016 Liam Doherty

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http:#www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

''' This list is frequency sorted. That means it can be sliced from the bottom
and be less agressive in excluding stopwords '''

hau = ['ta', 'da', 'ya', 'sai', 'ba', 'yi', 'na', 'kuma', 'ma', 'ji', 'cikin', 'in', 'ni', 'wata', 'wani', 'ce', 'tana', 'don', 'za', 'sun', 'amma', 'ga', 'ina', 'ne', 'tselane', 'mai', 'suka', 'wannan', 'a', 'ko', 'lokacin', 'su', 'take', 'kaka', 'shi', 'yake', 'yana', 'mulongo', 'mata', 'ka', 'ban', 'ita', 'tafi', 'shanshani', 'kai', 'daɗi', 'mi', 'ƙato', 'fara', 'rana']

'''
The MIT License (MIT)
Guy Saar - Stop words list
'''
heb = ['אבל', 'או', 'אולי', 'אותה', 'אותו', 'אותי', 'אותך', 'אותם', 'אותן', 'אותנו', 'אז', 'אחר', 'אחרות', 'אחרי', 'אחריכן', 'אחרים', 'אחרת', 'אי', 'איזה', 'איך', 'אין', 'איפה', 'איתה', 'איתו', 'איתי', 'איתך', 'איתכם', 'איתכן', 'איתם', 'איתן', 'איתנו', 'אך', 'אל', 'אלה', 'אלו', 'אם', 'אנחנו', 'אני', 'אס', 'אף', 'אצל', 'אשר', 'את', 'אתה', 'אתכם', 'אתכן', 'אתם', 'אתן', 'באיזומידה', 'באמצע', 'באמצעות', 'בגלל', 'בין', 'בלי', 'במידה', 'במקוםשבו', 'ברם', 'בשביל', 'בשעהש', 'בתוך', 'גם', 'דרך', 'הוא', 'היא', 'היה', 'היכן', 'היתה', 'היתי', 'הם', 'הן', 'הנה', 'הסיבהשבגללה', 'הרי', 'ואילו', 'ואת', 'זאת', 'זה', 'זות', 'יהיה', 'יוכל', 'יוכלו', 'יותרמדי', 'יכול', 'יכולה', 'יכולות', 'יכולים', 'יכל', 'יכלה', 'יכלו', 'יש', 'כאן', 'כאשר', 'כולם', 'כולן', 'כזה', 'כי', 'כיצד', 'כך', 'ככה', 'כל', 'כלל', 'כמו', 'כן', 'כפי', 'כש', 'לא', 'לאו', 'לאיזותכלית', 'לאן', 'לבין', 'לה', 'להיות', 'להם', 'להן', 'לו', 'לי', 'לכם', 'לכן', 'למה', 'למטה', 'למעלה', 'למקוםשבו', 'למרות', 'לנו', 'לעבר', 'לעיכן', 'לפיכך', 'לפני', 'מאד', 'מאחורי', 'מאיזוסיבה', 'מאין', 'מאיפה', 'מבלי', 'מבעד', 'מדוע', 'מה', 'מהיכן', 'מול', 'מחוץ', 'מי', 'מכאן', 'מכיוון', 'מלבד', 'מן', 'מנין', 'מסוגל', 'מעט', 'מעטים', 'מעל', 'מצד', 'מקוםבו', 'מתחת', 'מתי', 'נגד', 'נגר', 'נו', 'עד', 'עז', 'על', 'עלי', 'עליה', 'עליהם', 'עליהן', 'עליו', 'עליך', 'עליכם', 'עלינו', 'עם', 'עצמה', 'עצמהם', 'עצמהן', 'עצמו', 'עצמי', 'עצמם', 'עצמן', 'עצמנו', 'פה', 'רק', 'שוב', 'של', 'שלה', 'שלהם', 'שלהן', 'שלו', 'שלי', 'שלך', 'שלכה', 'שלכם', 'שלכן', 'שלנו', 'שם', 'תהיה', 'תחת']

'''
The MIT License (MIT)

Copyright (c) 2016 Gene Diaz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Originates from: https:#github.com/stopwords-iso/stopwords-hi/
'''

hin = ['अंदर', 'अत', 'अदि', 'अप', 'अपना', 'अपनि', 'अपनी', 'अपने', 'अभि', 'अभी', 'आदि', 'आप', 'इंहिं', 'इंहें', 'इंहों', 'इतयादि', 'इत्यादि', 'इन', 'इनका', 'इन्हीं', 'इन्हें', 'इन्हों', 'इस', 'इसका', 'इसकि', 'इसकी', 'इसके', 'इसमें', 'इसि', 'इसी', 'इसे', 'उंहिं', 'उंहें', 'उंहों', 'उन', 'उनका', 'उनकि', 'उनकी', 'उनके', 'उनको', 'उन्हीं', 'उन्हें', 'उन्हों', 'उस', 'उसके', 'उसि', 'उसी', 'उसे', 'एक', 'एवं', 'एस', 'एसे', 'ऐसे', 'ओर', 'और', 'कइ', 'कई', 'कर', 'करता', 'करते', 'करना', 'करने', 'करें', 'कहते', 'कहा', 'का', 'काफि', 'काफ़ी', 'कि', 'किंहें', 'किंहों', 'कितना', 'किन्हें', 'किन्हों', 'किया', 'किर', 'किस', 'किसि', 'किसी', 'किसे', 'की', 'कुछ', 'कुल', 'के', 'को', 'कोइ', 'कोई', 'कोन', 'कोनसा', 'कौन', 'कौनसा', 'गया', 'घर', 'जब', 'जहाँ', 'जहां', 'जा', 'जिंहें', 'जिंहों', 'जितना', 'जिधर', 'जिन', 'जिन्हें', 'जिन्हों', 'जिस', 'जिसे', 'जीधर', 'जेसा', 'जेसे', 'जैसा', 'जैसे', 'जो', 'तक', 'तब', 'तरह', 'तिंहें', 'तिंहों', 'तिन', 'तिन्हें', 'तिन्हों', 'तिस', 'तिसे', 'तो', 'था', 'थि', 'थी', 'थे', 'दबारा', 'दवारा', 'दिया', 'दुसरा', 'दुसरे', 'दूसरे', 'दो', 'द्वारा', 'न', 'नहिं', 'नहीं', 'ना', 'निचे', 'निहायत', 'नीचे', 'ने', 'पर', 'पहले', 'पुरा', 'पूरा', 'पे', 'फिर', 'बनि', 'बनी', 'बहि', 'बही', 'बहुत', 'बाद', 'बाला', 'बिलकुल', 'भि', 'भितर', 'भी', 'भीतर', 'मगर', 'मानो', 'मे', 'में', 'यदि', 'यह', 'यहाँ', 'यहां', 'यहि', 'यही', 'या', 'यिह', 'ये', 'रखें', 'रवासा', 'रहा', 'रहे', 'ऱ्वासा', 'लिए', 'लिये', 'लेकिन', 'व', 'वगेरह', 'वरग', 'वर्ग', 'वह', 'वहाँ', 'वहां', 'वहिं', 'वहीं', 'वाले', 'वुह', 'वे', 'वग़ैरह', 'संग', 'सकता', 'सकते', 'सबसे', 'सभि', 'सभी', 'साथ', 'साबुत', 'साभ', 'सारा', 'से', 'सो', 'हि', 'ही', 'हुअ', 'हुआ', 'हुइ', 'हुई', 'हुए', 'हे', 'हें', 'है', 'हैं', 'हो', 'होता', 'होति', 'होती', 'होते', 'होना', 'होने']

# Copyright (c) 2017 Peter Graham, contributors. Released under the Apache-2.0 license.

gle = ['a', 'ach', 'ag', 'agus', 'an', 'aon', 'ar', 'arna', 'as', 'b\'', 'ba', 'beirt', 'bhúr', 'caoga', 'ceathair', 'ceathrar', 'chomh', 'chtó', 'chuig', 'chun', 'cois', 'céad', 'cúig', 'cúigear', 'd\'', 'daichead', 'dar', 'de', 'deich', 'deichniúr', 'den', 'dhá', 'do', 'don', 'dtí', 'dá', 'dár', 'dó', 'faoi', 'faoin', 'faoina', 'faoinár', 'fara', 'fiche', 'gach', 'gan', 'go', 'gur', 'haon', 'hocht', 'i', 'iad', 'idir', 'in', 'ina', 'ins', 'inár', 'is', 'le', 'leis', 'lena', 'lenár', 'm\'', 'mar', 'mo', 'mé', 'na', 'nach', 'naoi', 'naonúr', 'ná', 'ní', 'níor', 'nó', 'nócha', 'ocht', 'ochtar', 'os', 'roimh', 'sa', 'seacht', 'seachtar', 'seachtó', 'seasca', 'seisear', 'siad', 'sibh', 'sinn', 'sna', 'sé', 'sí', 'tar', 'thar', 'thú', 'triúr', 'trí', 'trína', 'trínár', 'tríocha', 'tú', 'um', 'ár', 'é', 'éis', 'í', 'ó', 'ón', 'óna', 'ónár']

# Copyright (c) 2017 Peter Graham, contributors. Released under the Apache-2.0 license.

hun = ['a', 'abba', 'abban', 'abból', 'addig', 'ahhoz', 'ahogy', 'ahol', 'aki', 'akik', 'akkor', 'akár', 'alapján', 'alatt', 'alatta', 'alattad', 'alattam', 'alattatok', 'alattuk', 'alattunk', 'alá', 'alád', 'alájuk', 'alám', 'alánk', 'alátok', 'alól', 'alóla', 'alólad', 'alólam', 'alólatok', 'alóluk', 'alólunk', 'amely', 'amelybol', 'amelyek', 'amelyekben', 'amelyeket', 'amelyet', 'amelyik', 'amelynek', 'ami', 'amikor', 'amit', 'amolyan', 'amott', 'amíg', 'annak', 'annál', 'arra', 'arról', 'attól', 'az', 'aznap', 'azok', 'azokat', 'azokba', 'azokban', 'azokból', 'azokhoz', 'azokig', 'azokkal', 'azokká', 'azoknak', 'azoknál', 'azokon', 'azokra', 'azokról', 'azoktól', 'azokért', 'azon', 'azonban', 'azonnal', 'azt', 'aztán', 'azután', 'azzal', 'azzá', 'azért', 'bal', 'balra', 'ban', 'be', 'belé', 'beléd', 'beléjük', 'belém', 'belénk', 'belétek', 'belül', 'belőle', 'belőled', 'belőlem', 'belőletek', 'belőlük', 'belőlünk', 'ben', 'benne', 'benned', 'bennem', 'bennetek', 'bennük', 'bennünk', 'bár', 'bárcsak', 'bármilyen', 'búcsú', 'cikk', 'cikkek', 'cikkeket', 'csak', 'csakhogy', 'csupán', 'de', 'dehogy', 'e', 'ebbe', 'ebben', 'ebből', 'eddig', 'egy', 'egyebek', 'egyebet', 'egyedül', 'egyelőre', 'egyes', 'egyet', 'egyetlen', 'egyik', 'egymás', 'egyre', 'egyszerre', 'egyéb', 'együtt', 'egész', 'egészen', 'ehhez', 'ekkor', 'el', 'eleinte', 'ellen', 'ellenes', 'elleni', 'ellenére', 'elmondta', 'első', 'elsők', 'elsősorban', 'elsőt', 'elé', 'eléd', 'elég', 'eléjük', 'elém', 'elénk', 'elétek', 'elő', 'előbb', 'elől', 'előle', 'előled', 'előlem', 'előletek', 'előlük', 'előlünk', 'először', 'előtt', 'előtte', 'előtted', 'előttem', 'előttetek', 'előttük', 'előttünk', 'előző', 'emilyen', 'engem', 'ennek', 'ennyi', 'ennél', 'enyém', 'erre', 'erről', 'esetben', 'ettől', 'ez', 'ezek', 'ezekbe', 'ezekben', 'ezekből', 'ezeken', 'ezeket', 'ezekhez', 'ezekig', 'ezekkel', 'ezekké', 'ezeknek', 'ezeknél', 'ezekre', 'ezekről', 'ezektől', 'ezekért', 'ezen', 'ezentúl', 'ezer', 'ezret', 'ezt', 'ezután', 'ezzel', 'ezzé', 'ezért', 'fel', 'fele', 'felek', 'felet', 'felett', 'felé', 'fent', 'fenti', 'fél', 'fölé', 'gyakran', 'ha', 'halló', 'hamar', 'hanem', 'harmadik', 'harmadikat', 'harminc', 'hat', 'hatodik', 'hatodikat', 'hatot', 'hatvan', 'helyett', 'hetedik', 'hetediket', 'hetet', 'hetven', 'hirtelen', 'hiszen', 'hiába', 'hogy', 'hogyan', 'hol', 'holnap', 'holnapot', 'honnan', 'hova', 'hozzá', 'hozzád', 'hozzájuk', 'hozzám', 'hozzánk', 'hozzátok', 'hurrá', 'huszadik', 'hány', 'hányszor', 'hármat', 'három', 'hát', 'hátha', 'hátulsó', 'hét', 'húsz', 'ide', 'ide-оda', 'idén', 'igazán', 'igen', 'ill', 'illetve', 'ilyen', 'ilyenkor', 'immár', 'inkább', 'is', 'ismét', 'ison', 'itt', 'jelenleg', 'jobban', 'jobbra', 'jó', 'jól', 'jólesik', 'jóval', 'jövőre', 'kell', 'kellene', 'kellett', 'kelljen', 'keressünk', 'keresztül', 'ketten', 'kettő', 'kettőt', 'kevés', 'ki', 'kiben', 'kiből', 'kicsit', 'kicsoda', 'kihez', 'kik', 'kikbe', 'kikben', 'kikből', 'kiken', 'kiket', 'kikhez', 'kikkel', 'kikké', 'kiknek', 'kiknél', 'kikre', 'kikről', 'kiktől', 'kikért', 'kilenc', 'kilencedik', 'kilencediket', 'kilencet', 'kilencven', 'kin', 'kinek', 'kinél', 'kire', 'kiről', 'kit', 'kitől', 'kivel', 'kivé', 'kié', 'kiért', 'korábban', 'képest', 'kérem', 'kérlek', 'kész', 'késő', 'később', 'későn', 'két', 'kétszer', 'kívül', 'körül', 'köszönhetően', 'köszönöm', 'közben', 'közel', 'közepesen', 'közepén', 'közé', 'között', 'közül', 'külön', 'különben', 'különböző', 'különbözőbb', 'különbözőek', 'lassan', 'le', 'legalább', 'legyen', 'lehet', 'lehetetlen', 'lehetett', 'lehetőleg', 'lehetőség', 'lenne', 'lenni', 'lennék', 'lennének', 'lesz', 'leszek', 'lesznek', 'leszünk', 'lett', 'lettek', 'lettem', 'lettünk', 'lévő', 'ma', 'maga', 'magad', 'magam', 'magatokat', 'magukat', 'magunkat', 'magát', 'mai', 'majd', 'majdnem', 'manapság', 'meg', 'megcsinál', 'megcsinálnak', 'megint', 'megvan', 'mellett', 'mellette', 'melletted', 'mellettem', 'mellettetek', 'mellettük', 'mellettünk', 'mellé', 'melléd', 'melléjük', 'mellém', 'mellénk', 'mellétek', 'mellől', 'mellőle', 'mellőled', 'mellőlem', 'mellőletek', 'mellőlük', 'mellőlünk', 'mely', 'melyek', 'melyik', 'mennyi', 'mert', 'mi', 'miatt', 'miatta', 'miattad', 'miattam', 'miattatok', 'miattuk', 'miattunk', 'mibe', 'miben', 'miből', 'mihez', 'mik', 'mikbe', 'mikben', 'mikből', 'miken', 'miket', 'mikhez', 'mikkel', 'mikké', 'miknek', 'miknél', 'mikor', 'mikre', 'mikről', 'miktől', 'mikért', 'milyen', 'min', 'mind', 'mindegyik', 'mindegyiket', 'minden', 'mindenesetre', 'mindenki', 'mindent', 'mindenütt', 'mindig', 'mindketten', 'minek', 'minket', 'mint', 'mintha', 'minél', 'mire', 'miről', 'mit', 'mitől', 'mivel', 'mivé', 'miért', 'mondta', 'most', 'mostanáig', 'már', 'más', 'másik', 'másikat', 'másnap', 'második', 'másodszor', 'mások', 'másokat', 'mást', 'még', 'mégis', 'míg', 'mögé', 'mögéd', 'mögéjük', 'mögém', 'mögénk', 'mögétek', 'mögött', 'mögötte', 'mögötted', 'mögöttem', 'mögöttetek', 'mögöttük', 'mögöttünk', 'mögül', 'mögüle', 'mögüled', 'mögülem', 'mögületek', 'mögülük', 'mögülünk', 'múltkor', 'múlva', 'na', 'nagy', 'nagyobb', 'nagyon', 'naponta', 'napot', 'ne', 'negyedik', 'negyediket', 'negyven', 'neked', 'nekem', 'neki', 'nekik', 'nektek', 'nekünk', 'nem', 'nemcsak', 'nemrég', 'nincs', 'nyolc', 'nyolcadik', 'nyolcadikat', 'nyolcat', 'nyolcvan', 'nála', 'nálad', 'nálam', 'nálatok', 'náluk', 'nálunk', 'négy', 'négyet', 'néha', 'néhány', 'nélkül', 'o', 'oda', 'ok', 'olyan', 'onnan', 'ott', 'pedig', 'persze', 'pár', 'például', 'rajta', 'rajtad', 'rajtam', 'rajtatok', 'rajtuk', 'rajtunk', 'rendben', 'rosszul', 'rá', 'rád', 'rájuk', 'rám', 'ránk', 'rátok', 'régen', 'régóta', 'részére', 'róla', 'rólad', 'rólam', 'rólatok', 'róluk', 'rólunk', 'rögtön', 's', 'saját', 'se', 'sem', 'semmi', 'semmilyen', 'semmiség', 'senki', 'soha', 'sok', 'sokan', 'sokat', 'sokkal', 'sokszor', 'sokáig', 'során', 'stb.', 'szemben', 'szerbusz', 'szerint', 'szerinte', 'szerinted', 'szerintem', 'szerintetek', 'szerintük', 'szerintünk', 'szervusz', 'szinte', 'számára', 'száz', 'századik', 'százat', 'szépen', 'szét', 'szíves', 'szívesen', 'szíveskedjék', 'sőt', 'talán', 'tavaly', 'te', 'tegnap', 'tegnapelőtt', 'tehát', 'tele', 'teljes', 'tessék', 'ti', 'tied', 'titeket', 'tizedik', 'tizediket', 'tizenegy', 'tizenegyedik', 'tizenhat', 'tizenhárom', 'tizenhét', 'tizenkettedik', 'tizenkettő', 'tizenkilenc', 'tizenkét', 'tizennyolc', 'tizennégy', 'tizenöt', 'tizet', 'tovább', 'további', 'továbbá', 'távol', 'téged', 'tényleg', 'tíz', 'több', 'többi', 'többször', 'túl', 'tőle', 'tőled', 'tőlem', 'tőletek', 'tőlük', 'tőlünk', 'ugyanakkor', 'ugyanez', 'ugyanis', 'ugye', 'urak', 'uram', 'urat', 'utoljára', 'utolsó', 'után', 'utána', 'vagy', 'vagyis', 'vagyok', 'vagytok', 'vagyunk', 'vajon', 'valahol', 'valaki', 'valakit', 'valamelyik', 'valami', 'valamint', 'való', 'van', 'vannak', 'vele', 'veled', 'velem', 'veletek', 'velük', 'velünk', 'vissza', 'viszlát', 'viszont', 'viszontlátásra', 'volna', 'volnának', 'volnék', 'volt', 'voltak', 'voltam', 'voltunk', 'végre', 'végén', 'végül', 'által', 'általában', 'ám', 'át', 'éljen', 'én', 'éppen', 'érte', 'érted', 'értem', 'értetek', 'értük', 'értünk', 'és', 'év', 'évben', 'éve', 'évek', 'éves', 'évi', 'évvel', 'így', 'óta', 'ön', 'önbe', 'önben', 'önből', 'önhöz', 'önnek', 'önnel', 'önnél', 'önre', 'önről', 'önt', 'öntől', 'önért', 'önök', 'önökbe', 'önökben', 'önökből', 'önöket', 'önökhöz', 'önökkel', 'önöknek', 'önöknél', 'önökre', 'önökről', 'önöktől', 'önökért', 'önökön', 'önön', 'össze', 'öt', 'ötven', 'ötödik', 'ötödiket', 'ötöt', 'úgy', 'úgyis', 'úgynevezett', 'új', 'újabb', 'újra', 'úr', 'ő', 'ők', 'őket', 'őt']

'''
Copyright (c) 2019, Luthfi Azhari

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Originates from: https:#github.com/stopwords-iso/stopwords-id/
'''

ind = ['ada', 'adalah', 'adanya', 'adapun', 'agak', 'agaknya', 'agar', 'akan', 'akankah', 'akhir', 'akhiri', 'akhirnya', 'aku', 'akulah', 'amat', 'amatlah', 'anda', 'andalah', 'antar', 'antara', 'antaranya', 'apa', 'apaan', 'apabila', 'apakah', 'apalagi', 'apatah', 'artinya', 'asal', 'asalkan', 'atas', 'atau', 'ataukah', 'ataupun', 'awal', 'awalnya', 'bagai', 'bagaikan', 'bagaimana', 'bagaimanakah', 'bagaimanapun', 'bagi', 'bagian', 'bahkan', 'bahwa', 'bahwasanya', 'bakal', 'bakalan', 'balik', 'banyak', 'bapak', 'baru', 'bawah', 'beberapa', 'begini', 'beginian', 'beginikah', 'beginilah', 'begitu', 'begitukah', 'begitulah', 'begitupun', 'bekerja', 'belakang', 'belakangan', 'belum', 'belumlah', 'benar', 'benarkah', 'benarlah', 'berada', 'berakhir', 'berakhirlah', 'berakhirnya', 'berapa', 'berapakah', 'berapalah', 'berapapun', 'berarti', 'berawal', 'berbagai', 'berdatangan', 'beri', 'berikan', 'berikut', 'berikutnya', 'berjumlah', 'berkali-kali', 'berkata', 'berkehendak', 'berkeinginan', 'berkenaan', 'berlainan', 'berlalu', 'berlangsung', 'berlebihan', 'bermacam', 'bermacam-macam', 'bermaksud', 'bermula', 'bersama', 'bersama-sama', 'bersiap', 'bersiap-siap', 'bertanya', 'bertanya-tanya', 'berturut', 'berturut-turut', 'bertutur', 'berujar', 'berupa', 'besar', 'betul', 'betulkah', 'biasa', 'biasanya', 'bila', 'bilakah', 'bisa', 'bisakah', 'boleh', 'bolehkah', 'bolehlah', 'buat', 'bukan', 'bukankah', 'bukanlah', 'bukannya', 'bulan', 'bung', 'cara', 'caranya', 'cukup', 'cukupkah', 'cukuplah', 'cuma', 'dahulu', 'dalam', 'dan', 'dapat', 'dari', 'daripada', 'datang', 'dekat', 'demi', 'demikian', 'demikianlah', 'dengan', 'depan', 'di', 'dia', 'diakhiri', 'diakhirinya', 'dialah', 'diantara', 'diantaranya', 'diberi', 'diberikan', 'diberikannya', 'dibuat', 'dibuatnya', 'didapat', 'didatangkan', 'digunakan', 'diibaratkan', 'diibaratkannya', 'diingat', 'diingatkan', 'diinginkan', 'dijawab', 'dijelaskan', 'dijelaskannya', 'dikarenakan', 'dikatakan', 'dikatakannya', 'dikerjakan', 'diketahui', 'diketahuinya', 'dikira', 'dilakukan', 'dilalui', 'dilihat', 'dimaksud', 'dimaksudkan', 'dimaksudkannya', 'dimaksudnya', 'diminta', 'dimintai', 'dimisalkan', 'dimulai', 'dimulailah', 'dimulainya', 'dimungkinkan', 'dini', 'dipastikan', 'diperbuat', 'diperbuatnya', 'dipergunakan', 'diperkirakan', 'diperlihatkan', 'diperlukan', 'diperlukannya', 'dipersoalkan', 'dipertanyakan', 'dipunyai', 'diri', 'dirinya', 'disampaikan', 'disebut', 'disebutkan', 'disebutkannya', 'disini', 'disinilah', 'ditambahkan', 'ditandaskan', 'ditanya', 'ditanyai', 'ditanyakan', 'ditegaskan', 'ditujukan', 'ditunjuk', 'ditunjuki', 'ditunjukkan', 'ditunjukkannya', 'ditunjuknya', 'dituturkan', 'dituturkannya', 'diucapkan', 'diucapkannya', 'diungkapkan', 'dong', 'dulu', 'empat', 'enggak', 'enggaknya', 'entah', 'entahlah', 'guna', 'gunakan', 'hal', 'hampir', 'hanya', 'hanyalah', 'harus', 'haruslah', 'harusnya', 'hendak', 'hendaklah', 'hendaknya', 'hingga', 'ia', 'ialah', 'ibarat', 'ibaratkan', 'ibaratnya', 'ikut', 'ingat', 'ingat-ingat', 'ingin', 'inginkah', 'inginkan', 'ini', 'inikah', 'inilah', 'itu', 'itukah', 'itulah', 'jadi', 'jadilah', 'jadinya', 'jangan', 'jangankan', 'janganlah', 'jauh', 'jawab', 'jawaban', 'jawabnya', 'jelas', 'jelaskan', 'jelaslah', 'jelasnya', 'jika', 'jikalau', 'juga', 'jumlah', 'jumlahnya', 'justru', 'kala', 'kalau', 'kalaulah', 'kalaupun', 'kalian', 'kami', 'kamilah', 'kamu', 'kamulah', 'kan', 'kapan', 'kapankah', 'kapanpun', 'karena', 'karenanya', 'kasus', 'kata', 'katakan', 'katakanlah', 'katanya', 'ke', 'keadaan', 'kebetulan', 'kecil', 'kedua', 'keduanya', 'keinginan', 'kelamaan', 'kelihatan', 'kelihatannya', 'kelima', 'keluar', 'kembali', 'kemudian', 'kemungkinan', 'kemungkinannya', 'kenapa', 'kepada', 'kepadanya', 'kesampaian', 'keseluruhan', 'keseluruhannya', 'keterlaluan', 'ketika', 'khususnya', 'kini', 'kinilah', 'kira', 'kira-kira', 'kiranya', 'kita', 'kitalah', 'kok', 'kurang', 'lagi', 'lagian', 'lah', 'lain', 'lainnya', 'lalu', 'lama', 'lamanya', 'lanjut', 'lanjutnya', 'lebih', 'lewat', 'lima', 'luar', 'macam', 'maka', 'makanya', 'makin', 'malah', 'malahan', 'mampu', 'mampukah', 'mana', 'manakala', 'manalagi', 'masa', 'masalah', 'masalahnya', 'masih', 'masihkah', 'masing', 'masing-masing', 'mau', 'maupun', 'melainkan', 'melakukan', 'melalui', 'melihat', 'melihatnya', 'memang', 'memastikan', 'memberi', 'memberikan', 'membuat', 'memerlukan', 'memihak', 'meminta', 'memintakan', 'memisalkan', 'memperbuat', 'mempergunakan', 'memperkirakan', 'memperlihatkan', 'mempersiapkan', 'mempersoalkan', 'mempertanyakan', 'mempunyai', 'memulai', 'memungkinkan', 'menaiki', 'menambahkan', 'menandaskan', 'menanti', 'menanti-nanti', 'menantikan', 'menanya', 'menanyai', 'menanyakan', 'mendapat', 'mendapatkan', 'mendatang', 'mendatangi', 'mendatangkan', 'menegaskan', 'mengakhiri', 'mengapa', 'mengatakan', 'mengatakannya', 'mengenai', 'mengerjakan', 'mengetahui', 'menggunakan', 'menghendaki', 'mengibaratkan', 'mengibaratkannya', 'mengingat', 'mengingatkan', 'menginginkan', 'mengira', 'mengucapkan', 'mengucapkannya', 'mengungkapkan', 'menjadi', 'menjawab', 'menjelaskan', 'menuju', 'menunjuk', 'menunjuki', 'menunjukkan', 'menunjuknya', 'menurut', 'menuturkan', 'menyampaikan', 'menyangkut', 'menyatakan', 'menyebutkan', 'menyeluruh', 'menyiapkan', 'merasa', 'mereka', 'merekalah', 'merupakan', 'meski', 'meskipun', 'meyakini', 'meyakinkan', 'minta', 'mirip', 'misal', 'misalkan', 'misalnya', 'mula', 'mulai', 'mulailah', 'mulanya', 'mungkin', 'mungkinkah', 'nah', 'naik', 'namun', 'nanti', 'nantinya', 'nyaris', 'nyatanya', 'oleh', 'olehnya', 'pada', 'padahal', 'padanya', 'paling', 'panjang', 'pantas', 'para', 'pasti', 'pastilah', 'penting', 'pentingnya', 'per', 'percuma', 'perlu', 'perlukah', 'perlunya', 'pernah', 'persoalan', 'pertama', 'pertama-tama', 'pertanyaan', 'pertanyakan', 'pihak', 'pihaknya', 'pukul', 'pula', 'pun', 'punya', 'rasa', 'rasanya', 'rata', 'rupanya', 'saat', 'saatnya', 'saja', 'sajalah', 'saling', 'sama', 'sama-sama', 'sambil', 'sampai', 'sampai-sampai', 'sampaikan', 'sana', 'sangat', 'sangatlah', 'satu', 'saya', 'sayalah', 'se', 'sebab', 'sebabnya', 'sebagai', 'sebagaimana', 'sebagainya', 'sebagian', 'sebaik', 'sebaik-baiknya', 'sebaiknya', 'sebaliknya', 'sebanyak', 'sebegini', 'sebegitu', 'sebelum', 'sebelumnya', 'sebenarnya', 'seberapa', 'sebesar', 'sebetulnya', 'sebisanya', 'sebuah', 'sebut', 'sebutlah', 'sebutnya', 'secara', 'secukupnya', 'sedang', 'sedangkan', 'sedemikian', 'sedikit', 'sedikitnya', 'seenaknya', 'segala', 'segalanya', 'segera', 'seharusnya', 'sehingga', 'seingat', 'sejak', 'sejauh', 'sejenak', 'sejumlah', 'sekadar', 'sekadarnya', 'sekali', 'sekali-kali', 'sekalian', 'sekaligus', 'sekalipun', 'sekarang', 'sekarang', 'sekecil', 'seketika', 'sekiranya', 'sekitar', 'sekitarnya', 'sekurang-kurangnya', 'sekurangnya', 'sela', 'selain', 'selaku', 'selalu', 'selama', 'selama-lamanya', 'selamanya', 'selanjutnya', 'seluruh', 'seluruhnya', 'semacam', 'semakin', 'semampu', 'semampunya', 'semasa', 'semasih', 'semata', 'semata-mata', 'semaunya', 'sementara', 'semisal', 'semisalnya', 'sempat', 'semua', 'semuanya', 'semula', 'sendiri', 'sendirian', 'sendirinya', 'seolah', 'seolah-olah', 'seorang', 'sepanjang', 'sepantasnya', 'sepantasnyalah', 'seperlunya', 'seperti', 'sepertinya', 'sepihak', 'sering', 'seringnya', 'serta', 'serupa', 'sesaat', 'sesama', 'sesampai', 'sesegera', 'sesekali', 'seseorang', 'sesuatu', 'sesuatunya', 'sesudah', 'sesudahnya', 'setelah', 'setempat', 'setengah', 'seterusnya', 'setiap', 'setiba', 'setibanya', 'setidak-tidaknya', 'setidaknya', 'setinggi', 'seusai', 'sewaktu', 'siap', 'siapa', 'siapakah', 'siapapun', 'sini', 'sinilah', 'soal', 'soalnya', 'suatu', 'sudah', 'sudahkah', 'sudahlah', 'supaya', 'tadi', 'tadinya', 'tahu', 'tahun', 'tak', 'tambah', 'tambahnya', 'tampak', 'tampaknya', 'tandas', 'tandasnya', 'tanpa', 'tanya', 'tanyakan', 'tanyanya', 'tapi', 'tegas', 'tegasnya', 'telah', 'tempat', 'tengah', 'tentang', 'tentu', 'tentulah', 'tentunya', 'tepat', 'terakhir', 'terasa', 'terbanyak', 'terdahulu', 'terdapat', 'terdiri', 'terhadap', 'terhadapnya', 'teringat', 'teringat-ingat', 'terjadi', 'terjadilah', 'terjadinya', 'terkira', 'terlalu', 'terlebih', 'terlihat', 'termasuk', 'ternyata', 'tersampaikan', 'tersebut', 'tersebutlah', 'tertentu', 'tertuju', 'terus', 'terutama', 'tetap', 'tetapi', 'tiap', 'tiba', 'tiba-tiba', 'tidak', 'tidakkah', 'tidaklah', 'tiga', 'tinggi', 'toh', 'tunjuk', 'turut', 'tutur', 'tuturnya', 'ucap', 'ucapnya', 'ujar', 'ujarnya', 'umum', 'umumnya', 'ungkap', 'ungkapnya', 'untuk', 'usah', 'usai', 'waduh', 'wah', 'wahai', 'waktu', 'waktunya', 'walau', 'walaupun', 'wong', 'yaitu', 'yakin', 'yakni', 'yang']

'''
Copyright (c) 2011, David Przybilla, Chris Umbel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

ita = ['ad', 'al', 'allo', 'ai', 'agli', 'all', 'agl', 'alla', 'alle', 'con', 'col', 'coi', 'da', 'dal', 'dallo', 'dai', 'dagli', 'dall', 'dagl', 'dalla', 'dalle', 'di', 'del', 'dello', 'dei', 'degli', 'dell', 'degl', 'della', 'delle', 'in', 'nel', 'nello', 'nei', 'negli', 'nell', 'negl', 'nella', 'nelle', 'su', 'sul', 'sullo', 'sui', 'sugli', 'sull', 'sugl', 'sulla', 'sulle', 'per', 'tra', 'contro', 'io', 'tu', 'lui', 'lei', 'noi', 'voi', 'loro', 'mio', 'mia', 'miei', 'mie', 'tuo', 'tua', 'tuoi', 'tue', 'suo', 'sua', 'suoi', 'sue', 'nostro', 'nostra', 'nostri', 'nostre', 'vostro', 'vostra', 'vostri', 'vostre', 'mi', 'ti', 'ci', 'vi', 'lo', 'la', 'li', 'le', 'gli', 'ne', 'il', 'un', 'uno', 'una', 'ma', 'ed', 'se', 'perché', 'anche', 'come', 'dov', 'dove', 'che', 'chi', 'cui', 'non', 'più', 'quale', 'quanto', 'quanti', 'quanta', 'quante', 'quello', 'quelli', 'quella', 'quelle', 'questo', 'questi', 'questa', 'queste', 'si', 'tutto', 'tutti', 'a', 'c', 'e', 'i', 'l', 'o', 'ho', 'hai', 'ha', 'abbiamo', 'avete', 'hanno', 'abbia', 'abbiate', 'abbiano', 'avrò', 'avrai', 'avrà', 'avremo', 'avrete', 'avranno', 'avrei', 'avresti', 'avrebbe', 'avremmo', 'avreste', 'avrebbero', 'avevo', 'avevi', 'aveva', 'avevamo', 'avevate', 'avevano', 'ebbi', 'avesti', 'ebbe', 'avemmo', 'aveste', 'ebbero', 'avessi', 'avesse', 'avessimo', 'avessero', 'avendo', 'avuto', 'avuta', 'avuti', 'avute', 'sono', 'sei', 'è', 'siamo', 'siete', 'sia', 'siate', 'siano', 'sarò', 'sarai', 'sarà', 'saremo', 'sarete', 'saranno', 'sarei', 'saresti', 'sarebbe', 'saremmo', 'sareste', 'sarebbero', 'ero', 'eri', 'era', 'eravamo', 'eravate', 'erano', 'fui', 'fosti', 'fu', 'fummo', 'foste', 'furono', 'fossi', 'fosse', 'fossimo', 'fossero', 'essendo', 'faccio', 'fai', 'facciamo', 'fanno', 'faccia', 'facciate', 'facciano', 'farò', 'farai', 'farà', 'faremo', 'farete', 'faranno', 'farei', 'faresti', 'farebbe', 'faremmo', 'fareste', 'farebbero', 'facevo', 'facevi', 'faceva', 'facevamo', 'facevate', 'facevano', 'feci', 'facesti', 'fece', 'facemmo', 'faceste', 'fecero', 'facessi', 'facesse', 'facessimo', 'facessero', 'facendo', 'sto', 'stai', 'sta', 'stiamo', 'stanno', 'stia', 'stiate', 'stiano', 'starò', 'starai', 'starà', 'staremo', 'starete', 'staranno', 'starei', 'staresti', 'starebbe', 'staremmo', 'stareste', 'starebbero', 'stavo', 'stavi', 'stava', 'stavamo', 'stavate', 'stavano', 'stetti', 'stesti', 'stette', 'stemmo', 'steste', 'stettero', 'stessi', 'stesse', 'stessimo', 'stessero', 'stando']

# Original copyright:
'''
 Licensed to the Apache Software Foundation (ASF) under one or more
 contributor license agreements.  See the NOTICE file distributed with
 this work for additional information regarding copyright ownership.
 The ASF licenses this file to You under the Apache License, Version 2.0
 the "License"); you may not use this file except in compliance with
 the License.  You may obtain a copy of the License at

 http:#www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
'''

# This version:
''' The MIT License (MIT)
Copyright (c) 2012, Guillaume Marty

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

# Original location:
# http:#svn.apache.org/repos/asf/lucene/dev/trunk/lucene/analysis/kuromoji/src/resources/org/apache/lucene/analysis/ja/stopwords.txt

jpn = ['の', 'に', 'は', 'を', 'た', 'が', 'で', 'て', 'と', 'し', 'れ', 'さ', 'ある', 'いる', 'も', 'する', 'から', 'な', 'こと', 'として', 'い', 'や', 'れる', 'など', 'なっ', 'ない', 'この', 'ため', 'その', 'あっ', 'よう', 'また', 'もの', 'という', 'あり', 'まで', 'られ', 'なる', 'へ', 'か', 'だ', 'これ', 'によって', 'により', 'おり', 'より', 'による', 'ず', 'なり', 'られる', 'において', 'ば', 'なかっ', 'なく', 'しかし', 'について', 'せ', 'だっ', 'その後', 'できる', 'それ', 'う', 'ので', 'なお', 'のみ', 'でき', 'き', 'つ', 'における', 'および', 'いう', 'さらに', 'でも', 'ら', 'たり', 'その他', 'に関する', 'たち', 'ます', 'ん', 'なら', 'に対して', '特に', 'せる', '及び', 'これら', 'とき', 'では', 'にて', 'ほか', 'ながら', 'うち', 'そして', 'とともに', 'ただし', 'かつて', 'それぞれ', 'または', 'お', 'ほど', 'ものの', 'に対する', 'ほとんど', 'と共に', 'といった', 'です', 'とも', 'ところ', 'ここ']

# Copyright (c) 2017 Peter Graham, contributors. Released under the Apache-2.0 license.

kor = ['가', '가까스로', '가령', '각', '각각', '각자', '각종', '갖고말하자면', '같다', '같이', '개의치않고', '거니와', '거바', '거의', '것', '것과 같이', '것들', '게다가', '게우다', '겨우', '견지에서', '결과에 이르다', '결국', '결론을 낼 수 있다', '겸사겸사', '고려하면', '고로', '곧', '공동으로', '과', '과연', '관계가 있다', '관계없이', '관련이 있다', '관하여', '관한', '관해서는', '구', '구체적으로', '구토하다', '그', '그들', '그때', '그래', '그래도', '그래서', '그러나', '그러니', '그러니까', '그러면', '그러므로', '그러한즉', '그런 까닭에', '그런데', '그런즉', '그럼', '그럼에도 불구하고', '그렇게 함으로써', '그렇지', '그렇지 않다면', '그렇지 않으면', '그렇지만', '그렇지않으면', '그리고', '그리하여', '그만이다', '그에 따르는', '그위에', '그저', '그중에서', '그치지 않다', '근거로', '근거하여', '기대여', '기점으로', '기준으로', '기타', '까닭으로', '까악', '까지', '까지 미치다', '까지도', '꽈당', '끙끙', '끼익', '나', '나머지는', '남들', '남짓', '너', '너희', '너희들', '네', '넷', '년', '논하지 않다', '놀라다', '누가 알겠는가', '누구', '다른', '다른 방면으로', '다만', '다섯', '다소', '다수', '다시 말하자면', '다시말하면', '다음', '다음에', '다음으로', '단지', '답다', '당신', '당장', '대로 하다', '대하면', '대하여', '대해 말하자면', '대해서', '댕그', '더구나', '더군다나', '더라도', '더불어', '더욱더', '더욱이는', '도달하다', '도착하다', '동시에', '동안', '된바에야', '된이상', '두번째로', '둘', '둥둥', '뒤따라', '뒤이어', '든간에', '들', '등', '등등', '딩동', '따라', '따라서', '따위', '따지지 않다', '딱', '때', '때가 되어', '때문에', '또', '또한', '뚝뚝', '라 해도', '령', '로', '로 인하여', '로부터', '로써', '륙', '를', '마음대로', '마저', '마저도', '마치', '막론하고', '만 못하다', '만약', '만약에', '만은 아니다', '만이 아니다', '만일', '만큼', '말하자면', '말할것도 없고', '매', '매번', '메쓰겁다', '몇', '모', '모두', '무렵', '무릎쓰고', '무슨', '무엇', '무엇때문에', '물론', '및', '바꾸어말하면', '바꾸어말하자면', '바꾸어서 말하면', '바꾸어서 한다면', '바꿔 말하면', '바로', '바와같이', '밖에 안된다', '반대로', '반대로 말하자면', '반드시', '버금', '보는데서', '보다더', '보드득', '본대로', '봐', '봐라', '부류의 사람들', '부터', '불구하고', '불문하고', '붕붕', '비걱거리다', '비교적', '비길수 없다', '비로소', '비록', '비슷하다', '비추어 보아', '비하면', '뿐만 아니라', '뿐만아니라', '뿐이다', '삐걱', '삐걱거리다', '사', '삼', '상대적으로 말하자면', '생각한대로', '설령', '설마', '설사', '셋', '소생', '소인', '솨', '쉿', '습니까', '습니다', '시각', '시간', '시작하여', '시초에', '시키다', '실로', '심지어', '아', '아니', '아니나다를가', '아니라면', '아니면', '아니었다면', '아래윗', '아무거나', '아무도', '아야', '아울러', '아이', '아이고', '아이구', '아이야', '아이쿠', '아하', '아홉', '안 그러면', '않기 위하여', '않기 위해서', '알 수 있다', '알았어', '앗', '앞에서', '앞의것', '야', '약간', '양자', '어', '어기여차', '어느', '어느 년도', '어느것', '어느곳', '어느때', '어느쪽', '어느해', '어디', '어때', '어떠한', '어떤', '어떤것', '어떤것들', '어떻게', '어떻해', '어이', '어째서', '어쨋든', '어쩔수 없다', '어찌', '어찌됏든', '어찌됏어', '어찌하든지', '어찌하여', '언제', '언젠가', '얼마', '얼마 안 되는 것', '얼마간', '얼마나', '얼마든지', '얼마만큼', '얼마큼', '엉엉', '에', '에 가서', '에 달려 있다', '에 대해', '에 있다', '에 한하다', '에게', '에서', '여', '여기', '여덟', '여러분', '여보시오', '여부', '여섯', '여전히', '여차', '연관되다', '연이서', '영', '영차', '옆사람', '예', '예를 들면', '예를 들자면', '예컨대', '예하면', '오', '오로지', '오르다', '오자마자', '오직', '오호', '오히려', '와', '와 같은 사람들', '와르르', '와아', '왜', '왜냐하면', '외에도', '요만큼', '요만한 것', '요만한걸', '요컨대', '우르르', '우리', '우리들', '우선', '우에 종합한것과같이', '운운', '월', '위에서 서술한바와같이', '위하여', '위해서', '윙윙', '육', '으로', '으로 인하여', '으로서', '으로써', '을', '응', '응당', '의', '의거하여', '의지하여', '의해', '의해되다', '의해서', '이', '이 되다', '이 때문에', '이 밖에', '이 외에', '이 정도의', '이것', '이곳', '이때', '이라면', '이래', '이러이러하다', '이러한', '이런', '이럴정도로', '이렇게 많은 것', '이렇게되면', '이렇게말하자면', '이렇구나', '이로 인하여', '이르기까지', '이리하여', '이만큼', '이번', '이봐', '이상', '이어서', '이었다', '이와 같다', '이와 같은', '이와 반대로', '이와같다면', '이외에도', '이용하여', '이유만으로', '이젠', '이지만', '이쪽', '이천구', '이천육', '이천칠', '이천팔', '인 듯하다', '인젠', '일', '일것이다', '일곱', '일단', '일때', '일반적으로', '일지라도', '임에 틀림없다', '입각하여', '입장에서', '잇따라', '있다', '자', '자기', '자기집', '자마자', '자신', '잠깐', '잠시', '저', '저것', '저것만큼', '저기', '저쪽', '저희', '전부', '전자', '전후', '점에서 보아', '정도에 이르다', '제', '제각기', '제외하고', '조금', '조차', '조차도', '졸졸', '좀', '좋아', '좍좍', '주룩주룩', '주저하지 않고', '줄은 몰랏다', '줄은모른다', '중에서', '중의하나', '즈음하여', '즉', '즉시', '지든지', '지만', '지말고', '진짜로', '쪽으로', '차라리', '참', '참나', '첫번째로', '쳇', '총적으로', '총적으로 말하면', '총적으로 보면', '칠', '콸콸', '쾅쾅', '쿵', '타다', '타인', '탕탕', '토하다', '통하여', '툭', '퉤', '틈타', '팍', '팔', '퍽', '펄렁', '하', '하게될것이다', '하게하다', '하겠는가', '하고 있다', '하고있었다', '하곤하였다', '하구나', '하기 때문에', '하기 위하여', '하기는한데', '하기만 하면', '하기보다는', '하기에', '하나', '하느니', '하는 김에', '하는 편이 낫다', '하는것도', '하는것만 못하다', '하는것이 낫다', '하는바', '하더라도', '하도다', '하도록시키다', '하도록하다', '하든지', '하려고하다', '하마터면', '하면 할수록', '하면된다', '하면서', '하물며', '하여금', '하여야', '하자마자', '하지 않는다면', '하지 않도록', '하지마', '하지마라', '하지만', '하하', '한 까닭에', '한 이유는', '한 후', '한다면', '한다면 몰라도', '한데', '한마디', '한적이있다', '한켠으로는', '한항목', '할 따름이다', '할 생각이다', '할 줄 안다', '할 지경이다', '할 힘이 있다', '할때', '할만하다', '할망정', '할뿐', '할수있다', '할수있어', '할줄알다', '할지라도', '할지언정', '함께', '해도된다', '해도좋다', '해봐요', '해서는 안된다', '해야한다', '해요', '했어요', '향하다', '향하여', '향해서', '허', '허걱', '허허', '헉', '헉헉', '헐떡헐떡', '형식으로 쓰여', '혹시', '혹은', '혼자', '훨씬', '휘익', '휴', '흐흐', '흥', '힘입어', '︿', '～', '￥']

''' The MIT License (MIT)

Copyright (c) 2016 Gene Diaz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. '''

kur = ['ئێمە', 'ئێوە', 'ئەم', 'ئەو', 'ئەوان', 'ئەوەی', 'بۆ', 'بێ', 'بێجگە', 'بە', 'بەبێ', 'بەدەم', 'بەردەم', 'بەرلە', 'بەرەوی', 'بەرەوە', 'بەلای', 'بەپێی', 'تۆ', 'تێ', 'جگە', 'دوای', 'دوو', 'دە', 'دەکات', 'دەگەڵ', 'سەر', 'لێ', 'لە', 'لەبابەت', 'لەباتی', 'لەبارەی', 'لەبرێتی', 'لەبن', 'لەبەر', 'لەبەینی', 'لەدەم', 'لەرێ', 'لەرێگا', 'لەرەوی', 'لەسەر', 'لەلایەن', 'لەناو', 'لەنێو', 'لەو', 'لەپێناوی', 'لەژێر', 'لەگەڵ', 'من', 'ناو', 'نێوان', 'هەر', 'هەروەها', 'و', 'وەک', 'پاش', 'پێ', 'پێش', 'چەند', 'کرد', 'کە', 'ی']

# Copyright (c) 2017 Peter Graham, contributors. Released under the Apache-2.0 license.

lat = ['a', 'ab', 'ac', 'ad', 'at', 'atque', 'aut', 'autem', 'cum', 'de', 'dum', 'e', 'erant', 'erat', 'est', 'et', 'etiam', 'ex', 'haec', 'hic', 'hoc', 'in', 'ita', 'me', 'nec', 'neque', 'non', 'per', 'qua', 'quae', 'quam', 'qui', 'quibus', 'quidem', 'quo', 'quod', 're', 'rebus', 'rem', 'res', 'sed', 'si', 'sic', 'sunt', 'tamen', 'tandem', 'te', 'ut', 'vel']

# Copyright (c) 2017 Peter Graham, contributors. Released under the Apache-2.0 license.

lav = ['aiz', 'ap', 'apakš', 'apakšpus', 'ar', 'arī', 'augšpus', 'bet', 'bez', 'bija', 'biji', 'biju', 'bijām', 'bijāt', 'būs', 'būsi', 'būsiet', 'būsim', 'būt', 'būšu', 'caur', 'diemžēl', 'diezin', 'droši', 'dēļ', 'esam', 'esat', 'esi', 'esmu', 'gan', 'gar', 'iekam', 'iekams', 'iekām', 'iekāms', 'iekš', 'iekšpus', 'ik', 'ir', 'it', 'itin', 'iz', 'ja', 'jau', 'jeb', 'jebšu', 'jel', 'jo', 'jā', 'ka', 'kamēr', 'kaut', 'kolīdz', 'kopš', 'kā', 'kļuva', 'kļuvi', 'kļuvu', 'kļuvām', 'kļuvāt', 'kļūs', 'kļūsi', 'kļūsiet', 'kļūsim', 'kļūst', 'kļūstam', 'kļūstat', 'kļūsti', 'kļūstu', 'kļūt', 'kļūšu', 'labad', 'lai', 'lejpus', 'līdz', 'līdzko', 'ne', 'nebūt', 'nedz', 'nekā', 'nevis', 'nezin', 'no', 'nu', 'nē', 'otrpus', 'pa', 'par', 'pat', 'pie', 'pirms', 'pret', 'priekš', 'pār', 'pēc', 'starp', 'tad', 'tak', 'tapi', 'taps', 'tapsi', 'tapsiet', 'tapsim', 'tapt', 'tapāt', 'tapšu', 'taču', 'te', 'tiec', 'tiek', 'tiekam', 'tiekat', 'tieku', 'tik', 'tika', 'tikai', 'tiki', 'tikko', 'tiklab', 'tiklīdz', 'tiks', 'tiksiet', 'tiksim', 'tikt', 'tiku', 'tikvien', 'tikām', 'tikāt', 'tikšu', 'tomēr', 'topat', 'turpretim', 'turpretī', 'tā', 'tādēļ', 'tālab', 'tāpēc', 'un', 'uz', 'vai', 'var', 'varat', 'varēja', 'varēji', 'varēju', 'varējām', 'varējāt', 'varēs', 'varēsi', 'varēsiet', 'varēsim', 'varēt', 'varēšu', 'vien', 'virs', 'virspus', 'vis', 'viņpus', 'zem', 'ārpus', 'šaipus']

''' The MIT License (MIT)

Copyright (c) 2016 Gene Diaz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. '''

lit = ['abi', 'abidvi', 'abiejose', 'abiejuose', 'abiejø', 'abiem', 'abigaliai', 'abipus', 'abu', 'abudu', 'ai', 'ana', 'anaiptol', 'anaisiais', 'anajai', 'anajam', 'anajame', 'anapus', 'anas', 'anasai', 'anasis', 'anei', 'aniedvi', 'anieji', 'aniesiems', 'anoji', 'anojo', 'anojoje', 'anokia', 'anoks', 'anosiomis', 'anosioms', 'anosios', 'anosiose', 'anot', 'ant', 'antai', 'anuodu', 'anuoju', 'anuosiuose', 'anuosius', 'anàja', 'anàjà', 'anàjá', 'anàsias', 'anøjø', 'apie', 'aplink', 'ar', 'arba', 'argi', 'arti', 'aukðèiau', 'að', 'be', 'bei', 'beje', 'bemaþ', 'bent', 'bet', 'betgi', 'beveik', 'dar', 'dargi', 'daugmaþ', 'deja', 'dëka', 'dël', 'dëlei', 'dëlto', 'ech', 'et', 'gal', 'galbût', 'galgi', 'gan', 'gana', 'gi', 'greta', 'idant', 'iki', 'ir', 'irgi', 'it', 'itin', 'ið', 'iðilgai', 'iðvis', 'jaisiais', 'jajai', 'jajam', 'jajame', 'jei', 'jeigu', 'ji', 'jiedu', 'jiedvi', 'jieji', 'jiesiems', 'jinai', 'jis', 'jisai', 'jog', 'joji', 'jojo', 'jojoje', 'jokia', 'joks', 'josiomis', 'josioms', 'josios', 'josiose', 'judu', 'judvi', 'juk', 'jumis', 'jums', 'jumyse', 'juodu', 'juoju', 'juosiuose', 'juosius', 'jus', 'jàja', 'jàjà', 'jàsias', 'jájá', 'jøjø', 'jûs', 'jûsiðkis', 'jûsiðkë', 'jûsø', 'kad', 'kada', 'kadangi', 'kai', 'kaip', 'kaipgi', 'kas', 'katra', 'katras', 'katriedvi', 'katruodu', 'kaþin', 'kaþkas', 'kaþkatra', 'kaþkatras', 'kaþkokia', 'kaþkoks', 'kaþkuri', 'kaþkuris', 'kiaurai', 'kiek', 'kiekvienas', 'kieno', 'kita', 'kitas', 'kitokia', 'kitoks', 'kodël', 'kokia', 'koks', 'kol', 'kolei', 'kone', 'kuomet', 'kur', 'kurgi', 'kuri', 'kuriedvi', 'kuris', 'kuriuodu', 'lai', 'lig', 'ligi', 'link', 'lyg', 'man', 'manaisiais', 'manajai', 'manajam', 'manajame', 'manas', 'manasai', 'manasis', 'mane', 'manieji', 'maniesiems', 'manim', 'manimi', 'maniðkis', 'maniðkë', 'mano', 'manoji', 'manojo', 'manojoje', 'manosiomis', 'manosioms', 'manosios', 'manosiose', 'manuoju', 'manuosiuose', 'manuosius', 'manyje', 'manàja', 'manàjà', 'manàjá', 'manàsias', 'manæs', 'manøjø', 'mat', 'maþdaug', 'maþne', 'mes', 'mudu', 'mudvi', 'mumis', 'mums', 'mumyse', 'mus', 'mûsiðkis', 'mûsiðkë', 'mûsø', 'na', 'nagi', 'ne', 'nebe', 'nebent', 'negi', 'negu', 'nei', 'nejau', 'nejaugi', 'nekaip', 'nelyginant', 'nes', 'net', 'netgi', 'netoli', 'neva', 'nors', 'nuo', 'në', 'o', 'ogi', 'oi', 'paeiliui', 'pagal', 'pakeliui', 'palaipsniui', 'palei', 'pas', 'pasak', 'paskos', 'paskui', 'paskum', 'pat', 'pati', 'patiems', 'paties', 'pats', 'patys', 'patá', 'paèiais', 'paèiam', 'paèiame', 'paèiu', 'paèiuose', 'paèius', 'paèiø', 'per', 'pernelyg', 'pirm', 'pirma', 'pirmiau', 'po', 'prie', 'prieð', 'prieðais', 'pro', 'pusiau', 'rasi', 'rodos', 'sau', 'savaisiais', 'savajai', 'savajam', 'savajame', 'savas', 'savasai', 'savasis', 'save', 'savieji', 'saviesiems', 'savimi', 'saviðkis', 'saviðkë', 'savo', 'savoji', 'savojo', 'savojoje', 'savosiomis', 'savosioms', 'savosios', 'savosiose', 'savuoju', 'savuosiuose', 'savuosius', 'savyje', 'savàja', 'savàjà', 'savàjá', 'savàsias', 'savæs', 'savøjø', 'skersai', 'skradþiai', 'staèiai', 'su', 'sulig', 'ta', 'tad', 'tai', 'taigi', 'taip', 'taipogi', 'taisiais', 'tajai', 'tajam', 'tajame', 'tamsta', 'tarp', 'tarsi', 'tartum', 'tarytum', 'tas', 'tasai', 'tau', 'tavaisiais', 'tavajai', 'tavajam', 'tavajame', 'tavas', 'tavasai', 'tavasis', 'tave', 'tavieji', 'taviesiems', 'tavimi', 'taviðkis', 'taviðkë', 'tavo', 'tavoji', 'tavojo', 'tavojoje', 'tavosiomis', 'tavosioms', 'tavosios', 'tavosiose', 'tavuoju', 'tavuosiuose', 'tavuosius', 'tavyje', 'tavàja', 'tavàjà', 'tavàjá', 'tavàsias', 'tavæs', 'tavøjø', 'taèiau', 'te', 'tegu', 'tegul', 'tiedvi', 'tieji', 'ties', 'tiesiems', 'tiesiog', 'tik', 'tikriausiai', 'tiktai', 'toji', 'tojo', 'tojoje', 'tokia', 'toks', 'tol', 'tolei', 'toliau', 'tosiomis', 'tosioms', 'tosios', 'tosiose', 'tu', 'tuodu', 'tuoju', 'tuosiuose', 'tuosius', 'turbût', 'tàja', 'tàjà', 'tàjá', 'tàsias', 'tøjø', 'tûlas', 'uþ', 'uþtat', 'uþvis', 'va', 'vai', 'viduj', 'vidury', 'vien', 'vienas', 'vienokia', 'vienoks', 'vietoj', 'virð', 'virðuj', 'virðum', 'vis', 'vis dëlto', 'visa', 'visas', 'visgi', 'visokia', 'visoks', 'vos', 'vël', 'vëlgi', 'ypaè', 'á', 'ákypai', 'ástriþai', 'ðalia', 'ðe', 'ði', 'ðiaisiais', 'ðiajai', 'ðiajam', 'ðiajame', 'ðiapus', 'ðiedvi', 'ðieji', 'ðiesiems', 'ðioji', 'ðiojo', 'ðiojoje', 'ðiokia', 'ðioks', 'ðiosiomis', 'ðiosioms', 'ðiosios', 'ðiosiose', 'ðis', 'ðisai', 'ðit', 'ðita', 'ðitas', 'ðitiedvi', 'ðitokia', 'ðitoks', 'ðituodu', 'ðiuodu', 'ðiuoju', 'ðiuosiuose', 'ðiuosius', 'ðiàja', 'ðiàjà', 'ðiàsias', 'ðiøjø', 'ðtai', 'ðájá', 'þemiau']

''' Copyright 2016 Liam Doherty

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http:#www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

''' This list is frequency sorted. That means it can be sliced from the bottom
and be less agressive in excluding stopwords '''

lgg = ['́', '̀', 'nɨ', 'mà', 'rɨ', 'dɨ', 'ɨ', '́nɨ', 'èrɨ', '́á\'', 'sɨ', 'àzɨ', 'yɨ', 'rá', 'vɨ', 'nga', 'be', 'mɨ', 'à', 'dà', 'kʉ', 'bá', ' ́lé', 'má', 'e', 'yo', '̀yɨ', 'ma', 'kɨ', 'àlʉ', '́mà', 'rʉ́', 'drɨ', 'patí', 'a', 'è', 'yó', 'te', '̀á', 'mà', 'mâ', 'dálé', 'yí', '̌', 'pɨ', 'e\'yó', 'ndráa', 'bo', 'di', 'drìá']

''' Copyright 2016 Liam Doherty

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http:#www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

''' This list is frequency sorted. That means it can be sliced from the bottom
and be less agressive in excluding stopwords '''

lggNd = ['ma', 'ni', 'ri', 'eri', 'di', 'yi', 'si', 'ba', 'nga', 'i', 'ra', 'ku', 'be', 'yo', 'da', 'azini', 'dria', 'ru', 'azi', 'mu', 'te', 'ndra', 'diyi', 'ima', 'mi', 'alu', 'nde', 'alia', 'le', 'vile', 'dri', 'pati', 'aria', 'bo', 'e\'yo', 'tu', 'kini', 'dii', 'ama', 'eyi', 'dika', 'pi', 'e', 'angu', 'e\'do', 'pie', 'ka', 'ti', 'o\'du', 'du']

''' The MIT License (MIT)

Copyright (c) 2016 Gene Diaz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. '''

msa = ['abdul', 'abdullah', 'acara', 'ada', 'adalah', 'ahmad', 'air', 'akan', 'akhbar', 'akhir', 'aktiviti', 'alam', 'amat', 'amerika', 'anak', 'anggota', 'antara', 'antarabangsa', 'apa', 'apabila', 'april', 'as', 'asas', 'asean', 'asia', 'asing', 'atas', 'atau', 'australia', 'awal', 'awam', 'bagaimanapun', 'bagi', 'bahagian', 'bahan', 'baharu', 'bahawa', 'baik', 'bandar', 'bank', 'banyak', 'barangan', 'baru', 'baru-baru', 'bawah', 'beberapa', 'bekas', 'beliau', 'belum', 'berada', 'berakhir', 'berbanding', 'berdasarkan', 'berharap', 'berikutan', 'berjaya', 'berjumlah', 'berkaitan', 'berkata', 'berkenaan', 'berlaku', 'bermula', 'bernama', 'bernilai', 'bersama', 'berubah', 'besar', 'bhd', 'bidang', 'bilion', 'bn', 'boleh', 'bukan', 'bulan', 'bursa', 'cadangan', 'china', 'dagangan', 'dalam', 'dan', 'dana', 'dapat', 'dari', 'daripada', 'dasar', 'datang', 'datuk', 'demikian', 'dengan', 'depan', 'derivatives', 'dewan', 'di', 'diadakan', 'dibuka', 'dicatatkan', 'dijangka', 'diniagakan', 'dis', 'disember', 'ditutup', 'dolar', 'dr', 'dua', 'dunia', 'ekonomi', 'eksekutif', 'eksport', 'empat', 'enam', 'faedah', 'feb', 'global', 'hadapan', 'hanya', 'harga', 'hari', 'hasil', 'hingga', 'hubungan', 'ia', 'iaitu', 'ialah', 'indeks', 'india', 'indonesia', 'industri', 'ini', 'islam', 'isnin', 'isu', 'itu', 'jabatan', 'jalan', 'jan', 'jawatan', 'jawatankuasa', 'jepun', 'jika', 'jualan', 'juga', 'julai', 'jumaat', 'jumlah', 'jun', 'juta', 'kadar', 'kalangan', 'kali', 'kami', 'kata', 'katanya', 'kaunter', 'kawasan', 'ke', 'keadaan', 'kecil', 'kedua', 'kedua-dua', 'kedudukan', 'kekal', 'kementerian', 'kemudahan', 'kenaikan', 'kenyataan', 'kepada', 'kepentingan', 'keputusan', 'kerajaan', 'kerana', 'kereta', 'kerja', 'kerjasama', 'kes', 'keselamatan', 'keseluruhan', 'kesihatan', 'ketika', 'ketua', 'keuntungan', 'kewangan', 'khamis', 'kini', 'kira-kira', 'kita', 'klci', 'klibor', 'komposit', 'kontrak', 'kos', 'kuala', 'kuasa', 'kukuh', 'kumpulan', 'lagi', 'lain', 'langkah', 'laporan', 'lebih', 'lepas', 'lima', 'lot', 'luar', 'lumpur', 'mac', 'mahkamah', 'mahu', 'majlis', 'makanan', 'maklumat', 'malam', 'malaysia', 'mana', 'manakala', 'masa', 'masalah', 'masih', 'masing-masing', 'masyarakat', 'mata', 'media', 'mei', 'melalui', 'melihat', 'memandangkan', 'memastikan', 'membantu', 'membawa', 'memberi', 'memberikan', 'membolehkan', 'membuat', 'mempunyai', 'menambah', 'menarik', 'menawarkan', 'mencapai', 'mencatatkan', 'mendapat', 'mendapatkan', 'menerima', 'menerusi', 'mengadakan', 'mengambil', 'mengenai', 'menggalakkan', 'menggunakan', 'mengikut', 'mengumumkan', 'mengurangkan', 'meningkat', 'meningkatkan', 'menjadi', 'menjelang', 'menokok', 'menteri', 'menunjukkan', 'menurut', 'menyaksikan', 'menyediakan', 'mereka', 'merosot', 'merupakan', 'mesyuarat', 'minat', 'minggu', 'minyak', 'modal', 'mohd', 'mudah', 'mungkin', 'naik', 'najib', 'nasional', 'negara', 'negara-negara', 'negeri', 'niaga', 'nilai', 'nov', 'ogos', 'okt', 'oleh', 'operasi', 'orang', 'pada', 'pagi', 'paling', 'pameran', 'papan', 'para', 'paras', 'parlimen', 'parti', 'pasaran', 'pasukan', 'pegawai', 'pejabat', 'pekerja', 'pelabur', 'pelaburan', 'pelancongan', 'pelanggan', 'pelbagai', 'peluang', 'pembangunan', 'pemberita', 'pembinaan', 'pemimpin', 'pendapatan', 'pendidikan', 'penduduk', 'penerbangan', 'pengarah', 'pengeluaran', 'pengerusi', 'pengguna', 'pengurusan', 'peniaga', 'peningkatan', 'penting', 'peratus', 'perdagangan', 'perdana', 'peringkat', 'perjanjian', 'perkara', 'perkhidmatan', 'perladangan', 'perlu', 'permintaan', 'perniagaan', 'persekutuan', 'persidangan', 'pertama', 'pertubuhan', 'pertumbuhan', 'perusahaan', 'peserta', 'petang', 'pihak', 'pilihan', 'pinjaman', 'polis', 'politik', 'presiden', 'prestasi', 'produk', 'program', 'projek', 'proses', 'proton', 'pukul', 'pula', 'pusat', 'rabu', 'rakan', 'rakyat', 'ramai', 'rantau', 'raya', 'rendah', 'ringgit', 'rumah', 'sabah', 'sahaja', 'saham', 'sama', 'sarawak', 'satu', 'sawit', 'saya', 'sdn', 'sebagai', 'sebahagian', 'sebanyak', 'sebarang', 'sebelum', 'sebelumnya', 'sebuah', 'secara', 'sedang', 'segi', 'sehingga', 'sejak', 'sekarang', 'sektor', 'sekuriti', 'selain', 'selama', 'selasa', 'selatan', 'selepas', 'seluruh', 'semakin', 'semalam', 'semasa', 'sementara', 'semua', 'semula', 'sen', 'sendiri', 'seorang', 'sepanjang', 'seperti', 'sept', 'september', 'serantau', 'seri', 'serta', 'sesi', 'setiap', 'setiausaha', 'sidang', 'singapura', 'sini', 'sistem', 'sokongan', 'sri', 'sudah', 'sukan', 'suku', 'sumber', 'supaya', 'susut', 'syarikat', 'syed', 'tahap', 'tahun', 'tan', 'tanah', 'tanpa', 'tawaran', 'teknologi', 'telah', 'tempat', 'tempatan', 'tempoh', 'tenaga', 'tengah', 'tentang', 'terbaik', 'terbang', 'terbesar', 'terbuka', 'terdapat', 'terhadap', 'termasuk', 'tersebut', 'terus', 'tetapi', 'thailand', 'tiada', 'tidak', 'tiga', 'timbalan', 'timur', 'tindakan', 'tinggi', 'tun', 'tunai', 'turun', 'turut', 'umno', 'unit', 'untuk', 'untung', 'urus', 'usaha', 'utama', 'walaupun', 'wang', 'wanita', 'wilayah', 'yang']

# Copyright (c) 2017 Peter Graham, contributors. Released under the Apache-2.0 license.

mar = ['अधिक', 'अनेक', 'अशी', 'असलयाचे', 'असलेल्या', 'असा', 'असून', 'असे', 'आज', 'आणि', 'आता', 'आपल्या', 'आला', 'आली', 'आले', 'आहे', 'आहेत', 'एक', 'एका', 'कमी', 'करणयात', 'करून', 'का', 'काम', 'काय', 'काही', 'किवा', 'की', 'केला', 'केली', 'केले', 'कोटी', 'गेल्या', 'घेऊन', 'जात', 'झाला', 'झाली', 'झाले', 'झालेल्या', 'टा', 'डॉ', 'तर', 'तरी', 'तसेच', 'ता', 'ती', 'तीन', 'ते', 'तो', 'त्या', 'त्याचा', 'त्याची', 'त्याच्या', 'त्याना', 'त्यानी', 'त्यामुळे', 'त्री', 'दिली', 'दोन', 'न', 'नाही', 'निर्ण्य', 'पण', 'पम', 'परयतन', 'पाटील', 'म', 'मात्र', 'माहिती', 'मी', 'मुबी', 'म्हणजे', 'म्हणाले', 'म्हणून', 'या', 'याचा', 'याची', 'याच्या', 'याना', 'यानी', 'येणार', 'येत', 'येथील', 'येथे', 'लाख', 'व', 'व्यकत', 'सर्व', 'सागित्ले', 'सुरू', 'हजार', 'हा', 'ही', 'हे', 'होणार', 'होत', 'होता', 'होती', 'होते']

'''
The MIT License (MIT)

Copyright (c) 2019 Kyaw-Zin-Thant

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the 'Software'), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

mya = ['အပေါ်', 'အနက်', 'အမြဲတမ်း', 'အတွင်းတွင်', 'မကြာမီ', 'မတိုင်မီ', 'ဒါ့အပြင်', 'အောက်မှာ', 'အထဲမှာ', 'ဘယ်တော့မျှ', 'မကြာခဏ', 'တော်တော်လေး', 'စဉ်တွင်', 'နှင့်အတူ', 'နှင့်', 'နှင့်တကွ', 'ကျွန်တော်', 'ကျွန်မ', 'ငါ', 'ကျုပ်', 'ကျွနု်ပ်', 'ကျနော်', 'ကျမ', 'သူ', 'သူမ', 'ထိုဟာ', 'ထိုအရာ', 'ဤအရာ', 'ထို', '၄င်း', 'ကျွန်တော်တို့', 'ကျွန်မတို့', 'ငါတို့', 'ကျုပ်တို့', 'ကျွနု်ပ်တို့', 'ကျနော်တို့', 'ကျမတို့', 'သင်', 'သင်တို့', 'နင်တို့', 'မင်း', 'မင်းတို့', 'သူတို့', 'ကျွန်တော်အား', 'ကျွန်တော်ကို', 'ကျွန်မကို', 'ငါကို', 'ကျုပ်ကို', 'ကျွနု်ပ်ကို', 'သူ့ကို', 'သူမကို', 'ထိုအရာကို', 'သင့်ကို', 'သင်တို့ကို', 'နင်တို့ကို', 'မင်းကို', 'မင်းတို့ကို', 'ငါတို့ကို', 'ကျုပ်တို့ကို', 'ကျွနု်ပ်တို့ကို', 'မိမိကိုယ်တိုင်', 'မိမိဘာသာ', 'မင်းကိုယ်တိုင်', 'မင်းဘာသာ', 'မင်းတို့ကိုယ်တိုင်', 'မင်းတို့ဘာသာ', 'သူကိုယ်တိုင်', 'ကိုယ်တိုင်', 'သူမကိုယ်တိုင်', 'သူ့ဘာသာ', 'သူ့ကိုယ်ကို', 'ကိုယ့်ကိုယ်ကို', 'မိမိကိုယ်ကို', '၄င်းပင်', 'ထိုအရာပင်', 'သည့်', 'မည့်', 'တဲ့', 'ကျွနု်ပ်၏', 'ကျွန်တော်၏', 'ကျွန်မ၏', 'ကျနော်၏', 'ကျမ၏', 'သူ၏', 'သူမ၏', 'ထိုအရာ၏', 'ထိုဟာ၏', 'ကျွနု်ပ်တို့၏', 'ငါတို့၏', 'ကျွန်တော်တို့၏', 'ကျွန်မတို့၏', 'ကျနော်တို့၏', 'ကျမတို့၏', 'သင်၏', 'သင်တို့၏', 'မင်း၏', 'မင်းတို့၏', 'သူတို့၏', 'ကျွန်တော့်ဟာ', 'ကျွန်မဟာ', 'ကျနော်၏ဟာ', 'ကျမ၏ဟာ', 'ကျမဟာ', 'ကျနော်ဟာ', 'သူဟာ', 'သူမဟာ', 'သူ့ဟာ', 'ကျွနု်ပ်တို့ဟာ', 'ကျွန်တော်တို့ဟာ', 'ကျွန်မတို့ဟာ', 'သင်တို့ဟာ', 'မင်းတို့ဟာ', 'သူတို့ဟာ', 'သူမတို့ဟာ', 'ဤအရာ', 'ဟောဒါ', 'ဟောဒီ', 'ဟောဒီဟာ', 'ဒီဟာ', 'ဒါ', 'ထိုအရာ', '၄င်းအရာ', 'ယင်းအရာ', 'အဲဒါ', 'ဟိုဟာ', 'အချို့', 'တစ်ခုခု', 'အဘယ်မဆို', 'ဘယ်အရာမဆို', 'အဘယ်မည်သော', 'အကြင်', 'အရာရာတိုင်း', 'စိုးစဉ်မျှ', 'စိုးစဉ်းမျှ', 'ဘယ်လောက်မဆို', 'တစ်စုံတစ်ရာ', 'တစုံတရာ', 'အလျဉ်းမဟုတ်', 'မည်သည့်နည်းနှင့်မျှမဟုတ်', 'အလျဉ်းမရှိသော', 'အခြားဖြစ်သော', 'အခြားသော', 'အခြားတစ်ခု', 'အခြားတစ်ယောက်', 'အားလုံး', 'အရာရာတိုင်း', 'အကုန်လုံး', 'အလုံးစုံ', 'အရာခပ်သိမ်း', 'တစ်ခုစီ', 'အသီးသီး', 'တစ်ဦးဦး', 'တစ်ခုခု', 'ကိုယ်စီကိုယ်ငှ', 'ကိုယ်စီ', 'တစ်ဦးစီ', 'တစ်ယောက်စီ', 'တစ်ခုစီ', 'အကုန်', 'အပြည့်အစုံ', 'လုံးလုံး', 'နှစ်ခုလုံး', 'နှစ်ယောက်လုံး', 'နှစ်ဘက်လုံး', 'တစ်စုံတစ်ရာ', 'တစ်စုံတစ်ခု', 'တစုံတခု', 'တစ်စုံတစ်ယောက်', 'တစုံတယောက်', 'တစ်ယောက်ယောက်', 'မည်သူမဆို', 'ဘာမျှမရှိ', 'ဘာမှမရှိ', 'အဘယ်အရာမျှမရှိ', 'လူတိုင်း', 'လူတကာ', 'နှင့်', 'ပြီးလျှင်', '၄င်းနောက်', 'သို့မဟုတ်', 'သို့တည်းမဟုတ်', 'သို့မဟုတ်လျှင်', 'ဒါမှမဟုတ်', 'ဖြစ်စေ', 'သို့စေကာမူ', 'ဒါပေမယ့်', 'ဒါပေမဲ့', 'မှတစ်ပါး', 'မှလွဲလျှင်', 'အဘယ်ကြောင့်ဆိုသော်', 'သောကြောင့်', 'သဖြင့်', '၍', 'သည့်အတွက်ကြောင့်', 'လျှင်', 'ပါက', 'အကယ်၍', 'သော်ငြားလည်း', 'စေကာမူ', 'နည်းတူ', 'ပေမယ့်', 'ပေမဲ့', 'ထိုနည်းတူစွာ', 'ထိုနည်းတူ', 'ကဲ့သို့', 'သကဲ့သို့', 'ယင်းကဲ့သို့', 'ထိုကဲ့သို့', 'နှင့်စပ်လျဉ်း၍', 'ဤမျှ', 'ဤမျှလောက်', 'ဤကဲ့သို့', 'အခုလောက်ထိ', 'ဒါကတော့', 'အဘယ်ကဲ့သလို့', 'မည်ကဲ့သို့', 'မည်သည့်နည်းနှင့်', 'မည်သည့်နည်းဖြင့်', 'မည်သည့်နည့်နှင့်မဆို', 'မည်သည့်နည်းဖြင့်မဆို', 'မည်သို့', 'ဘယ်လိုလဲ', 'သို့ပေတည့်', 'သို့ပေမည့်', 'ဘယ်နည်းနှင့်', 'မည်ရွေ့မည်မျှ', 'အဘယ်မျှလောက်', 'ဘယ်လောက်', 'မည်သူ', 'ဘယ်သူ', 'မည်သည့်အကြောင်းကြောင့်', 'ဘာအတွက်ကြောင့်', 'အဘယ်ကြောင့်', 'မည်သည့်အတွက်ကြောင့်', 'ဘာကြောင့်', 'ဘာအတွက်နဲ့လဲ', 'မည်သည်', 'ဘာလဲ', 'အဘယ်အရာနည်း', 'မည်သည့်အရပ်မှာ', 'ဘယ်နေရာတွင်', 'မည်သည့်နေရာတွင်', 'မည်သည့်နေရာသို့', 'ဘယ်နေရာသို့', 'ဘယ်နေရာမှာ', 'ဘယ်သူ၏', 'မည်သည့်အရာ၏', 'မည်သည့်အခါ', 'ဘယ်အချိန်', 'ဘယ်အခါ', 'မည်သည့်အချိန်', 'ဘယ်တော့', 'မည်သူကို', 'မည်သူက', 'ဘယ်သူ့ကို', 'မည်သူမည်ဝါ', 'မည်သည့်အရာ', 'ဘယ်အရာ', 'မည်သို့ပင်ဖြစ်စေ', 'ဘယ်လိုပဲဖြစ်ဖြစ်', 'မည်ရွေ့မည်မျှဖြစ်စေ', 'မည်သည့်နည်းနှင့်မဆို', 'ဘယ်နည်းနဲ့ဖြစ်ဖြစ်', 'မည်သူမဆို', 'ဘယ်သူမဆို', 'အဘယ်သူမဆို', 'မည်သည့်အရာမဆို', 'ဘာဖြစ်ဖြစ်', 'မည်သည့်အရာဖြစ်ဖြစ်', 'မည်သည့်အရပ်၌မဆို', 'မည်သည့်နေရာမဆို', 'ဘယ်အခါမဆို', 'ဘယ်အချိန်မဆို', 'ဘယ်အခါဖြစ်ဖြစ်', 'အချိန်အခါမရွေး']

'''
Copyright (c) 2014, Kristoffer Brabrand

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

nob = ['og', 'i', 'jeg', 'det', 'at', 'en', 'et', 'den', 'til', 'er', 'som', 'på', 'de', 'med', 'han', 'av', 'ikke', 'der', 'så', 'var', 'meg', 'seg', 'men', 'ett', 'har', 'om', 'vi', 'min', 'mitt', 'ha', 'hadde', 'hun', 'nå', 'over', 'da', 'ved', 'fra', 'du', 'ut', 'sin', 'dem', 'oss', 'opp', 'man', 'kan', 'hans', 'hvor', 'eller', 'hva', 'skal', 'selv', 'sjøl', 'her', 'alle', 'vil', 'bli', 'ble', 'blitt', 'kunne', 'inn', 'når', 'kom', 'noen', 'noe', 'ville', 'dere', 'som', 'deres', 'kun', 'ja', 'etter', 'ned', 'skulle', 'denne', 'for', 'deg', 'si', 'sine', 'sitt', 'mot', 'å', 'meget', 'hvorfor', 'dette', 'disse', 'uten', 'hvordan', 'ingen', 'din', 'ditt', 'blir', 'samme', 'hvilken', 'hvilke', 'sånn', 'inni', 'mellom', 'vår', 'hver', 'hvem', 'vors', 'hvis', 'både', 'bare', 'enn', 'fordi', 'før', 'mange', 'også', 'slik', 'vært', 'være', 'begge', 'siden', 'henne', 'hennar', 'hennes']

''' The MIT License (MIT)
Copyright (c) 2018-20 Espen Klem

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

''' This list is frequency sorted. That means it can be sliced from the bottom
and be less agressive in excluding stopwords '''

panGu = ['ਦੇ', 'ਵਿੱਚ', 'ਦਾ', 'ਅਤੇ', 'ਦੀ', 'ਇੱਕ', 'ਨੂੰ', 'ਹੈ', 'ਤੋਂ', 'ਇਸ', 'ਇਹ', 'ਨੇ', 'ਤੇ', 'ਨਾਲ', 'ਲਈ', 'ਵੀ', 'ਸੀ', 'ਵਿਚ', 'ਕਿ', 'ਜੋ', 'ਉਹ', 'ਉਸ', 'ਹਨ', 'ਜਾਂਦਾ', 'ਕੀਤਾ', 'ਗਿਆ', 'ਹੀ', 'ਕੇ', 'ਜਾਂ', 'ਦੀਆਂ', 'ਜਿਸ', 'ਕਰਨ', 'ਹੋ', 'ਕਰ', 'ਆਪਣੇ', 'ਕੀਤੀ', 'ਤੌਰ', 'ਬਾਅਦ', 'ਨਹੀਂ', 'ਭਾਰਤੀ', 'ਪਿੰਡ', 'ਸਿੰਘ', 'ਉੱਤੇ', 'ਸਾਲ', '।', 'ਪੰਜਾਬ', 'ਸਭ', 'ਭਾਰਤ', 'ਉਨ੍ਹਾਂ', 'ਹੁੰਦਾ', 'ਤੱਕ', 'ਇਕ', 'ਹੋਇਆ', 'ਜਨਮ', 'ਬਹੁਤ', 'ਪਰ', 'ਦੁਆਰਾ', 'ਰੂਪ', 'ਹੋਰ', 'ਕੰਮ', 'ਆਪਣੀ', 'ਤਾਂ', 'ਸਮੇਂ', 'ਪੰਜਾਬੀ', 'ਗਈ', 'ਦਿੱਤਾ', 'ਦੋ', 'ਕਿਸੇ', 'ਕਈ', 'ਜਾ', 'ਵਾਲੇ', 'ਸ਼ੁਰੂ', 'ਉਸਨੇ', 'ਕਿਹਾ', 'ਹੋਣ', 'ਲੋਕ', 'ਜਾਂਦੀ', 'ਵਿੱਚੋਂ', 'ਨਾਮ', 'ਜਦੋਂ', 'ਪਹਿਲਾਂ', 'ਕਰਦਾ', 'ਹੁੰਦੀ', 'ਹੋਏ', 'ਸਨ', 'ਵਜੋਂ', 'ਰਾਜ', 'ਮੁੱਖ', 'ਕਰਦੇ', 'ਕੁਝ', 'ਸਾਰੇ', 'ਹੁੰਦੇ', 'ਸ਼ਹਿਰ', 'ਭਾਸ਼ਾ', 'ਹੋਈ', 'ਅਨੁਸਾਰ', 'ਸਕਦਾ', 'ਆਮ', 'ਵੱਖ', 'ਕੋਈ', 'ਵਾਰ', 'ਗਏ', 'ਖੇਤਰ', 'ਜੀ', 'ਕਾਰਨ', 'ਕਰਕੇ', 'ਜਿਵੇਂ', 'ਜ਼ਿਲ੍ਹੇ', 'ਲੋਕਾਂ', 'ਚ', 'ਸਾਹਿਤ', 'ਸਦੀ', 'ਬਾਰੇ', 'ਜਾਂਦੇ', 'ਵਾਲਾ', 'ਜਾਣ', 'ਪਹਿਲੀ', 'ਪ੍ਰਾਪਤ', 'ਰਿਹਾ', 'ਵਾਲੀ', 'ਨਾਂ', 'ਦੌਰਾਨ', 'ਤਰ੍ਹਾਂ', 'ਯੂਨੀਵਰਸਿਟੀ', 'ਨਾ', 'ਏ', 'ਤਿੰਨ', 'ਇਨ੍ਹਾਂ', 'ਗੁਰੂ', 'ਇਸਨੂੰ', 'ਇਹਨਾਂ', 'ਪਿਤਾ', 'ਲਿਆ', 'ਸ਼ਾਮਲ', 'ਸ਼ਬਦ', 'ਅੰਗਰੇਜ਼ੀ', 'ਉਸਨੂੰ', 'ਉਹਨਾਂ', 'ਸਥਿਤ', 'ਫਿਰ', 'ਜੀਵਨ', 'ਸਕੂਲ', 'ਹੁਣ', 'ਦਿਨ', 'ਕੀਤੇ', 'ਆਦਿ', 'ਵੱਧ', 'ਲੈ', 'ਘਰ', 'ਵੱਲ', 'ਦੇਸ਼', 'ਵਲੋਂ', 'ਬਣ', 'ਵੀਂ', 'ਫਿਲਮ', 'ਉਮਰ', 'ਬਲਾਕ', 'ਰਹੇ', 'ਸਾਹਿਬ', 'ਕਰਦੀ', 'ਹਰ', 'ਪੈਦਾ', 'ਘੱਟ', 'ਲੇਖਕ', 'ਹਿੱਸਾ', 'ਫ਼ਿਲਮ', 'ਮੌਤ', 'ਜਿੱਥੇ', 'ਵੱਡਾ', 'ਵਿਖੇ', 'ਆਪਣਾ', 'ਪਹਿਲਾ', 'ਵਰਤੋਂ', 'ਆਪ', 'ਕਰਨਾ', 'ਵਿਆਹ', 'ਰਹੀ', 'ਰਾਹੀਂ', 'ਦਿੱਤੀ', 'ਉਸਦੇ', 'ਪਰਿਵਾਰ', 'ਆ', 'ਦੂਜੇ', 'ਅਮਰੀਕਾ', 'ਮੰਨਿਆ', 'ਇਸਦੇ', 'ਈ', 'ਕਾਲਜ', 'ਸਰਕਾਰ', 'ਇੱਥੇ', 'ਪਾਕਿਸਤਾਨ', 'ਸ਼ਾਮਿਲ', 'ਵਿਗਿਆਨ', 'ਉਸਦੀ', 'ਪੇਸ਼', 'ਕਿਉਂਕਿ', 'ਪਹਿਲੇ', 'ਧਰਮ', 'ਮਸ਼ਹੂਰ', 'ਅੰਦਰ', 'ਵਿਚੋਂ', 'ਜਿਨ੍ਹਾਂ', 'ਜਾਣਿਆ', 'ਪਾਣੀ', 'ਇਲਾਵਾ', 'ਅਰਥ', 'ਚਾਰ', 'ਪ੍ਰਸਿੱਧ', 'ਨਾਵਲ', 'ਵੱਡੇ', 'ਵੱਲੋਂ', 'ਕਹਾਣੀ', 'ਵਿਸ਼ਵ', 'ਮੂਲ', 'ਅਮਰੀਕੀ', 'ਸਥਾਨ', 'ਇਤਿਹਾਸ', 'ਕੁੱਝ', 'ਵਿਕਾਸ', 'ਉੱਤਰ', 'ਸਿੱਖਿਆ', 'ਹਿੰਦੀ', 'ਪ੍ਰਮੁੱਖ', 'ਰਚਨਾ', 'ਬਣਾਇਆ', 'ਵਿਸ਼ੇਸ਼', 'ਡਾ', 'ਉੱਪਰ', 'ਪੱਛਮੀ', 'ਦੇਣ', 'ਇਸਦਾ', 'ਸਕਦੇ', 'ਰੱਖਿਆ', 'ਕਵੀ', 'ਦਿੱਲੀ', 'ਵੱਡੀ', 'ਭੂਮਿਕਾ', 'ਸਮਾਜ', 'ਕਾਵਿ', 'ਕੀ', 'ਕੋਲ', 'ਦ', 'ਗੱਲ', 'ਸੰਸਾਰ', 'ਭਾਗ', 'ਆਈ', 'ਦੱਖਣ', 'ਅੱਜ', 'ਸਿੱਖ', 'ਕਹਿੰਦੇ', 'ਸੰਗੀਤ', 'ਕਿਲੋਮੀਟਰ', 'ਜਿਹਨਾਂ', 'ਸਭਾ', 'ਜਿਸਦਾ', 'ਜਨਵਰੀ', 'ਕਵਿਤਾ', 'ਮੈਂਬਰ', 'ਲਿਖਿਆ', 'ਮਾਂ', 'ਕਲਾ', 'ਪੰਜ', 'ਥਾਂ', 'ਹੇਠ', 'ਜਿਆਦਾ', 'ਵਰਤਿਆ', 'ਮਾਰਚ', 'ਡੀ', 'ਅਕਤੂਬਰ', 'ਤਕ', 'ਨਾਟਕ', 'ਬੀ', 'ਖਾਸ', 'ਇਸੇ', 'ਆਧੁਨਿਕ', 'ਅਗਸਤ', 'ਤਿਆਰ', 'ਮਾਤਾ', 'ਬਣਾਉਣ', 'ਨਵੰਬਰ', 'ਵਿਅਕਤੀ', 'ਦੱਖਣੀ', 'ਦਸੰਬਰ', 'ਆਫ', 'ਗੀਤ', 'ਗਿਣਤੀ', 'ਕਾਲ', 'ਖੋਜ', 'ਸਾਲਾਂ', 'ਪੂਰੀ', 'ਸਮਾਂ', 'ਜ਼ਿਆਦਾ', 'ਇਸਦੀ', 'ਸਕਦੀ', 'ਵਿਚਕਾਰ', 'ਰਾਜਧਾਨੀ', 'ਉਸਦਾ', 'ਜੁਲਾਈ', 'ਜੂਨ', 'ਅਧੀਨ', 'ਸਥਾਪਨਾ', 'ਸੇਵਾ', 'ਭਾਵ', 'ਵਰਗ', 'ਛੋਟੇ', 'ਦਿੰਦਾ', 'ਸਮਾਜਿਕ', 'ਹੁੰਦੀਆਂ', 'ਟੀਮ', 'ਔਰਤਾਂ', 'ਅਕਸਰ', 'ਪ੍ਰਕਾਸ਼ਿਤ', 'ਉਰਦੂ', 'ਰੰਗ', 'ਪਾਰਟੀ', 'ਬਣਾ', 'ਪ੍ਰਭਾਵ', 'ਸ਼ੁਰੂਆਤ', 'ਲਗਭਗ', 'ਮਈ', 'ਸਿਰਫ', 'ਨੇੜੇ', 'ਜਿਸਨੂੰ', 'ਹਾਲਾਂਕਿ', 'ਦੂਰ', 'ਸਤੰਬਰ', 'ਕਿਤਾਬ', 'ਕਦੇ', 'ਉੱਤਰੀ', 'ਪ੍ਰਕਾਰ', 'ਇਸਨੇ', 'ਪ੍ਰਦੇਸ਼', 'ਅੱਗੇ', 'ਸੰਯੁਕਤ', 'ਪੜ੍ਹਾਈ', 'ਵਧੇਰੇ', 'ਨਾਲ਼', 'ਮਨੁੱਖ', 'ਬਾਕੀ', 'ਪ੍ਰਧਾਨ', 'ਦੂਜੀ', 'ਕੁੱਲ', 'ਆਫ਼', 'ਅਧਿਐਨ', 'ਰਾਸ਼ਟਰੀ', 'ਪੁੱਤਰ', 'ਅੰਤਰਰਾਸ਼ਟਰੀ', 'ਧਰਤੀ', 'ਕੇਂਦਰ', 'ਦੇਸ਼ਾਂ', 'ਮੱਧ', 'ਜ਼ਿਲ੍ਹਾ', 'ਸਾਰੀਆਂ', 'ਪੱਧਰ', 'ਹੋਵੇ', 'ਜੇ', 'ਭਾਈ', 'ਰਹਿਣ', 'ਪੁਰਸਕਾਰ', 'ਸਭਿਆਚਾਰ', 'ਪਤਾ', 'ਪਾਸੇ', 'ਨਵੇਂ', 'ਕੰਪਨੀ', 'ਬਾਹਰ', 'ਵੇਲੇ', 'ਸੰਨ', 'ਪੂਰਬੀ', 'ਵਿਚਾਰ', 'ਕਾਰਜ', 'ਪੀ', 'ਮਹੱਤਵਪੂਰਨ', 'ਦੁਨੀਆਂ', 'ਧਾਰਮਿਕ', 'ਮਨੁੱਖੀ', 'ਸਮੂਹ', 'ਅਜਿਹੇ', 'ਲਾਲ', 'ਦੂਜਾ', 'ਭਰਾ', 'ਸ੍ਰੀ', 'ਅੰਤ', 'ਜਾਂਦੀਆਂ', 'ਸ਼ਾਹ', 'ਰਹਿੰਦੇ', 'ਮਹਾਨ', 'ਚੀਨ', 'ਮੀਟਰ', 'ਵਰਗੇ', 'ਨਾਲੋਂ', 'ਹਾਸਲ', 'ਕਿਸਮ', 'ਅਜਿਹਾ', 'ਬਣਿਆ', 'ਭਰ', 'ਛੱਡ', 'ਲੈਣ', 'ਹਿੱਸੇ', 'ਟੀ', 'ਲਿਖੇ', 'ਮਿਲ', 'ਮੌਜੂਦ', 'ਦਿੱਤੇ', 'ਵਾਸਤੇ', 'ਵਾਲੀਆਂ', 'ਵਧੀਆ', 'ਰੂਸੀ', 'ਜਾਰੀ', 'ਸਰਕਾਰੀ', 'ਡਿਗਰੀ', 'ਪੱਛਮ', 'ਲੜਾਈ', 'ਭਾਸ਼ਾਵਾਂ', 'ਰਾਜਾ', 'ਜਲੰਧਰ', 'ਹਿੰਦੂ', 'ਔਰਤ', 'ਜੰਗ', 'ਬਾਬਾ', 'ਬੱਚਿਆਂ', 'ਮੰਤਰੀ', 'ਪਟਿਆਲਾ', 'ਵਾਂਗ', 'ਆਉਣ', 'ਭਾਵੇਂ', 'ਕੇਵਲ', 'ਐਸ', 'ਪ੍ਰਾਚੀਨ', 'ਰਹਿੰਦਾ', 'ਬੋਲੀ', 'ਅਵਾਰਡ', 'ਨਗਰ', 'ਖੇਡਾਂ', 'ਫਿਲਮਾਂ', 'ਬੱਚੇ', 'ਕੌਰ', 'ਤੋ', 'ਪ੍ਰਤੀ', 'ਕੁਆਂਟਮ', 'ਅਬਾਦੀ', 'ਪੁਸਤਕ', 'ਐਮ', 'ਰਾਮ', 'ਖੇਤਰਾਂ', 'ਫਰਵਰੀ', 'ਕ੍ਰਿਕਟ', 'ਪੈਂਦਾ', 'ਇਤਿਹਾਸਕ', 'ਲੱਗ', 'ਬ੍ਰਿਟਿਸ਼', 'ਆਇਆ', 'ਮਿਲਦਾ']

'''
Copyright (c) 2011, Chris Umbel
Farsi Stop Words by Fardin Koochaki <me@fardinak.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the 'Software'), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to fdo so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

fas = ['از', 'با', 'به', 'برای', 'و', 'باید', 'شاید', 'اکنون', 'اگر', 'اگرچه', 'الا', 'اما', 'اندر', 'اینکه', 'باری', 'بالعکس', 'بدون', 'بر', 'بلکه', 'بنابراین', 'بی', 'پس', 'تا', 'جز', 'چنانچه', 'چه', 'چون', 'در', 'را', 'روی', 'زیرا', 'سپس', 'غیر', 'که', 'لیکن', 'مانند', 'مثل', 'مگر', 'نه', 'نیز', 'هرچند', 'هم', 'همان', 'وانگهی', 'ولی', 'ولو', 'همانند', 'همچو']

'''
Copyright (c) 2013, Paweł Łaskarzewski

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

# list based on: http:#pl.wikipedia.org/wiki/Wikipedia:Stopwords

pol = ['a', 'aby', 'ach', 'acz', 'aczkolwiek', 'aj', 'albo', 'ale', 'ależ', 'ani', 'aż', 'bardziej', 'bardzo', 'bo', 'bowiem', 'by', 'byli', 'bynajmniej', 'być', 'był', 'była', 'było', 'były', 'będzie', 'będą', 'cali', 'cała', 'cały', 'ci', 'cię', 'ciebie', 'co', 'cokolwiek', 'coś', 'czasami', 'czasem', 'czemu', 'czy', 'czyli', 'daleko', 'dla', 'dlaczego', 'dlatego', 'do', 'dobrze', 'dokąd', 'dość', 'dużo', 'dwa', 'dwaj', 'dwie', 'dwoje', 'dziś', 'dzisiaj', 'gdy', 'gdyby', 'gdyż', 'gdzie', 'gdziekolwiek', 'gdzieś', 'i', 'ich', 'ile', 'im', 'inna', 'inne', 'inny', 'innych', 'iż', 'ja', 'ją', 'jak', 'jakaś', 'jakby', 'jaki', 'jakichś', 'jakie', 'jakiś', 'jakiż', 'jakkolwiek', 'jako', 'jakoś', 'je', 'jeden', 'jedna', 'jedno', 'jednak', 'jednakże', 'jego', 'jej', 'jemu', 'jest', 'jestem', 'jeszcze', 'jeśli', 'jeżeli', 'już', 'ją', 'każdy', 'kiedy', 'kilka', 'kimś', 'kto', 'ktokolwiek', 'ktoś', 'która', 'które', 'którego', 'której', 'który', 'których', 'którym', 'którzy', 'ku', 'lat', 'lecz', 'lub', 'ma', 'mają', 'mało', 'mam', 'mi', 'mimo', 'między', 'mną', 'mnie', 'mogą', 'moi', 'moim', 'moja', 'moje', 'może', 'możliwe', 'można', 'mój', 'mu', 'musi', 'my', 'na', 'nad', 'nam', 'nami', 'nas', 'nasi', 'nasz', 'nasza', 'nasze', 'naszego', 'naszych', 'natomiast', 'natychmiast', 'nawet', 'nią', 'nic', 'nich', 'nie', 'niech', 'niego', 'niej', 'niemu', 'nigdy', 'nim', 'nimi', 'niż', 'no', 'o', 'obok', 'od', 'około', 'on', 'ona', 'one', 'oni', 'ono', 'oraz', 'oto', 'owszem', 'pan', 'pana', 'pani', 'po', 'pod', 'podczas', 'pomimo', 'ponad', 'ponieważ', 'powinien', 'powinna', 'powinni', 'powinno', 'poza', 'prawie', 'przecież', 'przed', 'przede', 'przedtem', 'przez', 'przy', 'roku', 'również', 'sam', 'sama', 'są', 'się', 'skąd', 'sobie', 'sobą', 'sposób', 'swoje', 'ta', 'tak', 'taka', 'taki', 'takie', 'także', 'tam', 'te', 'tego', 'tej', 'temu', 'ten', 'teraz', 'też', 'to', 'tobą', 'tobie', 'toteż', 'trzeba', 'tu', 'tutaj', 'twoi', 'twoim', 'twoja', 'twoje', 'twym', 'twój', 'ty', 'tych', 'tylko', 'tym', 'u', 'w', 'wam', 'wami', 'was', 'wasz', 'zaś', 'wasza', 'wasze', 'we', 'według', 'wiele', 'wielu', 'więc', 'więcej', 'tę', 'wszyscy', 'wszystkich', 'wszystkie', 'wszystkim', 'wszystko', 'wtedy', 'wy', 'właśnie', 'z', 'za', 'zapewne', 'zawsze', 'ze', 'zł', 'znowu', 'znów', 'został', 'żaden', 'żadna', 'żadne', 'żadnych', 'że', 'żeby']

'''
Copyright (c) 2011, Luís Rodrigues

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

por = ['a', 'à', 'ao', 'aos', 'aquela', 'aquelas', 'aquele', 'aqueles', 'aquilo', 'as', 'às', 'até', 'com', 'como', 'da', 'das', 'de', 'dela', 'delas', 'dele', 'deles', 'depois', 'do', 'dos', 'e', 'ela', 'elas', 'ele', 'eles', 'em', 'entre', 'essa', 'essas', 'esse', 'esses', 'esta', 'estas', 'este', 'estes', 'eu', 'isso', 'isto', 'já', 'lhe', 'lhes', 'mais', 'mas', 'me', 'mesmo', 'meu', 'meus', 'minha', 'minhas', 'muito', 'muitos', 'na', 'não', 'nas', 'nem', 'no', 'nos', 'nós', 'nossa', 'nossas', 'nosso', 'nossos', 'num', 'nuns', 'numa', 'numas', 'o', 'os', 'ou', 'para', 'pela', 'pelas', 'pelo', 'pelos', 'por', 'quais', 'qual', 'quando', 'que', 'quem', 'se', 'sem', 'seu', 'seus', 'só', 'sua', 'suas', 'também', 'te', 'teu', 'teus', 'tu', 'tua', 'tuas', 'um', 'uma', 'umas', 'você', 'vocês', 'vos', 'vosso', 'vossos']

'''
Copyright (c) 2017, Micael Levi and Fabrício Rodrigues

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

porBr = ['a', 'à', 'adeus', 'agora', 'aí', 'ainda', 'além', 'algo', 'alguém', 'algum', 'alguma', 'algumas', 'alguns', 'ali', 'ampla', 'amplas', 'amplo', 'amplos', 'ano', 'anos', 'ante', 'antes', 'ao', 'aos', 'apenas', 'apoio', 'após', 'aquela', 'aquelas', 'aquele', 'aqueles', 'aqui', 'aquilo', 'área', 'as', 'às', 'assim', 'até', 'atrás', 'através', 'baixo', 'bastante', 'bem', 'boa', 'boas', 'bom', 'bons', 'breve', 'cá', 'cada', 'catorze', 'cedo', 'cento', 'certamente', 'certeza', 'cima', 'cinco', 'coisa', 'coisas', 'com', 'como', 'conselho', 'contra', 'contudo', 'custa', 'da', 'dá', 'dão', 'daquela', 'daquelas', 'daquele', 'daqueles', 'dar', 'das', 'de', 'debaixo', 'dela', 'delas', 'dele', 'deles', 'demais', 'dentro', 'depois', 'desde', 'dessa', 'dessas', 'desse', 'desses', 'desta', 'destas', 'deste', 'destes', 'deve', 'devem', 'devendo', 'dever', 'deverá', 'deverão', 'deveria', 'deveriam', 'devia', 'deviam', 'dez', 'dezenove', 'dezesseis', 'dezessete', 'dezoito', 'dia', 'diante', 'disse', 'disso', 'disto', 'dito', 'diz', 'dizem', 'dizer', 'do', 'dois', 'dos', 'doze', 'duas', 'dúvida', 'e', 'é', 'ela', 'elas', 'ele', 'eles', 'em', 'embora', 'enquanto', 'entre', 'era', 'eram', 'éramos', 'és', 'essa', 'essas', 'esse', 'esses', 'esta', 'está', 'estamos', 'estão', 'estar', 'estas', 'estás', 'estava', 'estavam', 'estávamos', 'este', 'esteja', 'estejam', 'estejamos', 'estes', 'esteve', 'estive', 'estivemos', 'estiver', 'estivera', 'estiveram', 'estivéramos', 'estiverem', 'estivermos', 'estivesse', 'estivessem', 'estivéssemos', 'estiveste', 'estivestes', 'estou', 'etc', 'eu', 'exemplo', 'faço', 'falta', 'favor', 'faz', 'fazeis', 'fazem', 'fazemos', 'fazendo', 'fazer', 'fazes', 'feita', 'feitas', 'feito', 'feitos', 'fez', 'fim', 'final', 'foi', 'fomos', 'for', 'fora', 'foram', 'fôramos', 'forem', 'forma', 'formos', 'fosse', 'fossem', 'fôssemos', 'foste', 'fostes', 'fui', 'geral', 'grande', 'grandes', 'grupo', 'há', 'haja', 'hajam', 'hajamos', 'hão', 'havemos', 'havia', 'hei', 'hoje', 'hora', 'horas', 'houve', 'houvemos', 'houver', 'houvera', 'houverá', 'houveram', 'houvéramos', 'houverão', 'houverei', 'houverem', 'houveremos', 'houveria', 'houveriam', 'houveríamos', 'houvermos', 'houvesse', 'houvessem', 'houvéssemos', 'isso', 'isto', 'já', 'la', 'lá', 'lado', 'lhe', 'lhes', 'lo', 'local', 'logo', 'longe', 'lugar', 'maior', 'maioria', 'mais', 'mal', 'mas', 'máximo', 'me', 'meio', 'menor', 'menos', 'mês', 'meses', 'mesma', 'mesmas', 'mesmo', 'mesmos', 'meu', 'meus', 'mil', 'minha', 'minhas', 'momento', 'muita', 'muitas', 'muito', 'muitos', 'na', 'nada', 'não', 'naquela', 'naquelas', 'naquele', 'naqueles', 'nas', 'nem', 'nenhum', 'nenhuma', 'nessa', 'nessas', 'nesse', 'nesses', 'nesta', 'nestas', 'neste', 'nestes', 'ninguém', 'nível', 'no', 'noite', 'nome', 'nos', 'nós', 'nossa', 'nossas', 'nosso', 'nossos', 'nova', 'novas', 'nove', 'novo', 'novos', 'num', 'numa', 'número', 'nunca', 'o', 'obra', 'obrigada', 'obrigado', 'oitava', 'oitavo', 'oito', 'onde', 'ontem', 'onze', 'os', 'ou', 'outra', 'outras', 'outro', 'outros', 'para', 'parece', 'parte', 'partir', 'paucas', 'pela', 'pelas', 'pelo', 'pelos', 'pequena', 'pequenas', 'pequeno', 'pequenos', 'per', 'perante', 'perto', 'pode', 'pude', 'pôde', 'podem', 'podendo', 'poder', 'poderia', 'poderiam', 'podia', 'podiam', 'põe', 'põem', 'pois', 'ponto', 'pontos', 'por', 'porém', 'porque', 'porquê', 'posição', 'possível', 'possivelmente', 'posso', 'pouca', 'poucas', 'pouco', 'poucos', 'primeira', 'primeiras', 'primeiro', 'primeiros', 'própria', 'próprias', 'próprio', 'próprios', 'próxima', 'próximas', 'próximo', 'próximos', 'pude', 'puderam', 'quais', 'quáis', 'qual', 'quando', 'quanto', 'quantos', 'quarta', 'quarto', 'quatro', 'que', 'quê', 'quem', 'quer', 'quereis', 'querem', 'queremas', 'queres', 'quero', 'questão', 'quinta', 'quinto', 'quinze', 'relação', 'sabe', 'sabem', 'são', 'se', 'segunda', 'segundo', 'sei', 'seis', 'seja', 'sejam', 'sejamos', 'sem', 'sempre', 'sendo', 'ser', 'será', 'serão', 'serei', 'seremos', 'seria', 'seriam', 'seríamos', 'sete', 'sétima', 'sétimo', 'seu', 'seus', 'sexta', 'sexto', 'si', 'sido', 'sim', 'sistema', 'só', 'sob', 'sobre', 'sois', 'somos', 'sou', 'sua', 'suas', 'tal', 'talvez', 'também', 'tampouco', 'tanta', 'tantas', 'tanto', 'tão', 'tarde', 'te', 'tem', 'tém', 'têm', 'temos', 'tendes', 'tendo', 'tenha', 'tenham', 'tenhamos', 'tenho', 'tens', 'ter', 'terá', 'terão', 'terceira', 'terceiro', 'terei', 'teremos', 'teria', 'teriam', 'teríamos', 'teu', 'teus', 'teve', 'ti', 'tido', 'tinha', 'tinham', 'tínhamos', 'tive', 'tivemos', 'tiver', 'tivera', 'tiveram', 'tivéramos', 'tiverem', 'tivermos', 'tivesse', 'tivessem', 'tivéssemos', 'tiveste', 'tivestes', 'toda', 'todas', 'todavia', 'todo', 'todos', 'trabalho', 'três', 'treze', 'tu', 'tua', 'tuas', 'tudo', 'última', 'últimas', 'último', 'últimos', 'um', 'uma', 'umas', 'uns', 'vai', 'vais', 'vão', 'vários', 'vem', 'vêm', 'vendo', 'vens', 'ver', 'vez', 'vezes', 'viagem', 'vindo', 'vinte', 'vir', 'você', 'vocês', 'vos', 'vós', 'vossa', 'vossas', 'vosso', 'vossos', 'zero']

# Copyright (c) 2017 Peter Graham, contributors. Released under the Apache-2.0 license.

ron = ['acea', 'aceasta', 'această', 'aceea', 'acei', 'aceia', 'acel', 'acela', 'acele', 'acelea', 'acest', 'acesta', 'aceste', 'acestea', 'aceşti', 'aceştia', 'acolo', 'acord', 'acum', 'ai', 'aia', 'aibă', 'aici', 'al', 'ale', 'alea', 'altceva', 'altcineva', 'am', 'ar', 'are', 'asemenea', 'asta', 'astea', 'astăzi', 'asupra', 'au', 'avea', 'avem', 'aveţi', 'azi', 'aş', 'aşadar', 'aţi', 'bine', 'bucur', 'bună', 'ca', 'care', 'caut', 'ce', 'cel', 'ceva', 'chiar', 'cinci', 'cine', 'cineva', 'contra', 'cu', 'cum', 'cumva', 'curând', 'curînd', 'când', 'cât', 'câte', 'câtva', 'câţi', 'cînd', 'cît', 'cîte', 'cîtva', 'cîţi', 'că', 'căci', 'cărei', 'căror', 'cărui', 'către', 'da', 'dacă', 'dar', 'datorită', 'dată', 'dau', 'de', 'deci', 'deja', 'deoarece', 'departe', 'deşi', 'din', 'dinaintea', 'dintr-', 'dintre', 'doi', 'doilea', 'două', 'drept', 'după', 'dă', 'ea', 'ei', 'el', 'ele', 'eram', 'este', 'eu', 'eşti', 'face', 'fata', 'fi', 'fie', 'fiecare', 'fii', 'fim', 'fiu', 'fiţi', 'frumos', 'fără', 'graţie', 'halbă', 'iar', 'ieri', 'la', 'le', 'li', 'lor', 'lui', 'lângă', 'lîngă', 'mai', 'mea', 'mei', 'mele', 'mereu', 'meu', 'mi', 'mie', 'mine', 'mult', 'multă', 'mulţi', 'mulţumesc', 'mâine', 'mîine', 'mă', 'ne', 'nevoie', 'nici', 'nicăieri', 'nimeni', 'nimeri', 'nimic', 'nişte', 'noastre', 'noastră', 'noi', 'noroc', 'nostru', 'nouă', 'noştri', 'nu', 'opt', 'ori', 'oricare', 'orice', 'oricine', 'oricum', 'oricând', 'oricât', 'oricînd', 'oricît', 'oriunde', 'patra', 'patru', 'patrulea', 'pe', 'pentru', 'peste', 'pic', 'poate', 'pot', 'prea', 'prima', 'primul', 'prin', 'printr-', 'puţin', 'puţina', 'puţină', 'până', 'pînă', 'rog', 'sa', 'sale', 'sau', 'se', 'spate', 'spre', 'sub', 'sunt', 'suntem', 'sunteţi', 'sută', 'sînt', 'sîntem', 'sînteţi', 'să', 'săi', 'său', 'ta', 'tale', 'te', 'timp', 'tine', 'toate', 'toată', 'tot', 'totuşi', 'toţi', 'trei', 'treia', 'treilea', 'tu', 'tăi', 'tău', 'un', 'una', 'unde', 'undeva', 'unei', 'uneia', 'unele', 'uneori', 'unii', 'unor', 'unora', 'unu', 'unui', 'unuia', 'unul', 'vi', 'voastre', 'voastră', 'voi', 'vostru', 'vouă', 'voştri', 'vreme', 'vreo', 'vreun', 'vă', 'zece', 'zero', 'zi', 'zice', 'îi', 'îl', 'îmi', 'împotriva', 'în', 'înainte', 'înaintea', 'încotro', 'încât', 'încît', 'între', 'întrucât', 'întrucît', 'îţi', 'ăla', 'ălea', 'ăsta', 'ăstea', 'ăştia', 'şapte', 'şase', 'şi', 'ştiu', 'ţi', 'ţie']

'''
Copyright (c) 2011, Polyakov Vladimir, Chris Umbel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

rus = ['и', 'в', 'во', 'не', 'что', 'он', 'на', 'я', 'с', 'со', 'как', 'а', 'то', 'все', 'она', 'так', 'его', 'но', 'да', 'ты', 'к', 'у', 'же', 'вы', 'за', 'бы', 'по', 'только', 'ее', 'мне', 'было', 'вот', 'от', 'меня', 'еще', 'нет', 'о', 'из', 'ему', 'теперь', 'когда', 'даже', 'ну', 'ли', 'если', 'уже', 'или', 'ни', 'быть', 'был', 'него', 'до', 'вас', 'нибудь', 'уж', 'вам', 'сказал', 'ведь', 'там', 'потом', 'себя', 'ничего', 'ей', 'может', 'они', 'тут', 'где', 'есть', 'надо', 'ней', 'для', 'мы', 'тебя', 'их', 'чем', 'была', 'сам', 'чтоб', 'без', 'будто', 'чего', 'раз', 'тоже', 'себе', 'под', 'будет', 'ж', 'тогда', 'кто', 'этот', 'того', 'потому', 'этого', 'какой', 'совсем', 'ним', 'этом', 'почти', 'мой', 'тем', 'чтобы', 'нее', 'были', 'куда', 'всех', 'никогда', 'сегодня', 'можно', 'при', 'об', 'другой', 'хоть', 'после', 'над', 'больше', 'тот', 'через', 'эти', 'нас', 'про', 'всего', 'них', 'какая', 'много', 'разве', 'эту', 'моя', 'свою', 'этой', 'перед', 'иногда', 'лучше', 'чуть', 'том', 'нельзя', 'такой', 'им', 'более', 'всегда', 'конечно', 'всю', 'между', 'это', 'лишь']

# Copyright (c) 2017 Peter Graham, contributors. Released under the Apache-2.0 license.

slk = ['a', 'aby', 'aj', 'ako', 'aký', 'ale', 'alebo', 'ani', 'avšak', 'ba', 'bez', 'buï', 'cez', 'do', 'ho', 'hoci', 'i', 'ich', 'im', 'ja', 'jeho', 'jej', 'jemu', 'ju', 'k', 'kam', 'kde', 'kedže', 'keï', 'kto', 'ktorý', 'ku', 'lebo', 'ma', 'mi', 'mne', 'mnou', 'mu', 'my', 'mòa', 'môj', 'na', 'nad', 'nami', 'neho', 'nej', 'nemu', 'nich', 'nielen', 'nim', 'no', 'nám', 'nás', 'náš', 'ním', 'o', 'od', 'on', 'ona', 'oni', 'ono', 'ony', 'po', 'pod', 'pre', 'pred', 'pri', 's', 'sa', 'seba', 'sem', 'so', 'svoj', 'taký', 'tam', 'teba', 'tebe', 'tebou', 'tej', 'ten', 'ti', 'tie', 'to', 'toho', 'tomu', 'tou', 'tvoj', 'ty', 'tá', 'tým', 'v', 'vami', 'veï', 'vo', 'vy', 'vám', 'vás', 'váš', 'však', 'z', 'za', 'zo', 'a', 'èi', 'èo', 'èí', 'òom', 'òou', 'òu', 'že']

# Copyright (c) 2017 Peter Graham, contributors. Released under the Apache-2.0 license.

slv = ['a', 'ali', 'april', 'avgust', 'b', 'bi', 'bil', 'bila', 'bile', 'bili', 'bilo', 'biti', 'blizu', 'bo', 'bodo', 'bojo', 'bolj', 'bom', 'bomo', 'boste', 'bova', 'boš', 'brez', 'c', 'cel', 'cela', 'celi', 'celo', 'd', 'da', 'daleč', 'dan', 'danes', 'datum', 'december', 'deset', 'deseta', 'deseti', 'deseto', 'devet', 'deveta', 'deveti', 'deveto', 'do', 'dober', 'dobra', 'dobri', 'dobro', 'dokler', 'dol', 'dolg', 'dolga', 'dolgi', 'dovolj', 'drug', 'druga', 'drugi', 'drugo', 'dva', 'dve', 'e', 'eden', 'en', 'ena', 'ene', 'eni', 'enkrat', 'eno', 'etc.', 'f', 'februar', 'g', 'g.', 'ga', 'ga.', 'gor', 'gospa', 'gospod', 'h', 'halo', 'i', 'idr.', 'ii', 'iii', 'in', 'iv', 'ix', 'iz', 'j', 'januar', 'jaz', 'je', 'ji', 'jih', 'jim', 'jo', 'julij', 'junij', 'jutri', 'k', 'kadarkoli', 'kaj', 'kajti', 'kako', 'kakor', 'kamor', 'kamorkoli', 'kar', 'karkoli', 'katerikoli', 'kdaj', 'kdo', 'kdorkoli', 'ker', 'ki', 'kje', 'kjer', 'kjerkoli', 'ko', 'koder', 'koderkoli', 'koga', 'komu', 'kot', 'kratek', 'kratka', 'kratke', 'kratki', 'l', 'lahka', 'lahke', 'lahki', 'lahko', 'le', 'lep', 'lepa', 'lepe', 'lepi', 'lepo', 'leto', 'm', 'maj', 'majhen', 'majhna', 'majhni', 'malce', 'malo', 'manj', 'marec', 'me', 'med', 'medtem', 'mene', 'mesec', 'mi', 'midva', 'midve', 'mnogo', 'moj', 'moja', 'moje', 'mora', 'morajo', 'moram', 'moramo', 'morate', 'moraš', 'morem', 'mu', 'n', 'na', 'nad', 'naj', 'najina', 'najino', 'najmanj', 'naju', 'največ', 'nam', 'narobe', 'nas', 'nato', 'nazaj', 'naš', 'naša', 'naše', 'ne', 'nedavno', 'nedelja', 'nek', 'neka', 'nekaj', 'nekatere', 'nekateri', 'nekatero', 'nekdo', 'neke', 'nekega', 'neki', 'nekje', 'neko', 'nekoga', 'nekoč', 'ni', 'nikamor', 'nikdar', 'nikjer', 'nikoli', 'nič', 'nje', 'njega', 'njegov', 'njegova', 'njegovo', 'njej', 'njemu', 'njen', 'njena', 'njeno', 'nji', 'njih', 'njihov', 'njihova', 'njihovo', 'njiju', 'njim', 'njo', 'njun', 'njuna', 'njuno', 'no', 'nocoj', 'november', 'npr.', 'o', 'ob', 'oba', 'obe', 'oboje', 'od', 'odprt', 'odprta', 'odprti', 'okoli', 'oktober', 'on', 'onadva', 'one', 'oni', 'onidve', 'osem', 'osma', 'osmi', 'osmo', 'oz.', 'p', 'pa', 'pet', 'peta', 'petek', 'peti', 'peto', 'po', 'pod', 'pogosto', 'poleg', 'poln', 'polna', 'polni', 'polno', 'ponavadi', 'ponedeljek', 'ponovno', 'potem', 'povsod', 'pozdravljen', 'pozdravljeni', 'prav', 'prava', 'prave', 'pravi', 'pravo', 'prazen', 'prazna', 'prazno', 'prbl.', 'precej', 'pred', 'prej', 'preko', 'pri', 'pribl.', 'približno', 'primer', 'pripravljen', 'pripravljena', 'pripravljeni', 'proti', 'prva', 'prvi', 'prvo', 'r', 'ravno', 'redko', 'res', 'reč', 's', 'saj', 'sam', 'sama', 'same', 'sami', 'samo', 'se', 'sebe', 'sebi', 'sedaj', 'sedem', 'sedma', 'sedmi', 'sedmo', 'sem', 'september', 'seveda', 'si', 'sicer', 'skoraj', 'skozi', 'slab', 'smo', 'so', 'sobota', 'spet', 'sreda', 'srednja', 'srednji', 'sta', 'ste', 'stran', 'stvar', 'sva', 't', 'ta', 'tak', 'taka', 'take', 'taki', 'tako', 'takoj', 'tam', 'te', 'tebe', 'tebi', 'tega', 'težak', 'težka', 'težki', 'težko', 'ti', 'tista', 'tiste', 'tisti', 'tisto', 'tj.', 'tja', 'to', 'toda', 'torek', 'tretja', 'tretje', 'tretji', 'tri', 'tu', 'tudi', 'tukaj', 'tvoj', 'tvoja', 'tvoje', 'u', 'v', 'vaju', 'vam', 'vas', 'vaš', 'vaša', 'vaše', 've', 'vedno', 'velik', 'velika', 'veliki', 'veliko', 'vendar', 'ves', 'več', 'vi', 'vidva', 'vii', 'viii', 'visok', 'visoka', 'visoke', 'visoki', 'vsa', 'vsaj', 'vsak', 'vsaka', 'vsakdo', 'vsake', 'vsaki', 'vsakomur', 'vse', 'vsega', 'vsi', 'vso', 'včasih', 'včeraj', 'x', 'z', 'za', 'zadaj', 'zadnji', 'zakaj', 'zaprta', 'zaprti', 'zaprto', 'zdaj', 'zelo', 'zunaj', 'č', 'če', 'često', 'četrta', 'četrtek', 'četrti', 'četrto', 'čez', 'čigav', 'š', 'šest', 'šesta', 'šesti', 'šesto', 'štiri', 'ž', 'že']

''' Copyright 2016 Liam Doherty

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http:#www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

''' This list is frequency sorted. That means it can be sliced from the bottom
and be less agressive in excluding stopwords '''

som = ['oo', 'atabo', 'ay', 'ku', 'waxeey', 'uu', 'lakin', 'si', 'ayuu', 'soo', 'waa', 'ka', 'kasoo', 'kale', 'waxuu', 'ayee', 'ayaa', 'kuu', 'isku', 'ugu', 'jiray', 'dhan', 'dambeestii', 'inuu', 'in', 'jirtay', 'uheestay', 'aad', 'uga', 'hadana', 'timaado', 'timaaday']

''' Copyright 2016 Liam Doherty

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http:#www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

''' This list is frequency sorted. That means it can be sliced from the bottom
and be less agressive in excluding stopwords '''

sot = ['a', 'le', 'o', 'ba', 'ho', 'oa', 'ea', 'ka', 'hae', 'tselane', 'eaba', 'ke', 'hore', 'ha', 'e', 'ne', 're', 'bona', 'me', 'limo', 'tsa', 'haholo', 'la', 'empa', 'ngoanake', 'se', 'moo', 'm\'e', 'bane', 'mo', 'tse', 'sa', 'li', 'ena', 'bina', 'pina', 'hape']

'''
Copyright (c) 2011, David Przybilla, Chris Umbel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

spa = ['a', 'un', 'el', 'ella', 'y', 'sobre', 'de', 'la', 'que', 'en', 'los', 'del', 'se', 'las', 'por', 'un', 'para', 'con', 'no', 'una', 'su', 'al', 'lo', 'como', 'más', 'pero', 'sus', 'le', 'ya', 'o', 'porque', 'cuando', 'muy', 'sin', 'sobre', 'también', 'me', 'hasta', 'donde', 'quien', 'desde', 'nos', 'durante', 'uno', 'ni', 'contra', 'ese', 'eso', 'mí', 'qué', 'otro', 'él', 'cual', 'poco', 'mi', 'tú', 'te', 'ti', 'sí']

'''
Copyright (c) 2016 Liam Doherty

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http:#www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

# This list is frequency sorted. That means it can be sliced from the bottom
# and be less agressive in excluding stopwords '''

swa = ['na', 'ya', 'wa', 'kwa', 'ni', 'za', 'katika', 'la', 'kuwa', 'kama', 'kwamba', 'cha', 'hiyo', 'lakini', 'yake', 'hata', 'wakati', 'hivyo', 'sasa', 'wake', 'au', 'watu', 'hii', 'zaidi', 'vya', 'huo', 'tu', 'kwenye', 'si', 'pia', 'ili', 'moja', 'kila', 'baada', 'ambao', 'ambayo', 'yao', 'wao', 'kuna', 'hilo', 'kutoka', 'kubwa', 'pamoja', 'bila', 'huu', 'hayo', 'sana', 'ndani', 'mkuu', 'hizo', 'kufanya', 'wengi', 'hadi', 'mmoja', 'hili', 'juu', 'kwanza', 'wetu', 'kuhusu', 'baadhi', 'wote', 'yetu', 'hivi', 'kweli', 'mara', 'wengine', 'nini', 'ndiyo', 'zao', 'kati', 'hao', 'hapa', 'kutokana', 'muda', 'habari', 'ambaye', 'wenye', 'nyingine', 'hakuna', 'tena', 'hatua', 'bado', 'nafasi', 'basi', 'kabisa', 'hicho', 'nje', 'huyo', 'vile', 'yote', 'mkubwa', 'alikuwa', 'zote', 'leo', 'haya', 'huko', 'kutoa', 'mwa', 'kiasi', 'hasa', 'nyingi', 'kabla', 'wale', 'chini', 'gani', 'hapo', 'lazima', 'mwingine', 'bali', 'huku', 'zake', 'ilikuwa', 'tofauti', 'kupata', 'mbalimbali', 'pale', 'kusema', 'badala', 'wazi', 'yeye', 'alisema', 'hawa', 'ndio', 'hizi', 'tayari', 'wala', 'muhimu', 'ile', 'mpya', 'ambazo', 'dhidi', 'kwenda', 'sisi', 'kwani', 'jinsi', 'binafsi', 'kutumia', 'mbili', 'mbali', 'kuu', 'mengine', 'mbele', 'namna', 'mengi', 'upande']

'''
Creative Commons – Attribution / ShareAlike 3.0 license
http:#creativecommons.org/licenses/by-sa/3.0/

List based on frequently used words in subtitles in 2012.

Thanks to
opensubtitles.org
https:#invokeit.wordpress.com/frequency-word-lists/#comment-9707
'''

swe = ['jag', 'det', 'är', 'du', 'inte', 'att', 'en', 'och', 'har', 'vi', 'på', 'i', 'för', 'han', 'vad', 'med', 'mig', 'som', 'här', 'om', 'dig', 'var', 'den', 'så', 'till', 'kan', 'de', 'ni', 'ska', 'ett', 'men', 'av', 'vill', 'nu', 'ja', 'nej', 'bara', 'hon', 'hur', 'min', 'där', 'honom', 'kom', 'din', 'då', 'när', 'ha', 'er', 'ta', 'ut', 'får', 'man', 'vara', 'oss', 'dem', 'eller', 'varför', 'alla', 'från', 'upp', 'igen', 'sa', 'hade', 'allt', 'in', 'sig', 'ingen', 'henne', 'vem', 'mitt', 'nåt', 'blir', 'än', 'bli', 'ju', 'två', 'tar', 'hans', 'ditt', 'mina', 'åt', 'väl', 'också', 'nån', 'låt', 'detta', 'va', 'dina', 'dom', 'blev', 'inga', 'sin', 'just', 'många', 'vart', 'vilken', 'ur', 'ens', 'sitt', 'e', 'jo', 'era', 'deras', 'fem', 'sex', 'denna', 'vilket', 'fyra', 'vårt', 'emot', 'tio', 'ert', 'sju', 'åtta', 'nånting', 'ned', 'ers', 'nio', 'mej']

# Copyright (c) 2017 Peter Graham, contributors. Released under the Apache-2.0 license.

tha = ['กล่าว', 'กว่า', 'กัน', 'กับ', 'การ', 'ก็', 'ก่อน', 'ขณะ', 'ขอ', 'ของ', 'ขึ้น', 'คง', 'ครั้ง', 'ความ', 'คือ', 'จะ', 'จัด', 'จาก', 'จึง', 'ช่วง', 'ซึ่ง', 'ดัง', 'ด้วย', 'ด้าน', 'ตั้ง', 'ตั้งแต่', 'ตาม', 'ต่อ', 'ต่าง', 'ต่างๆ', 'ต้อง', 'ถึง', 'ถูก', 'ถ้า', 'ทั้ง', 'ทั้งนี้', 'ทาง', 'ที่', 'ที่สุด', 'ทุก', 'ทํา', 'ทําให้', 'นอกจาก', 'นัก', 'นั้น', 'นี้', 'น่า', 'นํา', 'บาง', 'ผล', 'ผ่าน', 'พบ', 'พร้อม', 'มา', 'มาก', 'มี', 'ยัง', 'รวม', 'ระหว่าง', 'รับ', 'ราย', 'ร่วม', 'ลง', 'วัน', 'ว่า', 'สุด', 'ส่ง', 'ส่วน', 'สําหรับ', 'หนึ่ง', 'หรือ', 'หลัง', 'หลังจาก', 'หลาย', 'หาก', 'อยาก', 'อยู่', 'อย่าง', 'ออก', 'อะไร', 'อาจ', 'อีก', 'เขา', 'เข้า', 'เคย', 'เฉพาะ', 'เช่น', 'เดียว', 'เดียวกัน', 'เนื่องจาก', 'เปิด', 'เปิดเผย', 'เป็น', 'เป็นการ', 'เพราะ', 'เพื่อ', 'เมื่อ', 'เรา', 'เริ่ม', 'เลย', 'เห็น', 'เอง', 'แต่', 'แบบ', 'แรก', 'และ', 'แล้ว', 'แห่ง', 'โดย', 'ใน', 'ให้', 'ได้', 'ไป', 'ไม่', 'ไว้']

''' The MIT License (MIT)

Copyright (c) 2016 Gene Diaz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. '''

tgl = ['akin', 'aking', 'ako', 'alin', 'am', 'amin', 'aming', 'ang', 'ano', 'anumang', 'apat', 'at', 'atin', 'ating', 'ay', 'bababa', 'bago', 'bakit', 'bawat', 'bilang', 'dahil', 'dalawa', 'dapat', 'din', 'dito', 'doon', 'gagawin', 'gayunman', 'ginagawa', 'ginawa', 'ginawang', 'gumawa', 'gusto', 'habang', 'hanggang', 'hindi', 'huwag', 'iba', 'ibaba', 'ibabaw', 'ibig', 'ikaw', 'ilagay', 'ilalim', 'ilan', 'inyong', 'isa', 'isang', 'itaas', 'ito', 'iyo', 'iyon', 'iyong', 'ka', 'kahit', 'kailangan', 'kailanman', 'kami', 'kanila', 'kanilang', 'kanino', 'kanya', 'kanyang', 'kapag', 'kapwa', 'karamihan', 'katiyakan', 'katulad', 'kaya', 'kaysa', 'ko', 'kong', 'kulang', 'kumuha', 'kung', 'laban', 'lahat', 'lamang', 'likod', 'lima', 'maaari', 'maaaring', 'maging', 'mahusay', 'makita', 'marami', 'marapat', 'masyado', 'may', 'mayroon', 'mga', 'minsan', 'mismo', 'mula', 'muli', 'na', 'nabanggit', 'naging', 'nagkaroon', 'nais', 'nakita', 'namin', 'napaka', 'narito', 'nasaan', 'ng', 'ngayon', 'ni', 'nila', 'nilang', 'nito', 'niya', 'niyang', 'noon', 'o', 'pa', 'paano', 'pababa', 'paggawa', 'pagitan', 'pagkakaroon', 'pagkatapos', 'palabas', 'pamamagitan', 'panahon', 'pangalawa', 'para', 'paraan', 'pareho', 'pataas', 'pero', 'pumunta', 'pumupunta', 'sa', 'saan', 'sabi', 'sabihin', 'sarili', 'sila', 'sino', 'siya', 'tatlo', 'tayo', 'tulad', 'tungkol', 'una', 'walang']

# Copyright (c) 2017 Peter Graham, contributors. Released under the Apache-2.0 license.

tur = ['acaba', 'acep', 'adeta', 'altmış', 'altmış', 'altı', 'altı', 'ama', 'ancak', 'arada', 'artık', 'aslında', 'aynen', 'ayrıca', 'az', 'bana', 'bari', 'bazen', 'bazı', 'bazı', 'başka', 'belki', 'ben', 'benden', 'beni', 'benim', 'beri', 'beş', 'beş', 'beş', 'bile', 'bin', 'bir', 'biraz', 'biri', 'birkaç', 'birkez', 'birçok', 'birşey', 'birşeyi', 'birşey', 'birşeyi', 'birşey', 'biz', 'bizden', 'bize', 'bizi', 'bizim', 'bu', 'buna', 'bunda', 'bundan', 'bunlar', 'bunları', 'bunların', 'bunu', 'bunun', 'burada', 'böyle', 'böylece', 'bütün', 'da', 'daha', 'dahi', 'dahil', 'daima', 'dair', 'dayanarak', 'de', 'defa', 'deđil', 'değil', 'diye', 'diđer', 'diğer', 'doksan', 'dokuz', 'dolayı', 'dolayısıyla', 'dört', 'edecek', 'eden', 'ederek', 'edilecek', 'ediliyor', 'edilmesi', 'ediyor', 'elli', 'en', 'etmesi', 'etti', 'ettiği', 'ettiğini', 'eđer', 'eğer', 'fakat', 'gibi', 'göre', 'halbuki', 'halen', 'hangi', 'hani', 'hariç', 'hatta', 'hele', 'hem', 'henüz', 'hep', 'hepsi', 'her', 'herhangi', 'herkes', 'herkesin', 'hiç', 'hiçbir', 'iken', 'iki', 'ila', 'ile', 'ilgili', 'ilk', 'illa', 'ise', 'itibaren', 'itibariyle', 'iyi', 'iyice', 'için', 'işte', 'işte', 'kadar', 'kanımca', 'karşın', 'katrilyon', 'kendi', 'kendilerine', 'kendini', 'kendisi', 'kendisine', 'kendisini', 'kere', 'kez', 'keşke', 'ki', 'kim', 'kimden', 'kime', 'kimi', 'kimse', 'kırk', 'kısaca', 'kırk', 'lakin', 'madem', 'međer', 'milyar', 'milyon', 'mu', 'mü', 'mı', 'mı', 'nasıl', 'nasıl', 'ne', 'neden', 'nedenle', 'nerde', 'nere', 'nerede', 'nereye', 'nitekim', 'niye', 'niçin', 'o', 'olan', 'olarak', 'oldu', 'olduklarını', 'olduğu', 'olduğunu', 'olmadı', 'olmadığı', 'olmak', 'olması', 'olmayan', 'olmaz', 'olsa', 'olsun', 'olup', 'olur', 'olursa', 'oluyor', 'on', 'ona', 'ondan', 'onlar', 'onlardan', 'onlari', 'onların', 'onları', 'onların', 'onu', 'onun', 'otuz', 'oysa', 'pek', 'rağmen', 'sadece', 'sanki', 'sekiz', 'seksen', 'sen', 'senden', 'seni', 'senin', 'siz', 'sizden', 'sizi', 'sizin', 'sonra', 'tarafından', 'trilyon', 'tüm', 'var', 'vardı', 've', 'veya', 'veyahut', 'ya', 'yahut', 'yani', 'yapacak', 'yapmak', 'yaptı', 'yaptıkları', 'yaptığı', 'yaptığını', 'yapılan', 'yapılması', 'yapıyor', 'yedi', 'yerine', 'yetmiş', 'yetmiş', 'yetmiş', 'yine', 'yirmi', 'yoksa', 'yüz', 'zaten', 'çok', 'çünkü', 'öyle', 'üzere', 'üç', 'şey', 'şeyden', 'şeyi', 'şeyler', 'şu', 'şuna', 'şunda', 'şundan', 'şunu', 'şey', 'şeyden', 'şeyi', 'şeyler', 'şu', 'şuna', 'şunda', 'şundan', 'şunları', 'şunu', 'şöyle', 'şayet', 'şimdi', 'şu', 'şöyle']

''' The MIT License (MIT)

Copyright (c) 2016 Gene Diaz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. '''

ukr = ['авжеж', 'адже', 'але', 'б', 'без', 'був', 'була', 'були', 'було', 'бути', 'більш', 'вам', 'вас', 'весь', 'вздовж', 'ви', 'вниз', 'внизу', 'вона', 'вони', 'воно', 'все', 'всередині', 'всіх', 'від', 'він', 'да', 'давай', 'давати', 'де', 'дещо', 'для', 'до', 'з', 'завжди', 'замість', 'й', 'коли', 'ледве', 'майже', 'ми', 'навколо', 'навіть', 'нам', 'от', 'отже', 'отож', 'поза', 'про', 'під', 'та', 'так', 'такий', 'також', 'те', 'ти', 'тобто', 'тож', 'тощо', 'хоча', 'це', 'цей', 'чи', 'чого', 'що', 'як', 'який', 'якої', 'є', 'із', 'інших', 'їх', 'її']

''' The MIT License (MIT)

Copyright (c) 2016 Gene Diaz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. '''

urd = ['آئی', 'آئے', 'آج', 'آخر', 'آخرکبر', 'آدهی', 'آًب', 'آٹھ', 'آیب', 'اة', 'اخبزت', 'اختتبم', 'ادھر', 'ارد', 'اردگرد', 'ارکبى', 'اش', 'اضتعوبل', 'اضتعوبلات', 'اضطرذ', 'اضکب', 'اضکی', 'اضکے', 'اطراف', 'اغیب', 'افراد', 'الگ', 'اور', 'اوًچب', 'اوًچبئی', 'اوًچی', 'اوًچے', 'اى', 'اً', 'اًذر', 'اًہیں', 'اٹھبًب', 'اپٌب', 'اپٌے', 'اچھب', 'اچھی', 'اچھے', 'اکثر', 'اکٹھب', 'اکٹھی', 'اکٹھے', 'اکیلا', 'اکیلی', 'اکیلے', 'اگرچہ', 'اہن', 'ایطے', 'ایک', 'ب', 'ت', 'تبزٍ', 'تت', 'تر', 'ترتیت', 'تریي', 'تعذاد', 'تن', 'تو', 'توبم', 'توہی', 'توہیں', 'تٌہب', 'تک', 'تھب', 'تھوڑا', 'تھوڑی', 'تھوڑے', 'تھی', 'تھے', 'تیي', 'ثب', 'ثبئیں', 'ثبترتیت', 'ثبری', 'ثبرے', 'ثبعث', 'ثبلا', 'ثبلترتیت', 'ثبہر', 'ثدبئے', 'ثرآں', 'ثراں', 'ثرش', 'ثعذ', 'ثغیر', 'ثلٌذ', 'ثلٌذوثبلا', 'ثلکہ', 'ثي', 'ثٌب', 'ثٌبرہب', 'ثٌبرہی', 'ثٌبرہے', 'ثٌبًب', 'ثٌذ', 'ثٌذکرو', 'ثٌذکرًب', 'ثٌذی', 'ثڑا', 'ثڑوں', 'ثڑی', 'ثڑے', 'ثھر', 'ثھرا', 'ثھراہوا', 'ثھرپور', 'ثھی', 'ثہت', 'ثہتر', 'ثہتری', 'ثہتریي', 'ثیچ', 'ج', 'خب', 'خبرہب', 'خبرہی', 'خبرہے', 'خبهوظ', 'خبًب', 'خبًتب', 'خبًتی', 'خبًتے', 'خبًٌب', 'خت', 'ختن', 'خجکہ', 'خص', 'خططرذ', 'خلذی', 'خو', 'خواى', 'خوًہی', 'خوکہ', 'خٌبة', 'خگہ', 'خگہوں', 'خگہیں', 'خیطب', 'خیطبکہ', 'در', 'درخبت', 'درخہ', 'درخے', 'درزقیقت', 'درضت', 'دش', 'دفعہ', 'دلچطپ', 'دلچطپی', 'دلچطپیبں', 'دو', 'دور', 'دوراى', 'دوضرا', 'دوضروں', 'دوضری', 'دوضرے', 'دوًوں', 'دکھبئیں', 'دکھبتب', 'دکھبتی', 'دکھبتے', 'دکھبو', 'دکھبًب', 'دکھبیب', 'دی', 'دیب', 'دیتب', 'دیتی', 'دیتے', 'دیر', 'دیٌب', 'دیکھو', 'دیکھٌب', 'دیکھی', 'دیکھیں', 'دے', 'ر', 'راضتوں', 'راضتہ', 'راضتے', 'رریعہ', 'رریعے', 'رکي', 'رکھ', 'رکھب', 'رکھتب', 'رکھتبہوں', 'رکھتی', 'رکھتے', 'رکھی', 'رکھے', 'رہب', 'رہی', 'رہے', 'ز', 'زبصل', 'زبضر', 'زبل', 'زبلات', 'زبلیہ', 'زصوں', 'زصہ', 'زصے', 'زقبئق', 'زقیتیں', 'زقیقت', 'زکن', 'زکویہ', 'زیبدٍ', 'صبف', 'صسیر', 'صفر', 'صورت', 'صورتسبل', 'صورتوں', 'صورتیں', 'ض', 'ضبت', 'ضبتھ', 'ضبدٍ', 'ضبرا', 'ضبرے', 'ضبل', 'ضبلوں', 'ضت', 'ضرور', 'ضرورت', 'ضروری', 'ضلطلہ', 'ضوچ', 'ضوچب', 'ضوچتب', 'ضوچتی', 'ضوچتے', 'ضوچو', 'ضوچٌب', 'ضوچی', 'ضوچیں', 'ضکب', 'ضکتب', 'ضکتی', 'ضکتے', 'ضکٌب', 'ضکی', 'ضکے', 'ضیذھب', 'ضیذھی', 'ضیذھے', 'ضیکٌڈ', 'ضے', 'طرف', 'طریق', 'طریقوں', 'طریقہ', 'طریقے', 'طور', 'طورپر', 'ظبہر', 'ع', 'عذد', 'عظین', 'علاقوں', 'علاقہ', 'علاقے', 'علاوٍ', 'عووهی', 'غبیذ', 'غخص', 'غذ', 'غروع', 'غروعبت', 'غے', 'فرد', 'فی', 'ق', 'قجل', 'قجیلہ', 'قطن', 'لئے', 'لا', 'لازهی', 'لو', 'لوجب', 'لوجی', 'لوجے', 'لوسبت', 'لوسہ', 'لوگ', 'لوگوں', 'لڑکپي', 'لگتب', 'لگتی', 'لگتے', 'لگٌب', 'لگی', 'لگیں', 'لگے', 'لی', 'لیب', 'لیٌب', 'لیں', 'لے', 'ه', 'هتعلق', 'هختلف', 'هسترم', 'هسترهہ', 'هسطوش', 'هسیذ', 'هطئلہ', 'هطئلے', 'هطبئل', 'هطتعول', 'هطلق', 'هعلوم', 'هػتول', 'هلا', 'هوکي', 'هوکٌبت', 'هوکٌہ', 'هٌبضت', 'هڑا', 'هڑًب', 'هڑے', 'هکول', 'هگر', 'هہرثبى', 'هیرا', 'هیری', 'هیرے', 'هیں', 'و', 'وار', 'والے', 'وٍ', 'ًئی', 'ًئے', 'ًب', 'ًبپطٌذ', 'ًبگسیر', 'ًطجت', 'ًقطہ', 'ًو', 'ًوخواى', 'ًکبلٌب', 'ًکتہ', 'ًہ', 'ًہیں', 'ًیب', 'ًے', 'ٓ آش', 'ٹھیک', 'پبئے', 'پبش', 'پبًب', 'پبًچ', 'پر', 'پراًب', 'پطٌذ', 'پل', 'پورا', 'پوچھب', 'پوچھتب', 'پوچھتی', 'پوچھتے', 'پوچھو', 'پوچھوں', 'پوچھٌب', 'پوچھیں', 'پچھلا', 'پھر', 'پہلا', 'پہلی', 'پہلےضی', 'پہلےضے', 'پہلےضےہی', 'پیع', 'چبر', 'چبہب', 'چبہٌب', 'چبہے', 'چلا', 'چلو', 'چلیں', 'چلے', 'چکب', 'چکی', 'چکیں', 'چکے', 'چھوٹب', 'چھوٹوں', 'چھوٹی', 'چھوٹے', 'چھہ', 'چیسیں', 'ڈھوًڈا', 'ڈھوًڈلیب', 'ڈھوًڈو', 'ڈھوًڈًب', 'ڈھوًڈی', 'ڈھوًڈیں', 'ک', 'کئی', 'کئے', 'کب', 'کبفی', 'کبم', 'کت', 'کجھی', 'کرا', 'کرتب', 'کرتبہوں', 'کرتی', 'کرتے', 'کرتےہو', 'کررہب', 'کررہی', 'کررہے', 'کرو', 'کرًب', 'کریں', 'کرے', 'کطی', 'کل', 'کن', 'کوئی', 'کوتر', 'کورا', 'کوروں', 'کورٍ', 'کورے', 'کوطي', 'کوى', 'کوًطب', 'کوًطی', 'کوًطے', 'کھولا', 'کھولو', 'کھولٌب', 'کھولی', 'کھولیں', 'کھولے', 'کہ', 'کہب', 'کہتب', 'کہتی', 'کہتے', 'کہو', 'کہوں', 'کہٌب', 'کہی', 'کہیں', 'کہے', 'کی', 'کیب', 'کیطب', 'کیطرف', 'کیطے', 'کیلئے', 'کیوًکہ', 'کیوں', 'کیے', 'کے', 'کےثعذ', 'کےرریعے', 'گئی', 'گئے', 'گب', 'گرد', 'گروٍ', 'گروپ', 'گروہوں', 'گٌتی', 'گی', 'گیب', 'گے', 'ہر', 'ہن', 'ہو', 'ہوئی', 'ہوئے', 'ہوا', 'ہوبرا', 'ہوبری', 'ہوبرے', 'ہوتب', 'ہوتی', 'ہوتے', 'ہورہب', 'ہورہی', 'ہورہے', 'ہوضکتب', 'ہوضکتی', 'ہوضکتے', 'ہوًب', 'ہوًی', 'ہوًے', 'ہوچکب', 'ہوچکی', 'ہوچکے', 'ہوگئی', 'ہوگئے', 'ہوگیب', 'ہوں', 'ہی', 'ہیں', 'ہے', 'ی', 'یقیٌی', 'یہ', 'یہبں']

'''
Copyright (c) 2011, David Przybilla, Chris Umbel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

vie = ['bị', 'bởi', 'cả', 'các', 'cái', 'cần', 'càng', 'chỉ', 'chiếc', 'cho', 'chứ', 'chưa', 'chuyện', 'có', 'có thể', 'cứ', 'của', 'cùng', 'cũng', 'đã', 'đang', 'để', 'đến nỗi', 'đều', 'điều', 'do', 'đó', 'được', 'dưới', 'gì', 'khi', 'không', 'là', 'lại', 'lên', 'lúc', 'mà', 'mỗi', 'một cách', 'này', 'nên', 'nếu', 'ngay', 'nhiều', 'như', 'nhưng', 'những', 'nơi', 'nữa', 'phải', 'qua', 'ra', 'rằng', 'rất', 'rồi', 'sau', 'sẽ', 'so', 'sự', 'tại', 'theo', 'thì', 'trên', 'trước', 'từ', 'từng', 'và', 'vẫn', 'vào', 'vậy', 'vì', 'việc', 'với', 'vừa', 'vâng', 'à', 'ừ', 'từ']

''' Copyright 2016 Liam Doherty

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http:#www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

''' This list is frequency sorted. That means it can be sliced from the bottom
and be less agressive in excluding stopwords '''

yor = ['ó', 'ní', 'ìjàpá', 'ṣe', 'rẹ̀', 'tí', 'àwọn', 'sí', 'ni', 'náà', 'anansi', 'láti', 'kan', 'ti', 'ń', 'lọ', 'o', 'bí', 'padà', 'sì', 'wá', 'wangari', 'lè', 'wà', 'kí', 'púpọ̀', 'odò', 'mi', 'wọ́n', 'pẹ̀lú', 'a', 'ṣùgbọ́n', 'fún', 'jẹ́', 'fẹ́', 'oúnjẹ', 'rí', 'igi', 'kò', 'ilé', 'jù', 'olóńgbò', 'pé', 'é', 'gbogbo', 'iṣu', 'inú', 'bẹ̀rẹ̀', 'jẹ', 'fi', 'dúró', 'alẹ́', 'ọjọ́', 'nítorí', 'nǹkan', 'ọ̀rẹ́', 'àkókò', 'sínú', 'ṣ', 'yìí']

''' Copyright 2016 Liam Doherty

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http:#www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

''' This list is frequency sorted. That means it can be sliced from the bottom
and be less agressive in excluding stopwords '''

zul = ['ukuthi', 'kodwa', 'futhi', 'kakhulu', 'wakhe', 'kusho', 'uma', 'wathi', 'umama', 'kanye', 'phansi', 'ngesikhathi', 'lapho', 'u', 'zakhe', 'khona', 'ukuba', 'nje', 'phezulu', 'yakhe', 'kungani', 'wase', 'la', 'mina', 'wami', 'ukuze', 'unonkungu', 'wabona', 'wahamba', 'lakhe', 'yami', 'kanjani', 'kwakukhona', 'ngelinye']

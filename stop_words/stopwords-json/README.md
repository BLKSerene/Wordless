# stopwords-json [![Build Status](https://travis-ci.org/6/stopwords-json.svg?branch=travis)](https://travis-ci.org/6/stopwords-json) [![npm](https://img.shields.io/npm/v/stopwords-json.svg?maxAge=3600)](https://www.npmjs.com/package/stopwords-json) [![Bower](https://img.shields.io/bower/v/stopwords-json.svg?maxAge=3600)](https://bower.io/)

Stopwords for various languages in JSON format. Per [Wikipedia](http://en.wikipedia.org/wiki/Stop_words):

> Stop words are words which are filtered out prior to, or after, processing of natural language data [...] these are some of the most common, short function words, such as *the*, *is*, *at*, *which*, and *on*.

You can use all stopwords with [stopwords-all.json](stopwords-all.json) (keyed by language ISO 639-1 code), or see the below table for individual language stopword files.

## Languages
There are a total of 50 supported languages:

Language | Stopword count | Filename
--- | --- | ---
Afrikaans | 51 | [af.json](dist/af.json)
Arabic | 162 | [ar.json](dist/ar.json)
Armenian | 45 | [hy.json](dist/hy.json)
Basque | 98 | [eu.json](dist/eu.json)
Bengali | 116 | [bn.json](dist/bn.json)
Breton | 126 | [br.json](dist/br.json)
Bulgarian | 259 | [bg.json](dist/bg.json)
Catalan | 218 | [ca.json](dist/ca.json)
Chinese | 542 | [zh.json](dist/zh.json)
Croatian | 179 | [hr.json](dist/hr.json)
Czech | 346 | [cs.json](dist/cs.json)
Danish | 101 | [da.json](dist/da.json)
Dutch | 275 | [nl.json](dist/nl.json)
English | 570 | [en.json](dist/en.json)
Esperanto | 173 | [eo.json](dist/eo.json)
Estonian | 35 | [et.json](dist/et.json)
Finnish | 772 | [fi.json](dist/fi.json)
French | 606 | [fr.json](dist/fr.json)
Galician | 160 | [gl.json](dist/gl.json)
German | 596 | [de.json](dist/de.json)
Greek | 75 | [el.json](dist/el.json)
Hausa | 39 | [ha.json](dist/ha.json)
Hebrew | 194 | [he.json](dist/he.json)
Hindi | 225 | [hi.json](dist/hi.json)
Hungarian | 781 | [hu.json](dist/hu.json)
Indonesian | 355 | [id.json](dist/id.json)
Irish | 109 | [ga.json](dist/ga.json)
Italian | 619 | [it.json](dist/it.json)
Japanese | 109 | [ja.json](dist/ja.json)
Korean | 679 | [ko.json](dist/ko.json)
Latin | 49 | [la.json](dist/la.json)
Latvian | 161 | [lv.json](dist/lv.json)
Marathi | 99 | [mr.json](dist/mr.json)
Norwegian | 172 | [no.json](dist/no.json)
Persian | 332 | [fa.json](dist/fa.json)
Polish | 260 | [pl.json](dist/pl.json)
Portuguese | 408 | [pt.json](dist/pt.json)
Romanian | 282 | [ro.json](dist/ro.json)
Russian | 539 | [ru.json](dist/ru.json)
Slovak | 110 | [sk.json](dist/sk.json)
Slovenian | 446 | [sl.json](dist/sl.json)
Somalia | 30 | [so.json](dist/so.json)
Southern Sotho | 31 | [st.json](dist/st.json)
Spanish | 577 | [es.json](dist/es.json)
Swahili | 74 | [sw.json](dist/sw.json)
Swedish | 401 | [sv.json](dist/sv.json)
Thai | 115 | [th.json](dist/th.json)
Turkish | 279 | [tr.json](dist/tr.json)
Yoruba | 60 | [yo.json](dist/yo.json)
Zulu | 29 | [zu.json](dist/zu.json)


## Sources

- [Apache Lucene](http://lucene.apache.org/) - [Apache 2.0 License](http://www.apache.org/licenses/LICENSE-2.0)
- [Carrot2](https://github.com/carrot2/carrot2) - [License](http://project.carrot2.org/license.html)
- [cue.language](https://github.com/vcl/cue.language) - [Apache 2.0 License](https://github.com/vcl/cue.language/blob/master/license.txt)
- [Jacques Savoy](http://members.unine.ch/jacques.savoy/clef/index.html) - BSD License
- SMART Information Retrieval System: ftp://ftp.cs.cornell.edu/pub/smart/
- [ASP Stoplist Project](https://github.com/dohliam/more-stoplists) - CC-BY and Apache 2.0

## License and Copyright
Copyright (c) 2017 Peter Graham, contributors.
Released under the Apache-2.0 license.

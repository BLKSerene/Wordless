# ----------------------------------------------------------------------
# Wordless: Tagsets - Universal POS tags - Nigerian Pidgin
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

# Universal POS Tags: https://universaldependencies.org/pcm/pos/
tagset_mapping = [
    ['ADJ', 'ADJ', 'Adjective', '(Make im no leave) small (chance for us to thank am.), (Na) big (lie.), (Na very) bad (thing.), (Im dey cause) plenty (accident.), (We don check di matter for our) national (headquarters.)'],
    ['ADP', 'ADP', 'Adposition', '(No dey stand) for (middle of road.), (Some) of (una no know.), (Because speed im dey lead) to (accident.), (And im no suppose be) like (dat.), (You dey do two things) at (di same time.), (Im don dey bleed) from (inside.), (Make you continue) wit (your journey.), (Come push you enter) inside (bush.), (Na so di bleed go continue) till (di person go die.), (Im pull) over., After (dey don drink finish.), (And people dey live) under (one illusion.), (You wake) up (di next morning.)'],
    ['ADV', 'ADV', 'Adverb', 'Used to focalize the attention): So (na bad thing.)\nUsed as a marker in the second part of a cleft phrase): (Na only di living) naim (dey celebrate.)'],
    ['AUX', 'AUX', 'Auxiliary', 'No (negative marker): I no know.\nCome (realis mood): But if we come look di matter well.\nDey (continuous aspect): Because as you dey use phone and dey do two thing at di same time.\nDon (perfect aspect): So ma people we don show again as we dey always show.\nFit (similar to modal auxiliary can): Dem fit reach too.\nFor (hypothetical mood): But dis kind thing for no happen o.\nGo (prospective aspect, future): Nobody go ever talk sey rain do bad thing o.\nmake (jussive mood): Make we talk true sef o.'],
    ['CONJ', 'CONJ', 'Coordinating/subordinating conjunction', 'See CCONJ and SCONJ'],
    ['CCONJ', 'CCONJ', 'Coordinating conjunction', '(You dey use phone) and (you dey drive.), (If you want drink and drive drink wata) or (drink coke.), (Some people no go die) but (for di rest of deir life dey no go fit waka again.)'],
    ['SCONJ', 'SCONJ', 'Subordinating conjunction', '(Make im make sure) sey (di brake dey okay.), (because na di vehicule) wey (una dey take move be dis.), (So) if (we catch you make you no vex.), Because (speed im dey lead to accident.), (anoder thing wey i want follow una relate na di attitude of sey make we dey use phone) as (we dey drive.)'],
    ['DET', 'DET', 'Determiner', 'Singular definite article: (Now see) di (process)\nPlural definite article: Dem (no dey send)\nSingular demonstrative pronoun: (na me park) dis (car)\nPlural demonstrative pronoun: (so) dese (kind thing no good)'],
    ['INTJ', 'INTJ', 'Interjection', 'Em (na we FRSC as una know.), Em (na distraction.), See (two lose now.), (Wey come dey check sey) ah ah (ma car na me park dis car.), Mtschew (I go fit go.), (Some people go say dis brak) ah (dis brake dey too go down.), Ehn (one thing one thing.), (So dat you no go go enter) em (mouth of anoder car.)'],
    ['NOUN', 'NOUN', 'Noun', '(Our) work (na to ensure sey) accident (no too happen for) road., (And im dey cause plenty) accident., (And now wey be sey) government (don even come make am easier.), (So make una try comply wit dese) policy., (Make una see sey una put) speed limiter (for una) motor (so dat) speed (go reduce.)'],
    ['PROPN', 'PROPN', 'Proper noun', '(Right now we dey) Ifesinachi (park for) Dugbe (for) Ibadan., (Wey be sey una comot go high) saturday, friday (night go party, go club.), (Im go come reach) Ogere (now.), (Before im reach) Nigeria (di whole sea wata corrosion everything don affect di tire.), (You go enter) Lagos Ibadan (expressway.)'],
    ['NUM', 'NUM', 'Numeral', 'Fifty eight (percent of accident wey im happen for road na overspeeding naim dey cause am.), (Make I give you) one (instance.), (Im daughter fall from) three (storey build for school.)'],
    ['PART', 'PART', 'Particle', 'Copulative particle of focalization\nMarker of cleft clause: Na (our work we dey do.)\nNegation: (and im) no (suppose be like dat.)\n(And make we try drive) to (stay alive.), (we) sha (carry di man comot carry am go hospital.)\nEmphatic marker: (Anyone) o (wey you want do) o (make you do am because time wait for nobody) o.\nEmphasizes the preceding token: (Sotay ground) sef (go soft proper.)'],
    ['PRON', 'PRON', 'Pronoun', 'First-person, singular\n\tPersonal pronoun, subject: I (want drive.)\n\tPersonal pronoun, complement: (Follow) me.\n\tPossessive pronoun: (I go look for one of) ma (boy.)\nSecond-person, singular/plural\n\tPersonal pronoun, subject: You (dey drive.)\n\tPersonal pronoun, complement: (e fit sharply carry) you.\n\tPossessive pronoun: Your (tyre dey very important.)\nThird-person, singular\n\tPersonal pronoun, subject: Im (pick di call.)\n\tPersonal pronoun, complement: (Im go fit help) us.\n\tPossessive determiner: Im (daughter fall from three storey build for school.)\nFirst-person, plural\n\tPersonal pronoun, subject: We (see di man.)\n\tPersonal pronoun, complement: (e fit sharply carry) you.\n\tPossessive pronoun: (We never send) our (pikin go school.)\nThird-person, plural\n\tPersonal pronoun, subject: Dem (dey always talk.)\n\tPersonal pronoun, complement: (Make sure sey you no leave) am.\n\tPossessive determiner: (For di rest of) deir (life.)\nGeneric pronoun\n\t(Make) una (try.)'],
    ['VERB', 'VERB', 'Verb', '(You dey) follow (person talk.), (Make I) give (you one instance.), (Im) dey (very unfortunate.), (Naim im phone just) ring., (We) see (di man.)'],

    ['PUNCT', 'PUNCT', 'Punctuation', 'Period: .\nComma: ,\nParentheses: ()'],
    ['SYM', 'SYM', 'Symbol', '$, %, §, ©\n+, −, ×, ÷, =, <, >\n:), ♥‿♥, 😝'],
    ['X', 'X', 'Other', '(And then he just) xfgh pdl jklw']
]

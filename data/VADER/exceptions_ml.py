NEGATE = ['അല്ല', 'ഒന്നും', 'കഴിയില്ല', 'പറ്റില്ല', 'കഴിഞ്ഞില്ല', 'ധൈര്യശാലി', 'ചെയ്തില്ല', 'ഇല്ല', 'ധൈര്യമില്ല', 'ചെയ്യുന്നില്ല', 'ചെയ്യരുത്', 'ഉണ്ടായിരുന്നില്ല', 'സാധ്യമല്ല', 'നിർബന്ധമില്ല', 'ഒന്നുമില്ല', 'ഇല്ലായിരുന്നു', 'ചെയ്തിട്ടില്ല', 'അല്ലായിരിക്കാം', 'പാടില്ല', 'ആവശ്യമില്ല', 'ഒരിക്കലും', 'ഒരിടത്തുമില്ല', 'ഷാൻ്റ്', 'ഊഹൂ', 'ആയിരുന്നില്ല', 'ഷാനില്ല', 'ഊഹ്-ഉഹ്', 'കൂടാതെ', 'പതിവില്ല', 'ചെയ്യില്ല', 'അപൂർവ്വമായി', 'ഉണ്ടായിരുന്നിട്ടും']
BOOSTER_DICT = {'തികച്ചും': 0.293, 'അത്ഭുതകരമായി': 0.293, 'ഭയങ്കരമായി': 0.293, 'പൂർണ്ണമായും': 0.293, 'ഗണ്യമായ': 0.293, 'ഗണ്യമായി': 0.293, 'നിശ്ചയമായും': 0.293, 'ആഴത്തിൽ': 0.293, 'എഫിംഗ്': 0.293, 'വലിയ': 0.293, 'വളരെയധികം': 0.293, 'പ്രത്യേകിച്ച്': 0.293, 'അസാധാരണമായ': 0.293, 'അസാധാരണമായി': 0.293, 'അങ്ങേയറ്റം': 0.293, 'അതിശയകരമായി': 0.293, 'ഫ്ലിപ്പിംഗ്': 0.293, 'ഫ്ലിപ്പിൻ': 0.293, 'ഫ്രാക്കിൻ': 0.293, 'ഫ്രാക്കിംഗ്': 0.293, 'fricking': 0.293, 'ഫ്രിക്കിൻ': 0.293, 'ഫ്രിഗ്ഗിംഗ്': 0.293, 'ഫ്രിഗ്ഗിൻ': 0.293, 'വിഡ്ഢി': 0.293, 'ഫക്കിംഗ്': 0.293, 'ഫഗ്ഗിൻ': 0.293, 'ഫഗ്ഗിംഗ്': 0.293, 'അത്യന്തം': 0.293, 'ഹല്ല': 0.293, 'വളരെ': 0.293, 'വലിയതോതിൽ': 0.293, 'അവിശ്വസനീയമായ': 0.293, 'അവിശ്വസനീയമാംവിധം': 0.293, 'തീവ്രമായി': 0.293, 'പ്രധാന': 0.293, 'പ്രധാനമായും': 0.293, 'കൂടുതൽ': 0.293, 'ഏറ്റവും': 0.293, 'ശരിക്കും': 0.293, 'ശ്രദ്ധേയമായി': 0.293, 'അങ്ങനെ': 0.293, 'നന്നായി': 0.293, 'ആകെ': 0.293, 'അതിഗംഭീരമായ': 0.293, 'അതിഗംഭീരമായി': 0.293, 'uber': 0.293, 'ഉച്ചരിക്കുക': 0.293, 'ഏതാണ്ട്': -0.293, 'കഷ്ടിച്ച്': -0.293, 'മതി': -0.293, 'ഇത്തരം': -0.293, 'ഒരു': -0.293, 'തരത്തിൽ': -0.293, 'കുറവ്': -0.293, 'അല്പം': -0.293, 'അരികിലുള്ള': -0.293, 'നാമമാത്രമായി': -0.293, 'വല്ലപ്പോഴും': -0.293, 'ഇടയ്ക്കിടെ': -0.293, 'ഭാഗികമായി': -0.293, 'വിരളമാണ്': -0.293, 'വിരളമായി': -0.293, 'നേരിയ': -0.293, 'ചെറുതായി': -0.293, 'പരിധിവരെ': -0.293, 'ഒരുതരം': -0.293, 'തരം': -0.293, 'അടുക്കുക': -0.293, 'തരത്തിലുള്ള': -0.293}
SENTIMENT_LADEN_IDIOMS = {'കടുക് മുറിക്കുക': 2.0, 'കൈ വായിൽ': -2.0, 'തിരികെ കൈ': -2.0, 'പുക ഊതുക': -2.0, 'പുക വീശുന്നു': -2.0, 'മികവ്': 1.0, 'ഒരു കാൽ ഒടിക്കും': 2.0, 'ഗ്യാസ് ഉപയോഗിച്ച് പാചകം': 2.0, 'കറുപ്പിൽ': 2.0, 'ചുവപ്പിൽ': -2.0, 'പന്തിൽ': 2.0, 'കാലാവസ്ഥയ്ക്ക് കീഴിൽ': -2.0}
SPECIAL_CASES = {'ഷിറ്റ്': 3.0, 'ബോംബ്': 3.0, 'ചീത്ത കഴുത': 1.5, 'ദുഷ്ടൻ': 1.5, 'ബസ് സ്റ്റോപ്പ്': 0.0, 'അതെ ശരിയാണ്': -2.0, 'മരണം ചുംബനം': -1.5, 'മരിക്കാൻ': 3.0, 'തുടിക്കുന്ന ഹൃദയം': 3.5}

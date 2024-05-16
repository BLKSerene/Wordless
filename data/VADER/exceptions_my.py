NEGATE = ['မ', 'ဟုတ်', 'ဘူး', 'ရ', 'နိုင်', 'ပါ', '။', 'darent', 'လား', 'ခံဝံ့', 'မလုပ်', 'နဲ့', 'ရှိ', 'ခဲ့', 'မရှိ', 'အားကြီး', 'တယ်', 'ဖြစ်', 'သေး', 'လုပ်', 'လိုအပ်', 'ဘယ်တော့', 'မှ', 'ဘာ', 'ဘယ်', 'နေရာ', 'မှာ', 'သင့်', 'shant', 'အူး', 'အာ့', 'ဘဲ', 'wont', 'သလောက်', 'တော်ရုံ', 'သို့ပေမယ့်']
BOOSTER_DICT = {'လုံးဝ': 0.293, 'အံ့သြ': 0.293, 'လောက်': 0.293, 'အောင်': 0.293, 'ဆိုးဆိုး': 0.293, 'ရွားရွား': 0.293, 'အတော်အတန်': 0.293, 'သိသိသာသာ': 0.293, 'ဆုံးဖြတ်': 0.293, 'နက်နက်': 0.293, 'ရှိုင်းရှိုင်း': 0.293, 'effing': 0.293, 'ကြီးမား': 0.293, 'သည်': -0.293, '။': -0.293, 'အလွန်': 0.293, 'တရာ': 0.293, 'အထူးသဖြင့်': 0.293, 'ခြွင်းချက်': 0.293, 'အစွန်းရောက်': 0.293, 'အမင်း': 0.293, 'ရိုးသားဖြူစင်': 0.293, 'လှန်': 0.293, 'flippin': 0.293, 'ဖရော်ကင်': 0.293, 'fracking': 0.293, 'fricking': 0.293, 'frickin': 0.293, 'frigging': 0.293, 'ဖရီးဂျင်': 0.293, 'အပြည့်အဝ': 0.293, 'fuckin': 0.293, 'fucking': 0.293, 'fuggin': 0.293, 'fugging': 0.293, 'ဟယ်လို': 0.293, 'စွာ': 0.293, 'မယုံနိုင်': 0.293, 'ပြင်းပြင်းထန်ထန်': 0.293, 'အဓိက': 0.293, 'အားဖြင့်': 0.293, 'နောက်ထပ်': 0.293, 'အများဆုံး': 0.293, 'သက်သက်': 0.293, 'အတော်လေး': 0.293, 'တကယ်': 0.293, 'ဒါကြောင့်': 0.293, 'ဟုတ်တိပတ်': 0.293, 'တိ': 0.293, 'နှိုက်နှိုက်': 0.293, 'ချွတ်ချွတ်': 0.293, 'စုစုပေါင်း': 0.293, 'သော': -0.293, 'လွန်စွာ': 0.293, 'uber': 0.293, 'စရာ': 0.293, 'ပုံမှန်': 0.293, 'မ': 0.293, 'ဟုတ်': 0.293, 'မြွက်ဟ': 0.293, 'ရှင်းရှင်း': 0.293, 'အရမ်း': 0.293, 'နီးပါး': -0.293, 'အနိုင်': -0.293, 'နိုင်': -0.293, 'ခဲ': -0.293, 'လုံလောက်': -0.293, 'ပါ': -0.293, 'တယ်': -0.293, 'ကဲ့သို့': -0.293, 'တစ်': -0.293, 'မျိုး': -0.293, 'နည်း': -0.293, 'နည်းနည်း': -0.293, 'မဖြစ်စလောက်': -0.293, 'ဟု': -0.293, 'ဆို': -0.293, 'ရံဖန်': -0.293, 'ရံခါ': -0.293, 'တစ်စိတ်တစ်ပိုင်း': -0.293, 'ရှားပါး': -0.293, 'မရှိ': -0.293, 'သလောက်': -0.293, 'အနည်းငယ်': -0.293, 'အတန်ငယ်': -0.293, 'အမျိုးအစား': -0.293}
SENTIMENT_LADEN_IDIOMS = {'မုန်ညင်း ခုတ်': 2.0, 'လက်မှ ပါးစပ်': -2.0, 'ပြန်ပေး သည် ။': -2.0, 'မီးခိုး မှုတ်': -2.0, 'အထက် လက်': 1.0, 'ခြေထောက်ကွဲ': 2.0, 'ဓာတ်ငွေ့ ဖြင့် ချက်ပြုတ်': 2.0, 'အနက်ရောင် ၌': 2.0, 'အနီရောင် ၌': -2.0, 'ဘောလုံး ပေါ်မှာ': 2.0, 'ရာသီဥတု အောက် မှာ': -2.0}
SPECIAL_CASES = {'ပြော ရ မှာ ပါ ။': 3.0, 'ဗုံး': 3.0, 'ဖင်ဆိုး တယ် ။': 1.5, 'ခွေးဆိုး': 1.5, 'ဘတ်စ်ကား မှတ်တိုင်': 0.0, 'ဟုတ် ပါ တယ် ။': -2.0, 'သေ ခြင်း တရား ၏ အနမ်း': -1.5, 'သေ ရန် အတွက်': 3.0, 'နှလုံး ခုန်': 3.5}

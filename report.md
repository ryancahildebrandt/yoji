# Wisdom in 4 Characters Or Less
#### *Training a neural network to generate 四字熟語 (as best it can!)*

四字熟語 (yoji-jukugo) are 4 character Japanese compunds, some idiomatic and some not. Many are derived from Chinese classical texts, Buddhist scriptures, and folk sayings. But can a computer make new ones? Are they any **_good_**?

---
header

---
## Dataset
The dataset used for the current project was scraped/pulled from the following: 
- [Yojijukugo](http://www.edrdg.org/projects/yojijukugo.html) for idioms and meanings/readings
- [Jamdict](https://github.com/neocl/jamdict) for kanji readings, meanings, and other information
- [Kanji Database](https://www.kanjidatabase.com/) for kanji classification, grade level, and misc characteristics 
*Some of the above will be used for other projects so aren't necessarily fully incorporated into this project*

---
yoji_df

---
## Model
*Adapted from (this)[#https://github.com/RajkumarGalaxy/NLP/blob/master/beginners-guide-to-text-generation-with-rnns.ipynb] example*

Since this is my first solo foray into implementing a ML model, I thought it best to adapt some working code so I could play around, tweak some parameters, and get a sense for how each of the parts work together. The model I adapted is linked just above.

---
### Model Summary

Model: "sequential"
| **Layer (type)**      | **Output Shape** | **Param #** |
|-----------------------|------------------|-------------|
| embedding (Embedding) | (64, None, 64)   | 175744      |
| lstm (LSTM)           | (64, None, 352)  | 587136      |
| dropout (Dropout)     | (64, None, 352)  | 0           |
| lstm_1 (LSTM)         | (64, None, 352)  | 992640      |
| dropout_1 (Dropout)   | (64, None, 352)  | 0           |
| dense (Dense)         | (64, None, 2746) | 969338      |

+ Total params: 2,724,858
+ Trainable params: 2,724,858
+ Non-trainable params: 0

---
## Model Evaluation

Originally I was going to implement a couple different techniques to predict sequences of kanji. I ended up keeping only the above model, as the others I tried were absolutely **dismal** at predicting sequences based on semantic, orthographic, and other characteristics. That probably shouldn't be surprising, since the dataset only has a couple thousand compounds. Of these, plenty were missing meanings and readings, as were a large portion of the individual kanji.
The included sequence model performed a lot better, though that's not to say the sequence model performs *well*; the sparse categorical accuracy generally doesn't get too far beyond 2%. That *is* to say that the model doesn't do a great job of "learning" how to generate realistic idioms, and I for one am ~~not exactly~~ shocked.

---
## Idiom Generation

Using the trained model, we feed it a randomly selected compound as a starting sequence, and generate the next 400 or so characters to get roughly 100 new idioms and filter out any idioms which occur in the original dataset. This output will change every time the code is run, but I saved a copy to crystalize some examples.

---
> ['事膝采中', '倉潮久弓', '拠文町次', '扇不那中', '両近怱分', '子入裂兵', '算休目発', '調知車軽', '面軻漏明', '車行命道', '面思同鳳', '注汰属血', '寝雨麗心', '果者影行', '一気門奇', '虻八食施', '心試縦風', '恩大廉題', '記尚一数', '虫三黄気', '中格況急', '正無気戒', '路作快野', '上有雨模', '遠見満人', '棒里之生', '勉流悪人', '発地者無', '血風之所', '思忍洒厚', '世次術趣', '髪田吉補', '労寸之淡', '如畳踵行', '穴一言言', '実下蓬難', '切多場勢', '一断風雨', '起食山怒', '一用発四', '二索呻馬', '節拝身戦', '下様食作', '赫之志下', '喜人天反', '大己憂満', '蛇落玉水', '類言槍不', '光知伝明', '軌仏明議', '世城不然', '者狼信屨', '得力答憂', '中針鳥本', '曲争首氷', '平之出大', '不察的窮', '書天雨改', '湾山水紫', '境戚代励', '滅釘斉来', '足天常色', '達旦之無', '転意靡一', '不才由明', '扼構之識', '厚閥同令', '不心禽斥', '一復作識', '下然間係', '束基世末', '落民作行', '火端鱗之', '雨根義伐', '業由用淫', '中不旨濁', '知郷発豊', '明思面不', '条友質居', '之嫁山首', '之織子夕', '用人同曲', '迹泥歩刀', '改慢来心', '変兎哮地', '古知順招', '中日説衰', '疎尊頭之', '軽語乙要', '林安過没', '途弁説大', '苦闘力不', '然見致転', '水女倥義', '象刀水事', '無多門主', '退死省雨', '之体扼曲', '線濯政合', '無莱逆文']


---
Once we have the new idioms, we split them up and look up the meaning and reading for each constituent character using the lookup functions from the scrape.py module in the current project. We can also leverage the fact that 2 kanji compounds are not only common in Japanese but also show up plenty in yoji-jukugo to make some of the idioms simpler to interpret. That gives us (most of) what we need to interpret and define some juicy new idioms!

Keep in mind that the sequential model used here doesn't take into account meaning or gramaticality in the output, so making sense of some of these will take... imagination. I've also taken liberties with selecting readings, in some cases opting for a particular on or kun yomi in order to make a more attractive overall pronunciation.

---		
yoji_out_df

---
# A Few Highlights

## <ruby>一断風雨<rp>(</rp><rt>いちだんふうう</rt><rp>)</rp><ruby>
+ ichi-dan-fu-u
+ Something akin to the domino/butterfly effect, one small decision and all hell breaks loose

## <ruby>二索呻馬<rp>(</rp><rt>にさくしんば</rt><rp>)</rp><ruby>
+ ni-saku-shin-ba
+ Too many cooks in the kitchen; pulled in too many directions

## <ruby>一気門奇<rp>(</rp><rt>いっきもんき</rt><rp>)</rp><ruby> 
+ i-kki-mon-ki
+ Losening up after a couple drinks

## <ruby>勉流悪人<rp>(</rp><rt>べんりゅうあくにん</rt><rp>)</rp><ruby> 
+ ben-ryuu-aku-nin
+ Those in high places aren't always the best people, this would be a label for such a person

## <ruby>面思同鳳<rp>(</rp><rt>めんしどうほう</rt><rp>)</rp><ruby>
+ men-shi-dou-hou
+ The thoughts you show mirror the phoenix: something like "great idea!" or "you have the mind of a mastermind!"

## <ruby>苦闘力不<rp>(</rp><rt>くとうりょくふ</rt><rp>)</rp><ruby> 
+ ku-tou-ryoku-fu
+ Exhaustion after a long, strenuous day

## <ruby>不才由明<rp>(</rp><rt>ふさいゆうみょう</rt><rp>)</rp><ruby> 
+ fu-sai-yuu-myou
+ Exceedingly and conspicuously incompetent

## <ruby>用人同曲<rp>(</rp><rt>ようにんどうきょく</rt><rp>)</rp><ruby> 
+ you-nin-dou-kyoku
+ Birds of a feather flock together; great minds think alike

## <ruby>不心禽斥<rp>(</rp><rt>ふしんきんたい</rt><rp>)</rp><ruby>
+ fu-shin-kin-tai
+ Be of no mind, be free

## <ruby>一用発四<rp>(</rp><rt>ひとようはっし</rt><rp>)</rp><ruby> 
+ hito-you-ha-sshi
+ Finish one thing, 4 more pop up

## <ruby>寝雨麗心<rp>(</rp><rt>ねあめれいしん</rt><rp>)</rp><ruby> 
+ ne-ame-rei-shin
+ Sleeping through the storm can cleanse the soul; pick your battles

## <ruby>車行命道<rp>(</rp><rt>しゃこうめいどう</rt><rp>)</rp><ruby>
+ sha-kou-mei-dou
+ Life in the fast lane



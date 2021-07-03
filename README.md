# Wisdom in 4 Characters Or Less

---
![Training a neural network to generate 四字熟語 (as best it can!)](./outputs/header.jpg)

---
[*Open*](https://gitpod.io/#https://github.com/ryancahildebrandt/yoji) *in gitpod*

## *Purpose*

A project to generate 四字熟語 (yoji-jukugo, 4 character Japanese idioms), using a sequential tenworflow model.

---
## *Dataset*
The dataset used for the current project was scraped/pulled from the following: 
- [Yojijukugo](http://www.edrdg.org/projects/yojijukugo.html) for idioms and meanings/readings
- [Jamdict](https://github.com/neocl/jamdict) for kanji readings, meanings, and other information
- [Kanji Database](https://www.kanjidatabase.com/) for kanji classification, grade level, and misc characteristics 

---

## *Outputs*

+ The main [report](https://datapane.com/u/ryancahildebrandt/reports/wisdom-in-4-characters/), compiled with datapane and also in [html](./outputs/yoji_rprt.html) format
+ The full [yoji_df](./outputs/yoji_df.csv) dataframe describing the idioms, their constituent kanji, and all additional characteristics from the data linked above
+ List of generated [idioms](./outputs/yoji_out.txt), sans definitions and readings
+ The same list, expanded out to a [dataframe](./outputs/yoji_out_df.csv) including readings and meanings of constituent characters and bigrams 


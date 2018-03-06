# ChineseWiki
## 维基百科中文词条
维基百科开源的中文词条内容，收集了99W+词条，当然比百度少了不少。
有效处理该原始语料的方法主要有两个：1、Wikipedia Extractor；2、gensim的wikicorpus库。
两种处理都比较粗糙，导致：

 - Wikipedia Extractor提取出来的结果，会去掉很多空格与括号里面的内容；
 - gensim.corpora.wikicorpus.WikiCorpus处理，问题更严重，因为它连所有标点都去掉了。

先下载语料文件：[下载地址](https://dumps.wikimedia.org/zhwiki/)

![这里写图片描述](https://github.com/mattzheng/ChineseWiki/blob/master/wiki.png?raw=true)

zhwiki-20180301-pages-articles-multistream.xml.bz2 是主文件；
zhwiki-20180301-pages-articles-multistream-index.txt.bz2 是每个词条的编号信息。



**本篇主要是写如何进行整理：**

 - 1、繁简转化库——opencc的安装与使用
 - 2、wiki中文词条整理
 - 3、关键词检索模块


**额外的还有一些其他辅助信息：**

 - 1、重定向匹配表，[中文维基重定向的同义词表](https://spaces.ac.cn/usr/uploads/2017/01/4014947738.7z)
 - 2、词条的编号信息，官方提供
   [zhwiki-20180301-pages-articles-multistream-index.txt.bz2 23.6
   MB](https://dumps.wikimedia.org/zhwiki/20180301/zhwiki-20180301-pages-articles-multistream-index.txt.bz2)

----------


## 1、繁简转化库——opencc的安装与使用
其中繁体转简体中文的库，opencc的安装，网上的说明程序真尼玛多，没一个搞的定的，吐槽一下！！！
直接来看[github](https://github.com/yichen0831/opencc-python)原文，安装方式：

```
pip install opencc-python-reimplemented
```
或者把github下载下来用`python setup.py install`安装，哪有网上教程那么麻烦！

使用也不太一样：

```
from opencc import OpenCC 

openCC = OpenCC('s2t')  # convert from Simplified Chinese to Traditional Chinese
# can also set conversion by calling set_conversion
# openCC.set_conversion('s2tw')
to_convert = '开放中文转换'
converted = openCC.convert(to_convert)
```

支持的转换模式有：

```
'hk2s': Traditional Chinese (Hong Kong standard) to Simplified Chinese

's2hk': Simplified Chinese to Traditional Chinese (Hong Kong standard)

's2t': Simplified Chinese to Traditional Chinese

's2tw': Simplified Chinese to Traditional Chinese (Taiwan standard)

's2twp': Simplified Chinese to Traditional Chinese (Taiwan standard, with phrases)

't2hk': Traditional Chinese to Traditional Chinese (Hong Kong standard)

't2s': Traditional Chinese to Simplified Chinese

't2tw': Traditional Chinese to Traditional Chinese (Taiwan standard)

'tw2s': Traditional Chinese (Taiwan standard) to Simplified Chinese

'tw2sp': Traditional Chinese (Taiwan standard) to Simplified Chinese (with phrases)
```

## 2、wiki中文词条整理
参考并整理代码参考苏神的：[获取并处理中文维基百科语料](https://spaces.ac.cn/archives/4176/)

先从官网下载了`zhwiki-20180301-pages-articles-multistream.xml.bz2`文件，然后先用`wiki_parser.py`将其进行解析，变成以下格式：
```
=== 词源 ===
英语词语Philosophy（philosophia）源于古希腊语中的φιλοσοφία，意思为「爱智慧」，有时也译为「智慧的朋友」

=== 主分支 ===
哲学可以分为很多不同的分支，主要包括形而上学、知识论、伦理学、逻辑学和美学。
* 形而上学/宇宙论
* 知识论
```
然后笔者的做法是利用给每一行进行打标`wiki_clean.py`，因为每一行通过符号是可以直接从属关系。记号遵从以下表格：


内容级别 | 内容 | 标记  
 | :-: | -: 
1级标题 | 【政治学】| 1 
2级标题 | == 历史 ==  | 2 
3级标题 | === 古典时期 === | 3
4级标题 | ==== 古典时期 ==== | 4
平行关系 | * 知识论 | 5
正文 | 英语词语Philosophy | 0


最后生成的如下表格：
![这里写图片描述](https://github.com/mattzheng/ChineseWiki/blob/master/corpus.png?raw=true)


## 3、关键词检索模块
本模块目前还在考虑，遇到了中文分词一样的问题，如果给入的数据是：`'民用无人机到自主驾驶汽车'`，那么我们应该是想了解这句话里面的：`无人机;自主驾驶汽车`，但最后会分出：`民用；无人机；自主；驾驶；汽车；无人...`
概念从属关系，`驾驶汽车与汽车`，肯定想知道`驾驶汽车`

目前做到的效果是：

```
search_txt = '民用无人机到自主驾驶汽车'
search(search_txt)
```
结果输出：
```
{'无人机': '各种类型的无人机。\r\n无人机（Uncrewed vehicle、Unmanned vehicle、Drone）或称无人载具是一种无搭载人员的载具。通常使用遥控、导引或自动驾驶来控制。可在科学研究、军事、休闲娱乐用途上使用。\r\n在日常用语中，“无人机”被特指为“无人飞行载具”。\r\n',
 '汽车': 'Benz Patent-Motorwagen Nummer 1，第一辆“现代汽车”。\r\n1927年的汽车，福特T型车。\r\n1942年的汽车，纳许大使。\r\n1980年的汽车，大众帕萨特\r\n1999年的汽车，西雅特托莱多\r\n2008年的超级跑车，科尼赛克CCX。\r\n日产Maxima SR\r\n怪兽卡车\r\n汽车或称机动车（英式英语：car；美式英语：automobile；美国口语：auto），即本身具有动力得以驱动，不须依轨道或电缆，得以动力行驶之车辆。广义来说，具有四轮或以上行驶的车辆，普遍多称为汽车。虽然，长久以来学术各界对「谁是第一位汽车发明者」皆有不同的看法及论述，未有完全一致性的看法，但是，绝大部份学者皆将德国工程师卡尔·本茨视为第一位发明者。美国人亨利·福特首先大量生产平价汽车，是使汽车得以普及化的人。\r\n',
 '驾驶': '驾驶，指的是人类在操纵交通工具或一些机械设备时的行为，可分为机动车驾驶、船舶驾驶、列车驾驶、航空器驾驶、其它驾驶，这些一般都属于真实驾驶，可采用手动驾驶或自动驾驶的方式进行驾驶。对于通过电子系统以游戏等方式进行模拟真实驾驶情况的行为，则被称为虚拟驾驶。对于交通工具或一些机械设备的驾驶者，被称为驾驶员。对于驾驶交通工具或一些机械设备时应随身携带的证件，则被称为驾驶证。\r\n'}
```



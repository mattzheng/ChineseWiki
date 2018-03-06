# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 15:46:34 2018

@author: mattzheng
"""


import gensim
from tqdm import tqdm
input_file = "E:\matt\get\wiki\zhwiki-20180301-pages-articles-multistream.xml.bz2"
f = open('E:\matt\get\wiki\zhwiki.txt',encoding='utf8',mode='w')
wiki =  gensim.corpora.WikiCorpus(input_file, lemmatize=False, dictionary={})

for text in tqdm(list(wiki.get_texts())):
    str_line = bytes.join(b' ', text).decode()
    f.write(str_line+'\n')


    
    
    
# from https://spaces.ac.cn/archives/4176/
from gensim.corpora.wikicorpus import extract_pages,filter_wiki
import bz2file
import re
import opencc
from tqdm import tqdm
import codecs

input_file = "E:\matt\get\wiki\zhwiki-20180301-pages-articles-multistream.xml.bz2"
wiki = extract_pages(bz2file.open(input_file))

def wiki_replace(d):
    s = d[1]
    s = re.sub(':*{\|[\s\S]*?\|}', '', s)
    s = re.sub('<gallery>[\s\S]*?</gallery>', '', s)
    s = re.sub('(.){{([^{}\n]*?\|[^{}\n]*?)}}', '\\1[[\\2]]', s)
    s = filter_wiki(s)
    s = re.sub('\* *\n|\'{2,}', '', s)
    s = re.sub('\n+', '\n', s)
    s = re.sub('\n[:;]|\n +', '\n', s)
    s = re.sub('\n==', '\n\n==', s)
    s = u'【' + d[0] + u'】\n' + s
    return opencc.convert(s).strip() # 

i = 0
f = codecs.open('E:\matt\get\wiki\zhwiki.txt', 'w', encoding='utf-8')
w = tqdm(wiki, desc=u'已获取0篇文章')
for d in w:
    if not re.findall('^[a-zA-Z]+:', d[0]) and d[0] and not re.findall(u'^#', d[1]):
        s = wiki_replace(d)
        f.write(s+'\n\n\n')
        i += 1
        if i % 100 == 0:
            w.set_description(u'已获取%s篇文章'%i)

f.close()

# ----------------------------------整理--------------------------------------
from tqdm import tqdm
import pandas as pd
txt_path = 'E:\matt\get\wiki\zhwiki.txt'

f = open(txt_path,encoding = 'utf-8')

f_txt = []
for line in f.readlines():
    f_txt.append(line)
#正文 0
#1级 【政治学】   1
#2级 == 历史 ==  2
#3级  === 古典时期 === 3
#4级  ==== 古典时期 ==== 4
# 平行关系：*   5
def adj_1(sting,limit = '【'):
    try:
        if sting.index(limit) < 1:
            result = True
        else:
            result = False
    except:
        result = False
    return result


judge_list = []
for txt in tqdm(f_txt):
    if '【' in txt and '】' in txt and adj_1(txt):
        judge_list.append(1)
    elif '====' in txt and adj_1(txt,limit = '===='):
        judge_list.append(4)
    elif '==='  in txt and adj_1(txt,limit = '==='):
        judge_list.append(3)
    elif '=='  in txt and adj_1(txt,limit = '=='):
        judge_list.append(2)
    elif '*'  in txt and adj_1(txt,limit = '*'):
        judge_list.append(5)
    else:
        judge_list.append(0)

# 修正
#wiki_dataframe[wiki_dataframe.tag==1]

#
wiki_dataframe = pd.DataFrame(list(zip(f_txt,judge_list)))
wiki_dataframe.columns = ['content','tag']

# 清洗
wiki_dataframe = wiki_dataframe[list(map(lambda x : x!='\n',wiki_dataframe.content))]
wiki_dataframe.reset_index(inplace=True,drop=True)

# 验证
wiki_dataframe[wiki_dataframe.tag==1].content[:1000]

# 总表输出
wiki_dataframe.to_csv('E:\matt\get\wiki\wiki_dataframe_1.csv',index = False,encoding = 'utf-8')
wiki_dataframe=pd.read_csv('E:\matt\get\wiki\wiki_dataframe_1.csv',encoding = 'utf-8')


#  -----------------------------------wiki ---封装 ----------------
from gensim.corpora.wikicorpus import extract_pages,filter_wiki
import bz2file
import re
from opencc import OpenCC 
from tqdm import tqdm
import codecs
import pandas as pd

def wiki_replace(d):
    s = d[1]
    s = re.sub(':*{\|[\s\S]*?\|}', '', s)
    s = re.sub('<gallery>[\s\S]*?</gallery>', '', s)
    s = re.sub('(.){{([^{}\n]*?\|[^{}\n]*?)}}', '\\1[[\\2]]', s)
    s = filter_wiki(s)
    s = re.sub('\* *\n|\'{2,}', '', s)
    s = re.sub('\n+', '\n', s)
    s = re.sub('\n[:;]|\n +', '\n', s)
    s = re.sub('\n==', '\n\n==', s)
    s = u'【' + d[0] + u'】\n' + s
    return openCC.convert(s) 

def wiki_process(input_file,save_path):
    # wikicorpus解析
    wiki = extract_pages(bz2file.open(input_file))
    # 处理并导出
    i = 0
    f = codecs.open(save_path, 'w', encoding='utf-8')
    w = tqdm(wiki, desc=u'已获取0篇文章')
    openCC = OpenCC('t2s') 
    for d in w:
        if not re.findall('^[a-zA-Z]+:', d[0]) and d[0] and not re.findall(u'^#', d[1]):
            s = wiki_replace(d)
            f.write(s+'\n\n\n')
            i += 1
            if i % 100 == 0:
                w.set_description(u'已获取%s篇文章'%i)
    
    f.close()
    
if __name__ == '__main__':
    input_file = "E:\matt\get\wiki\zhwiki-20180301-pages-articles-multistream.xml.bz2"  # bz2文件存放位置
    save_path = 'E:\matt\get\wiki\zhwiki_2.txt'   # txt文件保存位置
    wiki_process(input_file,save_path)
    # >>> 已获取0篇文章: 46it [00:02, 16.40it/s]





# -------------------找到1级-2级之间的内容,提取主要内容---------------------

def locate_2(i,ranges = 30,wiki_dataframe = wiki_dataframe):
    j = i
    for j in range(j,j+ranges):
        if wiki_dataframe.tag[j] == 2:
            break
        j = j + 1
    if sum(wiki_dataframe.tag[i:j]==1) > 1:
        # 这种情况，代表，这个词条只有概述，没有2级标题
        tmp_data = wiki_dataframe.tag[i:j]
        j = tmp_data[tmp_data == 1].index[1]
    return j

#i = 6998948
#j = i
#locate_2(6998948)

#[1 in i for i in list(wiki_dataframe.tag[i:j])]
#wiki_dataframe[wiki_dataframe.tag[i:j]==1]
#wiki_dataframe[i:locate_2(6998948)]

def dict2dataframe(content_dict):  
    return pd.DataFrame(list(content_dict.values()), index = list(content_dict.keys()))  
    
locate_1 = list(wiki_dataframe.index[wiki_dataframe.tag==1])

# 整理，词条：词条解释
content_1 = {}
#locate = 6998955
for locate in tqdm(locate_1):
    x = locate
    y = locate_2(locate)
    content_1[wiki_dataframe.content[x]]  = ''.join(list(wiki_dataframe.content[x+1:y]))

    
# 格式转化
content_1_dataframe = dict2dataframe(content_1)
content_1_dataframe.columns = ['content']
content_1_dataframe['keyword'] = content_1_dataframe.index

# 第一轮清洗
content_1_dataframe['keyword'] = list(map(lambda x : x.replace('【',''),content_1_dataframe['keyword']))
content_1_dataframe['keyword'] = list(map(lambda x : x.replace('\r\n',''),content_1_dataframe['keyword']))
content_1_dataframe['keyword'] = list(map(lambda x : x.replace('】',''),content_1_dataframe['keyword']))
#content_1_dataframe['content'] = list(map(lambda x : x.replace('\r\n',''),content_1_dataframe['content']))
#content_1_dataframe['content'] = list(map(lambda x : x.replace('\r',''),content_1_dataframe['content']))
#content_1_dataframe['content'] = list(map(lambda x : x.replace('\n',''),content_1_dataframe['content']))
#content_1_dataframe.content[20000:20200]
# 第二轮清洗


content_1_dataframe.to_csv('E:\matt\get\wiki\content_1_dataframe_2.csv',index = False,encoding = 'utf-8')
content_1_dataframe=pd.read_csv('E:\matt\get\wiki\content_1_dataframe_1.csv',encoding = 'utf-8')

content_1_dataframe.keyword[0].replace('【','')
content_1_dataframe.keyword[0].replace('\r\n','')


#
wiki_dataframe.content[6998948:6998955]
wiki_dataframe.ix[1000:2000,:]
wiki_dataframe[ list(map(lambda x : '【成人游戏】' in x,wiki_dataframe.content))]
list(content_1_dataframe[content_1_dataframe.keyword == '成人游戏'].content)    
        
6998955 in locate_1
6998948
locate_2(6998955)


#  ----------------- 相似性逻辑 -------------------
content_1_dataframe.keyword
import jieba
import copy


def Intention_Identification(c_lists):
    '''
    # 最高概念判别
    # 意思就是：出来的这个概念，是包括其他概念的
    '''
    c_list = copy.copy(c_lists)
    # 筛出一些重复概念
    for _ in range(len(c_list)):
        for word in c_list:
            if sum([ word in c  for c in c_list]) > 1:
                c_list.remove(word) 
    # 删除单字
    c_list = [i for i in c_list if len(i) > 1]
    return c_list

def dataframe2dict(search_txt_content_understand):
    return dict(zip(search_txt_content_understand.keyword,search_txt_content_understand.content))

def search(search_txt,content_1_dataframe = content_1_dataframe):
    search_txt_content = content_1_dataframe[[str(con) in search_txt for con in content_1_dataframe.keyword]]
    c_list = list(search_txt_content.keyword)
    #keywords = Intention_Identification(c_list)
    if c_list:
        result = dataframe2dict(search_txt_content[[i in Intention_Identification(c_list) for i in c_list]])
    else:
        result = 'sorry,no keyword.'
    return result

search_txt = '这一研究可以从短期和长期来讨论。一些短期的担忧在无人驾驶方面，从民用无人机到自主驾驶汽车。'
search_txt = '济'
search_txt = '出来的这个概念，是包括其他概念的'
search_txt = '亮眼睛系统'
search(search_txt)


list(content_1_dataframe[content_1_dataframe.keyword=='成人游戏'].content)












                                               


# -*- coding: utf-8 -*-
"""
数据格式:
    #正文            0
    #1级 【政治学】   1
    #2级 == 历史 ==  2
    #3级  === 古典时期 === 3
    #4级  ==== 古典时期 ==== 4
    # 平行关系：*   5

清洗逻辑:
    目前是按行保存在txt之中，给每一行打上标签。
"""

from tqdm import tqdm
import pandas as pd



def adj_1(sting,limit = '【'):
    try:
        if sting.index(limit) < 1:
            result = True
        else:
            result = False
    except:
        result = False
    return result

#清洗函数
def wiki_clean(txt_path):
    # 加载并读出
    f = open(txt_path,encoding = 'utf-8')
    
    f_txt = []
    for line in f.readlines():
        f_txt.append(line)
    
    # 标注
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
    
    # dataframe
    wiki_dataframe = pd.DataFrame(list(zip(f_txt,judge_list)))
    return wiki_dataframe

if __name__ == '__main__':
    txt_path = 'E:\matt\get\wiki\zhwiki.txt'
    wiki_dataframe = wiki_clean(txt_path)
    wiki_dataframe.to_csv('./wiki.csv',index = False,encoding = 'utf-8')


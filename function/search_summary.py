#coding:utf8

import os
import sys
# 引入自定义模块入口
# sys.path.append(r"./Tools")

import time
from urllib.parse import quote

from function.Tools import Html_Tools as To
from function.Tools import TextProcess as T
# from Tools import Html_Tools as To
# from Tools import TextProcess as T


'''
对百度、Bing 的搜索摘要进行答案的检索
（需要加问句分类接口）
'''

def kwquery(query):
    #分词 去停用词 抽取关键词
    keywords = []
    words = T.postag(query)
    # 获取搜索的关键词
    for k in words:
        # 只保留名词
        # __contains__是一个内建方法，判断一个字符串中是否包含给定的子字符串
        if k.flag.__contains__("n"):
            # print k.flag  k的词性
            # print k.word  k这个词语
            keywords.append(k.word)

    answer = []
    text = ''
    # 找到答案就置1
    flag = 0

    # 抓取百度前10条的摘要
    # quete对传入的字符串进行编码，quote 除了 -._/09AZaz ,都会进行编码
    soup_baidu = To.get_html_baidu('https://www.baidu.com/s?wd='+quote(query))

    for i in range(1,10):
        # 如果抓取到的网页为空，则直接跳出处理程序段
        if soup_baidu == None:
            break
        # 获取返回的第i条摘要
        results = soup_baidu.find(id=i)

        # 如果第i条摘要为空（也就是没有相关的搜索结果了），直接跳出处理程序段
        if results == None:
            pass
            # print("百度摘要找不到答案")
            break
        # print(results)
        # print '============='
        # print results.attrs
        # print len(results.attrs)
        # print results['class']
        # print '============='
        #判断是否有mu,如果第一个是百度知识图谱的 就直接命中答案
        if 'mu' in results.attrs and i == 1:
            # print results.attrs["mu"]
            r = results.find(class_='op_exactqa_s_answer')
            if r == None: # 百度知识图谱没有找到答案就跳过
                # print("pass")
                pass
            else:
                # print r.get_text()
                pass
                # print("百度知识图谱找到答案")
                answer.append(r.get_text().strip())
                flag = 1
                break


        #古诗词判断
        if 'mu' in results.attrs and i == 1:
            r = results.find(class_="op_exactqa_detail_s_answer")
            if r == None:
                pass
                # print("百度诗词找不到答案")
            else:
                # print r.get_text()
                # print("百度诗词找到答案")
                pass
                answer.append(r.get_text().strip())
                flag = 1
                break

        #万年历 & 日期
        if 'mu' in results.attrs and i == 1 and results.attrs['mu'].__contains__('http://open.baidu.com/calendar'):
            r = results.find(class_="op-calendar-content")
            if r == None:
                pass
                # print("百度万年历找不到答案")
            else:
                # print r.get_text()
                pass
                # print("百度万年历找到答案")
                answer.append(r.get_text().strip().replace("\n","").replace(" ",""))
                flag = 1
                break
        try:
            if 'tpl' in results.attrs and i == 1 and results.attrs['tpl'].__contains__('calendar_new'):
                print("---------------------------------")
                print(results)
                # r = results.attrs['fk'].replace("6018_", "") # 原版
                # r = results.attrs['mu'].replace("6018_","")
                r = results.find(class_="op-calendar-content")
                print(r)

                if r == None:
                    pass
                    # print("百度万年历新版找不到答案")
                    # continue
                else:
                    # print r.get_text()
                    pass
                    # print("百度万年历新版找到答案")
                    answer.append(r)
                    flag = 1
                    break
        except:
            pass


        #计算器
        if 'mu' in results.attrs and i == 1 and results.attrs['mu'].__contains__('http://open.baidu.com/static/calculator/calculator.html'):
            # r = results.find('div').find_all('td')[1].find_all('div')[1]
            r = results.find(class_="op_new_val_screen_result")
            if r == None:
                pass
                # print("计算器找不到答案")
                # continue
            else:
                # print r.get_text()
                pass
                # print("计算器找到答案")
                answer.append(r.get_text().strip())
                flag = 1
                break


        # 百度知道答案
        if 'mu' in results.attrs and i == 1:
            r = results.find(class_='op_best_answer_question_link')
            if r == None:
                pass
                # print("百度知道图谱找不到答案")
            else:
                pass
                # print("百度知道图谱找到答案")
                url = r['href']
                zhidao_soup = To.get_html_zhidao(url)
                r = zhidao_soup.find(class_='bd answer').find('pre')
                if r == None:
                    r = zhidao_soup.find(class_='bd answer').find(class_='line content')

                answer.append(r.get_text())
                flag = 1
                break

        if results.find("h3") != None:
            # 百度知道
            if results.find("h3").find("a").get_text().__contains__("百度知道") and (i == 1 or i ==2):
                url = results.find("h3").find("a")['href']
                if url == None:
                    pass
                    # print("百度知道图谱找不到答案")
                    continue
                else:
                    pass
                    # print("百度知道图谱找到答案")
                    zhidao_soup = To.get_html_zhidao(url)

                    r = zhidao_soup.find(class_='bd answer')
                    if r == None:
                        continue
                    else:
                        r = r.find('pre')
                        if r == None :
                            r = zhidao_soup.find(class_='bd answer').find(class_='line content')
                    answer.append(r.get_text().strip())
                    flag = 1
                    break

            # 百度百科
            if results.find("h3").find("a").get_text().__contains__("百度百科") and (i == 1 or i ==2):
                url = results.find("h3").find("a")['href']
                if url == None:
                    pass
                    # print("百度百科找不到答案")
                    continue
                else:
                    pass
                    # print("百度百科找到答案")
                    baike_soup = To.get_html_baike(url)

                    r = baike_soup.find(class_='lemma-summary')
                    if r == None:
                        continue
                    else:
                        r = r.get_text().replace("\n","").strip()
                    answer.append(r)
                    flag = 1
                    break
        text += results.get_text()

    if flag == 1:
        return answer

    #获取bing的摘要
    soup_bing = To.get_html_bing('https://www.bing.com/search?q='+quote(query))
    # 判断是否在Bing的知识图谱中
    # bingbaike = soup_bing.find(class_="b_xlText b_emphText")
    bingbaike = soup_bing.find(class_="bm_box")

    if bingbaike != None:
        if bingbaike.find_all(class_="b_vList")[1] != None:
            if bingbaike.find_all(class_="b_vList")[1].find("li") != None:
                pass
                # print("Bing知识图谱找到答案")
                flag = 1
                answer.append(bingbaike.get_text())
                # print "====="
                # print answer
                # print "====="
                return answer
    else:
        pass
        # print("Bing知识图谱找不到答案")
        results = soup_bing.find(id="b_results")
        bing_list = results.find_all('li')
        for bl in bing_list:
            temp =  bl.get_text()
            if temp.__contains__(" - 必应网典"):
                pass
                # print("查找Bing网典")
                url = bl.find("h2").find("a")['href']
                if url == None:
                    pass
                    # print("Bing网典找不到答案")
                    continue
                else:
                    pass
                    # print("Bing网典找到答案")
                    bingwd_soup = To.get_html_bingwd(url)

                    r = bingwd_soup.find(class_='bk_card_desc').find("p")
                    if r == None:
                        continue
                    else:
                        r = r.get_text().replace("\n","").strip()
                    answer.append(r)
                    flag = 1
                    break

        if flag == 1:
            return answer

        text += results.get_text()

    # print text


    # 如果再两家搜索引擎的知识图谱中都没找到答案，那么就分析摘要
    if flag == 0:
        #分句
        cutlist = ["。","?",".", "_", "-",":","！","？"]
        temp = ''
        sentences = []
        for i in range(0,len(text)):
            if text[i] in cutlist:
                if temp == '':
                    continue
                else:
                    # print temp
                    sentences.append(temp)
                temp = ''
            else:
                temp += text[i]

        # 找到含有关键词的句子,去除无关的句子
        key_sentences = {}
        for s in sentences:
            for k in keywords:
                if k in s:
                    key_sentences[s]=1


        # 根据问题制定规则

        # 识别人名
        target_list = {}
        for ks in key_sentences:
            # print ks
            words = T.postag(ks)
            for w in words:
                # print "====="
                # print w.word
                if w.flag == ("nr"):
                    if w.word in target_list:
                        target_list[w.word] += 1
                    else:
                        target_list[w.word] = 1

        # 找出最大词频
        if len(target_list)>0:
            sorted_lists = sorted(list(target_list.items()), lambda x, y: cmp(x[1], y[1]), reverse=True)
            # print len(target_list)
            #去除问句中的关键词
            sorted_lists2 = []
            # 候选队列
            for i, st in enumerate(sorted_lists):
                # print st[0]
                if st[0] in keywords:
                    continue
                else:
                    sorted_lists2.append(st)

            # print("返回前n个词频")
            answer = []
            for i,st in enumerate(sorted_lists2):
                # print st[0]
                # print st[1]
                if i< 3:
                    # print st[0]
                    # print st[1]
                    answer.append(st[0])
        # print answer
        else:
            answer="question is not find"

    return answer

# 利用搜索引擎查找答案
def search_for_answer(quesiton):
    ans = kwquery(quesiton)
    print("###################")
    print(ans)
    if "not find" in ans:
        return ans
    return ans[0]
    # for a in ans:
    #     return a
        # print(a)
        # print("~~~~~~~")


if __name__ == '__main__':
    pass
    query = "日期"
    print(query)
    ans = kwquery(query)
    # print("~~~~~~~")
    for a in ans:
        print("####")
        print(a)
    # print("~~~~~~~")

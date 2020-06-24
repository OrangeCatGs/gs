import re
import requests
import csv

link = []
title = []
watchs = []
num = []
day = []
up_space = []
up_names = []
message = input("请输入想要搜索的内容：")
op = int(input("请问您想要爬取多少页呢？（至多50页）"))
for i in range(1,op+1):
    try:
        url = 'https://search.bilibili.com/all?keyword=' + str(message)+"&from_source=nav_search_new&page="+str(i)
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}
        response = requests.get(url,headers=headers)
        response.encoding='encoding=utf-8'
        html = response.text
        pattern = re.compile('<li class="video-item matrix"><a href="//(.*?)" title="(.*?)" target="_blank" class="img-anchor"><div class="img"><div class="lazy-img"><img alt="" src=""></div><span class="so-imgTag_rb">.*?</span><div class="watch-later-trigger watch-later"></div><span class="mask-video"></span></div><!----></a><div class="info"><div class="headline clearfix"><!----><!----><span class="type hide">.*?</div><div class="tags"><span title="观看" class="so-icon watch-num"><i class="icon-playtime"></i>(.*?)</span><span title="弹幕" class="so-icon hide"><i class="icon-subtitle"></i>(.*?)</span><span title="上传时间" class="so-icon time"><i class="icon-date"></i>(.*?)</span><span title="up主" class="so-icon"><i class="icon-uper"></i><a href="//(.*?)" target="_blank" class="up-name">(.*?)</a></span></div></div></li>',re.S)
        items = re.findall(pattern,html)
        print("正在爬取第",str(i),"页")
        for it in items:
            link.append(it[0].strip())
            title.append(it[1].strip())
            watchs.append(it[2].strip())
            num.append(it[3].strip())
            day.append(it[4].strip())
            up_space.append(it[5].strip())
            up_names.append(it[6].strip())
        
    except:
        pass
    
    
with open('输出.csv', mode='w',newline='',encoding = 'gb18030') as csv_file:
    fieldnames = ['视频链接', '标题', '播放量','弹幕量','UP空间','up']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    n = 0
    for li in link:
        try:
            writer.writerow({'视频链接':link[n], '标题':title[n], '播放量':watchs[n],'弹幕量':num[n],'UP空间':up_space[n],'up':up_names[n]})
            n = n + 1
        except:
            pass
print("爬取完成！")

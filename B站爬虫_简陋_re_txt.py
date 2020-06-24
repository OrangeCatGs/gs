import re#引入正则表达式
import requests

def get_it(url):#获得源代码的函数
    try :
        kv = {'user-agent':'Mozilla/5.0'}#请求头
        r = requests.get(url , headers=kv)#获得响应
        r.raise_for_status()#如果状态不是200报错
        r.encoding = r.apparent_encoding#替换编码格式
        return r.text#返回HTML文本信息
    except:
        return  print("异常")

def alalysis_it(ilt,html):#解析源代码的函数
    titles = re.findall(r'<a title=\"(.*?)\"',html)
    links = re.findall(r'<li class="video-item matrix"><a href="//www.bilibili.com/video/(.*?)?from=search" ',html)
    up_names = re.findall(r'class="up-name">(.*?)</a>',html)
    watch_num = re.findall(r'<i class="icon-playtime"></i>(.*?)</span>', html, re.S)
    barrages = re.findall(r'<i class="icon-subtitle"></i>(.*?)</span>', html, re.S)
    time = re.findall(r'<i class="icon-date"></i>(.*?)</span>', html, re.S)
    #数据清洗
    a = []
    b = []
    for i in range(len(titles)):
        a.append(watch_num[i].replace(" ",""))
        b.append(a[i].replace("\n",""))
    watch_num = b
    a = []
    b = []
    for i in range(len(titles)):
        a.append(barrages[i].replace(" ",""))
        b.append(a[i].replace("\n",""))
    barrages = b
    a = []
    b = []
    for i in range(len(titles)):
        a.append(time[i].replace(" ",""))
        b.append(a[i].replace("\n",""))
    time = b
    for i in range(len(titles)):
        title = titles[i]
        link = links[i]
        up_name = up_names[i]
        watch_nu = watch_num[i]
        barrage = barrages[i]
        tim = time[i]
        ilt.append([title,link,up_name,watch_nu,barrage,tim])#将数据依次加入列表
    return ilt

def printit(ilt):#打印解析后的数据
    tplt = "{:4}\t{:10}\t{:20}\t{:10}\t{:4}\t{:4}\t{:10}"
    count=0
    for g in ilt:
        count = count + 1#计数器
        print(tplt.format(count,g[0],"www.bilibili.com/video/" +g[1]+ "from=search",g[2],g[3],g[4],g[5],chr(12288)))

def saveist(ilt):#将解析后的数据保存到本地用TXT格式
    with open("D://B站搜索.txt", "a", encoding='utf-8') as f:
        f.write("视频标题"+"\t"+"视频AV号"+"\t"+ "up主"+"\t"+ "\t" + "播放量"+"\t"+ "弹幕量"+"\t"+ "上传时间"+"\t"+"\n")
        for i in ilt:
            for j in i:
                f.write(j +"\t")
            f.write("\n")
        f.close()

def main():#主函数
    tplt = "{:4}\t{:10}\t{:20}\t{:10}\t{:4}\t{:4}\t{:10}"

    ilt = []
    kw = input("请输入你的搜索：")
    depth = 50
    print(tplt.format("视频编号", "视频标题", "视屏链接", "up主",  "播放量", "弹幕量", "上传时间"))
    start_url = "https://search.bilibili.com/all?keyword=" + str(kw) + "&from_source=nav_search_new&page="
    for i in range(depth):
        url = start_url + str(i+1)
        html = get_it(url)
        alalysis_it(ilt, html)
    printit(ilt)
    saveist(ilt)

main()#应用主函数

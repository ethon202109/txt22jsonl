# import srsly
import os
import re
import json

import chardet
path = r"E:\baiduwangpan\20230105\20230105\aliyun.20230105.1.小说"
def getFileName(path):
    filesList = []
    filesName = []
    for root, dirs, files in os.walk(path):
        isExists = os.path.exists(path)
        # 新建文件夹
        if not isExists:
            os.makedirs(path)
        for file in files:
            # 判断尾缀是不是txt
            suffix = file.split('.')[1]
            fileName = file.split('.')[0]
            if suffix == 'txt':
                filesList.append(root + '\\' + file)
                filesName.append(fileName)
    return filesList
    # return filesList, filesName


#可以根据文件夹序号与文件名、负责人id、时间序列，编码64位id，便于最后去重
import base64
import hmac
b64_token = base64.urlsafe_b64encode('ai'.encode("utf-8"))
sha1_tshexstr  = hmac.new('ai'.encode("utf-8"),'ai'.encode("utf-8"),'sha1').hexdigest()
print(sha1_tshexstr)

def en_get(pathi,en):
    with open(pathi, encoding=en) as file:
        json1 = {"title": "您下载的该电子书来自:TXT", "pre-prompt": "", "content": "", "post-prompt": "", "type": ""}
        txt = file.read().replace("\n", "").replace(" ", "")
        r = re.search(r"《(.*?)》", txt)
        if r:
            print(r.groups())
            bookname = r.group(1)
        else:
            bookname = ''

        prompt = "下面这段文本出自小说" + bookname + "的某个章节"
        post_prompt = "以上文本是对小说" + bookname + "中某个故事情节的详细描写"

        json1["pre-prompt"] = prompt
        json1["content"] = txt
        # json1["content"] = txt[:1000]#测试用，截取一小段内容文本
        json1["post-prompt"] = post_prompt
    return json1



with open("E:/baiduwangpan/20230105/20230105.jsonl", 'w', encoding='utf-8') as fw:
    # for i in getFileName(path)[10:100]:#测试用，测试一部分文档
    for i in getFileName(path):
        #检测文档编码
        bytes = min(32, os.path.getsize(i))
        raw = open(i, 'rb').read(bytes)
        result = chardet.detect(raw)
        encoding = result['encoding']
        print(encoding)

        #如果检测编码提取时出现异常，用其他编码尝试，不报错时输出
        try:
            json1=en_get(pathi=i,en=encoding)
        except Exception as e:
            print(1,e)
            encodings=["gb18030","gbk","gb2312","utf-8"]
            for j in encodings:
                try:
                    json1 = en_get(pathi=i, en=j)
                    break
                except Exception as e:
                    print(2, j)
                    print(e)

                    json1 = {"title": "您下载的该电子书来自:TXT赛看", "pre-prompt": "", "content": "", "post-prompt": "", "type": ""}

        json.dump(json1, fw, ensure_ascii=False)#写入json行
        # json.dump(json1, fw, indent=4, ensure_ascii=False)#格式化写入，缩进4，可用于测试时方便观察
        fw.writelines('\n')#写入回车



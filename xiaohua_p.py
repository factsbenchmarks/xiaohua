import os
import requests
import time
from multiprocessing import Pool
import re
import hashlib

BASE_URL = 'https://www.duodia.com/gaozhongxiaohua/list_{}.html'
TOTAL_NUM = 8
STORAGE_PATH = r'C:\xiaohua'
RET_FAIL = 1

def get_detail_info(page_url):
    print('current process {}',os.getpid())
    detai_urls = []
    try:
        r = requests.get(page_url,timeout = 5)
    except:
        return RET_FAIL
    tmp_urls = re.findall('href="(.*?)"',r.text)

    for url in tmp_urls:
        if re.search('gaozhongxiaohua/\d{1,}',url):
            if url not in detai_urls:
                detai_urls.append(url)
    detai_introductions = re.findall('<h3>(\w*?)</h3>',r.text)

    return {'detail_urls':detai_urls,"detail_introductions":detai_introductions}

def get_detail_max_page_num(detail_url):
    try:
        r = requests.get(detail_url,timeout = 5)
    except:
        return RET_FAIL

    PagsNums = re.findall('(\d{1,2})</a>',r.text)

    return int(PagsNums[-1])

def getphotourl(detail_page_url,detail_page_num):

    tmp_url = detail_page_url.rstrip('.html')+'_{}.html'
    try:
        r = requests.get(tmp_url.format(detail_page_num))
    except:
        return RET_FAIL

    photo_url = re.findall('target="_self"><img src="(.*?)"\s',r.text)[0]
    return photo_url

def get_detail_photo(detail_info):
    for url in detail_info['detail_urls']:
        max_page_num = get_detail_max_page_num(url)
        if max_page_num == RET_FAIL:
            return RET_FAIL
        index = detail_info['detail_urls'].index(url)
        for num in range(1,max_page_num+1):
            photo_url = getphotourl(url,num)
            if photo_url == RET_FAIL:
                continue
            save_photo(photo_url,detail_info['detail_introductions'][index])

def save_photo(photo_url,detai_introductions):
    try:
        r = requests.get(photo_url,timeout=5)
    except:
        return RET_FAIL
    m = hashlib.md5()
    m.update(photo_url.encode())
    photo_name = m.hexdigest()
    folder_path = os.path.join(STORAGE_PATH,detai_introductions)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    photo_path = os.path.join(folder_path,photo_name+'.jpg')
    if os.path.exists(photo_path):
        return RET_FAIL
    f = open(photo_path,'wb')
    f.write(r.content)
    f.close()

def main():
    n = os.cpu_count()
    pool = Pool(n)
    task_list = []
    for num in range(1,TOTAL_NUM+1):
        page_url = BASE_URL.format(num)
        task = pool.apply_async(get_detail_info,args=(page_url,),callback=get_detail_photo)
        task_list.append(task)
    pool.close()
    pool.join()
    for task in task_list:
        task.get()

if __name__ == '__main__':
    t1 = time.time()
    main()
    print('time cost {}'.format(time.time() - t1))



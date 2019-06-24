import requests 
import re
import os
import hashlib
import time

DOWLOAD_PATH=r'D:\DOWNLOAD'

def get_page(url):
    try:
        response=requests.get(url,)
        if response.status_code == 200:
            return response.text
    except Exception:
        pass

def parse_index(index_contents):
    # print(type(index_contents))
    detail_urls=re.findall('class="items".*?href="(.*?)"',index_contents,re.S)
    for detail_url in detail_urls:
        if not detail_url.startswith('http'):
            detail_url='http://www.xiaohuar.com'+detail_url
        yield detail_url

def parse_detail(detail_contents):
    movie_urls=re.findall('id="media".*?src="(.*?)"',detail_contents,re.S)
    if movie_urls:
        movie_url=movie_urls[0]
        if movie_url.endswith('mp4'):
           yield movie_url

def download(movie_url):
    print(movie_url)
    try:
        response=requests.get(movie_url,
                              )
        if response.status_code == 200:
            data=response.content
            m=hashlib.md5()
            m.update(str(time.time()).encode('utf-8'))
            m.update(movie_url.encode('utf-8'))
            filepath=os.path.join(DOWLOAD_PATH,'%s.mp4' %m.hexdigest())
            with open(filepath,'wb') as f:
                f.write(data)
                f.flush()
                print('下载成功',movie_url)
    except Exception:
        pass

def main():
    raw_url='http://www.xiaohuar.com/list-3-{page_num}.html'
    for i in range(5):
        #请求索引页,解析拿到详情页链接
        index_url=raw_url.format(page_num=i)
        index_contents=get_page(index_url)
        detail_urls=parse_index(index_contents)

        #请求详情页，解析拿到视频的链接地址
        for detail_url in detail_urls:
            detail_contents=get_page(detail_url)
            movie_urls=parse_detail(detail_contents)

            #下载视频
            for movie_url in movie_urls:
                download(movie_url)



if __name__ == '__main__':
    t1=time.time()
    main()
    print(time.time()-t1)
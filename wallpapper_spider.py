import json
import multiprocessing
import os
from multiprocessing.pool import ThreadPool

import redis

import urllib3
from bs4 import BeautifulSoup

host = 'http://bizhi.sogou.com'


# 从最大id开始,每次向前取28个
def getJson(min_wp_id=100000000, index=1):
    conn = urllib3.connection_from_url(host)
    r = conn.request('GET', '/cate/getCate/' + str(index) + '/' + str(min_wp_id), headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})
    conn.close()
    html = r.data.decode("gbk")
    # print(html)
    data = json.loads(html)
    # for i in range(len(data['wallpapers'])):
    #     print(data['wallpapers'][i]['wp_id'])
    return data


r = redis.Redis()

# 返回操作影响条数(1,0)
def saveWpId(wpId):
    if (r.sadd("wpid_set", wpId) == 1):
        r.rpush("imgid_list", wpId)
        print("saveWpId-----> sadd  wpid_set   " + str(wpId))
        print("saveWpId-----> rpush imgid_list " + str(wpId))


# url保存到redis同时返回url
def saveImageUrl(wp_id):
    conn = urllib3.connection_from_url(host)
    resp = conn.request(method='GET', url='http://bizhi.sogou.com/detail/info/' + str(wp_id),
                        headers={
                            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})
    conn.close()
    html = resp.data.decode('gbk')
    # html = resp.data
    soup = BeautifulSoup(html, "lxml")
    for v in soup.find_all(id='unews_show'):
        src = v.get('src')
        print("saveImageUrl--->rpush imgurl_list--->" + src)
        r.rpush('imgurl_list',src)
        return src


def save_img(img_url,save_dir):
    img_url = img_url.replace('dl', 'img')
    conn = urllib3.connection_from_url(img_url)
    resp = conn.request(method='GET', url=img_url,
                        headers={
                            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})
    conn.close()
    img_name = img_url[img_url.rindex('/') + 1:]
    img_data = resp.data
    # if os.path.exists('8/' + img_name):
    if os.path.exists(save_dir + img_name):
        print("save_img---->文件:" + img_name + "已经存在")
        print("\n")
        return
    f = open(save_dir + img_name, 'wb')
    f.write(img_data)
    f.close()
    print("写入到--->"+save_dir + img_name  )
    print("\n")


def download(num):
    wpid = r.lpop('imgid_list')
    while (wpid != None):
        wp_id = int(wpid)
        print("process" + str(num) + ":download--->" +str(wp_id))
        url = saveImageUrl(wp_id)
        save_img(url)


if __name__ == '__main__':
    min_wp_id = 100000000
    while (True):
        data = getJson(min_wp_id=min_wp_id, index=2)
        min_wp_id = data['min_wp_id']
        if (min_wp_id == -1):
            break
        for i in range(len(data['wallpapers'])):
            wp_id = data['wallpapers'][i]['wp_id']
            saveWpId(wp_id)
            url=saveImageUrl(wp_id)
            save_img(url,save_dir="2/")
    # wpid = r.lpop('imgid_list')
    # while (wpid != None):
    #     wp_id = int(wpid)
    #     print( "download--->" +str(wp_id))
    #     url = saveImageUrl(wp_id)
    #     save_img(url)


        # if __name__ == '__main__':
# min_wp_id = 1000000
#     while (True):
#         data = getJson(min_wp_id=min_wp_id, index=1)
#         min_wp_id = data['min_wp_id']
#         if (min_wp_id == -1):
#             break
#         for i in range(len(data['wallpapers'])):
#             wp_id = data['wallpapers'][i]['wp_id']
#             saveWpId(wp_id)

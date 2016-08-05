import json
import os
import random

import redis
import time
import urllib3
from bs4 import BeautifulSoup

host = 'http://bizhi.sogou.com'

# 黑名单，不爽的壁纸id放进这个数组
blacklist = [
    -1,
]


# 获取一个图片id
def getMinWpId(min_wp_id=100000000, index=1):
    conn = urllib3.connection_from_url(host)
    r = conn.request('GET', '/cate/getCate/' + str(index) + '/' + str(min_wp_id), headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})
    conn.close()
    html = r.data.decode("gbk")
    # print(html)
    data = json.loads(html)

    # for i in range(len(data['wallpapers'])):
    #     print(data['wallpapers'][i]['wp_id'])
    return int(data['min_wp_id'])


# 随机获取一个分类
def getCate():
    cate = [0, 1, 2, 8]
    return random.choice(cate)


def getImageUrl(wp_id):
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
        return src


def save_img(img_url, save_dir):
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
        return save_dir + img_name
    f = open(save_dir + img_name, 'wb')
    f.write(img_data)
    f.close()
    print("写入到--->" + save_dir + img_name)
    print("\n")
    return save_dir + img_name


def set_wallpaper(picpath):
    # curpath = commands.getstatusoutput('gsettings get org.gnome.desktop.background picture-uri')[1][1:-1]
    # if curpath == picpath:
    #     pass
    # else:
    os.system('gsettings set org.gnome.desktop.background picture-uri file://"%s"' % (picpath))
    # os.system('DISPLAY=:0 gsettings set org.gnome.desktop.background picture-uri "%s"' % (picpath))


def recordTmpIMG(picpath):
    tmpfile = open("/tmp/wallpapper_tmp.txt", 'wb')
    tmpfile.write(str.encode(picpath))
    tmpfile.close()


def removeTmpIMG():
    tmpfile = open("/tmp/wallpapper_tmp.txt")
    lastWallPapper = tmpfile.readline()
    tmpfile.close()
    os.system('rm -rf ' + lastWallPapper)


if __name__ == '__main__':
    # os.system('rm -rf /tmp/*.jpg')
    cate = getCate()
    max_wp_id = getMinWpId(min_wp_id=100000000, index=cate)
    random_wp_id = random.randint(1, max_wp_id)
    wp_id = getMinWpId(random_wp_id, cate)
    while ((wp_id == -1) or (wp_id in blacklist)):
        random_wp_id = random.randint(1, max_wp_id)
        wp_id = getMinWpId(random_wp_id, cate)

    url = getImageUrl(wp_id)
    file = save_img(url, "/tmp/")
    set_wallpaper(file)
    removeTmpIMG()
    recordTmpIMG(file)

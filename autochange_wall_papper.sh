#!/bin/sh
 #超时时间
    timeout=5

    #目标网站
    target=bizhi.sogou.com

    #获取响应状态码
    ret_code=`curl -I -s --connect-timeout $timeout $target -w %{http_code} | tail -n1`

    while [ "x$ret_code" != "x200" ];
    do
        echo '不通'
        sleep 5s
        ret_code=`curl -I -s --connect-timeout $timeout $target -w %{http_code} | tail -n1`
    done
    cd $HOME/pycharmprojects/sg_wp_spider
    git pull
    touch /tmp/wallpapper_tmp.txt
    while(true)
        do
            python3.5 $HOME/pycharmprojects/sg_wp_spider/autochangeWallPapper_core.py
            sleep 1m
        done


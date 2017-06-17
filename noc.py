#encoding:utf-8
import cookielib
import urllib
import urllib2
import os
from PIL import Image
from time import sleep
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

cookie = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)

data = {
    'return_url': 'comp_index.html',
    'user_name': 'lihangyu',
    'password': '123456',
    'valicode': ''}

put_login_url = 'http://j.noc.net.cn/login/check_data.html'
valcode_url = 'http://j.noc.net.cn/index.php/rand_func/valcode'

table = [0 if x < 160 else 1 for x in range(256)]
charset = ''
for i in range(10):
    charset += str(i)
for i in range(65, 65+26):
    charset += chr(i)
for i in range(97, 97+26):
    charset += chr(i)

start_time = dict(
    day_of_week='0-6',
    hour=8,
)


def job():
    while(1):
        response = opener.open(valcode_url)
        img = response.read()

        with open('./img.png', 'wb') as f:
            f.write(img)

        im = Image.open('./img.png')
        out = im.convert('L').point(table, '1')
        out.save('img.png')

        valicode = os.popen('tesseract img.png stdout -psm 8 -c tessedit_char_whitelist=%s' % charset).read()

        data['valicode'] = valicode
        login_data = urllib.urlencode(data)
        response = opener.open(put_login_url, login_data)

        sleep(1)
        if '登录成功' in response.read():
            break

    print '登录时间： ' + str(datetime.now())


scheduler = BlockingScheduler()
scheduler.add_job(job, 'cron', **start_time)
scheduler.start()
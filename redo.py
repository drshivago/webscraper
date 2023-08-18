import requests
from bs4 import BeautifulSoup
import shutil
import time
import os
import timedecorator
import re

home = "/Users/peterfile/Documents/webscraper/photos/redo"

counter = 0
timer = time.time()
session = requests.Session()
log_file = open("log.txt", 'r')

for j in log_file:
    try:
        if not re.search("-740.jpg*", j):

            sauce = j.split(' ')[0]
            r = session.get(sauce, timeout = 60)

            if r.status_code == 200:                                                    #if page exists

                soup = BeautifulSoup(r.text, features="html.parser")
                pics = soup.find(property="og:image")

                if pics == None:
                    continue
                res = session.get(pics["content"], stream = True, timeout = 60)
                pics_name = pics["content"].split('/')[-1]

                with open(os.path.join(home, pics_name), 'wb') as f:                    #Save file
                    shutil.copyfileobj(res.raw, f)
                    print(" Downloading: " + sauce + ' ' + pics_name)
                    counter += 1
                    print(sauce + ' ' + pics_name, file=open(os.path.join(home, "err_log.txt"), 'a+'))

            else:
                print("/",end="")
                if r.status_code != 404:
                    print(r.status_code, r.reason)
                    print(sauce,  r.status_code, r.reason, file=open(os.path.join(home, "err_log.txt"), 'a+'))
                    time.sleep(60)

    except Exception as e:
        print("\ncannot work " + sauce)
        print(f"Exception occured: {e}")

log_file.close()
print("time to pop champain!")                                                  #some how finised without error
print(counter)
print(timedecorator.time(int(time.time() - timer)))
print("\a")

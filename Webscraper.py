import requests
from bs4 import BeautifulSoup
import shutil
import time
import os
import timedecorator

link = "https://worldcosplay.net/photo/"
home = "/Users/peterfile/miniprograms/photos/"

with open('place.txt','r') as place:
    num = int(place.readline())
    file_num = int(place.readline())
    photo_saves = int(place.readline())

round = 1000                #number of download rounds per program run
set = 100                   #number of download atempts per round
retry = 0                   #don't fail twice
per_folder = 50050          #~number of photos saved per folder
sleep_time = 5
timer = time.time()
session = requests.Session()
path = os.path.join(home, str(file_num))

for i in range(0, round):

    for j in range(0, set):
        try:
            sauce = link + str(num + j)
            r = session.get(sauce, timeout = 60)

            if r.status_code == 200:                                                    #if page exists

                soup = BeautifulSoup(r.text, features="html.parser")
                pics = soup.find(property="og:image")

                if pics == None:
                    continue
                res = session.get(pics["content"], stream = True, timeout = 60)
                pics_name = pics["content"].split('/')[-1]

                with open(os.path.join(path, pics_name), 'wb') as f:                    #Save file
                    shutil.copyfileobj(res.raw, f)
                    photo_saves += 1
                    print(" Downloading: " + sauce + ' ' + pics_name)
                    print(sauce + ' ' + pics_name, file=open(os.path.join(path, "log.txt"), 'a'))

            else:
                print("/",end="")
                if r.status_code != 404:
                    print(sauce + ' ',  r.status_code, ' ' + r.reason, file=open(os.path.join(path, "log.txt"), 'a'))

        except Exception as e:
            print("\ncannot work " + sauce)
            print(f"Exception occured: {e}")

            if retry == num + j:
                with open('place.txt', 'w') as place:                           #failed 2 in row, save progress and quit
                    place.write(str(num) + '\n')
                    place.write(str(file_num) + '\n')
                    place.write(str(photo_saves))
                print("\a", "\a", "\a",)
                print("failed at: ", timedecorator.time(int(time.time() - timer)))
                exit()
            else:
                print("\a", "\a")                                               #stop and wait
                retry = num + j
                num -= 1
                time.sleep(1800)
                continue
    #r.close()
    #res.close()

    num += set
    if photo_saves >= per_folder:                                               #make new folder, use that

        file_num += 1
        path = os.path.join(home, str(file_num))
        os.mkdir(path)
        print("Download Log:", file=open(os.path.join(path, "log.txt"), 'w+'))
        print("Making new folder")
        photo_saves = 0

    with open('place.txt', 'w') as place:                                       #save progress
        place.write(str(num) + '\n')
        place.write(str(file_num) + '\n')
        place.write(str(photo_saves))
    print()
    print("Finished round: ", i+1)
    time.sleep(sleep_time)

print("time to pop champain!")                                                  #some how finised without error
print(timedecorator.time(int(time.time() - timer)))
print("\a")
